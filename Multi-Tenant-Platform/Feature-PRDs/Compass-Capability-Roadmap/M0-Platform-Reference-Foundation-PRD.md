# 🧩 Project Name: M0 — Compass Platform Reference Foundation

**PDLC Phase:** Definition  
**Authored Date:** August 7, 2026  
**Status:** DRAFT  
**Timebox:** 8 weeks  
**MVP Target Date:** September 1, 2026  
**CEI Priority:** `cei-strategic`  
**CEI Score:** 75/100 — C3 I4 E1  
**CEI Confidence:** Medium  
**CEI Assessment Date:** August 12, 2026  
**CEI Framework:** CEI 1.0  
**Roadmap Position:** M0 — required platform foundation  
**Initial Cohort:** One approved tenant across Member Chat and CSR Chat  
**Accountable Product Owner:** TBD — Compass Platform  
**Required Decision Owners:** Platform Engineering, AI Engineering, Identity, Benefits Service, Member Experience, CSR Experience, Operations, Security

## CEI Prioritization

**CEI: `cei-strategic` | 75/100 | C3 I4 E1 | confidence: medium**

**Decision:** Maintain M0 as the September 1, 2026 MVP commitment and require explicit delivery or decommit governance. The phrase “critical first step” does not qualify as CEI Category 4 without a verified safety, legal, regulatory, security, privacy, material-financial, or production-continuity obligation.

| Dimension | Class | Value | Points | Confidence | Rationale and evidence |
| --- | --- | :-: | ---: | --- | --- |
| Category | Committed / Time-bound | 3 | 30 | High | The user confirmed the September 1, 2026 planned MVP date, and M0 is the required foundation for the accepted roadmap. |
| Impact | Transformative | 4 | 40 | Medium | M0 establishes the shared Surfaces → Spine → Brain product contract, delivers Benefits Inquiry across Member and CSR, and enables C1–C6. Targets include ≥95% GRR, ≥99% Safe Handling, and complete outcome/provenance telemetry. |
| Effort | Large | 1 | 5 | Medium | The eight-week scope spans Platform, AI, Identity, Benefits Service, two surfaces, Security, evaluation, and operations. The timebox is understood but awaits engineering validation. |

**Category floor:** C3 has a minimum `cei-strategic` tag. No override was needed because the numeric score already falls in the strategic band.

```yaml
category_effort_impact:
  status: final
  tag: cei-strategic
  score: 75
  score_range: null
  category:
    value: 3
    classification: committed-or-time-bound
    weighted_points: 30
    confidence: high
    rationale: "M0 is the planned September 1, 2026 MVP and the required foundation for the accepted capability roadmap."
    evidence: "User-confirmed MVP date; Roadmap Position and Delivery Plan in this PRD."
  impact:
    value: 4
    classification: transformative
    weighted_points: 40
    confidence: medium
    rationale: "Creates the portfolio-level Compass contract and enables reusable capability delivery across Member and CSR surfaces."
    evidence: "Product Goals; Success Metrics; M0 work packages M0-01 through M0-12."
  effort:
    value: 1
    classification: large
    weighted_points: 5
    confidence: medium
    rationale: "Eight-week, multi-team foundation spanning identity, broker, agent, Brain integration, surfaces, security, telemetry, and operations."
    evidence: "Authored eight-week timebox and task-ready work packages; engineering validation remains pending."
  category_floor:
    applied: false
    reason: "C3 minimum is cei-strategic; the 75-point score already maps to cei-strategic."
  assumptions:
    - "September 1, 2026 remains the accepted MVP date."
    - "One approved tenant can access the required identity, Benefits Service, and surface environments."
  open_questions:
    - "Which accountable owner accepts the final end-to-end engineering estimate and delivery risk?"
    - "What baseline inquiry volume and operational KPI will quantify production reach?"
  next_action: "Validate the eight-week estimate and named ownership without changing the September 1 commitment silently; re-score if scope or obligation changes."
```

## 🎯 Problem Statement

Members and CSRs can ask benefits questions today, but the working experience and platform components do not yet operate as one consistent, governed product contract. The current estate contains useful pieces—tenant-scoped Broker resolution, a `benefits.query` route, a live CSR Chat agent, CCS context-token work, and customer-partitioned Benefits Service APIs—but capability selection, durable conversation state, response structure, provenance, terminal outcomes, and operational gates are not yet uniformly enforced across Member and CSR surfaces.

