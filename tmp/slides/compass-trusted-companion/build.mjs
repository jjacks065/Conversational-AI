import fs from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';

const root = '/Users/jjacks20/jjacks/Conversational-AI';
const scratch = `${root}/tmp/slides/compass-trusted-companion`;
const output = `${root}/Communications/outputs/019fd3d0-333d-75e2-ad43-c0e67aaccc4c/output.pptx`;
const template = `${root}/Communications/STL_Product_Pitch_Template.pptx`;
const deck = await PresentationFile.importPptx(await FileBlob.load(template));

const NAVY = '#20264D';
const DARK = '#222222';
const BLUE = '#3569BB';
const RED = '#F04455';

function addText(slide, name, copy, box, fontSize, opts = {}) {
  const shape = slide.shapes.add({ geometry: 'textbox', name, position: box, text: copy });
  shape.text.typeface = opts.typeface ?? 'Geist';
  shape.text.fontSize = fontSize;
  shape.text.color = opts.color ?? NAVY;
  shape.text.bold = opts.bold ?? false;
  shape.text.insets = 0;
  shape.text.autoFit = 'shrinkText';
  shape.text.verticalAlignment = 'middle';
  return shape;
}

function findText(slide, oldCopy) {
  const shape = slide.shapes.items.find((item) => String(item.text ?? '') === oldCopy);
  if (!shape) throw new Error(`Template text not found: ${oldCopy}`);
  return shape;
}

function updateText(slide, oldCopy, newCopy, fontSize, box) {
  const shape = findText(slide, oldCopy);
  shape.text = newCopy;
  if (fontSize) shape.text.fontSize = fontSize;
  shape.text.typeface = 'Geist';
  shape.text.color = fontSize && fontSize >= 20 ? NAVY : DARK;
  shape.text.autoFit = 'shrinkText';
  if (box) shape.position = box;
  return shape;
}

// Preserve the template slide as the concise product-detail page.
const detail = deck.slides.getItem(0);
updateText(detail, '[PILLAR] – [Product Module Name]', 'COMPASS – Trusted Health Companion', 40);
updateText(detail, '[Product name]  /  [Owner]  /  [Date]', 'Compass  /  Product Vision  /  October 2026', 16);
updateText(detail,
  '[Product] helps [target customer] achieve [primary outcome] through [how it works].',
  'Compass helps members make progress through care with grounded answers, permissioned outreach, and continuity across member-owned journeys.', 24);
updateText(detail,
  '[User / buyer] needs to [job or goal]. Today, [problem or workaround] costs [time, money, or risk].',
  'Members piece together benefits, claims, providers, medications, and care plans across disconnected channels. Every handoff can lose context and stall progress.', 17);
updateText(detail,
  '[Core capability] enables [key workflow]. Customers get started with [setup or integration].',
  'Surfaces (Member, CSR, Provider) → Spine (Auth, Agent Broker, AI Agents) → Brain (governed knowledge). Journeys carry goals, events, choices, next steps, and human help.', 17);
updateText(detail,
  'Deliver [measurable benefit] in [timeframe]. Compared with [alternative], we offer [difference] because [advantage].',
  'From answer engine to advocate, navigator, and companion: grounded resolution, visible progress, fewer restarts, and trust earned over time.', 17);
updateText(detail, 'Competitors', 'The alternative today', 21.3333333333);
updateText(detail, 'Known competing products',
  'Transaction-by-transaction portals, chats, and calls can address an immediate need without carrying the member’s goal, permissions, and context across care.', 17);
updateText(detail, 'The offer and next step', 'Roadmap and next step', 21.3333333333);
updateText(detail,
  'Which phase of the lifecycle are we in? Next step: [action] by [date]. Success: [metric]. Contact: [email / link].',
  'M0 journey foundation → Eligibility → Claims → Accumulators → Formulary → Provider Lookup → Scheduling. Validate each as a whole journey increment; rebaseline delivery scope before commitment.',
  17, { left: 98, top: 588, width: 1080, height: 60 });
detail.speakerNotes.text = 'Compass is a member-directed health companion. Member Progress and Earned Trust are top-line outcomes; grounded resolution and safe handling are quality gates. This pitch describes product direction, not confirmed delivery scope or dates. Provider-directed treatment decisions remain with the provider and member. Direct provider coordination requires authorization and technical availability; guided contact is the fallback. Caregiver, representative, and POA rights are deferred.';

