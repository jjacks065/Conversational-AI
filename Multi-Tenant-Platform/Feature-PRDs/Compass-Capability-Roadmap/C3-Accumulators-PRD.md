# 🧩 Project Name: C3 — Accumulators

**PDLC Phase:** Definition  
**Authored Date:** August 7, 2026  
**Status:** DRAFT  
**Timebox:** 5 weeks  
**CEI Priority:** `cei-opportunistic`  
**CEI Score:** 50/100 — C2 I2 E2  
**CEI Confidence:** Medium  
**CEI Assessment Date:** August 12, 2026  
**CEI Framework:** CEI 1.0  
**Roadmap Position:** C3 — baseline sequence after Claims  
**Dependency Rule:** Requires versioned M0 platform contracts; does not require Eligibility, Claims, or another healthcare capability  
**Initial Cohort:** One approved tenant across Member Chat and CSR Chat  
**Accountable Product Owner:** TBD — Accumulators Capability  
**Required Decision Owners:** Benefits/Accumulator Domain, Finance Operations, Member/CSR Experiences, Platform, Security, Operations

## CEI Prioritization

**CEI: `cei-opportunistic` | 50/100 | C2 I2 E2 | confidence: medium**

**Decision:** Preserve Accumulators as the third whole capability in the authored sequence, while treating it as opportunistic under current evidence. A funded commitment or quantified high-frequency reach would move it into the strategic tier.

| Dimension | Class | Value | Points | Confidence | Rationale and evidence |
| --- | --- | :-: | ---: | --- | --- |
| Category | Strategic | 2 | 20 | Medium | Accumulators is part of the accepted platform roadmap and materially extends financial self-service; no funded date, final source, or accountable owner is recorded. |
| Impact | Moderate | 2 | 20 | Medium | It provides exact deductible and out-of-pocket answers for Member and CSR users, but the first release is bounded to two surfaces and one cohort with no reach baseline. |
| Effort | Medium | 2 | 10 | Medium | The five-week scope includes a source adapter, financial reconciliation, response profiles, safety paths, evaluation, and operations. Engineering validation remains pending. |

**Category floor:** None for C2.

```yaml
category_effort_impact:
  status: final
  tag: cei-opportunistic
  score: 50
  score_range: null
  category:
    value: 2
    classification: strategic
    weighted_points: 20
    confidence: medium
    rationale: "Accepted roadmap capability that improves financial self-service but lacks a funded date and named source owner."
    evidence: "Roadmap Position, Product Goals, Dependencies and Decisions, and user direction."
  impact:
    value: 2
    classification: moderate
    weighted_points: 20
    confidence: medium
    rationale: "Creates useful exact-balance resolution for Member and CSR surfaces, with bounded initial reach and no production volume baseline."
    evidence: "Initial Cohort, Target Users, Supported User Journeys, and Success Metrics."
  effort:
    value: 2
    classification: medium
    weighted_points: 10
    confidence: medium
    rationale: "Five-week multi-component delivery with a material Accumulator source dependency and deterministic reconciliation work."
    evidence: "Authored timebox and work packages C3-01 through C3-09; engineering validation pending."
  category_floor:
    applied: false
    reason: null
  assumptions:
    - "M0 contracts are available and C3 remains independent from Claims and Eligibility."
    - "The first release remains limited to Member and CSR in one tenant cohort."
  open_questions:
    - "Which funded date and accountable owner establish a C3 commitment?"
    - "What deductible and out-of-pocket inquiry volume supports an I3 High classification?"
    - "Does engineering validate the five-week estimate after the authoritative source is selected?"
  next_action: "Validate source ownership and reach; re-score first when commitment or inquiry-volume evidence becomes available."
```

## 🎯 Problem Statement

