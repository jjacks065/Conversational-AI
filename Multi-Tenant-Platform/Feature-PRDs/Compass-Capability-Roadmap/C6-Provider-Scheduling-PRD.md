# 🧩 Project Name: C6 — Provider Scheduling

**PDLC Phase:** Definition  
**Authored Date:** August 7, 2026  
**Status:** DRAFT  
**Timebox:** 8 weeks  
**CEI Priority:** `cei-strategic`  
**CEI Score:** 65/100 — C2 I4 E1  
**CEI Confidence:** Medium  
**CEI Assessment Date:** August 12, 2026  
**CEI Framework:** CEI 1.0  
**Roadmap Position:** C6 — baseline sequence after Provider Lookup  
**Dependency Rule:** Requires versioned M0 platform contracts; accepts ProviderReference from Lookup, a host surface, or another approved source and does not require C5  
**Initial Cohort:** One approved tenant, provider organization, appointment type set, and Member/CSR surface flow; Provider workflow when enabled  
**Accountable Product Owner:** TBD — Provider Scheduling Capability  
**Required Decision Owners:** Scheduling Operations, Provider Organization, Member/CSR Experiences, Platform, Identity, Security/Privacy, Reliability

## CEI Prioritization

**CEI: `cei-strategic` | 65/100 | C2 I4 E1 | confidence: medium**

**Decision:** Preserve Scheduling as the sixth delivery milestone despite its second-highest CEI score. Its transformative product impact is offset by large transactional effort and the deliberate need to harden the platform action model through earlier releases.

| Dimension | Class | Value | Points | Confidence | Rationale and evidence |
| --- | --- | :-: | ---: | --- | --- |
| Category | Strategic | 2 | 20 | Medium | Scheduling is an accepted Compass milestone and action-model objective, but no funded delivery date, source commitment, or accountable owner is recorded. |
| Impact | Transformative | 4 | 40 | Medium | It moves Compass from information to governed healthcare transactions and establishes a reusable Broker action model for availability, booking, rescheduling, and cancellation. Initial reach remains one cohort. |
| Effort | Large | 1 | 5 | Medium | The eight-week scope is multi-team and operationally complex, spanning transactional integration, confirmation, idempotency, concurrency, compensation, reconciliation, security, and operations. Engineering validation remains pending. |

**Category floor:** None for C2.

```yaml
category_effort_impact:
  status: final
  tag: cei-strategic
  score: 65
  score_range: null
  category:
    value: 2
    classification: strategic
    weighted_points: 20
    confidence: medium
    rationale: "Accepted strategic milestone for Compass transactions without a funded date, final source commitment, or named accountable owner."
    evidence: "Roadmap Position, Product Goals, Dependency Rule, and user direction."
  impact:
    value: 4
    classification: transformative
    weighted_points: 40
    confidence: medium
    rationale: "Changes Compass from an informational product into a governed transactional product and creates a reusable action-control model."
    evidence: "Proposed Solution, Product Goals, Supported User Journeys, and Transaction Integrity success metric."
  effort:
    value: 1
    classification: large
    weighted_points: 5
    confidence: medium
    rationale: "Eight-week multi-team, operationally complex release with source writes, confirmation, idempotency, concurrency, compensation, reconciliation, security, and recovery."
    evidence: "Authored timebox and work packages C6-01 through C6-13; engineering validation pending."
  category_floor:
    applied: false
    reason: null
  assumptions:
    - "M0 contracts and Broker action controls are available."
    - "The first release remains limited to one tenant, provider organization, source, and appointment-type set."
    - "ProviderReference may come from Lookup, a host surface, or another approved source."
  open_questions:
    - "Which funded date, Scheduling source owner, and accountable product owner establish a C3 commitment?"
    - "What scheduling volume and current task-completion baseline quantify production reach?"
    - "Does engineering validate the eight-week estimate and source transaction guarantees?"
  next_action: "Validate the scheduling source, transaction guarantees, and estimate; keep C6 sixth unless leadership explicitly changes the delivery sequence."
```

