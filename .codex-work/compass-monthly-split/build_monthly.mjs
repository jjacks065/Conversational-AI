import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const dataDir = "/Users/jjacks20/jjacks/Conversational-AI/.codex-work/compass-monthly-split/data";
const outputDir = "/Users/jjacks20/jjacks/Conversational-AI/Minerva/_Data";
const previewDir = "/Users/jjacks20/jjacks/Conversational-AI/.codex-work/compass-monthly-split/previews";
const allMonths = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08"];
const months = process.env.COMPASS_MONTH ? [process.env.COMPASS_MONTH] : allMonths;
const chunkSize = 2500;

function restoreValue(value, columnIndex) {
  if (columnIndex === 0 && typeof value === "string") {
    return new Date(value);
  }
  if (typeof value === "string" && (value.startsWith("=") || value.startsWith("'="))) {
    return `'${value}`;
  }
  if (value && typeof value === "object" && value.__type === "datetime") {
    return new Date(`${value.value}Z`);
  }
  if (value && typeof value === "object" && value.__type === "date") {
    return new Date(`${value.value}T00:00:00Z`);
  }
  return value;
}

await fs.mkdir(previewDir, { recursive: true });
const results = [];

for (const month of months) {
  const payload = JSON.parse(await fs.readFile(path.join(dataDir, `${month}.json`), "utf8"));
  const workbook = Workbook.create();
  const sheet = workbook.worksheets.add(payload.sheet_name);
  sheet.showGridLines = true;

  sheet.getRangeByIndexes(0, 0, 1, payload.headers.length).values = [payload.headers];
  for (let start = 0; start < payload.rows.length; start += chunkSize) {
    const chunk = payload.rows
      .slice(start, start + chunkSize)
      .map((row) => row.map((value, columnIndex) => restoreValue(value, columnIndex)));
    sheet.getRangeByIndexes(start + 1, 0, chunk.length, payload.headers.length).values = chunk;
  }

  const usedRange = sheet.getRangeByIndexes(0, 0, payload.rows.length + 1, payload.headers.length);
  usedRange.format = {
    font: { name: "Aptos Narrow", size: 12 },
    horizontalAlignment: "left",
    verticalAlignment: "top",
    wrapText: true,
    rowHeight: 17,
  };
  sheet.getRange(`A2:A${payload.rows.length + 1}`).format.numberFormat = 'yyyy-mm-dd"T"hh:mm:ss.000"Z"';
  sheet.getRange(`C1:C${payload.rows.length + 1}`).format.numberFormat = "0";
  sheet.getRange(`E1:F${payload.rows.length + 1}`).format.numberFormat = "0";
  for (let rowIndex = 0; rowIndex < payload.rows.length; rowIndex += 1) {
    for (let columnIndex = 0; columnIndex < payload.rows[rowIndex].length; columnIndex += 1) {
      const value = payload.rows[rowIndex][columnIndex];
      if (value && typeof value === "object" && value.__type === "date") {
        sheet.getCell(rowIndex + 1, columnIndex).format.numberFormat = "m/d/yy";
      }
      if (value && typeof value === "object" && value.__type === "datetime") {
        sheet.getCell(rowIndex + 1, columnIndex).format.numberFormat = "m/d/yy h:mm";
      }
    }
  }
  for (const [column, width] of [
    ["A", 25.664], ["B", 25.664], ["C", 25.664], ["D", 25.664],
    ["E", 25.664], ["F", 25.664], ["G", 31.832], ["H", 35.5],
    ["I", 25.664], ["J", 25.664], ["K", 35.5],
  ]) {
    sheet.getRange(`${column}1:${column}${payload.rows.length + 1}`).format.columnWidth = width;
  }

  const outputPath = path.join(outputDir, `compass-csr-chat-queries-${month}.xlsx`);
  const output = await SpreadsheetFile.exportXlsx(workbook);
  await output.save(outputPath);

  const preview = await workbook.render({
    sheetName: payload.sheet_name,
    range: `A1:K${Math.min(payload.rows.length + 1, 18)}`,
    scale: 1,
    format: "png",
  });
  const previewPath = path.join(previewDir, `${month}.png`);
  await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

  const headCheck = await workbook.inspect({
    kind: "table",
    sheetId: payload.sheet_name,
    range: `A1:K${Math.min(payload.rows.length + 1, 6)}`,
    include: "values,formulas",
    tableMaxRows: 6,
    tableMaxCols: 11,
    maxChars: 5000,
  });
  results.push({
    month,
    outputPath,
    dataRows: payload.rows.length,
    totalRows: payload.rows.length + 1,
    previewPath,
    headCheck: headCheck.ndjson,
    errorCheck: "Deferred to full exported-workbook validation.",
  });
  console.log(`CREATED ${month} rows=${payload.rows.length} path=${outputPath}`);
}

await fs.writeFile(
  "/Users/jjacks20/jjacks/Conversational-AI/.codex-work/compass-monthly-split/build-results.json",
  JSON.stringify(results, null, 2),
);
console.log(JSON.stringify(results.map(({ month, outputPath, dataRows, totalRows, previewPath }) => ({
  month, outputPath, dataRows, totalRows, previewPath,
})), null, 2));
