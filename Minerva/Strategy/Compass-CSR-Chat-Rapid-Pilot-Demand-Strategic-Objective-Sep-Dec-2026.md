# OBJECTIVE: Compass CSR Chat Campaign & Rapid Deployment

**Status:** In-Review
**Authored Date:** 09/02/2026
**Objective Window:** 09/02/2026–12/31/2026

---

## 📝 Executive Summary

Compass CSR Chat needs a repeatable demand-creation motion that allows prospective customers to experience the complete product—from the customer-facing interface through AtlasIQ Benefits data services. By September 30, 2026, Sales will need an end-to-end, white-label-ready demonstration experience using a synthetic plan dataset and by November 1, 2026, the ability to launch at least one net-new customer in a tenant-specific rapid-deployment pilot. Using product-managed authentication and non-PHI capabilities prioritizing speed, product integrity, and repeatability by simplifying data delivery, minimum viable AtlasIQ ingestion path, and little to no customer-system integrations.

## 🎯 Strategic Context & Vision

- **Company Alignment:** Supports executive-sponsored growth priority to create net-new demand, shorten time-to-value, and turn Compass CSR Chat into a product that can be demonstrated and deployed without a bespoke implementation cycle.
- **Problem Statement:** The complete CSR Chat experience depends on customer-specific plan data, branding, tenant setup, access, and AtlasIQ services. If every prospect requires external identity, application, or real-time data integration before seeing value, Sales cannot move quickly enough to generate and convert demand.
- **Strategic Choice:** Productize two related but distinct paths: a rapidly configurable sales demo and a production-grade, tenant-specific customer pilot. Both use the shared Compass CSR Chat product and AtlasIQ services, while the live pilot is restricted to non-PHI capabilities and launch-grade controls.
- **The Vision:** A qualified prospect can move from interest to a branded, data-relevant demonstration in as little as 24 hours, and a signed net-new customer can be using theire tenant-isolated CSR Chat pilot within seven business days—without an external authentication or customer-application integration project.

## 📊 OKR Framework

### Objective (Qualitative)

> **Create a repeatable rapid-deployment motion for Compass CSR Chat that enables Sales to demonstrate customer-relevant end-to-end value by September 30, 2026, and brings the first net-new customer live on a limited, tenant-specific pilot within seven busness days of signing and no later than November 1, 2026.**

### Key Results (Quantitative)

| Key Result                                       | Committed Target and Planning Range                                                                                                                                                                                                                                                                                                                                              | Due Date                          | <br />Accountable Owner                                                                   |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | ----------------------------------------------------------------------------------------- |
| **KR1 — *Sales-ready end-to-end demo*** | One approved reference experience demonstrates the path from CSR Chat front end through AtlasIQ services with synthetic plan data; includes white-label configuration. Planning confidence: 80–90% if the minimum dataset and environment are confirmed by 09/08.                                                                                                            | 09/30/2026                        | **Product**<br />**Engineering**<br />**BD&P / Sales** |
| **KR3 — *First net-new customer online***   | At least one net-new customer signs and is live within 7 business days, white-labeled tenant using current GA features and product-managed username/password; 100% of signed rapid pilots meet a maximum seven-calendar-day sign-to-online time. Planning confidence: 70–85% because customer signature timing is an external dependency.                                       | 11/01/2026                        | **Product<br />BD&P / Sales**<br />**Implementation**                       |
| **KR4 — Safe, credible pilot operation**  | 100% of accepted pilot datasets pass the non-PHI intake gate;<br />100% of launch-blocking tenant, access, data, and GA-capability checks pass; <br />pilot benefit-answer QA achieves at least 95% on the customer-approved sample; <br />zero Sev-1/Sev-2 security or cross-tenant incidents. <br />Target confidence: 85–95% when customer inputs meet the defined contract. | Demo: 09/30/2026; live pilot: TBD | **Engineering**<br />**Security**<br />**Product** <br />**BD&P** |

### KR Independence

