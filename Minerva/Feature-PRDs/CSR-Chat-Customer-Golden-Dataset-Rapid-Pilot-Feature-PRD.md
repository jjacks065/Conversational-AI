# Project Name: CSR Chat Customer Golden Dataset for Rapid Pilots

**PDLC Phase:** Definition  
**Authored Date:** October 2, 2026  
**Status:** DRAFT  
**Target Timebox:** 4 weeks  
**Decision Owner:** Product  
**Delivery Partners:** Data Science, Benefits SMEs, Implementation, Engineering, Security, Customer Success

## Problem Statement

Compass CSR Chat needs customer-specific evidence that it can answer the questions a customer expects before a rapid pilot goes live. The current baseline-generation concept emphasizes producing 500 or more question-answer pairs per plan type, but it excludes the human validation and approval workflow needed to establish whether each answer is correct, supported by the accepted customer dataset, safe for the pilot, and traceable to a specific source version.

The rapid-pilot strategy requires a non-PHI, tenant-specific experience that can launch within seven calendar days and achieve at least a 95% pass rate on a customer-approved sample. A large automatically generated set does not satisfy that requirement by itself. The team needs a repeatable way to turn the CSR Chat taxonomy library and an accepted customer data package into a bounded, approved golden dataset that defines what the pilot must answer, clarify, decline, or escalate.

**Impact:** Without a customer-specific golden dataset package, launch QA can become an open-ended review of generated questions, unsupported questions can appear answerable, defects are difficult to reproduce, and the seven-day deployment window can be consumed by late scope negotiation and manual answer reconciliation.

## Source Evaluation and Diagnosis

### Evidence

| Classification | Finding | Product implication |
| --- | --- | --- |
| FACT | The F3A baseline PRD targets 500+ generated question-answer pairs per plan type and completion within 48 hours. | F3A establishes useful generation capacity and a turnaround ambition. |
| FACT | F3A explicitly excludes human validation workflow integration and custom baseline management. | F3A cannot, by itself, produce customer-approved launch evidence. |
| FACT | The rapid-pilot strategy requires non-PHI intake, tenant association, source/version traceability, a customer-approved question sample with at least 95% pass, and launch within seven calendar days. | The golden dataset must be bounded by the accepted pilot data contract and packaged as a launch artifact. |
| FACT | `Compass-Golden-Dataset.xlsx` contains 104 CSR Chat examples across 17 taxonomies. | The workbook is a reference question library and coverage frame, not a ready-to-launch customer dataset. |
| FACT | Several workbook questions depend on member, claims, accumulator, provider, formulary, authorization, or other data that may not be present in a non-PHI pilot. | Taxonomy inclusion and answerability must be evaluated against the accepted data package rather than assumed. |
| INFERENCE | For the first rapid pilots, correctness, coverage boundaries, and reviewer throughput are more valuable than maximizing generated pair count. | Measure approved coverage and QA quality; treat dataset size as an output, not a success metric. |
| ASSUMPTION | Data Science can assemble and version a structured dataset using existing generation and analysis tools without a new production UI. | A managed artifact workflow can fit the four-week timebox. Validate in Week 1. |
| ASSUMPTION | Each pilot has a named customer or delegated benefits SME available for two bounded review sessions. | Reviewer availability becomes an intake prerequisite and launch dependency. |

### Root-Cause Diagnosis

The bottleneck is not only question generation. The bottleneck is converting a broad reference library into a customer-specific, answerable, approved, and reproducible evaluation contract quickly enough to protect the pilot launch window.

### Strategy Kernel

**Diagnosis:** Question volume without answerability and source approval creates review load rather than launch confidence.  
**Guiding policy:** Build the smallest customer-specific golden dataset that proves the in-scope CSR Chat experience across eligible taxonomies, boundaries, and safe failure behaviors.  
**Coherent actions:** Freeze the pilot data contract, classify taxonomy eligibility, assemble source-grounded cases, conduct bounded dual review, publish a versioned QA package, and reuse the resulting method for the next customer.

## Proposed Solution

