import fs from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const root = '/Users/jjacks20/jjacks/Conversational-AI';
const scratch = path.join(root, 'tmp/slides/compass-bsc-roadmap-reconciled');
const outDir = path.join(root, 'outputs/01a1b226-71b1-7090-817e-da53a9413d41/source-reconciled');
const runtimeModules = '/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
await fs.mkdir(scratch, { recursive: true });
await fs.mkdir(path.join(scratch, 'preview'), { recursive: true });
await fs.mkdir(outDir, { recursive: true });
await fs.symlink(runtimeModules, path.join(scratch, 'node_modules')).catch(e => { if(e.code !== 'EEXIST') throw e; });
const { FileBlob, PresentationFile } = await import('@oai/artifact-tool');

if(process.argv.includes('--render-existing')) {
 const p=await PresentationFile.importPptx(await FileBlob.load(path.join(outDir,'output.pptx')));
 for(let i=0;i<p.slides.count;i++) {
  const png=await p.export({slide:p.slides.getItem(i),format:'png',scale:1});
  await fs.writeFile(path.join(scratch,'preview',`exported-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 }
 console.log('Exported PPT rendered for visual verification');
 process.exit(0);
}

const template = path.join(root, 'Communications/STL_Product_Pitch_Template.pptx');
const deck = await PresentationFile.importPptx(await FileBlob.load(template));
const outline = await fs.readFile(path.join(root, 'reports/Compass-BSC-Source-Reconciled-Slide-Outline-2026-11-06.md'), 'utf8');
const c = { navy: '#20264D', coral: '#F04455', blue: '#3569BB', ink: '#222222', muted: '#626778', line: '#D8DCE8', pale: '#F4F6FA', white: '#FFFFFF', clear: '#FFFFFF00' };
const records = [];
const logPath = path.join(scratch, 'render_verify_loops.ndjson');
const priorLog = await fs.readFile(logPath, 'utf8').catch(() => '');
const loop = priorLog.trim().split('\n').filter(Boolean).length + 1;
if(loop > 3) throw new Error('Three render/verify loops already used');

if(loop === 1) {
  const ref = await deck.export({slide: deck.slides.getItem(0), format: 'png', scale: 1});
  await fs.writeFile(path.join(scratch, 'source-reference.png'), new Uint8Array(await ref.arrayBuffer()));
  const inspect = await deck.inspect({select:'$.slides[*]',include:['id','index','layout','elements.id','elements.kind','elements.text','elements.position']});
  await fs.writeFile(path.join(scratch, 'source-inspect.ndjson'), inspect.ndjson);
}
const logoBytes = execFileSync('unzip', ['-p', template, 'ppt/media/image2.svg']);
const logoBlob = logoBytes.buffer.slice(logoBytes.byteOffset, logoBytes.byteOffset + logoBytes.byteLength);

function text(s, name, copy, x, y, w, h, size = 23, opts={}) {
  const sh = s.shapes.add({ geometry: 'textbox', name, position: {left:x,top:y,width:w,height:h}, text:copy });
  sh.text.typeface = opts.light ? 'Geist Light' : 'Geist';
  sh.text.fontSize = size;
  sh.text.color = opts.color ?? c.ink;
  sh.text.bold = opts.bold ?? false;
  sh.text.insets = 0;
  sh.text.autoFit = 'none';
  sh.text.verticalAlignment = opts.valign ?? 'top';
  if(opts.align) sh.text.alignment = opts.align;
  records.push({kind:'textbox',slide:s._number,role:name,text:copy,textChars:copy.length,textLines:copy.split('\n').length,bbox:{left:x,top:y,width:w,height:h},fontSize:size});
  return sh;
}
function rect(s,name,x,y,w,h,fill) {
  return s.shapes.add({geometry:'rect',name,position:{left:x,top:y,width:w,height:h},fill,line:{fill,width:0}});
}
function rule(s,x,y,w,color=c.line,height=1) { return rect(s,`rule-${x}-${y}`,x,y,w,height,color); }
function emptySlide(index) {
  const slide = index === 0 ? deck.slides.getItem(0) : deck.slides.getItem(0).duplicate();
  if(index > 0) slide.moveTo(index);
  for(const sh of [...slide.shapes.items]) sh.delete();
  for(const im of [...slide.images.items]) im.delete();
  for(const tb of [...slide.tables.items]) tb.delete();
  slide._number = index + 1;
  slide.background.fill = c.white;
  return slide;
}
function frame(s, title) {
  text(s,'title',title,92,74,1105,60,40,{color:c.navy,bold:true});
  text(s,'footer','Compass / BSC roadmap / November 2026',91,665,870,26,16,{color:c.blue});
  text(s,'page-number',String(s._number),43,668,28,22,15,{color:'#858585'});
  const logo = s.images.add({blob:logoBlob,fit:'contain',alt:'Stellarus logo'});
  logo.position = {left:1129,top:657,width:113,height:27};
}
function table(s,name,values,x,y,widths,rowHeights,fontSize=20) {
  const height = rowHeights.reduce((a,b)=>a+b,0);
  const t = s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width:widths.reduce((a,b)=>a+b,0),height,columnWidths:widths,values});
  t.name = name;
  t.styleOptions = {headerRow:false,firstColumn:false,lastColumn:false,bandedRows:false,bandedColumns:false};
  t.borders.assign({style:'solid',fill:c.white,width:2});
  for(let r=0;r<values.length;r++) {
    t.rows[r].height = rowHeights[r];
    for(let col=0;col<values[0].length;col++) {
      const cell = t.getCell(r,col);
      cell.fill = r===0 ? c.navy : r%2===1 ? c.pale : c.white;
      cell.text.typeface = 'Geist';
      cell.text.fontSize = r===0 ? fontSize-1 : fontSize;
      cell.text.color = r===0 ? c.white : col===0 ? c.navy : c.ink;
      cell.text.bold = r===0 || col===0;
      cell.text.insets = {left:14,right:14,top:9,bottom:7};
      cell.text.verticalAlignment = 'middle';
      cell.text.autoFit = 'none';
    }
  }
  records.push({kind:'table',slide:s._number,role:name,text:values.flat().join('\n'),textChars:values.flat().join('\n').length,textLines:values.length,bbox:{left:x,top:y,width:widths.reduce((a,b)=>a+b,0),height}});
  return t;
}
const sections = outline.split(/^## /m);
function sourceSection(prefix) { return sections.find(t=>t.startsWith(prefix)) ?? ''; }
const commonNotes = `Sources: ${root}/Minerva/Background/Compass + ShieldAdvisor.md, supplied export of the requested Notion page, last reviewed November 5, 2026; ${root}/Minerva/Background/Compass-Executive-Briefing.pdf, 11 pages, November 2026; GAI-174.doc and GAI-663.doc supplied intake exports in the same Background directory. Full source mapping: ${root}/reports/Compass-BSC-Source-Reconciled-Slide-Outline-2026-11-06.md and prior intake mapping. Product foundation: local Compass CSR Chat product brief and implementation guide. The Notion export is the detailed proposed first-service scope; the PDF is a broader platform vision and maturity model. Neither establishes released end-to-end BSC voice/server functionality. Linked issue statuses are dated observations in the export, not independently refreshed. Referenced attachments/links were not reviewed. User directs Compass in place of the proposed Pega AI functions, retaining the CSR desktop. Exact Pega replacement and Shield Advisor versus Shield Central boundary remain to be agreed. User explicitly chose to retain Feb 1–28, 2027 as a launch target and flag the conflict with the export's Mar–Apr pilot / May–Jun controlled-production sequence. The date is not an engineering estimate or validated commitment. Genesys owns the live call, enforces configured routing and owns fallback. Compass proposes permitted Atlas context and a typed result/approved route class. SDK/adapter and direct API are alternatives; the SDK is a library, not a call-control service or independent member authorizer. Interactive voice, new conversational agents, summaries, coaching, automated quality scoring and new callbacks have separate scope. An AI destination must already be accepted or have a delivery dependency. Source header Q1 benefits/KB, Q2 transcription/summaries and Q3 live queries is directional, not release evidence. Top 20 remains an expansion ambition, not a February commitment or confirmed estimate. Q3/Q4 allocation is proposed. PDF Stage 4 includes outbound/SMS/Apple Business Chat and is an undated future horizon here, not Q4 2027 completion. Pega design testing approvals do not transfer to Compass production. No feature parity, universal recording, no-retention policy, PHI exclusion, backend availability, autonomous writeback, autonomous training or numerical savings claim is established. The user-provided 12M+ annual call figure is unverified and not used for savings. Source PDF slide 10 is now available as the maturity reference; this appendix adds the requested delivery windows and gates.`;
function notes(s,section,extra='') { s.speakerNotes.setText(`${commonNotes}\n\n${sourceSection(section)}\n\n${extra}`); }

// 1. Platform vision and bounded first release.
{
 const s=emptySlide(0); frame(s,'One Compass vision, delivered in bounded releases');
 text(s,'lead','Connect member intent, permitted data and the CSR experience\nthrough Compass Voice and Compass CSR Chat.',98,175,1090,90,29,{color:c.navy,light:true});
 const cols=[
  {x:98,n:'01',title:'Understand\nmember intent',body:'Front-door vision: recognize need,\nthen resolve or route.'},
  {x:467,n:'02',title:'Carry context\nto the CSR',body:'Permitted information arrives\nwith the member’s request.'},
  {x:836,n:'03',title:'Reduce manual\nagent effort',body:'Compass knowledge and Voice\nassistance in Shield Advisor.'}
 ];
 for(const v of cols) {
  rule(s,v.x,308,58,c.coral,4);
  text(s,`outcome-${v.n}`,v.n,v.x,273,60,35,24,{color:c.coral,bold:true});
  text(s,`outcome-title-${v.n}`,v.title,v.x,333,337,83,29,{color:c.navy,bold:true});
  text(s,`outcome-copy-${v.n}`,v.body,v.x,434,337,81,21,{light:true});
 }
 rect(s,'first-release-panel',98,554,1080,86,c.pale);
 text(s,'first-release-label','PROPOSED FIRST BSC RELEASE',116,568,1044,25,17,{color:c.blue,bold:true});
 text(s,'first-release','One authenticated inbound journey with trusted intent and Atlas context.',116,602,1044,34,24,{color:c.navy});
 notes(s,'Executive slide 1',sourceSection('Evidence and positioning'));
}
// 2. Specific service scope from the Notion export.
{
 const s=emptySlide(1); frame(s,'Compass prepares context; Genesys routes the call');
 text(s,'service-subtitle','First service: use an agreed post-authentication intent checkpoint.',98,175,1080,55,25,{color:c.navy,light:true});
 table(s,'context-service-features',[
  ['Proposed Compass feature','What the service provides','Delivery boundary'],
  ['Trusted intent\nand identity','Interpret the agreed intent and\nvalidate caller/service authority.','Confirm intent producer and\ntrusted identity propagation.'],
  ['Atlas context\nservice','Return permitted context, status,\nfreshness and an approved route class.','Validate required fields, access\nand data coverage.'],
  ['Context delivery\nand fallback','Deliver context to an authorized\nCSR or accepted AI destination.','Genesys enforces routing and\nfallback; late results cannot reroute.']
 ],98,248,[251,435,394],[46,88,88,88],21);
 text(s,'service-integration-label','INTEGRATION DECISION',98,587,1080,27,17,{color:c.blue,bold:true});
 text(s,'service-integration','SDK / adapter or direct API: validate hosting, identity and the wait budget.',98,620,1080,34,23,{color:c.navy});
 notes(s,'Executive slide 2',sourceSection('Evidence and positioning'));
}
// 3. Intake feature mapping with independently scoped delivery tracks.
{
 const s=emptySlide(2); frame(s,'Agent assistance has separate delivery tracks');
 text(s,'csr-subtitle','Compass features for GAI-174 and GAI-663, alongside the context service.',98,175,1080,55,24,{color:c.navy,light:true});
 table(s,'agent-assist-tracks',[
  ['BSC need','Compass feature direction','Readiness and timing'],
  ['Benefits and\nknowledge lookup','CSR Chat benefit answers and\napproved KB / SMP retrieval\nin Shield Advisor.','Benefit Q&A foundation.\nBSC integration to validate.\nQ1 planning track.*'],
  ['Transcription and\ncall summaries','Compass Voice transcription and\ndraft summaries for CSR review.','Separate voice/audio scope.\nQ2 planning track.*\nAgree retention and writeback.'],
  ['Agent queries and\nworkflow support','Proposed live queries, case/rule\nguidance, response and follow-up\ndrafts for CSR review.','Proposed extension.\nQ3 query planning track.*\nCase/rule scope to agree.']
 ],98,246,[243,460,377],[44,100,100,100],20);
 text(s,'csr-accountability','The context service can support these features; each needs its own delivery acceptance.',98,610,1080,31,22,{color:c.navy,light:true});
 text(s,'csr-source-note','*Directional sequence, not committed releases. The CSR owns final communication and actions.',98,643,1080,21,16,{color:c.muted});
 notes(s,'Executive slide 3',sourceSection('Choices alternatives and exclusions'));
}
// 4. User-selected February target, visibly distinct from the source plan.
{
 const s=emptySlide(3); frame(s,'February MVP target; expansion follows results');
 text(s,'roadmap-summary-subtitle','Planning windows from December 2026 through Q4 2027; readiness governs release.',98,175,1080,39,23,{color:c.navy,light:true});
 table(s,'roadmap-summary',[
  ['Stage','Timing','Compass focus'],
  ['0  Prove','Dec 2026','Demonstrate one journey; agree intent, context,\nPega overlap, interface and accountable owners.'],
  ['1  MVP','Feb 1–28, 2027\nLaunch target','One journey with context before routing. Self-service\nrequires an accepted voice / AI destination.'],
  ['2  Widen','Mar–Jun 2027\nMonthly releases','Expand validated intents toward the Top 20 ambition;\nseparate agent-assist features need their own acceptance.'],
  ['3  Routing pilots','Q2 discovery\nQ3 2027 proposed','Design all-LOB routing, digital context, callbacks and\nsupervisory assistance; pilot selected scopes.'],
  ['4  Expand','Q4 2027\nProposed','Scale proven inbound scope; retire only accepted\nPega AI functions. Outbound / new channels remain future.']
 ],98,226,[191,214,675],[44,62,68,68,64,64],20);
 text(s,'roadmap-conflict','Schedule conflict: source plan has Mar–Apr pilot / May–Jun production.\nFebruary remains a target; reconcile scope, dependencies and owner-approved readiness.',98,611,1080,49,18,{color:c.coral,bold:true});
 notes(s,'Executive slide 4',sourceSection('Proposed slide 10')+'\n\n'+sourceSection('Choices alternatives and exclusions'));
}
// 5. First-service acceptance distinct from later value hypotheses.
{
 const s=emptySlide(4); frame(s,'Prove service quality before claiming business value');
 text(s,'measurement-subtitle','Baseline the first service; measure later features against their own outcomes.',98,175,1080,39,24,{color:c.navy,light:true});
 table(s,'outcome-scorecard',[
  ['Outcome','Measures to baseline and track'],
  ['Intent and context','Intent accuracy, Atlas data quality\nand context delivery success'],
  ['Call continuity','Added wait, correct destination,\nfallback success and availability'],
  ['Agent / member\noutcomes','AHT, FCR, research/summary effort,\nrepeat contact, quality and adoption'],
  ['Economics','Cost per eligible interaction; later,\nCCaaS + AI cost per resolved contact'],
  ['Access and\nlifecycle','Authorized data, context freshness,\nexpiry and exposure incidents']
 ],98,238,[238,488],[44,64,64,64,64,64],21);
 rule(s,855,238,1,c.line,364);
 text(s,'decisions-heading','Pilot decisions',887,243,300,40,26,{color:c.navy,bold:true});
 const decisions=[['01','Exact service and\nPega overlap'],['02','Named owners,\nbaselines and thresholds'],['03','Compass data flow and\nproduction acceptance']];
 decisions.forEach(([n,t],i)=>{
  const y=309+i*96;
  text(s,`decision-number-${n}`,n,887,y,38,28,19,{color:c.coral,bold:true});
  text(s,`decision-text-${n}`,t,935,y-1,253,70,22,{color:c.navy,light:true});
 });
 text(s,'measurement-note','Savings remain a hypothesis. Compare like-for-like cohorts and include added wait / AI cost.',98,625,1080,32,19,{color:c.blue});
 notes(s,'Executive slide 5',sourceSection('Risks dependencies owners and validation')+'\n\n'+sourceSection('Requirement traceability'));
}
// 6. Roadmap detail for use as the referenced larger-deck slide 10.
{
 const s=emptySlide(5); frame(s,'Compass roadmap: December 2026 through Q4 2027');
 text(s,'roadmap-subtitle','Proposed delivery approach and evidence to proceed; dates are planning targets.',98,175,1080,32,23,{color:c.navy,light:true});
 table(s,'detailed-roadmap',[
  ['Stage','Timing','Delivery approach','Decision to proceed'],
  ['0  Prove','Dec 2026','One journey; agree intent, Atlas fields,\nPega overlap and interface.','Scope, contracts and\nowners accepted.'],
  ['Readiness','Jan 2027','Prove identity, approved reads, typed result\nand selected SDK / API path.','End-to-end, timeout and\nlate-result checks pass.'],
  ['1  MVP target','Feb 1–28, 2027','Context before routing; human fallback.\nVoice-agent readiness gates self-service.','BSC launch acceptance;\nsupport and rollback ready.'],
  ['2  Widen','Mar–Jun 2027\nMonthly releases','Expand validated intents toward Top 20;\nagent assist has separate release gates.','Context, wait, routing,\nquality and cost accepted.'],
  ['Phase 2\ndiscovery','Q2 2027\nParallel work','Design all-LOB routing, digital journeys,\ncallbacks and supervisory assistance.','Pilot scope, signals, owners\nand capacity agreed.'],
  ['3  Pilots*','Q3 2027','Pilot selected flows; validate exact Pega\nfunction transition where selected.','Service continuity and\nattributable value accepted.'],
  ['4  Expand*','Q4 2027','Scale proven inbound scope; retire only\naccepted migrated Pega AI functions.','Sustained value and\noperational ownership.']
 ],98,214,[160,183,463,274],[40,53,53,53,53,53,53,53],18);
 text(s,'roadmap-note','Schedule conflict: source plan has Mar–Apr pilot / May–Jun production; February target needs reconciliation.\n*Proposed allocation. Outbound and additional channels remain future scope.',98,632,1080,32,15,{color:c.coral,bold:true});
 notes(s,'Proposed slide 10',sourceSection('Executive slide 4')+'\n\n'+sourceSection('Risks dependencies owners and validation')+'\n\n'+sourceSection('Executive slide 3'));
}

if(deck.slides.count!==6) throw new Error(`Expected six slides, found ${deck.slides.count}`);
await fs.writeFile(path.join(scratch,'editable-text-records.json'),JSON.stringify(records,null,2));
const inspected = await deck.inspect({select:'$.slides[*]',include:['id','index','layout','elements.id','elements.kind','elements.text','elements.position','notes.text']});
await fs.writeFile(path.join(scratch,'final-inspect.ndjson'),inspected.ndjson);
console.log('Rendering six slides');
for(let i=0;i<deck.slides.count;i++) {
 const slide=deck.slides.getItem(i);
 const png=await deck.export({slide,format:'png',scale:1});
 await fs.writeFile(path.join(scratch,'preview',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 const layout=await slide.export({format:'layout'});
 await fs.writeFile(path.join(scratch,'preview',`slide-${String(i+1).padStart(2,'0')}.layout.json`),await layout.text());
 console.log(`Rendered slide ${i+1}`);
}
const output=path.join(outDir,'output.pptx');
const pptx=await PresentationFile.exportPptx(deck); await pptx.save(output);
await fs.appendFile(logPath,JSON.stringify({loop,output,slides:6,date:new Date().toISOString()})+'\n');
const reopened=await PresentationFile.importPptx(await FileBlob.load(output));
if(reopened.slides.count!==6) throw new Error('Exported deck did not reopen with six slides');
const snapshot=await reopened.inspect({select:'$.slides[*]',include:['index','elements.kind','elements.text','notes.text']});
await fs.writeFile(path.join(scratch,'reopened-inspect.ndjson'),snapshot.ndjson);
const content = snapshot.records.map(r=>JSON.stringify(r)).join('\n');
for(const required of ['December 2026','Feb 1–28, 2027','Mar–Jun 2027','Q2 2027','Q3 2027','Q4 2027','Shield Advisor','Top 20','supervisory','Compass Voice','Compass CSR Chat','GAI-174','GAI-663','SMP','Proposed extension','CSR review','Atlas','Genesys','Mar–Apr pilot / May–Jun production','Schedule conflict','fallback','SDK','approved route class','cost per resolved contact']) {
 if(!content.includes(required)) throw new Error(`Missing expected editable content: ${required}`);
}
await fs.writeFile(path.join(scratch,'verification.json'),JSON.stringify({output,slides:6,loop,editableTextboxes:records.filter(r=>r.kind==='textbox').length,nativeTables:5,template,sourceMatched:['Geist','Geist Light','1280x720','navy headings','coral rule','Stellarus logo'],sourceIntakes:['GAI-174','GAI-663'],reimport:'PASS',content:'PASS',visualReview:'PENDING'},null,2));
console.log(JSON.stringify({output,slides:6,loop,editableTextboxes:records.filter(r=>r.kind==='textbox').length,reimport:'PASS'}));
