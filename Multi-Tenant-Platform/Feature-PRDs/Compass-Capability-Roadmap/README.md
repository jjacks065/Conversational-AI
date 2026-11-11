# Compass Capability Roadmap — Feature PRD Set

**Authored Date:** August 7, 2026  
**CEI Assessment Date:** August 12, 2026  
**Status:** DRAFT  
**PDLC Phase:** Definition  
**Purpose:** Position Compass as a member-directed Personal Health Assistant and connect its foundational Member Journey to independently releasable capability milestones.

> **Roadmap direction, not a retroactive PRD sign-off (October 23, 2026).** The Member Journey foundation and C6 signature journey below are product decisions from discovery. The linked feature PRDs, original timeboxes, CEI scores, and release gates were authored for a narrower capability-first scope. Product and Engineering must reconcile their scope, estimates, evidence, and acceptance criteria before treating this expanded roadmap as a delivery commitment.

## Product Position and Strategy Kernel

**Position:** Compass earns trust through grounded help, then becomes a member-directed Personal Health Assistant across multiple concurrent care journeys. It remembers relevant context, offers timely assistance, coordinates with permission, and brings in people when a blocker exceeds its scope. The member chooses goals, engagement, cadence, proposed next steps, and journey closure.

**Diagnosis — FACT and INFERENCE:** The existing M0 PRD defines a Benefits Inquiry reference slice across Member and CSR surfaces, conversation continuity, Broker-governed actions, and GRR/Safe Handling evaluation. The six capability PRDs add discrete domain knowledge and actions. Those documented scopes are a credible answer-and-capability starting point. **Inference:** they do not yet specify the full member-owned journey behavior agreed in discovery. See [M0 scope](M0-Platform-Reference-Foundation-PRD.md) and the PRD index below.

**Guiding policy — PRODUCT DECISION:** Member Journey is the horizontal product foundation, established at M0 and matured by every interaction, capability, and feature set. Eligibility through Provider Scheduling remain whole, independently releasable domain increments; none is a substitute for the journey foundation. The baseline order remains C1 Eligibility, C2 Claims, C3 Accumulators, C4 Formulary, C5 Provider Lookup, C6 Provider Scheduling. Capability units may still be reordered as wholes without changing their acceptance semantics.

**Coherent actions — PROPOSED FOR PRD REBASELINE:**

1. Establish the M0 journey floor: visible member-owned journeys; member-defined goals; event history and provenance; choices for engagement, cadence, and consent; member-attested progress; proposed next steps; human escalation; and basic Progress/Trust instrumentation.
2. Require each C1–C6 release to demonstrate a complete, narrower member experience that advances the same journey foundation, including safe fallback and measurement.
3. Demonstrate the specialist-visit-plus-medication signature journey end to end at C6. Direct provider coordination is used where available and member-authorized; guided contact is the fallback. Provider and member retain treatment decision authority.

**Choice and exclusion:** Treating Member Journey as a seventh capability would delay the core product promise and leave C1–C6 as isolated transactions. The chosen horizontal model has a larger M0 scope and cross-team dependency cost. It does not authorize a broad migration, autonomous clinical advice, automatic member enrollment in outreach, or unreviewed PRD scope expansion.

## Member Journey Product Contract