Members and CSRs need to understand deductible and out-of-pocket progress, but accumulator data is multidimensional and time-sensitive. A single member may have individual and family balances, in-network and out-of-network buckets, multiple benefit periods, separate medical and pharmacy accumulators, pending activity, and source adjustments. A conversational answer that omits one dimension can be numerically correct yet materially misleading.

Compass does not yet provide a governed Accumulators capability with authoritative amount semantics, effective periods, as-of evidence, and deterministic reconciliation. Neither Claims nor Eligibility should be used as a substitute for the accumulator system of record.

**Impact:** Members may make care decisions using the wrong remaining amount; CSRs spend time locating and explaining bucket dimensions; and model-derived arithmetic or stale balances can create financial misinformation.

**Baseline:** Cross-surface Accumulator GRR, monetary exactness, and Safe Handling are not available. Week 1 establishes the authoritative source, field semantics, and a frozen test set containing individual/family, network, period, stale, and adjusted-balance cases.

## 💡 Proposed Solution

Introduce `accumulators.query` as a read-only capability for deductible and out-of-pocket balances. The governed Brain adapter will return authoritative accumulator buckets with currency, maximum, applied, remaining when source-provided, subject level, network, benefit category, effective period, as-of time, and status/adjustment qualifiers.

The agent will help the user choose the intended bucket and explain the result. It may not infer balances from claims, predict year-end spend, or merge buckets that the source keeps separate. The default structured response will visually preserve bucket dimensions and as-of information; Member and CSR profiles may vary explanatory detail without changing values.

## 👥 Target Users

**Primary Users:**

* **Member:** Needs to know how much has been applied and remains for a specific deductible or out-of-pocket bucket.
* **CSR:** Needs to identify the correct bucket, explain dimensions and dates, and recognize when an adjustment or source issue requires escalation.

**Secondary Users:**

* **Benefits and finance operations:** Need auditable source reconciliation and safe handling of adjustments.
* **Surface and capability teams:** Need a versioned financial response contract that remains independent of Claims.
* **AI Quality and compliance:** Need exact-value checks and evidence that the model does not invent financial facts.

## Product Goals and Non-Goals

### Goals

1. Resolve common deductible and out-of-pocket balance inquiries with exact source values.
2. Preserve individual/family, network, category, period, and as-of dimensions.
3. Clarify ambiguous buckets instead of collapsing them into a single “deductible” answer.
4. Establish deterministic reconciliation and stale/adjusted-data handling.

### Non-Goals

1. Recalculate accumulators from claim lines or estimate pending claims.
2. Forecast future spend, coverage, or cost.
3. Explain detailed claims or determine why a specific claim did or did not apply.
4. Change, reset, or transfer accumulator balances.
5. Require Claims or Eligibility to complete the supported journey.

## Supported User Journeys

| Journey | Expected behavior |
| --- | --- |
| Member asks “How much is left on my deductible?” | Resolve or clarify benefit period, network, individual/family, and category; return applied/remaining/maximum with as-of evidence. |
| CSR asks for individual and family OOP status | Return separate source buckets and explain their relationship only where the source/domain rules explicitly support it. |
| User asks about a prior benefit year | Retrieve the supported historical period or clearly state that the requested period is unavailable. |
| Several deductible buckets match | Ask a minimal clarification or present a compact structured comparison rather than merging amounts. |
| Source reports a recent adjustment, pending state, stale snapshot, or outage | Preserve the qualifier and timestamp, avoid certainty beyond the source, and offer an approved escalation path. |

## ✅ Success Metrics

| Metric | Baseline | Release target | Measurement window and source |
| --- | --- | --- | --- |
| Accumulators Grounded Resolution Rate | Establish Week 1 | ≥95% of eligible scenarios | Source-adjudicated evaluation and first 30 cohort days |
| Financial and dimension exactness | Current Compass baseline unavailable | 100% exact match for displayed currency values, benefit period, subject level, network, and accumulator type on resolved scenarios | Automated schema/source fixture comparison plus production sample reconciliation |
| Safe Handling Rate | Establish Week 1 | ≥99% across ambiguous-bucket, stale, adjusted, unsupported-period, unauthorized, and outage scenarios | Full evaluation set plus weekly adjudicated sample |