Create a managed Customer Golden Dataset workflow for CSR Chat rapid pilots. Data Science starts from the CSR Chat taxonomy library, maps each candidate question to the accepted customer plan data and GA capability matrix, and produces a versioned golden dataset package for customer or delegated SME approval.

Each golden case defines the intended user question, required context, expected response outcome, source evidence, answerability state, and review status. The package covers supported answers as well as clarification, unsupported, refusal, and escalation behaviors. Only cases supported by the accepted non-PHI data contract count toward answer-quality scoring; excluded taxonomies and unsupported questions remain visible as declared coverage boundaries.

The first release is a managed workflow and reusable data contract, not a self-service application. It uses automation where it reduces assembly effort while retaining human approval for ground truth.

## Target Users

**Primary Users:**

* **Data scientist / evaluation lead:** Needs a repeatable method to assemble, score, version, and compare customer-specific golden cases.
* **Customer or delegated benefits SME:** Needs a bounded reviewer view with source evidence and clear approve, reject, or revise decisions.
* **Implementation lead:** Needs an approved dataset version, coverage statement, and launch QA result that fit the rapid-deployment runbook.
* **CSR Chat product owner:** Needs an explicit contract for what the pilot will and will not answer.

**Secondary Users:**

* **Engineering and QA:** Need machine-readable expected outcomes for repeatable prelaunch validation and regression checks.
* **Customer Success and Sales:** Need a truthful coverage summary, limitations, and evidence for the pilot conversation.
* **Security and compliance reviewers:** Need proof that the dataset is non-PHI, tenant-bound, source-traceable, and free of credentials or member records.

## Success Metrics

| Metric | Baseline | Target | Measurement window and source |
| --- | --- | --- | --- |
| **Review-ready dataset lead time** | Not yet measured; F3A sets a 48-hour generation target but not end-to-end approval time. | By the third rehearsal, produce a review-ready customer dataset within 2 business days after complete intake acceptance. | Intake and package timestamps for each rehearsal or pilot. This leaves capacity inside the seven-day deployment runbook. |
| **Approved launch-sample quality** | No customer-approved rapid-pilot baseline supplied. | At least 95% pass on the customer-approved launch sample, with zero critical unsupported assertions and zero cross-customer source contamination. | Prelaunch QA results and exception log for every dataset version. |
| **Coverage and traceability completeness** | The reference workbook supplies taxonomy examples but not customer eligibility or approval status. | Cover 100% of customer-approved, in-pilot taxonomies; include at least one supported, one boundary/clarification, and one unsupported/escalation case where applicable; 100% of scored cases contain required source, version, answerability, and approval fields. | Dataset completeness check and coverage matrix before release. |

## Scope

### In-Scope Capabilities

1. **CSR Chat taxonomy eligibility matrix**  
   For each of the 17 reference taxonomies, record `Included`, `Conditional`, or `Excluded` for the pilot based on the GA capability matrix, accepted customer data, non-PHI boundary, and customer-approved use cases. Record the reason, required source, and owner of each decision.

2. **Golden case contract**  
   Define the required record fields for case ID, CSR Chat experience, taxonomy, question, required context, expected outcome, expected answer or response behavior, source reference, plan/dataset version, effective date, answerability state, risk tier, reviewer decision, and approval timestamp.

3. **Answerability and response-state model**  
   Classify each case as `Supported answer`, `Clarification required`, `Unsupported by accepted data`, `Safety refusal`, or `Human escalation`. Scored quality must evaluate the expected state, not reward an answer when the correct behavior is to clarify or escalate.

4. **Data Science assembly workflow**  
   Produce candidate cases from the CSR Chat reference library and customer data, deduplicate equivalent questions, preserve meaningful variations, attach source evidence, and flag unresolved or unsupported cases before customer review.

5. **Bounded SME review and adjudication**  
   Provide a reviewer-ready view that supports approve, reject, and revise decisions; captures rationale; prevents unresolved cases from entering the scored launch sample; and identifies the decision owner for disputed benefit interpretation.

