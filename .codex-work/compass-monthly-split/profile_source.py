from collections import Counter
from datetime import date, datetime
from pathlib import Path
from openpyxl import load_workbook

SOURCE = Path("/Users/jjacks20/jjacks/Conversational-AI/Minerva/_Data/compass-csr-chat-all-time.xlsx")

workbook = load_workbook(SOURCE, read_only=True, data_only=False)
sheet = workbook[workbook.sheetnames[0]]
rows = sheet.iter_rows(values_only=True)
header = next(rows)
samples = []
last_rows = []
types = [Counter() for _ in header]
date_bounds = [[None, None] for _ in header]
nonempty = Counter()
row_count = 1

for row in rows:
    row_count += 1
    if len(samples) < 5:
        samples.append(row)
    last_rows.append(row)
    if len(last_rows) > 5:
        last_rows.pop(0)
    for index, value in enumerate(row):
        if value is None:
            continue
        nonempty[index] += 1
        types[index][type(value).__name__] += 1
        if isinstance(value, (datetime, date)):
            lower, upper = date_bounds[index]
            date_bounds[index][0] = value if lower is None or value < lower else lower
            date_bounds[index][1] = value if upper is None or value > upper else upper

print({
    "sheet": sheet.title,
    "dimensions": sheet.calculate_dimension(),
    "row_count": row_count,
    "column_count": len(header),
    "headers": header,
    "auto_filter": "A1:K31351 (from workbook defined name)",
    "freeze_panes": "None (from sheet XML)",
})
for index, name in enumerate(header):
    print({
        "column": index + 1,
        "header": name,
        "nonempty": nonempty[index],
        "types": dict(types[index]),
        "date_bounds": [str(value) if value is not None else None for value in date_bounds[index]],
    })
print("FIRST_ROWS")
for row in samples:
    print(row)
print("LAST_ROWS")
for row in last_rows:
    print(row)
