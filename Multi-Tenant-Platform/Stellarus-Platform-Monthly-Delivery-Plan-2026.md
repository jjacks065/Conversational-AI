# Stellarus Conversational AI Platform Monthly Delivery Plan

**Status:** Draft
**Authored Date:** 06/18/2026
**Planning Horizon:** 06/18/2026 through 12/31/2026
**Primary MVP Target:** 09/01/2026

---

## Planning Assumptions

- July 1 remains the near-term non-Stellarus BSC/Genesys/Sierra member chat release path.
- September 1 is the Stellarus Platform MVP target, with BSC member chat as the first customer implementation on the multi-tenant platform, not just a re-skin of the July path.
- Sierra.ai remains the initial AI runtime for the MVP, while platform contracts are shaped to support Stellarus Member Agent and CSR Agent expansion.
- Benefits Service is the initial governed data service and should become the source of truth for plan and coverage data exposed to chat; Q4 hardening should add new data services and make them available through the same tenant-aware platform pattern.
- Post-September hardening should expand beyond BSC member chat to support additional conversational surfaces, including CSR assist and customer-embedded experiences.
- Stellarus UI is useful for demos and test harnesses, but the customer-facing MVP depends on SDK/API integration into customer-controlled UI.
- The plan is intentionally month-by-month and milestone-oriented; detailed engineering tickets should derive from this plan after owner and capacity review.

## MVP Definition

The September MVP is successful when BSC can run member chat as the first customer surface on the Stellarus multi-tenant platform with:

- Customer UI or demo UI using a Stellarus SDK/API integration.
- Broker API as the conversation entry point.
- CCS context-token validation across BFF, broker, and Benefits Service.
- Sierra.ai-backed answer generation with platform-owned routing, telemetry, and failure behavior.
- Benefits Service plan and coverage data available for all MVP-required lines of business, or an accepted temporary fallback.
- Basic escalation action with tracked event metadata and a known CCaaS handoff path.
- Launch evidence for security, tenant isolation, reliability, answer quality, support, and rollback.

## Workstreams

| Workstream | Outcome |
|---|---|
| Product scope and release governance | MVP scope, launch gates, risk owners, weekly readiness cadence |
| SDK and customer integration | SDK/API v1, SDK/API v2 escalation, docs, samples, versioning |
| Broker and orchestration | Chat API, streaming, sessions, Sierra integration, data enrichment, telemetry |
| Data services | Benefits all-LoB readiness, coverage checks, future data-service contracts |
| Escalation and CCaaS | Genesys routing discovery, SDK escalation action, handoff tracking |
| AI agents | Sierra stabilization, Member Agent/CSR Agent contract and transition plan |
| Operations | Dashboards, runbooks, failure modes, rollout/rollback, support model |

## Month-by-Month Plan

### June 2026: Lock MVP Scope and Remove Ambiguity

**Objective:** Convert concept and partial implementation into an executable September delivery plan.

**Deliverables**

- MVP scope brief with in-scope/out-of-scope, launch gates, and success metrics.
- Architecture decision record for the platform spine: Customer UI or Stellarus UI -> SDK/BFF -> Broker -> Data Services and AI runtime.
- Data readiness decision for specialty LoB: source, format, ingestion owner, validation owner, fallback, and fallback removal condition.
- Escalation discovery plan with BSC/PTP/Genesys owner, required APIs, routing metadata, and target decision date.
- SDK v1 contract draft covering chat start, streaming, session metadata, plan context, error handling, and versioning.
- Broker MVP gap assessment against current modules and September needs.

**Exit criteria**

- Scope and launch gates approved by Product, Apps, Data, and required customer-facing stakeholders.
- Specialty LoB path has a named owner and a documented fallback.
- Genesys escalation unknowns are converted into explicit decision questions with due dates.
- SDK v1 and broker API contracts are stable enough for implementation and docs.

### July 2026: Alpha Platform Path

**Objective:** Deliver the first Stellarus-owned platform path while the July 1 Sierra release continues as the immediate customer path.

**Deliverables**

