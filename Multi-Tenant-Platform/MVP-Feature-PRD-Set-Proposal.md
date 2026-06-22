# Stellarus Platform MVP Feature PRD Set Proposal

**PDLC Phase:** Definition
**Authored Date:** 2026-06-22
**Status:** DRAFT
**Skill:** feature-prd v1.1
**Output Location:** `Conversational-AI/Multi-Tenant-Platform/`

---

## Purpose

This document proposes the minimum set of Feature PRDs needed to deliver the September 1, 2026 Stellarus multi-tenant platform MVP for BSC member chat.

The proposal decomposes the MVP into delivery-sized PRDs that each fit a 2-8 week feature timebox, have measurable outcomes, and map directly to the initiative and delivery plan.

## Source Alignment

The proposed PRD set is anchored in these MVP requirements:

- BSC member chat must be the first implementation on the reusable Stellarus multi-tenant platform, not a one-off Sierra.ai path.
- The September MVP must prove a customer chat surface can run through a Stellarus-owned SDK/API path, broker API, CCS context token, Benefits Service grounding, Sierra.ai runtime, and basic escalation action.
- The platform must produce launch evidence for security, tenant isolation, reliability, answer quality, support, and rollback.
- The delivery plan targets a July 15 alpha, August 1 escalation contract, August 15 release candidate, and September 1 MVP launch.

## Recommended MVP PRD Set

| PRD | Feature PRD | Primary Outcome | Target Window | Critical Dependency |
| --- | --- | --- | --- | --- |
| PRD-01 | SDK/API Customer Integration Path | Customer or demo UI can initiate and stream chat through a Stellarus-owned integration surface | June 24-August 15 | SDK v1 surface area decision |
| PRD-02 | Tenant Context and Auth Spine | CCS-issued context tokens work consistently across BFF, broker, and Benefits Service | June 24-July 15 | CCS token contract |
| PRD-03 | Broker Conversation Orchestration | Broker is the standard entry point for chat, streaming, Sierra.ai calls, sessions, failure handling, and telemetry | June 24-August 15 | Broker MVP gap assessment |
| PRD-04 | Benefits Grounding for MVP Lines of Business | MVP benefits and coverage questions are grounded in Benefits Service or an approved fallback | June 24-August 15 | Specialty LoB decision |
| PRD-05 | Escalation and CCaaS Handoff Action | Escalation is a tracked platform action with routing metadata, result status, and failure behavior | July 1-August 15 | Genesys/CCaaS mechanics |
| PRD-06 | Launch Telemetry, Quality Gates, and Support Readiness | Product, engineering, and support can monitor, evaluate, triage, and roll back the MVP | July 1-September 1 | Telemetry event taxonomy |

## Why These Six PRDs

These six PRDs are the smallest coherent set because each owns one launch-critical contract:

- PRD-01 owns the customer-facing entry contract.
- PRD-02 owns tenant safety and identity propagation.
- PRD-03 owns runtime orchestration.
- PRD-04 owns grounded answers.
- PRD-05 owns human handoff.
- PRD-06 owns production readiness and launch evidence.

Items intentionally excluded from the MVP PRD set include full Stellarus-owned agent replacement, universal low-code workflow building, full white-label Stellarus UI, claims/eligibility/member-profile production data services, and dedicated per-customer platform cells.

---

# PRD-01: SDK/API Customer Integration Path

**PDLC Phase:** Definition
**Status:** DRAFT
**Recommended File:** `Feature-PRD-01-SDK-API-Customer-Integration.md`
**Target Window:** June 24-August 15, 2026

## Problem Statement

BSC member chat cannot become a reusable platform implementation if customer UI integration depends on one-off Sierra.ai or demo-only wiring. External and internal implementers need a stable Stellarus-owned SDK/API path that supports chat initiation, streaming, session metadata, errors, escalation events, and customer configuration.

**Impact:** Without this PRD, the July Sierra release risks becoming throwaway integration work and the September MVP risks failing the customer integration launch gate.

## Proposed Solution

Publish a versioned SDK/API integration path that customer-controlled UI or Stellarus demo UI can use to start chat sessions, stream broker responses, pass session metadata, handle standard errors, emit analytics hooks, and capture escalation actions.

