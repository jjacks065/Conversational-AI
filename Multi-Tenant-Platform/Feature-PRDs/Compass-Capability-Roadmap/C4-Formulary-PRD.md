# 🧩 Project Name: C4 — Formulary

**PDLC Phase:** Definition  
**Authored Date:** August 7, 2026  
**Status:** DRAFT  
**Timebox:** 6 weeks  
**CEI Priority:** `cei-strategic`  
**CEI Score:** 60/100 — C2 I3 E2  
**CEI Confidence:** Medium  
**CEI Assessment Date:** August 12, 2026  
**CEI Framework:** CEI 1.0  
**Roadmap Position:** C4 — baseline sequence after Accumulators  
**Dependency Rule:** Requires versioned M0 platform contracts; does not require Eligibility, Claims, Accumulators, or another healthcare capability  
**Initial Cohort:** One approved tenant across Member Chat, CSR Chat, and Provider Chat  
**Accountable Product Owner:** TBD — Formulary Capability  
**Required Decision Owners:** Pharmacy/Formulary Domain, Clinical Safety, Member/Provider Services, Platform, Security, Operations

## CEI Prioritization

**CEI: `cei-strategic` | 60/100 | C2 I3 E2 | confidence: medium**

**Decision:** Retain Formulary as a strategic whole capability. Its cross-surface pharmacy value and clinical-safety boundary justify roadmap review, while commitment evidence and source ownership remain prerequisites to C3 classification.

| Dimension | Class | Value | Points | Confidence | Rationale and evidence |
| --- | --- | :-: | ---: | --- | --- |
| Category | Strategic | 2 | 20 | Medium | Formulary is an accepted Compass milestone with clear platform and safety value, but no funded delivery date, authoritative source, or accountable owner is recorded. |
| Impact | High | 3 | 30 | Medium | It serves Member, CSR, and Provider surfaces and targets ≥95% GRR, ≥98% drug resolution, exact policy facts, and ≥99% Safe Handling. Production reach is not baselined. |
| Effort | Medium | 2 | 10 | Medium | The six-week scope includes drug normalization, policy mapping, clinical review, three profiles, handoff, evaluation, and operations. Engineering validation remains pending. |

**Category floor:** None for C2.

```yaml
category_effort_impact:
  status: final
  tag: cei-strategic
  score: 60
  score_range: null
  category:
    value: 2
    classification: strategic
    weighted_points: 20
    confidence: medium
    rationale: "Accepted roadmap capability for governed formulary explanations without a funded date or final source owner."
    evidence: "Roadmap Position, Product Goals, Dependencies and Decisions, and user direction."
  impact:
    value: 3
    classification: high
    weighted_points: 30
    confidence: medium
    rationale: "Improves drug coverage and administrative-restriction workflows across Member, CSR, and Provider surfaces while enforcing a clinical boundary."
    evidence: "Target Users, Supported User Journeys, Success Metrics, and Quality Gates."
  effort:
    value: 2
    classification: medium
    weighted_points: 10
    confidence: medium
    rationale: "Six-week multi-component capability with terminology, policy-version, source, clinical-safety, and operational dependencies."
    evidence: "Authored timebox and work packages C4-01 through C4-10; engineering validation pending."
  category_floor:
    applied: false
    reason: null
  assumptions:
    - "M0 contracts are available and authorized policy context can be supplied without Eligibility."
    - "The first release targets one approved tenant cohort."
  open_questions:
    - "Which source owner, funded date, and accountable product owner establish a C3 commitment?"
    - "What formulary inquiry volume and affected population quantify production impact?"
    - "Does engineering validate the six-week estimate after terminology and clinical review?"
  next_action: "Name the Formulary source and owner, validate the estimate, and re-score when commitment or reach evidence changes."
```

## 🎯 Problem Statement

Drug coverage questions require precise identification of both the drug and the applicable policy. A brand name may map to multiple strengths, dosage forms, routes, and identifiers; formulary status can vary by plan, effective date, tier, and policy version. Restrictions such as prior authorization, step therapy, and quantity limits are administrative coverage rules, but conversational wording can easily be mistaken for clinical advice.

