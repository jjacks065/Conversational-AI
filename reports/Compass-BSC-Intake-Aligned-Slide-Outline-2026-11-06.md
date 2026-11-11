# Compass for BSC Intake Aligned Executive Presentation

Revision date: November 6, 2026. Audience: BSC executives and service/product delivery stakeholders. Deliverable: five executive slides and a detailed roadmap appendix for use as the larger presentation's slide 10. Dates remain December 2026 through Q4 2027, as previously confirmed. This revision uses the actual intake exports and supersedes the earlier concepts-only narrative for the revised PPT.

## Evidence and positioning

**FACT — GAI-174:** the request is for Pega Voice AI integration through Audiohook, secure live audio streaming, APIs, architecture and operational readiness. Its business outcome is automated call summarization, fewer manual steps, improved summary quality, and more agent attention to member service. The February 6 risk review describes an assistive use case with human review of all summaries. The export status is Approved for Testing. Historical dates in the request are not adopted as Compass dates.

**FACT — GAI-663:** the request is for Knowledge/Content Buddy and Coach AI inside Shield Advisor. It asks for natural-language answers grounded in enterprise knowledge, knowledge/article retrieval, case/history summaries, relevant next actions, response drafting, and routine follow-up/documentation assistance. It identifies research and navigation delays, benefit-lookup effort, and agent training challenges. Measures include AHT, first-call resolution, research time, usability, adoption, accuracy/relevance, and security/access adherence.

**FACT — GAI-663 scope clarification:** July 31 comments state that customer-service knowledge is SMP procedural articles; case coaching uses configured business rules and deliberately supplied application context. Coach does not consume live audio, recordings, or transcripts in the described configuration. Notes may be deliberately supplied from the host application. Adding interaction summaries as a source would be additional configuration, not automatic behavior. The CSR remains the person interacting with the member. The export status is Approved for Testing; September 4 and 8 comments require test results and a production plan before separate Stellarus production approval.

**FACT — Compass product evidence:** the October product brief describes representative-assisted benefit inquiry with natural-language questions and structured, plan-specific answers grounded in validated customer data. Supplied plan context is required; the product does not independently match a member to a plan. Additional sources, domains, delivery integrations and workflows are deployment-specific or roadmap until integrated and validated. The implementation guide describes a joint discovery, data, identity, configuration, validation, pilot and production path. Neither document establishes that the requested BSC SMP, Shield Advisor, voice-summary, case-coaching or drafting integrations are currently delivered.

**USER DIRECTION:** propose Compass AI products in place of the Pega AI components, while retaining Shield Advisor as the desktop. Preserve the previously outlined inbound/self-service roadmap and delivery windows. This is a solution proposal and presentation revision, not authorization to implement product features or assert feature parity.

**INFERENCE:** BSC's strongest executive frame is agent productivity and member interaction quality, supported by a connected voice and desktop experience. Lead with research effort, summary work, guidance, and resolution, with self-service as a complementary roadmap outcome. Confidence: high in this interpretation of the two intakes, moderate in the proposed feature sequencing, and unvalidated in delivery feasibility.

## Feature mapping and capability boundaries

| Intake need | Proposed Compass response | Evidence boundary | Roadmap treatment |
| --- | --- | --- | --- |
| Live voice integration and conversational context, GAI-174 | Compass Voice audio integration, intent recognition and transcription | Proposed BSC scope from the user's roadmap. Audiohook is an interface to assess, not a mandatory architecture selection. | Prototype review in December 2026, then validate launch scope. |
| Automated call summaries and less manual effort, GAI-174 | Compass Voice drafts a structured summary for CSR review; intent and reviewed summary appear through CSR Chat in Shield Advisor | Requested outcome and proposed integration. No claim of existing writeback or approval to save data. | Validate data flow, review and writeback during readiness; Phase 1 intent/summary outcome. |
| Natural-language knowledge and benefit lookup, GAI-663 | Compass CSR Chat answers using approved plan data and, after integration, SMP procedures and other approved BSC content | Benefit Q&A is documented product foundation. SMP connection and source coverage require BSC-specific integration and validation. | December source-retrieval prototype, initial agreed scope in MVP; expand as sources validate. |
| Case/history context and next actions, GAI-663 | Proposed CSR Chat workflow assistance using approved case context and configured business rules | Proposed extension. No blanket Pega Coach equivalence and no automatic ingestion of host history, notes or transcripts. | Q1 discovery defines candidate scope and sequencing; no new delivery promise. |
| Draft responses, follow-ups and documentation, GAI-663 | Proposed CSR Chat drafting and case-summary assistance for human review | Proposed extension requiring source, workflow and writeback agreement. | Q1 discovery defines candidate scope for staged releases; release assignment remains open. |
| AHT, FCR, research effort, training, adoption and quality | Shared outcome scorecard across assisted calls and self-service | Intended benefits with no numerical performance claims. | Baseline before pilot and compare like-for-like cohorts after release. |
| Broader routing, digital journeys, callbacks and supervisory support | Phase 2 Compass routing, context, enhanced callbacks, and supervisory AI copilots | Additional roadmap concepts from the user, not evidence of GAI-663 CSR-coach functionality or current availability. | Q2 discovery, proposed Q3 pilots and Q4 expansion. |

