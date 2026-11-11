# 🧩 Project Name: Sales CSR Chat App

## 🎯 Problem Statement

Stellarus BD&P team will begin, in October 2026, to drive demand creation with new customers buying into Compass CSR Chat. All currently available implementations of CSR Chat maintain Blue Shield of California benefit plan data with California specific details and trademarked information. These cannot be used to sell to demonstrate the product and its capabilities to new customers.

**Current baseline:** The application tenant and core Compass CSR Chat path are accepted as capable. Formal readiness evidence for the three remaining areas is not yet established: no approved synthetic plan coverage matrix, no approved application-access completion target, and no completed sanitation inventory for prompts, rules, and scripts.

### 💡 Proposed Solution

Establish Stellarus as a customer tenant and delivering three coordinated readiness packages on top of the existing Compass CSR Chat with the new user interface, in production:

1. **Synthetic Benefits Data:** Publish a versioned, synthetic-only, or sanitized, plan catalog in the tenant's Benefits Service partition. The catalog will use the supported plan schema and cover the benefit structures needed for the approved sales and quality scenarios.
2. **Application Authentication:** Provide a supported sign-in and role-mapping flow for authorized internal Sales team users. Authentication will resolve the correct tenant and CSR persona, establish a bounded session, and fail closed for unauthorized or incorrectly scoped users.
3. **Sanitized CSR Content Profile:** Create a versioned tenant-neutral prompt, rule, and script bundle. It will remove customer names, customer-only links, proprietary language, real contact details, and unsupported customer-specific assumptions while preserving the approved benefits-answer behavior and structured presentation required by the new UI.

The release will bind these three packages to the existing tenant configuration and validate them through the new UI. Core platform services remain dependencies and regression boundaries, not delivery scope.

### Reference Journey

1. An authorized presenter signs in through the approved authentication flow and enters the synthetic tenant as a CSR user.
2. The user selects or enters an approved synthetic plan and sees plan details retrieved from Benefits Service in the new UI.
3. Suggested questions align to facts that exist in the selected synthetic plan.
4. The user asks a benefits question and receives a structured response governed by the sanitized prompt, rule, and script profile.
5. The answer uses tenant-neutral language, references only synthetic plan facts, and contains no real customer identifiers, links, contacts, or branded operational instructions.
6. Invalid credentials, missing roles, missing plans, unsupported questions, and unavailable data produce the approved safe behavior.

## 👥 Target Users

**Primary Users:**

* **Sales or product presenter:** Needs predictable sign-in and a credible, neutral benefits experience that can be demonstrated without customer data or manual setup.
* **Customer implementation lead:** Uses the tenant to explain the product workflow and the data, identity, and content inputs required for a future customer implementation.

**Secondary Users:**

* **CSR experience designer or researcher:** Validates that the new UI renders plan context, suggested questions, answers, disclosures, warnings, and failures coherently.
* **Support engineer:** Diagnoses access, data, configuration, and content-version issues in the hosted tenant.

## ✅ Success Metrics

| Metric                                     | Baseline                                                          | Release target                                                                                                                                                                                                                          | Window and measurement source                                                                                                 |
| ------------------------------------------ | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Synthetic scenario data coverage** | No approved hosted synthetic-plan coverage matrix                 | 100% of at least 20 approved benefits scenarios map to versioned Benefits Service source facts; zero real PHI/PII, real customer plan records, or production contact details                                                            | Before release and on each seed revision; scenario-to-source matrix plus data provenance review                               |
| **Authenticated access success**     | No approved synthetic-tenant access completion target             | 100% of approved positive and negative role/tenant scenarios pass; all five pilot internal users sign in and reach the correct tenant without manual credential or configuration intervention; median sign-in-to-ready time ≤2 minutes | Three release-candidate runs and first 30 days; authentication events and moderated access checks                             |
| **Sanitized answer quality**         | No completed sanitation inventory or tenant-neutral quality score | 100% of prompt/rule/script inventory reviewed with zero unresolved customer-specific leakage; ≥95% grounded resolution on eligible scenarios, ≥99% safe handling overall, and zero critical unsupported benefit or cost-share claims  | Frozen evaluation set before release and weekly for 30 days; content diff, automated scans, SME review, and AI Quality rubric |

**Guardrails:** zero cross-tenant access; zero real customer or member data; zero customer-specific names, URLs, phone numbers, credentials, or proprietary operational instructions in the approved content bundle or rendered responses; 100% of evaluated turns identify the synthetic tenant, dataset version, and content-profile version; no material regression in the established core Compass CSR Chat journey.

## 📦 Scope

### Task-Ready Work Packages