This fragmentation means the same inquiry can be authenticated, routed, answered, measured, and escalated differently by surface. It also makes each new healthcare domain likely to reproduce auth, retrieval, response, and telemetry logic instead of extending a stable platform.

**Current-state evidence:**

- Broker code supports resolver dispatch using capability plus tenant context, but durable conversation continuity is identified as deferred.
- CSR Chat's multi-customer path is moving toward CCS context verification and Benefits Service reads; base auth behavior remains compatibility-configurable.
- Benefits Service can return governed customer-plan data and audit reads, but callers still resolve the applicable member plan/product.
- Existing chat responses are primarily content strings rather than a consistent product-level evidence, outcome, and action envelope.

**Impact:** Without M0, C1–C6 cannot be independently released through shared contracts. Product quality remains difficult to compare across surfaces, unsafe or unsupported answers are harder to detect, and CSR Chat convergence becomes a series of bespoke integrations rather than a repeatable platform pattern.

**Baseline:** A comparable cross-surface GRR, Safe Handling Rate, provenance rate, and typed-outcome rate are not consistently available. Week 1 establishes the frozen baseline set and publishes the measurements before implementation scope is finalized.

## 💡 Proposed Solution

Productize Benefits Inquiry as the Compass reference capability across Member Chat and CSR Chat. Both surfaces will submit a versioned request through the Spine; the Broker will establish trusted actor, subject, tenant, authorization, and conversation context; route explicitly or infer `benefits.query`; invoke a configured benefits agent; govern Benefits Service access; and return one standard response envelope.

The response envelope will make structured answers the default while allowing approved surface response profiles. It will contain the answer, evidence, freshness, confidence/limitations, clarification state, optional action proposals, and exactly one typed terminal outcome. The Broker will own action authorization and execution, even when an agent recommends an action under configuration.

M0 is complete when Benefits Inquiry operates as a measurable, supportable reference path—not merely when the APIs connect.

## 👥 Target Users

**Primary Users:**

* **Member Chat user:** Needs a clear, plan-specific benefits answer with understandable limitations and next steps.
* **CSR Chat user:** Needs the same grounded answer plus service-oriented detail appropriate to an authenticated representative workflow.

**Secondary Users:**

* **CSR supervisor and operations analyst:** Needs traceable outcomes, escalation visibility, and cohort health.
* **Surface product teams:** Need stable request/response contracts and configurable rendering without duplicating capability logic.
* **Capability and Brain service teams:** Need explicit tool permissions, input contracts, and source provenance requirements.
* **Security, privacy, and compliance reviewers:** Need auditable tenant, actor, subject, and authorization enforcement.

## Product Goals and Non-Goals

### Goals

1. Prove one end-to-end Compass capability across two distinct surfaces.
2. Establish versioned platform contracts reusable by C1–C6.
3. Make grounded quality and safe handling measurable at turn, conversation, surface, tenant, capability, agent, and contract version levels.
4. Preserve CSR-specific presentation and workflow policy while converging its platform path.
5. Demonstrate cohort release and rollback without affecting disabled tenants or surfaces.

### Non-Goals

1. Replace or redesign all legacy CSR functionality and telemetry.
2. Deliver Eligibility, Claims, Accumulators, Formulary, Provider Lookup, or Scheduling.
3. Enable cross-capability planning or multi-agent orchestration as a launch requirement.
4. Permit an AI agent to execute side effects directly.
5. Select one response style for every surface; only the underlying contract is standardized.

## Supported User Journeys

| Journey | Expected behavior |
| --- | --- |
| Member asks a plan benefits question | Infer or accept `benefits.query`, resolve authorized plan context, retrieve governed plan evidence, return a member-readable structured answer with source and as-of data. |
| CSR asks the same question on behalf of a member | Preserve actor and subject separately, enforce representative authorization, return a CSR response profile with the same underlying evidence. |
| Inquiry lacks plan, date, or benefit detail | Ask the minimum necessary clarification and emit `clarification_required`; do not fabricate a likely answer. |
| Source data is missing, stale, contradictory, or unavailable | Return a safe limitation, abstention, or escalation path with a typed outcome and observable dependency status. |
| Surface requests escalation | Broker retrieves and redacts the permitted conversation context, authorizes the escalation request, and records an audited outcome. |

