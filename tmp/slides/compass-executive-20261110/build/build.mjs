import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {FileBlob, PresentationFile} from '@oai/artifact-tool';

const ROOT='/Users/jjacks20/jjacks/Conversational-AI';
const WORK=ROOT+'/tmp/slides/compass-executive-20261110';
const SKILL='/Users/jjacks20/.codex/plugins/cache/openai-primary-runtime/presentations/26.1105.12137/skills/presentations';
const SOURCE=ROOT+'/Minerva/Compass_Executive_Briefing_Updated.pptx';
process.env.RUNTIME_NODE_MODULES='/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE='/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node';
const p=await PresentationFile.importPptx(await FileBlob.load(SOURCE));
const source=await p.inspect({select:'$.slides[0]',include:['id','elements.id','elements.text','notes.text']});
const slide=p.slides.getItem(0);
const originalNotes=source.records[0].notes.text;
p.delete(source.records[0].elements.map(e=>e.id));
slide.background.fill='#FFFFFF';

const C={navy:'#15213A',blue:'#1F5FD1',green:'#14523B',purple:'#5D4BBA',muted:'#5B6B82',line:'#D9E1EA',mint:'#F2F8F5',lavender:'#F6F4FC'};
const records=[];
function rect(name,x,y,w,h,fill,line='none',lw=0){
  return slide.shapes.add({name,geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:line,width:lw,style:'solid'}});
}
function txt(role,text,x,y,w,h,size=20,color=C.navy,bold=false,align='left'){
  const box=slide.shapes.add({name:role,geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  box.text=text;
  box.text.style={fontSize:size,typeface:'Arial',color,bold,alignment:align,verticalAlignment:'top',wrap:true};
  box.text.insets=0;
  records.push({kind:'textbox',slide:1,role,text,textChars:text.length,textLines:text.split('\n').length,bbox:{x,y,w,h}});
  return box;
}

txt('title','Compass agent roadmap',64,47,1152,56,42,C.navy,true);
txt('subtitle','Two coordinated tracks on a shared ATLASIQ foundation',64,111,1152,31,24,C.muted);

const cols=[{x:280,w:162,title:'Q4 2026'},{x:486,w:330,title:'H1 2027'},{x:866,w:334,title:'H2 2027 onward'}];
cols.forEach((c,i)=>{
  txt('horizon-'+i,c.title,c.x,170,c.w,31,23,C.blue,true);
  rect('horizon-rule-'+i,c.x,207,c.w,2,C.line);
});

rect('csr-track-band',64,224,1152,176,C.mint);
rect('voice-track-band',64,416,1152,176,C.lavender);
rect('csr-track-rule',64,224,4,176,C.green);
rect('voice-track-rule',64,416,4,176,C.purple);
txt('csr-track-name','Shield Advisor\n+ Compass',84,244,174,59,22,C.green,true);
txt('csr-track-purpose','CSR assistance',84,320,163,25,18,C.green);
txt('voice-track-name','Voice /\nCCaaS',84,438,165,62,24,C.purple,true);
txt('voice-track-purpose','Intent front door',84,516,165,26,18,C.purple);

function milestone(role,title,detail,col,y,color){
  const c=cols[col];
  txt(role+'-heading',title,c.x,y,c.w,25,20,color,true);
  txt(role+'-detail',detail,c.x,y+25,c.w,col===0?64:27,20,C.navy);
}
milestone('csr-prototype','Prototype','Documents by intent',0,244,C.green);
milestone('csr-assist','CSR guided / AI assisted','Benefits & knowledge base',1,234,C.green);
milestone('csr-transcribe','CSR guided / AI transcribed','Intent & call summary',1,288,C.green);
milestone('csr-guide','AI guided / CSR empowered','Verify early value',1,342,C.green);
milestone('csr-expand','Expand','Content & intents',2,234,C.green);
milestone('csr-journey','Next horizon','Journey context',2,288,C.green);
milestone('csr-supervisor','Explore','Supervisor copilot',2,342,C.green);
milestone('voice-prototype','Stage 0','Listening & intent demo',0,438,C.purple);
milestone('voice-discovery','Discovery','Intents & integrations',1,426,C.purple);
milestone('voice-build','Build / test','Stream & agent-leg test',1,480,C.purple);
milestone('voice-mvp','MVP target','Selected deflection',1,534,C.purple);
milestone('voice-stage2','Stage 2','Expand to top 20 intents',2,426,C.purple);
milestone('voice-stage3','Stage 3','Micro-route / callback',2,480,C.purple);
milestone('voice-stage4','Stage 4','Predictive reach',2,534,C.purple);

rect('foundation-band',64,610,1152,61,'#E6F5ED');
txt('foundation-title','ATLASIQ',84,618,184,29,24,C.green,true);
txt('foundation-caption','Shared foundation',84,647,200,22,16,C.green);
txt('foundation-capabilities','Approved sources, member/plan matching, service contracts\nFreshness, provenance and tenant controls',322,618,872,49,19,C.green);
txt('footer','November 2026. Internal discussion draft. Planning windows require product and engineering approval.',64,688,1093,23,14,C.muted);
txt('page-number','10',1180,688,36,23,14,C.muted,true,'right');

slide.speakerNotes.setText('Current presentation timing, November 10, 2026: retain the Voice / CCaaS MVP in H1 2027. This supersedes the earlier July 2027 reference in the historical planning context below. All windows remain indicative and require product and engineering approval.\n\nHistorical planning context:\n'+originalNotes);
await fs.writeFile(WORK+'/editable-text.json',JSON.stringify(records,null,2));
const inspect=await p.inspect({select:'$.slides[*]',include:['id','index','elements.id','elements.kind','elements.text','elements.position','elements.style','notes.text']});
await fs.writeFile(WORK+'/final-inspect.ndjson',inspect.ndjson);
await fs.writeFile(WORK+'/preview/cleaned.png',new Uint8Array(await (await p.export({slide,format:'png',scale:1.5})).arrayBuffer()));
await fs.appendFile(WORK+'/render-attempts.ndjson',JSON.stringify({attempt:Number(process.env.COMPASS_RENDER_ATTEMPT??1),when:new Date().toISOString(),file:'cleaned.png'})+'\n');
await (await PresentationFile.exportPptx(p)).save(WORK+'/candidate.pptx');
console.log(JSON.stringify({stage:'draft-ready',textboxes:records.length,slideCount:p.slides.count}));

if(process.argv.includes('--finalize')){
  const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
  const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:WORK+'/candidate.pptx',finalPath:ROOT+'/Minerva/Outputs/compass-executive-20261110/output.pptx',pythonExecutable:'/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:SKILL+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:SKILL+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:1,fontPolicy:{basis:'reference',families:['Arial'],referencePath:SOURCE,referenceSha256:createHash('sha256').update(await fs.readFile(SOURCE)).digest('hex')},verifyArtifactToolImport:true,receiptPath:WORK+'/validation.json'});
  console.log(JSON.stringify(result));
}