Compass does not yet expose a governed Formulary capability with drug normalization, policy versioning, and an explicit clinical boundary. If the wrong drug concept or policy version is selected, the response can be confidently incorrect even when the underlying source is accurate.

**Impact:** Members and providers may misunderstand coverage or delay appropriate administrative next steps; CSRs spend time reconciling drug names and policy rules; and clinically suggestive language creates safety and liability risk.

**Baseline:** Formulary GRR, drug-entity resolution accuracy, and Safe Handling are not currently measured across Compass surfaces. Week 1 establishes an authoritative formulary/policy source, a drug normalization authority, and a frozen evaluation set.

## 💡 Proposed Solution

Introduce `formulary.query` as a read-only Compass capability. It will normalize the user's drug reference to an approved concept, resolve the applicable plan/product and policy effective date from trusted or directly supplied authorized context, and return source-supported coverage status, tier, prior authorization, step therapy, quantity limits, and other approved administrative restrictions.

The Formulary agent will ask clarifying questions when strength, form, route, or policy context changes the answer. It will explain administrative rules in surface-appropriate language, preserve policy version and as-of evidence, and explicitly avoid diagnosis, dosing, substitution, or treatment recommendations.

## 👥 Target Users

**Primary Users:**

* **Member:** Needs to understand whether a specific medication is listed and what administrative restrictions apply.
* **CSR:** Needs to resolve ambiguous drug references and explain tier/restriction facts and approved next steps.
* **Provider user:** Needs authorized formulary status and requirements for a precisely identified drug and patient plan context.

**Secondary Users:**

* **Pharmacy/formulary operations:** Need traceable policy version and source evidence.
* **Clinical safety and compliance:** Need enforcement of administrative-versus-clinical boundaries.
* **Prior authorization teams:** Need accurate handoff context when a source-supported requirement applies.

## Product Goals and Non-Goals

### Goals

1. Resolve common formulary status, tier, and restriction questions against the correct drug concept and policy version.
2. Clarify ambiguity whenever strength, form, route, or plan context can change the result.
3. Provide approved administrative next steps without clinical advice.
4. Make policy version, effective date, provenance, and freshness visible and measurable.

### Non-Goals

1. Recommend treatment, dose, substitution, or a clinically preferable drug.
2. Submit prior authorization or exception requests.
3. Predict member cost or pharmacy availability.
4. Require Eligibility or Benefits to complete a supported request when authorized plan/product context is provided.

## Supported User Journeys

| Journey | Expected behavior |
| --- | --- |
| Member asks whether a named drug is covered | Normalize or clarify drug identity, resolve policy context, and return coverage/tier/restrictions with policy version and date. |
| CSR asks what “step therapy” means for the selected drug | Explain the source-supported administrative requirement and approved contact/authorization next step without treatment guidance. |
| Provider asks about prior authorization or quantity limit | Enforce provider access, return exact policy facts for the drug strength/form/route and plan, and offer configured handoff. |
| Brand/generic or dosage form is ambiguous | Ask a minimum clinical-identity clarification; do not choose based on popularity or language-model probability. |
| Drug/policy is not found, expired, conflicting, or source is unavailable | Distinguish no match from unavailable data and safely abstain, clarify, or escalate. |

## ✅ Success Metrics

| Metric | Baseline | Release target | Measurement window and source |
| --- | --- | --- | --- |
| Formulary Grounded Resolution Rate | Establish Week 1 | ≥95% of eligible scenarios | Domain-adjudicated evaluation and first 30 cohort days |
| Drug concept resolution accuracy | Establish Week 1 on ambiguous and exact drug references | ≥98% correct concept selection or correct clarification; zero critical wrong-drug selections | Labeled drug entity set compared with resolver traces |
| Safe Handling Rate | Establish Week 1 | ≥99% across clinical-boundary, ambiguous-drug, missing-policy, stale, unauthorized, and outage cases | Full evaluation set plus adjudicated cohort sample |

**Guardrails:** 100% exact match for displayed tier/restriction/policy fields on resolved scenarios; zero clinical recommendations; zero unsupported coverage or cost promises.

