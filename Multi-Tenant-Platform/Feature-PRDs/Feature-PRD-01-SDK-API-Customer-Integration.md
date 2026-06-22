# 🧩 Project Name: SDK/API Customer Integration Path

**PDLC Phase:** Definition
**Authored Date:** 2026-06-22
**Status:** DRAFT
**Target Window:** June 24-August 15, 2026

## 🎯 Problem Statement

BSC member chat cannot become a reusable platform implementation if customer UI integration depends on one-off Sierra.ai or demo-only wiring. External and internal implementers need a stable Stellarus-owned SDK/API path that supports chat initiation, streaming, session metadata, errors, escalation events, analytics hooks, and customer configuration.

**Impact:** Without this PRD, the July Sierra release risks becoming throwaway integration work and the September MVP risks failing the customer integration launch gate.

## 💡 Proposed Solution

Publish a versioned SDK/API integration path that customer-controlled UI or Stellarus demo UI can use to start chat sessions, stream broker responses, pass session metadata, handle standard errors, emit analytics hooks, and capture escalation actions.

The SDK/API path should make customer integration repeatable by documenting required configuration, versioning rules, sample implementation behavior, supported events, and failure semantics.

## 👥 Target Users

**Primary Users:**

* **Customer implementation engineer:** Integrates BSC-owned or customer-controlled UI with Stellarus platform chat.
* **Stellarus Apps engineer:** Maintains SDK/API compatibility, samples, configuration patterns, and integration support.

**Secondary Users:**

* **Product owner:** Uses SDK readiness as a launch gate and customer-integration acceptance signal.
* **Support engineer:** Uses documented configuration, correlation IDs, and errors to triage integration issues.

## ✅ Success Metrics

* **Chat initiation and streaming readiness:** Baseline is no Stellarus-owned customer SDK/API path for the September platform MVP; target is SDK/API v1 supporting chat initiation and streaming in the July 15 alpha with one working sample implementation; measurement source is alpha demo validation and SDK sample execution record.
* **Escalation event readiness:** Baseline is no SDK-level escalation event contract; target is SDK/API v2 supporting escalation event capture by August 1; measurement source is reviewed SDK/API contract and escalation event test evidence.
* **External engineer usability:** Baseline is integration support dependent on core Apps team context; target is one engineer outside the core Apps team completing the sample integration by August 15 without undocumented environment assumptions; measurement source is integration dry-run notes and issue log.

## 📦 Scope

* SDK/API contract for chat start, streaming, session metadata, plan context policy, error handling, and versioning.
* Customer configuration model for environment, customer slug, scopes, endpoints, and correlation identifiers.
* Sample implementation for customer UI or agreed integration shell.
* SDK documentation covering install/use, environment variables, known limitations, migration notes, and troubleshooting.
* Analytics hook points for chat start, stream lifecycle, error, and escalation events.
* Trace propagation requirements so SDK/API events can be correlated through BFF, broker, Benefits Service, Sierra.ai, and escalation.

**Milestone Breakdown:**

* **June 24-June 30:** Lock SDK/API v1 surface area, configuration fields, versioning approach, and sample integration target.
* **July 1-July 15:** Deliver SDK/API v1 alpha for chat initiation, streaming, session metadata, errors, and correlation identifiers.
* **July 16-August 1:** Add SDK/API v2 escalation event capture and analytics hook coverage.
* **August 2-August 15:** Complete docs, sample integration dry run, known limitations, and release-candidate readiness evidence.

**Dependencies and Risks:**

* Depends on stable broker API, CCS context-token requirements, and customer environment configuration.
* Risk: SDK docs lag implementation and become the integration bottleneck; mitigation is treating docs and sample integration as exit criteria, not post-build cleanup.
* Risk: Customer-specific assumptions leak into SDK behavior; mitigation is release-candidate validation against target environments with no hardcoded customer, port, or local assumptions.

## 🚫 Out-of-Scope

* Full white-labeled production Stellarus UI; this release supports customer UI or demo/integration shell only.
* Universal widget builder or arbitrary customer workflow automation; this PRD is limited to MVP chat integration.
* Non-chat conversational surfaces; future surfaces should enter through post-MVP platform onboarding.
* Backward compatibility beyond v1/v2 MVP contracts; long-term lifecycle policy belongs to the post-MVP SDK versioning PRD.

## 🏁 Exit Criteria

* [ ] SDK/API v1 contract is reviewed by Product and Apps and supports chat initiation and streaming.
* [ ] SDK/API v2 contract supports escalation event capture and handoff status.
* [ ] Sample integration runs against target MVP environments without hardcoded customer, port, or local assumptions.
* [ ] Integration docs include configuration, error handling, versioning, known limitations, and troubleshooting.
* [ ] Analytics hooks and correlation IDs are emitted for chat start, stream lifecycle, error, and escalation events.
* [ ] A non-core Apps engineer completes the sample integration dry run and documents any remaining blockers.
* [ ] Product, Apps, and Support accept the SDK/API path as ready for August 15 release-candidate validation.

