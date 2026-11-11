# Compass for BSC — source-reconciled presentation

Review date: November 6, 2026. Audience: BSC executive sponsors and delivery partners. Deliverable: five executive slides and one detailed roadmap appendix suitable for the referenced slide 10. This is a presentation and planning revision, not a product implementation or an approved delivery commitment.

## Evidence and positioning

**FACT — source statements:** The supplied `Minerva/Background/Compass + ShieldAdvisor.md` is an export of the requested Notion page, last reviewed November 5, 2026. It proposes a bounded service: one authenticated inbound BSC journey, an agreed intent producer/checkpoint, approved Atlas reads, a typed result consumed by Genesys, permitted context at the destination, and normal routing when assistance is unavailable. It targets Q2 2027 production subject to gates. The export calls the SDK a library/client contract rather than a deployed call-control service. It says the current SDK is chat-oriented and the completed Genesys connector is text-only/staging-scoped; this is not evidence of released server/voice integration. Linked backlog observations are as of November 4–5 and have not been refreshed in this task.

**FACT — vision:** `Minerva/Background/Compass-Executive-Briefing.pdf`, 11 pages, November 2026, describes a broader front door: understand, resolve, route with context, speech, recording, agent assistance, and eventual outreach/channel consolidation. Pages 7–9 retain CCaaS telephony, numbers, IVR authentication, queues and dialer; Pega case/workflow responsibilities remain to be confirmed. Pages 10–11 describe maturity stages whose progression depends on evidence, without dates. Stage 4 includes outbound, SMS and Apple Business Chat. These are vision statements, not feature release or production approval evidence. The MRI/prior-authorization story is illustrative, not evidence of an integrated prior-authorization API.

**FACT — intake:** GAI-174 asks for live voice integration and automated summaries with CSR review. GAI-663 asks for enterprise knowledge, guidance, drafting and reduced agent effort; later comments constrain the described Coach's input to deliberately supplied context, not live audio/transcripts. Both are Pega-design testing approvals. They do not authorize the Compass data flow or production release. Detailed source interpretations and mapping are retained in `reports/Compass-BSC-Intake-Aligned-Slide-Outline-2026-11-06.md`.

**FACT — product foundation:** the local Compass CSR Chat product brief and integration guide establish plan-grounded benefit Q&A using supplied plan context. The BSC SMP source connection, Shield Advisor integration, case/rule coaching, drafting and voice-summary integration require scope and release validation. Neither the vision PDF nor a backlog Done status establishes full end-to-end BSC production readiness.

**USER CHOICE:** Preserve the February 1–28, 2027 launch target and visibly flag its conflict with the export's Mar–Apr pilot and May–Jun controlled-production sequence. Do not relabel February as technical validation or silently move the launch. Preserve December 2026–Q4 2027 planning horizon, progressive monthly March–June releases, Q2 discovery and proposed Q3/Q4 expansion. Outbound remains future scope.

**INFERENCE — diagnosis:** The earlier agent-assist deck and the broader front-door vision need a concrete first increment between them. Leading with a bounded context service makes the proposal reviewable without implying that it delivers a new voice agent, summaries or all Pega AI replacement. Confidence is high in the documented boundary, moderate in narrative fit, and unvalidated in engineering feasibility and dates.

**Guiding policy:** Keep the broader Compass vision, define the first BSC increment precisely, and earn expansion through source quality, call continuity, service performance and business evidence. Treat the February date as a target with an unresolved source-plan conflict, not as a validated commitment.

## Executive slide 1 — One Compass vision, delivered through bounded releases

Lead with Compass connecting member intent, permitted data and the CSR experience. Three complementary outcomes: a front door that understands need; context carried to the receiving agent; less manual agent effort through separately scoped assistance. The first proposed BSC release is one authenticated inbound journey and Atlas context before Genesys routing. The wider voice, self-service and agent-assist vision remains visible.

The service returns a structured outcome and approved routing class. Genesys retains the live call, validates the routing class against configured policy, executes routing and owns fallback. Shield Advisor remains the proposed CSR experience, with its relationship to Shield Central explicitly unresolved in the notes. Do not claim wholesale replacement of Pega, Shield Advisor or CCaaS.

Discussion: choose the initial population, journey and exact Pega function being superseded. BSC business, Compass Product, Contact Center/Genesys/PTP and Pega/desktop architecture must agree the boundary.

## Executive slide 2 — Compass prepares context; Genesys routes the call

Describe the concrete first-service features:

1. Trusted intent and identity: use the agreed post-authentication checkpoint and producer. Compass validates service and caller authority before interpreting intent or selecting data. Caller ID/member reference alone is not authentication. Intent recognition here does not mean Compass is already asking the caller questions.
2. Atlas context service: select approved reads for the agreed intent; return complete/partial/unavailable status, permitted context or a reference, freshness and an approved route class. Required fields, current data coverage, identity mapping and access remain to be validated.
3. Context delivery and fallback: make allowed context available to the authorized human or already accepted AI destination. Genesys enforces routing policy and human fallback. Late results cannot alter completed routing. Optional later context retrieval requires an agreed lifecycle and receiving-application authorization.

SDK/adapter and direct Genesys-to-API are alternatives, not two simultaneous paths. Select based on supported hosting/runtime, service identity, reuse and operational ownership. The SDK packages requests/results; it does not independently authorize the member or directly access Atlas. The bounded service needs a waiting request/result checkpoint with success/failure/timeout handling. Passive audio monitoring and a new interactive voice session are separate integrations. Avoid a blanket claim of compatibility with any CCaaS.

Discussion: decide the supported Genesys/PTP interface, intent producer, authentication delegation, required Atlas fields, request deadline, context lifecycle and destination readiness. No numerical wait threshold is invented.

## Executive slide 3 — Compass agent assistance has separate delivery tracks

Keep GAI-174 and GAI-663 needs visible and map them to Compass features rather than relabeling the Pega products:

| BSC need | Compass feature direction | Evidence / delivery boundary |
| --- | --- | --- |
| Benefit and knowledge lookup | Plan-grounded CSR Chat answers plus approved KB/SMP retrieval in Shield Advisor | Benefit Q&A foundation; BSC sources and desktop integration to validate. Export's header places benefits/KB in Q1 as a directional track, not a confirmed release. |
| Call transcription and summaries | Compass Voice live transcription and draft summaries for CSR review | Separate audio/voice workstream, GAI-174. Export header labels Q2; the detailed bounded service excludes automated summaries. Recording, retention and writeback require agreement. |
| Agent queries and workflow support | Proposed live queries, approved case/rule guidance, response/follow-up drafts | Separate scope, GAI-663. Export header labels live queries Q3 without detailed delivery acceptance. Coaching/drafting are proposed extensions; do not imply availability or a live-audio Coach. |

Use the header's Q1/Q2/Q3 sequence as directional planning context only. The detailed text governs what the bounded service actually delivers. Coaching, automated quality scoring, new callbacks and development of a new conversational AI agent are separate scope. A self-service destination must already be accepted or have an explicit delivery dependency. Human review remains necessary for summaries, suggested actions and drafted communication. Supervisory copilots for QM, queues and analytics differ from individual CSR workflow guidance.

Discussion: confirm independent owners, scope, feature readiness and delivery gates for these tracks. The context service can support them but does not establish their completion.

## Executive slide 4 — Keep the February target; advance on evidence

| Stage | Planning window | Focus / gate |
| --- | --- | --- |
| 0 — Prove | December 2026 | Demonstrate one journey; agree intent/checkpoint, permitted context, integration boundary, exact Pega overlap and owners. Broader voice/recording/source prototype review remains a separate prototype scope. |
| 1 — MVP | February 1–28, 2027 target | One journey and bounded context before routing. Human fallback proven. Original deflection ambition requires an accepted voice/AI destination and separate interactive-voice delivery readiness. |
| 2 — Widen | Monthly March–June 2027 | Stage supported intent releases toward the original Top 20 ambition; expand eligible scope only after quality, handoff and source readiness. All 20 are not a February commitment or a proven Q2 estimate. |
| 3 — Routing pilots | Q2 discovery / Q3 2027 pilots | Design all-LOB policy, digital journeys, callbacks and supervisory workflows; pilot selected flows. Compass route recommendations/policy require agreed boundaries; Genesys executes approved routing. |
| 4 — Expand proven scope | Q4 2027 proposed | Extend successful inbound routes, contexts and assistance with accountable support and sustained value. Retire only the selected Pega AI functions after requirements and transition evidence are accepted. |

**Visible schedule conflict:** The source plan proposes Mar–Apr pilot and May–Jun production. February remains the user's launch target; scope, capacity, interface/identity/Atlas readiness, accepted destinations and governance must reconcile the gap. The source plan is a proposed sequence, not engineering estimates. This deck does not resolve the conflict by asserting feasibility.

The PDF's maturity Stage 4 means a broader one-platform end-state including outbound/SMS/Apple Business Chat. Q4 2027 expansion here is progress toward that maturity, not a promise to complete it. Outreach (including IHA/care gaps), new channels and vendor consolidation remain an undated future horizon. Full Avaya decommission is not established as a prerequisite; the chosen population needs a supported Genesys path. Existing Q4 2026 COC titles and Q1/Q2 Pega gates require owner reconciliation rather than silent rescheduling.

