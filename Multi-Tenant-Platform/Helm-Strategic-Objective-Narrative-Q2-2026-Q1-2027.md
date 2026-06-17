# Helm Platform Foundational Strategic Objective

****PDLC Phase:**** Definition
**Status:** Draft
**Authored Date:** 06/03/2026

---

## 📝 Executive Summary

Stellarus is establishing multiple conversational Artificial Intelligence (AI) capabilities from related but fragmented foundations withing the Compass Product Family: Member Chat through Sierra.ai, Customer Service Representative (CSR) Chat through Databricks-hosted Nexus Benefits application services, Kubernetes foundational rebuild, agentic broker services, chat/Backend-for-Frontend (BFF) experience work, and emerging tenant-aware data services. These efforts are directionally aligned, but they do not yet operate under a single product objective with shared success metrics, domain data-plane contracts, runtime portability expectations, compliance guardrails, and cost controls.

Helm will establish the reusable, multi-tenant, runtime-portable conversational AI platform for enterprise chat products, enabling Benefits Chat for both members and CSR experiences as the reference implementation and multi-tenant isolated domain data planes. The business value is faster product onboarding, stronger compliance evidence, lower duplicated engineering effort, improved operational visibility, and a more sustainable path toward high-accuracy, low-latency AI chat at enterprise scale.

## 🎯 Strategic Context & Vision

* **Company Alignment:** Helm supports the platform modernization, customer scalability, operational efficiency, and AI-enabled service experience pillars by turning isolated conversational products into a reusable internal platform foundation.
* **Problem Statement:** Without a formal product-led platform, each conversational product risks rebuilding tenant context handling, domain routing, response grounding, model orchestration, telemetry, runtime deployment patterns, and compliance evidence independently. That increases cost, slows customer onboarding, weakens cross-product observability, and creates unnecessary risk for regulated, multi-tenant customer data.
* **The Vision:** Helm becomes the governed conversational AI foundation that lets Stellarus launch and operate enterprise chat experiences across customers and domains with reusable capability contracts, trusted data-plane access, runtime portability, self-adapting quality baselines, and measurable cost/performance discipline.

## 📊 Objectives and Key Restults Framework

### Objective (Qualitative)

> **Establish Helm as the reusable, multi-tenant, runtime-portable conversational AI platform for enterprise chat products, enabling Benefits Chat for both Member and CSR experiences as the reference implementation and expanding toward additional tenant-isolated domain data planes.**

Helm will provide standard capabilities for customer context, domain routing, grounded response orchestration, compliance controls, runtime migration, cost-aware AI execution, per-customer observability, and product onboarding so future conversational products can launch faster without compromising tenant integrity or data governance.

### Key Results (Quantitative)

**KR1: Runtime Foundation and Migration Readiness**

* Establish the first tenant-isolated conversational AI routing layer for voice and chat experiences, with benefits inquiries as the initial supported domain and a repeatable expansion model for additional governed data planes.
* Complete Kubernetes cutover readiness for CSR Benefits/Nexus Benefits with documented smoke/regression evidence, rollback path to Databricks App runtime, Azure API Management (APIM) route validation, and telemetry-write validation.
* Make Kubernetes the primary runtime pattern for new conversational product deployments, with Databricks Lakebase and Databricks MLflow dependencies explicitly documented as active data and telemetry dependencies where still required.
* Define platform runtime standards for health checks, APIM routes, deployment promotion, rollback, model failover, circuit breaking, and per-runtime telemetry isolation.

**KR2: Tenant Integrity and Data-Plane Governance**

* Maintain **zero known cross-tenant data access incidents** across platform reference flows.
* Define the domain data-plane contract covering tenant isolation, effective dating, source freshness, access scopes, audit logging, observability dimensions, and migration-state labeling.
* Validate at least three reference data-plane scenarios: benefits plan lookup, formulary/medication intelligence, and one non-benefits enterprise chat capability.

**KR3: Platform Reuse and Product Onboarding**

* Publish the initial capability registry model for declaring conversational capabilities, domain adapters, required scopes, data-plane dependencies, response contracts, and evaluation requirements.
* Onboard at least two reusable platform capabilities beyond the initial benefits query path.
* Reduce estimated new conversational product onboarding effort by **50%** versus building a standalone product path, measured through repeated use of shared runtime, broker, data-plane, telemetry, and evaluation patterns.

**KR4: Quality, Compliance, and Self-Adapting Evaluation**

* Sustain **>95% grounded-answer accuracy target** for Benefits reference flows where validated source data exists.
* Establish a reusable evaluation harness covering source-grounding checks, compliance/script validation, answer completeness, fallback behavior, and human review outcomes.
* Establish self-adapting baseline capabilities that use telemetry, feedback, source-grounding evidence, and data-change signals to recommend and validate improvements to routing, retrieval, prompting, response templates, and data-plane usage while maintaining accuracy and latency targets.
* Require each platform capability to define measurable quality gates before production routing, including regression evidence and owner acceptance for waived gaps.

