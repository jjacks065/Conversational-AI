import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = "/Users/jjacks20/jjacks/Conversational-AI";
const sourcePath = path.join(workspaceDir, "Minerva/Background/Montly-Update-Slide.pptx");
const buildDir = path.join(workspaceDir, ".codex-build/compass-september-review");
const outputDir = path.join(workspaceDir, "Minerva/Outputs");
const finalPath = path.join(outputDir, "Compass-CSR-Chat-September-Month-In-Review-v2.pptx");
const skillDir = "/Users/jjacks20/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations";
const runtimePython = "/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";

await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });

const presentation = await PresentationFile.importPptx(await FileBlob.load(sourcePath));
const before = await presentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  maxChars: 50000,
});
await fs.writeFile(path.join(buildDir, "before.ndjson"), before.ndjson);
const records = before.ndjson.trim().split("\n").map((line) => JSON.parse(line));

function recordByName(name) {
  const record = records.find((item) => item.name === name);
  if (!record) throw new Error(`Missing template object: ${name}`);
  return record;
}

function objectByName(name) {
  return presentation.resolve(recordByName(name).id);
}

function replaceText(name, nextText) {
  const record = recordByName(name);
  const object = presentation.resolve(record.id);
  object.text.replace(record.text, nextText);
}

function setPosition(name, position) {
  const object = objectByName(name);
  object.position = { ...object.position, ...position };
}

objectByName("TextBox 4").text.replace("Five months in", "September review");
objectByName("TextBox 4").text.replace("Apr 7 - Sept 14, 2026", "Sep 1 - 30, 2026");
replaceText("TextBox 6", "82.1%");
replaceText("TextBox 7", "August users returned");

replaceText("TextBox 9", "116,857");
replaceText("TextBox 12", "1,071");
replaceText("TextBox 15", "328");
replaceText("TextBox 18", "11 sec");
replaceText("TextBox 19", "median answer time");

replaceText("TextBox 60", "+3.4%");
replaceText("TextBox 84", "+2.4%");
replaceText("TextBox 81", "WEEKLY ACTIVE\nUSERS P50");

const mau = [
  { bar: "Rectangle 64", valueBox: "TextBox 65", monthBox: "TextBox 66", changeBox: "TextBox 67", value: 724, month: "Jun", change: "+28.8%" },
  { bar: "Rectangle 68", valueBox: "TextBox 69", monthBox: "TextBox 70", changeBox: "TextBox 71", value: 1107, month: "Jul", change: "+52.9%" },
  { bar: "Rectangle 72", valueBox: "TextBox 73", monthBox: "TextBox 74", changeBox: "TextBox 75", value: 1292, month: "Aug", change: "+16.7%" },
  { bar: "Rectangle 76", valueBox: "TextBox 77", monthBox: "TextBox 78", changeBox: "TextBox 79", value: 1336, month: "Sep", change: "+3.4%" },
];
const mauBaseline = 499.14;
const mauScale = 153.83 / 1290;
for (const item of mau) {
  const height = item.value * mauScale;
  const top = mauBaseline - height;
  setPosition(item.bar, { top, height });
  setPosition(item.valueBox, { top: top - 23.1 });
  replaceText(item.valueBox, item.value.toLocaleString("en-US"));
  replaceText(item.monthBox, item.month);
  replaceText(item.changeBox, item.change);
}

const wau = [
  { bar: "Rectangle 88", valueBox: "TextBox 89", monthBox: "TextBox 90", changeBox: "TextBox 91", value: 452, month: "Jun", change: "+37.8%" },
  { bar: "Rectangle 92", valueBox: "TextBox 93", monthBox: "TextBox 94", changeBox: "TextBox 95", value: 696, month: "Jul", change: "+54.0%" },
  { bar: "Rectangle 96", valueBox: "TextBox 97", monthBox: "TextBox 98", changeBox: "TextBox 99", value: 891, month: "Aug", change: "+28.0%" },
  { bar: "Rectangle 100", valueBox: "TextBox 101", monthBox: "TextBox 102", changeBox: "TextBox 103", value: 913, month: "Sep", change: "+2.4%" },
];
const wauBaseline = 499.14;
const wauScale = 154.92 / 895;
for (const item of wau) {
  const height = item.value * wauScale;
  const top = wauBaseline - height;
  setPosition(item.bar, { top, height });
  setPosition(item.valueBox, { top: top - 23.1 });
  replaceText(item.valueBox, item.value.toLocaleString("en-US"));
  replaceText(item.monthBox, item.month);
  replaceText(item.changeBox, item.change);
}

const slide = presentation.slides.items[0];
slide.speakerNotes.textFrame.setText([
  "September review covers Sep 1-30, 2026 in Pacific time.",
  "September: 32,114 human interactions, 1,336 monthly active users, 82.1% month-over-month retention, rolling seven-day WAU P50 of 913, and median answer time of 11 seconds.",
  "Daily queries and daily active agents use calendar-day averages to preserve the prior slide definition. Business-hours-adjusted DAU P50/P95 are 458/520 using weekday weight 1.0, Saturday 0.25, and Sunday 0.",
  "The cumulative interaction count excludes explicitly labeled smoke/test accounts across Apr 7-Sep 30.",
  "Sources: Minerva/_Data/Monthly-Extracts/compass-csr-chat-queries-2026-04.xlsx through compass-csr-chat-queries-2026-09.xlsx.",
]);
slide.speakerNotes.setVisible(true);

const after = await presentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  maxChars: 50000,
});
await fs.writeFile(path.join(buildDir, "after.ndjson"), after.ndjson);

const candidatePath = path.join(buildDir, "candidate.pptx");
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);

const { finalizePresentation } = await import(
  pathToFileURL(path.join(skillDir, "container_tools/artifact_tool_utils.mjs")).href
);

const result = await finalizePresentation({
  explicitTotalSlideCount: 1,
  requiredNativeTableOwnerSlides: [],
  requiredNativeChartOwnerSlides: [],
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: runtimePython,
  integrityValidatorPath: path.join(skillDir, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(skillDir, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: [
    "--expected-slide-size-emu", "12192000,6858000",
    "--validate-bullet-geometry",
    "--validate-heading-fit",
  ],
  fontPolicy: {
    basis: "reference",
    families: ["Arial"],
    referencePath: sourcePath,
    referenceSha256: "d3c366aaf077e20d10df990f9d1ca5e389db4b8a4ed216b72f9f391523e9ee80",
  },
  verifyArtifactToolImport: true,
  receiptPath: path.join(buildDir, "validation-v2.json"),
});

const finalPresentation = await PresentationFile.importPptx(await FileBlob.load(finalPath));
const finalSlide = finalPresentation.slides.items[0];
const preview = await finalPresentation.export({ slide: finalSlide, format: "png", scale: 2 });
await fs.writeFile(path.join(buildDir, "final-slide.png"), new Uint8Array(await preview.arrayBuffer()));
const finalLayout = await finalSlide.export({ format: "layout" });
await fs.writeFile(path.join(buildDir, "final-slide.layout.json"), await finalLayout.text());
const finalInspect = await finalPresentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  maxChars: 50000,
});
await fs.writeFile(path.join(buildDir, "final-inspect.ndjson"), finalInspect.ndjson);

console.log(JSON.stringify({ finalPath, result }, null, 2));