## Executive slide 1 — Compass addresses BSC's agent productivity priorities

**Message:** propose Compass Voice and Compass CSR Chat in Shield Advisor to help CSRs find information, document calls, and guide member interactions.

**Features and value:** approved knowledge and benefit information through CSR Chat; voice transcription and draft summaries for CSR review; case and workflow guidance as a scoped extension. Present AHT/research time, first-call resolution, and onboarding/quality as BSC priority measures. The proposal replaces the requested Pega AI components, not the Shield Advisor desktop.

**Speaker notes:** GAI-174's immediate business objective is automated call summarization and summary quality. GAI-663 supplies the knowledge/navigation, coaching and agent-productivity language. Keep this broader than call deflection alone. Self-service remains in the roadmap but is not the full intake ask.

**Collaboration prompt:** confirm the priority agent workflows and pilot population with the business owner.

## Executive slide 2 — Compass Voice for live context and call summaries

**Message:** translate GAI-174 into a proposed Compass Voice feature and integration scope.

**Features:** recognize voice intent; transcribe live interactions; generate a structured call-summary draft; deliver intent and reviewed summary through CSR Chat in Shield Advisor. A CSR reviews and edits the summary before agreed writeback. Do not claim that an unreviewed draft automatically becomes an authoritative case record.

**Approach:** assess secure contact-center audio connectivity and APIs, validate transcription/summary quality with representative interactions, and agree desktop handoff and writeback. Audiohook is referenced in the original Pega request, not assumed to be the correct Compass design. The Compass design must establish what audio, transcripts, recordings and summaries are processed or retained and who may access them.

**Boundary:** live audio belongs to the proposed Voice workstream. The original GAI-663 Coach scope does not consume live audio/transcripts. An intentionally designed Compass connection between voice and desktop is new integration scope, not inherited Pega behavior.

**Additional roadmap scope:** inbound self-service and high-volume intent deflection are complementary user-proposed capabilities beyond the GAI-174 agent-assist request. Outbound voice remains future scope. Recording/transcription is in the supplied prototype concepts; that recording design requires its own retention agreement rather than adopting the source requestor's no-storage statement.

**Collaboration prompt:** agree the audio path, summary fields, review process, writeback destination, and recording/retention boundary.

## Executive slide 3 — Compass CSR Chat for knowledge and workflow support

**Message:** translate GAI-663 into a specific Compass agent experience, with boundaries visible.

1. Knowledge and benefit answers: natural-language questions, approved plan-specific benefit information, and SMP procedure retrieval after integration. Benefit Q&A is the documented foundation; SMP is BSC-specific source scope to validate.
2. Case and workflow guidance: deliberately supplied, approved case context and configured rules support suggested next actions. This is a proposed extension, not a currently proven Compass capability.
3. Response and documentation support: draft responses, follow-ups and case summaries for CSR review. Source permissions, output quality and any writeback are proposed implementation scope.

**Boundary:** the CSR remains responsible for member communication. Additional data/history sources require explicit agreement. Do not imply independent member-to-plan matching, direct clinical decisions, autonomous actions, or automatic use of all Shield Advisor/Facets information. Rule-based next actions are distinct from later predictive engagement and from supervisor/QM copilots.

**Acceptance examples for later scoping:** with an approved SMP source, a supported procedural question retrieves relevant content for CSR review; an unavailable/out-of-scope answer is limited or escalated. With intentionally supplied masked case context, guidance uses only approved fields and rules. A draft is presented for review, with no silent case update. These are proposed product acceptance examples, not implemented or tested behavior in this presentation task.

**Collaboration prompt:** confirm SMP source owners, plan scope, allowed case fields, initial guidance/drafting workflows, and the desktop integration owner.

## Executive slide 4 — One Compass roadmap connects the intake needs

**Stage 0, December 2026:** review the connected prototype: inbound voice, intent recognition, recording/transcription, BSC document retrieval, CSR Chat and Shield Advisor integration.