## ✅ Success Metrics

| Metric | Baseline | Release target | Measurement window and source |
| --- | --- | --- | --- |
| Benefits Inquiry Grounded Resolution Rate | Establish in Week 1 on frozen cross-surface evaluation set | ≥95% of eligible scenarios | Pre-release evaluation and first 30 days of cohort traffic; reviewed weekly by AI Quality and Product |
| Safe Handling Rate | Establish in Week 1; current cross-surface value unavailable | ≥99% across all evaluated turns | Frozen evaluation set plus adjudicated production sample; includes correct clarify/abstain/escalate behavior |
| Contract and telemetry completeness | Current platform paths do not uniformly emit the target fields | 100% of evaluated turns include contract version, capability/agent identifiers, provenance/freshness when resolved, and one terminal outcome | Automated schema validation and telemetry reconciliation for 30 days |

**Guardrail metrics:** zero cross-tenant access; zero critical unsupported factual claims; no raw context token in application logs; P95 response latency and availability SLO approved before cohort release.

## 📦 Scope

### Task-Ready Work Packages

| ID | Deliverable | Start condition | Completion evidence | Estimate |
| --- | --- | --- | --- | ---: |
| M0-01 | Benefits Inquiry taxonomy and eligibility rules | Product/domain workshop scheduled | Approved intent, entity, clarification, and unsupported-topic catalog | 3 days |
| M0-02 | Versioned capability manifest | Taxonomy approved | `benefits.query` manifest defines supported inputs, output schema, agent/runtime, tools, permissions, and response profiles | 4 days |
| M0-03 | Surface profiles for Member and CSR | Response contract draft available | Persona-specific presentation, detail, disclosure, and action policy accepted by both surface owners | 4 days |
| M0-04 | Trusted context envelope | Identity claims confirmed | Actor, subject, tenant, persona, scopes, consent/delegation, locale, correlation, and effective-date context validated end to end | 5 days |
| M0-05 | Persistent conversation state | Context envelope stable | Conversation can resume across supported turns with capability, clarification, evidence, and outcome history retained per policy | 5 days |
| M0-06 | Explicit and inferred routing | Taxonomy and manifest available | Explicit selection and inference both choose one primary capability; ambiguous or unsupported routes fail safely | 5 days |
| M0-07 | Benefits Brain tool policy | Benefits Service contract confirmed | Broker-governed read tools enforce scopes, tenant context, input validation, timeout, provenance, and freshness capture | 5 days |
| M0-08 | Benefits agent runtime adapter | Tool policy and schema available | Configured agent accepts normalized context and returns schema-valid candidate responses; runtime is replaceable by manifest | 5 days |
| M0-09 | Standard response and outcome envelope | Surface profiles approved | Structured answer, evidence, freshness, limitations, proposed actions, render hints, and one typed outcome validate against v1 schema | 5 days |
| M0-10 | Broker-controlled escalation action | Conversation state and auth available | Surface can request escalation; optional agent recommendation is configuration-gated; Broker authorizes and audits execution | 4 days |
| M0-11 | Telemetry and evaluation harness | Contract identifiers stable | Turn/outcome traces, source events, GRR/Safe Handling scoring, and ≥100-scenario suite available by version | 5 days |
| M0-12 | Cohort controls and operations | SLOs drafted | Tenant/surface/version enablement, runbook, dashboards, alerting, rollback, and post-release sampling approved | 5 days |

Work packages are parallelizable across Platform, AI, Surface, and Operations teams. Any package estimated above five engineering days must be decomposed during planning without weakening its completion evidence.

### Functional Requirements