## 🎯 Problem Statement

Scheduling moves Compass from information delivery into real-world transactions. A user may search availability, select a slot, book, reschedule, or cancel while slot state changes concurrently in the source system. An answer that merely sounds successful is unacceptable: the action must be authorized for the correct patient, confirmed with the user, idempotent under retries, reconciled to the source, and auditable.

Compass does not yet have a complete product contract for transactional healthcare actions. Provider Lookup can supply a useful ProviderReference, but Scheduling must also accept a provider reference from a host surface or other approved source so delivery order does not become a hidden dependency.

**Impact:** Without a governed action model, retries can create duplicate appointments, stale slots can be booked unsuccessfully, reschedule can leave an appointment in an unknown state, and surfaces or agents may perform inconsistent confirmation and audit behavior.

**Baseline:** Scheduling task completion, duplicate-action rate, confirmation compliance, and Safe Handling are not currently measured through Compass. Week 1 selects one source integration and narrow appointment-type cohort, then establishes baseline completion and failure reasons.

## 💡 Proposed Solution

Introduce `provider.scheduling` as one capability with versioned operations for `availability.search`, `appointment.book`, `appointment.reschedule`, and `appointment.cancel`.

The capability agent may interpret intent, clarify preferences, request availability, explain source policies, and propose an action when configuration permits. The Broker alone validates trusted actor/subject authority, revalidates the selected slot or appointment, presents/records explicit confirmation, generates and enforces idempotency, executes the source action, reconciles the result, persists an audit record, and returns an authoritative action status.

Surface-initiated action is the default. Agent-recommended action is optional by tenant, surface, capability, and agent configuration. No conversational success message is emitted until the source transaction is confirmed or clearly identified as pending/unknown.

## 👥 Target Users

**Primary Users:**

* **Member:** Needs to find and manage an appointment through a clear, confirmable, trustworthy flow.
* **CSR:** Needs to schedule on behalf of a member with actor/subject authorization and a complete audit trail.

**Secondary Users:**

* **Provider scheduling staff:** Need source-consistent appointment state, supported provider workflows, and operational handoffs for exceptions.
* **Scheduling operations and support:** Need reconciliation, failure categorization, and recovery tools.
* **Surface teams:** Need a stable action contract and status model without implementing source-specific transaction logic.

## Product Goals and Non-Goals

### Goals

1. Complete search, booking, reschedule, and cancel flows safely for a narrow approved cohort.
2. Guarantee explicit confirmation and Broker-only execution for side effects.
3. Prevent duplicate actions under retries and concurrent requests.
4. Make pending, failed, compensated, and unknown transaction states visible and recoverable.
5. Prove the Compass action model can support future transactional capabilities.

### Non-Goals

1. Require Provider Lookup or any earlier healthcare capability.
2. Perform clinical triage, determine appointment urgency, or select a clinically appropriate provider.
3. Take payment, estimate cost, arrange transportation, or manage referrals/authorizations.
4. Support every provider organization, appointment type, or scheduling source in the first release.
5. Allow an AI agent or surface to call the source transaction directly.

## Supported User Journeys

| Journey | Expected behavior |
| --- | --- |
| Member searches availability | Validate ProviderReference or approved source input, collect required appointment preferences, return source slots with timezone, location/modality, appointment type, and expiry/freshness. |
| Member books a selected slot | Revalidate slot and patient context, show exact confirmation summary, obtain affirmative confirmation, execute once through Broker, and return source-confirmed appointment reference/status. |
| CSR reschedules for a member | Preserve CSR actor/member subject, verify authority and existing appointment, show old/new details, confirm, execute the source-supported transaction, and reconcile partial failure. |
| User cancels an appointment | Retrieve permitted appointment and policy, show cancellation consequence, confirm, execute once, and return source-confirmed status. |
| Slot becomes unavailable or source outcome is uncertain | Do not claim success; return refreshed options, pending/unknown status, or escalation according to reconciliation rules. |