6. **Versioned pilot evidence package**  
   Publish a machine-readable dataset, human-readable coverage and limitations summary, QA result, exception log, and dataset/version identifier tied to one customer tenant and accepted source package.

7. **Two timed rehearsals**  
   Run the workflow once with the approved reference/synthetic plan package and once with a customer-provided or approved representative non-PHI package. Measure elapsed effort, review changes, defects, and the steps that should be automated next.

### Taxonomy Eligibility Rules for the First Release

* A taxonomy is eligible only when the accepted customer package and GA services contain the facts needed to produce the expected outcome.
* A taxonomy may be conditional when only a subset of its questions is answerable. For example, static deductible limits may be supported while “How much have I met?” remains unsupported without member accumulator data.
* Claims, eligibility, member balances, account transactions, and other member-specific questions are excluded unless separately approved data and capability are present. Their expected golden behavior is escalation or an explicit unsupported response, not a fabricated answer.
* Dataset-size targets do not override eligibility, source quality, reviewer capacity, or launch relevance.

### Initial CSR Chat Eligibility Hypothesis

This is the Week 0 product hypothesis, not an approval of data availability or GA capability. Week 1 must confirm or change every row against the accepted customer package.

| CSR Chat taxonomy | Initial status | First-release boundary |
| --- | --- | --- |
| `COVERED_SERVICE` | Candidate included | Answer only when the accepted plan source defines the service, effective period, and applicable conditions. |
| `MEMBER_COST_SHARE` | Candidate included | Support static plan cost share with explicit network/site assumptions; exclude personalized estimates that need member accumulators or claims. |
| `PROVIDER_NETWORK` | Conditional | Requires approved provider-directory and network-participation data; otherwise clarify or route to the approved directory/support channel. |
| `PHARMACY_BENEFIT` | Conditional | Requires current formulary, tier, pharmacy-channel, and utilization-management sources. |
| `CODE_BENEFIT_MAPPING` | Conditional | Requires approved code sets and code-to-benefit mappings for the customer plan. |
| `OUT_OF_AREA_COVERAGE` | Candidate included | Support plan-level travel, emergency, reciprocity, and geographic rules when present in the accepted source. |
| `AUTHORIZATION_REFERRAL` | Candidate included | Requires current service/code authorization and referral rules, effective dates, and approved process references. |
| `ACCUMULATORS` | Conditional | Support static deductible and out-of-pocket rules; current met/remaining balances are unsupported without approved member data. |
| `BENEFIT_LIMITS` | Candidate included | Support static limits and frequency rules; remaining utilization is unsupported without approved member history. |
| `CLAIMS_MEMBER_ADMIN` | Boundary / escalation only | Claims, EOB, denial, eligibility, and dependent questions require member or transaction data outside the default non-PHI pilot. |
| `BENEFIT_ACCOUNTS_PROGRAMS` | Conditional | General plan/program rules may be supported; balances, transactions, reimbursement status, and tax advice remain outside the default pilot. |
| `ANCILLARY_SPECIALTY_BENEFITS` | Conditional | Requires the applicable dental, vision, hearing, or specialty plan sources and vendor/network data. |
| `CARE_NAVIGATION_CONTINUITY` | Conditional | Requires approved provider, service-area, continuity, referral, and authorization sources; no subjective provider recommendation. |
| `MEMBER_SUPPORT_RESOLUTION` | Candidate included | Validate approved routing, escalation, grievance, and human-handoff behavior without exposing member-specific case data. |
| `CLINICAL_SAFETY_BOUNDARIES` | Candidate included | Validate refusal, emergency/crisis language, and routing; diagnosis or treatment advice is never a supported answer. |
| `CONVERSATION_QUALITY_INCLUSION` | Candidate included | Validate clarification, consistency, feedback, and approved language/accessibility behavior within GA capability. |
| `BENEFIT_TRANSITIONS_EXCEPTIONS` | Conditional | Support only scenarios whose controlling dates, classifications, and exception rules are present; member-specific transitions otherwise escalate. |

### Open Strategy-Alignment Decisions

