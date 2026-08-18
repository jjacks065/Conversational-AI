# 🧩 Project Name: Tenant-Scoped Curated Chat Suggestions

**PDLC Phase:** Definition
**Authored Date:** 2026-08-17
**Status:** DRAFT
**Target Window:** Six weeks from approved kickoff

## 🎯 Problem Statement

Authenticated chat users need relevant, safe starter questions, but the platform does not yet have approved end-to-end release evidence for a shared capability that selects those questions from trusted tenant and persona context. Content managers also need to change and publish starter questions without requiring a frontend deployment or exposing targeting logic to the chat client.

**Impact:** Without this feature, chat surfaces must omit starter questions or recreate content and targeting logic per consumer, increasing frontend release coupling, tenant-safety risk, inconsistent user experiences, and gaps in content auditability and engagement measurement.

## 💡 Proposed Solution

Deliver the first governed `agentic-content-service` capability for curated chat suggestions and integrate it with one approved pilot chat surface. Authorized content managers can create, revise, publish, pause, and archive tenant-owned suggestions, while authenticated consumers receive deterministic placements based on verified customer and persona context plus optional validated application, surface, locale, and channel context.

The pilot consumer renders returned questions, submits a selected question through its existing chat API, and records displayed and selected events. Missing targeting attributes fail closed, published revisions remain immutable, locale selection follows explicit fallback policy, and consumer responses reveal no targeting internals.

## 👥 Target Users

**Primary Users:**

* **Authenticated chat user:** Receives relevant starter questions for the verified customer and persona without exposure of targeting logic or sensitive data.
* **Authorized content manager:** Changes governed starter-question content, targeting, scheduling, and publication state without a frontend deployment.

**Secondary Users:**

* **Chat integration engineer:** Integrates one stable placement and event contract instead of consumer-specific targeting.
* **Security and privacy reviewer:** Verifies tenant isolation, scope enforcement, safe locale behavior, and sensitive-data minimization.
* **Support and operations engineer:** Uses correlation IDs, sanitized errors, health signals, metrics, logs, and traces to diagnose delivery failures.

## ✅ Success Metrics

* **Safe and correct resolution:** Baseline is no approved end-to-end release evidence cited by the evaluated artifacts; target is 100% pass of the agreed context, lifecycle, locale, and cross-customer scenario matrix before pilot launch, with zero successful cross-customer or trusted-context override attempts; measurement source is contract and PostgreSQL integration test reports for `ACS-FR-001` through `ACS-FR-012`.
* **Pilot adoption and usefulness:** Baseline is no service-backed placement funnel established for the pilot surface; target is at least 95% of successful placement responses with results rendered and recorded as `displayed`, plus at least a 10% `selected / displayed` rate within 30 days; measurement source is customer-scoped placement and idempotent event telemetry, with the usefulness target reconfirmed after seven days of pilot evidence.
* **Operational readiness:** Baseline is no approved representative-load evidence cited by the evaluated artifacts; target is placement resolution p95 at or below 200 ms inside the service boundary at the approved load and 100% of sampled pilot requests containing required, permitted trace fields before launch; measurement source is the load-test report, trace review, and dashboard checklist.

## 📦 Scope

* Versioned placement resolution supporting empty or partial caller context, customer defaults, deterministic ordering, deduplication, successful empty results, and a maximum of ten consumer-safe placements.
* Trusted evaluation context from verified CCS customer, principal, persona, and scopes plus allowlisted caller context; trusted identity request fields and missing-attribute matches fail closed.
* Versioned allowlist rules using `equals`, `in`, and `exists`, with AND semantics inside a rule set and OR semantics across rule sets.
* Customer-scoped campaign discovery, creation, mutable scheduling and priority, draft revisions, transactional publication, pause, archive, immutable published content, and audit evidence.
* Canonical BCP 47 translations with a required default locale, explicit bounded fallback chains, stable suggestion identity, and omission when no permitted translation exists.
* Customer-scoped, idempotent `displayed` and `selected` events tied to the resolution, suggestion, revision, and translation without chat content or unrestricted free text.
* One named pilot chat surface that renders placements, submits selected questions through its existing chat API, records required events, and remains usable for empty or unavailable results.
* Production-readiness coverage for shared authentication, tenant isolation, PostgreSQL migrations, Docker builder validation, generated OpenAPI documentation, sanitized health and errors, bounded timeouts, structured telemetry, dashboards, alerts, runbook, and representative load.

**Milestone Breakdown:**