**Guardrails:** zero model-derived unapproved balances; zero cross-tenant or cross-subject access; 100% provenance/as-of and terminal outcomes.

## 📦 Scope

### Task-Ready Work Packages

| ID | Deliverable | Completion evidence | Estimate |
| --- | --- | --- | ---: |
| C3-01 | Accumulator field dictionary and bucket taxonomy | Domain-approved semantics for type, subject level, network, category, period, maximum/applied/remaining, and qualifiers | 4 days |
| C3-02 | `accumulators.query` capability manifest | Versioned inputs, outputs, scopes, source policy, profiles, and SLO | 3 days |
| C3-03 | Accumulators Brain adapter | Normalized, authoritative buckets with provenance, as-of, and source error mapping | 5 days |
| C3-04 | Deterministic reconciliation validator | Automated invariants and source comparisons identify mismatches without generative correction | 4 days |
| C3-05 | Bucket selection and clarification | Approved matching and compact comparison behavior for ambiguous inquiries | 4 days |
| C3-06 | Member and CSR response profiles | Accessible bucket presentation, plain-language labels, and factual-equivalence tests | 4 days |
| C3-07 | Safe fallback and escalation | Stale, adjusted, unsupported, unauthorized, and outage states map to typed outcomes | 3 days |
| C3-08 | Evaluation and telemetry | ≥100 scenarios, exactness/GRR/Safe Handling scoring, source reconciliation, dashboards | 5 days |
| C3-09 | Cohort operations | Capability enablement, SLO, alerting, runbook, rollback, and owner sign-off | 3 days |

### Functional Requirements

1. **C3-FR-01:** The request must use trusted tenant and subject context and may include accumulator type, service category, network, subject level, benefit period, and as-of date.
2. **C3-FR-02:** The Brain adapter must return each accumulator bucket separately with a stable bucket reference and authoritative source metadata.
3. **C3-FR-03:** Currency values must include amount and currency; dates must identify the applicable benefit period and source snapshot/as-of time.
4. **C3-FR-04:** Individual and family, in-network and out-of-network, medical and pharmacy, and current and prior-period buckets must not be merged unless the authoritative contract explicitly defines a combined bucket.
5. **C3-FR-05:** Maximum, applied, and remaining values must be source-provided or calculated by an approved deterministic rule outside the model and labeled as derived.
6. **C3-FR-06:** If approved reconciliation invariants fail, the capability must not repair values; it must surface a limitation and follow configured escalation behavior.
7. **C3-FR-07:** Ambiguous requests must ask a targeted clarification or show a safe structured comparison when that is more efficient and policy-approved.
8. **C3-FR-08:** Responses must explain that recent claim activity may not yet be reflected when the source indicates latency or pending updates.
9. **C3-FR-09:** The agent may not attribute accumulator changes to a claim unless the approved Accumulator source explicitly supplies that relationship.
10. **C3-FR-10:** Resolved responses must include bucket dimensions, exact values, period, as-of, provenance, limitations, and one terminal outcome.
11. **C3-FR-11:** The capability must support authorized accumulator context supplied directly and may not require a Claims or Eligibility call.
12. **C3-FR-12:** Structured response is default; less-structured profiles must retain every decision-relevant dimension and timestamp.

### Analytics Requirements

Capture capability/version, surface/persona, requested and resolved bucket dimensions, bucket-count class, clarification reason, exactness/reconciliation result, source snapshot age, qualifier class, outcome, source latency/error, escalation, and evaluation linkage. Store pseudonymous subject and bucket references only.

## 🚫 Out-of-Scope

