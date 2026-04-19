from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

from google.cloud import bigquery


PROJECT_ID = "liaohch3-trace-vault-260419"
TABLE_ID = f"{PROJECT_ID}.usage_public.hourly_metrics_v1"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "static" / "data"
HEATMAP_DAYS = 7 * 18
ROW_KEYS = {
    "hour",
    "source",
    "client",
    "model",
    "requests",
    "success_requests",
    "failed_requests",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "avg_latency_ms",
    "window_label",
    "generated_at",
}
SUMMARY_KEYS = {
    "window_hours",
    "updated_at",
    "requests",
    "success_requests",
    "failed_requests",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "avg_latency_ms",
    "sources",
    "clients",
    "source_breakdown",
    "client_breakdown",
}
DAILY_KEYS = {
    "date",
    "total_tokens",
}
INSIGHT_KEYS = {
    "updated_at",
    "model_mix",
    "hour_mix",
}
MODEL_MIX_KEYS = {"model", "total_tokens", "share"}
HOUR_MIX_KEYS = {"hour", "total_tokens"}


def _validate_row(row: dict) -> dict:
    unexpected = set(row) - ROW_KEYS
    missing = ROW_KEYS - set(row)
    if unexpected or missing:
        raise ValueError(f"public hourly row failed allowlist scan: unexpected={unexpected} missing={missing}")
    return {
        "hour": str(row["hour"]),
        "source": str(row["source"]),
        "client": str(row["client"]),
        "model": str(row["model"]),
        "requests": int(row["requests"]),
        "success_requests": int(row["success_requests"]),
        "failed_requests": int(row["failed_requests"]),
        "input_tokens": int(row["input_tokens"]),
        "output_tokens": int(row["output_tokens"]),
        "total_tokens": int(row["total_tokens"]),
        "avg_latency_ms": float(row["avg_latency_ms"]),
        "window_label": str(row["window_label"]),
        "generated_at": str(row["generated_at"]),
    }


def _validate_summary(summary: dict) -> dict:
    unexpected = set(summary) - SUMMARY_KEYS
    missing = SUMMARY_KEYS - set(summary)
    if unexpected or missing:
        raise ValueError(f"public summary failed allowlist scan: unexpected={unexpected} missing={missing}")
    return {
        "window_hours": int(summary["window_hours"]),
        "updated_at": str(summary["updated_at"]) if summary["updated_at"] else None,
        "requests": int(summary["requests"]),
        "success_requests": int(summary["success_requests"]),
        "failed_requests": int(summary["failed_requests"]),
        "input_tokens": int(summary["input_tokens"]),
        "output_tokens": int(summary["output_tokens"]),
        "total_tokens": int(summary["total_tokens"]),
        "avg_latency_ms": float(summary["avg_latency_ms"]),
        "sources": [str(item) for item in summary["sources"]],
        "clients": [str(item) for item in summary["clients"]],
        "source_breakdown": {
            str(key): int(value) for key, value in dict(summary["source_breakdown"]).items()
        },
        "client_breakdown": {
            str(key): int(value) for key, value in dict(summary["client_breakdown"]).items()
        },
    }


def _validate_daily_row(row: dict) -> dict:
    unexpected = set(row) - DAILY_KEYS
    missing = DAILY_KEYS - set(row)
    if unexpected or missing:
        raise ValueError(f"public daily row failed allowlist scan: unexpected={unexpected} missing={missing}")
    return {
        "date": str(row["date"]),
        "total_tokens": int(row["total_tokens"]),
    }


def _validate_insights(payload: dict) -> dict:
    unexpected = set(payload) - INSIGHT_KEYS
    missing = INSIGHT_KEYS - set(payload)
    if unexpected or missing:
        raise ValueError(
            f"public insights failed allowlist scan: unexpected={unexpected} missing={missing}"
        )

    model_mix = []
    for row in payload["model_mix"]:
        unexpected = set(row) - MODEL_MIX_KEYS
        missing = MODEL_MIX_KEYS - set(row)
        if unexpected or missing:
            raise ValueError(
                f"public model mix failed allowlist scan: unexpected={unexpected} missing={missing}"
            )
        model_mix.append(
            {
                "model": str(row["model"]),
                "total_tokens": int(row["total_tokens"]),
                "share": int(row["share"]),
            }
        )

    hour_mix = []
    for row in payload["hour_mix"]:
        unexpected = set(row) - HOUR_MIX_KEYS
        missing = HOUR_MIX_KEYS - set(row)
        if unexpected or missing:
            raise ValueError(
                f"public hour mix failed allowlist scan: unexpected={unexpected} missing={missing}"
            )
        hour_mix.append(
            {
                "hour": str(row["hour"]),
                "total_tokens": int(row["total_tokens"]),
            }
        )

    return {
        "updated_at": str(payload["updated_at"]) if payload["updated_at"] else None,
        "model_mix": model_mix,
        "hour_mix": hour_mix,
    }