* **Week 1:** Reconcile implementation status; name the pilot consumer and content-manager cohort; approve API vocabulary and error codes, caller-context registry, CCS scopes and personas including `system`, tenant-isolation approach, locale and translation-review policy, publication roles, event and audit retention, registered service and database ports, representative load, availability, and recovery objectives.
* **Week 2:** Validate the service foundation, migrations, customer-scoped persistence, campaign lifecycle, revisions, publication, audit, locale, health, and database behavior against `ACS-MGT-*`, `ACS-REV-*`, `ACS-PUB-*`, `ACS-HLT-*`, and `ACS-DB-*`, with tests citing each applicable clause ID.
* **Week 3:** Validate and harden the reported-complete curated-resolution path—context construction, fail-closed rules, deterministic ranking, translation selection, response mapping, and error behavior—against `ACS-RES-*` and `ACS-RULE-*`, with tests citing each applicable clause ID.
* **Week 4:** Validate `ACS-EVT-*`, including identical retry success and conflicting idempotency-key reuse, then complete pilot consumer integration, graceful degradation, and placement-funnel instrumentation.
* **Week 5:** Validate Docker builds, migrations, generated OpenAPI schemas and safe Swagger examples against `ACS-DOC-*`; complete security, tenant-isolation, sensitive-data, representative-load, observability, runbook, rollback, and failure-mode validation.
* **Week 6:** Complete release-candidate testing, user acceptance, success-metric review, and a coverage audit showing all 58 behavioral-contract clauses passed or explicitly blocked before accepted exceptions and go/no-go approval.

**Dependencies and Risks:**

* **Behavioral acceptance reference:** [behavioral-contract.md at `75c01e3`](https://github.com/stellarus-dev/stellarus-apps/blob/75c01e3206c9b4f557b2d587f315024077672418/apps/agentic-content-service/docs/contracts/behavioral-contract.md) is the clause-level acceptance source for this PRD; tests and release evidence must cite applicable `ACS-*` clause IDs, and contract changes require a corresponding PRD traceability review.
* The source specifications remain `Proposed`, while the delivery plan calls curated resolution complete; Week 1 must map each capability to implementation and test evidence before the six-week estimate is accepted.
* Product, the pilot consumer, CCS, Security, Data Architecture, Content Governance, Operations, and Support must resolve all nine delivery-plan decisions, including the `system` persona, translation workflow, registered ports, retention, and service objectives.
* The API documents conflicting invalid-request codes (`PLACEMENT_REQUEST_INVALID` and `SUGGESTION_REQUEST_INVALID`); one v1 code must be approved across the contract, implementation, tests, and client documentation.
* Cross-customer exposure and wrong-language delivery are launch-blocking risks mitigated through verified context, customer-scoped persistence, explicit locale fallback, and negative integration testing.
* The broad service name could expand scope into generation or CMS capabilities; mitigation is curated-only provenance and separate approval for future generated, translated, or authoring features.

## 🚫 Out-of-Scope

* LLM generation, rewriting, ranking, machine translation, or automatic publication; these require separate governance, provenance, quality, safety, cost, and fallback decisions.
* Answering selected questions, managing chat sessions, or replacing the existing chat and broker APIs.
* Individualized clinical or benefits recommendations, behavioral persona inference, PHI-bearing suggestions, or unrestricted user-authored content.
* A content-authoring UI, general-purpose CMS, bulk campaign studio, or arbitrary expression language.
* More than one production consumer, broad customer rollout, or generalized non-chat placement surfaces.
* Redis or another cache without measured PostgreSQL need and an approved invalidation design.
* Automatic locale inference or a consumer-owned static fallback question set without a separate product decision.

## 🏁 Exit Criteria

* [ ] All nine delivery-plan decisions have named owners and written approval, and implementation evidence is reconciled with the source documents' `Proposed` status.
* [ ] The v1 API uses one approved resource vocabulary and invalid-request error code across contract, implementation, tests, generated OpenAPI, and client documentation.
* [ ] Empty, partial, complete, missing-attribute, default, lifecycle, limit, deduplication, stable-order, and locale scenarios pass against PostgreSQL.
* [ ] Trusted-context override attempts are rejected, and cross-customer reads, writes, publication, resolution, and events fail in integration testing.
* [ ] Duplicate keys, invalid delivery windows, second-draft conflicts, unsupported rules, executable content, arbitrary paths, unsafe metadata, and sensitive telemetry fail closed without partial state.
* [ ] Revision numbers increase monotonically; published revisions and translations are immutable; and publication atomically commits lifecycle, content, rules, pointer, and audit changes.
* [ ] Identical event retries remain idempotent; conflicting idempotency-key reuse returns a sanitized conflict; and events reject invalid ownership and unrestricted-text payloads.
* [ ] The pilot surface renders eligible placements, submits selected questions, records required events, and remains usable for empty and unavailable responses.
* [ ] Representative-load evidence shows placement resolution p95 at or below 200 ms at the approved load.
* [ ] Docker builder, health checks, migrations, generated OpenAPI schemas, safe Swagger examples, logs, metrics, traces, dashboards, alerts, runbook, failure modes, and rollback procedures pass release-candidate validation.
* [ ] Tests cite applicable behavioral clause IDs, and the release evidence matrix accounts for all 58 `ACS-*` clauses as passed or explicitly blocked.
* [ ] Success metrics are instrumented, and Day 7 and Day 30 pilot reviews have named owners and scheduled dates.
* [ ] Product, Content Governance, the pilot Consumer, Engineering, Security, Operations, and Support approve go-live with no unresolved launch-blocking defect.

---

Template Version: `v2.0`