**KR5: Cost and Performance Discipline**

* Establish baseline requests per minute (RPM), tokens per minute (TPM), latency, token usage (per session, per request), cached-token impact, model cost, and cost per successful answer.
* Progress toward the conversational AI unit economics target from the existing **$0.25-$0.27 per query baseline** toward **<$0.08 per query**, while preserving quality gates.
* Provide per-customer and per-capability dashboards for cost, throughput, latency, error rate, model fallback, and telemetry completeness.

## 🕹️Strategic Levers

* **Lever 1: Conversation Orchestration:** Standardize capability routing, prompt/context assembly, response grounding, streaming behavior, memory/session handling, fallback, and compliance guardrails so new chat experiences do not rebuild orchestration logic independently.
* **Lever 2: Domain Data-Plane Governance:** Define tenant-isolated benefits, formulary, provider, claims, customer configuration, and future enterprise data planes with clear source, freshness, versioning, lineage, auditability, and access contracts.
* **Lever 3: Runtime Portability and Deployment Standards:** Use Kubernetes as the preferred forward runtime path while documenting where Databricks, Lakebase, MLflow, Azure AI/APIM, Sierra.ai, and other managed services remain active dependencies.
* **Lever 4: Telemetry, Evaluation, and Self-Adapting Baselines:** Use common metrics, regression evidence, human review, source-grounding checks, and data-change signals to continuously improve platform behavior through governed recommendations rather than uncontrolled autonomous production changes.
* **Lever 5: Customer and Compliance Control:** Preserve verified tenant context, scope enforcement, audit trails, customer onboarding controls, and dedicated-cell exceptions where contractual, regulatory, scale, or risk conditions require them.

## 🎟️ Themes & High-Level Requirements

### Theme A: Governed Product Capability Model

* **Requirement 1:** Create the capability registry model that lets product and engineering teams declare supported intents, required data planes, access scopes, response expectations, quality gates, ownership, rollout status, and deprecation policy before a capability is exposed to production traffic.
* **Requirement 2:** Define the platform onboarding model for new customers, new conversational products, and new data domains, including readiness gates, implementation patterns, documentation, support ownership, and rollback requirements.

### Theme B: Domain Data-Plane and Tenant Integrity

* **Requirement 1:** Establish platform-level contracts for conversational capabilities, domain data-plane access, tenant context, response grounding, compliance controls, evaluation, telemetry, and operational readiness.
* **Requirement 2:** Define the long-term relationship between Lakebase-backed data, customer-schema service data, future domain services, and shared reference data so platform capabilities can route to trusted sources without creating duplicate sources of truth.
* **Requirement 3:** Confirm canonical customer, tenant, persona, scope, and correlation identifiers across chat user interface (UI), broker, application programming interfaces (APIs), domain services, telemetry, and reporting.

### Theme C: Quality, Compliance, and Self-Adapting Learning Loop

* **Requirement 1:** Establish quality and compliance practices for grounded-answer accuracy, source alignment, script/compliance validation, human review loops, regression evidence, and production acceptance.
* **Requirement 2:** Establish reusable test sets, regression workflows, human-review labels, answer-quality rubrics, and acceptance thresholds for each capability and data plane.
* **Requirement 3:** Build self-adapting baseline capabilities that recommend and validate improvements to routing, retrieval, prompting, response templates, and data-plane usage while preserving human approval for regulated behavior changes.

### Theme D: Runtime, Observability, and Cost Discipline

* **Requirement 1:** Define platform runtime standards for health checks, APIM routes, deployment promotion, rollback, model failover, circuit breaking, and per-runtime telemetry isolation.
* **Requirement 2:** Establish a platform measurement framework for quality, adoption, latency, throughput, requests per minute, tokens per minute, tokens per request, turns per session, model usage, cost, fallback, source usage, and per-user/per-customer usage patterns.
* **Requirement 3:** Align on canonical platform metrics, metric definitions, runtime labels, customer dimensions, dashboard owners, and executive reporting cadence.

### Theme E: Reference Implementation and Expansion Path

* **Requirement 1:** Use Benefits Chat as the reference implementation to prove platform contracts, while avoiding limits that make the platform specific to CSR Benefits, Nexus Benefits, or the current Databricks-to-Kubernetes transition.
* **Requirement 2:** Validate reference data-plane scenarios for benefits plan lookup, formulary/medication intelligence, and one non-benefits enterprise chat capability before broader platform expansion.
* **Requirement 3:** Decide when to prioritize platform hardening, new domain onboarding, customer expansion, cost optimization, and experience improvements when these compete for the same engineering capacity.

## ⚠️ Constraints, Risks & Dependencies