## Executive slide 5 — Prove service quality before claiming business value

Separate first-service acceptance from later agent-assist/self-service benefits:

| Level | Measures |
| --- | --- |
| Intent and context | Usable-intent coverage/accuracy; Atlas completeness, correctness and freshness; context delivery success |
| Call continuity | Added pre-routing wait, including tail latency; correct destination rate; fallback success and availability |
| Agent/member outcomes | AHT/research/summary effort, FCR, repeat contact, satisfaction and quality; agent adoption, time to proficiency and feedback for each separately released feature |
| Economics | Cost per eligible interaction for the bounded service; later total CCaaS + AI cost per resolved contact, including repeat calls and transfers |
| Access and lifecycle | Unauthorized retrieval prevented; receiving-application access; expiry/correlation; exposure incidents |

Baseline before pilot, agree numerical thresholds and review windows with BSC, then compare like-for-like populations. No invented savings, accuracy, time or containment target. Track assisted and self-service populations separately. Proposed review cadence: weekly pilot review, then 30/60-day value checks per feature release. Containment is not sufficient evidence of service resolution; monitor repeat contact, abandonment and satisfaction. Prioritize intents using volume, handle time, data/destination feasibility and service risk, rather than volume alone.

The PDF's shorter-call and reduced-CCaaS-minute economics are a hypothesis. Added pre-routing time and Compass processing cost may offset gains. Pega cost avoidance requires evidence of an actual service transition; the bounded context release cannot automatically claim full program savings.

Pilot decisions: exact service and Pega overlap; named owners and baseline/thresholds; Compass-specific data flow, operational and production acceptance. Historic intake sponsors and current issue assignees do not establish accepted accountability for this slice.

## Proposed slide 10 — Detailed Compass delivery roadmap

| Activity | Window | Delivery approach | Evidence to proceed |
| --- | --- | --- | --- |
| 0 — Prototype and scope | Dec 2026 | One journey; verify intent producer/checkpoint, Atlas fields, Pega overlap and supported interface. Review broader voice/CSR prototype separately. | Business, Genesys/PTP, Atlas/platform and delivery owners accept scope and contracts. |
| Readiness | Jan 2027 | Prove selected SDK/adapter or direct API; trusted identity, permitted reads, typed result and destination context. | End-to-end success, denied access, timeout, duplicate/cancelled and late-result behavior pass under realistic traffic. |
| 1 — MVP target | Feb 1–28, 2027 | Controlled initial population; context before routing; accepted destinations and human fallback. Self-service only if its separate dependencies are ready. | BSC launch acceptance, support, monitoring, rollback and agreed numeric thresholds. Schedule conflict remains explicit. |
| 2 — Intent releases | Mar–Jun 2027, monthly | Expand validated intent/context scope toward Top 20 ambition. Separate agent-assist features enter only with their own scope and acceptance. | Per-release context, wait, routing, continuity, quality and cost evidence. |
| Phase 2 discovery | Q2 2027, parallel | All-LOB routing design, Member/Provider/Broker digital context, enhanced callbacks and supervisory QM/queue/analytics scope. | Accepted pilot scope, journey signals, owners, capacity and measurable outcomes. |
| 3 — Selected pilots | Q3 2027 | Pilot agreed routing/context/callback/supervisory flows; validate exact Pega function transition where selected. | Pilot quality, service continuity, support and attributable value accepted. |
| 4 — Expand proven scope | Q4 2027, proposed | Scale eligible inbound populations and proven features; retire only accepted migrated Pega AI functions. | Sustained outcomes, operational ownership and transition evidence. |

Display the source's Mar–Apr pilot / May–Jun production conflict clearly below the detailed roadmap. Preserve outbound and additional-channel expansion as future, without implying that the PDF's full maturity Stage 4 is delivered in Q4 2027.

## Choices alternatives and exclusions

**Choice:** a staged Compass proposal with a clearly bounded first increment, while retaining the requested February target as explicitly unvalidated. It offers reuse and a measurable path to the wider vision. It does not claim Compass covers the Pega need until exact requirements are agreed.

**Material alternatives:** (1) move production to May–Jun to follow the export's sequence; the user explicitly selected retaining February and showing the conflict; (2) bundle interactive voice, summaries and coaching into the first release; this would erase the source's separate scope and require additional delivery estimates/acceptance; (3) keep the original Pega design; this remains a comparative requirements/transition reference but is outside the user's Compass substitution objective. No comparative price or capability advantage is asserted. (4) SDK/adapter versus direct API remain technical alternatives for engineering validation; the presentation does not choose an unverified architecture.

