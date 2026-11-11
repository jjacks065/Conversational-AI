import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Test");
sheet.getRange("A1:A3").format.numberFormat = "@";
sheet.getRange("A1:A3").values = [
  ["Event Time"],
  ["2026-04-07T17:04:27.457Z"],
  ["'2026-04-07T17:04:27.457Z"],
];
sheet.getRange("B1:B2").format.numberFormat = "@";
sheet.getRange("B1:B2").values = [["Formula-like"], ["'=SUM(1,2)"]];
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save("/Users/jjacks20/jjacks/Conversational-AI/.codex-work/compass-monthly-split/test-text-export.xlsx");
