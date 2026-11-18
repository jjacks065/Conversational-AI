# 🧩 Project Name: CSR Chat — Low-Code/No-Code Embedded Experience MVP

**PDLC Phase:** Build & Integrate  

## 🎯 Problem Statement

Customer service representatives need CSR Chat assistance within the workspace they already use to serve customers. Customers need to add a ready-to-use chat panel to that workspace and adapt its appearance without recreating the chat experience or requesting application changes for routine configuration. The CSR Chat panel must integrate with existing customer service desktop experiences (eg. Nexus and Shield Advisor at Blue Shield of California) built on React, Angular, Vue, and standard web technolgies. The surrounding application continues to provide plan selection and its other workflows.

**Impact:** A reusable, configurable panel lets customers introduce CSR Chat within familiar workflows and gives representatives a consistent way to ask questions and read responses. Reduced tool switching and configuration effort are product hypotheses to validate; current customer task-completion and configuration-time baselines have not been measured.

## 💡 Proposed Solution

Deliver a ready-to-use CSR Chat panel that customers can add to a supported experience once, then configure without code.

An authorized experience owner selects an approved brand, assistant label, and supported presentation options through the connected application's configuration controls. A representative uses the panel alongside the application's existing work, asks a question using the supplied plan context, reads the response, and continues the conversation.

**Low-code/no-code boundary:** A one-time application connection is permitted, including the existing sign-in and plan-context connections. After that connection, routine panel configuration requires no source-code or configuration-file editing and no rebuilding of the chat interface. The one-time connection must make the supported configuration controls available.

**Product approach:** Reuse the delivered standalone CSR Chat and existing SDK. Stellarus manages approved presentation presets shared across standalone and embedded experiences. The customer application supplies plan selection, identity, and surrounding workflow; the panel supplies its existing supported conversation experience.

The four-week release delivers the product to production, makes its SDK available through the CDN, and enables customers to begin integration. Nexus and ShieldAdvisor are reference experiences for acceptance; their customer-wide production rollouts are separate.

## 👥 Target Users

**Primary Users:**

- **Customer service representatives:** Need accessible chat assistance within their current workspace while retaining their existing customer-service context.
- **Customer experience owners:** Need to select the panel's approved branding and presentation options without code after the application is connected.

**Secondary Users:**

- **Customer business owners and supervisors:** Need a consistent assistant experience across supported customer-service applications.
- **Customer Success and Support:** Need clear setup prerequisites, supported configuration choices, and recovery guidance.

## ✅ Success Metrics

These are proposed product targets. Establish baselines in Week 1; assess the targets before release and repeat measurement during the first 30 days after the first customer activation.

| Outcome | Baseline | Target | Measurement / owner |
| --- | --- | --- | --- |
| **M1 — Configure without code** | Current completion rate and time are unmeasured. Observe the closest current configuration journey in Week 1. | Five representative experience owners complete three routine configuration tasks each. **At least 14 of 15 tasks** are correct within **10 minutes per task**, without code/file editing or assistance. | Observed selection of an approved brand, assistant label, and display option after connection; Product + Design. |
| **M2 — Complete work within the host experience** | Current completion rate and need to leave the workspace are unmeasured. Capture the existing representative journey in Week 1. | Five representative CSRs complete four supported chat tasks in each of the two reference experiences. **At least 36 of 40 tasks** succeed independently, without opening standalone CSR Chat or losing the host's active work. | Ask, follow up, recover from an error, and start a new conversation; moderated UAT and first-activation observation; Product + Customer Success. |

**Release guardrails:** All four supported web environments pass the common experience criteria. Branding choices do not change answers or access permissions. Existing chat quality, accessibility, and plan-context protections remain intact.

## 📦 Scope