**Stage 1, February 1–28, 2027:** launch initial high-volume self-service intents with Compass as the first intent gateway and an agreed CSR handoff; deliver intent and summary through CSR Chat in Shield Advisor. January readiness is a proposed activity within this milestone, not an additional committed stage.

**Stage 2, monthly March–June 2027:** expand toward the top 20 self-service intents. Q1 discovery defines release scope and candidate knowledge, case-guidance and drafting extensions. Intake requests justify evaluating these features; they do not establish capacity, feasibility or an agreed delivery month.

**Phase 2:** Q2 discovery for all-LOB intelligent routing design and enhanced callbacks. Proposed discovery also defines digital journey context and supervisory workflows. Stage 3 Q3 pilots and Stage 4 Q4 expansion remain proposed allocations. Extend successful routing, Member/Provider/Broker digital journeys, scheduled callbacks and supervisory AI assistance for QM, queues and analytics. Predictive engagement is a candidate expansion where usable journey signals support it. Intended outcomes are fewer misroutes/transfers, improved first-contact resolution, less avoidable handle time, fewer repeat calls, improved member satisfaction and reduced manual supervisory effort. These are outcomes to measure, not verified benefits; the 12M+ annual call figure is contextual and unverified.

**Boundary:** CSR workflow coaching requested by GAI-663 is distinct from the later supervisory copilots. All-LOB design does not mean simultaneous all-LOB delivery. Preserve Phase 1 versus Phase 2 outcomes and the top-20 end-state rather than promising all 20 in February.

## Executive slide 5 — Success follows the BSC intake measures

**Outcome scorecard:** handling effort (AHT, research time, manual summary work); resolution/quality (FCR, answer accuracy, source relevance, summary completeness); agent readiness (time to proficiency and pilot feedback); adoption (live-call usage and repeated use); data/access (security, access and exposure incidents).

**Targets and measurement:** the source intakes specify improvement directions, not numerical goals. Baseline before launch and agree thresholds, review windows and cohort definitions with BSC. Proposed reviews are weekly during MVP and 30/60 days per release or pilot. Compare equivalent intents and case mix; report assisted-call results separately from self-service, since deflecting simpler requests changes the remaining CSR population. Monitor repeat contact, abandonment and satisfaction alongside speed. A recorded case update is not proof of a correct summary or resolved service need.

**Pilot decisions:** confirm named owners and pilot agents; agree baseline and success thresholds; approve Compass-specific data flow and production readiness. Kari Hayes is the Business Sponsor and Sonya Wade is the Use Case Driver listed in both exports; confirm current accountable assignments before baselining.

**Governance evidence:** GAI-663 says changes in data, integrations, users, model behavior or functionality require re-review, and the latest Stellarus comments require test results/production plan. Do not describe these Pega-design approvals as transferable Compass production authorization. The intake metadata marks Public Data, while GAI-174's risk review identifies PHI access in call audio and GAI-663's detailed discussion relies on source/field selection and masking. Actual Compass data flow must resolve this discrepancy. No assertion of PHI exclusion, no retention, HIPAA compliance, or training-data policy is independently validated here.

**Collaboration prompt:** agree pilot outcomes and decision thresholds before committing broader scope.

## Proposed slide 10 — Detailed Compass roadmap

| Activity | Timing | Delivery approach | Decision to proceed |
| --- | --- | --- | --- |
| Stage 0 prototype | December 2026 | Review voice, intent, transcription, approved-source retrieval and the Shield Advisor experience. | Agree refinements and MVP scope. |
| MVP readiness, proposed within Stage 1 | January 2027 | Validate audio path, SMP/benefit sources, access, summary review and desktop integration; baseline outcomes. | Confirm readiness and Compass-specific approval path. |
| Stage 1 MVP | February 1–28, 2027 | Initial supported high-volume intents and CSR intent/summary handoff. | Review launch performance and approve expansion. |
| Stage 2 expansion | Monthly March–June 2027 | Progress toward top-20 intents. Q1 discovery scopes candidate knowledge/coaching/drafting extensions. | Review each release's sources, quality, handoff and value. |
| Phase 2 discovery | Q2 2027, parallel | Design routing/callbacks and define digital context and supervisory workflows. | Agree pilot scope, dependencies, owners and measures. |
| Stage 3 pilots, proposed | Q3 2027 | Pilot routing, context/callbacks and supervisor assistance in selected populations. | Review value, service quality and support readiness. |
| Stage 4 expansion, proposed | Q4 2027 | Extend proven features to eligible queues, LOBs, journeys and channels. | Confirm continuing value and operating ownership. |

