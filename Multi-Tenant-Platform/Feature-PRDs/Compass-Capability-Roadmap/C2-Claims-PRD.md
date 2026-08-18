# 🧩 Project Name: C2 — Claims

**PDLC Phase:** Definition  
**Authored Date:** August 7, 2026  
**Status:** DRAFT  
**Timebox:** 6 weeks  
**CEI Priority:** `cei-strategic`  
**CEI Score:** 60/100 — C2 I3 E2  
**CEI Confidence:** Medium  
**CEI Assessment Date:** August 12, 2026  
**CEI Framework:** CEI 1.0  
**Roadmap Position:** C2 — baseline sequence after Eligibility  
**Dependency Rule:** Requires versioned M0 platform contracts; does not require Eligibility or any other healthcare capability  
**Initial Cohort:** One approved tenant across Member Chat, CSR Chat, and Provider Chat  
**Accountable Product Owner:** TBD — Claims Capability  
**Required Decision Owners:** Claims Domain, Member Services, Provider Services, Platform, Security/Privacy, Operations

## CEI Prioritization

**CEI: `cei-strategic` | 60/100 | C2 I3 E2 | confidence: medium**

**Decision:** Retain Claims as a strategic roadmap capability following Eligibility. Promote it to Committed only when the Claims source, accountable owner, and delivery date are approved.

| Dimension | Class | Value | Points | Confidence | Rationale and evidence |
| --- | --- | :-: | ---: | --- | --- |
| Category | Strategic | 2 | 20 | Medium | Claims is an accepted Compass milestone addressing a material service capability, but the PRD still lists the authoritative Claims source and accountable owner as unresolved. |
| Impact | High | 3 | 30 | Medium | It serves Member, CSR, and Provider users and targets ≥95% GRR, ≥98% claim selection/clarification accuracy, exact monetary facts, and ≥99% Safe Handling. Reach is not baselined. |
| Effort | Medium | 2 | 10 | Medium | The six-week release spans source normalization, PHI policy, multi-record search, explanation, three profiles, handoff, evaluation, and operations. Engineering validation is pending. |

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
    rationale: "Accepted roadmap capability for governed claims explanation without a recorded funded date or final source owner."
    evidence: "Roadmap Position, Product Goals, Dependencies and Decisions, and user direction."
  impact:
    value: 3
    classification: high
    weighted_points: 30
    confidence: medium
    rationale: "Improves a consequential claims workflow across three surfaces with measurable record-selection, financial-exactness, and safe-handling targets."
    evidence: "Target Users, Supported User Journeys, Success Metrics, and Quality Gates."
  effort:
    value: 2
    classification: medium
    weighted_points: 10
    confidence: medium
    rationale: "Six-week multi-component capability with a material unresolved Claims source dependency and privacy review."
    evidence: "Authored timebox and work packages C2-01 through C2-10; engineering validation pending."
  category_floor:
    applied: false
    reason: null
  assumptions:
    - "M0 contracts are available and Claims remains independently releasable from Eligibility."
    - "The first release targets one approved tenant cohort."
  open_questions:
    - "Which authoritative Claims source, accountable owner, and delivery date establish a C3 commitment?"
    - "What claims inquiry volume and current handoff rate establish production impact?"
    - "Does engineering validate the six-week estimate after source and privacy review?"
  next_action: "Name the Claims source and owner, validate the end-to-end estimate, and re-score when commitment evidence is recorded."
