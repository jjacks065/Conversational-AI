# Stellarus Conversational AI Platform Initiative

**PDLC Phase:** Definition
**Status:** Draft
**Authored Date:** 06/18/2026
**Planning Horizon:** Now through 12/31/2026

---

## Executive Summary

Stellarus should treat Blue Shield of California (BSC) member chat as the first customer implementation on the reusable, multi-tenant conversational AI platform, not as a one-off Sierra.ai integration. The September 1, 2026 Minimum Viable Product (MVP) should prove that an external customer can run a member chat surface through a Stellarus-owned Software Development Kit (SDK) and agent-broker, with customer context resolved through Customer Confic Service (CCS), plan and coverage data served through Benefits Service, and Sierra.ai used as the initial AI runtime while Stellarus-owned Member and Customer Service Representative (CSR) agents mature.

The remainder of 2026 should convert that first-customer MVP into a broader platform foundation: capability routing, tenant-safe data access, new data services, additional conversational surfaces, external Contact Center as a Service (CCaaS) escalation patterns, telemetry, cost and quality gates, and onboarding contracts. The platform outcome is a governed path to launch member, CSR, customer-embedded, and future enterprise chat surfaces without rebuilding auth, orchestration, data enrichment, auditability, and SDK integration for each customer.

## Strategic Context and Vision

**Company alignment:** Supports the Compass conversational AI roadmap by turning member chat, CSR assist, Benefits Service, agent-broker, SDK, and agent work into one reusable platform foundation.

**Problem statement:** Current work contains a near-term BSC/Genesis/Sierra.ai path, a nascent Stellarus platform architecture, and several built services, but the roadmap still has product gaps around SDK ownership, escalation semantics, data completeness, telemetry, production readiness, and agent transition. Without a single objective, the July Sierra.ai release could become throwaway work and the September platform MVP could ship as another narrow integration.

**Vision:** By September 1, 2026, Stellarus can ship BSC member chat as the first customer surface on the multi-tenant platform. By December 31, 2026, Stellarus has the foundation for repeatable conversational AI expansion: tenant context, SDK distribution, agent-broker orchestration, additional data services, data service adapters, member/CSR/customer-embedded surfaces, escalation integration, telemetry, evaluation, and reusable agent capability contracts.

## Objective

**Deliver BSC member chat as the first customer implementation on the Stellarus multi-tenant conversational AI platform and SDK by September 2026, then harden the foundation through December 2026 by adding new tenant-aware data services and support for additional member, CSR, and customer-embedded conversational surfaces through reusable SDK, broker, agent, telemetry, and governance contracts.**

## Key Results

**KR1: September MVP delivery**

- Ship a September 1 MVP that uses a Stellarus-owned Chat User Interfasce (UI) SDK or Aplication Programming Interface (API) SDK path, an agent-broker API, Benefits Service plan and coverage data, Sierra.ai as the initial agent runtime, and a basic escalation action.
- Complete a July 15 alpha and August 15 release candidate with working demo UI, SDK API, agent-broker streaming, tenant context, plan lookup, and representative BSC member chat flows.
- Complete BSC integration readiness by August 31 with documented environment config, SDK integration guide, sample implementation, and go/no-go checklist.

**KR2: Tenant-safe platform foundation**

- Maintain zero known cross-tenant data access incidents.
- Standardize CCS context-token handling across Backend For Frontend (BFF), agent-broker, and data services, including customer slug, scopes, persona, principal, and correlation identifiers.
- Define the platform contract for tenant-aware data service access, including source of truth, freshness, authorization scopes, audit logging, and failure behavior.

**KR3: Data service readiness**

- Complete Benefits Service all-lines-of-business data required for the MVP, including specialty LoB data ingestion or an accepted fallback with owner signoff.
- Preserve Benefits Service as the plan data source of truth for platform flows while documenting any temporary Sierra-direct fetch path and its deprecation criteria.
- Define the next data service contracts for member profile, eligibility, and claims history by Q4 2026.

**KR4: Agent-Broker, SDK, and escalation maturity**

- Make the agent-broker the standard conversation entry point for chat surfaces, including streaming, session handling, Sierra.ai integration, rate limiting, circuit breaker behavior, data enrichment, and telemetry.
- Publish SDK v1 by July 15 for chat initiation and streaming, then SDK v2 by August 1 for escalation event capture and CCaaS handoff.
- Resolve Genesys escalation routing and model it as a tracked SDK action before the September release candidate.

**KR5: Operational readiness and learning loop**

- Establish MVP dashboards for volume, latency, error rate, escalation rate, agent-broker failures, Sierra.ai failures, data service failures, token usage, and answer-quality review.
- Define launch gates for quality, security, privacy, support handoff, incident response, and rollback.
- By December 31, 2026, publish platform onboarding and capability registry docs so new customer/chat capabilities can enter through a governed intake path.

## Strategic Levers

**Lever 1: Own the platform entry point.** The Stellarus agent-broker and SDK must become the durable integration layer even while Sierra.ai remains the initial AI runtime. This keeps the July work reusable for September and beyond.

