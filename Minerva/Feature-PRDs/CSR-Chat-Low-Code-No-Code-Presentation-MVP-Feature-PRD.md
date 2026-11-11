# 🧩 Project Name: CSR Chat Low-Code/No-Code Presentation MVP — Shared Presets & CDN SDK

## 🎯 Problem Statement

Stellarus implementers and customer developers need to reuse a branded CSR Chat experience across the hosted standalone app and customer applications without recreating appearance settings or maintaining customer-specific UI forks.

**FACT:** Standalone CSR Chat already supports names, logos, three color profiles, two conversation presentations, and sidebar/footer choices, with browser-local persistence. The existing SDK has managed theme presets and React/Web Component surfaces, but page branding remains host-owned. The inspected sources do not establish one accepted shared presentation release or a production CDN integration path. [Current-state evidence](/Users/jjacks20/jjacks/Conversational-AI/reports/CSR-Chat-Low-Code-No-Code-MVP-Discovery-2026-11-06.md).

**INFERENCE:** Separate configuration lifecycles create repeated setup and visual drift. The MVP addresses this reuse/distribution gap using delivered CSR Chat and existing SDK capabilities.

**Impact:** Repeated branding work and uncertain SDK handoff impede repeatable customer integration. Current setup time and engineering effort are unmeasured; Week 1 must establish them. Historical Mira cost, training, adoption, and disruption targets are not current baselines.

## 💡 Proposed Solution

Deliver a small catalog of **Stellarus-managed, versioned presentation presets** that the standalone app and existing SDK can consume. Publish a production browser-ready SDK release over a CDN, with a documented quickstart and verified customer integration journey.

**Guiding policy:** Configure an existing experience through supported presentation settings. Ship one reusable preset definition with explicit mappings for each surface; preserve existing chat, identity, tenant, plan, and answer behavior.

**Customer journey:** Obtain integration access → load a pinned SDK/CDN release → select an approved preset → connect the documented existing authentication/chat path → render and interact with the assistant.

**Stellarus journey:** Review preset values/assets → validate all supported surfaces → release a version → assign through application configuration → verify → restore the prior version if needed. Preset maintenance may use reviewed files and the existing release process; no new administration screen is required. Live publishing without a release/restart is not promised.

**Meaning of low-code/no-code:** Selecting a released preset needs no customer-specific UI development. Initial SDK integration still requires a developer to wire the documented host, authentication, and transport responsibilities. Customer application go-live is subsequent to this MVP's integration-readiness gate.

## 👥 Target Users

**Primary Users:**

- **Customer application developers:** Need a CDN-loadable SDK, supported preset selection, a working example, and clear integration responsibilities.
- **Stellarus implementation and Apps/SDK maintainers:** Need to release and assign reusable presentation settings without customer-specific application forks.

**Secondary Users:**

- **Customer service representatives:** Receive a consistent branded experience while retaining supported personal display preferences.
- **Design, QA, Customer Success, Support, and Platform:** Approve presentation, verify delivery, and support onboarding and recovery.

## ✅ Success Metrics

Targets below are proposed product acceptance targets. They are not historical performance claims. QA and Product record Week 1 baselines and confirm measurement feasibility before the end of Week 1.

| KPI | Current baseline | Target and measurement window | Owner / evidence |
| --- | --- | --- | --- |
| **M1 — Reusable presentation coverage** | Browser-local standalone settings and a separately managed SDK theme catalog; shared conformance has not been measured. | By Week 4, **two released presets × three surfaces**—standalone, SDK React, CDN Web Component—pass **100% of applicable declared-field and acceptance checks**, with no silent unsupported settings. | Design + QA; field matrix, preset versions, conformance report. |
| **M2 — Customer integration readiness** | Time to first successful external integration is unmeasured; SDK distribution records contain unresolved publication prerequisites. | Before release, **two developers outside the SDK implementation team** independently complete the published CDN quickstart and receive an authenticated supported answer within **four hands-on hours each**, with pre-provisioned access and no undocumented steps. Track the same measure during the first 30 days. | Customer Success + QA; timed rehearsal, support interventions, release/endpoint evidence. |
| **M3 — Repeatable preset assignment** | Current cross-surface assignment time is unmeasured; capture three representative current-state runs in Week 1. | By Week 4, **three consecutive assignments** of an existing approved preset/version across the reference surfaces require **≤30 minutes hands-on effort each**, with **zero customer-specific UI code changes**. Track first 30 days of actual assignments. | Implementation; step/timing log and release references. |

