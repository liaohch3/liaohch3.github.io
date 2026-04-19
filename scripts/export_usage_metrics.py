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


def fetch_rows() -> list[dict]:
    client = bigquery.Client(project=PROJECT_ID)
    end = datetime.now(tz=timezone.utc)
    start = end - timedelta(hours=24)
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


def main() -> None:
    rows = [_validate_row(row) for row in fetch_rows()]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_path = OUTPUT_DIR / "ai-usage-summary.json"
    hourly_path = OUTPUT_DIR / "ai-usage-hourly.json"

    summary_path.write_text(
        json.dumps(_validate_summary(build_summary(rows)), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    hourly_path.write_text(
        json.dumps({"rows": rows}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