// Duplicate the imported slide so its brand master, logo, rule, and footer stay intact.
const lead = detail.duplicate();
lead.moveTo(0);
for (const shape of [...lead.shapes.items]) shape.delete();

addText(lead, 'eyebrow', 'COMPASS  /  PERSONAL HEALTH ASSISTANT',
  { left: 98, top: 76, width: 980, height: 40 }, 21, { color: NAVY, bold: true });
addText(lead, 'compass-name', 'Compass',
  { left: 98, top: 174, width: 760, height: 82 }, 67, { color: NAVY, bold: true });
addText(lead, 'hero-tagline', 'Your care, carried forward.',
  { left: 98, top: 253, width: 1080, height: 70 }, 47, { color: NAVY, bold: true });
addText(lead, 'elevator-pitch',
  'A trusted health companion that starts with grounded answers and stays with members through what comes next—across benefits, providers, prescriptions, and care.',
  { left: 98, top: 347, width: 1080, height: 105 }, 28, { color: DARK, typeface: 'Geist Light' });

const cues = [
  ['Know what’s true.', 'Grounded answers'],
  ['Choose what’s next.', 'Member-directed journeys'],
  ['Keep moving.', 'Authorized, human-backed help'],
];
const cueLeft = [98, 467, 836];
for (let i = 0; i < cues.length; i += 1) {
  lead.shapes.add({ geometry: 'rect', name: `cue-rule-${i + 1}`,
    position: { left: cueLeft[i], top: 491, width: 58, height: 4 }, fill: RED,
    line: { fill: RED, width: 0 } });
  addText(lead, `cue-title-${i + 1}`, cues[i][0],
    { left: cueLeft[i], top: 509, width: 335, height: 39 }, 25, { color: NAVY, bold: true });
  addText(lead, `cue-subtitle-${i + 1}`, cues[i][1],
    { left: cueLeft[i], top: 548, width: 335, height: 34 }, 18,
    { color: DARK, typeface: 'Geist Light' });
}
addText(lead, 'choice-promise',
  'On demand when needed. Proactive by permission. In control, always.',
  { left: 98, top: 608, width: 1040, height: 42 }, 22, { color: BLUE });
addText(lead, 'lead-footer', 'Compass  /  Product Vision  /  October 2026',
  { left: 91, top: 663, width: 780, height: 28 }, 16, { color: BLUE });
lead.speakerNotes.text = 'Position Compass as a member-directed Personal Health Assistant, not merely a chatbot. Trust starts with accurate, source-grounded answers and is earned through continuity, visible progress, choice, and bounded human help. Member outreach requires opt-in; routine auto-approval can be granted later within an authorized journey. Compass never independently recommends treatment changes.';

// The discovery slide carries the six agreed questions into the pitch.
const discovery = detail.duplicate();
discovery.moveTo(2);
for (const shape of [...discovery.shapes.items]) shape.delete();
addText(discovery, 'discovery-title', 'Six questions to shape Compass',
  { left: 92, top: 72, width: 1100, height: 58 }, 40, { color: NAVY, bold: true });
addText(discovery, 'discovery-intro',
  'Start with member value and trust; let evidence define the boundaries for memory, action, and coordination.',
  { left: 98, top: 170, width: 1080, height: 58 }, 23,
  { color: NAVY, typeface: 'Geist Light' });

