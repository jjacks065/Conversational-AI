# 🧩 Project Name: Agent Experience: Intelligent Response Architecture & Progressive Disclosure

**PDLC Phase:** Define  
**Authored Date:** April 29, 2026  
**Status:** DRAFT  

---

## 🎯 Problem Statement

Current response format overwhelms agents with dense, unstructured information during live calls. Agents struggle to distinguish required audit-complete disclosures from contextual explanation, creating risk of incomplete member communication or misquoting in-network vs out-of-network benefits. The lack of response hierarchy and scoping increases cognitive load, slows parsing time, and reduces confidence in high-pressure call scenarios.

**Impact:** Dense, unstructured responses increase average handle time by forcing agents to parse complex information under pressure. Risk of misquoting benefits creates compliance exposure. Cognitive overload reduces agent confidence and adoption.

**Evidence from UX Evaluation:**
- "Must decide what to say vs. skip; risk of audit failure" (P0 Priority)
- "Mixed INN/OON details increase confusion and misquoting risk" (P1 Priority)
- CASTLE Framework: "Cognitive Load = High (3/3)" - Dense responses without clear hierarchy
- Agent quote: "Worried like, oh, did I accidentally give out of network instead of in-network"
- Agent quote: "In lieu of the 'brief answer,' I would ideally hope that it would have the correct scripting for how we're supposed to quote the benefit"

---

## 💡 Proposed Solution

Implement an **Intelligent Response Architecture** that structures all Minerva API responses into explicit, visually distinct three-tier hierarchy with progressive disclosure controls. Enable clear separation of in-network vs out-of-network benefits and provide context-aware defaults that adapt to query intent and agent workflow modes.

**Key Components:**
1. **Three-Tier Response Hierarchy:** Required Disclosures (Tier 1) + Contextual Explanation (Tier 2) + Optional Details (Tier 3)
2. **INN/OON Visual Separation:** Tab-based, card-based, or accordion-based separation patterns with scope intelligence
3. **Progressive Disclosure Framework:** Workspace modes (Live Call, Research, Documentation) with smart defaults
4. **Visual Information Hierarchy:** Typography system, emphasis patterns, scanability optimization, accessibility compliance

---

## 👥 Target Users

**Primary Users:**
- **Contact Center Agents:** Need clear, actionable responses structured for immediate member communication with audit compliance confidence
- **Quality Assurance Teams:** Need confidence that required disclosures are clearly identified and agents can quote accurately
- **Compliance Officers:** Need assurance that regulatory required disclosures are consistently included and identifiable

**Secondary Users:**
- **Training Teams:** Benefit from structured responses that teach agents benefit mechanics through contextual explanations
- **Customer Members:** Receive clearer, more complete benefit information when agents use structured responses

---

## ✅ Success Metrics

### Agent Performance Metrics
- **Parsing Efficiency:** Agent parsing time reduced by 45% (measured via session analytics and time-to-first-word metrics)
- **Cognitive Load:** Post-query cognitive load scores improve from 3/3 (high) to 1/3 (low) in CASTLE assessments
- **Response Satisfaction:** Agent satisfaction scores >4.5/5 for information clarity and structure

### Quality & Compliance Metrics
- **Misquoting Reduction:** Incidents of benefit misquoting reduced by 35% (tracked via quality monitoring)
- **Audit Compliance:** 100% of responses include clearly identified required disclosures (verified via automated checks)
- **Agent Confidence:** Self-reported confidence in using responses during live calls increases from 3.2/5 to 4.5/5

### Operational Metrics
- **Average Handle Time:** AHT reduction of 15% attributable to faster response parsing
- **Follow-Up Rate:** Member follow-up calls for clarification reduced by 20%

---

## 📦 Scope

**What's included in this release?**

### A. Three-Tier Response Hierarchy System