1. **M0-FR-01 — Trusted request context:** The Spine must derive tenant, actor, subject, persona, scopes, and correlation from verified context; untrusted request fields may not override them.
2. **M0-FR-02 — Actor/subject separation:** CSR requests must retain the representative as actor and the member as subject throughout policy checks, Brain calls, telemetry, and audit.
3. **M0-FR-03 — Capability selection:** A turn may specify a capability or request inference. The Broker must select exactly one primary capability or return clarify/unsupported behavior.
4. **M0-FR-04 — Version control:** Capability, agent, prompt/configuration, tool policy, response schema, and surface profile versions must be observable on every turn.
5. **M0-FR-05 — Conversation continuity:** The conversation store must preserve supported context across turns and prevent tenant, actor, or subject context from leaking between sessions.
6. **M0-FR-06 — Governed retrieval:** Agents may request Benefits Service data only through Broker-authorized tools using the trusted tenant and plan context.
7. **M0-FR-07 — Evidence:** Resolved answers must identify source service, source record/version or request reference, retrieval time, applicable effective date, and as-of/freshness status.
8. **M0-FR-08 — Response defaults:** The agent must produce the structured v1 envelope. Surfaces may render approved variants but may not remove required safety, provenance, or action-confirmation information.
9. **M0-FR-09 — Safe fallback:** Missing, conflicting, unauthorized, stale, or unavailable data must trigger an approved clarification, abstention, escalation, or failure outcome.
10. **M0-FR-10 — Actions:** Surfaces may request configured actions. Agents may recommend configured actions. Only the Broker may authorize and execute them.
11. **M0-FR-11 — Terminal outcome:** Every completed turn must persist exactly one value from the shared outcome taxonomy.
12. **M0-FR-12 — Enablement:** Tenant, surface, capability, agent recommendation, response profile, and contract version must be independently configurable.

### Experience Requirements

- A structured answer must clearly separate the direct answer, supporting benefit details, effective/as-of information, source, limitations, and next action.
- Member and CSR variants must retain factual equivalence for the same authorized context.
- Clarification asks one decision-relevant question at a time unless multiple fields are inseparable.
- Streaming or progressive rendering must not present unsupported factual content as final.
- Keyboard, screen-reader, focus, contrast, and status announcements must meet WCAG 2.2 AA on both reference surfaces.

### Analytics Requirements

Every turn records: tenant, surface, persona, actor type, subject type, conversation ID, turn ID, correlation ID, capability/version, route method, agent/runtime/version, Brain tools called, source/freshness metadata, response profile, outcome, latency, token/cost metrics where allowed, action proposal/execution state, error class, and evaluation linkage. Sensitive identifiers must be pseudonymized or excluded per policy.

## 🚫 Out-of-Scope

* **Additional healthcare capabilities:** Deferred to C1–C6 so M0 remains an eight-week reference release.
* **Full legacy CSR Chat retirement:** Convergence is proven for Benefits Inquiry; unrelated CSR functions remain on their current path until separately planned.
* **Unrestricted tenant rollout:** M0 launches to one approved cohort to validate the contract and operating model.
* **Autonomous agent actions:** Agent recommendations may be enabled, but direct agent execution is prohibited by the product architecture.
* **Broad prompt/model experimentation:** M0 may configure a runtime adapter but does not optimize multiple model families beyond meeting quality gates.
* **Cross-capability conversation planning:** The Broker selects one primary capability per turn; composition is future optional behavior.
* **Re-platforming Benefits Service:** Only contract gaps necessary for governed reads, evidence, or SLOs are in scope.

## Dependencies and Decisions

### Dependencies

- CCS / external identity contract supplies verifiable tenant, actor, persona, scopes, and expiration.
- Broker resolver and tenant-context paths remain available for productization.
- Benefits Service can serve the approved tenant with plan data and auditable source metadata.
- Member and CSR surfaces can adopt the versioned request/response contract and accessibility requirements.
- Telemetry storage supports privacy-approved turn and evaluation events.

### Decisions Required by End of Week 2

1. Standard response schema v1 and backward-compatibility policy.
2. Conversation retention, redaction, and subject-change behavior.
3. Approved source freshness thresholds and stale-data presentation.
4. Initial SLOs for Broker, agent runtime, and Benefits Service dependency.
5. Evaluation adjudication owners and severity definition for unsupported claims.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Identity contract changes during M0 | Rework or unsafe interim behavior | Isolate identity behind versioned context adapter; fail closed; decide production issuer/audience before cohort. |
| Existing CSR response shape conflicts with standard envelope | Surface regression or duplicated logic | Add adapter and compatibility profile; test factual equivalence and existing supported flows. |
| Plan context remains caller-supplied without validation | Wrong-plan answer | Require trusted/validated plan association for the cohort and capture effective date plus source evidence. |
| Conversation state stores excess PHI | Compliance and breach exposure | Minimize stored data, apply redaction/retention policy, and test deletion and tenant isolation. |
| GRR target masks unsafe abstention | Misleading product performance | Report GRR and Safe Handling separately using a fixed eligible-inquiry classification. |
| Eight-week scope expands into platform completion | Missed milestone | Treat M0 as the Benefits Inquiry reference slice; defer nonessential migration and advanced orchestration. |

