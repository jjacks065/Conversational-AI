import { Workbook } from "@oai/artifact-tool";

const workbook = Workbook.create();
workbook.worksheets.add("Help");
console.log(workbook.help("quotePrefix", {
  include: "index,examples,notes",
  maxChars: 8000,
}).ndjson);