## Target Users

**Primary Users:**

- **Customer implementation engineer:** Integrates BSC-owned or customer-controlled UI with Stellarus platform chat.
- **Stellarus Apps engineer:** Maintains SDK/API compatibility, samples, and integration support.

**Secondary Users:**

- **Product owner:** Uses SDK readiness as a launch gate.
- **Support engineer:** Uses documented configuration and errors to triage integration issues.

## Success Metrics

- SDK/API v1 enables chat initiation and streaming in the July 15 alpha with one sample implementation.
- SDK/API v2 includes escalation event capture by August 1.
- An engineer outside the core Apps team can complete the sample integration using published docs without undocumented environment assumptions by August 15.

## Scope

- SDK/API contract for chat start, streaming, session metadata, plan context policy, error handling, and versioning.
- Customer configuration model for environment, customer slug, scopes, endpoints, and correlation identifiers.
- Sample implementation for customer UI or agreed integration shell.
- SDK documentation covering install/use, environment variables, known limitations, and migration notes.
- Analytics hook points for chat start, stream lifecycle, error, and escalation events.

## Out-of-Scope

- Full white-labeled production Stellarus UI.
- Universal widget builder or arbitrary customer workflow automation.
- Non-chat conversational surfaces.
- Backward compatibility beyond v1/v2 MVP contracts.

## Definition of Done

- [ ] SDK/API v1 contract is reviewed by Product and Apps and supports chat initiation and streaming.
- [ ] SDK/API v2 contract supports escalation event capture and handoff status.
- [ ] Sample integration runs against target MVP environments without hardcoded customer, port, or local assumptions.
- [ ] Integration docs include configuration, error handling, versioning, and known limitations.
- [ ] SDK/API events include correlation IDs that can be traced through BFF, broker, Benefits Service, Sierra.ai, and escalation.

---

# PRD-02: Tenant Context and Auth Spine

**PDLC Phase:** Definition
**Status:** DRAFT
**Recommended File:** `Feature-PRD-02-Tenant-Context-Auth-Spine.md`
**Target Window:** June 24-July 15, 2026

## Problem Statement

The platform cannot safely serve multiple customers unless tenant context, persona, principal, scopes, and correlation identifiers are resolved and enforced consistently across UI/BFF, broker, and data services.

**Impact:** Inconsistent context-token handling creates cross-tenant data risk, support blind spots, and launch-blocking security uncertainty.

## Proposed Solution

Standardize CCS-issued context-token validation and propagation across the SDK/BFF, broker, and Benefits Service, including customer slug, scopes, persona, principal, and correlation IDs.

## Target Users

**Primary Users:**

- **Member end user:** Receives only data and actions allowed for their tenant and context.
- **Platform engineer:** Implements and validates context propagation across services.

**Secondary Users:**

- **Security/privacy reviewer:** Verifies tenant isolation and sensitive-log redaction.
- **Support engineer:** Traces issues without exposing protected data.

## Success Metrics

- Zero known cross-tenant data access incidents through MVP launch.
- 100% of MVP requests include customer slug, persona, principal, scopes, and correlation ID at broker entry.
- 100% of invalid or missing context-token scenarios fail closed with observable error telemetry in release-candidate testing.

## Scope

- Context-token contract fields and validation expectations for SDK/BFF, broker, and Benefits Service.
- Scope enforcement policy for benefits lookup and chat session actions.
- Correlation ID propagation across all MVP service boundaries.
- Sensitive-log redaction checklist for tenant, member, and plan data.
- Security and tenant-isolation verification checklist for release candidate.

## Out-of-Scope

- Dedicated per-customer platform cells.
- Full enterprise identity federation beyond MVP BSC/customer implementation needs.
- Non-MVP data domains such as claims, eligibility, provider, formulary, or member profile.

## Definition of Done