Report elapsed time, provisioning waits, build/deployment waits, and hands-on effort separately. Baseline absence must remain visible; do not claim percentage improvement without a comparable measurement. Any target revision requires Product approval and a recorded rationale.

**Guardrails:** No preset determines tenant access or changes answers; no secrets, transcripts, member/plan data, or private customer configuration in public artifacts. Existing supported chat journeys remain functional. Accessibility and production distribution are launch gates.

## 📦 Scope

| ID | Deliverable and completion boundary | Outcome |
| --- | --- | --- |
| **LCNC-01** | Bounded presentation field catalog: names/labels, approved logos, supported theme tokens, existing display defaults, validation/defaults, surface applicability, and version compatibility. | M1 |
| **LCNC-02** | Two approved presets—Stellarus and an existing customer brand, using approved existing assets—with one maintained definition and review/release instructions. Reuse existing BSC assets/preset where approved. | M1, M3 |
| **LCNC-03** | Standalone consumes an assigned preset/version. Managed branding overrides browser-local branding; existing supported personal display choices retain their documented precedence. Existing demo preferences are not silently migrated or deleted. | M1, M3 |
| **LCNC-04** | Existing SDK React and Web Component consumers select the same preset definition. Document host-owned branding and standalone-only controls; demonstrate host branding in the reference sample. Preserve the existing public authentication/transport contract. | M1, M2 |
| **LCNC-05** | Production CDN publishes a version-pinned browser-ready SDK, stylesheet, and public presentation assets with documented integrity/version information, appropriate delivery headers, and recoverable prior versions. | M2 |
| **LCNC-06** | Customer integration kit: CDN quickstart, React consumption example, preset/field reference, prerequisites, authentication and host responsibilities, errors, compatibility, limitations, and support route. | M2 |
| **LCNC-07** | Release verification: field conformance, browser/accessibility/regression checks, two independent integration rehearsals, three assignment rehearsals, and production authenticated acceptance. | M1–M3 |
| **LCNC-08** | Production rollout/handoff: release identity, preset/SDK versions, safe diagnostics, named operational owners, monitoring, and demonstrated rollback. | M1–M3 |

Full [field boundaries, acceptance examples, dependencies, estimates, and validation plan](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/CSR-Chat-Low-Code-No-Code-Presentation-MVP-Acceptance-and-Delivery.md) are part of this PRD.

**Four-week sequence:**

| Week | Milestone / exit | Accountable role |
| --- | --- | --- |
| **1** | Freeze field/applicability/precedence contract; capture baselines; approve two presets/assets; confirm production CDN and existing chat endpoint owners, onboarding, and delivery dates. | Product + Apps/SDK + Design + Platform |
| **2** | Shared presets work in standalone, React, and CDN sample; versioned release candidate loads in a clean browser; documentation follows the running sample. | Apps/SDK + Platform |
| **3** | Complete conformance, regression/accessibility checks and independent rehearsals; exercise recovery; freeze release candidate with no unresolved launch blocker. | QA + Design + Customer Success |
| **4** | Validate staged release; deploy standalone and publish immutable production CDN version; verify authenticated production path; deliver integration kit and operational acceptance. | Apps/SDK + Platform + QA |

Functional capacity is user-confirmed as available. Estimates and parallel sequencing remain planning assumptions until engineering review; this PRD is not an executed delivery commitment.