const questions = [
  {
    question: 'What first member moment should Compass help carry forward—not merely answer?',
    cue: 'Find the next meaningful step and member outcome.',
  },
  {
    question: 'What must a conversation do to earn trust?',
    cue: 'Test evidence, uncertainty, privacy, and correction.',
  },
  {
    question: 'What should Compass remember as a member-owned journey?',
    cue: 'Define goals, events, barriers, and member control.',
  },
  {
    question: 'When may Compass reach out or act?',
    cue: 'Set outreach, standing-approval, and fresh-consent limits.',
  },
  {
    question: 'How does continuity survive a change of surface or a human intervention?',
    cue: 'Carry context across Member, CSR, Provider, and human help.',
  },
  {
    question: 'What would show that Compass is becoming a trusted companion?',
    cue: 'Measure progress and trust alongside quality and safety.',
  },
];
const questionLeft = [98, 674];
const questionTop = [252, 365, 478];
for (let i = 0; i < questions.length; i += 1) {
  const column = i % 2;
  const row = Math.floor(i / 2);
  const left = questionLeft[column];
  const top = questionTop[row];
  if (row > 0) {
    discovery.shapes.add({ geometry: 'rect', name: `question-divider-${i + 1}`,
      position: { left, top: top - 10, width: 506, height: 1 }, fill: '#D8DCE8',
      line: { fill: '#D8DCE8', width: 0 } });
  }
  addText(discovery, `question-number-${i + 1}`, String(i + 1).padStart(2, '0'),
    { left, top: top + 2, width: 42, height: 32 }, 20, { color: RED, bold: true });
  addText(discovery, `question-${i + 1}`, questions[i].question,
    { left: left + 48, top, width: 458, height: 59 }, 20, { color: NAVY, bold: true });
  addText(discovery, `question-cue-${i + 1}`, questions[i].cue,
    { left: left + 48, top: top + 62, width: 458, height: 35 }, 16,
    { color: DARK, typeface: 'Geist Light' });
}
addText(discovery, 'discovery-footer', 'Compass  /  Product Discovery  /  October 2026',
  { left: 91, top: 663, width: 780, height: 28 }, 16, { color: BLUE });
discovery.speakerNotes.text = 'Use these questions in order to guide early discovery. First establish the member moment Compass should carry forward, then the evidence and control needed to earn trust. Next define member-owned journey memory and correction, granular permission for outreach and action, continuity across Member Chat, CSR Chat, Provider Chat, and temporary human intervention, and a measurement model for Member Progress and Earned Trust. Grounded Resolution Rate, Safe Handling, speed, sentiment, and engagement are supporting measures and guardrails. Begin member research with questions 1 and 2; do not assume more automation creates more trust.';

// The import/export path does not retain this master-only logo, so re-embed the
// source vector from the supplied template on all three slides.
const logoBytes = execFileSync('unzip', ['-p', template, 'ppt/media/image2.svg']);
const logoBlob = logoBytes.buffer.slice(logoBytes.byteOffset, logoBytes.byteOffset + logoBytes.byteLength);
for (const slide of [lead, detail, discovery]) {
  const logo = slide.images.add({ blob: logoBlob, fit: 'contain', alt: 'Stellarus logo' });
  logo.position = { left: 1129, top: 657, width: 113, height: 27 };
}

if (deck.slides.count !== 3) throw new Error(`Expected 3 slides, found ${deck.slides.count}`);
for (let i = 0; i < deck.slides.count; i += 1) {
  const slide = deck.slides.getItem(i);
  const png = await deck.export({ slide, format: 'png', scale: 1 });
  await fs.writeFile(`${scratch}/slide-${i + 1}.png`, new Uint8Array(await png.arrayBuffer()));
}
const inspect = await deck.inspect({ select: '$.slides[*].elements[*]', include: ['id', 'kind', 'text', 'position'] });
await fs.writeFile(`${scratch}/final-inspect.ndjson`, inspect.ndjson);
const lines = inspect.ndjson.split('\n').filter(Boolean);
console.log(`Editable elements: ${lines.length}`);
console.log(lines.filter((line) => line.includes('Compass') || line.includes('Your care') || line.includes('journey')));

await fs.mkdir(output.substring(0, output.lastIndexOf('/')), { recursive: true });
const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(output);
const reopened = await PresentationFile.importPptx(await FileBlob.load(output));
if (reopened.slides.count !== 3) throw new Error('Exported deck did not reopen with three slides');
const reopenedText = reopened.slides.items.flatMap((slide) =>
  slide.shapes.items.map((shape) => String(shape.text ?? ''))).join('\n');
for (const expected of ['Your care, carried forward.', 'Surfaces (Member, CSR, Provider)',
  'Roadmap and next step', 'Six questions to shape Compass',
  ...questions.map((item) => item.question)]) {
  if (!reopenedText.includes(expected)) throw new Error(`Exported deck is missing: ${expected}`);
}
console.log(`Saved: ${output}`);