**Lever 2: Treat tenant context as the platform spine.** CCS-issued context tokens, scopes, customer slug, persona, and correlation identifiers should be the common control plane for UI, agent-broker, Benefits Service, and future data services.

**Lever 3: Make Benefits Service the first governed data plane.** Plan reads, coverage checks, request logs, and customer-schema isolation should become the reference pattern for future data services.

**Lever 4: Turn escalation into a platform action.** Genesys or other CCaaS handoff should not be just a UI button. It should be an SDK event with routing metadata, conversation context, audit trail, and measurable completion state.

**Lever 5: Build for agent transition.** Sierra.ai should remain in scope for near-term release, but prompts, guardrails, data contracts, and telemetry should be shaped so Stellarus-owned Member and CSR agents can assume more responsibility later in 2026.

## Themes and High-Level Requirements

### Theme A: Customer Integration and SDK

- Provide a Stellarus-owned SDK/API path that supports custom customer UI and Stellarus UI integrations.
- Publish integration docs, sample code, configuration requirements, versioning policy, and migration notes.
- Support chat streaming, session metadata, plan context, escalation events, and analytics hooks.

### Theme B: Agent-Broker and Conversation Orchestration

- Agent-broker must own request validation, auth context, session state, token accounting, rate limits, Sierra.ai interaction, Server-Sent Event (SSE) streaming, and data enrichment.
- Agent-broker must support capability routing so Sierra.ai, Member Agent, CSR Agent, and future agents can be selected by product and use case.
- Agent-broker must emit consistent telemetry for routing, data access, agent runtime, errors, and escalations.

### Theme C: Data Services and Grounding

- Benefits Service remains the first production data service, with customer-specific schema isolation and verified context-token routing.
- MVP data readiness must close specialty LoB gaps or document a temporary fallback with a removal date.
- Q4 should define member, eligibility, claims, and additional data service adapter contracts.

### Theme D: Escalation and CCaaS Integration

- Define the minimum September escalation flow: always-available handoff action, routing metadata, conversation summary, reason, and result status.
- Resolve Genesys API/SDK mechanics and ownership before the release candidate.
- Generalize CCaaS handoff so future customer systems can integrate without hardcoding Genesys assumptions into the agent-broker.

### Theme E: Governance, Quality, and Operations

- Require launch evidence for tenant isolation, auth, data access, telemetry, support runbooks, rollback, and failure behavior.
- Define quality review for grounded answer correctness, unsupported answer fallback, escalation appropriateness, and source-data gaps.
- Establish owner-visible dashboards and a weekly launch-readiness review cadence through September.

## Constraints, Risks, and Dependencies

**Dependencies**

- BSC and PTP alignment on Genesys escalation routing, SOW scope, and customer integration timing.
- Data/App alignment on specialty LoB source data shape, ownership, ingestion path, and validation.
- CCS availability and context-token contracts for BFF, agentic-broker, and Benefits Service flows.
- Sierra.ai stability and clear boundary for what logic is temporary versus platform reusable.
- App team capacity across agentic-broker, SDK, Benefits Service, chat UI, and production readiness.

**Risks**

- Specialty LoB remains incomplete and causes MVP answer gaps.
- Genesys escalation scope remains unknown too late for SDK v2.
- July Sierra.ai release creates parallel logic that is not reusable for September.
- SDK documentation and distribution lag behind technical implementation.
- Telemetry and support readiness are deferred until after feature completion.

**Mitigations**

- Lock a June go/no-go matrix for data fallback, escalation fallback, and MVP scope.
- Treat all temporary Sierra-direct Benefits fetch behavior as migration debt with a named owner and exit condition.
- Define the SDK v1 and SDK v2 API contracts before implementation completion.
- Run weekly release-readiness reviews from July 1 through September 1.
- Keep December work focused on platform hardening and repeatability, not broad new feature sprawl.

**Out of scope for September MVP**

- Full replacement of Sierra.ai with Stellarus-owned agents.
- Full white-labeled production Stellarus UI beyond demo/test needs.
- Universal low-code builder or arbitrary customer workflow automation.
- Complete claims, eligibility, member profile, provider, formulary, or data lake migration.
- Dedicated per-customer platform cells unless required by a separate risk or contract decision.

## Health Metrics

- **Tenant integrity:** cross-tenant incidents, invalid context-token rejects, scope failures.
- **Reliability:** agent-broker uptime, Benefits Service uptime, Sierra.ai failure rate, circuit breaker opens, SSE disconnects.
- **Performance:** p50/p95 latency, time to first token, data enrichment latency, escalation latency.
- **Quality:** grounded-answer accuracy sample pass rate, unsupported-answer fallback rate, human review defects.
- **Adoption:** sessions, active users, SDK integrations, customer UI starts, repeat usage.
- **Escalation:** escalation starts, successful handoffs, failed handoffs, escalation reasons, avoidable escalation rate.
- **Cost:** token usage per request/session, Sierra.ai usage cost, cost per successful answer.
- **Platform reuse:** number of capabilities using agent-broker/SDK/data-service standards and number of data services under contract.
