import fs from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';
const root='/Users/jjacks20/jjacks/Conversational-AI';
const scratch=root+'/tmp/slides/csr-chat-pitch-v2';
async function finalizeCandidate(){
 process.env.RUNTIME_NODE_MODULES='/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
 const skill='/Users/jjacks20/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
 const {finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs').href);
 const original=root+'/Communications/STL_Product_Pitch - CSR Chat.pptx';
 const finalPath=root+'/Communications/outputs/csr-chat-pitch-v2/output.pptx';
 const result=await finalizePresentation({workspaceDir:root,candidatePath:scratch+'/candidate.pptx',finalPath,pythonExecutable:'/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:1,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'reference',families:['Geist','Geist Light'],referencePath:original,referenceSha256:createHash('sha256').update(await fs.readFile(original)).digest('hex')},verifyArtifactToolImport:true,receiptPath:scratch+'/validation.json'});
 console.log(JSON.stringify(result,null,2));
 const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
 const finalSlide=final.slides.getItem(0);
 await fs.writeFile(scratch+'/final-1.png',new Uint8Array(await (await final.export({slide:finalSlide,format:'png',scale:1.5})).arrayBuffer()));
 await fs.writeFile(scratch+'/final-inspect.ndjson',(await final.inspect({kind:'slide,textbox,notes',maxChars:100000})).ndjson);
}
if(process.argv.includes('--finalize-only')){await finalizeCandidate();process.exit(0);}
const presentation=await PresentationFile.importPptx(await FileBlob.load(root+'/Communications/STL_Product_Pitch - CSR Chat.pptx'));
await fs.writeFile(scratch+'/original-inspect.ndjson',(await presentation.inspect({kind:'slide,textbox,shape,image,layout',maxChars:100000})).ndjson);
for(const [i,slide] of presentation.slides.items.entries()) {
 const png=await presentation.export({slide,format:'png',scale:1.5});
 await fs.writeFile(scratch+`/original-${i+1}.png`,new Uint8Array(await png.arrayBuffer()));
 const layout=await slide.export({format:'layout'});
 await fs.writeFile(scratch+`/original-${i+1}-layout.json`,await layout.text());
}
const copy={
 'sh/547294r6':'COMPASS – CSR Chat',
 'sh/7qp4be9c':'CSR Chat  /  Jason Jackson  /  October 23, 2026  /  v2',
 'sh/65g3298r':'Product Overview',
 'sh/ts7md4r2':'CSR Chat helps health plan service teams answer benefit questions faster with structured, plan-specific guidance grounded in approved benefit data.',
 'sh/sryl4zqx':'The customer and problem',
 'sh/fu94fe98':'Health plan CSRs navigate complex plan data during live calls. Manual lookup increases handling time and the risk of inconsistent benefit explanations.',
 'sh/utg3698n':'The solution',
 'sh/wn6dc7eh':'Ask in plain language. CSR Chat returns coverage, cost sharing, limits and required disclosures from approved plan data for representative review.',
 'sh/hofulsf2':'The value proposition',
 'sh/ul4vaxgb':'BSC, Sep 2026: 11 sec median answer time.\n32,114 interactions. 1,336 monthly active users.\nGoal: less manual benefit research during calls.',
 'sh/3qxwn2x8':'Competitors',
 'sh/sfqdkrep':'NiCE CXone Copilot and Genesys Agent Copilot.\nCSR Chat focus: health plan benefit interpretation,\napproved disclosures and representative review.',
 'sh/5sfepcfe':'The offer and next step',
 'sh/ipovexwn':'Core in production at BSC. Standalone pilots in development. Next: scope a non-PHI pilot with Jason Jackson.\nTargets: ≥95% approved-case pass rate and launch within 7 days of signature, with inputs and approvals ready.',
};
for(const [id,text] of Object.entries(copy)){
 const shape=presentation.resolve(id);
 shape.text=text;
}
presentation.resolve('sh/ts7md4r2').position={left:98,top:204,width:1090,height:68};
for(const id of ['sh/fu94fe98','sh/wn6dc7eh','sh/ul4vaxgb','sh/sfqdkrep']){
 const shape=presentation.resolve(id);
 shape.text.fontSize=18.67;
 shape.text.typeface='Geist Light';
 shape.text.autoFit='none';
 shape.position={...shape.position,height:80};
}
presentation.resolve('sh/ipovexwn').position={left:98,top:588,width:1080,height:60};
const slide=presentation.slides.getItem(0);
slide.speakerNotes.setText(`CSR CHAT PRODUCT PITCH — OCTOBER 23, 2026

PRODUCT AND CUSTOMER
CSR Chat is the customer-facing product name throughout. It supports health plan customer service representatives during live benefit inquiries. Customer-service operations leaders are the primary buying audience. Representatives ask natural-language questions and review structured, plan-specific answers grounded in approved benefit data. Customer-approved configuration controls terminology, presentation, and required disclosure language. Unsupported questions require a safe decline or clarification. Representatives remain responsible for the final customer communication.
Sources: CSR Chat Product Brief, August 2026, sections 1–3 and 6, local file: ${root}/Minerva/Go-To-Market/Compass CSR Chat - Product Brief-v1.docx
Linear CSR Chat initiative, reviewed October 23, 2026: https://linear.app/stellarus/initiative/csr-chat-aka-minerva-43650102cc3b
Core benefits quoting project: https://linear.app/stellarus/project/minerva-benefits-quoting-mvp-d9623194f006

SCOPE AND DELIVERY
Supported populations depend on integrated and validated plan data. Current positioning is representative-assisted benefit inquiry. Claims adjudication, independent member/plan matching, member-facing chat, live accumulators, and broader information domains are excluded from this pitch. Benefits Service integration and approved plan context support customer-specific answers. Implementation requires agreement on data ownership, delivery/authentication, disclosures, validation, and support. The hosted standalone sales/pilot journey remains in development. Do not imply that every delivery pattern is available for immediate customer activation.
Sources: product brief sections 3.3–3.4, 6–7; Multi-Persona / Multi-Customer project, reviewed October 23, 2026: https://linear.app/stellarus/project/multi-persona-multi-customer-chat-8c83460151d1
Benefits Service integration issue COMPASS-376 is recorded Done. This does not establish blanket readiness of every new customer deployment.

OBSERVED PRODUCTION EVIDENCE
Blue Shield of California, September 1–30, 2026, Pacific time: 32,114 human interactions, 1,336 monthly active users, and an 11-second median answer time. These are dated deployment observations, not a performance guarantee or an independently measured reduction in call handle time. No manual baseline or causal control is established in the cited review. The deck therefore does not assert an accuracy improvement, labor savings, or a head-to-head performance advantage.
Source: ${root}/Minerva/Outputs/Compass-CSR-Chat-September-Month-In-Review-v4.pptx, slide 1 and notes. Source review derives these values from April–September monthly extracts. No member questions, user identities, or raw conversations are included here.

COMPETITIVE ALTERNATIVES
The comparison set includes NiCE CXone Copilot and Genesys Cloud Agent Copilot, plus manual plan-document/internal-tool research. Both named vendors describe real-time agent support using contextual knowledge. CSR Chat positioning emphasizes health plan benefit interpretation, approved plan context, required disclosures, and representative review. This focus is a positioning choice, not evidence that competitors lack these capabilities or that CSR Chat wins a benchmark. Broad contact-center copilots may offer wider workflow coverage, while a focused benefits assistant must prove plan-data fit and answer quality in the customer's own workflow.
Official sources reviewed October 23, 2026:
NiCE: https://www.nice.com/lps/cxone-copilot
Genesys: https://www.genesys.com/definitions/what-is-agent-assist

LIFECYCLE, OFFER, AND NEXT STEP
The core product is in production at BSC. The live sales app, standalone agent experience, and golden-dataset validation MVP are recorded Build & Integrate as of review. These records support an in-development pilot motion, not a claim of completed new-customer readiness.
Live Sales App: https://linear.app/stellarus/project/csr-chat-live-sales-app-382c90a423c2
Standalone Agent Experience: https://linear.app/stellarus/project/agent-experience-standalone-csr-chat-experience-bccbdf817c58
Latest standalone scope: https://linear.app/stellarus/document/standalone-csr-chat-agent-experience-sales-and-customer-pilots-0d4abbf418d4
Quality validation MVP: https://linear.app/stellarus/project/csr-chat-golden-dataset-quality-validation-mvp-d4ae00373c1e
Contact/decision coordinator: Jason Jackson, CSR Chat initiative and pilot-project owner in Linear. Next action is joint discovery to agree on the bounded pilot, approved non-PHI plan data, representative users, golden questions, disclosures, support, and commercial terms. No price, billing unit, or booked launch date is established by these sources, so none is quoted.

PILOT TARGETS AND APPROVALS
At least 95% pass rate on the customer-approved question set is a launch target, not observed universal product accuracy. A seven-calendar-day signature-to-online target assumes the customer pre-stages required inputs and approvals. Do not promise a seven-day deployment for incomplete intake, integrations, PHI, or new feature requests. Product, Engineering, Security, customer SMEs, Sales, and Customer Success must confirm readiness. Baseline answer latency, handle time, adoption, and feedback with each customer and compare after the pilot. Quality guardrails include zero cross-customer access, approved non-PHI data, safe unsupported-question outcomes, and no launch-blocking defects.
Source: ${root}/Minerva/Strategy/Compass-CSR-Chat-Rapid-Pilot-Demand-Strategic-Objective-Sep-Dec-2026.md, December live-pilot gate and measurement approach. The latest standalone scope also targets seven days with pre-staged inputs and explicitly retains release signoffs.

RISKS AND DECISION TRIGGERS
Poor source quality, stale plan versions, incorrect customer binding, unapproved disclosure language, or missing access approvals can block launch. Revisit scope and timing when a prospect needs PHI, customer SSO, CRM/contact-center integration, unsupported domains, or custom code. Customer SMEs own benefit approval, Product owns scope and exceptions, Engineering owns implementation readiness, Security owns access/data approval, and Sales/Customer Success own intake and handoff. Confidence is high in documented positioning and dated production observations, and moderate in transfer of those results to another customer. Customer-specific validation must establish the latter.
`);
const after=await presentation.inspect({kind:'slide,textbox,shape,image,notes',maxChars:100000});
await fs.writeFile(scratch+'/updated-inspect.ndjson',after.ndjson);
const layout=JSON.parse(await (await slide.export({format:'layout'})).text());
await fs.writeFile(scratch+'/updated-layout.json',JSON.stringify(layout,null,2));
await fs.writeFile(scratch+'/editable-text-records.json',JSON.stringify(layout.elements.filter(e=>e.text).map(e=>({kind:e.kind,slide:1,role:e.name,text:e.text,textChars:e.text.length,textLines:e.text.split('\n').length,bbox:e.position})),null,2));
await fs.writeFile(scratch+'/updated-1.png',new Uint8Array(await (await presentation.export({slide,format:'png',scale:1.5})).arrayBuffer()));
const candidate=scratch+'/candidate.pptx';
await (await PresentationFile.exportPptx(presentation)).save(candidate);
console.log('Candidate exported, rendered and text inspected:',candidate);
if(process.argv.includes('--finalize')){
 await finalizeCandidate();
}