## ✅ Success Metrics

| Metric | Baseline | Release target | Measurement window and source |
| --- | --- | --- | --- |
| Scheduling task completion | Establish Week 1 for the selected cohort/source | ≥90% of eligible, user-confirmed booking/reschedule/cancel tasks reach a definitive successful source state without manual recovery | First 30 cohort days; source transaction and Compass audit reconciliation |
| Transaction integrity | Current Compass baseline unavailable | 100% of side effects authorized, explicitly confirmed, idempotent, and audited; zero duplicate or wrong-subject actions | Automated action tests and continuous source/audit reconciliation |
| Grounded and safe handling | Establish Week 1 | Availability GRR ≥95% and Safe Handling Rate ≥99% across all informational and action scenarios | ≥100-scenario evaluation, concurrency tests, and weekly cohort adjudication |

**Guardrails:** zero false-success messages; 100% definitive actions include source appointment reference and state; 100% unknown/pending outcomes enter reconciliation with an owner and deadline.

## 📦 Scope

### Task-Ready Work Packages

| ID | Deliverable | Completion evidence | Estimate |
| --- | --- | --- | ---: |
| C6-01 | Scheduling cohort and operation taxonomy | Approved provider/org, appointment types, policies, action states, and exception severity | 4 days |
| C6-02 | `provider.scheduling` capability/action manifest | Versioned operation inputs/outputs, scopes, tools, confirmations, profiles, and SLOs | 5 days |
| C6-03 | ProviderReference and patient-context validation | References from Lookup, host, and approved source resolve consistently; wrong/expired context rejected | 4 days |
| C6-04 | Availability Brain adapter | Source slots normalize with stable slot reference, timezone, location/modality, type, freshness/expiry, and provenance | 5 days |
| C6-05 | Confirmation experience | Member/CSR confirmation summary and affirmative-consent evidence pass usability/accessibility tests | 5 days |
| C6-06 | Broker action executor | Source credentials, authorization, policy, idempotency, timeout, and audit are centralized and testable | 5 days |
| C6-07 | Booking operation | Slot revalidation, create action, definitive/pending/failed status, and source reference pass integration tests | 5 days |
| C6-08 | Reschedule operation | Old/new appointment validation, supported transaction strategy, compensation, and reconciliation pass tests | 5 days |
| C6-09 | Cancellation operation | Cancellation policy, consequence disclosure, confirmation, execution, and definitive status pass tests | 4 days |
| C6-10 | Concurrency, idempotency, and recovery | Duplicate, retry, race, timeout, partial-failure, and unknown-outcome suites pass | 5 days |
| C6-11 | Surface profiles and agent recommendation policy | Surface-initiated default and configuration-gated recommendations validated for Member/CSR/Provider profiles | 4 days |
| C6-12 | Evaluation, telemetry, and reconciliation | ≥100 scenarios, action ledger, source reconciliation, GRR/Safe Handling, operations dashboard | 5 days |
| C6-13 | Cohort operations and rollback | SLO, alerting, kill switch, runbook, recovery ownership, rollback, and UAT complete | 5 days |

### Functional Requirements