**Tier 1: Required Disclosures (Audit-Complete Script)**
- **Purpose:** Complete, quotable script that satisfies regulatory and compliance requirements
- **Visual Treatment:** Distinct header ("Member Communication Script"); high-contrast background; primary typography; copy-to-clipboard button with "Audit Compliant" indicator; regulatory citation badges
- **Content Characteristics:** Conversational, member-friendly language; complete sentences for direct reading; all required disclaimers and qualifiers; accessible language (8th-grade reading level)
- **White-Label Configuration:** Customer-specific compliance language templates; state-specific required disclosure variants; line-of-business terminology (Medicare, Medicaid, Commercial)

**Tier 2: Contextual Explanation (Agent Understanding)**
- **Purpose:** Supporting information helping agents understand benefit structure and answer follow-up questions
- **Visual Treatment:** Collapsible section with header ("How This Works"); secondary typography; neutral background; progressive disclosure (collapsed by default in Live Call mode)
- **Content Characteristics:** Plain-language explanation of benefit mechanics; common member questions and suggested responses; key terms and definitions; examples and scenarios
- **Configuration:** Toggle visibility per customer preference; agent-level expansion preference persistence

**Tier 3: Optional Details & Edge Cases**
- **Purpose:** Comprehensive information for complex scenarios, unusual member situations, or deep-dive research
- **Visual Treatment:** Accordion/expandable sections organized by topic; tertiary typography; "Show More Details" expansion control; fully collapsed by default
- **Content Characteristics:** Technical details (CPT codes, authorization requirements); edge case scenarios; alternative benefit structures; limitations and exclusions
- **Configuration:** Optional - can be disabled entirely for simplified deployments; role-based visibility (senior agents, supervisors)

### B. In-Network vs Out-of-Network Scope Clarity

**Visual Separation Patterns:**

1. **Tab-Based Separation (Preferred for Complex Benefits)**
   - Distinct tabs: "In-Network" | "Out-of-Network"
   - Active tab highlighted with customer brand color
   - Default to detected scope based on query intent
   - Badge indicators: "Lower Cost" on INN tab; "Higher Cost" on OON tab

2. **Card-Based Separation (Preferred for Side-by-Side Comparison)**
   - Side-by-side cards with distinct visual treatment
   - "In-Network" card: green accent, checkmark icon
   - "Out-of-Network" card: orange/yellow accent, information icon

3. **Accordion-Based Separation (Preferred for Sequential Disclosure)**
   - Sequential expandable sections
   - Lead with most relevant network type based on query intent
   - Collapsed secondary network type available on demand

**Scope Intelligence:**
- **Intent Detection:** Analyze member query for network preference indicators ("My doctor" → likely INN; "Out-of-network coverage" → explicit OON)
- **Proactive Clarification:** If scope ambiguous, prompt agent: "Clarify with member: In-network or out-of-network provider?"
- **Context-Aware Defaults:** Remember agent's last scope selection within session for faster follow-up queries

**White-Label Configuration:**
- Customer terminology preference ("In-Network" vs "Preferred Provider" vs "PPO Network")
- Network type emphasis based on customer plan designs (HMO-heavy vs PPO-heavy portfolios)
- Cost comparison visibility toggles

### C. Progressive Disclosure Framework

**Disclosure Patterns:**

1. **Live Call Mode (Minimal)**
   - Tier 1 (Required Disclosures) fully visible
   - Tier 2 (Contextual Explanation) collapsed with visible header and "Expand" control
   - Tier 3 (Optional Details) hidden entirely with "Show Advanced Details" link in footer
   - Estimated reading time displayed: "~30 seconds to read"

2. **Research Mode (Detailed)**
   - Tier 1 and Tier 2 fully expanded
   - Tier 3 sections collapsed but visible with descriptive headers
   - "Collapse All" quick action for switching to minimal view

3. **Documentation Mode (Comprehensive)**
   - All tiers expanded
   - Print-optimized layout
   - Copy-all-tiers button for complete documentation capture

**Agent Controls:**
- **View Mode Toggle:** Quick-switch button in header: "Minimal | Detailed | Complete"
- **Section-Level Expansion:** Each collapsible section independently expandable
- **"Expand All" / "Collapse All":** Bulk controls for rapid view switching
- **Keyboard Shortcuts:** Power-user navigation (Cmd/Ctrl + E = expand, Cmd/Ctrl + C = collapse)

