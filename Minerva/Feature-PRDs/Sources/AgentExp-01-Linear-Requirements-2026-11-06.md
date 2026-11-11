# Linear source extraction: Agent Experience: Low-Code/No-Code UI Foundation & Configuration Framework

- Retrieved: 2026-11-06 (America/Los_Angeles session date).
- Source: https://linear.app/stellarus/document/agent-experience-low-codeno-code-ui-foundation-and-configuration-7ef5e9915240
- Document ID: 8c1b1371-43ce-4bb7-9b95-8b1b88962aad; slug: 7ef5e9915240.
- Created: 2026-05-04T22:57:27.223Z; last updated at retrieval: 2026-11-06T22:50:33.006Z.
- Author / latest updater: Jason Jackson / Jason Jackson.
- Project: No-Code/Low-Code CSR Chat (fc93fc25-3b79-4235-8403-21297f9a5c06).
- Purpose: historical source snapshot for the new four-week MVP PRD. This snapshot is not an approved current requirements baseline.
- Extraction: title promoted to a heading below; source Markdown, including strikethrough and inline Linear comment markers, is preserved without editorial correction. Comment bodies are not included in the document response.

---

# Agent Experience: Low-Code/No-Code UI Foundation & Configuration Framework

**PDLC Phase:** Define
**Authored Date:** April 29, 2026
**Status:** DRAFT

---

## 🎯 Problem Statement

Current Mira UI creates experience challenges through fixed positioning, full-screen takeovers, and inflexible interface patterns that disrupt agent workflows during live calls. Each customer deployment requires custom development, complicatin cost of ownership and requireing slow and coordinated deployment cycles. Agents need a contextual, adaptable interface that integrates seamlessly with existing workflows while enabling customer-specific branding, layout, and configuration with minimal to no engineering effort.

**Impact:** Poor UX contributes to lack of stickiness and evidence of agents reverting back to legacy tools, reducing ROI on Minerva investment and preventing cost-per-query optimization through scale. Custom UI development creates unsustainable per-customer costs ($50K-100K per deployment) and slow onboarding cycles (weeks instead of days).

**Evidence from UX Evaluation:**

* "Full-screen takeover disrupts context at start of live call" (P0 Priority)
* "Fixed placement blocks key benefit fields and prevents side-by-side verification" (P1 Priority)
* Agent quote: "I'd prefer to go back to how you had it a moment ago, so I could be looking \[in Nexus\] while I'm waiting"
* Agent quote: "I was hoping we'd be able to kind of move it around the screen… but it stays on the right side"

---

## 💡 Proposed Solution

Deliver a **Low-Code/No-Code CSR Chat UI Foundation** that establishes CSR Chat as a configurable user experience with white-label capabilities, contextual panel architecture, and configurability. Enable rapid multi-customer or LOB deployment with customer-specific branding, layout preferences, and integration patterns limited engineering involvement.

**Key Components:**

1. **Contextual Panel Architecture:** Movable, resizable, non-modal interface that maintains workflow context
2. **White-Label Branding Framework:** Customer-specific theming and terminology without code changes
3. **Integration SDK:** Framework for embedding CSR Chat in customer applications (Nexus, etc.)
4. **Agent Workspace Management:** Personalized layouts within customer-defined guardrails

---

## 👥 Target Users

**Primary Users:**

* **Contact Center Agents:** Need contextual, flexible interface that integrates seamlessly with existing workflows during live member calls
* **Customer Deployment Teams:** Need ability to apply customer-specific branding, terminology, and styling, and configurations.

**Secondary Users:**

* **Minerva Product Team:** Benefits from reduced custom development costs and faster customer deployment cycles
* **Stellarus Customer Success Teams:** Can deploy and configure customer environments independently

---

## ✅ Success Metrics

### Agent Experience Metrics

* **Workflow Disruption:** Reduce agent workflow disruption by 60% (measured via user session analysis and time-to-task metrics)
* **Agent Satisfaction:** Workflow integration satisfaction >4.0/5 (measured through surveys or focus groups)

### Customer Deployment Metrics

* **Configuration Adoption:** >80% of customers utilize white-label customization within 30 days of deployment
* **Support Reduction:** Support tickets for UI-related issues reduced by 50% compared to Mira baseline

### Training & Adoption Metrics

* **Training Efficiency:** Agent onboarding time reduced by 50% (target: <2 hours to proficiency)
* **Feature Discovery:** >70% of agents discover and use movable/resizable panel features within first week

---

## 📦 Scope

**What's included in this release?**

### ~~A. Contextual Panel Architecture (Addresses P0/P1 UX Issues)~~

* <linear-comment id="7d19cc80-5c0e-44c0-a0a5-3e068a16cedd" resolved="false">~~Modal/Non-Modal configuration with floating panel that maintains context with underlying application (eg. Nexus, customer applications)~~</linear-comment>
* <linear-comment id="7d19cc80-5c0e-44c0-a0a5-3e068a16cedd" resolved="false">~~Movable panel with drag-to-reposition capability preserving spatial memory across sessions~~</linear-comment>
* <linear-comment id="7d19cc80-5c0e-44c0-a0a5-3e068a16cedd" resolved="false">~~Resizable width with agent preference persistence (supports narrow vertical scanning and wide horizontal reading)~~</linear-comment>
* <linear-comment id="7d19cc80-5c0e-44c0-a0a5-3e068a16cedd" resolved="false">~~Collapsible/expandable states with discoverable affordances (tooltips, first-run coachmarks)~~</linear-comment>
* <linear-comment id="7d19cc80-5c0e-44c0-a0a5-3e068a16cedd" resolved="false">~~Multiple docking positions: right-sidebar (default), left-sidebar, bottom-panel, floating~~</linear-comment>