- A member may have multiple concurrent journeys with different horizons: short acute care, finite multi-step care, and ongoing care. An event can complete without closing its journey. The member decides when care is complete and closes the relevant journey; a closing CSAT follow-up then asks separately about Compass support and goal attainment. Active, paused, and long-running journeys receive appropriately sampled pulse checks.
- Compass begins with a short, relevant invitation. The member may engage or self-manage. Care-signal personalization and outbound outreach are distinct choices; opting out of a journey does not imply failure. Engagement and cadence can grow only through member choice. Later, the member may grant revocable standing approval for routine checks and follow-ups within an already authorized request.
- Every automated routine check is visible in the journey with a transient, non-blocking notice. A result that changes future steps receives a persistent explanation. Compass may update its current understanding immediately, but new follow-ups remain proposed until the member accepts or adjusts them; new consequential actions require their own authority.
- The member's attestation advances journey progress immediately. Corroboration through available payer, provider, pharmacy, claim, or payment data updates provenance behind the scenes; it does not freeze progress. Conflicting accounts are preserved, never silently overwritten. A late or corrected event may revise the current view and future follow-ups without rewriting intervening history. Material discrepancies are surfaced when they affect a next step, access, or consequential decision.
- Member-shared barriers are optional to disclose, with a clear Skip path. Compass can reuse a prior choice as a hypothesis in a relevant future journey, then ask the member to confirm, change, or dismiss it. Journey shape informs a suggested cadence; complexity and the member's preferences remain separate dimensions, and the member can override the suggestion.
- CSR agents, case workers, or other accountable people enter a journey to clear a specific blocker, frustration, or complexity threshold, then exit. Member and Compass retain the coordination loop. Human teams oversee all active journeys through analytics and review rather than routine individual assignment. Resolution rules vary by reason and complexity, and the member can reopen any closed intervention.
- Compass can identify cost, coverage, authorization, and medication-access barriers and facilitate communication with payer and provider. It does not independently recommend treatment changes. Treatment remains guided by the provider in coordination with the member. Authorized direct coordination is preferred where provider technology supports it; otherwise Compass guides the member's contact and tracks the outcome.
- Authorized caregiver, representative, and POA participation is **deferred** for separate discovery of authority, permissions, visibility, and action rights. No proxy access is implied by the member journey model.

## Outcome and Measurement Tree

| Level | Measure | Proposed interpretation | Baseline and target | Guardrail / review |
| --- | --- | --- | --- | --- |
| Top-line outcome | **Member Progress** | Advancement against member-chosen goals and accepted next steps across active journeys; report episodic and ongoing journeys separately. | Net-new; instrument baseline before setting a numeric target. | Do not equate a closed event, a claim, or a long-running journey with success or failure by itself. Honor member attestation immediately and show source corroboration separately. |
| Top-line outcome | **Earned Trust** | Periodic and journey-close member pulse on control and confidence, interpreted with voluntary deeper engagement; the closure pulse can be integrated with support CSAT to limit survey burden. | Net-new; instrument baseline before setting a numeric target. | Report response rate; sample stuck, paused, and removed journeys so positive closures do not dominate. Engagement volume alone is not trust. |
| Quality gate | **Grounded Resolution Rate** | Correctly resolved eligible inquiry episodes with independently adjudicated evidence. | Existing proposed release target: ≥95% on eligible evaluation scenarios; production baseline still to be measured. | Report eligibility, volume, sampling confidence, and Safe Handling separately. GRR is the resolution-quality layer, not the whole product outcome. |
| Journey operations | Time to next verified step, time to accountable human, intervention reopen rate, and time blocked | Diagnose friction and trust recovery in a specific journey. | Baselines and targets require instrumentation and operational validation. | Segment by journey type, cohort, source availability, and member-selected assistance level. |
| Closure | Compass-support CSAT and member-rated goal attainment | Two distinct questions after member-confirmed closure. | Net-new; baseline and target to be set after sampling design. | Do not attribute the full clinical outcome to Compass; keep ongoing-journey pulses visible. |

**Measurement owner:** Product defines the member outcome and survey semantics; AI Quality owns GRR adjudication; Operations owns escalation and service-time review; Engineering validates event instrumentation and source reconciliation. Targets for new journey measures remain deliberately unset until a baseline and measurement window are approved.

**Proposed learning window and target decision:** Use the first 30 days of an approved cohort to establish separate baselines for short, finite multi-step, and ongoing journeys; include paused/stuck journeys and publish pulse response rates. Product Analytics and Operations then propose numerical Progress, Trust, and closure targets for Product approval. Until that decision, improvement versus the observed baseline is the directional objective, not a fabricated launch gate.

## Journey Maturity Across the Whole-Capability Roadmap