* **Dependencies:**
  * **Product operating model:** Confirm who owns product strategy, capability intake, architecture review, production readiness, support escalation, and roadmap prioritization across product, engineering, data, security, compliance, and operations.
  * **Runtime strategy:** Confirm Kubernetes-first direction for application runtime while documenting where Databricks, Lakebase, MLflow, Azure AI/APIM, Sierra.ai, and other managed services remain active platform dependencies.
  * **Capability governance:** Approve the capability registry standard before broad onboarding.
  * **Data-plane governance:** Align source-of-truth ownership across Lakebase-backed data, customer-schema service data, future domain services, and shared reference data.
  * **Compliance acceptance model:** Define what evidence is required before a capability can serve regulated production traffic, including source grounding, script validation, audit logs, human review, fallback behavior, and customer-specific policy handling.
* **Risks:**
  * Runtime migration consumes platform capacity before reusable product value is visible.
  * Cost reduction harms answer quality or compliance.
  * Multiple telemetry sources create inconsistent KPI reporting.
  * Domain-agnostic ambition dilutes the Benefits reference implementation.
  * Self-adapting baseline language is misread as autonomous AI changing regulated production behavior without review.
* **Mitigations:**
  * Treat Kubernetes cutover as one platform milestone, but require reusable runtime standards and evidence templates as migration outputs.
  * Tie cost targets to quality gates, regression evidence, and source-grounding metrics; do not count lower cost as success when accuracy or compliance falls below threshold.
  * Define canonical metrics, ownership, runtime labels, and migration-state dimensions before executive reporting.
  * Keep Benefits Chat as the reference implementation and require generalized contracts to be proven against current delivery needs.
  * Frame self-adapting baselines as AI-assisted continuous improvement with governed promotion and human approval for regulated behavior changes.
* **Out-of-Scope:**
  * Final external naming or brand decision for the Platform (Helm).
  * External packaging, pricing, SKU definition, or go-to-market positioning for the platform as a standalone commercial offering.
  * A full replacement of existing product applications before platform contracts are proven through reference implementations and adopted through planned product increments.
  * A universal low-code/no-code builder for arbitrary conversational applications; the near-term platform should prioritize governed reusable capabilities, not unrestricted app generation.
  * Dedicated customer cells as the default operating model; dedicated isolation remains an exception for contractual, regulatory, scale, or risk-based requirements.
  * Direct ownership of every source system, domain data service, or customer workflow that the platform integrates with; domain owners remain accountable for source truth, data quality, and business rules.
  * Decommissioning of Databricks Lakebase, MLflow, reporting workflows, or other incumbent data/telemetry systems without a separate migration strategy and acceptance criteria.
  * Replacing human review, compliance approval, or customer-specific policy interpretation with autonomous AI decisions where regulated judgement or accountable signoff is required.
  * Solving every enterprise chat domain in the first platform phase; expansion beyond Benefits should occur through prioritized domain onboarding and measurable reuse.
  * Bespoke one-off experiences that bypass the platform capability registry, tenant model, data-plane contract, telemetry model, or evaluation gates.

## 🏥 Health Metrics (Counter-Metrics)

* **Tenant integrity:** Zero known cross-tenant data access incidents; monitor rejected/invalid tenant-context attempts and scope failures.
* **Answer quality and compliance:** Grounded-answer accuracy, source alignment, compliance/script pass rate, unresolved human-review findings, and regression failure rate.
* **Latency and reliability:** p50/p95/p99 latency, timeout rate, fallback rate, model failover/circuit-breaker events, and APIM/runtime availability.
* **Cost and utilization:** Cost per successful answer, tokens per minute, tokens per request, cached-token impact, retry rate, and high-cost traffic cohorts.
* **Adoption and workflow value:** CSR/member usage, repeat usage, completion rate, turns per session, agent adoption, member/agent satisfaction, and avoidable escalation rate.
* **Platform reuse:** Number of capabilities using the registry, number of domain data planes under contract, onboarding cycle time, and percentage of traffic using platform-standard telemetry/evaluation gates.

## 🧱 Timeline & Milestones

* **Milestone 1: Definition alignment and baseline plan** — June 2026
  * Confirm platform objective, operating model, initial KR measurement owners, and target-setting process.
  * Confirm Kubernetes runtime readiness evidence as one platform proof point without making migration the full platform scope.
* **Milestone 2: Platform contracts and first reusable capabilities** — June 2026
  * Publish initial capability registry, data-plane contract(s), runtime standard, telemetry model, and production readiness gate.
  * Validate Benefits Chat reference flows for Member and CSR use cases.
* **Milestone 3: Expansion readiness and cost discipline** — August 2026
  * Demonstrate repeatable onboarding for additional capabilities/domains.
  * Review cost, latency, quality, compliance, and platform reuse evidence against locked KR targets.
* **Milestone 4: Self-adapting quality and evaluation foundation** — September 2026
  * Establish reusable evaluation harness, source-grounding checks, human-review workflows, and self-adapting baseline recommendations.
  * Validate at least three reference data-plane scenarios.
* **Final Review:** September 2026 - platform maturity review
  * Decide whether Helm is ready for broader domain expansion, customer expansion, and any future customer-facing platform packaging work.
