import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const workspaceDir = "/Users/jjacks20/jjacks/Conversational-AI";
const sourcePath = path.join(workspaceDir, "Minerva/Outputs/Compass-CSR-Chat-September-Month-In-Review-v2.pptx");
const buildDir = path.join(workspaceDir, ".codex-build/compass-september-review");
const finalPath = path.join(workspaceDir, "Minerva/Outputs/Compass-CSR-Chat-September-Month-In-Review-v4.pptx");
const skillDir = "/Users/jjacks20/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations";
const runtimePython = "/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";

await fs.mkdir(buildDir, { recursive: true });

const presentation = await PresentationFile.importPptx(await FileBlob.load(sourcePath));
const slide = presentation.slides.items[0];

function addRect(name, position, fill) {
  return slide.shapes.add({
    geometry: "rect",
    name,
    position,
    fill,
    line: { fill: "none", width: 0 },
  });
}

function addText(name, text, position, style) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name,
    position,
    fill: "none",
    line: { fill: "none", width: 0 },
  });
  shape.text = text;
  shape.text.style = {
    typeface: "Arial",
    autoFit: "none",
    wrap: "square",
    insets: { top: 0, right: 0, bottom: 0, left: 0 },
    ...style,
  };
  return shape;
}

addRect(
  "September User Movement Panel",
  { left: 349.33, top: 249.97, width: 287.6, height: 349.26 },
  "#FAF8F6",
);

addText(
  "September User Movement Title",
  "SEPTEMBER USER\nMOVEMENT",
  { left: 368.23, top: 266.07, width: 164, height: 36 },
  { fontSize: 16, bold: true, color: "#1A3563", lineSpacing: 0.94 },
);

addRect(
  "September Net User Badge",
  { left: 546.01, top: 264.32, width: 80, height: 29.4 },
  "#D9EBF8",
);
addText(
  "September Net User Badge Text",
  "+44 NET",
  { left: 550.31, top: 270.4, width: 71.39, height: 19.39 },
  { fontSize: 17, bold: true, color: "#00B050", alignment: "center" },
);

const rows = [
  { y: 327, value: "231", label: "LAPSED", detail: "17.9% of August users" },
  { y: 415, value: "227", label: "NEW", detail: "First seen in September" },
  { y: 503, value: "48", label: "REACQUIRED", detail: "Inactive in August" },
];

for (const [index, row] of rows.entries()) {
  addText(
    `User Movement Value ${index + 1}`,
    row.value,
    { left: 374, top: row.y, width: 68, height: 38 },
    { fontSize: 29, bold: true, color: "#1A3563", verticalAlignment: "middle" },
  );
  addText(
    `User Movement Label ${index + 1}`,
    row.label,
    { left: 451, top: row.y + 2, width: 158, height: 18 },
    { fontSize: 14, bold: true, color: "#33475C" },
  );
  addText(
    `User Movement Detail ${index + 1}`,
    row.detail,
    { left: 451, top: row.y + 23, width: 160, height: 24 },
    { fontSize: 11, color: "#788DA4" },
  );
}

for (const [index, y] of [399, 487].entries()) {
  addRect(
    `User Movement Divider ${index + 1}`,
    { left: 368.23, top: y, width: 250, height: 0.7 },
    "#D9E2EA",
  );
}

slide.speakerNotes.append(
  "\nUser movement: 231 August users were inactive in September, 227 users appeared for the first time, and 48 users returned after at least one inactive month. These movements produced net MAU growth of 44 users. Lapsed users are a monthly inactivity proxy, not confirmed account churn."
);

const after = await presentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  maxChars: 60000,
});
await fs.writeFile(path.join(buildDir, "churn-after.ndjson"), after.ndjson);

const candidatePath = path.join(buildDir, "candidate-churn.pptx");
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
    referenceSha256: "6d705f2a89e4a7e0130d43c17568a4d41a63d47a9d631f914a0c44a733c74a29",
  },
  verifyArtifactToolImport: true,
  receiptPath: path.join(buildDir, "validation-v4.json"),
});

const finalPresentation = await PresentationFile.importPptx(await FileBlob.load(finalPath));
const finalSlide = finalPresentation.slides.items[0];
const preview = await finalPresentation.export({ slide: finalSlide, format: "png", scale: 2 });
await fs.writeFile(path.join(buildDir, "final-slide-v4.png"), new Uint8Array(await preview.arrayBuffer()));
const finalInspect = await finalPresentation.inspect({
  kind: "slide,textbox,shape,image,notes,layout",
  maxChars: 60000,
});
await fs.writeFile(path.join(buildDir, "final-inspect-v4.ndjson"), finalInspect.ndjson);

console.log(JSON.stringify({ finalPath, result }, null, 2));
