import fs from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
import {FileBlob,PresentationFile} from '@oai/artifact-tool';
const root='/Users/jjacks20/jjacks/Conversational-AI';
const scratch=root+'/tmp/slides/compass-platform-pitch-v1';
const source=root+'/Communications/outputs/csr-chat-pitch-v2/output.pptx';
const finalPath=root+'/Communications/outputs/compass-platform-pitch-v1/output.pptx';
const sourceHash=createHash('sha256').update(await fs.readFile(source)).digest('hex');
async function finalizeCandidate(){
 process.env.RUNTIME_NODE_MODULES='/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
 const skill='/Users/jjacks20/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
 const {finalizePresentation}=await import(pathToFileURL(skill+'/container_tools/artifact_tool_utils.mjs').href);
 const result=await finalizePresentation({workspaceDir:root,candidatePath:scratch+'/candidate.pptx',finalPath,pythonExecutable:'/Users/jjacks20/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',integrityValidatorPath:skill+'/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:skill+'/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:1,requiredNativeChartOwnerSlides:[],requiredNativeTableOwnerSlides:[],fontPolicy:{basis:'reference',families:['Geist','Geist Light'],referencePath:source,referenceSha256:sourceHash},verifyArtifactToolImport:true,receiptPath:scratch+'/validation.json'});
 const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
 const s=final.slides.getItem(0);
 await fs.writeFile(scratch+'/final-1.png',new Uint8Array(await (await final.export({slide:s,format:'png',scale:1.5})).arrayBuffer()));
 await fs.writeFile(scratch+'/final-inspect.ndjson',(await final.inspect({kind:'slide,textbox,notes',maxChars:100000})).ndjson);
 console.log(JSON.stringify(result,null,2));
}
if(process.argv.includes('--finalize-only')){await finalizeCandidate();process.exit(0);}
const p=await PresentationFile.importPptx(await FileBlob.load(source));
const before=await p.inspect({kind:'slide,textbox,image,layout',maxChars:100000});
await fs.writeFile(scratch+'/source-inspect.ndjson',before.ndjson);
const slide=p.slides.getItem(0);
await fs.writeFile(scratch+'/source-1.png',new Uint8Array(await (await p.export({slide,format:'png',scale:1.5})).arrayBuffer()));
await fs.writeFile(scratch+'/source-layout.json',await (await slide.export({format:'layout'})).text());
const updates={
 'sh/547294r6':'COMPASS Platform',
 'sh/7qp4be9c':'Compass Platform  /  Jason Jackson  /  October 26, 2026  /  v1',
 'sh/65g3298r':'Platform Overview',
 'sh/ts7md4r2':'Compass Platform provides reusable integration, identity, orchestration and governance building blocks for products such as CSR Chat and Member Chat.',
 'sh/sryl4zqx':'The customer and problem',
 'sh/fu94fe98':'Product and engineering teams need AI experiences across customers. Bespoke identity, data and vendor integrations duplicate effort and complicate launches.',
 'sh/utg3698n':'The foundational building blocks',
 'sh/wn6dc7eh':'SDK/API and UI. Tenant identity and configuration.\nAgent broker and adapters. Benefits Service.\nContent, telemetry and quality controls.',
 'sh/hofulsf2':'The value proposition',
 'sh/ul4vaxgb':'One integration foundation for multiple products.\nReusable contracts for customer policy and data.\nGoal: less bespoke delivery and simpler support.',
 'sh/3qxwn2x8':'Products it enables',
 'sh/sfqdkrep':'CSR Chat: benefit support for representatives.\nMember Chat: conversational member support.\nReadiness is validated by product and customer.',
 'sh/5sfepcfe':'The offer and next step',
 'sh/ipovexwn':'Build & Integrate. Next: validate the shared foundation across CSR Chat and Member Chat with Jason Jackson.\nTarget: one approved tenant, two product journeys, with tenant isolation, grounded answers and traceability verified.',
};
for(const [id,value] of Object.entries(updates))p.resolve(id).text=value;
for(const id of ['sh/fu94fe98','sh/wn6dc7eh','sh/ul4vaxgb','sh/sfqdkrep','sh/ipovexwn']){
 const shape=p.resolve(id);shape.text.fontSize=18.67;shape.text.typeface='Geist Light';shape.text.autoFit='none';
}
slide.speakerNotes.setText(`COMPASS PLATFORM — OCTOBER 26, 2026

POSITIONING AND DIAGNOSIS
Compass Platform is the reusable conversational AI foundation that connects customer experiences to trusted context, domain data and AI runtimes. CSR Chat and Member Chat are product experiences using or converging on these shared building blocks. Product, engineering and implementation teams are the direct platform users. Health plan operations teams benefit through the product experiences. Bespoke customer/vendor integrations create duplicated delivery and support work. The platform strategy establishes shared contracts while preserving product-specific presentation, policy and answer semantics.
Sources:
${root}/Multi-Tenant-Platform/Compass-Platform.pptx, slides 1–4.
${root}/Multi-Tenant-Platform/Stellarus-Platform-Initiative-2026.md, strategic levers, themes A–E, and health metrics.
Current initiative: https://linear.app/stellarus/initiative/compass-platform-574a58a5a0d3

FOUNDATIONAL BUILDING BLOCKS
1. Integration and UI: versioned SDK/API contracts and reusable chat surfaces connect customer applications or hosted experiences to the platform. The SDK can standardize sessions, streaming, errors and integration hooks. Completion depends on the delivery path and environment.
Source: https://linear.app/stellarus/project/sdkapi-customer-integration-path-8652832f9ab6
Related delivery evidence: COMPASS-33 (framework-neutral Web Component), COMPASS-486 (themed ChatPanel), COMPASS-125 (consumer integration documentation), all recorded Done. Project-level completion is not inferred from these issues.
2. Tenant identity and customer configuration: Customer Configuration Service context carries verified customer, principal/persona and scopes. Shared validation and tenant-scoped access are designed to reject missing, expired or mismatched context. Customer configuration connects product behavior to the appropriate customer.
Source: https://linear.app/stellarus/project/tenant-context-and-auth-spine-3ece0fa797f8
3. Orchestration and adapters: the agent broker coordinates requests, streaming, failure handling and agent/data-service adapters. Stellarus-owned contracts separate customer integration from a specific agent runtime. Sierra and CSR Chat adapters represent runtime options, not an assertion that all adapters are fully deployed for every customer.
Source: https://linear.app/stellarus/project/broker-conversation-orchestration-cfa99b068775
4. Governed domain data: Benefits Service exposes structured customer plan benefits. Compass consumes this domain service for grounding. Data access, source provenance, effective dates and approved coverage constrain answers. Future AtlasIQ/domain integrations require their own contracts and validation. Compass is not represented as the benefits system of record.
Source: https://linear.app/stellarus/project/benefits-service-1f0d18290bb9
5. Content and operational controls: tenant-scoped content/configuration, request tracing, reporting, quality review, support runbooks and release gates support product operation. Curated starter questions and prompt/content integration still require consumer validation.
Sources: https://linear.app/stellarus/project/tenant-scoped-curated-chat-suggestions-5fb6aba1bed9
https://linear.app/stellarus/project/launch-telemetry-quality-gates-and-support-readiness-b57205de9e5d
These are logical shared building blocks. The slide is a platform positioning summary, not a deployment topology or a declaration that every cross-service path is complete.

PRODUCT RELATIONSHIP AND CURRENT READINESS
CSR Chat provides plan-grounded benefit support for health plan representatives. Member Chat provides conversational support to members. The platform supplies common integration/context/data/operational primitives while each product retains its audience-specific agent behavior and release requirements. The production CSR Chat product does not establish that its complete platform-converged path is production ready.
Current Linear project records for SDK/API, tenant context, broker, content, telemetry and multi-customer foundation remain Build & Integrate as reviewed October 26, 2026. ENG-1147 (verified broker-to-CSR caller path) and COMPASS-782 (verified CSR SDK turns) remain In Progress. COMPASS-810 (Member Chat into Production) is Staged. These constrain any claim of fully converged production delivery. No voice, contact-center handoff, conversation-history or cross-channel continuity capability is claimed as generally available here.
Sources:
https://linear.app/stellarus/issue/ENG-1147/broker-csr-chat-as-the-caller-roll-out-csrverified-chat-for-stellarus
https://linear.app/stellarus/issue/COMPASS-782/support-verified-csr-gateway-turns-in-the-stellarus-chat-sdk
https://linear.app/stellarus/issue/COMPASS-810/member-chat-into-production
${root}/Multi-Tenant-Platform/Feature-PRDs/Compass-Capability-Roadmap/M0-Platform-Reference-Foundation-PRD.md, initial cohort, product goals, non-goals and supported journeys.
Historical readiness context: ${root}/reports/Compass-Platform-Exit-Criteria-Assessment-2026-09-08.md. Its findings are dated, not a substitute for current release evidence.

CHOICES, ALTERNATIVES AND VALUE
The guiding policy is to reuse versioned platform contracts for customer integration, trusted context, approved data and agent adapters across products. The intended outcomes are less bespoke integration work, more consistent support evidence, and the ability to evolve agent implementations without forcing each customer to rebuild its integration. These are design benefits and outcome hypotheses, not measured cost or lead-time savings.
Material alternatives: keep independent per-product integrations, which can simplify the first isolated delivery but duplicates integration/support effort as products grow; or tightly couple the experience to one end-to-end vendor, which may simplify near-term delivery but ties product evolution to that vendor's contracts. Shared platform contracts add coordination, versioning and rollout discipline. The slide uses the existing competitor block for Products it enables because the requested purpose is to explain the platform-to-product relationship. No named competitive superiority is asserted.

BOUNDED NEXT STEP AND MEASUREMENT
Jason Jackson, the Compass Platform initiative/project owner, coordinates a scoped validation of one approved tenant across the CSR Chat and Member Chat product journeys. This target comes from the M0 reference-foundation scope and is a proposed completion boundary, not an observed result or newly committed delivery date.
Sequence: agree on the tenant, supported plans and representative/member authorization boundary; select the shared contracts and adapters; validate each product journey including safe failure behavior; review quality, telemetry, support and rollback evidence; obtain release approval before expansion.
Acceptance: both product journeys use the approved shared contracts and tenant context; unauthorized or mismatched requests expose no protected information; supported answers use approved plan evidence; unsupported or unavailable data produces safe clarification/limitation behavior; each journey carries traceable request/outcome evidence. Product-specific review and customer approval remain required.
Metrics: two validated product journeys for one approved tenant. Leading indicators are approved contracts, data readiness and passing scenario evidence. Guardrails are zero cross-tenant access and no unresolved launch-blocking security or correctness defects. Baseline integration effort, onboarding elapsed time, support defects and existing duplication before the cohort, then compare following delivery. Numeric speed/savings targets await an agreed baseline and are not invented here.
Owners: Product owns scope and acceptance, Engineering owns contracts/integration, Identity and Security own access approval, domain teams/customer SMEs own data and answer approval, and Operations/Support own operational readiness. Jason coordinates the decision and named assignments.

BOUNDARIES, RISKS AND CONFIDENCE
Claims, eligibility, accumulators, formulary, provider lookup/scheduling, broad voice/CCaaS support and autonomous multi-agent planning remain separately scoped capabilities. A universal low-code workflow platform is excluded. The focus is reusable foundations that enable bounded products.
Dependencies include customer configuration and identity, approved plan data, compatible SDK/broker/agent contracts, content routing, telemetry and cross-functional release evidence. Wrong-tenant context or data leakage blocks launch. Unsupported source data, incompatible contracts or missing telemetry require scope/plan revision. New PHI, external integrations, unsupported domains or customer-specific code forks trigger a separate decision.
Confidence is high in the documented logical building blocks and recorded Linear phases, and moderate in their completeness across products/customers. Local architecture documents contain historical target-state and implementation descriptions that do not always agree on endpoints; this slide therefore avoids endpoint-level assertions. Validate the exact deployed path for each product before making launch claims.
`);
const inspect=await p.inspect({kind:'slide,textbox,shape,notes',maxChars:100000});
await fs.writeFile(scratch+'/updated-inspect.ndjson',inspect.ndjson);
const layout=JSON.parse(await (await slide.export({format:'layout'})).text());
await fs.writeFile(scratch+'/updated-layout.json',JSON.stringify(layout,null,2));
await fs.writeFile(scratch+'/editable-text-records.json',JSON.stringify(layout.elements.filter(e=>e.text).map(e=>({kind:e.kind,slide:1,role:e.name,text:e.text,textChars:e.text.length,textLines:e.text.split('\n').length,bbox:e.position})),null,2));
await fs.writeFile(scratch+'/updated-1.png',new Uint8Array(await (await p.export({slide,format:'png',scale:1.5})).arrayBuffer()));
await (await PresentationFile.exportPptx(p)).save(scratch+'/candidate.pptx');
await fs.writeFile(scratch+'/source-hash.txt',sourceHash);
console.log('Companion slide authored and rendered. Source hash:',sourceHash);
if(process.argv.includes('--finalize'))await finalizeCandidate();
