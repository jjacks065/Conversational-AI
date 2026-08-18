# 🧩 Project Name: C1 — Eligibility

**PDLC Phase:** Definition
**Authored Date:** August 7, 2026
**Status:** DRAFT
**Timebox:** 6 weeks
**CEI Priority:** `cei-strategic`
**CEI Score:** 60/100 — C2 I3 E2
**CEI Confidence:** Medium
**CEI Assessment Date:** August 12, 2026
**CEI Framework:** CEI 1.0
**Roadmap Position:** C1 — first capability after M0
**Dependency Rule:** Requires versioned M0 platform contracts; does not require any other healthcare capability
**Initial Cohort:** One approved tenant across Member Chat, CSR Chat, and Provider Chat
**Accountable Product Owner:** TBD — Eligibility Capability
**Required Decision Owners:** Eligibility Domain, Identity, Platform, Member/CSR/Provider Surfaces, Security, Operations

## CEI Prioritization

**CEI: `cei-strategic` | 60/100 | C2 I3 E2 | confidence: medium**

**Decision:** Keep Eligibility as the first capability after M0. It is currently evidenced as Strategic rather than Committed; record a funded date and accountable owner before applying the C3 commitment floor.

| Dimension | Class     | Value | Points | Confidence | Rationale and evidence                                                                                                                                                                        |
| --------- | --------- | :---: | -----: | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Category  | Strategic |   2   |     20 | Medium     | Eligibility is the accepted first capability in the Compass roadmap and hardens actor/subject and provider authorization. No funded date or accountable owner is recorded.                    |
| Impact    | High      |   3   |     30 | Medium     | It serves Member, CSR, and Provider surfaces and targets ≥95% GRR, 100% deterministic eligibility-field exactness, and ≥99% Safe Handling. Production reach is not yet baselined.           |
| Effort    | Medium    |   2   |     10 | Medium     | The six-week scope includes a source adapter, authorization policy, point-in-time resolver, agent, three profiles, evaluation, and cohort operations. Engineering validation remains pending. |

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
    rationale: "Accepted first post-M0 capability that establishes point-in-time eligibility and actor-versus-subject authorization."
    evidence: "Roadmap Position, Dependency Rule, Product Goals, and user direction; no funded date or named accountable owner."
  impact:
    value: 3
    classification: high
    weighted_points: 30
    confidence: medium
    rationale: "Provides authoritative eligibility across Member, CSR, and Provider surfaces and creates optional reusable eligibility context."
    evidence: "Target Users, Supported User Journeys, and Success Metrics in this PRD."
  effort:
    value: 2
    classification: medium
    weighted_points: 10
    confidence: medium
    rationale: "Six-week multi-component release with one material source dependency and three surface profiles."
    evidence: "Authored timebox and work packages C1-01 through C1-10; engineering validation pending."
  category_floor:
    applied: false
    reason: null
  assumptions:
    - "M0 lands on September 1, 2026 and its versioned contracts are available."
    - "The initial release remains limited to one approved tenant cohort."
  open_questions:
    - "Which funded delivery date and accountable owner would promote Category to C3?"
    - "What inquiry volume and affected population establish production reach?"
    - "Does engineering validate the six-week end-to-end estimate and source integration?"
  next_action: "Confirm source ownership and engineering estimate, then record commitment evidence and re-score if Category changes."