1. **C6-FR-01:** Scheduling must accept a valid ProviderReference from Provider Lookup, the host surface, or another approved source; origin is recorded but does not change authorization rules.
2. **C6-FR-02:** Availability results must come from the authoritative scheduling source and include provider/location, appointment type, start time, timezone, modality, slot reference, retrieval time, and expiry/freshness.
3. **C6-FR-03:** The capability must collect only the source-required appointment and patient data and must derive tenant, actor, subject, persona, scopes, and correlation from trusted context.
4. **C6-FR-04:** Before any side effect, the Broker must revalidate actor/subject authorization, source appointment/slot state, applicable policy, and required input completeness.
5. **C6-FR-05:** The surface must present a confirmation summary containing patient-safe identity context, provider/location, appointment type, date/time/timezone, action type, and material cancellation/reschedule policy.
6. **C6-FR-06:** Execution requires an explicit affirmative confirmation bound to the exact action payload and confirmation expiry; ambiguous acknowledgments do not authorize execution.
7. **C6-FR-07:** Every action uses a Broker-generated idempotency key and stable action ID. Retries with the same intent must not create a second side effect.
8. **C6-FR-08:** The agent may propose an action only when enabled by configuration; it may never call source write tools or mark an action successful.
9. **C6-FR-09:** A success response requires authoritative source confirmation and appointment reference. Timeout or ambiguous source outcome must return pending/unknown and enter reconciliation.
10. **C6-FR-10:** Reschedule must use the source's atomic operation where available. If implemented as linked cancel/book steps, the order, compensation, and user-visible partial-failure behavior require explicit domain approval.
11. **C6-FR-11:** Cancellation must disclose material consequences and return the source-confirmed resulting state; repeated cancellation requests must be idempotent.
12. **C6-FR-12:** The action ledger must record action/version, actor/subject, source references, normalized request hash, confirmation evidence, idempotency key, attempt history, state transitions, source response reference, and reconciliation result.
13. **C6-FR-13:** Tenant/surface/capability/operation/agent-recommendation kill switches must stop new actions without preventing read-only status or recovery operations.
14. **C6-FR-14:** Every turn and every action emit typed outcomes/states; conversation state must reflect the authoritative action state after reconciliation.

### Action State Model

`proposed → confirmation_required → confirmed → executing → succeeded | failed | pending_reconciliation | cancelled`

An action may enter `compensation_required` or `compensating` when the approved reschedule strategy has multiple source steps. Terminal action state and terminal conversational outcome are related but separately recorded.

### Analytics Requirements

Capture capability/action/version, surface/persona, ProviderReference source/version, appointment type, slot age/expiry class, availability result count, action ID, authorization result, confirmation method/time, idempotency key hash, execution attempts, state transitions, source reference, reconciliation status/time, outcome, latency, error class, compensation state, and evaluation linkage. Do not store raw credentials or unnecessary patient details.

## 🚫 Out-of-Scope

* **Clinical triage or urgency determination:** Scheduling operates on a preselected appointment type and approved workflow.
* **Provider recommendation:** ProviderReference must already be selected or supplied; search is C5 or host-owned.
* **Payment, cost estimate, referral, or authorization:** Separate capabilities and workflows.
* **Waitlists, recurring appointments, group visits, and complex series:** Deferred unless explicitly included in the narrow Week 1 cohort.
* **Every scheduling vendor or organization:** One approved source and provider cohort validate the action model.
* **Agent-autonomous execution:** Prohibited regardless of model confidence.
* **Irreversible source migration:** Rollback disables Compass actions; it does not replace the source scheduling system.

## Dependencies and Decisions

- **Required:** authoritative Scheduling API and owner; source sandbox/test patients; provider/appointment cohort; identity/delegation policy; action ledger; Broker secrets and execution boundary; recovery operations; M0 contracts.
- **Current-state gap:** no final governed Scheduling Brain/action service was established in the reviewed Compass evidence. Source selection and transactional guarantees are Week 1 go/no-go decisions.
- **Decisions by Week 1:** supported operations and appointment types, reschedule atomicity, idempotency retention, confirmation expiry, slot freshness, unknown-outcome reconciliation SLA, cancellation disclosures, and kill-switch owners.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Retry creates duplicate appointment | Patient and operational harm | Broker idempotency key, source idempotency where available, action ledger, duplicate tests. |
| Slot changes between display and booking | False confirmation or failed task | Slot expiry, pre-execution revalidation, refreshed options, no false-success message. |
| Reschedule partially succeeds | Lost or duplicate appointment | Prefer atomic source operation; otherwise approved ordering, compensation, reconciliation, and clear user state. |
| Wrong actor or patient executes action | Severe privacy/safety incident | Trusted actor/subject authorization at request and immediately before execution. |
| Source timeout leaves unknown result | Duplicate retry or misleading state | Pending-reconciliation state, source lookup before retry, owner/SLA, blocked duplicate execution. |
| Agent language is mistaken for confirmation | Unauthorized action | Exact confirmation payload, affirmative control, expiry, and Broker enforcement independent of model text. |
| Eight-week scope expands to all scheduling | Missed delivery and unsafe breadth | One source, provider cohort, appointment-type set, and explicit deferred operations. |

