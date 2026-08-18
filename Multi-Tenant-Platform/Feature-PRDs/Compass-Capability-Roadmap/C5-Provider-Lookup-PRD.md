# 🧩 Project Name: C5 — Provider Lookup

**PDLC Phase:** Definition  
**Authored Date:** August 7, 2026  
**Status:** DRAFT  
**Timebox:** 6 weeks  
**CEI Priority:** `cei-strategic`  
**CEI Score:** 60/100 — C2 I3 E2  
**CEI Confidence:** Medium  
**CEI Assessment Date:** August 12, 2026  
**CEI Framework:** CEI 1.0  
**Roadmap Position:** C5 — baseline sequence after Formulary  
**Dependency Rule:** Requires versioned M0 platform contracts; does not require Eligibility, Claims, Accumulators, Formulary, or Scheduling  
**Initial Cohort:** One approved tenant across Member Chat and CSR Chat; Provider Chat when tenant-enabled  
**Accountable Product Owner:** TBD — Provider Directory Capability  
**Required Decision Owners:** Provider Directory, Network Management, Member/Provider Services, Accessibility, Platform, Operations

## CEI Prioritization

**CEI: `cei-strategic` | 60/100 | C2 I3 E2 | confidence: medium**

**Decision:** Retain Provider Lookup as a strategic roadmap capability and the portable identity/search foundation for later workflows. Do not treat its CEI tag as a requirement for Scheduling to depend on it.

| Dimension | Class | Value | Points | Confidence | Rationale and evidence |
| --- | --- | :-: | ---: | --- | --- |
| Category | Strategic | 2 | 20 | Medium | Provider Lookup is an accepted milestone and creates the stable ProviderReference contract, but no funded date, final directory source, or accountable owner is recorded. |
| Impact | High | 3 | 30 | Medium | It improves Member and CSR search, optionally Provider Chat, and enables portable provider identity with ≥95% GRR, ≥90% top-five relevance, and zero hard-filter violations. Reach is not baselined. |
| Effort | Medium | 2 | 10 | Medium | The six-week scope spans directory integration, entity normalization, geospatial/network filtering, ranking, three profiles, evaluation, and operations. Engineering validation remains pending. |

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
    rationale: "Accepted roadmap capability that establishes governed search and portable provider identity without a funded date or final source owner."
    evidence: "Roadmap Position, Product Goals, Dependency Rule, and user direction."
  impact:
    value: 3
    classification: high
    weighted_points: 30
    confidence: medium
    rationale: "Improves provider search across primary Member and CSR workflows and creates a reusable ProviderReference for approved downstream use."
    evidence: "Target Users, Supported User Journeys, Success Metrics, and Functional Requirements."
  effort:
    value: 2
    classification: medium
    weighted_points: 10
    confidence: medium
    rationale: "Six-week multi-component capability with material directory, terminology, network, geography, ranking, and operational dependencies."
    evidence: "Authored timebox and work packages C5-01 through C5-11; engineering validation pending."
  category_floor:
    applied: false
    reason: null
  assumptions:
    - "M0 contracts are available and the first release remains one approved tenant cohort."
    - "ProviderReference remains portable and Scheduling accepts approved alternatives."
  open_questions:
    - "Which funded date, directory source owner, and accountable product owner establish a C3 commitment?"
    - "What provider-search volume and zero-result baseline quantify production impact?"
    - "Does engineering validate the six-week estimate after directory and ranking design?"
  next_action: "Confirm directory ownership, reach, and engineering estimate; re-score when commitment evidence or source complexity changes."
