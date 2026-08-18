# Compass Capability Roadmap — Feature PRD Set

**Authored Date:** August 7, 2026  
**CEI Assessment Date:** August 12, 2026  
**Status:** DRAFT  
**PDLC Phase:** Definition  
**Purpose:** Convert the Compass capability roadmap into independently estimable, cohort-ready feature releases.

## PRD Index

| Milestone | Feature PRD | Draft timebox | Initial supported surfaces | CEI | Priority tag |
| --- | --- | ---: | --- | ---: | --- |
| M0 | [Platform Reference Foundation](M0-Platform-Reference-Foundation-PRD.md) | 8 weeks | Member Chat, CSR Chat | 75 | `cei-strategic` |
| C1 | [Eligibility](C1-Eligibility-PRD.md) | 6 weeks | Member Chat, CSR Chat, Provider Chat | 60 | `cei-strategic` |
| C2 | [Claims](C2-Claims-PRD.md) | 6 weeks | Member Chat, CSR Chat, Provider Chat | 60 | `cei-strategic` |
| C3 | [Accumulators](C3-Accumulators-PRD.md) | 5 weeks | Member Chat, CSR Chat | 50 | `cei-opportunistic` |
| C4 | [Formulary](C4-Formulary-PRD.md) | 6 weeks | Member Chat, CSR Chat, Provider Chat | 60 | `cei-strategic` |
| C5 | [Provider Lookup](C5-Provider-Lookup-PRD.md) | 6 weeks | Member Chat, CSR Chat; Provider Chat when enabled | 60 | `cei-strategic` |
| C6 | [Provider Scheduling](C6-Provider-Scheduling-PRD.md) | 8 weeks | Member Chat, CSR Chat; Provider workflows when enabled | 65 | `cei-strategic` |

The order above is the baseline delivery sequence. Reordering a capability changes sequence only; it must not change the capability's product scope, acceptance criteria, or reliance on the versioned platform contract.

## CEI Ranked Comparison

CEI scores use the canonical CEI 1.0 formula `10C + 10I + 5E`. All assessments have **medium overall confidence** because the capabilities are net-new and the authored timeboxes still require engineering validation.

| CEI rank | Milestone | Score | Dimensions | Tag | Ranking rationale |
| ---: | --- | ---: | --- | --- | --- |
| 1 | M0 — Platform Reference Foundation | 75 | C3 I4 E1 | `cei-strategic` | September 1, 2026 committed MVP; portfolio-enabling foundation; large multi-team delivery. |
| 2 | C6 — Provider Scheduling | 65 | C2 I4 E1 | `cei-strategic` | Transformative move from information to governed transactions, offset by large operational complexity. |
| 3 | C1 — Eligibility | 60 | C2 I3 E2 | `cei-strategic` | High-value cross-surface coverage context; first baseline capability after M0. |
| 4 | C2 — Claims | 60 | C2 I3 E2 | `cei-strategic` | High-value claims explanation across three surfaces; roadmap order breaks the CEI tie. |
| 5 | C4 — Formulary | 60 | C2 I3 E2 | `cei-strategic` | High-value pharmacy coverage workflow with explicit safety boundaries. |
| 6 | C5 — Provider Lookup | 60 | C2 I3 E2 | `cei-strategic` | High-value search workflow and portable ProviderReference; roadmap order breaks the CEI tie. |
| 7 | C3 — Accumulators | 50 | C2 I2 E2 | `cei-opportunistic` | Useful but initially bounded to two surfaces and one cohort, with no reach baseline yet. |

**Sequencing interpretation:** CEI is decision guidance, not implementation approval and not a replacement for the accepted milestone sequence. C6 scores above C1–C5 because of its portfolio-level transactional impact, but remains sixth in the delivery plan so the platform can harden context, precision, retrieval, and action safety through earlier whole-capability releases.

### Re-score Triggers

- Promote a C1–C6 Category from C2 to C3 only when a funded commitment, accountable owner, or delivery date is recorded.
- Reassess Impact when baseline inquiry volumes, affected populations, or production KPI movement become available.
- Reassess Effort after engineering validates the end-to-end estimate, source integration, security review, QA, rollout, and operational load.
- Preserve the prior score, assessment date, evidence, and decision owner when a score changes.

## Shared Product Model

```text
Surfaces                           Spine                                  Brain
Member / CSR / Provider  →  Auth → Agent Broker → AI Agents  →  Governed knowledge services
persona + presentation      context + routing + policy + actions      provenance + freshness
```