## Delivery Plan

| Week | Milestone | Exit signal |
| ---: | --- | --- |
| 1 | Cohort, source, baseline, and transactional decisions | Source owner/sandbox, appointment scope, state model, idempotency/confirmation/recovery decisions |
| 2 | Capability/action contracts | Manifest, ProviderReference validation, action ledger, surface profiles, and SLO draft approved |
| 3 | Availability and confirmation slice | Authoritative slots plus accessible Member/CSR confirmation pass integration/usability tests |
| 4 | Booking slice | Broker-only booking, idempotency, audit, definitive/pending states pass source tests |
| 5 | Reschedule and cancel slice | Approved atomic/compensating behavior and cancellation disclosures pass integration tests |
| 6 | Concurrency and recovery hardening | Retry/race/timeout/partial-failure/unknown-state tests and reconciliation operations pass |
| 7 | Evaluation, security, and operational readiness | ≥100 scenarios, authorization/accessibility/load/DR tests, dashboards, runbook, kill switch |
| 8 | Controlled cohort launch | UAT, go-live approval, action reconciliation, 48-hour validation, and rollback readiness |

## 🏁 Exit Criteria

### Functional Completion

* [ ] Availability search returns only authoritative, unexpired source slots with provider/location, appointment type, date/time/timezone, and provenance.
* [ ] Booking, reschedule, and cancellation execute only through the Broker after actor/subject authorization, source-state revalidation, and explicit payload-bound confirmation.
* [ ] Identical retries cannot create duplicate actions, and concurrent requests produce one authoritative result.
* [ ] Successful actions include a source appointment reference and reconcile to the source state.
* [ ] Timeout and ambiguous source outcomes enter pending reconciliation and never produce a false-success message.
* [ ] Reschedule partial failures follow the approved compensation/recovery behavior.
* [ ] Agent-recommended actions are disabled by default and function only for explicitly enabled configurations; agents never execute writes.
* [ ] ProviderReference from Lookup, a host surface, and another approved source each pass contract tests.
* [ ] C6 completes supported journeys when Provider Lookup is disabled.

### Quality, Transaction, and Launch Gates

* [ ] At least 100 representative scenarios—including retry, race, timeout, partial-failure, unauthorized, and stale-slot cases—are approved and executed.
* [ ] Availability GRR is ≥95%, Scheduling task completion is ≥90%, and Safe Handling Rate is ≥99%.
* [ ] 100% of side effects are authorized, explicitly confirmed, idempotent, and audited; duplicate and wrong-subject actions are zero.
* [ ] 100% of successful actions and resolved availability answers include provenance and freshness/as-of evidence.
* [ ] 100% of evaluated turns and actions emit defined terminal outcome/state data.
* [ ] Tenant, subject, persona, delegation, and provider-organization tests report zero unauthorized access or actions.
* [ ] Launch evaluation reports zero critical unsupported factual claims or false-success messages.
* [ ] Member and CSR action experiences pass WCAG 2.2 AA and usability testing with ≥90% confirmation comprehension.
* [ ] Capability/source SLO, reconciliation SLA, action ledger dashboard, alerts, kill switches, runbook, cohort controls, and rollback are approved and tested.
* [ ] Product, Scheduling Operations, Provider Organization, Security, Reliability, Member, CSR, and Operations owners sign off UAT.

---

## Source References

- [C5 Provider Lookup](C5-Provider-Lookup-PRD.md)
- [M0 Platform Reference Foundation](M0-Platform-Reference-Foundation-PRD.md)
- [Compass Capability Roadmap PRD Index](README.md)
