#!/usr/bin/env python3
"""Local runner for the Prod MLflow tracking v3 export notebook.

The Databricks notebook uses dbutils widgets/secrets and Spark display output.
This script keeps the same API pagination and feedback merge logic, then writes
local CSV/JSON files.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


BASE_URL_DEFAULT = (
    "https://apim-external-cub3dqcrgsdnebcb.a01.azurefd.net/benefits-prd/plan-list/"
)
MLFLOW_DATASET = "mlflow_tracking_v3"
FEEDBACK_DATASET = "benefitsquote_feedback"

OUTPUT_COLUMNS = [
    "tracking_id",
    "event_time",
    "facets_product_id",
    "effective_date",
    "user_id",
    "response_time_seconds",
    "retry_count",
    "request_text",
    "response_text",
    "feedback_type",
    "feedback_reason_code",
    "feedback_additional_comments",
]

MLFLOW_SOURCE_COLUMNS = [
    "tracking_id",
    "event_time",
    "facets_product_id",
    "effective_date",
    "user_id",
    "response_time_sec",
    "retry_count",
    "request_text",
    "response_text",
    "question_id",
    "session_id",
    "response_id",
    "user_name",
]

FEEDBACK_SOURCE_COLUMNS = [
    "response_id",
    "question_id",
    "session_id",
    "user_id",
    "user_name",
    "feedback_type",
    "reason_code",
    "additional_comments",
]


def parse_args() -> argparse.Namespace:
    today = dt.date.today().isoformat()
    parser = argparse.ArgumentParser(
        description="Export prod MLflow tracking v3 + feedback rows locally."
    )
    parser.add_argument("--base-url", default=os.getenv("BASE_URL", BASE_URL_DEFAULT))
    parser.add_argument("--start-date", default=os.getenv("START_DATE", today))
    parser.add_argument("--end-date", default=os.getenv("END_DATE", today))
    parser.add_argument("--limit", type=int, default=int(os.getenv("LIMIT", "10000")))
    parser.add_argument(
        "--include-failures",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("INCLUDE_FAILURES", "true").lower() in {"1", "true", "yes"},
    )
    parser.add_argument(
        "--subscription-key-env",
        default="PROD_APP_APIM_SUB_KEY",
        help="Environment variable containing the APIM subscription key.",
    )
    parser.add_argument(
        "--insecure-skip-tls-verify",
        action=argparse.BooleanOptionalAction,
        default=os.getenv("INSECURE_SKIP_TLS_VERIFY", "false").lower()
        in {"1", "true", "yes"},
        help="Disable TLS certificate verification for local corporate proxy testing.",
    )
    parser.add_argument(
        "--output-dir",
        default=os.getenv("OUTPUT_DIR", "prod-export-output"),
    )
    return parser.parse_args()


def request_json(
    base_url: str,
    subscription_key: str,
    params: dict[str, str],
    *,
    insecure_skip_tls_verify: bool = False,
    timeout: int = 120,
) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Ocp-Apim-Subscription-Key": subscription_key,
        },
    )
    context = ssl._create_unverified_context() if insecure_skip_tls_verify else None
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=context) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"APIM request failed with {exc.code}: {body[:1000]}") from exc


def fetch_page(
    *,
    base_url: str,
    subscription_key: str,
    dataset: str,
    event_date: dt.date,
    limit: int,
    include_failures: bool,
    insecure_skip_tls_verify: bool,
    cursor: str | None = None,
) -> dict[str, Any]:
    params = {
        "dataset": dataset,
        "event_date": event_date.isoformat(),
        "limit": str(limit),
    }
    if dataset == MLFLOW_DATASET:
        params["include_text"] = "true"
        if not include_failures:
            params["response_status"] = "success"
    if cursor:
        params["cursor"] = cursor
    return request_json(
        base_url,
        subscription_key,
        params,
        insecure_skip_tls_verify=insecure_skip_tls_verify,
    )


def collect_dataset(
    *,
    base_url: str,
    subscription_key: str,
    dataset: str,
    columns: list[str],
    start_date: dt.date,
    end_date: dt.date,
    limit: int,
    include_failures: bool,
    insecure_skip_tls_verify: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    collected_items: list[dict[str, Any]] = []
    day_summaries: list[dict[str, Any]] = []
    total_pages = 0
    day = start_date
    while day <= end_date:
        cursor = None
        day_rows = 0
        while True:
            payload = fetch_page(
                base_url=base_url,
                subscription_key=subscription_key,
                dataset=dataset,
                event_date=day,
                limit=limit,
                include_failures=include_failures,
                insecure_skip_tls_verify=insecure_skip_tls_verify,
                cursor=cursor,
            )
            if not isinstance(payload, dict) or "items" not in payload or "has_more" not in payload:
                preview = json.dumps(payload, ensure_ascii=False)[:1000]
                raise RuntimeError(
                    f"Unexpected response for dataset={dataset!r} day={day}: {preview}"
                )
            page_items = payload.get("items") or []
            trimmed_items = [
                {column: item.get(column) for column in columns}
                for item in page_items
                if isinstance(item, dict)
            ]
            collected_items.extend(trimmed_items)
            day_rows += len(trimmed_items)
            total_pages += 1
            if not payload.get("has_more"):
                break
            cursor = payload.get("next_cursor")
            if not cursor:
                raise RuntimeError(f"Missing next_cursor for dataset={dataset!r} day={day}.")
        day_summaries.append(
            {"dataset": dataset, "event_date": day.isoformat(), "row_count": day_rows}
        )
        print(f"{dataset} {day.isoformat()}: {day_rows} rows")
        day += dt.timedelta(days=1)
    return collected_items, day_summaries, total_pages


def feedback_join_key(item: dict[str, Any]) -> str | None:
    response_id = item.get("response_id")
    if response_id:
        return f"response:{response_id}"

    session_id = item.get("session_id")
    question_id = item.get("question_id")
    user_id = item.get("user_id")
    if session_id and question_id and user_id:
        return f"session:{session_id}|question:{question_id}|user:{user_id}"
    return None


def format_feedback(item: dict[str, Any]) -> dict[str, str | None]:
    feedback_type = item.get("feedback_type")

    reason_code = item.get("reason_code")
    if isinstance(reason_code, list):
        reason_text = ", ".join(str(v) for v in reason_code if v not in (None, ""))
    elif reason_code in (None, ""):
        reason_text = ""
    else:
        reason_text = str(reason_code)

    comment = item.get("additional_comments")
    return {
        "feedback_type": str(feedback_type) if feedback_type not in (None, "") else None,
        "feedback_reason_code": reason_text or None,
        "feedback_additional_comments": str(comment) if comment not in (None, "") else None,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    subscription_key = os.getenv(args.subscription_key_env, "").strip()
    if not subscription_key:
        print(f"Missing APIM key. Set {args.subscription_key_env}.", file=sys.stderr)
        return 2

    start_date = dt.date.fromisoformat(args.start_date)
    end_date = dt.date.fromisoformat(args.end_date)
    if end_date < start_date:
        print("end-date must be on or after start-date.", file=sys.stderr)
        return 2
    limit = max(1, min(args.limit, 10000))

    mlflow_items, mlflow_summaries, mlflow_pages = collect_dataset(
        base_url=args.base_url,
        subscription_key=subscription_key,
        dataset=MLFLOW_DATASET,
        columns=MLFLOW_SOURCE_COLUMNS,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        include_failures=args.include_failures,
        insecure_skip_tls_verify=args.insecure_skip_tls_verify,
    )
    feedback_items, feedback_summaries, feedback_pages = collect_dataset(
        base_url=args.base_url,
        subscription_key=subscription_key,
        dataset=FEEDBACK_DATASET,
        columns=FEEDBACK_SOURCE_COLUMNS,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        include_failures=args.include_failures,
        insecure_skip_tls_verify=args.insecure_skip_tls_verify,
    )

    feedback_lookup = {
        join_key: format_feedback(item)
        for item in feedback_items
        if (join_key := feedback_join_key(item))
    }
    merged_rows = [
        {
            "tracking_id": item.get("tracking_id"),
            "event_time": item.get("event_time"),
            "facets_product_id": item.get("facets_product_id"),
            "effective_date": item.get("effective_date"),
            "user_id": item.get("user_id"),
            "response_time_seconds": item.get("response_time_sec"),
            "retry_count": item.get("retry_count"),
            "request_text": item.get("request_text"),
            "response_text": item.get("response_text"),
            **(
                feedback_lookup.get(feedback_join_key(item))
                or {
                    "feedback_type": None,
                    "feedback_reason_code": None,
                    "feedback_additional_comments": None,
                }
            ),
        }
        for item in mlflow_items
    ]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "prod_mlflow_tracking_v3_export.csv"
    summary_path = output_dir / "prod_mlflow_tracking_v3_export_summary.json"

    summary = {
        "source_mode": "merged_tracking_feedback",
        "base_url": args.base_url,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "include_failures": args.include_failures,
        "row_count": len(merged_rows),
        "total_pages": {
            MLFLOW_DATASET: mlflow_pages,
            FEEDBACK_DATASET: feedback_pages,
        },
        "day_summaries": mlflow_summaries + feedback_summaries,
        "csv_path": str(csv_path),
    }

    write_csv(csv_path, merged_rows)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