- **KR1** proves that a credible product story exists.
- **KR2** proves that the story can be reproduced at demand-generation speed.
- **KR3** proves conversion from sales interest to real customer use.
- **KR4** ensures speed does not compromise accuracy, tenant isolation, data handling, or product truthfulness.

## 🕹️ Strategic Levers

- **Lever 1 — Standardized demo blueprint:** Maintain a deployable reference tenant, frozen GA capability matrix, scripted demonstration journey, and readiness checklist so each request starts from a known-good product baseline. This primarily moves KR1 and KR2.
- **Lever 2 — Minimum viable AtlasIQ data contract:** Define the smallest approved non-PHI customer plan-data package, validation rules, manual delivery method, ingestion runbook, and fallback dataset needed to populate AtlasIQ services. This primarily moves KR1, KR2, and KR4.
- **Lever 3 — Configuration instead of integration:** Use a bounded white-label configuration package and product-managed access instead of customer SSO, CRM, contact-center, or real-time source integrations. This primarily moves KR2 and KR3.
- **Lever 4 — Dual-mode product storytelling:** Demonstrate existing GA features as functional software and future roadmap ideas only as visibly labeled concept previews. This moves KR1 while protecting KR4.
- **Lever 5 — Pre-stage live-pilot inputs:** Complete commercial, data, brand, user-access, and compliance intake during the late sales stage so the seven-day sign-to-online clock can be met after signature. This primarily moves KR3.

## 🎟️ Themes & High-Level Requirements

### Theme A: Sales-Ready End-to-End Experience

- **GA product path:** The demo must operate from the customer-facing CSR Chat interface through the required AtlasIQ data services using the current supported CSR Chat feature set.
- **Customer-relevant plan data:** The experience must use a small, approved, non-PHI subset of customer plan data when supplied; an approved synthetic/reference dataset must be available when customer data is late or unusable.
- **Repeatable demo journey:** Sales must have an approved talk track, representative benefit questions, known limitations, reset instructions, and a clear escalation path.
- **Evidence:** The package must include an end-to-end smoke result, dataset/version identifier, build/version identifier, and readiness approval.

### Theme B: Bounded White Label and Roadmap Storytelling

- **White-label assets:** Support the approved customer-facing product name, logo, primary/accent colors, panel title, and customer terminology available within current configuration boundaries.
- **Asset kit:** Publish input specifications for file type, dimensions, accessibility, approval, and fallback assets so branding does not require design or engineering work for each demo.
- **Roadmap concept previews:** Future features may be shown through non-production mockups, prototypes, or clearly isolated preview states.
- **Truth-in-demo control:** Every concept preview must be labeled `Concept Preview — Not a Live Product Feature`, and Sales must distinguish it from GA behavior in the talk track.

### Theme C: Minimum Viable AtlasIQ Data Ingestion

- **Non-PHI boundary:** Customer-provided data must be limited to the non-PHI content required by GA CSR Chat features; datasets containing PHI or unapproved sensitive data are rejected.
- **Manual delivery:** Support a managed, secure, manual transfer and validation process; customer-built APIs, event streams, and real-time feeds are not prerequisites.
- **Minimum data contract:** Define required fields, supported formats, plan identifiers, effective dates, source/version metadata, volume limits, validation rules, and ownership.
- **AtlasIQ readiness:** Populate only the services and data structures required for the bounded experience; maintain dataset versioning, tenant association, ingestion status, and rollback/reload procedures.
- **Quality gate:** Fail closed on malformed, missing, stale, cross-tenant, or unapproved data rather than silently substituting another customer's data.

### Theme D: Rapid Live-Customer Pilot Deployment

