# CSR Chat Embedded Experience MVP — Acceptance & Delivery Notes

**Revised:** November 16, 2026  
**Status:** READY FOR REVIEW  
**Parent:** [Product PRD](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/CSR-Chat-Low-Code-No-Code-Presentation-MVP-Feature-PRD.md)  
**Purpose:** Define the customer experience, scope boundaries, and evidence required for the four-week MVP. These are future acceptance requirements.

## 1. Confirmed product decisions

| Decision | Confirmed boundary |
| --- | --- |
| Product experience | A ready-to-use chat panel. The surrounding application provides plan selection and other workflow elements. |
| Customer workspaces | Nexus in Vue.js and ShieldAdvisor through Pega Studio are named reference experiences. |
| Supported web environments | React, Angular, Vue, and standard web pages; supported versions and host limitations are documented before release. |
| Initial enablement | A one-time application connection is acceptable. It establishes the existing sign-in/context connections and makes the supported panel configuration controls available. |
| Routine configuration | After connection, configuration requires no code or file editing and no reconstruction of the chat interface. |
| Configuration scope | Appearance/presentation only. Stellarus manages approved presets reused by standalone and embedded experiences. |
| Product administration | Use the connected experience's bounded configuration controls; no new Compass administration portal or universal visual application builder. |
| Delivery | Four weeks to a production product and CDN SDK, with customers able to begin integration. Customer-wide rollout of Nexus or ShieldAdvisor is subsequent. |
| Capacity | Capacity across functions is available, as confirmed by the user. |

**Revision effect:** Product requirements EXP-01 through EXP-07 and experience cases EC-01 through EC-10 replace the earlier LCNC/AC preset-centered requirements in these two artifacts. The previous blanket Nexus exclusion is replaced by Nexus reference acceptance and one-time enablement; host workflow redesign and customer-wide production rollout remain excluded.

The absolute zero-code initial-placement interpretation was clarified by the user: a one-time connection is permitted. Nexus is not assumed to possess a universal visual builder. Pega Studio's exact supported release and authoring environment must be confirmed with the ShieldAdvisor owner; this PRD does not assume a particular Pega design system.

## 2. Product journeys and configuration boundaries

**Experience owner:** Open the connected application's panel settings → choose an approved brand → set the assistant label and an approved display option → preview/apply → verify the next panel launch. The owner can restore an approved prior choice.

**CSR:** Stay in the existing workspace → select a plan through the host workflow → ask a question in the panel → read and follow up → recover from an error or start a new conversation without losing the host's active work.

| Customer choice or responsibility | MVP behavior |
| --- | --- |
| Approved customer branding | Select a Stellarus-managed preset. The release evidence includes two representative approved brand configurations. Creating a new brand or authoring arbitrary themes is outside the routine configuration journey. |
| Assistant label | Set supported presentation text through visible configuration controls, with validation and readable defaults. Labels cannot change answer instructions or required disclosures. |
| Display preference | Select an approved existing color/theme or panel display option offered by the released configuration. The reference journeys must expose a usable choice; a configuration-file workaround does not satisfy M1. |
| Apply and restore | Changes are validated and saved with clear success/failure feedback. They may take effect on the next panel launch; live theme publishing into an active conversation is unnecessary. A failed change preserves the prior working choice. |
| Sign-in and selected plan | Supplied by the host through the one-time approved connection. Presentation settings cannot select permissions, replace identity, or alter benefit-answer behavior. |
| Plan changes or loss of access | Follow the existing chat/context safeguards. Clearly show when the panel needs valid context; do not answer using an earlier plan silently. |
| Host workflow and layout | Host supplies its own plan selector, page navigation, customer/case records, and surrounding work. The panel fits its allocated area. |
| Standalone compatibility | Reuse approved presentation choices where supported. Standalone-only page settings do not become new embedded-panel features. Existing supported standalone journeys remain available. |

