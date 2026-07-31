# Project Name: CSR Chat - Multi-Customer Foundation

**PDLC Phase:** Definition
**Authored Date:** 2026-06-29
**Status:** DRAFT
**Target Window:** 8 weeks

## Problem Statement

CSR Chat is moving from an initial customer-specific point solution into a product that must be sold and deployed across multiple health plan customers. Today, customer onboarding, customer-specific response logic, authentication, brand customization, and EOC plan-data setup are still too dependent on first-customer assumptions and manual implementation knowledge.

New customers need CSR Chat to work with their identity provider, agent roles, plan terminology, EOC source structure, compliance scripts, benefit interpretation rules, and brand expectations without creating a custom fork for each deployment. Stellarus teams need a repeatable implementation path that preserves Compass platform tenant isolation while allowing controlled customer-specific configuration.

**Impact:** Without this PRD, every new CSR Chat customer risks becoming a bespoke implementation, slowing sales-to-launch cycles, increasing onboarding cost, creating cross-tenant/security risk, and weakening answer accuracy for customer-specific EOC plan rules.

## Proposed Solution

Create the CSR Chat multi-customer foundation: a repeatable customer onboarding and configuration layer that sits on top of Compass platform tenant primitives and makes customer-specific CSR Chat behavior explicit, versioned, testable, and supportable.

The release will define and validate a multi-customer launch package covering tenant onboarding, customer-specific prompt and script logic, CSR authentication and role mapping, white-label UI configuration, and EOC plan-data onboarding requirements. The goal is not to build a universal low-code platform; it is to make the next customer implementation repeatable without hardcoded customer assumptions.

## Target Users

**Primary Users:**

* **Customer implementation lead:** Needs a clear onboarding path for identity, plan data, brand configuration, and launch readiness.
* **Customer service representative:** Needs accurate, compliant, customer-specific answers inside a branded CSR Chat experience.
* **Stellarus implementation engineer:** Needs reusable configuration contracts instead of custom code paths for each customer.
* **Stellarus product and customer success owner:** Needs measurable launch readiness and repeatable deployment evidence for sales and expansion.

**Secondary Users:**

* **Customer compliance or benefits SME:** Reviews and approves EOC interpretation, disclosure language, and prompt/script behavior.
* **Customer IT/security owner:** Validates SSO, tenant isolation, access control, logging, and data handling.
* **Stellarus support engineer:** Needs tenant-specific configuration, correlation IDs, and known limitations to triage customer issues.

## Success Metrics

* **Repeatable onboarding readiness:** Baseline is first-customer/manual onboarding; target is two customer onboarding packages completed through the same checklist and configuration artifacts within 5 business days after source data and SSO inputs are available. Measurement source is onboarding dry-run records and implementation issue log.
* **Tenant and access isolation:** Baseline is customer-specific behavior not fully standardized for CSR Chat multi-customer launch; target is 100% of defined auth, role, and tenant-mismatch negative tests passing with zero cross-tenant data access incidents in release-candidate validation. Measurement source is security test evidence and tenant trace review.
* **Customer-specific answer readiness:** Baseline is customer-specific EOC logic/prompt behavior embedded in implementation knowledge; target is at least 95% pass rate on each pilot customer's approved EOC benefit QA sample set, with prompt/script logic versioned and tied to source EOC plan data. Measurement source is SME review rubric, QA sample results, and configuration version log.

## Scope

* **Customer onboarding checklist and intake package:** Define the required inputs for a new CSR Chat customer, including customer slug, environments, contacts, SSO/IdP details, agent roles, branding assets, EOC data sources, plan types, compliance reviewers, launch gates, and support handoff.
* **Tenant configuration model for CSR Chat:** Define a versioned customer configuration record that maps customer slug to auth settings, UI branding, enabled features, EOC plan-data bindings, prompt/script profile, terminology dictionary, and support contacts.
* **Customer-specific prompt and script profile:** Create a controlled configuration surface for customer-approved benefit interpretation rules, required disclosure language, source-priority rules, fallback wording, and prompt variants without changing shared CSR Chat application code.
* **CSR authentication and role mapping:** Define MVP support for customer CSR, supervisor, customer admin, and Stellarus support roles, including SSO claim mapping, tenant resolution, scope expectations, and fail-closed behavior for missing, expired, malformed, tenant-mismatched, or unauthorized sessions.
* **White-label and customer customization baseline:** Support customer product name, logo, primary/accent colors, default panel title, customer terminology, citation/source labels, and basic feature toggles needed for branded deployment.
* **Multi-customer launch validation pack:** Create pass/fail evidence requirements for onboarding completion, auth and tenant isolation, prompt/script approval, EOC data readiness, white-label preview, QA sample pass rate, telemetry coverage, and support readiness.
* **Operational traceability:** Require customer slug, configuration version, prompt/script profile version, EOC dataset version, role, and correlation ID in support-safe telemetry and audit records without logging PHI or raw credentials.