* **Claim-level attribution or explanation:** Requires Claims source data and is not necessary for a balance answer.
* **Cost prediction or forecasting:** Future values are not authoritative accumulator facts.
* **Accumulator corrections or transfers:** Transactional operations require separate authorization and operational workflows.
* **Provider Chat launch:** Initial scope is Member and CSR; provider requirements may be added as a whole future profile.
* **Cross-capability reconciliation:** C3 reconciles its source contract, not Claims, Eligibility, or Benefits outputs.
* **Unsupported benefit periods or products:** Scope is limited to the source and tenant ranges approved in Week 1.

## Dependencies and Decisions

- **Required:** authoritative Accumulator source and owner; normalized bucket semantics; supported historical window; update/freshness SLA; M0 contracts.
- **Current-state gap:** no final governed Accumulator Brain service was established in the reviewed Compass evidence. It is a Week 1 go/no-go dependency.
- **Decisions by Week 1:** supported types/categories, remaining-balance calculation authority, pending/adjustment qualifiers, acceptable snapshot age, and which buckets can be compared in one answer.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Dimensions are omitted from conversational answer | Misleading financial guidance | Structured bucket schema, required dimension validator, and response-profile tests. |
| Source values do not reconcile | Incorrect balance | Deterministic invariants, safe limitation, operational escalation; never model correction. |
| Stale snapshot presented as current | User makes decision on outdated value | Visible as-of data, freshness threshold, and stale-state outcome rules. |
| Model attributes balance to a claim | Unsupported explanation | Prohibit inferred attribution and include adversarial evaluation cases. |
| Scope expands into full financial history | Missed five-week release | Limit to approved current/prior period buckets and common inquiry taxonomy. |

## Delivery Plan

| Week | Milestone | Exit signal |
| ---: | --- | --- |
| 1 | Source, baseline, and semantic definition | Source owner, field dictionary, supported periods, frozen evaluation set |
| 2 | Manifest, adapter, and reconciliation | Normalized contract and deterministic invariant suite pass fixtures |
| 3 | Selection, responses, and fallback | Member/CSR profiles and ambiguity/stale/adjusted paths pass integration tests |
| 4 | Quality and operational hardening | ≥100 scenarios, exactness/security/accessibility/load tests, dashboards and runbook |
| 5 | Cohort release | UAT, SLO/rollback approval, 48-hour validation, 30-day review owners |

## 🏁 Exit Criteria

### Functional Completion

* [ ] Member and CSR journeys resolve the approved accumulator types through `accumulators.query`.
* [ ] Every resolved bucket preserves exact values, currency, subject level, network, category, period, qualifier, and as-of evidence.
* [ ] Ambiguous bucket requests clarify or display an approved structured comparison without merging source-distinct values.
* [ ] Reconciliation failures, stale snapshots, adjustments, unsupported periods, unauthorized access, and outages follow approved safe outcomes.
* [ ] The agent performs no unapproved financial calculation or claim attribution.
* [ ] C3 completes supported journeys without Claims or Eligibility.

### Quality and Launch Gates

* [ ] At least 100 representative scenarios are approved and executed.
* [ ] GRR is ≥95%, financial/dimension exactness is 100% on resolved scenarios, and Safe Handling Rate is ≥99%.
* [ ] 100% of resolved answers include provenance and freshness/as-of evidence.
* [ ] 100% of evaluated turns emit exactly one terminal outcome.
* [ ] Tenant and subject isolation tests report zero unauthorized access.
* [ ] Launch evaluation reports zero critical unsupported financial claims.
* [ ] Member and CSR profiles pass WCAG 2.2 AA.
* [ ] Capability/source SLO, runbook, dashboards, cohort controls, and rollback are approved and tested.
* [ ] Product, Accumulator Domain, Finance Operations, Security, Member, CSR, and Operations owners sign off UAT.

---

## Source References

- [M0 Platform Reference Foundation](M0-Platform-Reference-Foundation-PRD.md)
- [Compass Capability Roadmap PRD Index](README.md)