## Delivery Plan

| Week | Product milestone | Exit signal |
| ---: | --- | --- |
| 1 | Baseline and contract discovery | Frozen evaluation set, current metrics, tenant/surface cohort, source and identity decisions recorded |
| 2 | Product and contract definition | Taxonomy, manifest, context envelope, response schema, profiles, and outcome definitions approved |
| 3 | Trusted context and conversation slice | Member and CSR requests establish isolated actor/subject/tenant context and persistent conversation |
| 4 | Routing and governed Brain slice | Explicit/inferred routing and Benefits Service tool policy pass integration tests |
| 5 | Agent and response slice | Runtime adapter returns schema-valid, evidence-bearing responses to both surfaces |
| 6 | Safe fallback, escalation, telemetry | Clarify/abstain/escalate/outage paths and terminal outcomes are observable |
| 7 | Evaluation and operational hardening | ≥100 scenarios run; security, load, accessibility, and rollback tests complete |
| 8 | Cohort launch and validation | Controlled release, operational sign-off, 48-hour validation, and rollback readiness |

## 🏁 Exit Criteria

### Functional Completion

* [ ] Member Chat and CSR Chat both complete the approved Benefits Inquiry journey through the same versioned capability contract.
* [ ] Explicit capability selection and inferred routing each select `benefits.query` correctly for approved scenarios.
* [ ] CSR actor and member subject remain distinct and authorized through the full request, retrieval, response, and audit flow.
* [ ] Conversation context survives supported multi-turn clarification and cannot cross tenant, actor, or subject boundaries.
* [ ] Resolved responses validate against the v1 structured envelope and approved surface profiles render factual-equivalent answers.
* [ ] Missing, stale, conflicting, unauthorized, and unavailable source conditions produce the approved non-resolution outcomes.
* [ ] Surface-requested escalation is Broker-authorized and audited; agent recommendation is disabled unless explicitly configured.

### Quality, Safety, and Performance Gates

* [ ] At least 100 representative Benefits Inquiry scenarios are approved and executed.
* [ ] GRR is at least 95% on eligible evaluation scenarios.
* [ ] Safe Handling Rate is at least 99% across the full evaluation set.
* [ ] 100% of successful answers include provenance and freshness/as-of evidence.
* [ ] 100% of evaluated turns persist exactly one terminal outcome.
* [ ] Automated tenant-isolation tests report zero cross-tenant data access.
* [ ] Launch evaluation contains zero critical unsupported factual claims.
* [ ] All configured side-effect actions are authorized, confirmed, idempotent, and audited; no agent executes a side effect directly.
* [ ] Accessibility testing passes WCAG 2.2 AA for the supported Member and CSR experiences.
* [ ] Approved capability SLOs pass load and dependency-failure tests.

### Analytics and Launch Readiness

* [ ] GRR, Safe Handling, outcome, provenance, routing, source, latency, error, and action events reconcile to turn totals with less than 1% unexplained variance.
* [ ] Security and privacy review closes with zero unresolved critical or high-severity findings.
* [ ] Product, Member Experience, CSR Experience, Benefits Service, Security, and Operations approve user acceptance testing.
* [ ] Tenant/surface/version cohort controls, dashboards, alerts, runbook, and rollback procedure are tested in the release environment.
* [ ] Baseline and first 48-hour cohort measurements are published with named owners for 30-day review.

---

## Source References

- `stellarus-apps/apps/agentic-broker-api/src/chat-handler/chat-handler.service.ts`
- `stellarus-apps/apps/agentic-broker-chat/src/hooks/use-chat-state.ts`
- `stellarus-ai/apps/csr-chat/README.md`
- `stellarus-ai/apps/csr-chat/docs/multi-customer-integration.md`
- `stellarus-apps/apps/benefits-service/docs/benefits-service.md`
- [Compass capability roadmap infographic](../../outputs/compass-capability-roadmap-executive-infographic.html)