~~**White-Label Configuration:**~~

* ~~Customer-defined default position, size, and docking behavior~~
* ~~Responsive layout adaptation based on customer application constraints~~

### B. White-Label Branding & Theming Framework

**Visual Identity:**

* Custom logo, product name, and iconography
* Brand color palette (primary, secondary, accent colors)
* Typography system (font families, weights, sizes)
* Light/dark theme variants with automatic contrast compliance

**Layout Customization:**

* Header/footer customization (show/hide, content, links)
* Panel chrome styling (borders, shadows, spacing)

**Terminology & Language:**

* Customizable product name ("CSR Chat", "Mira", customer-preferred naming)
* Help text and guidance customization per customer vocabulary

**Technical Implementation:**

* CSS custom property system for theme injection
* JSON-based configuration schema for customer branding packages
* Real-time theme switching without deployment (hot-reload capability)

### C. Low-Code Configuration

**Configuration Domains:**

1. **Interface Layout Configuration:** Default panel size, position, docking behavior; agent customization permissions; responsive breakpoint behavior; integration target specification
2. **Behavioral Configuration:** Auto-collapse settings; keyboard shortcuts; session persistence behavior; performance optimization settings
3. **Integration Configuration:** Parent application integration method; SSO/authentication parameters; deep-linking rules to customer source systems
4. **Feature Enablement:** Granular feature flag control; progressive rollout support; role-based access control

### D. Customer Integration & Workflow Preservation

* Side-by-side panel display maintaining container application content visibility
* Contextual awareness of customer application state (eg. current plan, member, benefit section)
* Synchronized scrolling and highlighting for verification workflows

**Customer Application Integration SDK:**

* JavaScript SDK for embedding CSR Chat in any web application
* React, Angular, Vue component libraries for framework-specific integration
* Message passing API for parent-child application communication
* Responsive container API for dynamic resizing based on parent constraints

## 🚫 Out-of-Scope

**What's explicitly out of scope?**

* Contextual Panel Architecture
* Advanced multi-language localization
* Complex role-based access control beyond basic agent/admin
* Mobile/tablet responsive design
* Integration with non-Nexus customer systems beyond generic SDK (Phase 2)
* Advanced configuration analytics and usage dashboards
* Custom UI component development per customer

---

## 🔗 Dependencies & Risks

### Critical Dependencies

* **Minerva API Stability:** Requires stable query processing API for consistent UI integration
* **Nexus API Access:** Requires deep-linking API documentation and SSO integration specifications for Blue Shield of California
* **Customer SSO/Authentication:** Requires customer identity provider integration specifications (Okta, Azure AD, etc.)

### Key Risks

**Risk 1: Configuration Complexity Overwhelming Self-Service Value**

* **Impact:** High - Could undermine rapid deployment goals and cost savings if admin portal too complex
* **Mitigation:** Progressive disclosure in 
* 
*  template-based configuration with sensible defaults; expert support services tier for complex scenarios; iterative testing with customer admin users

**Risk 2: Browser Compatibility Issues**

* **Impact:** Medium - Panel positioning/sizing may behave inconsistently across browsers and versions
* **Mitigation:** Standards-based CSS implementation; comprehensive browser testing matrix (Chrome, Firefox, Safari, Edge); graceful degradation for older browsers; clear browser support policy

**Risk 3: Performance Overhead from Configuration**

* **Impact:** Medium - Could jeopardize <15 second response time targets if configuration processing adds latency
* **Mitigation:** Configuration caching strategy; lazy loading of configuration; client-side configuration rendering; performance budgets for configuration processing; monitoring and alerting

**Risk 4: Agent Adoption During Transition**

* **Impact:** High - Agents may resist interface changes during transition from Mira
* **Mitigation:** Phased rollout approach; parallel Mira support during transition; agent champions program; comprehensive change management and training; continuous feedback collection

---

## 🏁 Definition of Done

**Task list of statements that define when implementation of this PRD would be considered complete:**

- [ ] ~~Contextual panel architecture functional: movable, resizable, non-modal, multiple docking positions working across major browsers~~
- [ ] Agent preference persistence working: panel position, size, workspace mode saved across sessions
- [ ] White-label theming operational: customer logo, colors, product name configurable and rendering correctly
- [ ] ~~Low-code configuration admin portal (MVP) deployed: visual configuration builder with live preview, validation, and save functionality~~
- [ ] Nexus side-by-side integration working: CSR Chat panel maintains Nexus context visibility and supports parallel workflows
- [ ] Customer Application Integration SDK functional: JavaScript SDK enables embedding in web applications with message passing API
- [ ] Agent workspace modes implemented: Live Call, Research, Documentation modes with distinct layouts
- [ ] Workflow disruption reduced by 60% (validated via user session analysis comparing Mira baseline to new platform)
- [ ] Agent satisfaction with workflow integration >4.0/5 (measured via post-deployment survey)
- [ ] Support tickets for UI-related issues reduced by 50% in first 30 days post-deployment
- [ ] Technical documentation complete: SDK documentation, configuration schema reference, admin portal user guide
- [ ] Performance validated: Configuration loading adds <200ms to page load; panel interactions <50ms response time