**Dependencies and decision triggers:** Reuse existing chat/identity/tenant services. CDN infrastructure [PE-1152](https://linear.app/stellarus/issue/PE-1152) is a delivery dependency. Package-registry work [PE-1153](https://linear.app/stellarus/issue/PE-1153) is optional unless needed by the chosen existing distribution path; it cannot replace CDN delivery. By the end of Week 1, Apps/Platform must evidence the selected production browser-to-chat path and its remaining work. Missing prerequisites trigger an explicit owner/date/impact decision; production, CDN, and customer-readiness requirements cannot silently become a pilot or tarball-only release.

**Confidence:** High in scope clarity and source reuse; medium in four-week delivery feasibility until CDN and authenticated production dependencies are confirmed.

## 🚫 Out-of-Scope

- **New visual administration screens or customer self-service:** Reviewed Stellarus-managed presets satisfy the selected authoring workflow.
- **Prompts, response profiles, benefit interpretation, disclosures, agent/capability selection, data-source bindings, or workflow authoring:** Configuration is appearance/presentation only.
- **New Nexus integration, Nexus API migration, Vermillion redesign, movable/docked panels, or workspace modes:** Separate workstreams; reuse compatible existing assets without making these delivery dependencies.
- **New identity/SSO/tenant/entitlement platforms or ingestion services:** Preserve and validate the selected existing path; escalate gaps rather than absorbing a platform rebuild.
- **New structured-answer renderers, Markdown parity, plan selectors, or standalone page chrome inside the generic SDK:** Existing surface responsibilities remain explicit.
- **A universal theme/layout builder, arbitrary scripts/CSS/HTML, font uploads, unrestricted asset hosting, hot reload, or remote configuration administration:** Keep the preset catalog bounded and versioned.
- **New package-registry launch, framework-specific wrappers, customer production-app go-live, mobile redesign, or new analytics dashboards:** CDN and existing framework-neutral SDK surfaces establish integration readiness.

## 🏁 Exit Criteria

Future implementation is complete only when all checks below pass; PRD review readiness does not assert product delivery.

- [ ] **LCNC-01/02:** Two approved presets have versioned definitions, validated fields/assets, published surface mappings, and no answer/identity/authorization settings.
- [ ] **LCNC-03/04:** Both presets pass every applicable acceptance case in standalone, SDK React, and CDN Web Component/reference host. Unknown IDs/versions, invalid fields, and asset failures have explicit safe outcomes.
- [ ] **LCNC-03:** Managed-brand precedence and legacy-browser preference handling pass; changing appearance does not clear active chat or grant plan readiness.
- [ ] **LCNC-05:** A fresh external-origin browser loads the pinned production SDK/CSS/assets from CDN without a customer build step, private-registry access, undeclared imports, or embedded credentials. Integrity, version immutability, MIME/CORS/CSP guidance, and prior-version recovery are verified.
- [ ] **LCNC-06/07:** Both independent developers complete M2; all three assignment rehearsals meet M3; M1 passes. Actual baseline/target results and interventions are recorded.
- [ ] **LCNC-07:** Supported desktop browsers, keyboard/focus/status behavior, contrast, performance budgets, and existing chat/auth/plan regression checks pass as specified in the supporting acceptance plan.
- [ ] **LCNC-08:** Standalone is deployed to production; the released CDN version and existing authenticated chat path pass production acceptance with approved test data. A download or fixture-only demo does not satisfy this gate.
- [ ] **LCNC-08:** Rollback is demonstrated; monitoring, limitations, integration/support materials, and operational owners are accepted by Product, Apps/SDK, Platform, QA, Design, and Customer Success. Customers have the access instructions and artifacts needed to begin integration.

---

Template Version: `v2.0`  
Feature PRD Skill: `v1.1`  
Historical sources: [Linear extraction](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/Sources/AgentExp-01-Linear-Requirements-2026-11-06.md), [original authored PRD](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/First-Pass/AgentExp-01-Low-Code-Platform-Foundation.md).  
This document is the proposed replacement baseline for this scoped MVP; it does not alter or supersede external Linear records automatically.
