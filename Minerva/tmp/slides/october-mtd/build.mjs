import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const INPUT = "/Users/jjacks20/jjacks/Conversational-AI/Minerva/Outputs/Compass-CSR-Chat-September-Month-In-Review-v4.pptx";
const SCRATCH = "/Users/jjacks20/jjacks/Conversational-AI/Minerva/tmp/slides/october-mtd";
const PREVIEW = path.join(SCRATCH, "preview", "slide-01.png");
const INSPECT = path.join(SCRATCH, "verification", "elements.ndjson");
const LOOP_LOG = path.join(SCRATCH, "verification", "render_verify_loops.ndjson");
const OUTPUT_DIR = "/Users/jjacks20/jjacks/Conversational-AI/Minerva/Outputs/Compass-CSR-Chat-October-MTD-Month-In-Review";
const OUTPUT = path.join(OUTPUT_DIR, "output.pptx");

const NAVY = "#1D3964";
const LIGHT_BLUE = "#8ABCE2";
const GRID = "#D8E2EC";
const TRANSPARENT = "#FFFFFF00";
const FONT = "Arial";

await fs.mkdir(path.dirname(PREVIEW), { recursive: true });
await fs.mkdir(path.dirname(INSPECT), { recursive: true });
await fs.mkdir(OUTPUT_DIR, { recursive: true });

const presentation = await PresentationFile.importPptx(await FileBlob.load(INPUT));
if (presentation.slides.count !== 1) throw new Error(`Expected one reference slide, found ${presentation.slides.count}`);
const slide = presentation.slides.getItem(0);

const before = await presentation.inspect({
  select: "$.slides[*].elements[*]",
  include: ["id", "name", "kind", "text", "position"],
});
const records = before.records;

function byName(name) {
  const matches = records.filter((record) => record.name === name);
  if (matches.length !== 1) throw new Error(`Expected one element named ${name}, found ${matches.length}`);
  return matches[0];
}

function byText(text) {
  const matches = records.filter((record) => record.text === text);
  if (matches.length !== 1) throw new Error(`Expected one element with text ${JSON.stringify(text)}, found ${matches.length}`);
  return matches[0];
}

function replaceTextByName(name, nextText) {
  const record = byName(name);
  presentation.resolve(record.id).text.replace(record.text, nextText);
}

function replaceText(oldText, nextText) {
  const record = byText(oldText);
  presentation.resolve(record.id).text.replace(oldText, nextText);
}

function deleteByNames(names) {
  presentation.delete(names.map((name) => byName(name).id));
}

function resizeByName(name, changes) {
  const record = byName(name);
  presentation.resolve(record.id).position = { ...record.position, ...changes };
}

replaceText("September review\nSep 1 - 30, 2026", "October MTD review\nOct 1 - 26, 2026");
replaceText("MONTHLY RETENTION", "MTD RETENTION");
replaceText("82.1%", "77.2%");
replaceText("August users returned", "September users returned");
replaceText("116,857", "146,086");
replaceText("1,071", "1,652");
replaceText("queries per day (30d avg)", "weekday queries/day (avg)");
replaceText("328", "501");
replaceText("daily active agents (30d avg)", "weekday active users P50");
replaceText("11 sec", "9 sec");

const partial = slide.shapes.add({
  geometry: "roundRect",
  position: { left: 37.33, top: 184, width: 112, height: 24 },
  fill: "#A7D4F2",
  line: { style: "solid", fill: TRANSPARENT, width: 0 },
});
partial.name = "October Partial Month Badge";
partial.text = "PARTIAL MONTH";
partial.text.typeface = FONT;
partial.text.fontSize = 10;
partial.text.bold = true;
partial.text.color = NAVY;
partial.text.alignment = "center";
partial.text.verticalAlignment = "middle";
partial.text.insets = { left: 4, right: 4, top: 2, bottom: 2 };

replaceTextByName("September User Movement Title", "OCTOBER MTD\nUSER MOVEMENT");
replaceTextByName("September Net User Badge Text", "+208 NET");
resizeByName("September Net User Badge", { left: 538, width: 88 });
resizeByName("September Net User Badge Text", { left: 542, width: 80 });
replaceTextByName("User Movement Value 1", "304");
replaceTextByName("User Movement Label 1", "INACTIVE MTD");
replaceTextByName("User Movement Detail 1", "22.8% of September users");
replaceTextByName("User Movement Value 2", "447");
replaceTextByName("User Movement Detail 2", "First seen in October");
replaceTextByName("User Movement Value 3", "65");
replaceTextByName("User Movement Detail 3", "Inactive in September");

