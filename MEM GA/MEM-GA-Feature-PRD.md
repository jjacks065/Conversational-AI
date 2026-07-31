# 🧩 Project Name: MEM GA (Member Engagement Model Generative Agent) Pilot

**PDLC Phase:** Discovery
**Updated Date:** March 23, 2026
**Status:** DRAFT

## 🎯 Problem Statement

BSC members struggle to get timely, accurate answers to benefits questions, leading to frustration, multiple touchpoints, and increased support costs. Current member portal interactions lack personalized guidance, forcing members to navigate complex benefits documentation or call into customer service to answer these basic benefits questions.

**Impact:** Member satisfaction suffers due to inefficient benefits information access, while customer service costs increase from high-touch support requirements for routine benefits inquiries.

## 💡 Proposed Solution

Deploy an AI-powered Generative Agent chat integrated with the member portal that provides instant, personalized benefits support directly within members' existing digital experience. The MEM GA will leverage member data to deliver contextual responses about their benefits.

## 👥 Target Users

**Primary Users:**

* **BSC Members (Employees):** Blue Shield CA employees with BSC insurance coverage seeking benefits information and support
* **Post-pilot will include additional BSC Members (Future LOBs):** Members across Individual/Family Plans, Small Business, Core Premier lines

**Secondary Users:**

* **Customer Service Representatives:** Support agents who receive escalated inquiries when chat cannot resolve member questions
* **Operations Leaders & Workforce Managers:** Monitor service performance, accuracy trends, and quality metrics to ensure efficient operations.

## ✅ Success Metrics- WIP/REVISIT

How will we measure success? Core KPIs covering user engagement, operational efficiency, and business impact:

- **Compliance:** 100% compliance with required disclosures and prohibited‑phrase rules.
- **User Adoption and Engagement:** TBD
- **Operational Efficiency:** Maintain <TBD% escalation rate from MEM GA to customer service (target: <TBD% of total chat sessions require human handoff)
- **Member Satisfaction:** TBD
- **Business Impact:** Process 15[?]% of total benefits page traffic through MEM GA (~1,425 daily sessions from current 9.5k daily benefits page sessions)
- **Accuracy:** ≥95%
- **Latency:** ≤ 15 seconds p95 latency for to generate a response
- **Containment rate** ≥70% (initial # from MEM- need to make sure this is realistic)

## 📦 Scope

What's included in this Pilot release?

- **AI Conversational Interface:** Natural language chat interface integrated with member portal and Genesys
- **Benefits use cases:** Core benefits support covering foundational questions, plan details, and educational content
- **Data source- still TBD which one:**
  - **Member Data Integration:** Nexus JSON integration providing personalized responses using member name and plan information
  - **Files:** Plan documents loaded directly into Sierra.
- **Escalation Workflow:** Seamless handoff to customer service teams with full conversation context
- **Analytics & Monitoring:** Real-time performance tracking, conversation transcripts, and feedback collection system
- **BSC Employee Pilot:** Limited rollout to Blue Shield CA employees with BSC insurance coverage
- **Data retention:** 7 years?
- **Reporting:**

## 🚫 Out-of-Scope for Pilot launch

What's explicitly excluded from Pilot?

- **Anything outside of benefits, such as:**
  - **Claims Processing Support:** Claims inquiries, status checks, and claims-related actions (planned for future iteration)
  - **Billing & Account Management:** Payment processing, account updates, billing inquiries (separate product roadmap)
- **Multi-LOB Launch:** IFP, Small Business, Core Premier will have a phased rollout post-pilot
- **Advanced Personalization:** Behavioral recommendations beyond name and plan data (future enhancement)
- **[TBD Mobile App Integration:** Native mobile app implementation (portal web interface only for MVP)
- **Voice Integration:** Speech-to-text or voice responses (chat interface only)

## 🏁 Definition of Done

Task list defining when MEM GA implementation would be considered complete:

* [ ] **Core Functionality Delivered:** MEM GA chat interface successfully integrated with member portal, responds to benefits questions using Nexus data, and handles member authentication through Genesys
* [ ] **Pilot Group Onboarded:** 100% of BSC employees with BSC insurance have access to MEM GA through member portal with training materials provided
* [ ] **Success Metrics Instrumented:** Analytics tracking operational for all defined KPIs with baseline measurements established and real-time monitoring dashboard deployed
* [ ] **Quality Assurance Completed:** All integration tests passing, security validation complete, customer service escalation workflow tested and operational
* [ ] **Operational Readiness Achieved:** Customer service teams trained on MEM GA escalation handling, 7-year transcript storage system operational, separate dev/QA/test/prod environments deployed and validated
* [ ] **Pilot Launch Criteria Met:** End-to-end system testing completed with >95% uptime over 1-week testing period, stakeholder sign-off received from BSC customer experience, Nexus, and enterprise architecture teams

---

**Evidence:**
F: [MEM_GA_Project_Plan.md](MEM_GA_Project_Plan.md), [Context.md](Background/Context.md), [Feature-1-Pager-PRD.md](../../Agentic-PM/templates/Feature-1-Pager-PRD.md)
T: Information validated against existing project documentation and skill methodology
C: Applied feature-prd skill v1.0 framework with 6-phase structured approach
O: Implementation-ready PRD with measurable success criteria and 20-25 week delivery timebox