- [ ] Context-token contract is documented and accepted by Product, Apps, and Security/Privacy stakeholders.
- [ ] BFF, broker, and Benefits Service reject missing, expired, malformed, or unauthorized context tokens.
- [ ] Tenant slug and scopes are enforced for all MVP Benefits Service reads.
- [ ] Correlation IDs are present in logs and telemetry across UI/BFF, broker, Sierra.ai, Benefits Service, and escalation.
- [ ] Release candidate includes passing tests or checklist evidence for auth failure, scope failure, tenant mismatch, and sensitive-log redaction.

---

# PRD-03: Broker Conversation Orchestration

**PDLC Phase:** Definition
**Status:** DRAFT
**Recommended File:** `Feature-PRD-03-Broker-Conversation-Orchestration.md`
**Target Window:** June 24-August 15, 2026

## Problem Statement

If chat surfaces call Sierra.ai, data services, or escalation paths directly, Stellarus loses the reusable platform entry point needed for tenant-safe routing, telemetry, failure handling, and future agent transition.

**Impact:** Direct or parallel runtime logic makes the September MVP hard to support and slows later migration to Member Agent, CSR Agent, and additional customer surfaces.

## Proposed Solution

Make the broker API the standard conversation entry point for MVP chat, owning request validation, session handling, SSE streaming, Sierra.ai integration, data enrichment, rate limits, circuit breakers, token accounting, and telemetry.

## Target Users

**Primary Users:**

- **Member end user:** Gets a streamed, grounded answer through a stable chat session.
- **Stellarus Apps engineer:** Owns the broker runtime contract and service behavior.

**Secondary Users:**

- **Data service owner:** Receives standardized tenant-aware data access calls from the broker.
- **AI/runtime owner:** Uses broker contracts to transition from Sierra.ai toward Stellarus-owned agents over time.

## Success Metrics

- July 15 alpha supports streamed responses through SDK/BFF to broker to Sierra.ai.
- August 15 release candidate passes happy-path, data-missing, auth-failure, Sierra-failure, Benefits-failure, and stream-disconnect scenarios.
- 100% of broker requests emit route, latency, token usage, data-service call, runtime call, and error telemetry.

## Scope

- Chat session creation and lifecycle handling.
- SSE streaming response contract.
- Sierra.ai runtime adapter for MVP.
- Benefits Service enrichment call pattern.
- Rate limiting, circuit breaker, and failure response behavior.
- Token accounting and broker-level telemetry.
- MVP capability route definition for BSC member benefits chat.

## Out-of-Scope

- Full replacement of Sierra.ai with Stellarus-owned Member Agent.
- Multi-agent orchestration beyond the MVP Sierra-backed route.
- Arbitrary external integration execution outside approved escalation flow.
- Long-term capability registry implementation, except for MVP route metadata.

## Definition of Done

- [ ] Broker exposes stable MVP conversation API accepted by SDK/BFF consumers.
- [ ] Broker streams Sierra-backed responses through the Stellarus path.
- [ ] Broker enriches supported requests with tenant-scoped Benefits Service data.
- [ ] Broker failure behavior is documented for auth, data service, Sierra.ai, rate limit, circuit breaker, and stream disconnect cases.
- [ ] Broker telemetry enables one request to be traced across UI/BFF, broker, Sierra.ai, Benefits Service, and escalation.

---

# PRD-04: Benefits Grounding for MVP Lines of Business

**PDLC Phase:** Definition
**Status:** DRAFT
**Recommended File:** `Feature-PRD-04-Benefits-Grounding-MVP-Lines-of-Business.md`
**Target Window:** June 24-August 15, 2026

## Problem Statement

MVP chat quality depends on plan and coverage answers being grounded in tenant-safe Benefits Service data. Specialty LoB gaps or temporary Sierra-direct fetch behavior can create incomplete answers, unclear source of truth, and operational risk.

**Impact:** Incomplete benefits data is the highest data risk for September because it directly affects answer completeness and launch confidence.

## Proposed Solution

Make Benefits Service the governed MVP source of truth for plan and coverage data, close all MVP-required LoB gaps or document an accepted fallback, and define deprecation criteria for any temporary non-platform fetch path.

## Target Users

**Primary Users:**

- **BSC member:** Receives benefits and coverage answers based on available plan data.
- **Data/App engineer:** Provides and validates tenant-scoped benefits data for chat grounding.

**Secondary Users:**