The panel's core scope includes question entry, response display, conversational follow-up, progress/error feedback, and starting a new conversation. Existing service content, including source information when supplied, must remain readable. The MVP does not require a new answer-generation capability, a universal response renderer, or reproduction of every standalone page control.

The one-time connection is a customer prerequisite supported by the released product and guidance. It is not repeated for routine appearance changes. After enablement, editing JavaScript, CSS, JSON, or another source/configuration file to make a routine change fails the no-code acceptance criterion. A standard host settings-save/publish action is acceptable.

## 3. Experience acceptance and traceability

| Case / requirements | Given / When / Then | Evidence |
| --- | --- | --- |
| **EC-01 · EXP-01/02** | **Given** an authorized user and a host-selected valid plan, **when** the CSR opens the connected panel and asks a supported question, **then** the panel presents the response, supports follow-up, and retains the host's active work. | Observed panel journey in the supported host environments. |
| **EC-02 · EXP-02/06** | **Given** missing, changed, or unauthorized context, **when** a question is attempted, **then** existing context protections apply and the CSR sees an actionable safe state. A stale plan must not silently ground a new interaction. | Success, plan-change, missing-context, and access-denial scenarios. |
| **EC-03 · EXP-03/04** | **Given** the completed one-time connection and an authorized experience owner, **when** the owner changes the approved brand, assistant label, and supported display preference, **then** the correct choices appear through the supported configuration journey without code/file editing or rebuilding the interface. | M1 task observations and saved/visible values. |
| **EC-04 · EXP-03/04** | **Given** invalid or unavailable settings, **when** a change is applied, **then** clear feedback explains the failure and the prior approved choice remains recoverable. Missing optional images use the documented neutral fallback; an unknown brand cannot become another customer's brand silently. | Invalid-choice, save-failure, missing-asset, and restore cases. |
| **EC-05 · EXP-01/05** | **Given** a supported React, Angular, Vue, or standard web environment, **when** the common panel journey is exercised, **then** the same supported question/response, follow-up, context, and recovery outcomes work without recreating the chat UI. | Four-of-four environment acceptance matrix with supported versions. |
| **EC-06 · EXP-03/05** | **Given** approved Nexus and ShieldAdvisor test environments with their one-time connections complete, **when** an experience owner configures and opens the panel, **then** the supported no-code choices and ready-to-use panel work within each workspace. | Two host-owner acceptance records; supported Vue and Pega environment details. |
| **EC-07 · EXP-01/06** | **Given** an active host task and a chat conversation, **when** the CSR follows up, encounters an error, starts a new conversation, or resizes the available panel area, **then** controls remain usable and the host's active work is preserved. Applying choices for a future panel launch does not interrupt the current conversation. | M2 observations plus state-preservation checks. |
| **EC-08 · EXP-05/06** | **Given** every released brand/display variant, **when** exercised by keyboard and with supported desktop sizing/zoom, **then** focus, labels, status/error messages, contrast, and response readability meet the agreed accessibility criteria. | Accessibility review and checks across the released variants. |
| **EC-09 · EXP-04/07** | **Given** the approved release, **when** customers access the production product and CDN offering, **then** the supported panel and presentation choices are available with connection prerequisites, compatibility limits, and configuration guidance. The authenticated production smoke journey succeeds. | Production release/CDN availability and authenticated acceptance record. |
| **EC-10 · EXP-03/07** | **Given** a working approved configuration and a later defective release/change, **when** the documented recovery is performed, **then** service is restored to the prior approved combination and Support can identify the active product and configuration versions. | Configuration restore and product-release recovery rehearsal; support handoff. |

**Traceability:** M1 is proved by EC-03/04/06/10; M2 by EC-01/02/05/06/07/08. EC-09/10 establish production and operational readiness. All seven EXP requirements have acceptance coverage.

### Quality boundaries

