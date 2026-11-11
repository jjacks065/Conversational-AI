# PROJECT NAME: Product Feedback Collection

**PDLC Phase:** Definition
**Authored Date:** 2026-09-15
**Status:** DRAFT

## 🎯 Problem Statement

Compass products and any future Stellarus product needs a consistent way to collect feedback and/or NPS-style signals and correlate them to the product interaction being evaluated. CSR Chat (Databricks) already demonstrates a product-specific feedback path with response, question, session, user, feedback type, reason, and comment fields, but the reviewed Compass platform artifacts do not define a product-agnostic capability for authenticated, tenant-isolated, idempotent, append-only feedback ingestion and governed retrieval.

Without a standalone capability, each product must design its own feedback schema, persistence, retention, security controls, and dashboard integration. That fragmentation makes cross-product quality learning slower, creates inconsistent handling of potentially sensitive free text, weakens correlation between feedback and the evaluated interaction, and increases implementation and support cost.

**Impact:** The absence of a reusable collection contract limits the ability to convert product feedback into reliable quality and experience signals while CSR Chat comes online through APIs. It also creates avoidable rework and governance risk as additional products adopt feedback loops.

### 💡 Proposed Solution

Deliver an API-first, standalone product-feedback collection capability that can support any approved product or tenant. Compass products, CSR Chat and Member Chat, are the first integration focus, but the capability launches with production controls and a product-neutral contract suitable for full adoption; it is not limited to a single-tenant pilot.

The versioned REST contract will provide authenticated ingestion, paginated query, and machine-readable export. Each accepted record will contain one or more feedback signals and correlation metadata. A signal may include an indicator, a numeric score with declared scale metadata such as NPS 0–10, a free-form description, or any valid combination; at least one signal is required. Free-form descriptions are accepted independently of whether an indicator or score is supplied.

Every record must correlate to at least one opaque session, conversation, response, or interaction identifier and may include all available identifiers. The capability also captures trusted tenant context, product, channel, authenticated principal, event timestamp, schema version, a server-assigned feedback identifier, and receipt timestamp. Correlation identifiers support joins and traceability but never establish authorization.

Records are immutable after acceptance. Identical retries return the original outcome, while reuse of an idempotency key for a different payload is rejected. Policy-driven expiration under the tenant's configured retention policy is required lifecycle enforcement and does not create a general update or delete API.

Free-form descriptions are treated as potentially containing PII or PHI. They are encrypted in transit and at rest, access-controlled, excluded from application and infrastructure logs, and retained only according to tenant policy. Automated detection or redaction is not included in v1.

## 👥 Target Users

**Primary Users:**

- **Product integration engineer:** Sends product feedback with stable correlation metadata through a documented API.
- **Product analytics or quality owner:** Queries or exports tenant-authorized feedback for experience, quality, or NPS analysis.
- **Compass product team:** Integrates chat experiences (CSR Chat and Member Chat) as the first production consumer without coupling its UI behavior to the collection capability.

**Secondary Users:**

- **Tenant administrator or data-governance owner:** Configures and approves tenant retention and access policy.
- **Security and privacy reviewer:** Verifies tenant isolation, sensitive-text protection, access controls, and lifecycle enforcement.
- **Dashboard engineer:** Uses the versioned query contract as a source for separately scoped dashboards.
- **Support and operations engineer:** Monitors service health and diagnoses ingestion or retrieval failures without accessing feedback text through logs.

## ✅ Success Metrics

- **Reliable, responsive ingestion:** Baseline is no reviewed standalone service-level baseline; target is at least 99.9% of valid accepted submissions durably persisted, with write latency p95 at or below 300 ms under the approved full-adoption forecast at 2× projected peak load. Measure through service telemetry and release-candidate durability/load evidence.
- **Retrieval and correlation integrity:** Baseline is a Compass-specific export path rather than a general query contract; target is query latency p95 at or below 1 second and 100% round-trip preservation of submitted correlation fields across ingestion, query, and export. Measure through contract, persistence, and representative-volume query tests.
- **Safe adoption readiness:** Baseline is no approved cross-product tenant-isolation and retention evidence for a standalone capability; target is zero successful cross-tenant access attempts, 100% expiry of eligible records within the approved tenant-policy enforcement window, a production CSR Chat integration, and approved onboarding/API documentation usable by additional products at launch. Measure through security tests, retention reconciliation, integration evidence, and readiness review.