replaceTextByName("TextBox 60", "+15.6%");
replaceTextByName("TextBox 66", "Jul");
replaceTextByName("TextBox 70", "Aug");
replaceTextByName("TextBox 74", "Sep");
replaceTextByName("TextBox 78", "Oct");
replaceTextByName("TextBox 67", "+52.8%");
replaceTextByName("TextBox 71", "+16.6%");
replaceTextByName("TextBox 75", "+3.5%");
replaceTextByName("TextBox 79", "+15.6%");

replaceTextByName("TextBox 84", "+8.9%");
replaceTextByName("TextBox 90", "Jul");
replaceTextByName("TextBox 94", "Aug");
replaceTextByName("TextBox 98", "Sep");
replaceTextByName("TextBox 102", "Oct");
replaceTextByName("TextBox 91", "+54.0%");
replaceTextByName("TextBox 95", "+28.0%");
replaceTextByName("TextBox 99", "+2.4%");
replaceTextByName("TextBox 103", "+8.9%");

deleteByNames([
  "Rectangle 61", "Rectangle 62", "Rectangle 63",
  "Rectangle 64", "Rectangle 68", "Rectangle 72", "Rectangle 76",
  "TextBox 65", "TextBox 69", "TextBox 73", "TextBox 77",
  "Rectangle 85", "Rectangle 86", "Rectangle 87",
  "Rectangle 88", "Rectangle 92", "Rectangle 96", "Rectangle 100",
  "TextBox 89", "TextBox 93", "TextBox 97", "TextBox 101",
]);

function addColumnChart({ left, values, max, majorUnit, name }) {
  const chart = slide.charts.add("bar", {
    position: { left, top: 318, width: 242, height: 188 },
    categories: ["Jul", "Aug", "Sep", "Oct"],
    series: [{
      name: "Users",
      values,
      fill: LIGHT_BLUE,
      points: [{ idx: 3, fill: NAVY }],
      dataLabels: {
        showValue: true,
        position: "outEnd",
        numberFormatCode: "#,##0",
        textStyle: { typeface: FONT, fontSize: 9, bold: true, fill: NAVY },
      },
    }],
    barOptions: { direction: "column", grouping: "clustered", gapWidth: 60 },
    hasLegend: false,
    xAxis: {
      visible: false,
      majorGridlines: null,
      line: { style: "solid", fill: TRANSPARENT, width: 0 },
    },
    yAxis: {
      visible: true,
      min: 0,
      max,
      majorUnit,
      tickLabelPosition: "none",
      line: { style: "solid", fill: TRANSPARENT, width: 0 },
      majorGridlines: { style: "solid", fill: GRID, width: 1 },
      minorGridlines: null,
    },
    chartLine: { style: "solid", fill: TRANSPARENT, width: 0 },
    plotAreaFill: TRANSPARENT,
    plotAreaLine: { style: "solid", fill: TRANSPARENT, width: 0 },
  });
  chart.name = name;
}

addColumnChart({ left: 672, values: [1106, 1290, 1335, 1543], max: 1750, majorUnit: 500, name: "Monthly Active Users Native Chart" });
addColumnChart({ left: 972, values: [696, 891, 913, 994], max: 1150, majorUnit: 300, name: "Weekly Active Users Native Chart" });

slide.speakerNotes.setText([
  "October MTD snapshot through October 26, 2026 at 9:46 a.m. Pacific; October 26 is a partial day.",
  "Weekday DAU and query averages exclude Sundays and report Saturdays separately because Saturday business hours are limited.",
  "Inactive MTD is provisional and must not be interpreted as final October churn.",
  "New means first observed since historical coverage began in April 2026.",
  "Monthly active users use cleaned production IDs. Weekly active users P50 uses the established rolling seven-day convention.",
]);

const after = await presentation.inspect({
  select: "$.slides[*].elements[*]",
  include: ["id", "name", "kind", "text", "position"],
});
await fs.writeFile(INSPECT, after.ndjson, "utf8");

const png = await presentation.export({ slide, format: "png", scale: 1 });
await fs.writeFile(PREVIEW, new Uint8Array(await png.arrayBuffer()));

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUTPUT);

const existingLog = await fs.readFile(LOOP_LOG, "utf8").catch(() => "");
const loop = existingLog.split(/\r?\n/).filter(Boolean).length + 1;
if (loop > 3) throw new Error("Render/verify/fix loop cap exceeded");
await fs.appendFile(LOOP_LOG, JSON.stringify({ loop, preview: PREVIEW, output: OUTPUT }) + "\n", "utf8");

console.log(JSON.stringify({ output: OUTPUT, preview: PREVIEW, inspect: INSPECT, loop, elements: after.recordCount }));