- Validate current supported desktop Chrome and Edge, retaining any additional existing contractual support. Record supported framework, host, and Pega versions; generic web compatibility does not establish every Pega deployment as supported.
- Changed experiences meet WCAG 2.2 AA, including keyboard/focus, accessible names, status announcements, text/control contrast, and usable 200% zoom in the assigned panel area.
- Proposed responsiveness target: once approved assets and host context are available, the panel is usable within two seconds at p95 on the agreed desktop test profile. Record first-load and chat-answer latency separately; do not represent this as a new answer-service SLA.
- Existing chat, authentication, plan-context, and standalone behavior pass applicable regression checks. Theme/label changes cannot grant access, change answers, or discard the host's active work.
- Shared panel settings use the connected application's existing configuration permissions. A CSR without configuration permission cannot change shared choices; an authorized experience owner can. No new identity/role platform is required.
- Production distribution includes version compatibility, reliable loading, and recovery. Public presentation assets contain no private customer or conversation data.
- Product events/observations identify panel readiness, configuration success/failure, supported environment, and released version without capturing conversation contents or credentials. Use existing measurement/monitoring capabilities.
- Engineering owns implementation strategy and maps the experience requirements to behavior contracts and applicable automated validation before production changes. This PM artifact reports no completed product test or deployment.

## 4. Measurement and delivery

### Measurement rules

**M1:** Recruit five representative experience owners. After the one-time connection, each selects an approved brand, changes an assistant label, and selects a supported display preference. Success means the correct result is visible through the supported apply/next-launch journey within ten minutes, independently and without code/file editing. At least 14 of the 15 tasks must pass. Log every failure and intervention; do not remove failed attempts from the denominator.

**M2:** Five representative CSRs each perform four tasks in both reference workspaces: ask with the selected plan, follow up, recover from a service error, and start a new conversation. At least 36 of 40 tasks must succeed independently without opening standalone chat or losing the host's active work. The host's normal plan-selection steps remain part of the surrounding workflow.

Week 1 captures comparable current journeys before implementation, including unsuccessful attempts, task time, tool switching, and interventions. No numeric baseline or percentage improvement is asserted until observed. Product confirms target feasibility at the end of Week 1; any revision retains the original target and rationale. Repeat observation during the first 30 days after first customer activation; this follow-up does not delay the four-week release.

### Sequencing, ownership, and estimates

| Week | Product exit | Accountable roles |
| --- | --- | --- |
| **1** | Approve journeys and bounded choices; baseline current tasks; confirm access, supported host versions, connection prerequisites, and release dates. | Product + Design; Engineering/host owners supply feasibility evidence. |
| **2** | Connected panel and no-code configuration work in the compatibility environments; demonstrate Nexus and ShieldAdvisor paths. | Engineering + host owners; Product/Design assess the experience. |
| **3** | M1/M2 UAT, accessibility and compatibility checks pass; recovery works; launch blockers are resolved. | Product + QA + Design + Customer Success. |
| **4** | Production product/CDN release and authenticated acceptance pass; customer and support guidance are ready. | Engineering + Platform + QA; Product accepts readiness. |

Indicative work-package sizing for engineering review: EXP-01 3–5 owner-days; EXP-02 2–4; EXP-03 2–3; EXP-04 3–5; EXP-05 2–4; EXP-06 2–3; EXP-07 3–5. These are **planning assumptions**, totaling 17–29 owner-days across parallel work, not completed estimates or a staffing commitment. Split any package that engineering finds exceeds five days. Existing product reuse and user-confirmed cross-functional capacity support parallel delivery.

### Dependencies and decision triggers