* The strategic source names both November 1 and December 31, 2026 as the first-customer deadline. The objective owner must identify the governing commitment.
* The strategic source uses both seven business days and seven calendar days. This PRD uses seven calendar days as the stricter constraint until the owner resolves the wording.
* The strategy refers to KR2 in its independence and lever sections but does not define KR2 in the OKR table. The objective owner should define whether repeatable dataset preparation is part of KR2 or only enabling evidence for KR3/KR4.
* The September 30 sales-demo milestone precedes this PRD's authored date. The decision owner should record whether the feature is a recovery action, a live-pilot dependency, or a post-demo scale improvement.

### Four-Week Milestones

* **Week 1 — Contract and eligibility:** Freeze required fields, scoring definitions, risk tiers, reviewer roles, accepted sources, and the first CSR Chat taxonomy eligibility matrix.
* **Week 2 — Reference package:** Assemble the reference/synthetic customer package, reviewer view, coverage report, and completeness checks.
* **Week 3 — Customer-like rehearsal:** Assemble and review the second non-PHI package; run CSR Chat against the approved sample; measure lead time and defects.
* **Week 4 — Operationalize:** Resolve launch-blocking gaps, publish the reusable runbook and evidence package, and obtain Product, Data Science, Implementation, Security, and SME signoff.

## Out-of-Scope

* **A universal 500+ pair requirement:** Dataset size is not a launch KPI because unsupported or redundant volume increases review effort without proving pilot quality.
* **Production self-service dataset administration UI:** The first release uses managed artifacts and a runbook to meet the timebox.
* **Automatic approval of generated answers:** Human approval remains required for customer ground truth.
* **Member-level PHI, claims, eligibility, current accumulator balances, or account transactions:** These require separate data, security, and product scope.
* **Customer SSO, contact-center integration, CRM integration, or real-time source synchronization:** The rapid-pilot strategy excludes these dependencies.
* **Cross-customer answer reuse without revalidation:** Taxonomy patterns and workflow components may be reused, but customer answers and source evidence cannot be assumed equivalent.
* **Adaptive production drift detection or continuous retraining:** Dataset refresh triggers are defined here; automated drift management is a later feature.
* **Replacing the GA capability matrix or minimum AtlasIQ data contract:** This feature consumes those approved inputs and does not broaden them.

## Product Requirements and Acceptance Semantics

| Requirement | Acceptance semantics | Intended outcome |
| --- | --- | --- |
| **REQ-GD-01 — Eligibility before generation** | No customer case enters review until its taxonomy, required facts, and source availability are classified. | Prevent review effort on questions the pilot cannot support. |
| **REQ-GD-02 — Source-grounded expected outcomes** | Every scored case resolves to an approved source and dataset version or to an explicitly approved non-answer behavior. | Make correctness reproducible and auditable. |
| **REQ-GD-03 — Boundary behavior is first-class** | Clarification, unsupported, refusal, and escalation cases are retained and evaluated alongside supported answers. | Prevent authoritative responses when facts or permissions are missing. |
| **REQ-GD-04 — Customer-specific approval** | Only cases approved by the named SME, or by a delegated approver recorded in the package, enter the launch sample. | Establish customer-owned ground truth. |
| **REQ-GD-05 — Versioned release evidence** | Every QA result identifies customer/tenant, golden dataset version, source dataset version, application/build version, date, and approved exceptions. | Support launch decisions, replay, and rollback. |
| **REQ-GD-06 — Fail closed on invalid source state** | Missing, stale, rejected, cross-customer, or unapproved sources block dataset release and cannot silently fall back to another customer or version. | Protect product truthfulness and tenant safety. |
| **REQ-GD-07 — Bounded review throughput** | The reviewer view separates unresolved cases, supports batch decisions, and reports review volume and elapsed time. | Keep approval work inside the rapid-pilot timeline. |

### Acceptance Examples

1. **Supported static benefit**  
   Given the accepted customer plan source defines physical therapy coverage and limits, when a physical therapy case is assembled, then the expected answer cites the correct plan/version and records the applicable limits and context.

