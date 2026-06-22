# 🧩 Project Name: Tenant Context and Auth Spine

**PDLC Phase:** Definition
**Authored Date:** 2026-06-22
**Status:** DRAFT
**Target Window:** June 24-July 15, 2026

## 🎯 Problem Statement

The platform cannot safely serve multiple customers unless tenant context, persona, principal, scopes, and correlation identifiers are resolved and enforced consistently across UI/BFF, broker, and data services.

**Impact:** Inconsistent context-token handling creates cross-tenant data risk, support blind spots, and launch-blocking security uncertainty.

## 💡 Proposed Solution

Standardize CCS-issued context-token validation and propagation across the SDK/BFF, broker, and Benefits Service, including customer slug, scopes, persona, principal, and correlation IDs.

The solution should fail closed for missing, malformed, expired, unauthorized, or tenant-mismatched context and should preserve enough non-sensitive trace data for support and security review.

## 👥 Target Users

**Primary Users:**

* **Member end user:** Receives only data and actions allowed for their tenant, identity, persona, and scopes.
* **Platform engineer:** Implements and validates context propagation across service boundaries.

**Secondary Users:**

* **Security/privacy reviewer:** Verifies tenant isolation, scope enforcement, and sensitive-log redaction.
* **Support engineer:** Traces issues across services without exposing protected data.

## ✅ Success Metrics

* **Tenant integrity:** Baseline target is zero tolerated cross-tenant access incidents; target remains zero known cross-tenant data access incidents through MVP launch; measurement source is security review, incident log, and release-candidate negative testing.
* **Context completeness:** Baseline is inconsistent context propagation across MVP components; target is 100% of MVP broker-entry requests carrying customer slug, persona, principal, scopes, and correlation ID; measurement source is broker telemetry sample and release-candidate trace review.
* **Fail-closed behavior:** Baseline is not fully verified across BFF, broker, and Benefits Service; target is 100% of invalid or missing context-token scenarios failing closed with observable error telemetry in release-candidate testing; measurement source is auth failure test evidence and support trace validation.

## 📦 Scope

* Context-token contract fields and validation expectations for SDK/BFF, broker, and Benefits Service.
* Scope enforcement policy for benefits lookup and chat session actions.
* Correlation ID propagation across all MVP service boundaries.
* Sensitive-log redaction checklist for tenant, member, and plan data.
* Security and tenant-isolation verification checklist for release candidate.
* Support trace expectations for rejected requests and authorized successful requests.

**Milestone Breakdown:**

* **June 24-June 28:** Confirm CCS context-token fields, scope model, persona model, and correlation ID requirements.
* **June 29-July 5:** Align BFF, broker, and Benefits Service validation/fail-closed behavior.
* **July 6-July 12:** Complete security/privacy checklist, sensitive-log redaction expectations, and trace review.
* **July 13-July 15:** Validate alpha scenarios for valid context, missing token, malformed token, expired token, scope failure, and tenant mismatch.

**Dependencies and Risks:**

* Depends on CCS availability, context-token schema stability, and agreement on scopes/personas for MVP chat.
* Risk: downstream services interpret tenant or scope differently; mitigation is one shared contract and release-candidate validation across BFF, broker, and Benefits Service.
* Risk: traceability conflicts with sensitive-data minimization; mitigation is explicit redaction checklist and correlation-only support traces.

## 🚫 Out-of-Scope

* Dedicated per-customer platform cells; this PRD covers shared-platform context enforcement only.
* Full enterprise identity federation beyond MVP BSC/customer implementation needs.
* Non-MVP data domains such as claims, eligibility, provider, formulary, or member profile.
* Authorization policy for future CSR or enterprise personas; those should be handled in post-MVP capability onboarding.

## 🏁 Exit Criteria

* [ ] Context-token contract is documented and accepted by Product, Apps, CCS owner, and Security/Privacy stakeholders.
* [ ] BFF, broker, and Benefits Service reject missing, expired, malformed, tenant-mismatched, or unauthorized context tokens.
* [ ] Tenant slug and scopes are enforced for all MVP Benefits Service reads.
* [ ] Correlation IDs are present in logs and telemetry across UI/BFF, broker, Sierra.ai, Benefits Service, and escalation.
* [ ] Sensitive-log redaction expectations are documented and verified in release-candidate evidence.
* [ ] Release candidate includes passing checklist evidence for auth failure, scope failure, tenant mismatch, and support traceability.

