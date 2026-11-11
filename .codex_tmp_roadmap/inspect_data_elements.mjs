import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = "/Users/jjacks20/jjacks/Conversational-AI/Product Roadmap Use Cases-JJ.xlsx";
const previewPath = "/Users/jjacks20/jjacks/Conversational-AI/.codex_tmp_roadmap/source_data_elements.png";
const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));

const values = await workbook.inspect({
  kind: "region",
  sheetId: "Skills Questions v2",
  range: "A1:E11",
  tableMaxRows: 11,
  tableMaxCols: 5,
  tableMaxCellChars: 600,
  maxChars: 30000,
});
console.log(values.ndjson);

const styles = await workbook.inspect({
  kind: "computedStyle",
  sheetId: "Skills Questions v2",
  range: "E2:E11",
  maxChars: 12000,
});
console.log(styles.ndjson);

const preview = await workbook.render({ sheetName: "Skills Questions v2", range: "A1:E11", scale: 0.75, format: "png" });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
console.log(`PREVIEW ${previewPath}`);