2. **Missing member-specific accumulator data**  
   Given the pilot contains static plan accumulator limits but no member balances, when the question asks how much deductible the member has met, then the golden outcome is `Human escalation` or `Unsupported by accepted data`, not a numeric answer.

3. **Ambiguous network context**  
   Given network tier or place of service changes the answer and the question supplies neither, when the case is evaluated, then the expected outcome is `Clarification required` and identifies the missing facts.

4. **Clinical advice boundary**  
   Given a question asks for diagnosis or presents an urgent safety signal, when the case is evaluated, then the expected outcome uses the approved safety refusal or emergency escalation language and does not provide clinical advice.

5. **Stale source version**  
   Given the approved plan source has expired or been replaced, when a dataset release is attempted, then the release is blocked until the case set is regenerated or reapproved against the current source.

6. **Excluded taxonomy**  
   Given a taxonomy requires data outside the approved pilot contract, when coverage is reviewed, then the taxonomy is listed as excluded or conditional with rationale, customer-facing limitation, and owner; its absence does not reduce the in-scope quality score.

## Material Alternatives Considered

| Alternative | Advantages | Costs and risks | Decision |
| --- | --- | --- | --- |
| **A. Extend F3A as a high-volume automated generator** | Maximizes question count and may support long-term scale. | Creates a large review surface; does not resolve answerability, approval, or launch packaging; risks missing the rapid-pilot window. | Not selected for the first rapid-pilot release. Preserve generation components as inputs to the managed workflow. |
| **B. Use one fixed reference dataset for every customer** | Fastest setup and easiest comparison across prospects. | Weak customer relevance; may test facts or capabilities the customer did not provide; cannot serve as customer-owned ground truth. | Retain only as the synthetic demo fallback and first rehearsal. |
| **C. Taxonomy-driven, answerability-gated customer package** | Aligns with non-PHI scope, 95% customer-approved QA, explicit limitations, and repeatability. | Requires SME time and disciplined source/version management; initially more managed than automated. | Selected. Most reversible path and best fit for the four-week timebox. |

## Dependencies, Owners, and Decision Gates

| Dependency or decision | Owner | Needed by | Gate or effect |
| --- | --- | --- | --- |
| Frozen GA capability and known-limitations matrix | Product + Engineering | Start of Week 1 | Defines which response behaviors may be represented as supported. |
| Approved minimum non-PHI AtlasIQ data contract and source package | Data/AtlasIQ + Security | Start of Week 1 | Determines taxonomy eligibility and blocks customer-case assembly if incomplete. |
| Named benefits SME and backup approver | Customer Success + customer | Before customer-like rehearsal | Blocks approval of the launch sample. |
| Taxonomy library owner and change process | Product + Data Science | End of Week 1 | Prevents uncontrolled taxonomy or semantics drift. |
| QA execution path that records dataset and application versions | Engineering + QA | Week 3 | Required for reproducible launch evidence. |
| Secure storage and tenant association for artifacts | Security + Engineering | Week 2 | Blocks customer-package use if isolation or access is unapproved. |

## Risks, Scenarios, Triggers, and Mitigations

| Risk or scenario | Trigger | Mitigation / decision response |
| --- | --- | --- |
| **Review volume threatens the timeline** | First-pass reviewer effort exceeds 8 person-hours or more than 20% of cases require substantive rewrite. | Reduce redundant variants, narrow the launch sample to highest-priority eligible use cases, and log automation candidates; do not lower the approval standard. |
| **Customer data supports fewer taxonomies than expected** | One or more priority taxonomies lack required facts. | Mark the taxonomy conditional/excluded, disclose the limitation, use approved escalation behavior, and require Product approval for any expanded data request. |
| **Generated answers inherit source or model errors** | Source mismatch, unsupported assertion, or reviewer rejection. | Require source-level traceability, independent SME approval, and regeneration/review after material source changes. |
| **Customer approval arrives late** | No named reviewer or review window before the customer-like rehearsal. | Make reviewer assignment and review dates part of intake acceptance; stop the launch clock until complete intake is accepted while continuing to report commercial sign-to-online separately. |
| **Cross-customer contamination** | Any source, answer, identifier, or artifact references another customer. | Block release, investigate the workflow, rebuild the package from tenant-bound inputs, and require Security/QA signoff before reuse. |
| **Scope expands into member-specific operations** | Claims, current balances, eligibility, or transaction questions are requested as supported answers. | Keep their golden behavior as unsupported/escalation unless a separately approved scope and data contract is provided. |
| **The four-week feature window misses the rapid-pilot need** | Week 1 cannot freeze contract/owners or Week 2 rehearsal cannot produce a complete reference package. | Ship a smaller approved taxonomy subset with explicit exclusions; do not substitute unreviewed generated volume. |

