import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workspace = "/Users/jjacks20/jjacks/Conversational-AI";
const inputPath = path.join(workspace, "Product Roadmap Use Cases-JJ.xlsx");
const previewDir = path.join(workspace, ".codex_tmp_roadmap", "previews_before");
await fs.mkdir(previewDir, { recursive: true });

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));
const sheetInspection = await workbook.inspect({
  kind: "sheet",
  include: "id,name",
  maxChars: 12000,
});
console.log("SHEETS");
console.log(sheetInspection.ndjson);

for (const sheetName of ["Skills Questions v2", "Compass CSR chat"]) {
  const region = await workbook.inspect({
    kind: "region",
    sheetId: sheetName,
    range: "A1:Z300",
    maxChars: 40000,
    tableMaxRows: 300,
    tableMaxCols: 26,
    tableMaxCellChars: 500,
  });
  console.log(`REGION ${sheetName}`);
  console.log(region.ndjson);

  const styles = await workbook.inspect({
    kind: "computedStyle",
    sheetId: sheetName,
    range: "A1:J25",
    maxChars: 12000,
  });
  console.log(`STYLES ${sheetName}`);
  console.log(styles.ndjson);
}

for (let i = 0; i < workbook.worksheets.items.length; i += 1) {
  const sheet = workbook.worksheets.getItemAt(i);
  const sheetName = sheet.name;
  try {
    const preview = await workbook.render({
      sheetName,
      autoCrop: "all",
      scale: 1,
      format: "png",
    });
    const safeName = `${String(i + 1).padStart(2, "0")}_${sheetName.replace(/[^a-z0-9_-]+/gi, "_")}.png`;
    await fs.writeFile(path.join(previewDir, safeName), new Uint8Array(await preview.arrayBuffer()));
    console.log(`RENDERED ${sheetName} -> ${safeName}`);
  } catch (error) {
    console.log(`RENDER_FAILED ${sheetName}: ${error.message}`);
  }
}
