import fs from "node:fs/promises";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const inputPath = "/Users/jjacks20/jjacks/Conversational-AI/Minerva/Outputs/Compass-CSR-Chat-September-Month-In-Review-v4.pptx";
const previewDir = "/Users/jjacks20/jjacks/Conversational-AI/Minerva/tmp/slides/october-mtd/reference-preview";
await fs.mkdir(previewDir, { recursive: true });

const presentation = await PresentationFile.importPptx(await FileBlob.load(inputPath));
const inspection = await presentation.inspect({
  select: "$.slides[*].elements[*]",
  include: ["id", "name", "kind", "text", "position"],
});
await fs.writeFile(`${previewDir}/elements.ndjson`, inspection.ndjson, "utf8");

for (let index = 0; index < presentation.slides.items.length; index += 1) {
  const slide = presentation.slides.items[index];
  const png = await presentation.export({ slide, format: "png", scale: 1 });
  const bytes = new Uint8Array(await png.arrayBuffer());
  await fs.writeFile(`${previewDir}/slide-${String(index + 1).padStart(2, "0")}.png`, bytes);
}

console.log(JSON.stringify({ slideCount: presentation.slides.count, records: inspection.recordCount }));
