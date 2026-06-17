import fs from "node:fs/promises";
import path from "node:path";
import { execFileSync } from "node:child_process";

const sourcePath = "/Users/jjacks20/jjacks/Conversational-AI/Multi-Tenant-Platform/SDK-Timeline.mmd";
const outDir = "/Users/jjacks20/jjacks/Conversational-AI/Multi-Tenant-Platform/outputs/sdk-timeline-slide";
const workDir = "/Users/jjacks20/jjacks/Conversational-AI/Multi-Tenant-Platform/tmp/slides/sdk-timeline-slide/pptx-src";
const pptxPath = path.join(outDir, "output.pptx");
const inspectPath = "/Users/jjacks20/jjacks/Conversational-AI/Multi-Tenant-Platform/tmp/slides/sdk-timeline-slide/inspect.json";

const slideW = 1280;
const slideH = 720;
const emu = 9525;

function parseMermaidGantt(text) {
  const lines = text.split(/\r?\n/);
  let title = "Timeline";
  let section = "";
  const tasks = [];
  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line === "gantt" || line.startsWith("dateFormat") || line.startsWith("axisFormat")) continue;
    if (line.startsWith("title ")) {
      title = line.replace(/^title\s+/, "").trim();
      continue;
    }
    if (line.startsWith("section ")) {
      section = line.replace(/^section\s+/, "").trim();
      continue;
    }
    const match = line.match(/^(.*?)\s*:\s*([^,]+),\s*(\d{4}-\d{2}-\d{2}),\s*(\d{4}-\d{2}-\d{2})\s*$/);
    if (match) {
      tasks.push({
        section,
        label: match[1].trim(),
        id: match[2].trim(),
        start: match[3],
        end: match[4],
      });
    }
  }
  return { title, tasks };
}

const source = await fs.readFile(sourcePath, "utf8");
const { title, tasks } = parseMermaidGantt(source);
if (!tasks.length) throw new Error("No gantt tasks parsed from SDK-Timeline.mmd");

const dates = tasks.flatMap((task) => [task.start, task.end]).map((date) => new Date(`${date}T00:00:00Z`));
const start = new Date(Math.min(...dates));
const end = new Date(Math.max(...dates));
const totalDays = Math.max(1, (end - start) / 86400000);

const sectionColors = new Map([
  ["SDK Foundation", "#0EA5A4"],
  ["Helm Platform <dark prod>", "#D97706"],
  ["Help Platform <live>", "#16A34A"],
]);

function colorFor(section, idx) {
  const fallback = ["#2563EB", "#7C3AED", "#0891B2", "#475569"];
  return sectionColors.get(section) || fallback[idx % fallback.length];
}

function shortDate(date) {
  const d = new Date(`${date}T00:00:00Z`);
  return d.toLocaleDateString("en-US", { timeZone: "UTC", month: "short", day: "numeric" });
}

function rangeLabel(startDate, endDate) {
  const s = new Date(startDate);
  const e = new Date(endDate);
  const sameYear = s.getUTCFullYear() === e.getUTCFullYear();
  const startText = s.toLocaleDateString("en-US", { timeZone: "UTC", month: "long", day: "numeric" });
  const endText = e.toLocaleDateString("en-US", { timeZone: "UTC", month: "long", day: "numeric", year: "numeric" });
  return sameYear ? `${startText} - ${endText}` : `${startText}, ${s.getUTCFullYear()} - ${endText}`;
}

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function xywh(left, top, width, height) {
  return `<a:xfrm><a:off x="${Math.round(left * emu)}" y="${Math.round(top * emu)}"/><a:ext cx="${Math.round(width * emu)}" cy="${Math.round(height * emu)}"/></a:xfrm>`;
}

let id = 2;
const inspect = [];

function shape({ left, top, width, height, fill = "FFFFFF", line = "FFFFFF", radius = false }) {
  const geom = radius ? "roundRect" : "rect";
  return `<p:sp><p:nvSpPr><p:cNvPr id="${id++}" name="Shape ${id}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>${xywh(left, top, width, height)}<a:prstGeom prst="${geom}"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="${fill.replace("#", "")}"/></a:solidFill><a:ln w="9525"><a:solidFill><a:srgbClr val="${line.replace("#", "")}"/></a:solidFill></a:ln></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/><a:p/></p:txBody></p:sp>`;
}