- **Product owner:** Decides whether data gaps are launch blockers or accepted deferrals.
- **Quality reviewer:** Evaluates grounded answer correctness and unsupported-answer fallback behavior.

## Success Metrics

- All MVP-required Benefits data is available through Benefits Service or covered by an accepted fallback with owner and removal date by August 15.
- Representative benefits/coverage sample set meets the agreed grounded-answer accuracy threshold before launch.
- Unsupported or missing-data scenarios fall back cleanly in release-candidate testing.

## Scope

- MVP-required plan and coverage data inventory by LoB.
- Specialty LoB source, format, ingestion owner, validation owner, fallback, and fallback removal condition.
- Tenant-scoped Benefits Service read behavior for broker enrichment.
- Data freshness, source-of-truth, and audit logging expectations.
- Human review sample set for representative benefits and coverage questions.

## Out-of-Scope

- Complete claims, eligibility, member profile, provider, formulary, or data lake migration.
- Production data services beyond Benefits Service.
- Full data lineage platform.
- Removing every temporary Sierra-direct path before MVP if an explicit fallback/deprecation decision is accepted.

## Definition of Done

- [ ] MVP-required LoB coverage matrix is documented with available data, gaps, owner, and resolution path.
- [ ] Benefits Service serves required plan and coverage data to broker through tenant-scoped reads.
- [ ] Any temporary fallback has named owner, accepted risk, removal condition, and target date.
- [ ] Release candidate includes passing tests or checklist evidence for data available, data missing, tenant mismatch, and stale/fallback scenarios.
- [ ] Quality review sample set and acceptance threshold are approved before go/no-go.

---

# PRD-05: Escalation and CCaaS Handoff Action

**PDLC Phase:** Definition
**Status:** DRAFT
**Recommended File:** `Feature-PRD-05-Escalation-CCaaS-Handoff-Action.md`
**Target Window:** July 1-August 15, 2026

## Problem Statement

Escalation cannot be a customer-specific UI button if the platform is expected to support reusable chat surfaces. The MVP needs a tracked escalation action with routing metadata, conversation context, auditability, and measurable handoff state.

**Impact:** Unresolved Genesys/CCaaS mechanics are the highest integration risk for release candidate readiness.

## Proposed Solution

Define and implement a minimal platform escalation action that captures reason, routing payload, conversation summary, allowed context policy, start event, handoff result, and failure behavior for Genesys or an approved CCaaS path.

## Target Users

**Primary Users:**

- **BSC member:** Can request or receive a human handoff when chat cannot resolve their need.
- **Customer service representative:** Receives enough context to continue the conversation when handoff succeeds.

**Secondary Users:**

- **Customer integration engineer:** Wires customer UI/CCaaS behavior through the SDK/API contract.
- **Support/operations owner:** Monitors failed handoffs and escalation reasons.

## Success Metrics

- SDK/API v2 includes escalation event capture by August 1.
- August 15 release candidate has a tracked start event, handoff result, and observable failure behavior.
- 100% of escalation events include correlation ID, reason, routing metadata, result status, and timestamp.

## Scope

- Escalation action event name and payload schema.
- Routing metadata required for Genesys or approved CCaaS path.
- Conversation summary and allowed plan/member context policy.
- Handoff result states and retry/failure behavior.
- Audit fields and telemetry for escalation start, success, failure, cancellation, and unavailable states.
- Minimal customer UI or integration-shell behavior for invoking escalation.

## Out-of-Scope

- Full CCaaS abstraction layer for every future customer system.
- Complex agent availability optimization or workforce routing.
- CSR desktop experience redesign.
- Post-handoff conversational continuity beyond MVP-required context transfer.

## Definition of Done

- [ ] BSC/PTP/Genesys decision questions are resolved or converted into accepted launch exceptions.
- [ ] SDK/API v2 contract documents escalation payload, result states, and failure behavior.
- [ ] MVP path supports a basic handoff action with tracked start event and result status.
- [ ] Escalation telemetry is visible in MVP dashboards and traceable by correlation ID.
- [ ] Release candidate passes escalation happy path, unavailable path, and failure path validation.

---

# PRD-06: Launch Telemetry, Quality Gates, and Support Readiness

