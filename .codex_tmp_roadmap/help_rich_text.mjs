import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbook = await SpreadsheetFile.importXlsx(
  await FileBlob.load("/Users/jjacks20/jjacks/Conversational-AI/Product Roadmap Use Cases-JJ.xlsx"),
);
console.log(workbook.help("*", { search: "richText|textRuns|text run|font.bold", include: "index,examples,notes", maxChars: 8000 }).ndjson);