## 📦 Scope

### Task-Ready Work Packages

| ID | Deliverable | Completion evidence | Estimate |
| --- | --- | --- | ---: |
| C4-01 | Formulary taxonomy and clinical boundary policy | Approved intents, administrative fields, prohibited advice, limitation, and escalation rules | 4 days |
| C4-02 | `formulary.query` capability manifest | Versioned request/response, scopes, tools, profiles, and SLO | 3 days |
| C4-03 | Drug normalization component | Approved concept identifiers and ambiguity/clarification behavior pass labeled fixtures | 5 days |
| C4-04 | Formulary Brain adapter | Policy-versioned coverage, tier, restrictions, effective dates, provenance, and errors normalize correctly | 5 days |
| C4-05 | Plan/policy context resolver | Directly supplied authorized context and optional platform context select the approved policy version | 4 days |
| C4-06 | Formulary agent and explanation mapping | Schema-valid administrative explanation preserves exact source facts and clinical boundary | 5 days |
| C4-07 | Member, CSR, and Provider response profiles | Factual-equivalence, minimum necessary detail, and accessible restrictions display pass tests | 4 days |
| C4-08 | PA/exception handoff proposal | Configured surface request or agent recommendation creates Broker-controlled handoff, not submission | 4 days |
| C4-09 | Evaluation and telemetry | ≥100 scenarios; concept, policy, exactness, GRR, safety, and boundary scoring operational | 5 days |
| C4-10 | Cohort operations | Source SLO, dashboards, alerts, runbook, rollback, and owner sign-off | 3 days |

### Functional Requirements

1. **C4-FR-01:** The request must include trusted tenant context, authorized plan/product or equivalent policy context, effective/service date, and a drug reference.
2. **C4-FR-02:** Drug normalization must use an approved identifier authority and preserve the original user term, resolved concept, strength, dose form, route, and confidence/clarification state.
3. **C4-FR-03:** The capability must clarify when missing strength, form, route, or product context can materially change the formulary result.
4. **C4-FR-04:** The Brain adapter must return exact coverage status, tier, prior authorization, step therapy, quantity limit, policy identifier/version, effective dates, and source metadata where available.
5. **C4-FR-05:** Policy selection must be deterministic and point-in-time; the agent may not combine rules from multiple policy versions.
6. **C4-FR-06:** The response must distinguish “not on formulary,” “not found,” “not covered under selected policy,” and “source unavailable.”
7. **C4-FR-07:** Explanations may describe administrative requirements but must not recommend a drug, dose, substitution, treatment sequence, or clinical action.
8. **C4-FR-08:** Source-listed alternatives may be displayed only as administrative formulary alternatives with a clear direction to consult an appropriate clinician; they may not be ranked clinically by the agent.
9. **C4-FR-09:** Prior authorization, exception, or contact handoff must be surface-initiated by default; agent recommendation requires configuration; Broker controls execution.
10. **C4-FR-10:** Resolved responses must include resolved drug concept, policy context, exact formulary facts, source, effective/as-of data, limitations, and one terminal outcome.
11. **C4-FR-11:** The capability must support approved policy context supplied directly and may not require Eligibility, Benefits, or another capability.
12. **C4-FR-12:** Structured response is default; variants must preserve drug identity, policy version, restrictions, dates, provenance, and clinical limitation.

### Analytics Requirements

Capture capability/version, surface/persona, drug-term class, resolved concept identifiers, clarification cause, policy/product/version, restriction classes, exactness result, clinical-boundary evaluation result, provenance/freshness, outcome, handoff proposal/execution state, source latency/error, and evaluation linkage. Do not record unnecessary diagnosis or free-text clinical context.

## 🚫 Out-of-Scope

* **Clinical decision support:** Diagnosis, dosing, treatment, contraindication, interaction, and substitution recommendations are prohibited.
* **Prior authorization or exception submission:** C4 may offer a Broker-controlled handoff, not execute the workflow.
* **Drug cost estimation:** Requires pricing, benefit, pharmacy, and accumulator context outside this capability.
* **Pharmacy inventory or dispensing status:** Separate source and product problem.
* **Automatic Eligibility dependency:** Direct authorized policy context must remain sufficient.
* **Comprehensive terminology platform:** Implement the approved cohort drug-resolution slice, not every medical entity type.