| Milestone | Complete member value in that increment | Horizontal journey maturity / acceptance evidence to add at PRD rebaseline |
| --- | --- | --- |
| **M0 — Member Journey foundation + Benefits Inquiry** | Resolve a supported benefits question across Member and CSR while starting, viewing, adjusting, or declining a member-owned journey. | Demonstrate goals, events/provenance, choices/cadence, member-attested progress, proposed steps, human intervention, and Progress/Trust instrumentation alongside the existing governed Surfaces → Spine → Brain contract. |
| **C1 — Eligibility** | Understand coverage status and timing for an upcoming care step. | Carry eligibility evidence into the relevant journey, explain uncertainty, and propose an accepted next step without making the journey depend on another domain capability. |
| **C2 — Claims** | Understand a post-care claim and what, if anything, needs attention. | Add claim events and member attestation without overwriting conflicting accounts; keep follow-up and human recovery visible. |
| **C3 — Accumulators** | Understand deductible and out-of-pocket position while planning care. | Relate cost context to member goals and proposed steps, with effective-date provenance and no unsupported price promise. |
| **C4 — Formulary** | Understand coverage and access rules for a prescribed medication. | Begin a medication-access thread through first fill, refills, and provider-directed adjustments as data and permissions permit; never originate a treatment recommendation. |
| **C5 — Provider Lookup** | Find relevant, current provider options for a stated need. | Connect choices to member preferences and journey goals, preserving source freshness and member control. |
| **C6 — Provider Scheduling** | Safely coordinate an appointment, with guided contact when direct integration is unavailable. | Demonstrate the specialist-visit-plus-medication journey end to end across preparation, visit, access/fill, follow-up, human help, member-confirmed closure, and separate CSAT/goal-attainment follow-up. |

**Whole-increment acceptance pattern:** For at least one representative journey scenario per milestone, show (1) member choice and goal, (2) grounded domain help or authorized action, (3) visible event/progress update, (4) a member-controlled proposed next step, (5) a safe stuck/escalation path, and (6) outcome telemetry. Existing capability quality gates still apply. This is a proposed product acceptance overlay; the detailed PRDs have not yet been amended or re-estimated.

**Dependencies and risks:** M0 expansion depends on product/engineering re-estimation and consent, event, provenance, and operational ownership contracts. Provider connectivity will vary, requiring a guided-contact fallback. Member attestation and later source records can disagree; the product must preserve both and explain material differences. Trust can be damaged by excessive outreach or invisible automation; member choice, activity visibility, and pulse sampling are guardrails. Clinical governance must review medication and treatment boundaries. Product, Platform Engineering, Domain Owners, Clinical Governance, and Customer Operations should jointly sign off the rebaselined acceptance criteria before a cohort release.

### Requirement-to-outcome traceability for the PRD rebaseline

| Product requirement | Outcome served | Representative acceptance evidence |
| --- | --- | --- |
| J-01 — Member control of goals, engagement, cadence, next steps, and closure | Earned Trust; voluntary engagement | Member can accept, decline, adjust, pause, or close the relevant journey; new consequential actions do not inherit a routine-check grant. |
| J-02 — Visible concurrent journeys with member attestation and source provenance | Member Progress; grounded continuity | Member-reported progress appears immediately; later corroboration changes provenance, not history; conflicts remain visible when consequential. |
| J-03 — Bounded human intervention in the continuing Compass/member loop | Trust recovery; time to accountable human | A stuck or out-of-control signal prompts immediate re-evaluation or threshold-based human help; when a human joins, owner/status is visible; the member can reopen a closed intervention. |
| J-04 — Capability-aware payer/provider coordination | Time to next meaningful step; safe handling | Member-authorized direct exchange works where available; guided contact works when not; no model-originated treatment change is offered. |
| J-05 — Member-confirmed journey closure with two-question follow-up | Closure CSAT; goal attainment | Member closes a completed-care journey; Compass separately captures satisfaction with its support and whether the member's goal was achieved. |
| J-06 — Whole journey-shaped release evidence at every milestone | Member Progress; GRR; operational readiness | At least one representative end-to-end scenario per milestone meets all six whole-increment elements above and existing quality gates. |