| ID     | Deliverable                                  | Completion evidence                                                                                                                                       |
| ------ | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SCT-01 | Scenario and synthetic-data coverage matrix  | At least 20 approved questions map to required plan structures, expected facts, boundaries, and safe outcomes                                             |
| SCT-02 | Contract-faithful synthetic plan catalog     | Versioned seed loads into the correct Benefits Service tenant partition, passes schema/provenance review, and supports the coverage matrix                |
| SCT-03 | Seed verification and reset process          | Authorized operator can verify, refresh, and restore the approved dataset without code changes or manual database edits                                   |
| SCT-04 | Authentication and role mapping              | Approved users sign in as the correct synthetic-tenant CSR persona; missing, expired, unauthorized, and wrong-tenant contexts fail closed                 |
| SCT-05 | Prompt sanitation and neutral system profile | Tenant-neutral system prompt preserves CSR behavior while removing customer identity, proprietary workflow, and customer-only references                  |
| SCT-06 | Rule and script sanitation                   | Rule/script inventory has approved neutral replacements, configuration-backed references, or explicit exclusions for every customer-specific item         |
| SCT-07 | New UI content integration                   | UI suggestions, plan preview, structured answers, disclosures, warnings, synthetic labeling, and reset behavior align with the seed and sanitized profile |

### Functional and Experience Requirements

#### Synthetic plan data

1. **SCT-FR-01 — Synthetic-only provenance:** Every hosted record must be generated or expressly approved as synthetic. No value may be copied from a real member, real customer plan, production log, credential, or proprietary customer artifact.
2. **SCT-FR-02 — Contract fidelity:** Synthetic plans must use the current supported Benefits Service schemas, tenant partitioning, effective-date semantics, nested benefit structures, cost-share structures, and source/freshness metadata.
3. **SCT-FR-03 — Scenario completeness:** The plan catalog must support every approved scenario with traceable source facts and expected answer semantics.
4. **SCT-FR-04 — Version and reset:** The active dataset version must be observable, reproducible, and restorable through an approved operator process.

#### Authentication

5. **SCT-FR-05 — Supported sign-in:** Authorized internal users must enter through the approved application authentication path without shared credentials, embedded secrets, or manual token handling.
6. **SCT-FR-06 — Trusted tenant and persona:** Tenant, CSR persona, actor, scopes, expiration, and correlation context must derive from verified identity and may not be overridden by browser-supplied tenant fields.
7. **SCT-FR-07 — Bounded authorization:** The initial role matrix must distinguish presenter, quality/reviewer, and support access where their permissions differ; unauthorized, expired, malformed, and wrong-tenant sessions fail closed.
8. **SCT-FR-08 — Session behavior:** Sign-out, expiration, and new-session behavior must clear prior synthetic member, plan, and conversation context.

#### Sanitized prompts, rules, and scripts

9. **SCT-FR-09 — Neutral content profile:** The approved system prompt must describe a tenant-neutral CSR benefits assistant and must not name or impersonate an existing customer.
10. **SCT-FR-10 — Customer-content removal:** Prompts, rules, scripts, suggestions, citations, links, contacts, terminology, and fallback text must contain no unapproved customer name, domain, phone number, knowledge-base link, credential, or proprietary operating instruction.
11. **SCT-FR-11 — Behavior preservation:** Sanitation must preserve supported benefits-answer behavior, including applicable cost shares, network distinctions, benefit limits, vendor/administrator handling, disclosures, unavailable-data behavior, and the prohibition against inventing absent facts.
12. **SCT-FR-12 — Configurable tenant references:** Where a response legitimately needs a tenant-specific label, resource, contact, or next step, it must resolve from approved tenant configuration or use an approved neutral fallback rather than hard-coded customer text.
13. **SCT-FR-13 — Versioned approval:** Prompt, rule, and script versions must be observable for every evaluated turn and require CSR Operations/Product approval before activation.

#### New UI integration and validation

14. **SCT-FR-14 — Synthetic labeling:** The new UI and captured artifacts must clearly identify the tenant and data as synthetic and not evidence of an individual's coverage.
15. **SCT-FR-15 — UI/data alignment:** Plan preview fields and suggested questions must derive from the active synthetic plan; changing plans must invalidate prior suggestions and conversation grounding.
16. **SCT-FR-16 — Structured response compatibility:** Sanitized content must render correctly in the new UI's coverage, detail, confidence/limitation, disclosure, and next-step structures without leaking raw templates or placeholders.
17. **SCT-FR-17 — Safe boundaries:** Missing plans, unsupported topics, absent source facts, unavailable Benefits Service, and authentication failures must produce the approved explicit error, clarification, abstention, or acknowledged degraded behavior.
18. **SCT-FR-18 — Accessibility:** Sign-in, plan selection, content, loading, warnings, errors, and chat interaction must meet WCAG 2.2 AA for the supported desktop journey.

### Synthetic Scenario Minimum Set

The initial catalog and evaluation set must cover, at minimum:

* primary-care and specialist visits with distinct cost shares;
* urgent and emergency care with an approved neutral disclosure;
* outpatient procedure with professional and facility distinctions;
* prescription benefit tier structure without claiming formulary status for a named drug when that data is absent;
* deductible and out-of-pocket maximum interpretation;
* in-network, out-of-network, and unsupported-network behavior;
* benefit with a synthetic vendor/administrator and non-routable approved contact presentation;
* no-charge and not-covered services;
* invalid plan, missing source fact, stale-data indicator, and Benefits Service unavailable;
* unsupported non-benefits question and neutral next-step behavior;
* authorized access, unauthorized role, expired session, and wrong-tenant denial; and
* plan change, sign-out, and new session with no prior-context carryover.