| ID | Product capability / completion boundary | Outcome |
| --- | --- | --- |
| **EXP-01** | **Ready-to-use chat panel:** Existing question entry, response display, conversation state, loading/error feedback, and conversation controls are available without rebuilding the interface for each application. | M2 |
| **EXP-02** | **Use the surrounding workflow:** After the one-time connection, the panel uses the host's approved sign-in and selected-plan context. Missing or changed context produces a clear, safe state. Plan selection remains in the host. | M2 |
| **EXP-03** | **Configure without code:** Authorized experience owners select an approved brand, assistant label, and supported display options through the connected application's configuration controls. Valid changes can be applied and restored without application source changes or a chat-interface rebuild. | M1 |
| **EXP-04** | **Consistent customer identity:** Stellarus-managed presentation presets work across standalone and embedded experiences. Available choices, defaults, and supported differences are explicit. | M1, M2 |
| **EXP-05** | **Supported experience compatibility:** The same product capabilities work in React, Angular, Vue, and standard web pages. Nexus and ShieldAdvisor demonstrate the intended customer experience in approved test environments. | M1, M2 |
| **EXP-06** | **Fit the existing workspace:** The panel fits its assigned area, supports accessible interaction, and preserves the surrounding application's active work during chat and appearance changes. | M2 |
| **EXP-07** | **Production availability and customer readiness:** Production standalone product and CDN SDK are available with supported connection/configuration guidance, compatibility boundaries, support, and recovery procedures. | M1, M2 |

**Four-week delivery sequence:**

| Week | Product milestone |
| --- | --- |
| **1** | Confirm supported host environments and connection prerequisites; capture baselines; approve panel/configuration journeys, presentation choices, and acceptance scenarios. |
| **2** | Make the connected panel and no-code configuration usable across the supported web environments; demonstrate the Nexus and ShieldAdvisor paths. |
| **3** | Complete experience-owner and CSR UAT, accessibility and compatibility validation; resolve blockers and validate recovery. |
| **4** | Deploy the shared product to production, publish the CDN SDK, verify customer integration readiness, and accept support handoff. |

Capacity across functions is confirmed as available. Access to the reference host environments, their configuration controls, existing chat services, and production distribution are delivery dependencies.

**Confidence:** High in the clarified product scope; medium in the four-week forecast until host/environment prerequisites are confirmed in Week 1. Missing prerequisites require an explicit delivery decision rather than reducing the promised outcome silently.

The [supporting acceptance and delivery notes](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/CSR-Chat-Low-Code-No-Code-Presentation-MVP-Acceptance-and-Delivery.md) define configuration boundaries, acceptance examples, alternatives, dependencies, and measurement rules.

## 🚫 Out-of-Scope

- **Recreating the complete host workflow:** Plan selection, customer records, case management, and other surrounding work stay with the application.
- **Assistant-behavior authoring:** No prompt, benefit-rule, answer-profile, agent, data-source, or workflow configuration.
- **A new visual application builder or Compass administration portal:** Expose the panel's bounded choices through the connected experience.
- **Unrestricted design tools:** No arbitrary scripts, page-layout builder, new floating/docking system, or customer-created components.
- **Host-product redesigns and customer-wide production rollouts:** No Nexus workflow migration, ShieldAdvisor business-process redesign, or mandatory redesign-system adoption.
- **New identity platforms or benefit domains:** Reuse existing approved platform capabilities.
- **Universal compatibility:** The promise applies to the documented supported framework and host versions; other environments require validation.

## 🏁 Exit Criteria

- [ ] **EXP-01/02:** The panel completes the supported chat journey with host-supplied context; unavailable, changed, or unauthorized context produces the expected safe outcome.
- [ ] **EXP-03/04:** M1 passes. Routine configuration uses visible supported controls and requires no code/file editing or interface rebuild after the one-time connection.
- [ ] **EXP-04/05:** Shared branding and the common chat capabilities pass in React, Angular, Vue, and standard web pages, with host-specific limits documented.
- [ ] **EXP-05/06:** Nexus and ShieldAdvisor reference acceptance and M2 pass in approved test environments; accessibility and preservation of host work are demonstrated.
- [ ] **EXP-07:** The shared product is deployed to production, the SDK is available over the CDN, and an authenticated production smoke check demonstrates readiness for customer integration.
- [ ] **EXP-07:** Connection/configuration guidance, measurement evidence, release/support ownership, and demonstrated recovery are accepted by Product, Design, Engineering, Platform, QA, and Customer Success.

---

Template Version: `v2.0`  
Feature PRD Skill: `v1.1`  
Source history: [Linear requirements extraction](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/Sources/AgentExp-01-Linear-Requirements-2026-11-06.md), [original authored PRD](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/First-Pass/AgentExp-01-Low-Code-Platform-Foundation.md). Product decisions confirmed November 16 govern this revision.