def fetch_rows(window_hours: int) -> list[dict]:
    client = bigquery.Client(project=PROJECT_ID)
    end = datetime.now(tz=timezone.utc)
    start = end - timedelta(hours=window_hours)
    sql = f"""
    WITH latest_rows AS (
      SELECT
        hour,
        source,
        client,
        model,
        requests,
        success_requests,
        failed_requests,
        input_tokens,
        output_tokens,
        total_tokens,
        avg_latency_ms,
        window_label,
        generated_at,
        ROW_NUMBER() OVER (
          PARTITION BY hour, source, client, model, window_label
          ORDER BY generated_at DESC
        ) AS row_num
      FROM `{TABLE_ID}`
      WHERE hour >= @start AND hour <= @end
    )
    SELECT
      hour,
      source,
      client,
      model,
      requests,
      success_requests,
      failed_requests,
      input_tokens,
      output_tokens,
      total_tokens,
      avg_latency_ms,
      window_label,
      generated_at
    FROM latest_rows
    WHERE row_num = 1
    ORDER BY hour, source, client, model
    """
    params = [
        bigquery.ScalarQueryParameter("start", "TIMESTAMP", start),
        bigquery.ScalarQueryParameter("end", "TIMESTAMP", end),
    ]
    job = client.query(sql, job_config=bigquery.QueryJobConfig(query_parameters=params))
    rows: list[dict] = []
    for row in job.result():
        rows.append(
            {
                "hour": row["hour"].isoformat().replace("+00:00", "Z"),
                "source": row["source"],
                "client": row["client"],
                "model": row["model"],
                "requests": row["requests"],
                "success_requests": row["success_requests"],
                "failed_requests": row["failed_requests"],
                "input_tokens": row["input_tokens"],
                "output_tokens": row["output_tokens"],
                "total_tokens": row["total_tokens"],
                "avg_latency_ms": float(row["avg_latency_ms"]),
                "window_label": row["window_label"],
                "generated_at": row["generated_at"].isoformat().replace("+00:00", "Z"),
            }
        )
    return rows


def build_summary(rows: list[dict]) -> dict:
    generated_at = max((row["generated_at"] for row in rows), default=None)
    source_counts = Counter(row["source"] for row in rows)
    client_counts = Counter(row["client"] for row in rows)
    return {
        "window_hours": 24,
        "updated_at": generated_at,
        "requests": sum(int(row["requests"]) for row in rows),
        "success_requests": sum(int(row["success_requests"]) for row in rows),
        "failed_requests": sum(int(row["failed_requests"]) for row in rows),
        "input_tokens": sum(int(row["input_tokens"]) for row in rows),
        "output_tokens": sum(int(row["output_tokens"]) for row in rows),
        "total_tokens": sum(int(row["total_tokens"]) for row in rows),
        "avg_latency_ms": round(
            sum(float(row["avg_latency_ms"]) for row in rows) / len(rows), 2
        )
        if rows
        else 0,
        "sources": sorted(source_counts),
        "clients": sorted(client_counts),
        "source_breakdown": dict(source_counts),
        "client_breakdown": dict(client_counts),
    }


def build_daily_rows(rows: list[dict]) -> list[dict]:
    daily_totals: dict[str, int] = {}
    for row in rows:
        date = str(row["hour"])[:10]
        daily_totals[date] = daily_totals.get(date, 0) + int(row["total_tokens"])

    dates = sorted(daily_totals)
    if not dates:
        return []

    end = datetime.fromisoformat(f"{dates[-1]}T00:00:00+00:00").date()
    start = end - timedelta(days=HEATMAP_DAYS - 1)
    rows_out = []
    cursor = start
    while cursor <= end:
        key = cursor.isoformat()
        rows_out.append({"date": key, "total_tokens": daily_totals.get(key, 0)})
        cursor += timedelta(days=1)
    return rows_out


def build_insights(rows: list[dict]) -> dict:
    generated_at = max((row["generated_at"] for row in rows), default=None)

    model_totals = Counter()
    hour_totals = Counter()
    for row in rows:
        tokens = int(row["total_tokens"])
        model_totals[str(row["model"])] += tokens
        hour_totals[str(row["hour"])[11:16]] += tokens

    total_model_tokens = sum(model_totals.values()) or 1
    model_mix = [
        {
            "model": model,
            "total_tokens": total_tokens,
            "share": round(total_tokens * 100 / total_model_tokens),
        }
        for model, total_tokens in model_totals.most_common(6)
    ]
    hour_mix = [
        {"hour": hour, "total_tokens": total_tokens}
        for hour, total_tokens in sorted(hour_totals.items())
    ]
    return {
        "updated_at": generated_at,
        "model_mix": model_mix,
        "hour_mix": hour_mix,
    }


def main() -> None:
    recent_rows = [_validate_row(row) for row in fetch_rows(window_hours=24)]
    long_rows = [_validate_row(row) for row in fetch_rows(window_hours=24 * HEATMAP_DAYS)]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_path = OUTPUT_DIR / "ai-usage-summary.json"
    hourly_path = OUTPUT_DIR / "ai-usage-hourly.json"
    daily_path = OUTPUT_DIR / "ai-usage-daily.json"
    insight_path = OUTPUT_DIR / "ai-usage-insights.json"

    summary_path.write_text(
        json.dumps(_validate_summary(build_summary(recent_rows)), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    hourly_path.write_text(
        json.dumps({"rows": recent_rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    daily_path.write_text(
        json.dumps({"rows": [_validate_daily_row(row) for row in build_daily_rows(long_rows)]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    insight_path.write_text(
        json.dumps(_validate_insights(build_insights(long_rows)), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