**Smart Defaults Based on Context:**
- **First Query in Session:** Start in "Detailed" mode to build agent confidence
- **Follow-Up Queries:** Switch to "Minimal" mode for efficiency
- **Complex Benefits (e.g., Deductible, Coinsurance):** Auto-expand Tier 2 for clarity
- **Simple Benefits (e.g., Telemedicine Copay):** Keep Tier 2 collapsed for speed

### D. Visual Information Hierarchy & Scanability

**Typography System:**
- Tier 1 Headers: Bold, 18px, customer primary color
- Tier 1 Body: Regular, 16px, high-contrast text (4.5:1 minimum)
- Tier 2 Headers: Semibold, 16px, neutral color
- Tier 2 Body: Regular, 14px, standard text contrast
- Tier 3 Headers: Medium, 14px, subdued color
- Tier 3 Body: Regular, 13px, secondary text color

**Emphasis & Signaling:**
- Critical Qualifiers: Inline badges or bold emphasis (e.g., "prior authorization required")
- Cost Information: Formatted with currency styling, right-aligned in consistent position
- Compliance Flags: Icon + text badges (e.g., 🛡️ "State Mandate", ⚕️ "ACA Essential Health Benefit")

**Accessibility Compliance:**
- WCAG 2.1 AA Standards: Minimum 4.5:1 contrast for body text, 3:1 for large text
- Semantic HTML: Proper heading hierarchy, ARIA labels for screen readers
- Keyboard Navigation: All expand/collapse controls accessible via keyboard
- Focus Indicators: High-visibility focus rings for keyboard users

---

## 🚫 Out-of-Scope

**What's explicitly out of scope?**

- Advanced intent detection and scope intelligence (Phase 2 - Q3 2026)
- Multi-language response templates (future roadmap)
- Voice-optimized response formatting for voice channel (future consideration)
- Mobile-responsive layout optimization (desktop-first priority)
- Real-time response customization based on agent skill level (future enhancement)
- Integration with external compliance validation systems (separate initiative)

---

## 🔗 Dependencies & Risks

### Critical Dependencies
- **Minerva API Response Structure:** Requires API modification to support three-tier structured output (Tier 1, 2, 3 separation)
- **Compliance Team Review:** Requires validation of Tier 1 response templates for regulatory accuracy across all benefit types
- **Customer Stakeholder Validation:** Requires customer approval of network separation patterns and terminology
- **PRD-1 Platform Foundation:** Requires contextual panel architecture and workspace mode framework

### Key Risks

**Risk 1: Over-Simplification of Tier 1 Responses**
- **Impact:** Medium - Risk of Tier 1 responses being too brief, lacking necessary context for member understanding
- **Mitigation:** Iterative agent testing during development; compliance team review at each iteration; balance brevity with completeness; pilot with real calls before full rollout

**Risk 2: Configuration Complexity Creating Admin Burden**
- **Impact:** Medium - Risk of too many template options creating overwhelming admin portal experience
- **Mitigation:** Sensible defaults that work for 80% of customers; template library with pre-built options; expert services support for custom templates; progressive disclosure in admin UI

**Risk 3: Scope Detection Accuracy for INN/OON**
- **Impact:** Medium - Risk of incorrect INN/OON default selection confusing agents and requiring manual override
- **Mitigation:** Conservative defaults (show both when ambiguous); clear visual indicators of which is displayed; easy manual override controls; track detection accuracy and refine algorithms

**Risk 4: Cognitive Load During Transition**
- **Impact:** Medium - Agents accustomed to current format may initially struggle with new structure
- **Mitigation:** Comprehensive training on new response structure; side-by-side comparison demos; gradual rollout with feedback collection; agent champions program

---

## 🏁 Definition of Done

**Task list of statements that define when implementation of this PRD would be considered complete:**