**Guardrails:** No feedback text appears in service logs; invalid or unauthorized submissions are not persisted; dashboard delivery and feedback participation rates are not service success metrics because solicitation and visualization are owned by consuming products.

## 📦 Scope

### Product Requirements

- **REQ-001 — Authenticated tenant boundary:** Require authenticated submit, query, and export access; derive tenant authorization from trusted identity context; enforce tenant-scoped writes and reads.
- **REQ-002 — Flexible feedback signals:** Accept an optional indicator, optional numeric score with required scale minimum and maximum plus an optional scheme label, and an optional free-form description of up to 4,000 Unicode characters. Require at least one of these signals.
- **REQ-003 — Product-neutral context:** Capture product, channel, event timestamp, schema version, authenticated principal, and an optional caller-defined feedback or survey type so NPS and other product-feedback models can coexist.
- **REQ-004 — Interaction correlation:** Require at least one session, conversation, response, or interaction identifier; accept and preserve all supplied identifiers as opaque values.
- **REQ-005 — Idempotent append-only ingestion:** Require a caller-provided idempotency key, return the same accepted outcome for an identical retry, reject conflicting reuse, and prohibit in-place record mutation.
- **REQ-007 — Query and export access:** Provide authorized tenant-scoped filtering by time, product, channel, feedback or survey type, signal, and correlation identifiers; return paginated API results and machine-readable exports suitable for downstream dashboard services.
- **REQ-008 — Tenant-configurable retention:** Require an approved retention configuration before tenant activation, apply policy to all tenant records, prevent one tenant from changing another tenant's policy, and produce auditable expiry evidence.
- **REQ-009 — Sensitive-text protection:** Treat descriptions as potentially containing PII or PHI; encrypt them in transit and at rest, restrict access by role, exclude payloads from logs and error messages, and audit authorized retrieval/export activity.
- **REQ-010 — Adoption readiness:** Complete CSR Chat production integration while keeping the service contract, configuration, documentation, operations, and capacity model free of CSR Chat-specific logic or a single-tenant rollout restriction.

**Scope Considerations**

- **Data Migration** - Facilities for migration all existing feedback collected in CSR Chat MVP on Databricks

### Dependencies, Risks, and Decision Triggers

| Dependency or risk                                                    | Consequence                                    | Mitigation / trigger                                                                                                                                                                                   |
| --------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Trusted identity does not provide stable tenant and principal context | Cross-tenant exposure or unauditable access    | Tenant activation is blocked until trusted context and negative isolation tests pass.                                                                                                                  |
| Free-form text contains PII or PHI                                    | Privacy, compliance, and breach exposure       | Treat all descriptions as sensitive, omit them from logs, enforce role access and tenant retention; add automated redaction only through a separately approved scope.                                  |
| Product-defined indicators and scales become inconsistent             | Cross-product analysis is misleading           | Preserve declared scale and feedback type metadata; analytics owners normalize interpretation outside ingestion. Revisit a governed taxonomy if two or more consumers cannot compare results reliably. |
| Forecast volume or retention creates unacceptable cost                | Reliability or operating-cost target is missed | Validate at 2× approved peak and model storage by tenant retention before go-live; revisit tiering or asynchronous export if targets fail.                                                            |
| CSR Chat assumptions leak into the shared contract                    | Later products require bespoke fields or forks | Require product-neutral naming and an additional-product contract review before release; reopen the envelope only if a second integration cannot map without product-specific fields.                  |