## Dependencies and Decisions

- **Required:** authoritative Formulary/policy source; drug terminology authority; plan/product-to-policy mapping; clinical safety policy; PA/exception handoff destination; M0 contracts.
- **Current-state gap:** no final governed Formulary Brain service was identified in the reviewed Compass evidence. Source nomination is a Week 1 go/no-go dependency.
- **Decisions by Week 1:** supported drug identifiers and fields, ambiguity threshold, policy effective-date rules, display of source-listed alternatives, restriction wording, and freshness SLA.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Wrong drug concept selected | Incorrect coverage answer and clinical risk | Approved normalization source, strict ambiguity threshold, zero-tolerance critical tests. |
| Wrong policy version used | Outdated or incorrect restriction | Deterministic point-in-time resolver and required policy/effective-date evidence. |
| Administrative explanation becomes clinical advice | Safety/liability exposure | Prohibited-content policy, response schema boundaries, adversarial evaluation, clinical review. |
| “Not found” is described as “not covered” | False negative | Explicit source result classes and exact outcome mapping. |
| Scope expands into PA transactions | Timebox and action risk | Limit to information plus optional Broker handoff; separate transactional PRD. |

## Delivery Plan

| Week | Milestone | Exit signal |
| ---: | --- | --- |
| 1 | Source, baseline, and safety definition | Source/terminology owners, clinical boundary, frozen evaluation set, policy decisions |
| 2 | Manifest, normalization, and Brain contract | Drug resolver and point-in-time policy fixtures pass |
| 3 | Agent and three surface profiles | Schema-valid exact facts, clarification, and clinical-boundary behavior pass integration tests |
| 4 | Handoff and failure behavior | Broker-controlled handoff plus not-found/stale/conflict/outage paths complete |
| 5 | Evaluation and operational hardening | ≥100 scenarios, exactness/security/accessibility/load/clinical tests, dashboards and runbook |
| 6 | Cohort release | UAT, SLO/rollback approval, 48-hour validation, 30-day review owners |

## 🏁 Exit Criteria

### Functional Completion

* [ ] Member, CSR, and Provider journeys complete through `formulary.query` for the approved cohort.
* [ ] Drug concept and policy version are selected correctly or the capability asks an approved clarification.
* [ ] Coverage, tier, restrictions, quantity limits, dates, and policy identifiers match the authoritative source exactly on resolved scenarios.
* [ ] Not-found, not-covered, expired/conflicting policy, unauthorized, stale, and outage cases remain distinguishable.
* [ ] All response profiles preserve clinical limitation language and contain no model-generated treatment recommendation.
* [ ] PA/exception handoff is Broker-controlled and does not submit a request.
* [ ] The capability completes supported journeys without Eligibility, Claims, Accumulators, or Benefits.

### Quality and Launch Gates

* [ ] At least 100 representative scenarios are approved and executed.
* [ ] GRR is ≥95%, drug resolution/clarification accuracy is ≥98%, and Safe Handling Rate is ≥99%.
* [ ] 100% of resolved answers include provenance and freshness/as-of evidence.
* [ ] 100% of evaluated turns emit exactly one terminal outcome.
* [ ] Tenant, subject, and provider authorization tests report zero unauthorized access.
* [ ] Launch evaluation reports zero critical unsupported factual claims or clinical recommendations.
* [ ] Member, CSR, and Provider profiles pass WCAG 2.2 AA.
* [ ] Capability/source SLO, runbook, dashboards, cohort controls, and rollback are approved and tested.
* [ ] Product, Formulary Domain, Clinical Safety, Security, Member, CSR, Provider, and Operations owners sign off UAT.

---

## Source References

- [M0 Platform Reference Foundation](M0-Platform-Reference-Foundation-PRD.md)
- [Compass Capability Roadmap PRD Index](README.md)