- **Dedicated tenant:** Deploy an isolated customer tenant with approved branding, configuration, dataset binding, logging, and support ownership.
- **Lightweight access:** Provide product-managed username/password or magic-link authentication appropriate to the approved pilot security posture.
- **No external identity dependency:** Customer SSO, IdP federation, and external role mapping are not required for the limited pilot.
- **GA-only experience:** The live customer tenant exposes only capabilities confirmed in the signed-off GA capability matrix; roadmap concepts are not enabled as functional pilot features.
- **Seven-day launch plan:** Use a day-by-day runbook covering intake confirmation, tenant/configuration creation, data validation and load, access provisioning, QA, customer acceptance, and launch.
- **Pilot controls:** Define participant limits, pilot duration, support hours, acceptable use, data retention, incident response, exit criteria, and conversion or shutdown steps before access is issued.

### Theme E: Demand Measurement and Learning

- **Funnel instrumentation:** Track qualified demo requests, demo completion, lead time, prospect feedback, pilot offers, signatures, launches, and conversion decisions.
- **Learning loop:** Record which data, brand, security, and feature requests repeatedly threaten the standard package; promote only validated recurring needs into roadmap consideration.
- **Commercial feedback:** Capture objections and buying signals without expanding the active pilot scope during a committed deployment.

## ✅ Strategic Acceptance Criteria

### September Sales-Demo Gate

- [ ] A reference environment completes an approved end-to-end journey from CSR Chat UI through the required AtlasIQ services.
- [ ] A limited customer or reference dataset passes the non-PHI, schema, quality, version, and tenant-association checks.
- [ ] The approved white-label asset set can be applied without a custom application build.
- [ ] The GA capability matrix and known limitations are signed off by Product and Engineering.
- [ ] Roadmap concepts are technically or visually separated from the live product path and carry the required concept-preview label.
- [ ] Sales enablement includes an approved script, reset/runbook, evidence packet, and escalation route.
- [ ] A timed dry run proves the standard demo can be prepared within 24 hours and the exception path within seven calendar days.

### December Live-Pilot Gate

- [ ] A net-new customer has signed the bounded rapid-pilot agreement.
- [ ] Customer brand, user roster, minimum dataset, named approvers, and acceptable-use acknowledgment are complete or pre-staged at signature.
- [ ] The customer tenant is isolated and exposes only signed-off GA features.
- [ ] Product-managed username/password or magic-link authentication passes access, expiration/revocation, and unauthorized-use checks.
- [ ] Customer plan data is manually delivered, validated as non-PHI, loaded into the required AtlasIQ services, and traceable to an approved version.
- [ ] Customer-approved sample questions achieve at least a 95% pass rate, with any accepted exceptions documented before launch.
- [ ] Launch evidence shows no cross-tenant access, no launch-blocking defects, and a sign-to-online duration of no more than seven calendar days.
- [ ] Support, incident, data-retention, pilot-exit, and customer-feedback responsibilities are accepted by named owners.

## ⚠️ Constraints, Risks & Dependencies

### Constraints

- The September deadline leaves less than one month from objective authorization; scope control and reuse of existing product capability are mandatory.
- Customer data is restricted to the minimum non-PHI data required for GA CSR Chat features.
- Demo preparation may take 24 hours and must never exceed seven calendar days after complete intake.
- A signed live pilot must be online within seven calendar days; input collection therefore needs to begin before signature whenever possible.
- No customer-specific code fork is permitted for the rapid-deployment motion.

### Dependencies and Gating Decisions

| Dependency / Decision                                                         | Required By              | Owner                                            | Gate or Effect                                       |
| ----------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------ | ---------------------------------------------------- |
| Freeze GA capability and known-limitations matrix                             | 09/08/2026               | Product + Engineering                            | Blocks demo story, QA scope, and live-pilot contract |
| Approve minimum non-PHI AtlasIQ data contract and secure manual delivery path | 09/08/2026               | AtlasIQ/Data + Security                          | Blocks customer-data demo and ingestion runbook      |
| Select reusable demo environment and tenant-reset approach                    | 09/08/2026               | Engineering / Platform                           | Blocks timed demo dry run                            |
| Approve bounded white-label asset schema                                      | 09/10/2026               | Product / Design                                 | Blocks repeatable branded demo                       |
| Approve concept-preview labeling and sales claims                             | 09/15/2026               | Product + Sales + Legal/Compliance as applicable | Blocks roadmap storytelling                          |
| Approve lightweight authentication pattern for live pilots                    | 10/15/2026               | Security + Engineering                           | Blocks customer access provisioning                  |
| Secure first qualified customer and pre-stage inputs                          | 12/17/2026 at the latest | Sales + Decision Owner                           | Protects the seven-day launch window before 12/31    |