### Pre-mortem and decision triggers

| Scenario | Trigger to inspect | Mitigation / decision owner |
| --- | --- | --- |
| Expanded M0 journey floor does not fit the inherited eight-week PRD scope. | Engineering cannot estimate or demonstrate a required floor behavior within the proposed cohort/timebox. | Product and Platform Engineering rebaseline the milestone explicitly; do not silently remove member control, provenance, or human recovery from the promise. |
| Provider connectivity cannot support direct coordination. | No approved interface, authorization path, or reliable response for the target provider cohort. | Provider Operations and Product validate a guided-contact path with visible follow-up before cohort release. |
| Progress and trust reporting overstates success. | Closure-only samples, low pulse response, or short journeys dominate portfolio averages. | Product Analytics stratifies by journey shape and status, reports response rate and member-attested advancement, and samples stuck/paused journeys. |
| Automation creates surprise or clinical overreach. | Member complaints, opt-outs, unexplained next-step changes, or treatment-related agent suggestions. | Product, Operations, and Clinical Governance tighten action scopes, make changes persistent and explainable, and route treatment decisions back to provider/member. |

**Confidence and decision triggers:** Product-direction confidence is high because the member-control, journey, clinical-boundary, and milestone choices were explicitly confirmed in discovery. Delivery confidence is low until Engineering validates the expanded M0 timebox, provider/payer source availability, action policy, data model, and operations capacity. Revisit the M0 floor or the C6 end-to-end acceptance point if an essential journey behavior cannot be delivered safely within the approved cohort or if provider connectivity makes direct coordination infeasible; preserve guided contact as the baseline fallback rather than silently narrowing the member promise.

## PRD Index

| Milestone | Feature PRD | Draft timebox | Initial supported surfaces | CEI | Priority tag |
| --- | --- | ---: | --- | ---: | --- |
| M0 | [Platform Reference Foundation](M0-Platform-Reference-Foundation-PRD.md) | 8 weeks | Member Chat, CSR Chat | 75 | `cei-strategic` |
| C1 | [Eligibility](C1-Eligibility-PRD.md) | 6 weeks | Member Chat, CSR Chat, Provider Chat | 60 | `cei-strategic` |
| C2 | [Claims](C2-Claims-PRD.md) | 6 weeks | Member Chat, CSR Chat, Provider Chat | 60 | `cei-strategic` |
| C3 | [Accumulators](C3-Accumulators-PRD.md) | 5 weeks | Member Chat, CSR Chat | 50 | `cei-opportunistic` |
| C4 | [Formulary](C4-Formulary-PRD.md) | 6 weeks | Member Chat, CSR Chat, Provider Chat | 60 | `cei-strategic` |
| C5 | [Provider Lookup](C5-Provider-Lookup-PRD.md) | 6 weeks | Member Chat, CSR Chat; Provider Chat when enabled | 60 | `cei-strategic` |
| C6 | [Provider Scheduling](C6-Provider-Scheduling-PRD.md) | 8 weeks | Member Chat, CSR Chat; Provider workflows when enabled | 65 | `cei-strategic` |

The order above is the baseline delivery sequence. Reordering a capability changes sequence only; it must not change the capability's product scope, acceptance criteria, or reliance on the versioned platform contract.

The PRD links and CEI table below preserve their **August 2026 authored state** for traceability. Their timeboxes, scores, and detailed acceptance criteria have **not** been recalculated for the October Member Journey direction.

## CEI Ranked Comparison

CEI scores use the canonical CEI 1.0 formula `10C + 10I + 5E`. All assessments have **medium overall confidence** because the capabilities are net-new and the authored timeboxes still require engineering validation.