**Assumptions and confidence:** High confidence in the approved product boundary and security posture; medium confidence in capacity and storage targets until the full-adoption volume forecast and tenant retention profiles are supplied. The 4,000-character description limit is a reversible v1 constraint and must be confirmed during Week 1 contract review. Material changes to signal semantics, tenant isolation, or storage sensitivity require Product, Security, and Data Governance approval.

## 🚫 Out-of-Scope

- Feedback controls, polls, prompts, placement, frequency, timing, blocking behavior, accessibility, or any other consuming-product UI decision.
- Product dashboards, reports, visualizations, alert thresholds, or interpretation of feedback and NPS results; the API only supplies governed data.
- Compass conversation routing, response generation, session management, orchestration, or ownership of this API.
- Language-specific client SDKs in v1; consumers integrate through the documented REST/OpenAPI contract.
- Automated sentiment analysis, feedback classification, PII/PHI detection or redaction, LLM-as-judge, quality scoring, or summarization.
- Automatic prompt, model, content, or workflow changes based on collected feedback.
- Case management, user follow-up, service-ticket creation, remediation workflows, or closed-loop notification.
- End-user editing, retraction, or deletion APIs; retention expiry and approved compliance administration remain governed lifecycle functions.
- Product-specific taxonomies beyond preserving the declared feedback type, indicator, score scale, and description.

## Requirement-to-Outcome Traceability

| Intended outcome                                                                | Requirements              | Validation evidence                                                                                     |
| ------------------------------------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------- |
| Products submit useful feedback without UI coupling                             | REQ-002, REQ-003, REQ-004 | OpenAPI review, signal/correlation scenario matrix, CSR Chat integration evidence                       |
| Retries never create ambiguous duplicate records                                | REQ-005                   | Identical-retry and conflicting-key contract tests plus persistence reconciliation                      |
| Authorized consumers can supply dashboards without this scope building them     | REQ-007                   | Query/filter/pagination tests and export consumer acceptance                                            |
| Feedback remains isolated, protected, and governed                              | REQ-001, REQ-008, REQ-009 | Cross-tenant negative tests, access audit, encryption/log review, retention reconciliation              |
| Capability is ready for broad adoption rather than a one-off CSR implementation | REQ-010                   | CSR Chat production integration, additional-product contract review, onboarding and operations approval |

## 🏁 Exit Criteria

- [ ] Product, Engineering, Security, Privacy, Data Governance, and Analytics owners approve the versioned API contract and full-adoption release boundary.
- [ ] Valid indicator-only, score-only, description-only, and combined-signal submissions are accepted; a submission with no signal is rejected without persistence.
- [ ] A submission with at least one correlation identifier is accepted; a submission with none is rejected; all supplied identifiers round-trip unchanged through query and export.
- [ ] Authenticated principal, trusted tenant, product, channel, event timestamp, schema version, feedback identifier, and receipt timestamp are captured for every accepted record.
- [ ] Identical retries return the original accepted outcome, conflicting idempotency-key reuse is rejected, and no supported API mutates an accepted record.
- [ ] Submit, query, and export authorization prevents cross-tenant access with zero successful attempts in the approved negative-security suite.
- [ ] Free-form descriptions are encrypted in transit and at rest, excluded from logs and error payloads, role-restricted, and covered by retrieval/export audit evidence.
- [ ] Every activated tenant has an approved retention configuration; eligible records expire within the approved enforcement window and expiry is auditable.
- [ ] At 2× the approved full-adoption peak forecast, at least 99.9% of valid accepted submissions are durably persisted, write latency p95 is at or below 300 ms, and query latency p95 is at or below 1 second.
- [ ] Query and export support the approved filters, pagination, versioning, and machine-readable output required by independent dashboard consumers.
- [ ] An integration representative from at least two product squads confirm that the documented contract and onboarding model can support its expected feedback use case without a product-specific API fork.
- [ ] Dashboards, UI presentation, automated analysis/redaction, historical migration, model training, and remediation workflows remain outside the release scope.
- [ ] Runbook, support guide, capacity model, retention operations, recovery procedure, monitoring, API examples, known limitations, and adoption guide are approved before production launch.

---

Template Version: `v2.0`