function textBox({ text, left, top, width, height, size = 20, color = "0F172A", bold = false, align = "l", role = "text" }) {
  inspect.push({ kind: "textbox", slide: 1, role, text, textChars: text.length, textLines: text.split("\n").length, bbox: { left, top, width, height } });
  const weight = bold ? `<a:b/>` : "";
  const paras = text.split("\n").map((line) => `<a:p><a:pPr algn="${align}"/><a:r><a:rPr lang="en-US" sz="${size * 100}"><a:solidFill><a:srgbClr val="${color.replace("#", "")}"/></a:solidFill>${weight}<a:latin typeface="${bold ? "Poppins" : "Lato"}"/></a:rPr><a:t>${esc(line)}</a:t></a:r></a:p>`).join("");
  return `<p:sp><p:nvSpPr><p:cNvPr id="${id++}" name="${esc(role)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>${xywh(left, top, width, height)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" anchor="mid"><a:spAutoFit/></a:bodyPr><a:lstStyle/>${paras}</p:txBody></p:sp>`;
}

function line({ x1, y1, x2, y2, color = "CBD5E1", width = 2 }) {
  return `<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="${id++}" name="Line ${id}"/><p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr><a:xfrm><a:off x="${Math.round(x1 * emu)}" y="${Math.round(y1 * emu)}"/><a:ext cx="${Math.round((x2 - x1) * emu)}" cy="${Math.round((y2 - y1) * emu)}"/></a:xfrm><a:prstGeom prst="line"><a:avLst/></a:prstGeom><a:ln w="${Math.round(width * 12700)}"><a:solidFill><a:srgbClr val="${color.replace("#", "")}"/></a:solidFill></a:ln></p:spPr></p:cxnSp>`;
}

const parts = [];
parts.push(shape({ left: 0, top: 0, width: slideW, height: slideH, fill: "F8FAFC", line: "F8FAFC" }));
parts.push(shape({ left: 0, top: 0, width: slideW, height: 84, fill: "0F172A", line: "0F172A" }));
parts.push(textBox({ text: title, left: 48, top: 18, width: 760, height: 40, size: 25, color: "FFFFFF", bold: true, role: "title" }));
parts.push(textBox({ text: rangeLabel(start, end), left: 930, top: 28, width: 300, height: 28, size: 15, color: "FFFFFF", bold: true, align: "r", role: "date-range" }));

parts.push(shape({ left: 48, top: 108, width: 1184, height: 556, fill: "FFFFFF", line: "E2E8F0", radius: true }));

const axisX = 338;
const axisY = 162;
const axisW = 790;
parts.push(textBox({ text: shortDate(start.toISOString().slice(0, 10)), left: axisX - 38, top: 126, width: 90, height: 22, size: 12, color: "475569", align: "c", role: "axis-label" }));
parts.push(textBox({ text: shortDate(end.toISOString().slice(0, 10)), left: axisX + axisW - 52, top: 126, width: 104, height: 22, size: 12, color: "475569", bold: true, align: "c", role: "axis-label" }));
parts.push(line({ x1: axisX, y1: axisY, x2: axisX + axisW, y2: axisY, color: "CBD5E1", width: 2 }));

const tickDates = [...new Set(tasks.flatMap((task) => [task.start, task.end]))].sort();
for (const date of tickDates) {
  const days = (new Date(`${date}T00:00:00Z`) - start) / 86400000;
  const x = axisX + (days / totalDays) * axisW;
  parts.push(line({ x1: x, y1: 150, x2: x, y2: 560, color: date === end.toISOString().slice(0, 10) ? "86EFAC" : "E2E8F0", width: date === end.toISOString().slice(0, 10) ? 2 : 1 }));
  parts.push(textBox({ text: shortDate(date), left: x - 35, top: 564, width: 70, height: 20, size: 10, color: "64748B", align: "c", role: "tick-label" }));
}

