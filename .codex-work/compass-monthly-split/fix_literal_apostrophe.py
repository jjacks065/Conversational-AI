from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile
from xml.etree import ElementTree as ET

TARGET = Path("/Users/jjacks20/jjacks/Conversational-AI/Minerva/_Data/compass-csr-chat-queries-2026-07.xlsx")
CELL_REFERENCE = "G13096"
EXPECTED_EXPORTED = "''=member covered in new york for school?"
EXPECTED_SOURCE = "'=member covered in new york for school?"
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS = {"x": MAIN_NS}

with ZipFile(TARGET, "r") as source_zip:
    worksheet = ET.fromstring(source_zip.read("xl/worksheets/sheet1.xml"))
    cell = worksheet.find(f".//x:c[@r='{CELL_REFERENCE}']", NS)
    if cell is None or cell.get("t") != "str":
        raise RuntimeError(f"Expected inline string cell at {CELL_REFERENCE}")
    value_node = cell.find("x:v", NS)
    current = value_node.text or ""
    if current != EXPECTED_EXPORTED:
        raise RuntimeError(f"Unexpected exported value at {CELL_REFERENCE}: {current!r}")
    value_node.text = EXPECTED_SOURCE
    updated_worksheet = ET.tostring(worksheet, encoding="utf-8", xml_declaration=True)

    with NamedTemporaryFile(prefix="compass-2026-07-", suffix=".xlsx", dir=TARGET.parent, delete=False) as temp_handle:
        temp_path = Path(temp_handle.name)
    try:
        with ZipFile(temp_path, "w", compression=ZIP_DEFLATED) as output_zip:
            for entry in source_zip.infolist():
                content = updated_worksheet if entry.filename == "xl/worksheets/sheet1.xml" else source_zip.read(entry.filename)
                output_zip.writestr(entry, content)
        temp_path.replace(TARGET)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise

print(f"Corrected {CELL_REFERENCE} in {TARGET}")