### Risks and Mitigations

- **Roadmap concepts are mistaken for committed functionality:** Prospects may assume previewed features are live or contractually included. **Mitigation:** separate preview surfaces, mandatory labeling, approved talk track, and written capability matrix.
- **September delivery is compressed:** Environment, data, or brand work could exceed the available time. **Mitigation:** use one reusable reference environment, cap configuration options, retain a synthetic dataset fallback, and run the first timed rehearsal by 09/18.
- **Customer data arrives late or fails validation:** Demo or pilot timing could be missed. **Mitigation:** publish the contract early, provide sample files and preflight validation, reject PHI, and use the reference dataset for sales demos when needed.
- **Seven-day sign-to-online target is consumed by intake:** A customer may sign before supplying usable data, assets, or users. **Mitigation:** pre-stage the minimum input package during late-stage sales and report both sign-to-online and complete-input-to-online durations.
- **Lightweight authentication is treated as enterprise integration:** Access requirements could expand into SSO or complex role mapping. **Mitigation:** contractually limit the pilot to username/password or magic link, a bounded user count, and a standard role model.
- **Manual ingestion does not scale:** Operational effort or data errors may grow with demand. **Mitigation:** instrument time and defect rates, standardize validation and reload steps, and use pilot evidence to prioritize automation only after repeat demand is proven.
- **Tenant or data leakage:** Fast setup can increase configuration error risk. **Mitigation:** fail-closed tenant binding, launch-blocking negative tests, dataset/version traceability, least privilege, and zero-tolerance cross-tenant incident health metric.
- **Pilot quality fails to establish value:** A narrow dataset may not answer representative questions well enough. **Mitigation:** agree on the sample question set before load, require 95% QA, disclose coverage limits, and prevent unsupported queries from appearing authoritative.
- **Commercial demand is weaker than delivery readiness:** A demo package alone does not ensure signed customers. **Mitigation:** assign a named target-account pipeline, instrument the funnel, and review qualified opportunities weekly with the decision owner.

### Out of Scope

- Customer SSO, IdP federation, SCIM, or customer-managed authentication integration.
- CRM, contact-center desktop, customer portal, Nexus, or other external application embedding/integration.
- Real-time customer data feeds, customer-built APIs, event streaming, or automated source-system synchronization.
- PHI, member-level data, claims, eligibility, or other data not required by GA CSR Chat features.
- Bespoke workflows, custom model training, customer-specific code forks, or features outside the frozen GA matrix.
- Treating roadmap concept previews as production features or including them in the live pilot.
- Full self-service administration, arbitrary low-code configuration, enterprise-scale identity, or broad production rollout.
- More than the minimum AtlasIQ services and data structures required for the bounded experience.

## 🏥 Health Metrics (Counter-Metrics)

- **Product truthfulness:** Zero roadmap previews presented without the required concept label; zero signed commitments that classify a preview as GA.
- **Security and tenancy:** Zero cross-tenant data access and zero Sev-1/Sev-2 security incidents.
- **Data handling:** 100% of customer datasets have non-PHI attestation, validation results, source/version metadata, and approved retention handling before load.
- **Answer quality:** At least 95% pass rate on the approved pilot question set; unsupported or out-of-scope questions must not be presented as verified answers.
- **Reliability:** 100% of demo and live-pilot launch smoke checks pass before access; availability target for the scheduled demo/pilot window must be agreed before launch.
- **Scope discipline:** Zero external integrations or customer-specific code forks introduced into the rapid-deployment path without decision-owner approval and objective revalidation.
- **Operational load:** Track person-hours per demo and live deployment from the first request; review after each launch and establish the automation threshold after five completed setups.
- **Customer experience:** No customer is declared online until their named approver completes the bounded acceptance check and receives limitations/support guidance.