**Proposed owner model:** BSC sponsor owns business scope and investment. BSC Operations owns pilot acceptance and service performance. Compass Product owns scope translation and feature prioritization. Engineering and delivery owners establish feasibility and integration design. Contact-center/audio and Shield Advisor owners own the respective connection points. SMP/content and benefit SMEs own authoritative sources and answer quality. Quality, Security/Privacy and AI Governance confirm applicable evidence within their authority. Names and capacities require confirmation, not inferred assignment from historic vendor intake records.

**Dependencies and sequencing:** source access, approved audio/data paths, user access, summary review/writeback, appropriate environments, pilot users, training and support are launch prerequisites. Q2 discovery runs alongside intent expansion subject to actual team capacity. If a dependency fails, reduce the agreed population or revise sequencing with the business owner rather than asserting an equivalent substitute is ready.

## Decisions alternatives and risks

**Diagnosis and guiding policy:** BSC's intakes seek fewer manual steps and faster, more consistent member service. Propose Compass as the AI layer around the existing Shield Advisor workflow, using the documented CSR benefit-Q&A foundation and explicitly scoped voice, source and workflow integrations. Use measured pilot evidence before expansion.

**Alternatives:** the recommended staged Compass proposal offers product reuse but requires evidence that it meets the actual intake scenarios. Keeping the originally requested Pega AI path could retain platform-native functionality but does not meet the user's Compass substitution objective; no comparative price or performance judgment is asserted. Treating Compass as a naming-only replacement is rejected because integration, data flow and feature availability differ. Reducing the proposal to benefit Q&A alone would be closer to documented baseline but omit the voice-summary and coaching asks. Delivery scope can be revised after discovery if the broader features are not feasible.

**Explicit exclusions:** autonomous case updates, clinical decisions, outbound voice delivery commitments, wholesale replacement of Shield Advisor, all-LOB or all-portal simultaneous launch, inherited vendor approval, asserted feature parity, and unvalidated savings or performance guarantees.

**Confidence:** high in source extraction and requirement mapping; moderate in the solution narrative; unvalidated in implementation feasibility, source availability, staffing and feature readiness. The old slide 10 is still unavailable; its content is proposed rather than represented as a direct edit. Revisit the proposal if SMP access fails, summaries/guidance do not meet quality thresholds, desktop writeback is unavailable, or live-call data flows require a different authorized scope.

**Risk responses:** validate retrieval/answers and summary completeness against representative scenarios; restrict unsupported data and cases; require CSR review of draft communication and summaries; observe access failures and inappropriate exposure; preserve a human service path; pause or restrict affected features when agreed quality/service limits fail. These are scoped responses to the supplied intakes, not assertions that current Compass already implements every control.

## Validation and traceability

| Requirement | Revised slide(s) | Evidence or acceptance |
| --- | --- | --- |
| GAI-174 voice context and call summaries | 1, 2, 4, 6 | Voice feature scope, summary review, integration boundary and phase treatment. |
| GAI-663 knowledge, coaching and drafting | 1, 3, 4, 6 | Explicit feature groups, product foundation versus proposed extensions, source/case context boundaries. |
| BSC productivity and member service outcomes | 1, 5 | Intake-derived measures without invented targets. |
| Compass replacing proposed Pega AI products | 1–3 and notes | Compass Voice and CSR Chat are the proposed AI products; Shield Advisor remains the desktop. No parity/approval assertion. |
| Existing staged roadmap and dates | 4, 6 | December 2026, February 1–28 and monthly March–June 2027, Q2 discovery, proposed Q3/Q4 sequence. |
| Phase 2 features | 4, 6 and notes | All-LOB routing design; Member/Provider/Broker journeys; enhanced callbacks; supervisory QM, queue and analytics assistance. |
| Consistent Stellarus theme and collaboration | All | Reuse prior branded template, native editable content/tables, notes with sources and discussion questions. |

**F:** both HTML-formatted DOC exports inspected, current Compass product brief and implementation guide inspected as OOXML, this revised outline created. Primary source anchors are the named request fields and dated comments, not unavailable attachments.

**T:** content validation must check six slides, expected feature and date coverage, no stale statement that the intake exports are unavailable, capability/approval boundaries, editability, notes, and visual match. No product software behavior is changed or tested. The attachments listed in the exports are not supplied and are not represented as reviewed.

**C:** replaces the deflection-led framing with intake-led agent productivity and explicit Compass feature mapping, while preserving the user's roadmap. Source clarifications govern over broad initial feature lists for what was actually reviewed in the Pega use cases. SCOPE DELTA: NONE — presentation revision only.

**O:** identified DOC files as HTML; extracted both with the standard-library HTML parser after an optional BeautifulSoup dependency was unavailable; reviewed DOCX product sources through OOXML; authored source-to-feature mapping and slide plan. No external system, product implementation, Git or GitHub state is changed.