```

## 🎯 Problem Statement

Finding an appropriate provider requires more than matching a name or specialty. Users need results constrained by network, location, distance, accepting-new-patient status where authoritative, accessibility, language, modality, provider type, and source freshness. Directory data can be stale or incomplete, and opaque ranking can surface results that violate a hard user requirement.

Compass does not yet provide a governed Provider Lookup capability with explicit filter semantics, ranking policy, source freshness, and a stable ProviderReference that other workflows can safely consume. Existing provider participation checks may answer a narrow par/non-par question but do not constitute a complete conversational search experience.

**Impact:** Members and CSRs repeat searches across tools, may contact out-of-network or unsuitable providers, and cannot easily understand why a result appeared. Scheduling workflows risk binding to display text instead of a stable provider/location identity.

**Baseline:** Cross-surface provider-search task success, ranking relevance, hard-filter compliance, and Safe Handling are not currently measured as a Compass capability. Week 1 establishes the authoritative directory source, cohort geography/network, and a labeled search evaluation set.

## 💡 Proposed Solution

Introduce `provider.lookup` as a read-only capability that normalizes search intent, applies authoritative hard filters, ranks eligible results using an approved policy, explains material match factors, and returns a stable `ProviderReference` for each provider-location-network context.

The default structured response will present a concise result set with specialty, location, distance or geography context, network status, contact details, accessibility/language/modality fields when sourced, source freshness, and limitations. The capability will distinguish authoritative filters from soft preferences and will never invent availability or guarantee that directory attributes remain current.

## 👥 Target Users

**Primary Users:**

* **Member:** Needs to find an in-network provider matching specialty, location, accessibility, language, or modality preferences.
* **CSR:** Needs to perform and explain a search on behalf of a member and provide traceable results.

**Secondary Users:**

* **Provider Chat user:** May search the directory for referral or peer-location purposes when tenant policy enables the profile.
* **Provider directory and network operations:** Need visibility into freshness, zero-result patterns, and suspected data quality gaps.
* **Scheduling capability:** May consume a stable ProviderReference, while remaining able to accept one from a host surface or other approved source.

## Product Goals and Non-Goals

### Goals

1. Return relevant providers without violating network, geography, provider-type, or other hard constraints.
2. Make ranking and source freshness understandable enough for users and operations.
3. Preserve provider, location, organization, and network identity in a portable ProviderReference.
4. Handle zero-result and stale-data cases without broadening constraints silently.

### Non-Goals

1. Book appointments or represent real-time availability.
2. Recommend the clinically best provider or guarantee quality/outcomes.
3. Correct the provider directory or credential a provider.
4. Require any prior Compass healthcare capability.
5. Guarantee accepting-new-patient status when the source does not provide a current authoritative value.

## Supported User Journeys

| Journey | Expected behavior |
| --- | --- |
| Member asks for an in-network specialist nearby | Resolve specialty and location, apply network and distance constraints, rank eligible results, and explain the core match factors. |
| CSR searches for accessibility and language needs | Treat explicitly required accessibility/language attributes as hard filters only when source semantics support them; disclose unknown fields. |
| User asks for a named provider | Resolve provider identity and location, return network status for the approved context, and clarify when several records match. |
| Search has no results | Preserve user constraints, explain which authoritative filters produced zero results, and offer configured ways to broaden them rather than doing so silently. |
| Directory data is stale, conflicting, or unavailable | Label source age and uncertainty, avoid asserting unsupported attributes, and offer an approved verification or escalation path. |

## ✅ Success Metrics

| Metric | Baseline | Release target | Measurement window and source |
| --- | --- | --- | --- |
| Provider Lookup Grounded Resolution Rate | Establish Week 1 | ≥95% of eligible lookup inquiries | Labeled search evaluation and first 30 cohort days |
| Ranked-result relevance and constraint compliance | Establish Week 1 on approved query set | ≥90% of queries have a relevant result in top five when an eligible record exists; zero hard-filter violations | Domain-adjudicated ranking set and automated constraint validator |
| Safe Handling Rate | Establish Week 1 | ≥99% across ambiguous, zero-result, stale, unknown-attribute, unauthorized, and outage cases | Full evaluation set plus weekly cohort sample |

**Guardrails:** 100% of results include source and freshness; zero invented availability, accessibility, language, network, or accepting-new-patient attributes; 100% stable ProviderReference validation.

## 📦 Scope

### Task-Ready Work Packages

| ID | Deliverable | Completion evidence | Estimate |
| --- | --- | --- | ---: |
| C5-01 | Provider search taxonomy and filter semantics | Approved intent/entity catalog; hard versus soft filter rules; zero-result behavior | 4 days |
| C5-02 | `provider.lookup` capability manifest | Versioned inputs, outputs, scopes, tools, profiles, and SLO | 3 days |
| C5-03 | Provider Directory Brain adapter | Normalized provider, organization, location, network, contact, attribute, and freshness contract | 5 days |
| C5-04 | Specialty/location/entity normalization | Labeled specialty, provider-name, address/geography, and ambiguity fixtures pass | 5 days |
| C5-05 | Constraint and network filter engine | Hard-filter validation reports zero excluded-record leakage on test set | 5 days |
| C5-06 | Approved ranking policy | Deterministic/observable ranking factors and top-five relevance evaluation implemented | 5 days |
| C5-07 | Stable ProviderReference | Versioned provider-location-network reference validates, resolves, and expires/refreshes per policy | 4 days |
| C5-08 | Member/CSR/optional Provider profiles | Accessible result cards/list, match explanations, source age, and unknown-attribute behavior | 4 days |
| C5-09 | Zero-result, stale, and verification paths | Constraint-preserving broadening prompts and Broker-controlled contact/escalation behavior | 4 days |
| C5-10 | Evaluation and telemetry | ≥100 scenarios, ranking/constraint/GRR/safety scoring, zero-result and freshness dashboards | 5 days |
| C5-11 | Cohort operations | SLO, alerts, runbook, rollback, source-owner escalation, and sign-off | 3 days |

### Functional Requirements

1. **C5-FR-01:** The capability must accept trusted tenant context plus specialty/provider name, geography, network/product context, provider type, language, accessibility, modality, distance, and preference fields as supported.
2. **C5-FR-02:** Query normalization must preserve the user's original terms, resolved entities, ambiguity, and which conditions are required versus preferred.
3. **C5-FR-03:** Hard filters must execute against normalized source fields before ranking; the agent may not reintroduce excluded records.
4. **C5-FR-04:** Network status must be tied to the applicable tenant/product/network and source effective/as-of context; generic provider participation may not substitute when insufficient.
5. **C5-FR-05:** Ranking must use an approved, versioned factor set and expose material match reasons; it must not use protected characteristics or unsupported quality inference.
6. **C5-FR-06:** Missing attribute values must display as unknown, not false or assumed.
7. **C5-FR-07:** Zero-result behavior must not silently relax network, distance, accessibility, language, provider type, or other hard constraints.
8. **C5-FR-08:** Every result must include a stable ProviderReference representing at least provider, location, organization where applicable, network context, source, and reference version.
9. **C5-FR-09:** The ProviderReference must be consumable by Scheduling, host surfaces, and approved services without making Provider Lookup a runtime dependency.
10. **C5-FR-10:** The capability must not state appointment availability, clinical fit, provider quality, or accepting-new-patient status unless the authoritative source supplies the exact attribute with acceptable freshness.
11. **C5-FR-11:** Structured results are default; alternative render profiles must preserve constraints, network, location, source age, unknowns, and ProviderReference.
12. **C5-FR-12:** Every completed turn must emit one terminal outcome and all returned results must be traceable to source records.

### Analytics Requirements

Capture capability/version, surface/persona, normalized query entities, hard/soft filter classes, result count, zero-result cause, rank positions, relevance labels when available, hard-filter compliance, ProviderReference version, source snapshot age, unknown-attribute classes, outcome, source latency/error, and evaluation linkage. Avoid recording precise member location beyond the approved geographic granularity.

## 🚫 Out-of-Scope

* **Scheduling or availability:** Delivered by C6 through separate read/action contracts.
* **Clinical recommendations or quality ranking:** Search relevance is not clinical suitability or care quality.
* **Directory remediation:** The release reports suspected gaps but does not replace source correction workflows.
* **Credentialing or sanctions decisions:** Directory display data is not an authorization to credential.
* **Route planning and transportation:** Distance/geography is limited to approved search features.
* **Mandatory Eligibility or Formulary context:** Network/product context may be supplied directly from an approved source.

## Dependencies and Decisions

- **Required:** authoritative Provider Directory source and owner; network/product mapping; specialty terminology; geocoding/location policy; accessibility/language field definitions; M0 contracts.
- **Current candidate limitation:** existing provider par/non-par functionality can inform participation checks but does not by itself establish complete directory search, ranking, or freshness behavior.
- **Decisions by Week 1:** cohort geography and networks, hard/soft filters, ranking factors, acceptable source age, ProviderReference lifetime/version, and which attributes can be displayed as authoritative.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Stale directory attribute presented as current | Failed contact or access barrier | Required source age, attribute-level freshness where available, verification language, operations feedback. |
| Ranking violates hard requirement | Unsafe or unusable result | Pre-ranking filter enforcement and zero-tolerance automated constraint tests. |
| Model invents accessibility or availability | Member harm | Structured source-only attributes and adversarial evaluation. |
| Network participation lacks product context | Out-of-network result | Require sufficient network/product context or disclose inability to verify. |
| ProviderReference becomes Scheduling dependency on Lookup | Roadmap coupling | Reference contract is portable; Scheduling accepts it from multiple approved sources. |

## Delivery Plan

| Week | Milestone | Exit signal |
| ---: | --- | --- |
| 1 | Source, baseline, and search policy | Directory owner, cohort, fields/freshness, query set, hard/soft and ranking decisions |
| 2 | Manifest, adapter, and entity normalization | Provider/source schema plus specialty/location fixtures pass |
| 3 | Filtering, ranking, and ProviderReference | Zero hard-filter violations, initial relevance target, stable reference contract |
| 4 | Surface profiles and safe fallback | Member/CSR/Provider render, zero-result/stale/unknown behavior pass integration tests |
| 5 | Evaluation and operational hardening | ≥100 scenarios, relevance/security/privacy/accessibility/load tests, dashboards/runbook |
| 6 | Cohort release | UAT, SLO/rollback approval, 48-hour validation, 30-day review owners |

## 🏁 Exit Criteria

### Functional Completion

* [ ] Member and CSR journeys—and Provider profile when enabled—complete through `provider.lookup`.
* [ ] Specialty, provider, geography, network, and supported attribute entities resolve correctly or trigger approved clarification.
* [ ] No returned result violates an explicit hard constraint in automated or UAT scenarios.
* [ ] Ranking uses the approved versioned policy and material match factors are observable.
* [ ] Zero-result behavior preserves hard constraints and offers only explicit, user-approved broadening.
* [ ] Every result includes source/freshness and a valid stable ProviderReference.
* [ ] The capability makes no unsupported availability, clinical-fit, quality, or attribute claims.
* [ ] C5 completes supported journeys without Eligibility, Claims, Accumulators, Formulary, or Scheduling.

### Quality and Launch Gates

* [ ] At least 100 representative scenarios are approved and executed.
* [ ] GRR is ≥95%, top-five relevance is ≥90% when an eligible record exists, hard-filter violations are zero, and Safe Handling Rate is ≥99%.
* [ ] 100% of returned results include provenance and freshness/as-of evidence.
* [ ] 100% of evaluated turns emit exactly one terminal outcome.
* [ ] Tenant/network authorization and location-privacy tests report zero unauthorized access or data retention.
* [ ] Launch evaluation reports zero critical unsupported factual claims.
* [ ] Supported profiles pass WCAG 2.2 AA.
* [ ] Capability/source SLO, runbook, dashboards, source feedback path, cohort controls, and rollback are approved and tested.
* [ ] Product, Provider Directory, Network, Accessibility, Security, Member, CSR, and Operations owners sign off UAT.

---

## Source References

- `stellarus-apps/apps/um-composite-api/docs/tech-spec.md`
- [M0 Platform Reference Foundation](M0-Platform-Reference-Foundation-PRD.md)
- [Compass Capability Roadmap PRD Index](README.md)