## 🧱 Timeline & Milestones

- **Milestone 1 — Scope and contracts frozen:** GA capability matrix, minimum AtlasIQ dataset, white-label schema, reference environment, owners, and demo checklist approved — **09/08/2026**
- **Milestone 2 — First integrated reference experience:** UI-to-AtlasIQ path operates with reference data and default branding — **09/15/2026**
- **Milestone 3 — Timed sales rehearsal:** White-label application, roadmap preview controls, reset, evidence pack, and standard demo setup completed in 24 hours — **09/18/2026**
- **Milestone 4 — Sales-ready launch:** Demo package approved and available to Sales — **09/30/2026**
- **Milestone 5 — Live-pilot deployment package:** Product-managed authentication, customer tenant runbook, data intake, QA, support, and pilot terms approved — **10/31/2026**
- **Milestone 6 — Customer inputs pre-staged:** First qualified customer's data, branding, user list, and approvers ready, subject to signature — **12/17/2026 at the latest**
- **Milestone 7 — First net-new customer online:** Signed customer live in a bounded rapid-deployment pilot within seven calendar days — **12/31/2026**
- **Final Review:** KR scorecard, demand funnel, customer feedback, operational effort, risks, and scale/no-scale recommendation — **01/08/2027**

## 📐 Measurement and Validation Approach

- Define the start and stop timestamps for each lead-time metric before the first timed run.
- **Demo clock:** starts when the complete demo intake package is accepted and stops when the environment passes readiness checks.
- **Commercial sign-to-online clock:** starts at pilot signature and stops at customer-accessible launch approval; data/assets/users should be pre-staged to prevent intake from consuming the seven-day limit.
- Also record complete-input-to-online time to isolate customer-input delay from Stellarus execution time without weakening the commercial commitment.
- Store demo, ingestion, QA, access, tenant, and acceptance evidence under a unique customer/demo identifier without PHI or credentials.
- Review KRs weekly using counts, percentages, median, 90th percentile, and maximum lead time once sufficient observations exist.
- Revalidate the objective if the live pilot requires PHI, external authentication, a customer application integration, a non-GA feature, or a customer-specific code fork.

## 🧾 Assumptions and Decision Record

| Decision / Assumption                                          | Rationale                                                                                                          | Validation or Revisit Trigger                                                          |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| Use separate sales-demo and live-pilot paths                   | Preserves sales storytelling flexibility while keeping the customer pilot restricted to supported product behavior | Revisit if Sales cannot clearly distinguish preview and GA surfaces                    |
| Limit customer data to minimum non-PHI plan data               | Reduces security review and integration time while supporting relevant benefit demonstrations                      | Revalidate against the approved AtlasIQ data contract and customer data classification |
| Use manual, secure data delivery and managed ingestion         | Fastest credible path for the first demonstrations and pilot                                                       | Revisit after five setups or when manual effort/defects breach the agreed threshold    |
| Use product-managed user/password or magic-link access         | Avoids an external IdP dependency for the limited pilot                                                            | Security approval required before customer access; revisit for production expansion    |
| Keep external integrations out of scope                        | Protects the seven-day deployment ceiling                                                                          | Any requested integration requires a separate plan and revised timing                  |
| Baseline demand funnel and operational effort during execution | Current qualified-pipeline and setup-effort baselines were not supplied                                            | Product/Sales scorecard must establish baselines by 09/08                              |
| Treat`AtlasIQ` as the canonical product/service spelling     | The request used both`AtlasIQ` and `AtlastIQ`; this document normalizes the name for consistency               | Correct globally if the product owner confirms another canonical name                  |

---

Strategic-Objective-Narrative: `v2.0`
Strategic Objective Skill: `v2.1`