**Decision criteria:** correct authenticated data, existing supported call path, normal fallback, added wait, actual destination readiness, delivery capacity, operating cost, source/feature quality and attributable business value. Preserve call continuity when a dependency is unavailable. A reduced release scope requires explicit business acceptance; routing to an arbitrary unaccepted AI service is not an equivalent substitute.

**Exclusions:** whole-Pega/Shield Advisor replacement; blanket SDK/server/voice availability; autonomous case updates; automatic live-transcript use in the originally described Coach; universal call recording or inherited no-retention promises; medical/clinical decision making; assumed full Atlas domain/API coverage; all-LOB launch; full Avaya decommission prerequisite; promised savings; autonomous model training from transcripts; committed outbound, SMS or Apple Business Chat dates.

**Recording and learning:** PDF references to every conversation recorded once are a target-state design. Define actual coverage, retention, lawful access and context lifecycle before delivery. Transcript-derived new intents can be proposed for human review only under approved data use; no self-training mechanism is assumed.

## Risks dependencies owners and validation

**Primary risk:** February launch target conflicts with the source's proposed integration → shadow/pilot → production sequence. Trigger: missing named capacity, unsupported interface, unaccepted destination, unavailable fields/identity or failed quality/wait thresholds. Response: escalate the exact constraint to BSC and delivery owners for a scope/date decision; do not imply the gap is already solved.

Other triggers: incorrect/stale context, authorization failure, excessive added wait, faulty destination mapping, unusable CSR context or unproven feature readiness. Restrict affected scope, preserve Genesys human fallback and use accepted rollback/support procedures. Late/duplicate/cancelled requests must not alter completed routing. The data-only call and the interactive voice path require separate validation.

Proposed roles: BSC business owns journey/population, value thresholds and acceptance; Compass Product owns feature boundary and prioritization; Contact Center/Genesys/PTP owns supported invocation, policy enforcement, routing and commercial entitlement; Atlas/platform/identity owners own required fields/access/identity; engineering/delivery owners establish contracts, estimates, capacity and operational evidence; desktop owners own authorized CSR display; AI destination owners own receiving readiness; governance/security/privacy review the actual Compass design. Named accountability and funding remain open.

No product implementation is performed. The deck's acceptance is source fidelity, five executive slides plus appendix, intact Stellarus theme, editable content, source notes, February conflict visible on both roadmap slides, clear first-service versus adjacent-feature boundary, and no unsupported feature/date/savings claim. Validate by reimporting PPTX, checking source/feature/date text and structure, and visually inspecting every exported slide.

## Requirement traceability

| Requirement | Slides | Acceptance evidence |
| --- | --- | --- |
| Incorporate Notion export and briefing | 1–6 + notes | Bounded context service distinguished from platform vision; both source paths in notes. |
| Describe Compass features for intake needs | 2–3 + notes | Atlas/intent/context features, CSR knowledge, voice summaries and proposed guidance/drafting mapped with boundaries. |
| Preserve February target and flag conflict | 4, 6 | Feb 1–28 target plus Mar–Apr pilot / May–Jun source-plan production visibly stated. |
| Dec 2026–Q4 2027 roadmap and detailed approach | 4, 6 | Stage windows, parallel Q2 discovery, proposed Q3/Q4 pilots/scale and decisions to proceed. |
| Broader Phase 2 and future scope | 4, 6 + notes | Routing, digital journeys, callbacks, supervisory copilots; outbound/new channels undated. |
| BSC measures and economics | 5 + notes | First-service measures distinct from later business benefits; no unsupported numerical outcomes. |
| Consistent Stellarus and collaboration | All | Existing template/font/palette/logo; editable tables/text; source and discussion notes. |

F: Notion Markdown export, 11-page briefing, existing intake mapping and branded source deck inspected; this revised outline created. T: PM coherence/source/traceability review complete; deck construction and visual/structural validation remain to be performed. C: explicit first-service boundary reduces unsupported bundling; user retains February target with conflict disclosure; SCOPE DELTA: NONE. O: Markdown read, PDF text extracted and relevant pages inspected, existing builder/template inspected; no external, Git or product state changed.

Final artifact validation: six exported slides reopened and rendered; all six inspected at 1280×720 after the second refinement loop. Five native tables, six source-note pages, 49 editable text boxes, 182 valid package relationship targets, Geist/Geist Light fonts, source/feature/date coverage and archive integrity passed. The February target and Mar–Apr pilot / May–Jun production conflict are visible on both roadmap slides. No product behavior was changed or tested; feasibility and business/production approvals remain explicit planning dependencies, not claimed accomplishments. Final deck: `outputs/01a1b226-71b1-7090-817e-da53a9413d41/source-reconciled/output.pptx`.
