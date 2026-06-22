# 🧩 Project Name: Broker Conversation Orchestration

**PDLC Phase:** Definition
**Authored Date:** 2026-06-22
**Status:** DRAFT
**Target Window:** June 24-August 15, 2026

## 🎯 Problem Statement

If chat surfaces call Sierra.ai, data services, or escalation paths directly, Stellarus loses the reusable platform entry point needed for tenant-safe routing, telemetry, failure handling, and future agent transition.

**Impact:** Direct or parallel runtime logic makes the September MVP hard to support and slows later migration to Member Agent, CSR Agent, and additional customer surfaces.

## 💡 Proposed Solution

Make the broker API the standard conversation entry point for MVP chat, owning request validation, session handling, SSE streaming, Sierra.ai integration, data enrichment, rate limits, circuit breakers, token accounting, and telemetry.

The MVP broker route should support BSC member benefits chat while preserving enough route, runtime, and data-service metadata to become the foundation for post-MVP capability routing.

## 👥 Target Users

**Primary Users:**

* **Member end user:** Gets a streamed, grounded answer through a stable chat session.
* **Stellarus Apps engineer:** Owns the broker runtime contract and service behavior.

**Secondary Users:**

* **Data service owner:** Receives standardized tenant-aware data access calls from the broker.
* **AI/runtime owner:** Uses broker contracts to transition from Sierra.ai toward Stellarus-owned agents over time.
* **Support engineer:** Traces failures across SDK/BFF, broker, Sierra.ai, Benefits Service, and escalation.

## ✅ Success Metrics

* **Alpha streaming path:** Baseline is no complete Stellarus-owned SDK/BFF-to-broker-to-Sierra alpha path; target is July 15 alpha supporting streamed responses through SDK/BFF to broker to Sierra.ai; measurement source is alpha demo evidence and stream lifecycle telemetry.
* **Release-candidate scenario coverage:** Baseline is component-level confidence without end-to-end validation; target is August 15 release candidate passing happy-path, data-missing, auth-failure, Sierra-failure, Benefits-failure, rate-limit, circuit-breaker, and stream-disconnect scenarios; measurement source is RC validation checklist.
* **Broker telemetry completeness:** Baseline is incomplete route/runtime/data-service telemetry; target is 100% of broker requests emitting route, latency, token usage, data-service call, runtime call, correlation ID, and error telemetry; measurement source is sampled request traces and dashboard fields.

## 📦 Scope

* Chat session creation and lifecycle handling.
* SSE streaming response contract.
* Sierra.ai runtime adapter for MVP.
* Benefits Service enrichment call pattern.
* Rate limiting, circuit breaker, and failure response behavior.
* Token accounting and broker-level telemetry.
* MVP capability route definition for BSC member benefits chat.
* Support trace fields for route, runtime, data service, error source, and correlation ID.

**Milestone Breakdown:**

* **June 24-June 30:** Complete broker MVP gap assessment and stabilize conversation API contract.
* **July 1-July 15:** Deliver alpha route with session handling, SSE streaming, Sierra.ai adapter, and Benefits Service enrichment.
* **July 16-August 1:** Add rate limiting, circuit breaker behavior, token accounting, and route/runtime telemetry.
* **August 2-August 15:** Complete release-candidate scenario validation and support trace review.

**Dependencies and Risks:**

* Depends on SDK/API contract, CCS context-token validation, Benefits Service readiness, and Sierra.ai runtime availability.
* Risk: temporary Sierra-specific logic becomes embedded in broker contracts; mitigation is isolating Sierra.ai as a runtime adapter and recording temporary behavior with exit criteria.
* Risk: telemetry is deferred until after functional behavior; mitigation is treating telemetry as a broker exit criterion for each scenario.

## 🚫 Out-of-Scope

* Full replacement of Sierra.ai with Stellarus-owned Member Agent.
* Multi-agent orchestration beyond the MVP Sierra-backed route.
* Arbitrary external integration execution outside approved escalation flow.
* Long-term capability registry implementation, except for MVP route metadata needed for traceability.

## 🏁 Exit Criteria

* [ ] Broker exposes stable MVP conversation API accepted by SDK/BFF consumers.
* [ ] Broker streams Sierra-backed responses through the Stellarus path.
* [ ] Broker enriches supported requests with tenant-scoped Benefits Service data.
* [ ] Broker failure behavior is documented for auth, data service, Sierra.ai, rate limit, circuit breaker, and stream disconnect cases.
* [ ] Broker telemetry enables one request to be traced across UI/BFF, broker, Sierra.ai, Benefits Service, and escalation.
* [ ] Release-candidate validation covers happy path and defined failure scenarios with pass/fail evidence.