## Assumptions, Confidence, and Validation Plan

* **High confidence:** Taxonomy eligibility, source traceability, and explicit non-answer behaviors directly support the strategy's answer-quality and truthfulness gates.
* **Medium confidence:** A review-ready package can be produced within two business days. Validate through two timed rehearsals; revise the operating target based on measured work without weakening the seven-day commercial commitment.
* **Medium confidence:** A managed artifact workflow is sufficient for the first pilots. Reconsider a production UI after five completed packages or when review/assembly effort exceeds the agreed threshold.
* **Low confidence / decision required:** The strategic source states both a November 1 and a December 31 first-customer deadline. This PRD uses relative launch-readiness gates and requires the objective owner to confirm the governing commercial date.

## Exit Criteria

* [ ] The CSR Chat taxonomy eligibility matrix covers all 17 reference taxonomies and records inclusion status, rationale, data dependency, limitation wording, and owner.
* [ ] The golden case contract is approved by Product, Data Science, Engineering/QA, Security, Implementation, and a benefits SME.
* [ ] Every scored case includes the required customer/tenant, taxonomy, context, expected outcome, source/version, answerability, risk, and approval fields.
* [ ] The package distinguishes supported answers, clarification, unsupported, safety refusal, and human escalation behaviors.
* [ ] The reference/synthetic rehearsal and customer-like non-PHI rehearsal complete using the same contract and runbook.
* [ ] At least 95% of the approved launch sample passes, with zero critical unsupported assertions and zero cross-customer contamination; all accepted exceptions identify owner, rationale, mitigation, and expiry/revisit date.
* [ ] Coverage reporting accounts for 100% of customer-approved in-pilot taxonomies and shows explicit conditional or excluded areas without lowering the in-scope quality denominator.
* [ ] A timed rehearsal demonstrates a review-ready package within two business days of complete intake, or the decision owner approves a narrower scope that preserves the seven-day launch ceiling.
* [ ] Release evidence identifies golden dataset version, source dataset version, customer/tenant, CSR Chat build/version, QA date, reviewer, and approval status.
* [ ] Security confirms non-PHI handling, tenant association, least-privilege access, retention, and rejection of invalid or cross-customer sources.
* [ ] Customer Success and Sales receive the approved coverage/limitations summary and do not present excluded capabilities as supported.
* [ ] The team records assembly hours, review hours, defect categories, rejected cases, and automation candidates for the scale/no-scale decision after five packages.

## Requirement-to-Outcome Traceability

| Requirement | Outcome | Metric / exit evidence |
| --- | --- | --- |
| REQ-GD-01, REQ-GD-07 | Faster, bounded dataset creation and review | Review-ready dataset lead time; timed rehearsal; review effort log |
| REQ-GD-02, REQ-GD-04 | Customer-approved answer correctness | ≥95% launch-sample pass; approval history; source references |
| REQ-GD-03 | Safe behavior when questions are ambiguous or unsupported | Boundary-case coverage; zero critical unsupported assertions |
| REQ-GD-05 | Reproducible launch and regression evidence | Versioned evidence package and replay metadata |
| REQ-GD-06 | Product truthfulness and tenant safety | Release-blocking source checks; zero cross-customer contamination |

---

Template: `Feature-1-Pager-PRD.md` `v2.0`  
Feature PRD Skill: `v1.1`
