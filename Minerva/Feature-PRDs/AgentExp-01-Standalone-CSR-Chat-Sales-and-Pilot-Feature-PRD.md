# 🧩 Project Name: Standalone CSR Chat Agent Experience — Sales & Customer Pilots

**PDLC Phase:** Definition  

## 🎯 Problem Statement

Sales needs to demonstrate CSR Chat without existing-customer data or prospect-system integrations. New customers need a bounded pilot that proves benefits-answer value quickly. The original foundation couples these goals to embedding, panel customization, and broad low-code administration, adding dependencies before users can experience value.

## 💡 Proposed Solution

One hosted desktop CSR Chat app with an isolated **Sales synthetic environment** and **customer pilot environments**. Sales demonstrates the CSR benefits assistant.

**Guiding policy:** Reuse supported chat and Benefits Service capabilities; configure environments without customer-specific application builds.

- **Sales journey:** Sign in → select synthetic plan → ask approved question → inspect answer/source → reset session.
- **Pilot journey:** Sign in to assigned customer → select approved plan → ask question → inspect answer/limitations/source → submit feedback or use support.

## 👥 Target Users

**Primary Users:** Sales presenters; pilot customer CSRs.

**Secondary Users:** Implementation/Customer Success for setup/support; customer SMEs/Product for answer approval.

## ✅ Success Metrics

| Metric / outcome | Target | Window and evidence |
| --- | --- | --- |
| **M1 — Sales readiness** | Three consecutive synthetic setups ready within 24 hours of complete intake; five presenters independently complete sign-in-to-answer. | Before release and first 30 days; readiness timestamps and journey results. |
| **M2 — Customer activation** | Two distinct customer configurations pass the same onboarding rehearsal without app changes; first signed pilot online within seven calendar days, with inputs pre-staged. | Rehearsals before release; actual launch within first 60 days. Record signature-to-online and complete-input-to-online, including misses. |

**Guardrails:** Zero cross-customer access or real customer/member data in Sales; no pilot PHI. Unsupported questions require safe outcomes. Track conversion as learning.

## 📦 Scope

| ID | Deliverable / completion boundary | Outcome |
| --- | --- | --- |
| CSR-01 | Direct browser workspace: sign-in, plan context, chat, source/details, help; no parent app. | M1, M2 |
| CSR-02 | Supported chat: suggestions, sourced answers, loading/errors, feedback, session reset; plan changes clear prior grounding. | M1 |
| CSR-03 | Managed name/logo/support configuration with validated defaults; same app release across customers. | M1, M2 |
| CSR-04 | Individual product-managed access, verified customer binding, expiration/revocation/sign-out; separate operator permissions. | M1, M2 |
| CSR-05 | Reusable pilot package: customer, users, branding, GA capabilities, dataset/content versions, support and terms; reject invalid activation. | M2 |
| CSR-06 | Intake checklist: approved non-PHI sources/effective dates, assets, users, boundaries, and SME-approved golden cases. | M2 |
| CSR-07 | Setup/handoff runbook, two customer rehearsals, rollback/disable/revoke procedures, support and pilot exit. | M2 |
| CSR-08 | Safe access/query/feedback/setup events with customer/config/data/content versions and correlation IDs; measurement sheet and Sales talk track. | M1, M2 |


**ASSUMPTIONS / dependencies:** Existing chat, Benefits Service, tenancy, synthetic/content packages, and golden-dataset workflow are reusable. Secure managed ingestion remains upstream. Security approves access/retention before invitations; Sales pre-stages inputs and secures a customer; SMEs approve samples. Missing prerequisites trigger replanning, not a platform build.

## 🚫 Out-of-Scope

- SDK/embedding, Nexus/CRM/contact-center integration, floating/docked panels: separate workflow-integration delivery.
- Self-service admin, visual builders, workspace modes, broad theme/layout controls: managed configuration serves initial pilots.
- Customer SSO/federation/SCIM and complex roles: avoid external identity dependencies.
- PHI, claims, eligibility, live accumulators, feeds, new benefit domains: approved non-PHI GA capabilities only.
- Model training, answer-architecture redesign, custom forks, mobile/tablet, enterprise rollout: reuse the desktop product.
- Roadmap previews and customer analytics portals: demonstrate working features; measure internally.

**Risks / decision triggers:**

| Trigger | Mitigation / owner |
| --- | --- |
| Wrong-customer binding or content leakage. | Block activation; Security/Engineering restore approved configuration and rerun checks. |
| Custom requests/manual effort threaten reuse. | Log effort/exceptions; Product reviews after two rehearsals and five setups; scope recurring needs separately. |

## 🏁 Exit Criteria

Future implementation requirements:

- [ ] **CSR-01/02:** Authorized users reach sourced answers directly. Plan change/reset clears prior grounding; missing facts, unsupported topics and service failures produce explicit clarification/decline/recoverable errors without fabricated facts or duplicate retries.
- [ ] **CSR-03/05/07:** Two customer packages resolve correct branding, plans, content and support on one release; incomplete/invalid configurations cannot activate; rollback restores the approved version.
- [ ] **CSR-04/05:** Missing, expired, revoked, unauthorized and wrong-customer sessions expose no protected content. CSRs cannot configure environments; sign-out/expiration clears context; individual accounts need no shared credentials/manual tokens.
- [ ] **CSR-05/06:** Every pilot has non-PHI approval, source/date/version evidence, capability boundaries and SME-approved cases. Stale or misbound data blocks launch; no other-customer fallback.
- [ ] **CSR-01/02:** Supported desktop journey passes WCAG 2.2 AA keyboard/focus/labels/status/contrast checks without blocking clipping. At approved load, p95 completed-answer time ≤15 seconds; visible loading/recovery.
- [ ] **CSR-05/07/08:** Rehearsals retain timing/quality/isolation evidence; rollback/disable/revoke steps pass. Invitations require approved participant limits, duration, use/retention terms, support/incident route, approver and exit steps. Sales/Support accept handoff; events support M1 and M2 without credentials/PHI.
- [ ] **Release:** Acceptance checks, M1 and M2 rehearsals pass; no launch blockers; Product/Engineering/Security/Sales/Customer Success sign off. Assess actual M2 launch within 60 days.

---

Template Version: `v2.0`  
Feature PRD Skill: `v1.1`  
Source relationship: Reduced standalone derivative of AgentExp-01; original retains future embedded/platform scope.
