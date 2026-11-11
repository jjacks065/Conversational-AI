import json
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

SOURCE = Path("/Users/jjacks20/jjacks/Conversational-AI/Minerva/_Data/compass-csr-chat-all-time.xlsx")
OUTPUT_DIR = SOURCE.parent
MONTHS = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08"]
PACIFIC = ZoneInfo("America/Los_Angeles")


def local_month(event_time):
    parsed = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(PACIFIC).strftime("%Y-%m")


def event_time_key(value):
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    elif isinstance(value, datetime):
        parsed = value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)
    else:
        return (type(value).__name__, value)
    return ("event_time", parsed.astimezone(timezone.utc).isoformat(timespec="milliseconds"))


def canonical(value, column_index):
    if column_index == 0:
        return event_time_key(value)
    if isinstance(value, datetime):
        return ("datetime", value.isoformat())
    if isinstance(value, date):
        return ("date", value.isoformat())
    return (type(value).__name__, value)


def canonical_row(row):
    return tuple(canonical(value, index) for index, value in enumerate(row))


source_workbook = load_workbook(SOURCE, read_only=True, data_only=False)
source_sheet = source_workbook[source_workbook.sheetnames[0]]
source_rows = source_sheet.iter_rows(values_only=True)
source_header = tuple(next(source_rows))
expected = defaultdict(list)
for row in source_rows:
    expected[local_month(row[0])].append(canonical_row(row))

results = []
total_output_rows = 0
for month in MONTHS:
    output_path = OUTPUT_DIR / f"compass-csr-chat-queries-{month}.xlsx"
    workbook = load_workbook(output_path, read_only=True, data_only=False)
    sheet = workbook[workbook.sheetnames[0]]
    rows = sheet.iter_rows(values_only=False)
    header = tuple(cell.value for cell in next(rows))
    actual = []
    wrong_month_rows = []
    invalid_event_time_rows = []
    formula_cells = 0
    error_cells = 0
    for row_number, cells in enumerate(rows, start=2):
        row = tuple(cell.value for cell in cells)
        formula_cells += sum(cell.data_type == "f" for cell in cells)
        error_cells += sum(cell.data_type == "e" for cell in cells)
        if not isinstance(row[0], (str, datetime)):
            if len(invalid_event_time_rows) < 10:
                invalid_event_time_rows.append({"row": row_number, "event_time": row[0], "type": type(row[0]).__name__})
        else:
            if isinstance(row[0], datetime):
                event_time = row[0].replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
            else:
                event_time = row[0]
            if local_month(event_time) != month and len(wrong_month_rows) < 10:
                wrong_month_rows.append({"row": row_number, "event_time": str(row[0]), "local_month": local_month(event_time)})
        actual.append(canonical_row(row))
    mismatches = []
    for offset, (expected_row, actual_row) in enumerate(zip(expected[month], actual), start=2):
        if expected_row != actual_row:
            mismatches.append({"row": offset, "expected": expected_row, "actual": actual_row})
            if len(mismatches) >= 3:
                break
    total_output_rows += len(actual)
    results.append({
        "month": month,
        "path": str(output_path),
        "sheet": sheet.title,
        "dimensions": sheet.calculate_dimension(force=True),
        "header_matches": header == source_header,
        "expected_data_rows": len(expected[month]),
        "actual_data_rows": len(actual),
        "row_count_matches": len(expected[month]) == len(actual),
        "content_order_matches": len(expected[month]) == len(actual) and not mismatches,
        "mismatch_samples": mismatches,
        "invalid_event_time_rows": invalid_event_time_rows,
        "wrong_pacific_month_rows": wrong_month_rows,
        "formula_cells": formula_cells,
        "error_cells": error_cells,
    })

report = {
    "source_data_rows": sum(len(rows) for rows in expected.values()),
    "output_data_rows": total_output_rows,
    "all_rows_reconciled": total_output_rows == sum(len(rows) for rows in expected.values()),
    "all_checks_pass": all(
        item["header_matches"]
        and item["row_count_matches"]
        and item["content_order_matches"]
        and not item["invalid_event_time_rows"]
        and not item["wrong_pacific_month_rows"]
        and item["formula_cells"] == 0
        and item["error_cells"] == 0
        for item in results
    ),
    "files": results,
}
print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