* [ ] Three-tier response hierarchy implemented: Tier 1, 2, 3 structure rendering correctly with distinct visual treatment
* [ ] INN/OON visual separation working: Tab-based pattern functional with scope intelligence and default detection
* [ ] Progressive disclosure controls operational: Expand/collapse controls, view mode toggle, workspace mode integration
* [ ] Copy-to-clipboard functionality working: Tier 1 responses copy with formatting and audit compliance indicator
* [ ] Configuration schema complete: Customer template configuration operational in admin portal
* [ ] Visual information hierarchy implemented: Typography system, emphasis patterns, scanability optimizations applied
* [ ] Accessibility compliance verified: WCAG 2.1 AA compliance validated via automated tools and manual expert audit
* [ ] Keyboard navigation functional: All expand/collapse controls accessible via keyboard with proper focus indicators
* [ ] Minerva API integration complete: API modified to return three-tier structured output for all benefit types
* [ ] Agent parsing time reduced by 45% (validated via session analytics comparing baseline to new architecture)
* [ ] Misquoting incidents reduced by 35% (measured via quality monitoring in first 60 days post-deployment)
* [ ] Agent satisfaction >4.5/5 for information clarity and structure (measured via post-deployment survey)
* [ ] 100% of responses include clearly identified required disclosures (verified via automated compliance checks)
* [ ] Technical documentation complete: Response structure specification, configuration guide, agent user guide

---

## 📊 Cost-Optimization Contribution

This PRD directly supports primary cost optimization objective ($0.25-$0.27 → $0.08 per query):

1. **Reduced Token Usage:** Streamlined response structure reduces unnecessary text generation (estimated 20-30% token reduction)
2. **Faster Query Resolution:** 45% parsing time reduction translates to lower average handle time and improved cost per query
3. **Decreased Escalations:** Clearer responses reduce member confusion and callback rates (estimated 20% reduction)
4. **Training Efficiency:** Structured responses with built-in guidance reduce training time and ongoing coaching needs by 30%
5. **Quality Maintenance:** Better response structure maintains >98% accuracy while reducing computational complexity

**ROI Estimate:** 15% AHT reduction = significant cost savings at scale; 30% training time reduction = $300-500 per agent savings

---

## 🗓️ Implementation Timeline

**Phase 1 - Q2 2026 (6 weeks):**

**Weeks 1-2: Design & API Specification**
- Finalize three-tier response structure and visual design
- Define Minerva API response schema modifications
- Create mockups for INN/OON separation patterns
- Validate compliance language templates with legal/compliance teams

**Weeks 3-5: Core Development**
- Implement three-tier response rendering engine
- Build INN/OON visual separation (tab-based pattern)
- Develop progressive disclosure controls and view mode toggle
- Create copy-to-clipboard functionality with formatting

**Week 6: Configuration & Testing**
- Implement configuration schema for customer templates
- Complete visual information hierarchy and accessibility audit
- Browser compatibility testing
- Agent pilot testing and feedback integration

**Phase 2 - Q3 2026 (4 weeks):**
- Smart defaults based on query context and session history
- Enhanced scope intelligence with proactive clarification prompts
- Keyboard shortcuts and power-user navigation enhancements
- Advanced configuration options for network separation patterns

---

## 📎 References & Alignment

**Strategic Alignment:**
- **KR5 Q3 2026:** Implement intelligent response architecture achieving 45% parsing time reduction
- **Roadmap Q3 2026:** "Agent Experience Evolution" - Enhanced information presentation and cognitive load reduction

**Related PRDs:**
- **PRD-1:** Low-Code Platform Foundation (dependency - provides panel framework and workspace modes)
- **PRD-3:** Real-Time System Feedback (integration - progressive loading during response generation)
- **PRD-4:** Context-Aware Workflow Integration (integration - source citations within response tiers)

**UX Research:**
- Mira UX Evaluation (April 2026) - Addresses P0 priority cognitive load issues
- CASTLE Framework Assessment - Targets "Cognitive Load = High (3/3)" finding

---

**Document Version:** 1.0  
**Last Updated:** April 29, 2026  
**Author:** Product Management, Minerva Team