**Milestone Breakdown:**

* **Week 1:** Confirm customer onboarding intake fields, role model, and Compass tenant/auth alignment for CSR Chat.
* **Weeks 2-3:** Define tenant configuration schema, prompt/script profile shape, and white-label baseline fields.
* **Weeks 4-5:** Define EOC plan-data onboarding profile, customer-specific QA sample workflow, and fallback semantics for missing/stale data.
* **Weeks 6-7:** Validate two pilot customer configuration dry runs, including SSO/role mapping simulation and EOC QA sample review.
* **Week 8:** Complete launch validation pack, support handoff checklist, and review-ready customer implementation guide.

## Out-of-Scope

* **Universal low-code workflow builder:** This PRD defines controlled customer configuration for CSR Chat, not arbitrary customer workflow automation.
* **Full self-service admin portal:** Admin UI may be designed later; this release can use managed configuration artifacts and implementation-runbook workflows.
* **New AI agent runtime or full Compass broker implementation:** CSR Chat should align to Compass platform primitives, but this PRD does not rebuild broker, SDK, tenant/auth, or telemetry infrastructure.
* **Advanced per-customer model fine-tuning:** Customer-specific behavior is managed through approved prompt/script profiles and source bindings, not model training or fine-tuning.
* **Full formulary or non-EOC data expansion for every customer:** This release covers EOC plan-data specifics and bindings; formulary, claims, eligibility, provider network, and other data domains require separate PRDs unless already contracted.
* **External customer-facing analytics portal:** Multi-customer operational telemetry and launch evidence are in scope; customer-facing dashboards and cross-customer BI are separate product surfaces.
* **Dedicated single-tenant infrastructure cells:** This release assumes shared Compass platform tenancy unless a customer contract or security review separately requires physical isolation.

## Dependencies and Risks

**Dependencies:**

* Benefits Service available with new customer EOC plan-data: EOC source access, plan identifier mapping, plan-year metadata,
* Customer SME availability for benefits review
* Compass tenant/auth spine or equivalent customer slug, role, scope, and context-token behavior for CSR Chat.
* Customer identity-provider details and approved CSR role/claim mappings.
* Agreement on which customer-specific prompt/script behaviors are configuration versus implementation changes.
* Telemetry fields that can safely include tenant/config/version metadata without PHI or credential exposure.

**Risks:**

* **Configuration sprawl:** Too many customer-specific options could recreate bespoke implementations. Mitigation: ship a narrow, versioned configuration schema with explicit allowed fields and review gates for new fields.
* **Auth mismatch between customer IdPs:** Different SSO providers and claim formats could delay onboarding. Mitigation: require a standard role/claim mapping worksheet and a dry-run before customer launch commitment.
* **EOC interpretation variance:** Customers may require different benefit interpretation or disclosure rules. Mitigation: require customer-approved prompt/script profiles, QA sample sets, and versioned signoff before launch.
* **Brand customization scope creep:** White-label requests may exceed MVP needs. Mitigation: limit v1 to product name, logo, colors, terminology, and baseline feature toggles.
* **Cross-tenant data exposure:** Incorrect customer slug, plan binding, or auth mapping could expose another customer's data. Mitigation: fail-closed auth, automated negative tests, tenant-scoped plan queries, and launch-blocking security evidence.

## Exit Criteria

* [ ] Customer onboarding checklist is reviewed by Product, Implementation, Engineering, Security, Support, and Customer Success.
* [ ] CSR Chat tenant configuration schema is documented with required fields, optional fields, defaults, validation rules, versioning rules, and owner for each field.
* [ ] Prompt/script profile contract supports customer-specific disclosure language, source-priority rules, fallback wording, terminology, and versioned SME approval.
* [ ] Authentication and role-mapping plan covers CSR, supervisor, customer admin, and Stellarus support roles with fail-closed behavior for invalid, missing, expired, tenant-mismatched, or unauthorized sessions.
* [ ] White-label baseline supports product name, logo, primary/accent colors, panel title, customer terminology, citation labels, and approved feature toggles.
* [ ] EOC plan-data sourced through Benefist Services validated.
* [ ] Two pilot customer onboarding dry runs complete using the same checklist and configuration artifacts, with open gaps logged and owners assigned.
* [ ] Release-candidate validation includes passing tenant-isolation, role-scope, prompt-profile, EOC data, missing-data, stale-data, and white-label preview scenarios.
* [ ] Customer-specific QA sample sets meet the agreed pass threshold or have accepted launch exceptions with owner, mitigation, and target date.
* [ ] Support handoff package includes customer slug, configuration version, prompt/script profile version, EOC dataset version, known limitations, escalation path, and troubleshooting guide.
* [ ] Telemetry and audit records expose support-safe tenant/config/version traceability while excluding PHI, raw EOC text beyond approved references, tokens, and credentials.

---
