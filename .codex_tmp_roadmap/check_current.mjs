import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workspace = "/Users/jjacks20/jjacks/Conversational-AI";
const inputPath = path.join(workspace, "Product Roadmap Use Cases-JJ.xlsx");
const previewDir = path.join(workspace, ".codex_tmp_roadmap", "current_destination");
await fs.mkdir(previewDir, { recursive: true });

const stat = await fs.stat(inputPath);
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));
const names = workbook.worksheets.items.map((sheet) => sheet.name);
console.log(JSON.stringify({ modified: stat.mtime.toISOString(), size: stat.size, sheets: names }, null, 2));

const candidates = names.filter((name) => /compass.*csr|csr.*compass|chat-jj/i.test(name));
for (const sheetName of candidates) {
  const sheet = workbook.worksheets.getItem(sheetName);
  const used = sheet.getUsedRange();
  const address = used?.address ?? "A1:M15";
  const region = await workbook.inspect({
    kind: "region",
    sheetId: sheetName,
    range: address,
    maxChars: 20000,
    tableMaxRows: 100,
    tableMaxCols: 20,
    tableMaxCellChars: 600,
  });
  console.log(`DESTINATION ${sheetName}`);
  console.log(region.ndjson);

  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  const outPath = path.join(previewDir, `${sheetName.replace(/[^a-z0-9_-]+/gi, "_")}.png`);
  await fs.writeFile(outPath, new Uint8Array(await preview.arrayBuffer()));
  console.log(`PREVIEW ${outPath}`);
}