| Dependency / risk | Owner and needed-by | Trigger and response |
| --- | --- | --- |
| Nexus and ShieldAdvisor test access, supported versions, and configuration mechanisms | Host owners + Engineering; confirmed in Week 1, usable for Week 2 demonstrations. | If unavailable, escalate the impact on reference acceptance immediately. A generic framework demonstration cannot silently replace a named-host acceptance requirement. |
| Approved sign-in, plan-context, and existing chat service availability | Host/Platform/Engineering; Week 1. | Missing connections require an explicit resolution plan; presentation configuration cannot bypass them. |
| Approved brand choices and representative UAT participants | Product + Design + Customer Success; Week 1. | Resolve missing approvals/access before Week 3; distinguish user-capacity commitments from actual environment readiness. |
| Production distribution and customer access | Platform + Engineering; ready for Week 4 acceptance. | CDN download alone cannot establish usable customer integration. Verify the authenticated panel journey and supported configuration. |
| Routine configuration still needs files or application changes | Product + Design + Engineering; assess during Week 2 demonstration. | Treat as an in-scope defect against EXP-03, not a documentation workaround. |
| Pressure to add new host workflows, assistant behavior, or a universal builder | Product; throughout. | Preserve the agreed panel boundary; any material expansion needs an explicit scope/timebox decision. |

**Release owners:** Product accepts outcomes; Design accepts usability/accessibility; Engineering and Platform own compatibility, release, and recovery; QA owns evidence; Customer Success/Support accept guidance. Named responsible owners and target host versions are recorded at kickoff.

**Confidence:** High in product-scope clarity; medium in the delivery forecast until the Week 1 host and production prerequisites are evidenced.

## 5. Product choices and source evidence

| Alternative | Choice and tradeoff |
| --- | --- |
| Standalone chat as the only experience | Retain the existing product, but this alone does not meet the in-workspace need. |
| Ready-to-use panel with one-time connection | Selected by the user. Reuses chat capabilities while allowing the customer to keep its plan selection and surrounding workflows. |
| Recreate complete host workflows in the panel | Excluded by the user; would duplicate the host and expand scope. |
| Require zero application work for initial placement in every environment | Superseded by the user's explicit one-time-connection allowance. Ongoing configuration remains no-code. |
| Lead with presets and SDK handoff | Superseded as the product framing. Presets and distribution support the customer experience; they are not the user problem. |
| Build a universal visual application builder | Excluded. Supported host configuration is enabled through the one-time connection and bounded panel choices. |

**Facts:** User decisions establish the intended panel, host responsibilities, named experiences, compatibility set, one-time connection, configuration limits, and release boundary. The current SDK guide documents existing controlled panel/theme capabilities.  
**Inference:** A reusable embedded panel can reduce tool switching and repeated experience work; UAT and first-customer measurement must validate this.  
**Assumptions:** Approved host environments can be made available in time; the existing sign-in/plan/chat capabilities are reusable; proposed metric and sizing targets are feasible. Week 1 owners validate these assumptions.

Sources:

- [November 6 discovery and historical source reconciliation](/Users/jjacks20/jjacks/Conversational-AI/reports/CSR-Chat-Low-Code-No-Code-MVP-Discovery-2026-11-06.md). Tracker observations there remain dated November 6; they are not asserted as current release status.
- [Linear source extraction](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/Sources/AgentExp-01-Linear-Requirements-2026-11-06.md) and [original authored requirements](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/First-Pass/AgentExp-01-Low-Code-Platform-Foundation.md).
- [Existing SDK panel, theme, and host responsibilities](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/packages/chat-client/README.md:63).
- [Existing standalone settings](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/apps/csr-demo-ui/src/app/settings/page.tsx:109).
- [Pega's component authoring guidance](https://docs.pega.com/bundle/constellation-dx-components/page/constellation-dx-components/custom-components/configure-component-app-studio.html). This is a platform reference, not proof of ShieldAdvisor's installed environment or readiness.

**F:** The product PRD and these supporting notes are revised in place; historical source documents remain intact.  
**T:** November 16 artifact validation passed: seven template sections, seven product requirements, ten Given/When/Then cases, two customer-outcome metrics, four weekly milestones, and ten local links with valid source-line references. Customer-role framing and all confirmed scope boundaries were checked. Product implementation tests remain future delivery requirements.  
**C:** The revision centers CSRs and customer experience owners, retains the approved product/release constraints, and incorporates the user's one-time-connection clarification.  
**O:** Interactive decisions, local source review, official Pega documentation research, Markdown edits, and document validation support the revision.