**PDLC Phase:** Definition
**Status:** DRAFT
**Recommended File:** `Feature-PRD-06-Launch-Telemetry-Quality-Support-Readiness.md`
**Target Window:** July 1-September 1, 2026

## Problem Statement

The MVP cannot be safely launched or stabilized if telemetry, answer-quality review, incident response, support triage, and rollback are deferred until after feature completion.

**Impact:** Without launch evidence, the platform may appear functionally complete but fail operational readiness, quality, privacy, or support gates.

## Proposed Solution

Establish MVP dashboards, quality review workflow, launch gates, runbooks, incident path, support triage guide, rollback plan, and daily launch monitoring for the first two weeks after September 1.

## Target Users

**Primary Users:**

- **Product owner:** Makes go/no-go decisions with objective launch evidence.
- **Support engineer:** Traces and triages member issues across the full path.
- **Operations/engineering owner:** Monitors health, reliability, cost, and failure patterns.

**Secondary Users:**

- **Security/privacy reviewer:** Confirms launch evidence for tenant isolation, auth, and sensitive logs.
- **Customer stakeholder:** Receives clear known issues and launch readiness status.

## Success Metrics

- MVP dashboards cover volume, latency, error rate, escalation rate, broker failures, Sierra.ai failures, data service failures, token usage, and answer-quality review before launch.
- Launch readiness pack is complete by August 15 release candidate.
- For the first two launch weeks, daily monitoring reports uptime, latency, failure rates, quality review, escalations, and data issues.

## Scope

- MVP metric taxonomy and dashboard views.
- Launch gates for functional, tenant/auth, data, operations, quality, and integration readiness.
- Human review rubric and sample set for grounded answer quality, unsupported-answer fallback, escalation appropriateness, and source-data gaps.
- Runbook, incident path, support triage guide, rollback plan, known issues, and customer communication notes.
- Go/no-go checklist and launch exception process.
- September stabilization cadence and post-launch retrospective inputs.

## Out-of-Scope

- Enterprise-wide observability platform replacement.
- Automated evaluation harness beyond MVP manual/human review requirements.
- Q4 capability registry and onboarding operating model.
- Full cost optimization program beyond MVP token/Sierra usage baselines.

## Definition of Done

- [ ] MVP dashboards are available to product, engineering, and support owners.
- [ ] Release candidate has completed launch gate evidence or explicit accepted exceptions.
- [ ] Runbook, incident path, support triage guide, rollback plan, known issues, and customer communication notes are approved.
- [ ] Quality review sample set, rubric, and pass threshold are approved before launch.
- [ ] Post-launch monitoring cadence and retrospective template are ready before September 1.

---

## Sequencing Recommendation

1. Start PRD-02 immediately because every other PRD depends on tenant-safe context propagation.
2. Start PRD-01 and PRD-03 in parallel once SDK v1 and broker contract decisions are stable enough for implementation.
3. Start PRD-04 immediately with a June decision deadline for specialty LoB, because data readiness has the highest answer-quality risk.
4. Start PRD-05 after escalation mechanics discovery begins, with SDK/API v2 contract complete by August 1.
5. Start PRD-06 no later than July 1 so telemetry and support readiness are part of the alpha-to-RC path rather than a launch-week scramble.

## MVP Acceptance Across the PRD Set

The MVP is ready when:

- A BSC member chat can start from customer UI or demo UI through the Stellarus SDK/API path.
- Broker is the only standard conversation entry point for MVP chat.
- CCS context-token validation is enforced across BFF, broker, and Benefits Service.
- Benefits Service provides MVP-required plan and coverage grounding, or an accepted fallback exists with owner and removal date.
- Sierra.ai-backed responses stream through the Stellarus path with platform-owned telemetry and failure behavior.
- Escalation is a tracked platform action with routing metadata, result status, and observable failure behavior.
- Product, engineering, support, and security/privacy stakeholders have launch evidence for functional readiness, tenant isolation, data readiness, operations, quality, and integration.

## Recommended Next Step

Approve this PRD set, then convert each proposed PRD into its own Feature PRD file using the `Feature-1-Pager-PRD.md` structure.