```

## 🎯 Problem Statement

Claims questions are among the most consequential service interactions because a single inquiry can involve multiple claims, lines, statuses, adjustment histories, denial codes, and financial amounts. Members want to know what happened and what they owe; CSRs need enough detail to explain and route next steps; providers need authorized status and adjudication context. Current Compass capabilities do not yet expose a governed, source-identified claims explanation contract.

If a conversation selects the wrong claim or lets a model infer financial responsibility from incomplete records, the user can receive a confident but incorrect answer. Raw codes are not useful to most users, while over-explaining them can cross into promises, legal interpretation, or unsupported appeal guidance. Claims data also raises stricter PHI minimization and record-selection requirements than general plan benefits.

**Impact:** Users repeat identifying information, CSRs manually reconcile records, avoidable calls or handoffs persist, and inaccurate explanations can create financial harm, complaint risk, or privacy exposure.

**Baseline:** Claims GRR, correct-record selection, and Safe Handling are not currently measured as a Compass capability. Week 1 establishes a source-backed evaluation baseline and quantifies the current clarification/handoff rate for the selected cohort.

## 💡 Proposed Solution

Introduce `claims.query` as a read-only Compass capability that locates authorized claims, safely disambiguates records, and explains claim status, adjudication, member financial responsibility, denial/reason context, and source-supported next steps.

The Claims Brain adapter will return deterministic claim facts and approved code descriptions. The agent will organize and explain those facts but may not calculate new liability, alter a claim, submit an appeal, or promise an outcome. The standard response will identify the selected claim, show line/amount context appropriate to the surface, include source and as-of data, and distinguish a source-supported next step from general guidance.

## 👥 Target Users

**Primary Users:**

* **Member:** Needs a comprehensible explanation of claim status, amount responsibility, denial context, and next step.
* **CSR:** Needs efficient claim selection, adjudication detail, and an evidence-backed explanation to support the member.
* **Provider user:** Needs authorized status and line-level context for a claim tied to their organization or treatment relationship.

**Secondary Users:**

* **Claims operations and appeals teams:** Need accurate handoffs with source references and redacted conversation context.
* **Privacy and compliance:** Need minimum-necessary disclosure and audited actor/subject access.
* **AI Quality:** Needs deterministic comparisons for amounts, status, codes, and record selection.

## Product Goals and Non-Goals

### Goals

1. Resolve common claim-status and explanation inquiries without requiring manual record reconciliation.
2. Select or clarify the intended claim with high precision.
3. Preserve exact source amounts, dates, statuses, and codes while explaining them in user-appropriate language.
4. Provide a safe, auditable escalation or handoff when the claim requires operational action.

### Non-Goals

1. Submit, correct, adjust, reopen, or appeal a claim.
2. Guarantee payment, overturn a denial, or provide legal/clinical advice.
3. Recompute member liability from benefits, accumulators, or pricing data.
4. Require Eligibility or Accumulators to answer a supported Claims inquiry.

## Supported User Journeys

| Journey | Expected behavior |
| --- | --- |
| Member asks for status of a recent claim | Use permitted subject context and filters, identify a unique claim or clarify, then return status, key dates, provider, amounts, and source-supported next step. |
| CSR asks why a claim was denied | Retrieve the selected claim/line, translate approved reason codes, distinguish factual reason from interpretation, and provide an approved escalation/handoff if needed. |
| Provider asks about a submitted claim | Enforce provider/organization relationship and purpose, expose only the permitted claim and line details, and avoid member-only financial information when policy disallows it. |
| Several claims plausibly match | Ask a minimum-necessary clarification using safe descriptors such as service date, provider, type, or claim reference fragment. |
| Claim is pending, adjusted, reversed, missing, or source is unavailable | Represent the exact lifecycle state and as-of time; do not collapse source ambiguity into “denied” or “not covered.” |

## ✅ Success Metrics

| Metric | Baseline | Release target | Measurement window and source |
| --- | --- | --- | --- |
| Claims Grounded Resolution Rate | Establish Week 1 | ≥95% of eligible scenarios | Source-adjudicated evaluation and first 30 cohort days |
| Claim selection accuracy | Establish Week 1 on multi-record cases | ≥98% correct unique selection or correct clarification; zero silent wrong-claim selections in critical scenarios | Evaluation traces compared with scenario labels and sampled production adjudication |
| Safe Handling Rate | Establish Week 1 | ≥99% across amount, denial, privacy, pending/adjusted, missing-record, and outage cases | Full evaluation set plus weekly cohort sample |

**Guardrails:** 100% exact source match for displayed monetary values and claim identifiers on resolved scenarios; zero unauthorized record disclosure; zero unsupported promises or denial interpretations.

## 📦 Scope

### Task-Ready Work Packages

| ID | Deliverable | Completion evidence | Estimate |
| --- | --- | --- | ---: |
| C2-01 | Claims inquiry taxonomy and claim-lifecycle glossary | Domain-approved intents, states, codes, next-step boundaries, and critical-error definitions | 4 days |
| C2-02 | `claims.query` capability manifest | Versioned request/response, scopes, tool policy, profiles, and SLO declaration | 3 days |
| C2-03 | Claims Brain adapter | Approved source returns normalized claim headers, lines, amounts, statuses, codes, timestamps, and provenance | 5 days |
| C2-04 | Claims authorization and minimization policy | Member/CSR/Provider access matrix and field-level response policy pass automated tests | 5 days |
| C2-05 | Search and multi-record clarification | Safe filters, result summaries, unique-selection criteria, and ambiguity paths pass scenario tests | 5 days |
| C2-06 | Status, amount, and code explanation mapping | Deterministic facts remain exact; approved descriptions and limitations render by surface | 5 days |
| C2-07 | Claims response profiles | Member, CSR, and Provider views meet factual-equivalence and minimum-necessary rules | 4 days |
| C2-08 | Escalation and next-step handoff | Broker-created handoff includes authorized claim reference, reason, evidence, and redacted context | 4 days |
| C2-09 | Evaluation and exactness harness | ≥100 scenarios; claim selection, monetary, code, GRR, and safety validators operational | 5 days |
| C2-10 | SLO, cohort controls, and runbook | Source failure modes, dashboards, alerts, rollback, and owners approved | 3 days |

### Functional Requirements

1. **C2-FR-01:** The capability must accept a trusted subject plus zero or more safe search filters: claim reference, service date/range, provider, claim type, or status.
2. **C2-FR-02:** Search results must be tenant- and subject-scoped before any model or agent sees them.
3. **C2-FR-03:** Provider access must be restricted to the approved organizational/treatment relationship and purpose; policy determines permitted member-financial fields.
4. **C2-FR-04:** The Brain adapter must preserve claim and line identifiers, status, lifecycle timestamps, submitted/allowed/paid/member-responsibility amounts, and reason codes as deterministic fields.
5. **C2-FR-05:** The capability must select a claim only when approved uniqueness rules are met; otherwise it must clarify using minimum-necessary descriptors.
6. **C2-FR-06:** Displayed monetary values must be copied from the authoritative source with currency and field meaning; the agent may not derive totals not returned by the approved contract.
7. **C2-FR-07:** Code explanations must come from an approved, versioned code-description source and state when the source does not provide a user-facing explanation.
8. **C2-FR-08:** Pending, rejected, denied, adjusted, reversed, voided, and paid states must remain distinguishable.
9. **C2-FR-09:** Next steps must be selected from a domain-approved mapping or presented as general contact/escalation guidance; they may not imply guaranteed resolution.
10. **C2-FR-10:** Resolved responses must include selected claim context, key facts, source, as-of/freshness, limitations, and one terminal outcome.
11. **C2-FR-11:** Escalation must be surface-initiated or configuration-permitted as an agent recommendation; the Broker creates the audited handoff.
12. **C2-FR-12:** The capability must function with authorized claim context supplied directly and may not require Eligibility, Benefits, or Accumulators at runtime.

### Analytics Requirements

Capture capability/version, surface/persona, actor/subject types, filters used, candidate-count class, selection/clarification result, claim lifecycle class, code-description version, monetary exactness result, provenance/freshness, outcome, escalation reason, source latency/error, and evaluation linkage. Analytics must use pseudonymous claim/subject references and prohibit raw clinical or free-text claim details unless explicitly approved.

## 🚫 Out-of-Scope

* **Claim submission, correction, adjustment, or appeal:** Transactional workflows require separate action PRDs and operational ownership.
* **Payment or remittance initiation:** Not needed to explain existing source data.
* **Independent liability calculation:** Amounts are source facts; cross-capability computation creates safety and dependency risk.
* **Clinical or legal interpretation:** The capability explains approved administrative facts only.
* **Broad document ingestion:** EOB or attachment ingestion is deferred unless the approved source contract already exposes a governed artifact.
* **Mandatory Eligibility/Benefits/Accumulator composition:** C2 must remain independently releasable.

## Dependencies and Decisions

- **Required:** authoritative Claims source and owner; source data dictionary; code-description authority; provider authorization policy; approved claims next-step mapping; M0 contracts.
- **Current-state gap:** no final governed Claims Brain service was established in the reviewed Compass plan/code evidence. Naming and approving it is a Week 1 launch dependency.
- **Decision by Week 1:** supported claim types and lookback window; unique-selection rules; monetary fields by persona; denial/reason code mapping; pending/adjusted semantics; escalation destinations.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Wrong claim selected from similar records | Financial misinformation or PHI exposure | Strict uniqueness threshold, safe descriptors, critical scenario tests, clarify by default. |
| Model changes exact amounts or status | User harm | Deterministic fields rendered from schema; exactness validator; agent limited to explanation. |
| Code explanation overstates source meaning | Unsupported appeal/payment guidance | Versioned approved descriptions, limitations, and safe escalation. |
| Provider sees member-only information | Privacy incident | Field-level response policy and relationship/purpose enforcement before retrieval. |
| Source lifecycle states are collapsed | Incorrect status | Domain glossary and explicit normalized state mapping with unknown-state fallback. |

## Delivery Plan

| Week | Milestone | Exit signal |
| ---: | --- | --- |
| 1 | Source, baseline, and domain definition | Source owner, taxonomy, code authority, privacy matrix, frozen evaluation set |
| 2 | Manifest and Brain adapter | Normalized claims contract and source reconciliation pass |
| 3 | Search, authorization, and selection | Member/CSR/Provider access and multi-record clarification pass integration tests |
| 4 | Explanation, profiles, and handoff | Exact facts plus surface-specific explanations and Broker escalation complete |
| 5 | Evaluation and hardening | ≥100 scenarios, exactness/privacy/accessibility/load/failure tests and dashboards complete |
| 6 | Cohort release | UAT, SLO/runbook/rollback approval, 48-hour validation, 30-day review owners |

## 🏁 Exit Criteria

### Functional Completion

* [ ] Member, CSR, and Provider journeys retrieve only authorized claims and lines through `claims.query`.
* [ ] Multi-record scenarios either select the correct unique claim or ask an approved minimum-necessary clarification.
* [ ] All displayed amounts, dates, statuses, codes, and claim references match the authoritative source on resolved evaluation scenarios.
* [ ] Pending, adjusted, reversed, missing, unauthorized, and outage scenarios remain distinguishable and safely handled.
* [ ] Surface profiles meet factual-equivalence and field-minimization policy.
* [ ] Escalation/handoff is Broker-controlled, audited, and contains only approved claim context.
* [ ] The capability completes supported journeys without calling Eligibility, Benefits, or Accumulators.

### Quality and Launch Gates

* [ ] At least 100 representative scenarios are approved and executed.
* [ ] GRR is ≥95%, claim selection/clarification accuracy is ≥98%, and Safe Handling Rate is ≥99%.
* [ ] 100% of resolved answers include provenance and freshness/as-of evidence.
* [ ] 100% of evaluated turns emit exactly one terminal outcome.
* [ ] Tenant, subject, and provider authorization tests report zero unauthorized access.
* [ ] Launch evaluation reports zero critical unsupported factual claims, amount changes, or outcome promises.
* [ ] Accessibility passes WCAG 2.2 AA across supported profiles.
* [ ] Capability/source SLO, runbook, dashboards, cohort controls, and rollback are approved and tested.
* [ ] Product, Claims Domain, Privacy/Security, Member, CSR, Provider, and Operations owners sign off UAT.

---

## Source References

- [M0 Platform Reference Foundation](M0-Platform-Reference-Foundation-PRD.md)
- [Compass Capability Roadmap PRD Index](README.md)
