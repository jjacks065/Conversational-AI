import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const sourcePath = "/Users/jjacks20/jjacks/Conversational-AI/Minerva/_Data/compass-csr-chat-all-time.xlsx";
const previewPath = "/Users/jjacks20/jjacks/Conversational-AI/.codex-work/compass-monthly-split/source-preview.png";

const input = await FileBlob.load(sourcePath);
const workbook = await SpreadsheetFile.importXlsx(input);
const overview = await workbook.inspect({
  kind: "workbook,sheet,table,drawing,definedName",
  maxChars: 12000,
  tableMaxRows: 8,
  tableMaxCols: 20,
  tableMaxCellChars: 120,
});
console.log("OVERVIEW");
console.log(overview.ndjson);

const sheet = workbook.worksheets.getItemAt(0);
const used = sheet.getUsedRange(true);
const values = used.values;
const formulas = used.formulas;
console.log("DATA_SUMMARY");
console.log(JSON.stringify({
  sheetName: sheet.name,
  rowCount: values.length,
  columnCount: values[0]?.length ?? 0,
  headers: values[0] ?? [],
  firstRows: values.slice(0, 6),
  lastRows: values.slice(-5),
  formulaCellCount: formulas.flat().filter(Boolean).length,
  tableCount: sheet.tables.items.length,
  chartCount: sheet.charts.items.length,
}, null, 2));

const style = await workbook.inspect({
  kind: "computedStyle",
  sheetId: sheet.name,
  range: `A1:${String.fromCharCode(64 + Math.min(values[0]?.length ?? 1, 26))}${Math.min(values.length, 8)}`,
  maxChars: 8000,
});
console.log("STYLE");
console.log(style.ndjson);

const preview = await workbook.render({
  sheetName: sheet.name,
  range: `A1:${String.fromCharCode(64 + Math.min(values[0]?.length ?? 1, 26))}${Math.min(values.length, 20)}`,
  scale: 1,
  format: "png",
});
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
console.log(`PREVIEW ${previewPath}`);