- July 1 release support for the BSC/Sierra path, with lessons captured as reusable platform requirements.
- July 15 platform alpha with demo UI, SDK/API v1, broker streaming, Sierra-backed responses, CCS context-token flow, and Benefits Service plan lookup.
- Benefits Service all-LoB ingestion path implemented or operational fallback accepted.
- Broker telemetry baseline for request volume, latency, error rate, Sierra calls, data service calls, token usage, and correlation ID propagation.
- SDK docs alpha: install/use guide, environment variables, sample customer integration, and known limitations.
- Initial human review rubric for grounded answer quality and unsupported-answer fallback behavior.

**Exit criteria**

- A demo user can load plan context, ask a coverage/benefits question, and receive a streamed response through the Stellarus path.
- Broker emits enough telemetry to debug one request across UI/BFF, broker, Sierra, and Benefits Service.
- SDK/API v1 docs are usable by an engineer outside the core Apps team.
- The July Sierra implementation is mapped to platform-owned reusable pieces and temporary pieces.

### August 2026: Escalation, Customer Integration, and Release Candidate

**Objective:** Move from alpha to release candidate by proving BSC integration, escalation, data completeness, and operational readiness.

**Deliverables**

- August 1 SDK/API v2 contract for escalation: event name, routing payload, conversation summary, plan/member context policy, handoff result, and audit fields.
- Genesys or approved CCaaS handoff path implemented in the minimal MVP form.
- BSC integration start with customer UI or agreed integration shell.
- August 15 release candidate with stable SDK/API, broker, Benefits Service, Sierra integration, telemetry, and escalation action.
- Launch readiness pack: runbook, incident path, support triage guide, rollback plan, known issues, and customer communication notes.
- Security and tenant-isolation verification checklist for context-token handling, customer slug routing, scopes, and sensitive log redaction.
- Answer-quality review sample set and acceptance threshold for MVP-covered scenarios.

**Exit criteria**

- Release candidate passes representative happy-path, data-missing, auth-failure, Sierra-failure, Benefits-failure, and escalation-failure scenarios.
- BSC integration can run against target environments without hardcoded customer or port assumptions.
- Escalation has a tracked start event, handoff result, and observable failure behavior.
- Go/no-go risks are reduced to explicit launch exceptions or accepted deferrals.

### September 2026: MVP Launch and Stabilization

**Objective:** Launch the Stellarus Platform MVP and stabilize it using production evidence.

**Deliverables**

- September 1 MVP launch or controlled pilot launch with BSC member chat.
- Daily launch monitoring for the first two weeks: uptime, latency, failure rates, quality review, escalations, and data issues.
- Post-launch defect triage and release cadence.
- MVP retrospective focused on reusable platform contracts, temporary Sierra/direct-fetch debt, SDK friction, data service readiness, and support gaps.
- Q4 foundation backlog approved and sequenced.

**Exit criteria**

- MVP meets launch gates or has explicitly accepted exceptions.
- Support can trace a user issue across UI, SDK/BFF, broker, Benefits Service, Sierra, and escalation handoff.
- Product and Engineering agree which parts of MVP are platform foundation versus temporary customer-release scaffolding.
- Q4 work is prioritized by platform leverage, risk reduction, and next product/customer demand.

### October 2026: Platform Hardening and Contract Generalization

**Objective:** Convert MVP implementation into durable platform contracts.

**Deliverables**

- Capability registry draft covering product, agent, required data services, scopes, quality gates, telemetry, owner, and rollout status.
- Data service adapter contract for Benefits Service and draft contracts for member profile, eligibility, and claims history.
- Broker routing model for Sierra, Member Agent, CSR Agent, and future agents.
- SDK versioning and deprecation policy.
- Production dashboard v1 by customer, capability, agent runtime, and data service.
- Cost baseline for token usage and Sierra calls per successful answer.

**Exit criteria**

- New platform capabilities can be described in a registry format before implementation.
- Benefits Service is documented as the reference data service pattern.
- MVP telemetry is sufficient for weekly product/operations review.
- The team has a measured cost baseline rather than anecdotal usage estimates.

### November 2026: Agent Expansion and Multi-Service Data Foundation

**Objective:** Expand beyond the initial Sierra member chat path without weakening platform governance.

**Deliverables**

- Member Agent alpha behind the broker for a narrow, evaluated use case.
- CSR Agent alpha or CSR assist integration path aligned with the existing agentic-broker-chat experience.
- Member/eligibility/claims service interface specs and mock-free integration plan.
- Escalation pattern generalized beyond Genesys where possible.
- Evaluation harness v1 for source grounding, unsupported-answer fallback, escalation appropriateness, and regression cases.
- Data freshness and lineage reporting for Benefits Service and the next planned data services.