```

## 🎯 Problem Statement

Members, CSRs, and providers need a reliable answer to a deceptively simple question: “Is this member covered for this date and under which plan?” Today, the relevant information is available through existing eligibility integrations, but it is not yet presented as a governed Compass capability. Benefits Service intentionally does not perform member lookup, eligibility resolution, or member-to-plan association, while the current UM Eligibility path retains legacy request and response behavior.

Without a capability contract, surfaces must know source-specific identifiers, callers can conflate the authenticated actor with the member subject, point-in-time coverage may be oversimplified, and downstream capabilities may receive an unverified plan or product context.

**Impact:** Users may act on an incorrect coverage period or plan association; provider and CSR workflows may expose member information without sufficient purpose-of-use; and every later capability must independently solve actor-versus-subject authorization and service-date context.

**Baseline:** Cross-surface Eligibility GRR, deterministic field exactness, and Safe Handling are not currently measured through Compass. Week 1 freezes a representative evaluation set and publishes current-path baselines before Build & Integrate approval.

## 💡 Proposed Solution

Introduce `eligibility.query` as an independently deployable Compass capability. It will resolve authorized member coverage for a requested service date and return coverage status, coverage/effective period, plan and product identifiers, line of business, and source-supported restrictions or qualifiers.

The Broker will preserve actor and subject separately, enforce persona- and purpose-specific scopes, select the configured Eligibility agent, and authorize a governed Eligibility Brain tool. The agent will explain source results in plain language without changing deterministic status or dates. The structured response is the source of truth; Member, CSR, and Provider surface profiles control presentation detail.

## 👥 Target Users

**Primary Users:**

* **Member:** Needs to know whether personal coverage is active for a date and which plan applies.
* **CSR:** Needs to verify coverage while serving a member and understand qualifiers or conflicting records.
* **Provider user:** Needs authorized point-in-time coverage confirmation for a patient and service context.

**Secondary Users:**

* **Eligibility operations and support:** Need traceable source requests and normalized outcomes.
* **Downstream capability owners:** Need an optional, versioned Eligibility context contract without making their capability dependent on C1.
* **Security and privacy reviewers:** Need proof that actor, subject, purpose, and tenant remain correctly bounded.

## Product Goals and Non-Goals

### Goals

1. Provide an authoritative, point-in-time eligibility answer across three surface profiles.
2. Harden actor-versus-subject authorization and provider access policy.
3. Produce a portable, versioned Eligibility context that other capabilities may optionally consume.
4. Clarify multiple coverage records without guessing which one the user means.

### Non-Goals

1. Explain detailed benefits, claims, accumulators, formulary, or provider network results.
2. Change enrollment, reinstate coverage, or correct source-system data.
3. Make Claims or any later capability call Eligibility as a mandatory prerequisite.
4. Determine medical necessity or guarantee payment.

## Supported User Journeys

| Journey                                            | Expected behavior                                                                                                                                  |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Member asks if coverage is active today            | Use the authenticated member as subject, retrieve current coverage, return status, plan/product, effective period, source, and as-of data.         |
| CSR asks about a past or future service date       | Preserve CSR actor/member subject, resolve coverage for the explicit date, and clearly label point-in-time context.                                |
| Provider checks a patient's coverage               | Require provider persona, permitted scope, authorized subject/purpose context, and minimum necessary disclosure.                                   |
| Multiple active or historical records match        | Present the minimum safe distinctions and request clarification rather than selecting silently.                                                    |
| Source returns no record, stale data, or an outage | Distinguish “no matching record” from “source unavailable” and emit the appropriate abstention, clarification, escalation, or failure outcome. |

## ✅ Success Metrics

| Metric                                    | Baseline                                        | Release target                                                                                                                                           | Measurement window and source                                                          |
| ----------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Eligibility Grounded Resolution Rate      | Establish in Week 1 on frozen cross-surface set | ≥95% of eligible scenarios                                                                                                                              | Pre-release evaluation and first 30 cohort days                                        |
| Deterministic Eligibility field exactness | Current Compass baseline unavailable            | 100% exact match for coverage status, effective/termination dates, plan/product identifiers, and requested service date on resolved evaluation scenarios | Automated comparison to authoritative source fixtures and sampled production responses |
| Safe Handling Rate                        | Establish in Week 1                             | ≥99% including multi-record, unauthorized, no-match, stale-source, and outage scenarios                                                                 | Full evaluation set plus adjudicated cohort sample                                     |

**Guardrails:** zero cross-tenant access; zero unauthorized provider/member disclosure; zero critical unsupported statements; 100% provenance and terminal outcomes.

## 📦 Scope

### Task-Ready Work Packages

| ID    | Deliverable                                 | Completion evidence                                                                      | Estimate |
| ----- | ------------------------------------------- | ---------------------------------------------------------------------------------------- | -------: |
| C1-01 | Eligibility taxonomy and field dictionary   | Approved intent/entity catalog and deterministic-versus-explanatory field classification |   3 days |
| C1-02 | `eligibility.query` capability manifest   | Versioned inputs, outputs, scopes, tools, profiles, and SLO declarations                 |   3 days |
| C1-03 | Eligibility Brain adapter                   | Normalized contract over the approved authoritative source with timeout/error mapping    |   5 days |
| C1-04 | Actor/subject/provider authorization policy | Automated policy matrix for Member, CSR, Provider, delegation, and purpose-of-use cases  |   5 days |
| C1-05 | Point-in-time coverage resolver             | Deterministic selection and multi-record classification using requested service date     |   5 days |
| C1-06 | Eligibility agent and response mapping      | Schema-valid answer preserves source facts and emits approved explanations/limitations   |   5 days |
| C1-07 | Member, CSR, and Provider response profiles | Surface-approved rendering and minimum-necessary disclosure tests                        |   4 days |
| C1-08 | Safe fallback and escalation behavior       | No-match, ambiguous, stale, unauthorized, and outage scenarios mapped to typed outcomes  |   4 days |
| C1-09 | Evaluation, telemetry, and reconciliation   | ≥100 scenarios, exact-field validator, GRR/Safe Handling scoring, operational dashboard |   5 days |
| C1-10 | Cohort release controls and runbook         | Capability-version enablement, SLO, alerts, rollback, and owner sign-off                 |   3 days |

### Functional Requirements

1. **C1-FR-01:** The request must identify or derive a member subject, requested service date, and trusted tenant context before retrieval.
2. **C1-FR-02:** Member self-service may only retrieve the authenticated member's permitted records unless an approved delegation relationship is present.
3. **C1-FR-03:** CSR and Provider flows must preserve actor identity, subject identity, persona, scopes, and purpose context in policy evaluation and audit.
4. **C1-FR-04:** The Brain adapter must normalize source status, effective/termination dates, plan/product, line of business, and record identifiers without generative transformation.
5. **C1-FR-05:** The capability must evaluate coverage against the explicit service date; “today” must be resolved using the tenant-approved timezone and recorded as an absolute date.
6. **C1-FR-06:** Multiple matching records must follow an approved deterministic rule or trigger clarification; the agent may not silently choose based on conversational probability.
7. **C1-FR-07:** A resolved structured response must include subject-safe display context, coverage status, period, plan/product, requested date, source, retrieval time, and as-of/freshness.
8. **C1-FR-08:** Explanatory text must not state that eligibility guarantees coverage, authorization, medical necessity, or payment.
9. **C1-FR-09:** Unauthorized and not-found responses must avoid revealing whether another tenant or subject record exists.
10. **C1-FR-10:** Every turn must emit one terminal outcome and all resolved turns must be traceable to the source record/request reference.
11. **C1-FR-11:** The capability may publish an optional Eligibility context object, but consuming capabilities must also accept equivalent authorized context from other approved sources.
12. **C1-FR-12:** Structured response is default; configured variants must preserve dates, status, source, limitations, and requested-date context.

### Analytics Requirements

Capture capability/version, surface/persona, actor type, subject type, requested service date, route method, source status class, record-count class, clarification reason, deterministic-field match result, provenance/freshness, outcome, latency, error class, and optional context-publication event. Do not persist unnecessary member data in analytics.

## 🚫 Out-of-Scope

* **Enrollment transactions or source corrections:** Require separate operational workflows and side-effect controls.
* **Detailed benefit coverage:** Remains `benefits.query`; C1 returns coverage and plan association only.
* **Claims and authorization status:** Separate capabilities with different sources and user expectations.
* **Mandatory cross-capability preflight:** Later capabilities must not become unavailable when C1 is disabled.
* **Enterprise-wide provider access policy redesign:** C1 implements the approved cohort policy and reusable hooks, not every future provider role.
* **Unrestricted historical search:** The initial release supports the approved source retention window and service-date range.

## Dependencies and Decisions

- **Required:** authoritative Eligibility source and owner; source contract and non-production fixtures; production identity/purpose-of-use policy; M0 context, response, outcome, telemetry, and enablement contracts.
- **Current candidate source:** the Enterprise Eligibility integration represented in `um-composite-api`; final ownership and whether to wrap or replace the legacy contract must be decided.
- **Decision by Week 1:** supported service-date range, record-selection rules, provider purpose codes, source freshness threshold, and displayable plan/product names.

## Risks and Mitigations

| Risk                                             | Impact                        | Mitigation                                                                                                     |
| ------------------------------------------------ | ----------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Legacy source semantics do not map cleanly       | Incorrect normalized status   | Domain-approved field dictionary, fixture reconciliation, and no generative rewriting of deterministic fields. |
| Provider access is over-broad                    | PHI disclosure                | Explicit provider scope/purpose matrix, minimum necessary profile, deny-by-default tests.                      |
| Dual or overlapping coverage is simplified       | Wrong plan association        | Preserve all matching source records, apply approved rules, otherwise clarify.                                 |
| “Eligible” is interpreted as payment guarantee | User harm and dissatisfaction | Required limitation language and evaluation cases for payment/authorization misconceptions.                    |
| C1 becomes a dependency for all capabilities     | Roadmap loses reorderability  | Publish optional context contract; require alternate approved context inputs for consumers.                    |

## Delivery Plan

| Week | Milestone                                | Exit signal                                                                                       |
| ---: | ---------------------------------------- | ------------------------------------------------------------------------------------------------- |
|    1 | Baseline, source, and policy definition  | Frozen evaluation set, source owner, field dictionary, provider policy, dates/freshness decisions |
|    2 | Manifest and Brain contract              | Capability contract, adapter schema, surface profiles, and failure taxonomy approved              |
|    3 | Authorization and point-in-time resolver | Member/CSR/Provider policies and deterministic coverage selection pass integration tests          |
|    4 | Agent, response, and clarification       | Three profiles render schema-valid, factual-equivalent results and safe ambiguity handling        |
|    5 | Quality and operational hardening        | ≥100 scenarios, isolation/security/accessibility/load tests, dashboards and alerts complete      |
|    6 | Cohort release                           | UAT approval, version enablement, 48-hour validation, and rollback readiness                      |

## 🏁 Exit Criteria

### Functional Completion

* [ ] Member, CSR, and Provider surface journeys complete through `eligibility.query` for the approved cohort.
* [ ] Actor, subject, tenant, persona, scopes, purpose, and requested service date remain correct through source retrieval and audit.
* [ ] Coverage status, dates, plan/product, and record references match the authoritative source exactly on all resolved evaluation scenarios.
* [ ] Multiple-record, no-match, unauthorized, stale, and outage cases produce approved clarification or safe non-resolution behavior.
* [ ] Resolved responses include required limitation language and do not imply payment, medical necessity, or authorization guarantees.
* [ ] Optional Eligibility context is versioned and no consuming capability is required for C1 completion.

### Quality and Launch Gates

* [ ] At least 100 representative scenarios are approved and executed.
* [ ] GRR is ≥95% and Safe Handling Rate is ≥99%.
* [ ] 100% of resolved answers include provenance and freshness/as-of evidence.
* [ ] 100% of evaluated turns emit exactly one terminal outcome.
* [ ] Tenant-isolation and provider-authorization tests report zero unauthorized access.
* [ ] Launch evaluation reports zero critical unsupported factual claims.
* [ ] Accessibility passes WCAG 2.2 AA for all three response profiles.
* [ ] Capability SLO, source dependency behavior, runbook, dashboards, cohort plan, and rollback are approved and tested.
* [ ] Product, Eligibility Domain, Security, Member, CSR, Provider, and Operations owners sign off UAT.

---

## Source References

- `stellarus-apps/apps/benefits-service/docs/benefits-service.md`
- `stellarus-apps/apps/um-composite-api/docs/tech-spec.md`
- [M0 Platform Reference Foundation](M0-Platform-Reference-Foundation-PRD.md)
