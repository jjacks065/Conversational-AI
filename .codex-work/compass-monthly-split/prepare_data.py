import json
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

SOURCE = Path("/Users/jjacks20/jjacks/Conversational-AI/Minerva/_Data/compass-csr-chat-all-time.xlsx")
OUTPUT_DIR = Path("/Users/jjacks20/jjacks/Conversational-AI/.codex-work/compass-monthly-split/data")
PACIFIC = ZoneInfo("America/Los_Angeles")


def json_value(value):
    if isinstance(value, datetime):
        return {"__type": "datetime", "value": value.isoformat()}
    if isinstance(value, date):
        return {"__type": "date", "value": value.isoformat()}
    return value


OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
workbook = load_workbook(SOURCE, read_only=True, data_only=False)
sheet = workbook[workbook.sheetnames[0]]
rows = sheet.iter_rows(values_only=True)
headers = list(next(rows))
groups = defaultdict(list)
utc_counts = Counter()
local_counts = Counter()
invalid_timestamps = []
local_bounds = {}
shifted_month_rows = []

for source_row_number, row in enumerate(rows, start=2):
    event_time = row[0]
    try:
        utc_time = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
        if utc_time.tzinfo is None:
            utc_time = utc_time.replace(tzinfo=timezone.utc)
    except (AttributeError, TypeError, ValueError):
        invalid_timestamps.append({"row": source_row_number, "value": event_time})
        continue
    local_time = utc_time.astimezone(PACIFIC)
    utc_month = utc_time.strftime("%Y-%m")
    local_month = local_time.strftime("%Y-%m")
    utc_counts[utc_month] += 1
    local_counts[local_month] += 1
    encoded = [json_value(value) for value in row]
    groups[local_month].append(encoded)
    if local_month not in local_bounds:
        local_bounds[local_month] = [local_time, local_time]
    else:
        local_bounds[local_month][0] = min(local_bounds[local_month][0], local_time)
        local_bounds[local_month][1] = max(local_bounds[local_month][1], local_time)
    if utc_month != local_month and len(shifted_month_rows) < 20:
        shifted_month_rows.append({
            "source_row": source_row_number,
            "event_time_utc": event_time,
            "event_time_pacific": local_time.isoformat(),
            "utc_month": utc_month,
            "pacific_month": local_month,
        })

manifest = {
    "source": str(SOURCE),
    "sheet_name": sheet.title,
    "headers": headers,
    "source_data_rows": sum(local_counts.values()),
    "invalid_timestamp_rows": invalid_timestamps,
    "utc_counts": dict(sorted(utc_counts.items())),
    "pacific_counts": dict(sorted(local_counts.items())),
    "pacific_bounds": {
        month: [lower.isoformat(), upper.isoformat()]
        for month, (lower, upper) in sorted(local_bounds.items())
    },
    "shifted_month_row_sample": shifted_month_rows,
}

for month, month_rows in sorted(groups.items()):
    payload = {
        "month": month,
        "sheet_name": sheet.title,
        "headers": headers,
        "rows": month_rows,
    }
    with (OUTPUT_DIR / f"{month}.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, separators=(",", ":"))

with (OUTPUT_DIR / "manifest.json").open("w", encoding="utf-8") as handle:
    json.dump(manifest, handle, ensure_ascii=False, indent=2)

print(json.dumps(manifest, ensure_ascii=False, indent=2))