- **Surfaces** own persona-specific presentation, interaction policy, and channel behavior.
- **The Spine** owns trusted actor/subject context, capability routing, conversation state, policy enforcement, action execution, and telemetry.
- **Capability agents** interpret the inquiry, request permitted Brain data, and return the standard response contract.
- **The Brain** owns governed data access, source authority, freshness, provenance, and deterministic business data.
- **Structured answers are the default.** Surface and tenant configuration may render approved less-structured or unstructured variants without changing the underlying evidence or outcome.
- **Surface-initiated actions are always supported.** Agent-recommended actions are optional by agent configuration. The Broker alone authorizes and executes side effects.

## Shared Measurement Definitions

### Grounded Resolution Rate

`GRR = eligible inquiries resolved correctly with sufficient source evidence / all eligible inquiries`

The numerator requires factual correctness, appropriate actor/subject context, current source data, provenance, and a usable response. Clarifications, abstentions, escalations, and failures are not counted as grounded resolutions.

### Safe Handling Rate

`Safe Handling Rate = turns correctly resolved, clarified, abstained, escalated, or safely failed / all evaluated turns`

Safe Handling is reported separately from GRR so appropriate abstention does not inflate product resolution.

### Required Turn Outcomes

Every turn emits exactly one terminal product outcome:

- `resolved_grounded`
- `clarification_required`
- `safe_abstention`
- `action_initiated`
- `escalated`
- `failed`
- `cancelled`

## Common Exit Gates for Every Milestone

These gates are repeated in each PRD's exit criteria and are non-negotiable unless the program steering group records an explicit exception:

1. At least 100 representative evaluation scenarios approved by Product, Operations, and the relevant domain owner.
2. GRR target of at least 95% on eligible scenarios.
3. Safe Handling target of at least 99% across the complete evaluation set.
4. 100% of successful answers include source provenance and freshness/as-of evidence.
5. 100% of evaluated turns emit one defined terminal outcome.
6. Zero cross-tenant data access in automated isolation testing.
7. Zero critical unsupported factual claims in launch evaluation.
8. 100% of side-effect actions are authorized, confirmed, idempotent, and audited.
9. Capability SLOs, runbook, cohort plan, rollback procedure, and owner sign-off are complete before release.

## Current-State Evidence Used in These Drafts

- `agentic-broker-api` already supports tenant-scoped resolver dispatch and an explicit `benefits.query` capability path; current source comments still identify durable conversation continuity as deferred work.
- `agentic-broker-chat` already passes a capability field and contains escalation flows that dispatch through the Broker.
- CSR Chat is live from `stellarus-ai/apps/csr-chat`, uses structured benefits plan data, and has an in-flight CCS context-token / Benefits Service integration path.
- Benefits Service provides customer-partitioned plan reads and coverage checks with audit logging, but deliberately does not resolve member eligibility or member-to-plan association.
- UM Composite exposes a current Enterprise Eligibility integration that can inform C1's governed Brain adapter.

These observations establish a credible starting point; they do not preselect the final runtime, service ownership, or source contract for every capability.

## Draft Assumptions Requiring Validation

- The first release of each PRD targets one approved tenant cohort and the listed surface profiles, not unrestricted enterprise rollout.
- Production source access, representative non-production data, and domain-owner availability are secured by the end of Week 1.
- Each capability is delivered through a versioned manifest, input/output schema, tool policy, and response contract.
- One primary capability is selected per turn. Cross-capability composition is optional and may not be required to complete a supported journey.
- Unknown metric baselines are measured against a frozen pre-release evaluation set during Week 1. Targets are release gates; baseline results are added before Build & Integrate sign-off.
- Accessibility conformance target is WCAG 2.2 AA for surface-rendered responses and controls.

## Program Decisions Still Open

| Decision | Needed by | Decision owner |
| --- | --- | --- |
| Initial tenant cohort and named surface owners for each milestone | Planning start | Product + Customer Operations |
| Production SLO values by capability and source system | End of Week 1 | Platform + Domain Engineering |
| Authoritative Claims, Accumulator, Formulary, Directory, and Scheduling services | Before each capability's Build & Integrate phase | Enterprise Architecture + Domain Owner |
| Standard response schema version and compatibility policy | M0 Week 2 | Product + Platform Architecture |
| Evaluation review and severity policy for unsupported claims | M0 Week 2 | AI Quality + Clinical/Domain Governance |
| Whether agent-recommended actions are enabled by tenant and capability | Before each capability cohort | Product + Risk/Operations |