**Exit criteria**

- At least one non-Sierra or Stellarus-owned agent capability can run behind the broker in a non-production or controlled environment.
- Future data services have clear contracts and owners.
- Evaluation results can block promotion when quality or grounding fails.
- Escalation remains a platform action, not a customer-specific UI-only behavior.

### December 2026: Foundation Review and 2027 Scale Plan

**Objective:** Close the year with a repeatable platform operating model and a 2027 scaling plan.

**Deliverables**

- Platform foundation review: what is production-grade, what is alpha, what remains temporary, and what should be retired.
- 2027 roadmap for customer onboarding, additional conversational surfaces, data service expansion, and agent maturity.
- Production readiness standard for future capabilities, including security, tenant context, data service contract, telemetry, evaluation, support, and rollback.
- SDK developer experience review and prioritized improvements.
- Cost and performance improvement plan for broker, Sierra usage, caching, data enrichment, and agent routing.
- Decision record for temporary Sierra-direct or non-platform flows with deprecation timing.

**Exit criteria**

- Leadership can see a clear path from the BSC MVP to a repeatable platform.
- Platform onboarding has a defined intake, readiness gate, and owner model.
- Engineering has a sequenced 2027 backlog grounded in evidence from the MVP.
- Temporary MVP debt is either retired or explicitly carried with owner and date.

## Cross-Month Decision Log

| Decision | Needed By | Owner Recommendation | Notes |
|---|---:|---|---|
| Specialty LoB source and ingestion path | 06/28/2026 | Apps + Data | Blocks confident July and September data readiness |
| SDK v1 surface area | 06/30/2026 | Apps | Needed for July 15 alpha |
| Genesys escalation mechanics | 07/19/2026 | Apps + PTP + BSC | Needed for SDK v2 and August RC |
| September MVP launch gates | 07/15/2026 | Product + Apps | Should be stable before alpha review |
| Sierra temporary logic deprecation | 08/15/2026 | Product + Apps | Should be decided by release candidate |
| Q4 agent expansion priority | 09/15/2026 | Product + Data Science + Apps | Determines October and November capacity allocation |

## MVP Launch Gates

- **Functional:** chat streaming, plan context, representative benefits answers, basic escalation, and error handling pass.
- **Tenant and auth:** context-token validation, customer slug routing, scopes, and sensitive-log redaction verified.
- **Data:** all MVP-required Benefits data available or fallback accepted with owner and removal date.
- **Operations:** dashboards, runbooks, incident path, rollback, and support triage are ready.
- **Quality:** grounded answer sample set passes agreed threshold; known unsupported cases fall back cleanly.
- **Integration:** BSC integration docs and configuration are complete; no hardcoded customer, port, or environment assumptions.

## Open Risks

- Specialty LoB remains the highest data risk because it directly affects answer completeness.
- Genesys escalation remains the highest integration risk because routing behavior and API/SDK mechanics are not yet fully understood.
- SDK distribution and documentation can become the release bottleneck if treated as an afterthought.
- Broker and Benefits Service are close to the right architecture, but September readiness depends on end-to-end validation, not individual module completeness.
- The Q4 foundation could dilute if it tries to absorb every data domain at once; use Benefits Service as the reference pattern and add data services through contracts.

## Evidence Used

- `Compass-next-steps-v2.pptx`: extracted slides identify July 1 non-Stellarus release, September 1 Stellarus platform target, July 15 alpha, August 1 SDK/escalation, August 15 release candidate, and blockers around specialty LoB, Genesys, Sierra reuse, and escalation UX.
- `ConvAI-Platform-v2.mmd`: defines customer UI and Stellarus UI inputs, CCS, Chat UI SDK, Chat Broker, Sierra.ai, Member Agent, CSR Agent, Data Services, Benefits Service, and external integrations as the platform concept.
- `benefits-service`: current implementation supports context-token routed plan ingestion/read APIs, customer-schema migrations, read logging, and coverage checks.
- `agentic-broker-api`: current implementation supports the broker module shape needed for auth, tenant context, Sierra, streaming, sessions, token counting, rate limiting, and circuit breaker behavior.
- `agentic-broker-chat`: current implementation supports the BFF pattern for Auth0 plus CCS context-token acquisition and forwarding to broker.
