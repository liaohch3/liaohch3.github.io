#!/usr/bin/env python3
"""Check whether the live usage metrics summary has been refreshed recently."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


USER_AGENT = "liaohch3-usage-metrics-freshness-monitor/1.0"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check the freshness of the live usage metrics summary JSON."
    )
    parser.add_argument(
        "--summary-url",
        default="https://liaohch3.com/data/ai-usage-summary.json",
        help="Live summary JSON URL to validate.",
    )
    parser.add_argument(
        "--threshold-hours",
        type=float,
        default=2.0,
        help="Maximum allowed age in hours before the summary is considered stale.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=15.0,
        help="HTTP timeout for the summary fetch.",
    )
    parser.add_argument(
        "--github-output",
        type=Path,
        default=None,
        help="Optional path to append GitHub Actions step outputs.",
    )
    return parser.parse_args()


def write_outputs(path: Path | None, values: dict[str, str]) -> None:
    if path is None:
        return

    with path.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            safe = str(value).replace("\r", " ").replace("\n", " ").strip()
            handle.write(f"{key}={safe}\n")


def parse_timestamp(raw: str) -> datetime:
    value = raw.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


def fetch_summary(url: str, timeout_seconds: float) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        return json.load(response)


def main() -> int:
    args = parse_args()
    checked_at = datetime.now(tz=timezone.utc)
    threshold_minutes = int(args.threshold_hours * 60)

    outputs = {
        "summary_url": args.summary_url,
        "checked_at": checked_at.isoformat().replace("+00:00", "Z"),
        "threshold_minutes": str(threshold_minutes),
        "status": "unknown",
        "stale": "true",
        "updated_at": "unknown",
        "age_minutes": "unknown",
        "detail": "",
    }

    try:
        payload = fetch_summary(args.summary_url, args.timeout_seconds)
        raw_updated_at = payload.get("updated_at")
        if not raw_updated_at:
            raise ValueError("summary payload is missing updated_at")

        updated_at = parse_timestamp(str(raw_updated_at))
        age_seconds = max((checked_at - updated_at).total_seconds(), 0)
        age_minutes = int(round(age_seconds / 60))
        is_stale = age_seconds > args.threshold_hours * 3600

        outputs.update(
            {
                "status": "stale" if is_stale else "fresh",
                "stale": "true" if is_stale else "false",
                "updated_at": updated_at.isoformat().replace("+00:00", "Z"),
                "age_minutes": str(age_minutes),
                "detail": (
                    f"live summary age is {age_minutes} minutes"
                    if not is_stale
                    else f"live summary age is {age_minutes} minutes, above the {threshold_minutes}-minute threshold"
                ),
            }
        )
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        outputs.update(
            {
                "status": "error",
                "stale": "true",
                "detail": f"failed to fetch or parse the live summary: {exc}",
            }
        )

    write_outputs(args.github_output, outputs)

    print(
        json.dumps(
            {
                "summary_url": outputs["summary_url"],
                "checked_at": outputs["checked_at"],
                "updated_at": outputs["updated_at"],
                "age_minutes": outputs["age_minutes"],
                "threshold_minutes": outputs["threshold_minutes"],
                "status": outputs["status"],
                "stale": outputs["stale"] == "true",
                "detail": outputs["detail"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