## 🚫 Out-of-Scope

* **Core platform construction:** Tenant hosting, BFF, broker routing, agent runtime integration, Benefits Service APIs, conversation transport, and platform telemetry are assumed operational and are not rebuilt in this release.
* **Real customer or member data:** No production PHI/PII, customer plan extracts, credentials, logs, or customer-authored proprietary content.
* **New identity platform:** The feature integrates an approved authentication path; it does not create a general identity provider or enterprise access-management system.
* **External self-service trial:** Independent prospective-customer account creation, persistent external access, terms acceptance, and external support are separate work.
* **All CSR domains:** Claims, eligibility, accumulators, formulary, provider lookup, scheduling, case management, and side-effecting service actions remain outside this Benefits Inquiry release.
* **General synthetic-data generation platform:** This release creates and governs one reference plan catalog, not an on-demand generator for arbitrary tenants or domains.
* **Prompt-management product:** Versioning and approval are required, but a new visual prompt/rule/script editor or approval workflow is not included.
* **Production-scale certification:** The release performs regression and readiness validation but does not claim customer peak-volume certification.

## Risks, Scenarios, Triggers, and Mitigations

| Risk / pre-mortem scenario                                            | Trigger                                                                                | Mitigation and decision response                                                                                             | Owner                      |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| Synthetic plans are too simple to exercise real answer behavior       | Coverage matrix lacks nested cost shares, network differences, limits, or vendor cases | Require contract-fidelity and scenario-to-field review before seed acceptance                                                | Benefits Data + AI Quality |
| Sanitization changes factual behavior                                 | Grounded-answer score falls or required disclosures disappear after content changes    | Compare source facts and expected semantics before/after sanitation; block activation on material regression                 | CSR Content + AI Quality   |
| Customer-specific content remains in a low-frequency rule             | Scan or scenario reveals a name, URL, phone number, or customer-only instruction       | Maintain complete asset inventory; combine automated scanning with SME review; zero unresolved leakage at release            | CSR Content Owner          |
| Authentication works only through presenter workarounds               | Users require manual tokens, shared credentials, or operator configuration             | Make unsupported access paths ineligible for acceptance; validate five pilot users independently                             | Identity Owner             |
| Wrong tenant or persona is resolved                                   | Negative access test reaches plan or chat data                                         | Fail closed and block release; derive context only from verified identity                                                    | Identity + Security        |
| New data/content configuration regresses the working platform journey | Baseline smoke passes but release-candidate journey fails                              | Compare against kickoff baseline; fix in-scope configuration or triage an external platform defect with owner before release | Delivery Lead              |
| Synthetic content is mistaken for actual coverage                     | UI or screenshot lacks synthetic labeling                                              | Persistent synthetic labeling and presenter guidance; block unlabeled artifact export                                        | Product + Design           |

## 🏁 Exit Criteria

### Synthetic Plan Data

* [ ] A versioned synthetic plan catalog is hosted in the correct Benefits Service tenant partition and can be restored through the approved reset process.
* [ ] The dataset provenance review confirms zero real PHI/PII, real customer plan records, production identifiers, or production contact details.
* [ ] At least 20 approved scenarios map to explicit source facts in the catalog, including required success, boundary, missing-data, and unsupported cases.
* [ ] Plan preview, suggested questions, and expected answers use the current Benefits Service contract and the active dataset version.

### Authentication

* [ ] Five pilot internal users can sign in through the supported application path and reach the correct synthetic tenant and CSR persona without shared credentials, manual tokens, or operator intervention.
* [ ] Approved presenter, reviewer, and support permissions match the signed-off role matrix.
* [ ] Missing, malformed, expired, unauthorized, and wrong-tenant contexts fail closed and expose no plan or conversation data.
* [ ] Sign-out, expiration, and new-session behavior clear prior member, plan, and conversation context.

### Sanitized Prompts, Rules, and Scripts

* [ ] Every prompt, rule, script, suggestion, citation, link, contact, disclosure, and fallback asset is inventoried with keep, replace, configure, or exclude disposition.
* [ ] The approved bundle contains zero unresolved customer-specific names, domains, phone numbers, knowledge-base links, credentials, or proprietary instructions.
* [ ] Tenant-neutral replacements preserve supported CSR benefits behavior and render without raw placeholders, template instructions, or customer impersonation.
* [ ] Legitimate tenant references resolve from approved configuration or use approved neutral fallback language.
* [ ] Prompt, rule, and script versions are visible in evaluation evidence and approved by Product.

### New UI and Release Readiness

* [ ] The hosted new UI completes the approved sign-in, plan selection, suggested question, structured answer, failure, sign-out, and reset journeys.
* [ ] A kickoff smoke and final regression run confirm no material regression in the established Compass CSR Chat platform path.
* [ ] Dataset reset, content rollback, access revocation, and tenant-disable procedures are rehearsed and documented.

---

Template Version: `v2.0`