| CEI rank | Milestone | Score | Dimensions | Tag | Ranking rationale |
| ---: | --- | ---: | --- | --- | --- |
| 1 | M0 — Platform Reference Foundation | 75 | C3 I4 E1 | `cei-strategic` | September 1, 2026 committed MVP; portfolio-enabling foundation; large multi-team delivery. |
| 2 | C6 — Provider Scheduling | 65 | C2 I4 E1 | `cei-strategic` | Transformative move from information to governed transactions, offset by large operational complexity. |
| 3 | C1 — Eligibility | 60 | C2 I3 E2 | `cei-strategic` | High-value cross-surface coverage context; first baseline capability after M0. |
| 4 | C2 — Claims | 60 | C2 I3 E2 | `cei-strategic` | High-value claims explanation across three surfaces; roadmap order breaks the CEI tie. |
| 5 | C4 — Formulary | 60 | C2 I3 E2 | `cei-strategic` | High-value pharmacy coverage workflow with explicit safety boundaries. |
| 6 | C5 — Provider Lookup | 60 | C2 I3 E2 | `cei-strategic` | High-value search workflow and portable ProviderReference; roadmap order breaks the CEI tie. |
| 7 | C3 — Accumulators | 50 | C2 I2 E2 | `cei-opportunistic` | Useful but initially bounded to two surfaces and one cohort, with no reach baseline yet. |

**Sequencing interpretation:** CEI is decision guidance, not implementation approval and not a replacement for the accepted milestone sequence. C6 scores above C1–C5 because of its portfolio-level transactional impact, but remains sixth in the delivery plan so the platform can harden context, precision, retrieval, and action safety through earlier whole-capability releases.

### Re-score Triggers

- Promote a C1–C6 Category from C2 to C3 only when a funded commitment, accountable owner, or delivery date is recorded.
- Reassess Impact when baseline inquiry volumes, affected populations, or production KPI movement become available.
- Reassess Effort after engineering validates the end-to-end estimate, source integration, security review, QA, rollout, and operational load.
- Preserve the prior score, assessment date, evidence, and decision owner when a score changes.

## Shared Product Model

```text
Member Journey foundation (M0 → C1–C6): goals · events · choice · attestation · proposed steps · human help · Progress/Trust

Surfaces                           Spine                                  Brain
Member / CSR / Provider  →  Auth → Agent Broker → AI Agents  →  Governed knowledge services
persona + presentation      context + routing + policy + actions      provenance + freshness
```

- **Surfaces** own persona-specific presentation, interaction policy, and channel behavior.
- **The Spine** owns trusted actor/subject context, capability routing, conversation state, policy enforcement, action execution, and telemetry.
- **Capability agents** interpret the inquiry, request permitted Brain data, and return the standard response contract.
- **The Brain** owns governed data access, source authority, freshness, provenance, and deterministic business data.
- **Structured answers are the default.** Surface and tenant configuration may render approved less-structured or unstructured variants without changing the underlying evidence or outcome.
- **Surface-initiated actions are always supported.** Agent-recommended actions are optional by agent configuration. The Broker alone authorizes and executes side effects.
- **Member Journey spans all three layers.** Surfaces make the journey and controls visible; the Spine governs continuity, permissions, and actions; the Brain supplies source-backed context. The member's attestation remains a first-class progress signal even when source corroboration is pending.

## Shared Measurement Definitions

The top-line product outcomes are Member Progress and Earned Trust as described above. GRR and Safe Handling remain necessary inquiry-quality and safety gates, not substitutes for journey progress or the member's experience.

### Grounded Resolution Rate

`GRR = eligible inquiries resolved correctly with sufficient source evidence / all eligible inquiries`

The numerator requires factual correctness, appropriate actor/subject context, current source data, provenance, and a usable response. Clarifications, abstentions, escalations, and failures are not counted as grounded resolutions.

### Safe Handling Rate

`Safe Handling Rate = turns correctly resolved, clarified, abstained, escalated, or safely failed / all evaluated turns`

Safe Handling is reported separately from GRR so appropriate abstention does not inflate product resolution.

### Required Turn Outcomes

Every turn emits exactly one terminal product outcome:

- `resolved_grounded`
- `clarification_required`
- `safe_abstention`
- `action_initiated`
- `escalated`
- `failed`
- `cancelled`

## Common Exit Gates for Every Milestone

These gates are repeated in each PRD's exit criteria and are non-negotiable unless the program steering group records an explicit exception:

1. At least 100 representative evaluation scenarios approved by Product, Operations, and the relevant domain owner.
2. GRR target of at least 95% on eligible scenarios.
3. Safe Handling target of at least 99% across the complete evaluation set.
4. 100% of successful answers include source provenance and freshness/as-of evidence.
5. 100% of evaluated turns emit one defined terminal outcome.
6. Zero cross-tenant data access in automated isolation testing.
7. Zero critical unsupported factual claims in launch evaluation.
8. 100% of side-effect actions are authorized, confirmed, idempotent, and audited.
9. Capability SLOs, runbook, cohort plan, rollback procedure, and owner sign-off are complete before release.

## Current-State Evidence Used in These Drafts

- `agentic-broker-api` already supports tenant-scoped resolver dispatch and an explicit `benefits.query` capability path; current source comments still identify durable conversation continuity as deferred work.
- `agentic-broker-chat` already passes a capability field and contains escalation flows that dispatch through the Broker.
- CSR Chat is live from `stellarus-ai/apps/csr-chat`, uses structured benefits plan data, and has an in-flight CCS context-token / Benefits Service integration path.
- Benefits Service provides customer-partitioned plan reads and coverage checks with audit logging, but deliberately does not resolve member eligibility or member-to-plan association.
- UM Composite exposes a current Enterprise Eligibility integration that can inform C1's governed Brain adapter.

These observations were recorded for the August 2026 PRD drafts and require re-verification against the current repositories before technical commitment. They establish a credible starting point; they do not preselect the final runtime, service ownership, or source contract for every capability.

## Draft Assumptions Requiring Validation

- The first release of each PRD targets one approved tenant cohort and the listed surface profiles, not unrestricted enterprise rollout.
- Production source access, representative non-production data, and domain-owner availability are secured by the end of Week 1.
- Each capability is delivered through a versioned manifest, input/output schema, tool policy, and response contract.
- One primary capability is selected per turn. Cross-capability composition is optional and may not be required to complete a supported journey.
- Unknown metric baselines are measured against a frozen pre-release evaluation set during Week 1. Targets are release gates; baseline results are added before Build & Integrate sign-off.
- Accessibility conformance target is WCAG 2.2 AA for surface-rendered responses and controls.

## Program Decisions Still Open

| Decision | Needed by | Decision owner |
| --- | --- | --- |
| Initial tenant cohort and named surface owners for each milestone | Planning start | Product + Customer Operations |
| Production SLO values by capability and source system | End of Week 1 | Platform + Domain Engineering |
| Authoritative Claims, Accumulator, Formulary, Directory, and Scheduling services | Before each capability's Build & Integrate phase | Enterprise Architecture + Domain Owner |
| Standard response schema version and compatibility policy | M0 Week 2 | Product + Platform Architecture |
| Evaluation review and severity policy for unsupported claims | M0 Week 2 | AI Quality + Clinical/Domain Governance |
| Whether agent-recommended actions are enabled by tenant and capability | Before each capability cohort | Product + Risk/Operations |
| Rebaseline M0 scope, timebox, CEI, and cohort exit criteria against the approved Member Journey floor | Before approving revised M0 delivery | Product + Platform Engineering + Operations |
| Define journey event/provenance contract, member control semantics, and material-discrepancy threshold | M0 product/technical design | Product + Platform Architecture + Privacy/Clinical Governance |
| Validate the C6 specialist-plus-medication end-to-end acceptance scenario, including fill/refill data and guided-contact fallback | Before C6 commitment | Product + Domain Owners + Provider Operations |
| Establish baselines, windows, and targets for Member Progress, Earned Trust, closure CSAT, and goal attainment | Before publishing journey outcome targets | Product Analytics + Operations |