let y = 206;
let lastSection = "";
tasks.forEach((task, index) => {
  const color = colorFor(task.section, index);
  if (task.section !== lastSection) {
    parts.push(textBox({ text: task.section, left: 72, top: y - 2, width: 216, height: 22, size: 12, color: color.replace("#", ""), bold: true, role: "section" }));
    lastSection = task.section;
  }
  const taskStartDays = (new Date(`${task.start}T00:00:00Z`) - start) / 86400000;
  const taskEndDays = (new Date(`${task.end}T00:00:00Z`) - start) / 86400000;
  const barX = axisX + (taskStartDays / totalDays) * axisW;
  const barW = Math.max(24, ((taskEndDays - taskStartDays) / totalDays) * axisW);
  parts.push(shape({ left: barX, top: y, width: barW, height: 28, fill: color, line: color, radius: true }));
  parts.push(textBox({ text: task.label, left: 72, top: y + 25, width: 230, height: 30, size: 10, color: "334155", role: "task-label" }));
  parts.push(textBox({ text: `${shortDate(task.start)} - ${shortDate(task.end)}`, left: barX + 8, top: y + 1, width: Math.max(120, barW - 16), height: 26, size: 10, color: "FFFFFF", bold: true, align: "c", role: "task-dates" }));
  y += 72;
});

const groupedSections = [...new Set(tasks.map((task) => task.section))];
const legendY = 608;
groupedSections.forEach((section, index) => {
  const left = 92 + index * 330;
  const color = colorFor(section, index);
  parts.push(shape({ left, top: legendY, width: 18, height: 18, fill: color, line: color, radius: true }));
  parts.push(textBox({ text: section, left: left + 28, top: legendY - 3, width: 270, height: 24, size: 11, color: "334155", bold: true, role: "legend" }));
});

const slideXml = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="${slideW * emu}" cy="${slideH * emu}"/><a:chOff x="0" y="0"/><a:chExt cx="${slideW * emu}" cy="${slideH * emu}"/></a:xfrm></p:grpSpPr>${parts.join("")}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>`;

const files = {
  "[Content_Types].xml": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>`,
  "_rels/.rels": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>`,
  "docProps/core.xml": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>${esc(title)}</dc:title><dc:creator>Codex</dc:creator><cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">2026-06-04T00:00:00Z</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">2026-06-04T00:00:00Z</dcterms:modified></cp:coreProperties>`,
  "docProps/app.xml": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft PowerPoint</Application><PresentationFormat>On-screen Show (16:9)</PresentationFormat><Slides>1</Slides></Properties>`,
  "ppt/presentation.xml": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst><p:sldSz cx="${slideW * emu}" cy="${slideH * emu}" type="wide"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>`,
  "ppt/_rels/presentation.xml.rels": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/></Relationships>`,
  "ppt/slides/slide1.xml": slideXml,
  "ppt/slides/_rels/slide1.xml.rels": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>`,
  "ppt/slideLayouts/slideLayout1.xml": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>`,
  "ppt/slideLayouts/_rels/slideLayout1.xml.rels": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>`,
  "ppt/slideMasters/slideMaster1.xml": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>`,
  "ppt/slideMasters/_rels/slideMaster1.xml.rels": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>`,
  "ppt/theme/theme1.xml": `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="MemChat"><a:themeElements><a:clrScheme name="MemChat"><a:dk1><a:srgbClr val="0F172A"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="334155"/></a:dk2><a:lt2><a:srgbClr val="F8FAFC"/></a:lt2><a:accent1><a:srgbClr val="0EA5A4"/></a:accent1><a:accent2><a:srgbClr val="2563EB"/></a:accent2><a:accent3><a:srgbClr val="D97706"/></a:accent3><a:accent4><a:srgbClr val="16A34A"/></a:accent4><a:accent5><a:srgbClr val="64748B"/></a:accent5><a:accent6><a:srgbClr val="CBD5E1"/></a:accent6><a:hlink><a:srgbClr val="2563EB"/></a:hlink><a:folHlink><a:srgbClr val="7C3AED"/></a:folHlink></a:clrScheme><a:fontScheme name="MemChat"><a:majorFont><a:latin typeface="Poppins"/></a:majorFont><a:minorFont><a:latin typeface="Lato"/></a:minorFont></a:fontScheme><a:fmtScheme name="MemChat"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>`,
};

await fs.rm(workDir, { recursive: true, force: true });
for (const [file, content] of Object.entries(files)) {
  const dest = path.join(workDir, file);
  await fs.mkdir(path.dirname(dest), { recursive: true });
  await fs.writeFile(dest, content);
}
await fs.writeFile(inspectPath, JSON.stringify({ sourcePath, title, tasks, inspect }, null, 2));
await fs.rm(pptxPath, { force: true });
execFileSync("zip", ["-qr", pptxPath, "."], { cwd: workDir });
console.log(pptxPath);
