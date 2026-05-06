# CSR Chat (Minerva) UI Platform - PRD Proposals

**UX Research Source:** Mira UX Evaluation (April 2026)
**Decision Context:** Replace fixed Mira UI with cost-efficient, white-label CSR Chat Low-Code/No-Code platform

---

## Executive Summary

Based on comprehensive UX evaluation of the current Mira interface (powered by Minerva APIs), this document proposes **six focused Feature PRDs** that address critical usability barriers while advancing strategic cost optimization and agent adoption objectives. These PRDs organize UX findings into independent, measurable, customer-configurable deliverables aligned with achieving **<$0.08 per query** cost targets while enabling **>90% agent adoption** and **>95% agent satisfaction** by Q1 2027.

### Key Finding from UX Evaluation

**Current State:** Mira's core AI capability is recognized and valued by agents, but UX execution creates adoption barriers. Agents report improved efficiency and confidence but must work around workflow friction, system uncertainty, and interface limitations during live calls.

**Strategic Imperative:** UX improvements are not optional enhancements—they are critical enablers of cost optimization through increased adoption, reduced training overhead, decreased support costs, and elimination of redundant tool usage.

### Cost-Optimization Rationale for UX Investment

- **Adoption Impact:** Poor UX drives agents back to legacy tools, reducing ROI on Minerva investment and preventing cost-per-query optimization through scale
- **Training Costs:** Intuitive, low-code UI reduces onboarding time by 50% and eliminates recurring training overhead
- **Support Reduction:** Clear system feedback, error recovery, and contextual guidance reduce support tickets by 50%
- **Workflow Efficiency:** Contextual integration eliminates tool-switching overhead, reducing average handle time and improving cost metrics
- **Multi-Customer Scale:** White-label, configurable platform enables rapid customer deployment without custom development costs

---

## Foundation Analysis

### Current Strategic Alignment

**Primary Goal:** Achieve 70% per-query cost reduction ($0.25-$0.27 → $0.08) by Q1 2027
**Adoption Target:** Scale from <10% to >90% agent utilization
**Quality Target:** Maintain >98% accuracy across expanded plan coverage

### KR5: Agent Experience & Adoption Excellence (from Strategic Objective)

- **Q2 2026:** Deploy Low-Code/No-Code UI platform foundation reducing workflow disruption by 60%
- **Q3 2026:** Implement intelligent response architecture and real-time system feedback achieving >80% agent adoption and 45% parsing time reduction
- **Q4 2026:** Complete context-aware workflow integration and error handling framework reducing verification overhead by 50% and achieving >90% agent utilization
- **Q1 2027:** Sustain >95% agent satisfaction with cost-optimized UX achieving target adoption while maintaining $0.08 per query constraint

### Roadmap Q2 2026 "Enhanced Agent Experience" Card Alignment

The roadmap explicitly calls for:

- Release no-code/low-code user interface
- Contextual panel and configurable architecture
- Seamless integration into existing agent workflows
- Reduced workflow disruption through in-context information display
- Increased agent confidence via real-time guidance and progress indicators
- Addresses HyperCare Live Issue Log ID:4-11 (UI Display Issues)

### UX Evaluation Priority Framework

The evaluation identified **24 specific design recommendations** organized into three priority tiers:

- **P0 (Critical - 5 items):** Block adoption if unaddressed - full-screen disruption, silent loading, no progress indication, no cancel control, unclear response hierarchy
- **P1 (High - 6 items):** Significantly limit effectiveness - fixed positioning, non-resizable, hidden sources, no deep links, INN/OON confusion, generic errors
- **P2 (Medium - 5 items):** Reduce learnability and efficiency - weak onboarding, unclear prompt guidance, auto-scroll issues, low discoverability, accessibility concerns

---

## PRD Structure

### PRD-1: Low-Code/No-Code UI Platform Foundation & Configuration Framework

### Problem Statement

Current Mira UI creates adoption barriers through fixed positioning, full-screen takeovers, and inflexible interface patterns that disrupt agent workflows during live calls. Each customer deployment requires custom development, creating unsustainable costs and slow deployment cycles. Agents need a contextual, adaptable interface that integrates seamlessly with existing workflows while enabling customer-specific branding, layout, and configuration without engineering effort.

### Strategic Alignment

- **Cost Impact:**

  - Eliminate custom UI development costs (estimated 50% reduction in per-customer deployment costs)
  - Reduce training overhead by 50% through intuitive, self-service configuration
  - Decrease support costs by 40% through better workflow integration
  - Enable rapid multi-customer scaling supporting cost-per-query optimization through volume
- **Adoption Driver:** Flexible, contextual interface increases agent confidence and sustained usage, directly supporting >90% adoption target
- **Quality Enabler:** Better workflow integration reduces misquoting risk and maintains >98% accuracy standards

### Success Metrics (Measurable)

- **Workflow Disruption:** Reduce agent workflow disruption by 60% (measured via user session analysis and time-to-task metrics)
- **Configuration Adoption:** >80% of customers utilize white-label customization within 30 days of deployment
- **Agent Preference:** Interface customization adoption >80% within 30 days of agent access
- **Support Reduction:** Support tickets for UI-related issues reduced by 50% compared to Mira baseline
- **Deployment Speed:** Customer deployment time reduced from weeks to days (target: 3-day deployment cycle)
- **Training Efficiency:** Agent onboarding time reduced by 50% (target: <2 hours to proficiency)

### Key Capabilities

#### A. Contextual Panel Architecture (Addresses P0/P1 UX Issues)

**Replaces:** Full-screen takeover pattern that disrupts spatial continuity and blocks underlying workflow

**Core Features:**

- Non-modal, floating panel that maintains context with underlying application (Nexus, customer systems)
- Movable panel with drag-to-reposition capability preserving spatial memory across sessions
- Resizable width with agent preference persistence (supports narrow vertical scanning and wide horizontal reading)
- Collapsible/expandable states with discoverable affordances (tooltips, first-run coachmarks)
- Multiple docking positions: right-sidebar (default), left-sidebar, bottom-panel, floating
- Picture-in-picture mode for minimal footprint during non-query states

**White-Label Configuration:**

- Customer-defined default position, size, and docking behavior
- Agent-level override capabilities with workspace preference saving
- Responsive layout adaptation based on customer application constraints

#### B. White-Label Branding & Theming Framework

**Enables:** Customer-specific branding without code changes, supporting multi-tenant deployment model

**Configuration Options:**

- **Visual Identity:**

  - Custom logo, product name, and iconography
  - Brand color palette (primary, secondary, accent colors)
  - Typography system (font families, weights, sizes)
  - Light/dark theme variants with automatic contrast compliance
- **Layout Customization:**

  - Header/footer customization (show/hide, content, links)
  - Panel chrome styling (borders, shadows, spacing)
  - Component-level styling (buttons, inputs, cards)
- **Terminology & Language:**

  - Customizable product name ("CSR Chat", "Mira", customer-preferred naming)
  - Microcopy localization framework for multi-language support
  - Help text and guidance customization per customer vocabulary

**Technical Implementation:**

- CSS custom property system for theme injection
- JSON-based configuration schema for customer branding packages
- Theme preview and validation tools in customer admin portal
- Real-time theme switching without deployment (hot-reload capability)

#### C. Low-Code Configuration Interface (Admin Portal)

**Purpose:** Enable customer administrators and IT teams to configure CSR Chat without engineering support

**Configuration Domains:**

1. **Interface Layout Configuration:**

   - Default panel size, position, docking behavior
   - Agent customization permissions (lock/unlock specific settings)
   - Responsive breakpoint behavior for different screen sizes
   - Integration target specification (embedded vs standalone)
2. **Behavioral Configuration:**

   - Auto-collapse on inactivity (timeout settings)
   - Keyboard shortcuts and accessibility options
   - Session persistence behavior (remember queries, context, position)
   - Performance optimization settings (lazy loading, caching policies)
3. **Integration Configuration:**

   - Parent application integration method (iframe, web component, SDK)
   - SSO/authentication integration parameters
   - Data exchange protocols (query context, user identity, session state)
   - Deep-linking rules to customer source systems (Nexus, claims systems, plan documents)
4. **Feature Enablement:**

   - Granular feature flag control (enable/disable specific capabilities per customer or agent group)
   - Progressive rollout support (A/B testing, phased deployment)
   - Role-based access control (agent roles, supervisor roles, admin roles)

**Admin Experience:**

- Visual configuration builder with live preview
- Configuration validation and error prevention
- Import/export configuration templates for multi-environment deployment
- Audit logging of configuration changes
- Rollback capability for configuration errors

#### D. Nexus Integration & Workflow Preservation

**Addresses:** Agents' need for parallel verification and trust-building workflows

**Integration Patterns:**

- Side-by-side panel display maintaining Nexus content visibility
- Contextual awareness of Nexus state (current plan, member, benefit section)
- Bi-directional communication (CSR Chat queries informed by Nexus context; results deep-link back to Nexus)
- Synchronized scrolling and highlighting for verification workflows

**Customer Application Integration SDK:**

- JavaScript SDK for embedding CSR Chat in any web application
- React, Angular, Vue component libraries for framework-specific integration
- Message passing API for parent-child application communication
- Responsive container API for dynamic resizing based on parent constraints

#### E. Agent Preference & Workspace Management

**Purpose:** Enable agents to personalize interface while maintaining customer-defined guardrails

**Agent Controls:**

- Workspace layouts: save multiple layout configurations for different task contexts
- Quick-switch layouts: toggle between "minimal" (compact) and "detailed" (expanded) views
- Preference sync across devices and sessions (cloud-stored agent profiles)
- Reset to customer defaults option

**Workspace Scenarios:**

- **Live Call Mode:** Minimal footprint, quick-access position, essential controls only
- **Research Mode:** Expanded view, side-by-side verification layout, full citation visibility
- **Documentation Mode:** Optimized for copy/paste workflows, audit trail emphasis

### White-Label & Configuration Capabilities Summary

This PRD establishes CSR Chat as a **configurable product platform** rather than single-instance application:

- **Multi-Tenant Architecture:** Single codebase serving multiple customers with isolated configuration
- **Customer Admin Control:** Self-service configuration without vendor engineering involvement
- **Agent Empowerment:** Personal customization within customer-defined boundaries
- **Rapid Deployment:** Days instead of weeks for new customer onboarding
- **Consistent Updates:** Core platform improvements benefit all customers simultaneously
- **Cost Efficiency:** Shared infrastructure with customer-specific presentation

### Implementation Scope & Phasing

**Phase 1 - Q2 2026 (8 weeks):**

- **In-Scope:**

  - Contextual panel architecture (position, size, movable, modal/non-modal, full-screen)
  - Basic white-label theming (logo, colors, agent name, window title)
  - Customer applicatoin integration framework (eg. Nexus, side-by-side layout)
- **Out-of-Scope:**

  - Advanced multi-language localization
  - Complex role-based access control beyond basic agent/admin
  - Mobile/tablet responsive design (desktop-first)
  - Integration with non-Nexus customer systems (future roadmap)

**Phase 2 - Q3 2026 (4 weeks):**

- Configuration admin portal (MVP)
- Advanced configuration options (feature flags, behavioral settings)
- Accessibility compliance (WCAG 2.1 AA)

### Dependencies & Risks

**Dependencies:**

- Minerva API stability for query processing (performance optimization PRDs)
- Nexus API access for deep-linking and context awareness
- Customer SSO/authentication integration specifications

**Risks:**

- **Configuration Complexity:** Risk of admin portal becoming too complex, reducing self-service value

  - *Mitigation:* Progressive disclosure in admin UI; template-based configuration; expert support for complex scenarios
- **Browser Compatibility:** Risk of panel positioning/sizing issues across browsers and versions

  - *Mitigation:* Standards-based CSS; comprehensive browser testing matrix; graceful degradation for older browsers
- **Performance:** Risk of configuration overhead impacting sub-second response time targets

  - *Mitigation:* Configuration caching; lazy loading; performance budgets for configuration processing

### Cost-Optimization Contribution

This PRD directly supports primary cost optimization objective:

1. **Reduced Custom Development:** Eliminate per-customer UI engineering ($50K-100K per customer avoided)
2. **Faster Deployment Cycles:** 10x faster customer onboarding supports volume-based cost efficiency
3. **Lower Training Costs:** Intuitive, flexible UI reduces training time by 50% (estimated $500-1000 per agent savings)
4. **Decreased Support Overhead:** Self-service configuration and better UX reduce support tickets by 50% (estimated $100K annual savings)
5. **Higher Adoption ROI:** Better UX drives agent adoption, increasing query volume and improving per-query cost economics through scale

---

## PRD-2: Intelligent Response Architecture & Progressive Disclosure

### Problem Statement

Current response format overwhelms agents with dense, unstructured information during live calls. Agents struggle to distinguish required audit-complete disclosures from contextual explanation, creating risk of incomplete member communication or misquoting in-network vs out-of-network benefits. The lack of response hierarchy and scoping increases cognitive load, slows parsing time, and reduces confidence in high-pressure call scenarios.

**Evidence from UX Evaluation:**

- "Must decide what to say vs. skip; risk of audit failure" (P0 Priority)
- "Mixed INN/OON details increase confusion and misquoting risk" (P1 Priority)
- Agents report: "Worried like, oh, did I accidentally give out of network instead of in-network"
- CASTLE Framework: "Cognitive Load = High (3/3)" - Dense responses without clear hierarchy

### Strategic Alignment

- **Cost Impact:**

  - Reduced average handle time through faster parsing (estimated 15% AHT reduction = significant cost savings at scale)
  - Decreased misquoting incidents reduces compliance costs and member escalations
  - Streamlined responses reduce token usage and computational costs (supports $0.08 per query target)
- **Quality Driver:** Clear information hierarchy reduces misquoting risk and maintains >98% accuracy standards
- **Adoption Catalyst:** Agents confidently use tool when responses are actionable and audit-compliant (supports >80% Q3 adoption target)

### Success Metrics (Measurable)

- **Parsing Efficiency:** Agent parsing time reduced by 45% (measured via session analytics and time-to-first-word metrics)
- **Cognitive Load:** Post-query cognitive load scores improve from 3/3 (high) to 1/3 (low) in CASTLE assessments
- **Misquoting Reduction:** Incidents of benefit misquoting reduced by 35% (tracked via quality monitoring)
- **Response Satisfaction:** Agent satisfaction scores >4.5/5 for information clarity and structure
- **Audit Compliance:** 100% of responses include clearly identified required disclosures
- **Agent Confidence:** Self-reported confidence in using responses during live calls increases from 3.2/5 to 4.5/5

### Key Capabilities

#### A. Three-Tier Response Hierarchy System

**Architecture:** Structure all Minerva API responses into explicit, visually distinct tiers

**Tier 1: Required Disclosures (Audit-Complete Script)**

- **Purpose:** Complete, quotable script that satisfies regulatory and compliance requirements
- **Visual Treatment:**

  - Distinct header: "Member Communication Script" or "Required Disclosure"
  - High-contrast background (e.g., light blue/green tint indicating "safe to quote")
  - Primary typography emphasis
  - Copy-to-clipboard button with "Audit Compliant" indicator
  - Regulatory citation badge (e.g., "ACA Required", "State Mandated")
- **Content Characteristics:**

  - Conversational, member-friendly language
  - Complete sentences suitable for direct reading
  - All required disclaimers and qualifiers included
  - Accessible language (8th-grade reading level)
- **White-Label Configuration:**

  - Customer-specific compliance language templates
  - State-specific required disclosure variants
  - Line-of-business specific terminology (Medicare, Medicaid, Commercial)

**Tier 2: Contextual Explanation (Agent Understanding)**

- **Purpose:** Supporting information helping agents understand the benefit structure and answer follow-up questions
- **Visual Treatment:**

  - Collapsible section with header: "How This Works" or "Additional Context"
  - Secondary typography styling
  - Neutral background
  - Progressive disclosure (collapsed by default in "Live Call" mode; expanded in "Research" mode)
- **Content Characteristics:**

  - Plain-language explanation of benefit mechanics
  - Common member questions and suggested responses
  - Key terms and definitions
  - Examples and scenarios for clarity
- **Configuration:**

  - Toggle visibility per customer preference (some customers may prefer minimal context)
  - Agent-level expansion preference persistence

**Tier 3: Optional Details & Edge Cases**

- **Purpose:** Comprehensive information for complex scenarios, unusual member situations, or deep-dive research
- **Visual Treatment:**

  - Accordion/expandable sections organized by topic
  - Tertiary typography styling
  - "Show More Details" expansion control
  - Fully collapsed by default in all modes
- **Content Characteristics:**

  - Technical details (e.g., specific CPT codes, authorization requirements)
  - Edge case scenarios (e.g., "if the member has secondary insurance")
  - Alternative benefit structures
  - Limitations and exclusions details
- **Configuration:**

  - Optional - can be disabled entirely for simplified deployments
  - Role-based visibility (available to senior agents, supervisors)

#### B. In-Network vs Out-of-Network Scope Clarity

**Problem Addressed:** INN/OON paths currently interwoven, creating confusion and misquoting risk

**Solution:** Visual and structural separation of network types

**Visual Separation Patterns:**

1. **Tab-Based Separation (Preferred for Complex Benefits):**

   - Distinct tabs: "In-Network" | "Out-of-Network"
   - Active tab highlighted with customer brand color
   - Default to detected scope (INN if member asking about preferred provider; OON if asking about specific out-of-network provider)
   - Badge indicators: "Lower Cost" on INN tab; "Higher Cost" on OON tab
2. **Card-Based Separation (Preferred for Side-by-Side Comparison):**

   - Side-by-side cards with distinct visual treatment
   - "In-Network" card: green accent, checkmark icon
   - "Out-of-Network" card: orange/yellow accent, information icon
   - Side-by-side comparison highlights cost differential
3. **Accordion-Based Separation (Preferred for Sequential Disclosure):**

   - Sequential expandable sections
   - Lead with most relevant network type based on query intent
   - Collapsed secondary network type available on demand

**Scope Intelligence:**

- **Intent Detection:** Analyze member query for network preference indicators

  - "My doctor" → likely INN query (check if provider in-network)
  - "Out-of-network coverage" → explicit OON query
  - Generic benefit question → show both with INN emphasis
- **Proactive Clarification:** If scope ambiguous, prompt agent: "Clarify with member: In-network or out-of-network provider?"
- **Context-Aware Defaults:** Remember agent's last scope selection within session for faster follow-up queries

**White-Label Configuration:**

- Customer terminology preference ("In-Network" vs "Preferred Provider" vs "PPO Network")
- Network type emphasis based on customer plan designs (HMO-heavy vs PPO-heavy portfolios)
- Cost comparison visibility toggles

#### C. Progressive Disclosure Framework

**Interaction Model:** Show the minimum necessary information by default; reveal additional layers on demand

**Disclosure Patterns:**

1. **Live Call Mode (Minimal):**

   - Default state: Tier 1 (Required Disclosures) fully visible
   - Tier 2 (Contextual Explanation) collapsed with visible header and "Expand" control
   - Tier 3 (Optional Details) hidden entirely with "Show Advanced Details" link in footer
   - Estimated reading time displayed: "~30 seconds to read"
2. **Research Mode (Detailed):**

   - Default state: Tier 1 and Tier 2 fully expanded
   - Tier 3 sections collapsed but visible with descriptive headers
   - "Collapse All" quick action for switching to minimal view
3. **Documentation Mode (Comprehensive):**

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

#### D. Visual Information Hierarchy & Scanability

**Typography System:**

- **Tier 1 Headers:** Bold, 18px, customer primary color
- **Tier 1 Body:** Regular, 16px, high-contrast text (4.5:1 minimum)
- **Tier 2 Headers:** Semibold, 16px, neutral color
- **Tier 2 Body:** Regular, 14px, standard text contrast
- **Tier 3 Headers:** Medium, 14px, subdued color
- **Tier 3 Body:** Regular, 13px, secondary text color

**Emphasis & Signaling:**

- **Critical Qualifiers:** Inline badges or bold emphasis (e.g., "prior authorization required")
- **Cost Information:** Formatted with currency styling, right-aligned in consistent position
- **Compliance Flags:** Icon + text badges (e.g., 🛡️ "State Mandate", ⚕️ "ACA Essential Health Benefit")

**Layout Principles:**

- **Breathing Room:** Generous whitespace between tiers (24px minimum)
- **Consistent Margins:** Left-aligned text with predictable indentation for hierarchy
- **Scan Patterns:** Support F-pattern and Z-pattern reading with strategic information placement
- **Mobile-First Considerations:** Single-column layout, touch-friendly expand controls (future roadmap)

**Accessibility Compliance:**

- **WCAG 2.1 AA Standards:** Minimum 4.5:1 contrast for body text, 3:1 for large text
- **Semantic HTML:** Proper heading hierarchy, ARIA labels for screen readers
- **Keyboard Navigation:** All expand/collapse controls accessible via keyboard
- **Focus Indicators:** High-visibility focus rings for keyboard users

### White-Label & Configuration Capabilities

**Response Templating Engine:**

- Customer-defined response templates per benefit type (Medical, Rx, Dental, Vision)
- Tier content rules: define what belongs in Tier 1 vs Tier 2 vs Tier 3 per customer compliance requirements
- State-specific disclosure language injection
- Line-of-business specific terminology and phrasing

**Configuration Options:**

- **Default Disclosure Mode:** Minimal | Detailed | Complete (customer-level default)
- **Agent Override Permissions:** Lock/unlock agent's ability to change disclosure mode
- **Tier Visibility:** Enable/disable Tier 3 entirely for simplified deployments
- **Network Separation Pattern:** Tabs | Cards | Accordion (customer preference)
- **Compliance Emphasis:** High (all badges, warnings, citations) | Medium (key badges only) | Low (minimal compliance signaling)

### Implementation Scope & Phasing

**Phase 1 - Q2 2026 (6 weeks):**

- **In-Scope:**

  - Three-tier response hierarchy (Tier 1, 2, 3 structure)
  - INN/OON visual separation (tab-based pattern)
  - Basic progressive disclosure (expand/collapse controls)
  - Copy-to-clipboard for Tier 1 responses
  - Configuration schema for customer templates
- **Out-of-Scope:**

  - Advanced intent detection and scope intelligence (Q3 roadmap)
  - Multi-language response templates
  - Voice-optimized response formatting (future consideration)
  - Mobile-responsive layout (desktop-first priority)

**Phase 2 - Q3 2026 (4 weeks):**

- Smart defaults based on query context
- Workspace mode integration (Live Call, Research, Documentation modes)
- Enhanced scope intelligence with proactive clarification prompts
- Keyboard shortcuts and power-user navigation

### Dependencies & Risks

**Dependencies:**

- Minerva API response structure modification to support three-tier output
- Compliance team review of Tier 1 response templates for regulatory accuracy
- Customer stakeholder validation of network separation patterns

**Risks:**

- **Over-Simplification:** Risk of Tier 1 responses being too brief, lacking necessary context for member understanding

  - *Mitigation:* Iterative agent testing; compliance review; balance brevity with completeness
- **Configuration Complexity:** Risk of too many template options creating admin burden

  - *Mitigation:* Sensible defaults; template library with pre-built options; expert services for custom templates
- **Scope Detection Accuracy:** Risk of incorrect INN/OON default selection confusing agents

  - *Mitigation:* Conservative defaults (show both when ambiguous); clear visual indicators; easy manual override

### Cost-Optimization Contribution

This PRD directly supports primary cost optimization objective:

1. **Reduced Token Usage:** Streamlined response structure reduces unnecessary text generation (estimated 20-30% token reduction)
2. **Faster Query Resolution:** 45% parsing time reduction translates to lower average handle time and improved cost per query
3. **Decreased Escalations:** Clearer responses reduce member confusion and callback rates
4. **Training Efficiency:** Structured responses with built-in guidance reduce training time and ongoing coaching needs
5. **Quality Maintenance:** Better response structure maintains >98% accuracy while reducing computational complexity

---

## PRD-3: Real-Time System Feedback & Agent Control Framework

### Problem Statement

Silent loading states and lack of progress visibility create awkward silence during member calls, eroding agent confidence and member trust. Agents cannot predict response latency, cancel in-progress queries, or rephrase problematic requests. The absence of system state feedback forces agents to compensate by switching to legacy tools, abandoning queries, or creating uncomfortable call pauses.

**Evidence from UX Evaluation:**

- "Can't predict latency; compensates by switching tools" (P0 Priority - Roadmap Phase 2 Alignment)
- "Silent skeleton bars provide no meaningful system status" (P0 Priority)
- "While loading, agents can't interrupt a bad query" (P0 Priority - No stop/cancel control)
- Agent quote: "I've had members like, 'are you still there?'… it does take a bit of time"
- Agent quote: "I'm like waiting and waiting for it to respond"
- CASTLE Framework: "Task Efficiency = Poor (3/3)" due to unpredictable system behavior

### Strategic Alignment

- **Cost Impact:**

  - Reduced query abandonment through better user control (estimated 40% reduction in abandoned queries)
  - Decreased redundant tool usage and duplicate queries (estimated 25% reduction in unnecessary Minerva calls)
  - Transparent processing supports <15 second response time perception even when actual time varies
  - Lower training and support costs through predictable system behavior
- **Performance:** Aligns with roadmap Q2 2026 target: "63% response times reduction (40s→15s)" and "Increase Concurrency / Eliminate timeouts" (HyperCare Log ID:19-20)
- **Adoption:** Predictable system behavior increases agent trust and usage (critical for >80% Q3 adoption target)

### Success Metrics (Measurable)

- **Silence Reduction:** "Awkward silence" reports reduced by 70% (tracked via agent feedback and quality monitoring)
- **Query Abandonment:** Abandonment rate reduced by 40% (measured via incomplete query analytics)
- **Agent Confidence:** Confidence scores for system predictability improve from 2.8/5 to 4.0/5
- **Tool Switching:** Frequency of mid-query tool switching reduced by 50% (measured via session analytics)
- **Perceived Performance:** Agent-reported satisfaction with response speed >4.0/5 even when actual response times vary
- **Control Usage:** >60% of agents utilize cancel/rephrase controls within first 30 days of availability

### Key Capabilities

#### A. Intelligent Progress Indicators & Loading States

**Replaces:** Silent skeleton loader bars that provide no meaningful feedback

**Progressive Feedback System:**

**Phase 1: Query Submission (0-500ms)**

- **Visual State:** Immediate feedback on query receipt
- **Message:** "Processing your question..."
- **Indicator:** Animated pulse on query input with customer brand color
- **User Perception:** System responsiveness and acknowledgment

**Phase 2: Processing (500ms-5s)**

- **Visual State:** Determinate progress bar (if processing time predictable) or indeterminate spinner
- **Message:** Context-aware status labels:
  - "Searching benefit information..." (0-2s)
  - "Analyzing plan details..." (2-5s)
  - "Generating response..." (5s+)
- **Indicator:** Animated progress visualization with customer brand styling
- **Additional Context:** Display estimated time remaining (e.g., "Typically ~3-5 seconds")

**Phase 3: Extended Processing (5s-15s)**

- **Visual State:** Enhanced feedback acknowledging longer-than-expected wait
- **Message:** "Still working on it... Complex benefit requires detailed analysis"
- **Indicator:** Progress visualization with context-specific messaging
- **Agent Support:** Display suggested interim actions:
  - "Let your member know you're getting detailed information"
  - Suggested phrase: "I'm pulling up comprehensive details for you—just a moment"

**Phase 4: Timeout Approach (15s+)**

- **Visual State:** Warning state indicating approaching timeout
- **Message:** "Taking longer than expected. You can cancel and try rephrasing."
- **Agent Controls:** Prominent "Cancel" button; suggested alternative phrasing
- **Escalation Path:** "Contact support" option if repeated timeouts occur

**Context-Aware Loading Messaging:**

- **First Query in Session:** "Initializing benefits engine... ~5 seconds"
- **Formulary Query:** "Checking drug coverage and formulary... ~8 seconds"
- **Complex Multi-Part Query:** "Analyzing multiple benefits... ~10 seconds"
- **Follow-Up Query:** "Quick follow-up search... ~2 seconds"

**Visual Design Principles:**

- **Brand Consistency:** Loading indicators use customer brand colors and styling
- **Attention Management:** Subtle animation that indicates activity without being distracting
- **Accessibility:** Loading states announced to screen readers; focus management for keyboard users
- **Performance Budget:** Loading indicators themselves must render in <100ms to maintain perceived responsiveness

#### B. Agent Control Framework: Cancel, Rephrase, and Fallback

**Problem Addressed:** Agents currently have no way to interrupt, modify, or abandon in-progress queries

**Cancel Control:**

- **Visual Placement:** Prominent "Cancel" button adjacent to progress indicator (always visible during processing)
- **Interaction:** Single-click cancellation with immediate feedback
- **Behavior on Cancel:**

  - Halt Minerva API request (server-side abort if possible)
  - Display cancellation confirmation: "Query canceled. Ready for new question."
  - Preserve query text in input field for easy editing
  - Log cancellation event for analytics (understand common cancellation triggers)
- **Use Cases:**

  - Agent realizes query is poorly phrased mid-processing
  - Member changes their question before response arrives
  - Response taking too long; agent needs to fall back to legacy tool
  - Accidental query submission

**Rephrase Control:**

- **Visual Placement:** "Rephrase" link or button near cancel control
- **Interaction:** Click to cancel current query and activate input field with original query text pre-populated for editing
- **Smart Suggestions:** If timeout or error occurs, system suggests rephrase options:
  - "Try asking about specific benefit categories (e.g., 'What's the copay for office visits?')"
  - "Break complex questions into separate queries"
  - "Verify plan ID and member eligibility are correct"

**Fallback Mechanisms:**

- **Quick Escape Hatch:** "Use Nexus Instead" button that deep-links to relevant Nexus section
- **Partial Results:** If query partially completed, offer: "Show what we found so far" option
- **Alternative Query Suggestions:** Based on original query, suggest simpler or related queries more likely to succeed

**Keyboard Shortcuts:**

- **Esc Key:** Cancel current query
- **Cmd/Ctrl + R:** Rephrase (cancel and re-focus input)
- **Cmd/Ctrl + N:** New query (clear input and start fresh)

#### C. System State Visibility & Transparency

**Objective:** Agents always understand what the system is doing and why

**Status Dashboard (Minimal, Non-Intrusive):**

- **Connection Status:** Green indicator: "Connected" | Yellow: "Slow Connection" | Red: "Connection Issues"
- **Service Health:** Real-time system health indicator

  - Green: "All systems operational"
  - Yellow: "Experiencing delays" (with estimated delay context)
  - Red: "Service degraded" (with fallback recommendations)
- **Session Context:** Display session metadata for agent awareness

  - Current plan ID and member context (if applicable)
  - Query count in current session
  - Last successful query timestamp

**Performance Expectations Setting:**

- **First-Time User Onboarding:** Brief tooltip on first query: "Most queries return in 3-8 seconds"
- **Persistent Performance Context:** After first query, display: "Average response time today: 5.2s" (dynamically updated)
- **Transparency During Issues:** If system experiencing degraded performance: "Response times currently 2x normal due to high volume"

**Error State Visibility:**

- **Immediate Error Feedback:** If query fails, display diagnostic error message (see PRD-5 for detailed error handling)
- **Historical Error Context:** If agent experiences repeated errors: "You've had 3 errors in this session—contact support if this continues"

#### D. Cost-Aware Processing & Resource Optimization

**Purpose:** Maintain responsive feedback while supporting $0.08 per query cost target

**Intelligent Resource Allocation:**

- **Quick Response Prioritization:** Simple queries (e.g., copay lookups) prioritized in processing queue
- **Complexity-Based Routing:** Complex queries routed to optimized processing pipelines
- **Caching Intelligence:** Frequently asked questions served from cache with <1s response time
- **Predictive Pre-Loading:** Based on session context, anticipate likely follow-up queries and pre-warm cache

**Cost-Efficient Progress Indication:**

- **Client-Side Rendering:** All progress indicators rendered client-side to minimize server load
- **Efficient Polling:** If progress updates require server polling, use exponential backoff to minimize API calls
- **Streaming Responses:** Where possible, stream response chunks for incremental display (reducing perceived latency)

**Performance Monitoring & Optimization:**

- **Real-Time Latency Tracking:** Monitor p50, p95, p99 response times per customer
- **Automatic Escalation:** If latency exceeds thresholds, trigger engineering alerts
- **Agent-Visible Feedback Loop:** Allow agents to report "felt slow" for qualitative performance tracking

### White-Label & Configuration Capabilities

**Progress Indicator Customization:**

- **Visual Style:** Brand-consistent progress bars, spinners, or custom animations
- **Messaging Tone:** Customer-specific voice (formal vs conversational)
- **Timeout Thresholds:** Configurable timeout values per customer (based on their performance SLAs)

**Control Availability:**

- **Cancel Control:** Enable/disable per customer (some may prefer no-cancel to ensure query completion logging)
- **Rephrase Suggestions:** Toggle automatic suggestion system on/off
- **Fallback Options:** Customize fallback links (e.g., link to customer's preferred legacy tool)

**Status Dashboard Configuration:**

- **Visibility Level:** Full dashboard | Minimal indicators | Hidden (for simplified deployments)
- **Health Indicator Sensitivity:** Thresholds for yellow/red health status per customer tolerance
- **Performance Context:** Show/hide average response time messaging per customer preference

### Implementation Scope & Phasing

**Phase 1 - Q2 2026 (4 weeks):**

- **In-Scope:**

  - Progressive loading states with context-aware messaging (Phase 1-3 feedback)
  - Cancel control with immediate query termination
  - Basic system health indicator
  - Timeout warning state (Phase 4 feedback)
  - Client-side progress rendering framework
- **Out-of-Scope:**

  - Advanced streaming responses (Q3 performance optimization)
  - Predictive pre-loading and caching intelligence (Q3-Q4 roadmap)
  - Detailed performance analytics dashboard (separate PRD: Performance Dashboard)
  - Mobile-optimized progress indicators (desktop-first)

**Phase 2 - Q3 2026 (3 weeks):**

- Rephrase control with smart suggestion engine
- Fallback mechanism integration with customer legacy systems
- Enhanced status dashboard with session context
- Keyboard shortcuts for power users

### Dependencies & Risks

**Dependencies:**

- Minerva API support for query cancellation (server-side abort capability)
- Real-time system health monitoring infrastructure
- Performance data pipeline for latency tracking and reporting

**Risks:**

- **Cancel Behavior:** Risk of cancel requests not terminating server-side processing, continuing to incur costs

  - *Mitigation:* Implement proper API abort handling; track canceled query costs; set abort timeout limits
- **Progress Accuracy:** Risk of progress indicators being inaccurate if processing time unpredictable

  - *Mitigation:* Use indeterminate indicators for unpredictable operations; calibrate estimates based on historical data
- **User Trust:** Risk of too many warnings/alerts eroding confidence in system reliability

  - *Mitigation:* Calibrate thresholds carefully; focus on actionable feedback; test messaging with agent focus groups

### Cost-Optimization Contribution

This PRD directly supports primary cost optimization objective:

1. **Reduced Abandoned Queries:** 40% reduction in abandonment saves wasted API costs (estimated $0.02-0.04 per abandoned query)
2. **Decreased Redundant Queries:** Better control reduces duplicate queries and tool switching (estimated 25% reduction in unnecessary calls)
3. **Efficient Resource Usage:** Intelligent progress indication and cancellation optimize server resource utilization
4. **Training Reduction:** Predictable system behavior reduces training time by 30% (estimated $300-500 per agent savings)
5. **Support Cost Reduction:** Transparent system state reduces "system not responding" support tickets by 60%

---

## PRD-4: Context-Aware Workflow Integration & Verification Support

### Problem Statement

Current interface obscures underlying Nexus content and other source systems, forcing agents to switch back and forth for verification. This creates inefficiency, reduces trust in AI responses, and increases compliance risk in audited environments. Agents need seamless side-by-side verification workflows that maintain spatial continuity while providing transparent source citations and deep-linked access to underlying benefit information.

**Evidence from UX Evaluation:**

- "Fixed placement blocks key benefit fields and prevents side-by-side verification" (P1 Priority)
- "Sources hidden behind low-affordance 'Expand Table' can be missed" (P1 Priority)
- "Mira shows where information comes from, but does not support real-time verification actions" (P1 Priority - No deep links)
- Agent quote: "I still want to verify… I can't help but to just double check"
- Agent quote: "They always want to know… if we get audited, where did we get that information from"
- "Trust but verify" behavior repeatedly observed in user sessions

### Strategic Alignment

- **Cost Impact:**

  - Reduced verification overhead through seamless workflow integration (estimated 30% reduction in verification time)
  - Decreased tool-switching overhead reduces average handle time (estimated 10-15% AHT improvement)
  - Transparent sourcing reduces post-call verification and escalations
  - Efficient parallel workflows support higher query volume per agent
- **Quality:** Parallel verification supports >98% accuracy maintenance through agent confidence and source transparency
- **Compliance:** Audit trail preservation and source transparency critical for regulatory environments

### Success Metrics (Measurable)

- **Verification Workflow Time:** Time spent on benefit verification reduced by 50% (measured via session analytics)
- **Context Switching:** Agent context switching between systems reduced by 60% (measured via user interaction tracking)
- **Audit Compliance:** Audit compliance score maintained at >95% (tracked via quality monitoring)
- **Source Link Usage:** >70% of agents utilize deep-link citations within first 30 days
- **Agent Trust:** Self-reported trust in AI responses increases from 3.5/5 to 4.5/5
- **Workflow Disruption:** Agent-reported workflow disruption reduced by 60% (supports Q2 KR5 target)

### Key Capabilities

#### A. Side-by-Side Verification Architecture

**Purpose:** Enable simultaneous viewing of CSR Chat responses and underlying source content (Nexus, plan documents)

**Dual-Panel Integration:**

**Option 1: CSR Chat + Nexus Parallel View (Recommended for Nexus Integration)**

- **Layout:** CSR Chat panel (30-40% width, resizable) + Nexus content (60-70% width)
- **Behavior:** CSR Chat overlays or docks alongside Nexus without obscuring critical benefit fields
- **Synchronization:** When CSR Chat returns response, Nexus automatically navigates to cited source section
- **Agent Control:** Drag to reposition; resize panel boundary; collapse CSR Chat to maximize Nexus view

**Option 2: Picture-in-Picture Citation Preview**

- **Layout:** Small preview window showing source content alongside response
- **Behavior:** Click citation link → preview overlay displays source excerpt without leaving CSR Chat
- **Use Case:** Quick verification without full context switch
- **Agent Control:** Expand preview to full view; close preview to return to CSR Chat

**Option 3: Embedded Iframe Source Display**

- **Layout:** Within CSR Chat response, collapsible iframe displays source content inline
- **Behavior:** Click "View Source" → iframe expands showing Nexus benefit section
- **Use Case:** All-in-one verification without leaving CSR Chat interface
- **Agent Control:** Expand/collapse iframe; open in full Nexus view

**Spatial Continuity Principles:**

- **Persistent Positioning:** CSR Chat maintains position across queries (no full-screen takeover mid-session)
- **Smooth Transitions:** Animated transitions when resizing or repositioning (avoid jarring layout shifts)
- **Context Preservation:** Underlying content remains visible and accessible throughout agent interaction
- **Anchor Points:** CSR Chat can "dock" to Nexus interface edges for predictable spatial relationship

#### B. Deep-Linked Source Citations & Transparency

**Problem Addressed:** Sources displayed but not actionable; agents must manually navigate to verify

**Intelligent Citation System:**

**Citation Types:**

1. **Plan Document Citations:**

   - **Display:** "Source: [Plan Name] Evidence of Coverage, Section 3.2: Medical Benefits"
   - **Action:** Click → Deep link to PDF page 47, Section 3.2 with highlight on relevant paragraph
   - **Context:** Display plan effective dates, version, and document type
2. **Nexus Benefit Section Citations:**

   - **Display:** "Source: Nexus → Medical Benefits → Office Visits"
   - **Action:** Click → Navigate to specific Nexus benefit section, highlight relevant field
   - **Context:** Display last updated timestamp, data source (carrier file, manual entry)
3. **Formulary Database Citations:**

   - **Display:** "Source: Formulary Database → [Drug Name] Tier 2, Requires Prior Auth"
   - **Action:** Click → Open formulary lookup tool pre-populated with drug name and plan context
   - **Context:** Display formulary effective date, tier information
4. **Multi-Source Aggregation Citations:**

   - **Display:** "Synthesized from: EOC Section 4.1 + Nexus Deductible + Formulary Rules"
   - **Action:** Expandable list showing each source with individual deep links
   - **Context:** Indicate which parts of response came from which sources

**Citation Presentation:**

**Collapsed State (Default):**

- **Position:** Footer of each response tier (Tier 1, Tier 2)
- **Visual:** Subtle link: "Sources (3)" with document icon
- **Affordance:** Underline on hover; click to expand
- **Accessibility:** Keyboard accessible; screen reader announcement

**Expanded State:**

- **Layout:** Accordion-style expansion showing detailed source list
- **Visual Treatment:** Each source as clickable card with icon, title, and deep-link action
- **Metadata Display:** Source type, date, version, confidence indicator
- **Bulk Actions:** "Open All Sources in New Tabs" for comprehensive verification

**Audit Trail Integration:**

- **Source Capture:** When agent copies response to notes, automatically append source citations
- **Timestamping:** Log exact timestamp of source data retrieval for audit purposes
- **Version Tracking:** If plan document updated, flag responses based on outdated versions

#### C. Context Preservation & Session Management

**Purpose:** Maintain agent workflow continuity across queries and sessions

**Session State Persistence:**

- **Query History:** Maintain visible query history within session (scrollable sidebar or timeline view)
- **Response Persistence:** Previous responses remain accessible via history (avoid disappearing context)
- **Source Context:** Remember last-accessed Nexus section for continuity across queries
- **Panel State:** Persist panel position, size, and workspace mode across page reloads

**Contextual Query Intelligence:**

- **Member Context Awareness:** If agent has member ID in Nexus, pre-populate CSR Chat with member plan context
- **Plan Context Persistence:** Remember active plan across queries (avoid re-asking)
- **Follow-Up Query Detection:** Recognize follow-up queries and maintain context ("What about specialists?" following "What's the PCP copay?")

**Cross-Session Continuity:**

- **Agent Preferences:** Remember agent's preferred layout, workspace mode, disclosure settings across days/weeks
- **Frequent Queries:** Surface agent's most common queries for quick re-execution
- **Bookmarked Responses:** Allow agents to bookmark useful responses for future reference

#### D. Audit Trail & Compliance Support

**Purpose:** Provide complete documentation trail for regulatory and quality audits

**Automatic Documentation Capture:**

- **Query Logging:** Every query timestamped with agent ID, member context, plan context
- **Response Versioning:** Store exact response delivered to agent (with version ID)
- **Source Attribution:** Log all source documents consulted for response generation
- **Agent Actions:** Track which responses copied to notes, which sources clicked, verification behaviors

**Compliance Export Capabilities:**

- **Call Documentation Export:** Generate audit-ready export of query/response/source for specific call
- **Bulk Audit Reports:** Export all queries for a time period, agent, or plan for compliance review
- **Format Options:** PDF, CSV, JSON formats for different audit use cases

**Regulatory Requirement Tracking:**

- **State-Specific Rules:** Flag responses that include state-mandated disclosures
- **ACA Requirements:** Indicate when response covers ACA essential health benefits
- **HIPAA Compliance:** Ensure audit trail meets HIPAA documentation requirements

**Quality Monitoring Integration:**

- **Sample Exports:** Enable quality team to sample queries for review
- **Error Flagging:** Allow quality team to flag incorrect responses for retraining
- **Agent Performance Tracking:** Provide metrics on query quality, verification behaviors, accuracy

### White-Label & Configuration Capabilities

**Integration Patterns:**

- **Nexus Integration:** Pre-built integration with deep-link API for Blue Shield of California
- **Generic Integration Framework:** Configurable deep-link patterns for other customer source systems
- **Citation Customization:** Customer-defined citation format, terminology, and source types
- **Audit Trail Customization:** Configurable retention periods, export formats, compliance requirements

**Layout Configuration:**

- **Side-by-Side Enablement:** Toggle side-by-side mode on/off per customer deployment
- **Default Layout:** Configure default CSR Chat position relative to customer application
- **Verification Pattern Preference:** Select preferred verification pattern (parallel view, PIP, embedded iframe)

**Source System Integration:**

- **Deep-Link Mapping:** Configure URL patterns for customer source systems
- **Authentication Handling:** SSO integration for seamless deep-link navigation
- **Source System API Integration:** If customer source system has API, direct integration for inline display

### Implementation Scope & Phasing

**Phase 1 - Q2 2026 (5 weeks):**

- **In-Scope:**

  - Side-by-side panel architecture (parallel view with Nexus)
  - Basic deep-link citation system (Nexus benefit sections)
  - Citation expand/collapse UI with source links
  - Session state persistence (panel position, query history)
  - Basic audit trail logging (query, response, timestamp)
- **Out-of-Scope:**

  - Advanced multi-source aggregation citations (Q3)
  - Cross-session continuity and bookmarking (Q3-Q4)
  - Complex audit export formats (compliance team to define requirements)
  - Generic integration framework for non-Nexus systems (Q3 roadmap)

**Phase 2 - Q3 2026 (4 weeks):**

- Picture-in-picture citation preview mode
- Enhanced audit trail with agent action tracking
- Compliance export capabilities
- Follow-up query context intelligence
- Generic deep-link framework for customer source systems

### Dependencies & Risks

**Dependencies:**

- Nexus deep-link API access and documentation
- Plan document hosting with stable URL schemes for deep-linking
- SSO integration for seamless navigation to source systems
- Customer source system APIs or URL patterns

**Risks:**

- **Deep-Link Fragility:** Risk of deep-links breaking if source system URLs change

  - *Mitigation:* Stable URL API contracts; fallback to top-level navigation if deep-link fails; automated link validation testing
- **Source System Performance:** Risk of slow source system load impacting verification workflow

  - *Mitigation:* Async loading for deep-links; loading indicators; timeout handling with fallback options
- **Citation Accuracy:** Risk of incorrect source attribution reducing agent trust

  - *Mitigation:* Rigorous source mapping validation; agent feedback mechanism for reporting attribution errors; regular audits

### Cost-Optimization Contribution

This PRD directly supports primary cost optimization objective:

1. **Reduced Verification Time:** 50% reduction in verification overhead translates to lower average handle time (estimated 5-8% AHT improvement)
2. **Decreased Tool Switching:** 60% reduction in context switching reduces cognitive overhead and improves efficiency
3. **Lower Training Costs:** Transparent sourcing and built-in verification reduce training time by 30%
4. **Compliance Cost Avoidance:** Audit trail automation reduces manual documentation time and compliance investigation costs
5. **Higher Agent Productivity:** Seamless workflows enable agents to handle more queries per shift (estimated 10-15% productivity gain)

---

## PRD-5: Intelligent Error Handling & Recovery Framework

### Problem Statement

Current error responses fail to support agent recovery, providing only generic messages that stop task completion and provide no diagnostic context or next steps. Agents experiencing errors must escalate to support, abandon the tool, or guess at solutions—all of which reduce adoption, increase support costs, and disrupt member calls. The absence of intelligent error handling creates uncertainty and erodes trust in system reliability.

**Evidence from UX Evaluation:**

- "Generic errors stop task completion" (P1 Priority - Roadmap Phase 2 Alignment: HyperCare Log ID:19-20)
- "Error states: Replace generic errors with diagnostic states, preserve prompt context, offer guided recovery" (P1 Priority Design Recommendation)
- CASTLE Framework: "Errors = Difficult Resolution (3/3)" - Agents cannot recover independently
- Roadmap: "Reduce error rate and timeout events to zero or near zero" (Q2 2026 Performance target)

### Strategic Alignment

- **Cost Impact:**

  - Reduced support escalations through self-service error recovery (estimated 60% reduction in error-related support tickets)
  - Lower training costs through contextual error guidance
  - Decreased query abandonment due to recoverable errors (estimated 50% reduction in error-driven abandonment)
  - Improved system utilization through confidence in error resilience
- **Performance:** Directly supports roadmap Q2 2026 target: "Reduce error rate and timeout events to zero or near zero"
- **Adoption:** Robust error handling increases agent trust and willingness to rely on system (critical for >80% Q3 adoption target)

### Success Metrics (Measurable)

- **Error Recovery Rate:** >75% of errors resolved by agent without support escalation
- **Support Ticket Reduction:** Error-related support tickets reduced by 60%
- **Query Abandonment:** Abandonment following errors reduced by 50%
- **Agent Trust:** Confidence in system reliability increases from 2.9/5 to 4.2/5
- **Error Resolution Time:** Average time from error to successful query reduced by 70%
- **Self-Service Success:** >80% of agents utilize guided recovery options without external help

### Key Capabilities

#### A. Diagnostic Error Classification & Messaging

**Replaces:** Generic "Something went wrong" messages with no context

**Error Classification System:**

**Category 1: User Input Errors (Agent-Recoverable)**

**1.1: Insufficient Plan Context**

- **Scenario:** Agent queries without specifying plan ID or member eligibility
- **Error Message:** "We need plan information to answer this question"
- **Diagnostic Detail:** "No active plan ID detected. Please select a member or enter plan ID."
- **Guided Recovery:**
  - Action button: "Select Member in Nexus"
  - Alternative: Manual plan ID input field
  - Context help: "Find plan ID in Nexus under Member Profile"

**1.2: Ambiguous or Unclear Query**

- **Scenario:** Query too vague for system to interpret intent
- **Error Message:** "This question needs more specifics"
- **Diagnostic Detail:** "We couldn't identify which benefit you're asking about."
- **Guided Recovery:**
  - Suggested rephrase: "Try asking: 'What's the copay for primary care office visits?'"
  - Common benefit categories: Clickable chips (Office Visits, Prescriptions, Hospital, etc.)
  - Context help: Tips for effective queries

**1.3: Out-of-Scope Query**

- **Scenario:** Agent asks about non-benefit topic (billing, claims status, etc.)
- **Error Message:** "That's outside my expertise"
- **Diagnostic Detail:** "I specialize in benefit coverage questions. For billing or claims, use [Customer System Name]."
- **Guided Recovery:**
  - Deep link to appropriate system for query type
  - Suggested alternative: "I can answer benefit questions like: [examples]"

**Category 2: Data Availability Errors (System-Recoverable)**

**2.1: Plan Data Not Yet Onboarded**

- **Scenario:** Query for plan not yet in Minerva system
- **Error Message:** "Plan data not available yet"
- **Diagnostic Detail:** "Plan ID [12345] hasn't been onboarded to CSR Chat. You can check Nexus or request plan onboarding."
- **Guided Recovery:**
  - Action button: "Open Plan in Nexus" (deep link)
  - Action button: "Request Plan Onboarding" (creates ticket)
  - Estimated onboarding timeline: "Typically added within 2-3 business days"

**2.2: Formulary Data Unavailable**

- **Scenario:** Prescription query when formulary not integrated for this plan
- **Error Message:** "Prescription coverage not available yet"
- **Diagnostic Detail:** "Formulary data for this plan is coming in Q3 2026. Use [Formulary Tool Name] for now."
- **Guided Recovery:**
  - Deep link to customer's formulary tool
  - Action button: "Notify Me When Available" (creates watch list)

**2.3: Outdated Plan Data**

- **Scenario:** Plan data exists but flagged as potentially outdated (annual plan change detected)
- **Error Message:** "Plan data may be outdated"
- **Diagnostic Detail:** "This plan was recently updated. Response based on [Date] version—verify in Nexus for latest."
- **Guided Recovery:**
  - Proceed with caution: "Show response anyway" (with prominent outdated warning)
  - Safe alternative: "Open Current Plan in Nexus"
  - Action button: "Request Plan Data Refresh"

**Category 3: System Performance Errors (Infrastructure-Related)**

**3.1: Timeout Error**

- **Scenario:** Query exceeds processing time limit (>15-20 seconds)
- **Error Message:** "Request timed out"
- **Diagnostic Detail:** "Complex query took too long. Try simplifying or breaking into parts."
- **Guided Recovery:**
  - Action button: "Retry Query" (with caching for faster retry)
  - Suggested simplification: "Ask about one benefit at a time (e.g., just copays, not entire plan)"
  - Fallback: "Use Nexus for Complex Research"
  - Automatic incident log: Send diagnostic data to engineering for performance investigation

**3.2: Service Degradation**

- **Scenario:** Minerva API experiencing high latency or partial outage
- **Error Message:** "System running slowly"
- **Diagnostic Detail:** "We're experiencing high volume. Responses may be delayed or unavailable."
- **Guided Recovery:**
  - Status indicator: "Estimated wait: 2-3x normal" or "Service partially unavailable"
  - Action button: "Retry in a moment"
  - Fallback: "Use Nexus until service restores" (prominent, guilt-free fallback)
  - Proactive notification: "We'll notify you when service is back to normal"

**3.3: Unexpected System Error**

- **Scenario:** Unhandled exception or infrastructure failure
- **Error Message:** "Unexpected error occurred"
- **Diagnostic Detail:** "Something went wrong on our end (Error Code: [UUID]). This has been logged."
- **Guided Recovery:**
  - Action button: "Try Again" (simple retry)
  - Action button: "Report Issue" (pre-populated support form with error code)
  - Fallback: "Use Nexus while we investigate"
  - Context preservation: Original query saved for easy retry after resolution

#### B. Context Preservation & Retry Intelligence

**Purpose:** Don't make agents start over after errors—preserve context and enable smart retries

**Query Preservation:**

- **Automatic Save:** Original query text preserved in input field after error
- **Editable Retry:** Agent can edit query and resubmit without retyping
- **Session Context:** If error related to missing context (plan ID), maintain query while agent provides context

**Smart Retry Logic:**

- **Exponential Backoff:** For timeout/service errors, implement intelligent retry timing (don't immediately retry if system overloaded)
- **Cached Retry:** If query retried within 5 minutes, use cached partial results if available for faster response
- **Alternative Routing:** For repeated errors on same query, route to alternative processing pipeline or simplified response mode

**Multi-Error Recovery Tracking:**

- **Error Frequency Awareness:** If agent experiences 3+ errors in session, proactively offer help:
  - "You've had several errors. Need assistance? [Contact Support] [View Help Docs]"
- **Pattern Detection:** If same error type repeated (e.g., multiple ambiguous queries), offer targeted guidance:
  - "Tip: For best results, ask about specific benefits like 'office visit copay' or 'deductible amount'"

#### C. Guided Recovery Workflows

**Purpose:** Transform error moments into learning opportunities and self-service resolution

**Interactive Recovery UI:**

**Visual Design:**

- **Error State Card:** Distinct visual treatment (yellow/orange for user-recoverable; red for system errors)
- **Icon System:** Diagnostic icon indicating error category (⚠️ user input, 🔄 retry, ⚙️ system)
- **Structured Layout:**
  1. Error headline (what happened)
  2. Diagnostic detail (why it happened)
  3. Guided recovery actions (what to do next)
  4. Additional context (help docs, support)

**Action Hierarchy:**

- **Primary Action:** Most likely resolution (e.g., "Rephrase Query", "Open Nexus")
- **Secondary Actions:** Alternative paths (e.g., "Try Again", "Contact Support")
- **Tertiary Links:** Help documentation, FAQ, system status page

**Inline Guidance:**

- **Query Assistance:** For ambiguous query errors, provide inline examples of well-formed queries
- **Common Fixes:** Display top 3 common resolutions for this error type
- **Contextual Help:** Based on error category, surface relevant help documentation sections

**Escalation Path:**

- **Support Contact:** One-click support form pre-populated with error context, agent ID, query text, error code
- **Incident Tracking:** Provide agent with incident reference number for follow-up
- **SLA Transparency:** Set expectations: "Support typically responds within 2 hours"

#### D. Error Analytics & Continuous Improvement

**Purpose:** Use error data to improve system reliability and user experience

**Agent-Visible Error Insights:**

- **Personal Error Dashboard:** Show agent their error frequency, common error types, resolution success
- **Comparative Context:** "Your error rate: 2% | System average: 3%" (no shaming—positive framing)
- **Learning Resources:** Based on error patterns, suggest relevant training or help docs

**System-Level Error Monitoring:**

- **Error Rate Tracking:** Real-time monitoring of error rates by type, customer, plan
- **Threshold Alerting:** Automatic escalation if error rates exceed acceptable thresholds
- **Root Cause Analysis:** Automated tagging of errors for engineering investigation
- **Feedback Loop:** Error patterns inform product roadmap and Minerva API improvements

**Proactive Error Prevention:**

- **Query Validation:** Client-side validation catches common errors before submission (e.g., empty query, invalid characters)
- **Contextual Warnings:** If query likely to fail, proactive warning: "This plan doesn't include dental coverage—did you mean medical benefits?"
- **Input Assistance:** Autocomplete, suggested queries, and query templates reduce malformed queries

### White-Label & Configuration Capabilities

**Error Messaging Customization:**

- **Tone & Voice:** Customer-defined error message tone (formal, conversational, empathetic)
- **Terminology:** Custom product names, system names, fallback tool names
- **Escalation Paths:** Customer-specific support contact methods (email, phone, ticketing system)

**Error Handling Behavior:**

- **Retry Limits:** Configurable retry attempts before forcing fallback
- **Timeout Thresholds:** Customer-defined timeout values based on their performance expectations
- **Fallback Preferences:** Configure preferred fallback system (Nexus, legacy tool, manual lookup)

**Error Visibility:**

- **Error Dashboard Access:** Configure which agents/roles see error analytics
- **Incident Reporting:** Customize support escalation workflows and ticketing integration
- **Error Logging:** Configure error log retention, export formats, compliance requirements

### Implementation Scope & Phasing

**Phase 1 - Q2 2026 (4 weeks):**

- **In-Scope:**

  - Diagnostic error classification (Category 1: User Input, Category 2: Data Availability)
  - Context preservation and query retry
  - Guided recovery UI with primary/secondary actions
  - Basic error logging and incident tracking
  - Customer configuration for error messaging tone
- **Out-of-Scope:**

  - Advanced error analytics dashboard (Q3-Q4 roadmap)
  - Predictive error prevention (Q3 performance optimization)
  - Complex escalation workflow automation (depends on customer ticketing integrations)
  - Mobile-optimized error states (desktop-first)

**Phase 2 - Q3 2026 (3 weeks):**

- System performance errors (Category 3: Timeouts, Service Degradation)
- Smart retry logic with caching and alternative routing
- Multi-error recovery tracking and proactive assistance
- Agent error dashboard with insights and learning resources

### Dependencies & Risks

**Dependencies:**

- Minerva API error response structure supporting diagnostic detail (not just generic 500 errors)
- Error logging infrastructure for analytics and monitoring
- Customer support system integration for escalation workflows

**Risks:**

- **Over-Explanation:** Risk of error messages being too verbose, slowing recovery

  - *Mitigation:* Progressive disclosure: headline + detail expandable; test messaging with agent focus groups
- **False Confidence:** Risk of guided recovery suggesting wrong path, worsening agent frustration

  - *Mitigation:* Conservative recovery suggestions; always offer fallback; track recovery success rates and refine
- **Support Escalation:** Risk of error analytics creating anxiety or performance pressure for agents

  - *Mitigation:* Positive framing; comparative context; focus on learning not blame; opt-in visibility

### Cost-Optimization Contribution

This PRD directly supports primary cost optimization objective:

1. **Reduced Support Costs:** 60% reduction in error-related support tickets (estimated $50K-80K annual savings)
2. **Decreased Abandonment:** 50% reduction in error-driven query abandonment saves wasted API costs
3. **Higher Adoption:** Robust error handling increases agent confidence and sustained usage
4. **Training Efficiency:** Contextual error guidance reduces training time by 25%
5. **System Reliability:** Error analytics inform infrastructure improvements, reducing costly downtime and performance issues

---

## PRD-6: Enhanced Agent Experience & Productivity Enablers

### Problem Statement

Current interface suffers from low discoverability of controls, weak onboarding guidance, accessibility concerns, and missing productivity features that slow agent workflows. While other PRDs address structural UX issues (layout, response architecture, system feedback), this PRD focuses on the "polish" and productivity enhancements that transform CSR Chat from functional to delightful and that accelerate agent proficiency.

**Evidence from UX Evaluation:**

- "Low discoverability of resize/collapse affordances" (P2 Priority)
- "Weak onboarding—'Message Mira' doesn't guide what to ask" (P2 Priority)
- "Low contrast and over-bolding reduce scanability; accessibility risk" (P2 Priority)
- Agent quote: "I didn't know that little arrow feature… I thought I had to exit out of the whole thing"
- Agent quote: "I might not necessarily know if the way I'm entering a question is a way that the system's going to really recognize"

### Strategic Alignment

- **Cost Impact:**

  - Reduced training time through better onboarding and discoverability (estimated 40% reduction in training duration)
  - Increased agent productivity through keyboard shortcuts and productivity tools (estimated 10-15% efficiency gain)
  - Lower support costs through better self-service guidance (estimated 30% reduction in "how-to" support tickets)
- **Adoption:** Delightful, productive experience increases agent preference for tool over legacy workflows
- **Quality:** Accessibility compliance and better UX reduce agent errors and fatigue

### Success Metrics (Measurable)

- **Time-to-Proficiency:** Agent onboarding time reduced by 40% (target: <90 minutes to independent usage)
- **Feature Discovery:** >85% of agents discover and utilize movable panel, workspace modes, keyboard shortcuts within first week
- **Accessibility Compliance:** 100% WCAG 2.1 AA compliance (verified via automated and manual audits)
- **Productivity Gains:** Agent self-reported productivity improvement >15% (measured via quarterly satisfaction surveys)
- **Support Ticket Reduction:** "How-to" support tickets reduced by 30%
- **Agent Satisfaction:** Overall UX satisfaction >4.5/5

### Key Capabilities

#### A. Intelligent Onboarding & First-Run Experience

**Purpose:** Accelerate agent proficiency and reduce initial confusion

**First-Launch Tutorial (Optional, Dismissible):**

- **Welcome Screen:** Brief introduction to CSR Chat capabilities and value proposition
- **Interactive Walkthrough:** 3-5 step tutorial highlighting key features:

  1. How to ask a question (suggested query examples)
  2. How to interpret responses (Tier 1/2/3 hierarchy)
  3. How to verify sources (citation links)
  4. How to customize interface (movable panel, workspace modes)
  5. Where to get help (help icon, support contact)
- **User Control:** "Skip Tutorial" option; "Remind Me Later" option; Never auto-repeat after dismissal
- **Progress Tracking:** Tutorial progress saved (resume if interrupted)

**Contextual Tooltips & Coachmarks:**

- **Triggered on Hover:** First time user hovers over control (e.g., panel resize handle), show tooltip: "Drag to resize"
- **One-Time Display:** Each coachmark shown once; dismissed after interaction or explicit close
- **Priority Sequence:** Show most critical coachmarks first (movable panel, cancel control, source citations)

**Onboarding Checklist (Optional Dashboard Widget):**

- **Gamified Progress:** "Getting Started with CSR Chat" checklist:
  - ✅ Ask your first question
  - ✅ Verify a source citation
  - ✅ Customize your workspace
  - ✅ Use a keyboard shortcut
- **Incentive:** Completion badge or recognition (optional per customer culture)

#### B. Discoverable UI Controls & Affordances

**Purpose:** Make all interface capabilities obvious through visual design

**Visual Affordance Principles:**

**1. Movable Panel Affordance:**

- **Drag Handle:** Visible header bar with grip texture/icon indicating draggable area
- **Cursor Feedback:** Cursor changes to move icon on hover over drag handle
- **First-Use Coachmark:** "Click and drag to reposition" tooltip on first session

**2. Resizable Panel Affordance:**

- **Resize Handle:** Visible vertical bar between CSR Chat and adjacent content with resize cursor
- **Visual Hint:** Subtle double-arrow icon or texture on resize handle
- **Snap Guides:** When dragging resize handle, show snap guidelines for common widths (25%, 33%, 50%)

**3. Collapsible Sections Affordance:**

- **Consistent Icons:** Chevron (▼/▶) or plus/minus icons for all expandable sections
- **Hover State:** Highlight entire header area on hover to indicate clickability
- **Keyboard Hint:** Show "(Enter to expand)" on focus for keyboard users

**4. Workspace Mode Switcher:**

- **Prominent Placement:** Mode switcher in panel header (Live Call | Research | Documentation)
- **Visual State:** Active mode highlighted with customer brand color
- **Tooltip on Hover:** Brief description of each mode: "Live Call: Minimal view for active calls"

**5. Help & Support Access:**

- **Persistent Help Icon:** Question mark icon in panel header (always visible)
- **Click Behavior:** Opens help panel or modal with:
  - Quick tips
  - Keyboard shortcuts reference
  - Link to full documentation
  - Contact support

#### C. Accessibility Compliance & Inclusive Design

**Purpose:** Ensure CSR Chat usable by all agents regardless of abilities

**WCAG 2.1 AA Compliance Requirements:**

**Visual Design:**

- **Contrast Ratios:**
  - Body text: Minimum 4.5:1 contrast ratio
  - Large text (18px+ or 14px+ bold): Minimum 3:1
  - Interactive controls: Minimum 3:1
- **Color Independence:** Never rely solely on color to convey information (use icons, text labels, patterns)
- **Text Sizing:** Support browser zoom up to 200% without loss of functionality
- **Readable Typography:** Clear, legible fonts; adequate line height (1.5x font size); no justified text

**Keyboard Navigation:**

- **Full Keyboard Access:** All functionality accessible via keyboard (no mouse-only interactions)
- **Logical Tab Order:** Tab navigation follows visual flow (top-to-bottom, left-to-right)
- **Focus Indicators:** High-visibility focus rings (2px solid outline, customer brand color)
- **Keyboard Shortcuts:** See section D below

**Screen Reader Support:**

- **Semantic HTML:** Proper heading hierarchy (H1, H2, H3), landmark regions (main, nav, complementary)
- **ARIA Labels:** All interactive controls have descriptive labels
- **Live Regions:** Dynamic content (loading states, new responses) announced via ARIA live regions
- **Alt Text:** All icons have descriptive alt text or aria-label

**Motion & Animation:**

- **Reduced Motion Support:** Respect `prefers-reduced-motion` user preference (disable animations)
- **Pauseable Animations:** Any auto-scrolling or animated content can be paused
- **No Flashing Content:** Avoid flashing content (seizure risk)

**Form & Input Accessibility:**

- **Input Labels:** All form fields have visible, associated labels
- **Error Indication:** Errors indicated with text, not just color; announced to screen readers
- **Input Instructions:** Provide clear instructions for complex inputs (e.g., query format suggestions)

#### D. Productivity Tools & Power-User Features

**Purpose:** Enable efficient workflows for experienced agents

**Keyboard Shortcuts:**

- **Query Actions:**

  - `Cmd/Ctrl + K`: Focus query input (from anywhere in interface)
  - `Enter`: Submit query (when input focused)
  - `Esc`: Cancel current query or close modal
  - `Cmd/Ctrl + R`: Rephrase (cancel and re-focus input with previous query text)
- **Navigation:**

  - `Tab / Shift+Tab`: Navigate between interactive elements
  - `Arrow Keys`: Navigate within collapsed sections, tab controls
  - `Space / Enter`: Activate focused control
- **View Controls:**

  - `Cmd/Ctrl + E`: Expand all response tiers
  - `Cmd/Ctrl + C`: Collapse all response tiers
  - `Cmd/Ctrl + 1/2/3`: Switch workspace modes (1=Live Call, 2=Research, 3=Documentation)
  - `Cmd/Ctrl + /`: Show keyboard shortcuts reference
- **Copy Actions:**

  - `Cmd/Ctrl + Shift + C`: Copy Tier 1 (Required Disclosure) to clipboard
  - `Cmd/Ctrl + Shift + A`: Copy entire response with citations to clipboard

**Copy-to-Clipboard Enhancements:**

- **One-Click Copy:** Copy buttons adjacent to each response tier
- **Copy Confirmation:** Subtle toast notification: "Copied to clipboard" with undo option (if applicable)
- **Format Options:** Configure copy format (plain text, rich text, markdown)
- **Smart Formatting:** Auto-format for pasting into customer CRM/notes (remove extra whitespace, add citations footer)

**Query History & Quick Recall:**

- **Recent Queries:** Dropdown in input field showing last 10 queries
- **Click to Reuse:** Click previous query to re-populate input for editing or re-execution
- **Query Search:** Search previous queries within session by keyword

**Suggested Queries & Templates:**

- **Common Queries Library:** Pre-built query templates for frequent scenarios:
  - "What's the [benefit type] copay?"
  - "Does this plan cover [service]?"
  - "What's the deductible and out-of-pocket max?"
- **Customizable Favorites:** Allow agents to save personal favorite queries for quick access
- **Auto-Complete:** As agent types, suggest completions based on common queries

**Session Workspace Management:**

- **Multiple Workspaces:** Allow agents to open multiple CSR Chat instances for different members/plans (tabbed interface)
- **Workspace Naming:** Name each workspace/tab (e.g., "Member: Jane Doe", "Plan: ABC123")
- **Quick Switch:** Keyboard shortcut to switch between workspaces (Cmd/Ctrl + Shift + Arrow)

#### E. Microcopy & Guidance

**Purpose:** Improve clarity and reduce confusion through better language

**Input Placeholder Text:**

- **Current (Weak):** "Message Mira"
- **Improved (Task-Oriented):** "Ask a benefit question (e.g., 'What's the copay for office visits?')"
- **Contextual Variants:**
  - If no plan context: "Select a member first, then ask about benefits"
  - If formulary not available: "Ask about medical benefits (prescription coverage coming soon)"

**Empty State Messaging:**

- **Initial State:** Welcoming message with getting-started guidance:
  - "Welcome! Ask me any benefit question to get started."
  - "Popular questions: [clickable chips for common queries]"
- **Post-Query Clear:** After clearing conversation: "Ready for your next question"

**Status Messages:**

- **Connection Status:** "Connected to CSR Chat" (subtle, in footer)
- **Last Updated:** "Plan data current as of [date]" (builds trust)

**Help Text:**

- **Contextual Help:** Brief help text appearing contextually:
  - Hovering over citation: "Click to view source in Nexus"
  - Hovering over workspace mode: "Live Call mode shows minimal view for active calls"

### White-Label & Configuration Capabilities

**Onboarding Customization:**

- **Tutorial Content:** Customer-specific tutorial steps, screenshots, terminology
- **Skip Default:** Configure whether tutorial shown by default or opt-in
- **Branding:** Tutorial screens reflect customer brand styling

**Shortcut Customization:**

- **Keyboard Mapping:** Allow customers to customize keyboard shortcuts to match existing workflows
- **Disable Shortcuts:** Option to disable shortcuts if conflicts with customer application shortcuts

**Accessibility Options:**

- **High Contrast Mode:** Optional high-contrast theme for low-vision users
- **Font Size Override:** Agent-level control for increasing base font size
- **Motion Settings:** Customer-default for reduced motion (override user preference)

**Productivity Feature Enablement:**

- **Feature Flags:** Enable/disable specific productivity features per customer (e.g., workspaces, query history)
- **Query Templates:** Customer-defined suggested query library
- **Copy Format:** Customer-defined clipboard format for pasting into their CRM

### Implementation Scope & Phasing

**Phase 1 - Q2 2026 (3 weeks):**

- **In-Scope:**

  - First-run tutorial (dismissible, 3-5 steps)
  - Contextual tooltips for movable panel, resize handle, workspace modes
  - Basic keyboard shortcuts (focus input, submit, cancel, expand/collapse)
  - Copy-to-clipboard buttons with confirmation feedback
  - Improved placeholder text and empty state messaging
  - WCAG 2.1 AA compliance audit and remediation
- **Out-of-Scope:**

  - Advanced keyboard navigation (multiple workspaces, query history search)
  - Custom keyboard shortcut mapping (use standard shortcuts in Phase 1)
  - Gamified onboarding checklist (optional Q3 enhancement)

**Phase 2 - Q3 2026 (2 weeks):**

- Enhanced keyboard shortcuts (workspace switching, copy actions)
- Query history and quick recall
- Suggested queries library and auto-complete
- Multiple workspace/tab support (if user research validates need)

### Dependencies & Risks

**Dependencies:**

- Accessibility audit tooling and expert review for WCAG compliance verification
- User research to validate onboarding effectiveness and feature discoverability

**Risks:**

- **Tutorial Fatigue:** Risk of agents dismissing tutorial without learning, then struggling later

  - *Mitigation:* Keep tutorial brief (2-3 minutes max); offer "Learn Later" option; persistent help access
- **Keyboard Shortcut Conflicts:** Risk of shortcuts conflicting with browser, OS, or customer application shortcuts

  - *Mitigation:* Use standard conventions (Cmd/Ctrl+K, etc.); test across environments; allow customization
- **Accessibility False Confidence:** Risk of automated testing missing nuanced accessibility issues

  - *Mitigation:* Combine automated testing with manual expert review and real user testing with assistive technologies

### Cost-Optimization Contribution

This PRD directly supports primary cost optimization objective:

1. **Reduced Training Costs:** 40% reduction in training time (estimated $400-600 per agent savings)
2. **Increased Productivity:** 10-15% efficiency gain translates to more queries per agent per shift
3. **Lower Support Costs:** 30% reduction in "how-to" support tickets (estimated $20K-30K annual savings)
4. **Higher Adoption:** Delightful UX drives preference for CSR Chat over legacy tools, increasing query volume and improving per-query cost economics
5. **Reduced Errors:** Better UX and accessibility reduce agent errors, decreasing rework and compliance costs

---

## Implementation Roadmap & Sequencing

### Q2 2026 (Weeks 1-12): Foundation Sprint

**Objective:** Deliver core platform foundation and P0 UX risks

**Week 1-8: Platform Foundation (PRD-1)**

- Contextual panel architecture (movable, resizable, non-modal)
- Basic white-label theming
- Nexus integration framework
- Configuration admin portal (MVP)

**Week 3-8: Response Architecture (PRD-2) - Parallel Track**

- Three-tier response hierarchy
- INN/OON visual separation
- Basic progressive disclosure
- Configuration schema

**Week 5-8: System Feedback (PRD-3) - Parallel Track**

- Progressive loading states
- Cancel control
- Basic system health indicator

**Week 9-12: Integration & Polish**

- Workflow integration (PRD-4 Phase 1)
- Error handling (PRD-5 Phase 1)
- Productivity features (PRD-6 Phase 1)
- Accessibility compliance audit
- Customer beta testing and feedback integration

**Q2 End State:** All P0 UX risks addressed; platform foundation ready for customer deployment

### Q3 2026 (Weeks 13-24): Enhancement Sprint

**Objective:** Complete platform capabilities and achieve >80% agent adoption

**Week 13-16: Advanced Features**

- Enhanced configuration options
- Scope intelligence and smart defaults
- Rephrase control and smart suggestions
- Deep-linked citations enhancement

**Week 17-20: Integration Maturity**

- Picture-in-picture citation preview
- Compliance export capabilities
- Advanced error analytics
- Query history and productivity tools

**Week 21-24: Optimization & Scale**

- Performance optimization
- Cross-customer deployment tooling
- Advanced white-label capabilities
- Training and change management support

**Q3 End State:** >80% agent adoption; platform deployed to multiple customers; comprehensive capabilities

### Q4 2026 & Q1 2027: Continuous Improvement

- **Q4 2026:** >90% agent utilization; self-adapting intelligence integration; advanced analytics
- **Q1 2027:** >95% agent satisfaction; cost-optimized UX; platform maturity and innovation

---

## Cross-PRD Dependencies & Integration Points

### Integration Matrix

| PRD                                    | Dependencies              | Integration Points                                                 |
| -------------------------------------- | ------------------------- | ------------------------------------------------------------------ |
| **PRD-1: Platform Foundation**   | None (foundational)       | All other PRDs build on this architecture                          |
| **PRD-2: Response Architecture** | PRD-1 (panel framework)   | PRD-4 (citations), PRD-3 (progressive loading during response)     |
| **PRD-3: System Feedback**       | PRD-1 (UI framework)      | PRD-5 (timeout errors), PRD-2 (loading during response generation) |
| **PRD-4: Workflow Integration**  | PRD-1 (panel positioning) | PRD-2 (source citations), PRD-5 (fallback to Nexus)                |
| **PRD-5: Error Handling**        | PRD-3 (system state)      | PRD-1 (UI controls), PRD-4 (fallback workflows)                    |
| **PRD-6: Productivity**          | PRD-1 (UI framework)      | All PRDs (keyboard shortcuts, onboarding for all features)         |

### Shared Configuration Schema

All PRDs utilize unified customer configuration framework:

- **Theme & Branding:** Consistent across all UI components (PRD-1)
- **Terminology:** Shared terminology dictionary (PRD-1, 2, 5, 6)
- **Behavior Preferences:** Consistent configuration patterns (timeouts, defaults, feature flags)
- **Integration Patterns:** Shared SDK and API contracts (PRD-1, 4)

---

## Cost-Benefit Analysis Summary

### Investment Summary

**Total Implementation Effort:** ~30 weeks engineering (Q2-Q3 2026)

- PRD-1: 8 weeks
- PRD-2: 6 weeks
- PRD-3: 4 weeks
- PRD-4: 5 weeks
- PRD-5: 4 weeks
- PRD-6: 3 weeks

**Estimated Development Cost:** $400K-600K (based on team size and velocity)

### Return on Investment

**Direct Cost Savings (Annual, Post-Adoption):**

- **Reduced Custom Development:** $50K-100K per customer avoided (multi-customer scale)
- **Training Cost Reduction:** $300K-500K annually (50% reduction across 500-1000 agents)
- **Support Cost Reduction:** $150K-200K annually (50% reduction in UI/UX tickets)
- **Productivity Gains:** $500K-800K annually (10-15% efficiency improvement)

**Total Annual Savings:** $1M-1.6M (excluding adoption-driven query volume benefits)

**ROI:** 170-300% Year 1; >500% over 3 years

### Adoption Impact on Cost-per-Query Economics

- **Q2 2026:** 40% adoption → Higher per-query costs due to lower volume
- **Q3 2026:** 80% adoption → Cost-per-query improving through scale
- **Q4 2026:** 90% adoption → Target cost-per-query achievable ($0.10)
- **Q1 2027:** 95% adoption + efficiency → Final cost target ($0.08) achievable

**Conclusion:** UX investment is not optional—it's a critical enabler of cost optimization through adoption and efficiency at scale.

---

## Risk Register & Mitigation Summary

### Top Risks Across PRD Portfolio

**Risk 1: Configuration Complexity Overwhelms Self-Service Value**

- **Impact:** High - Could undermine rapid deployment and cost savings
- **Mitigation:** Progressive disclosure in admin UI; template library; sensible defaults; expert services tier

**Risk 2: Performance Overhead from UI Complexity**

- **Impact:** Medium - Could jeopardize <15s response time targets
- **Mitigation:** Performance budgets; lazy loading; client-side rendering; continuous monitoring

**Risk 3: Adoption During Transition Period**

- **Impact:** High - Could delay ROI and cost-per-query improvements
- **Mitigation:** Phased rollout; parallel legacy support; change management; agent champions program

**Risk 4: Deep-Link Fragility in Customer Integrations**

- **Impact:** Medium - Could reduce verification workflow value
- **Mitigation:** Stable URL contracts; fallback navigation; automated link testing; customer API partnerships

**Risk 5: Accessibility Compliance Gaps**

- **Impact:** Medium - Could block deployment in regulated environments
- **Mitigation:** Expert accessibility audit; assistive technology testing; continuous compliance monitoring

---

## Success Criteria & Go/No-Go Gates

### Q2 2026 Completion Criteria (Platform Foundation)

**Must-Have (Go/No-Go):**

- ✅ All P0 UX risks addressed (full-screen, silent loading, no cancel, response hierarchy)
- ✅ Contextual panel architecture functional (movable, resizable, non-modal)
- ✅ Basic white-label theming operational (logo, colors, product name)
- ✅ Nexus side-by-side integration working
- ✅ WCAG 2.1 AA compliance verified
- ✅ Configuration admin portal functional (MVP)
- ✅ Agent adoption >40% within 30 days of deployment

**Nice-to-Have (Defer if Needed):**

- Advanced configuration options beyond basics
- Picture-in-picture citation preview (can move to Q3)
- Multiple workspace support (can move to Q3)

### Q3 2026 Completion Criteria (Enhancement & Scale)

**Must-Have:**

- ✅ All PRDs Phase 1 complete and deployed
- ✅ Agent adoption >80%
- ✅ Workflow disruption reduced by 60%
- ✅ Support ticket volume reduced by 50%
- ✅ Agent satisfaction >4.0/5 for system predictability and information clarity

### Q1 2027 Success Criteria (Final Targets)

- ✅ Agent utilization >90%
- ✅ Agent satisfaction >4.5/5
- ✅ Cost-per-query at or below $0.08
- ✅ All KR5 targets achieved
- ✅ Platform deployed to multiple customers with self-service configuration

---

## Appendix A: Traceability Matrix

### UX Findings → PRD Mapping

| UX Priority | Finding                         | PRD   | Capability                               |
| ----------- | ------------------------------- | ----- | ---------------------------------------- |
| P0          | Full-screen disrupts context    | PRD-1 | Contextual panel architecture            |
| P0          | Silent loading states           | PRD-3 | Progressive loading indicators           |
| P0          | Can't predict latency           | PRD-3 | Progress hints and timing estimates      |
| P0          | Can't cancel query              | PRD-3 | Cancel control framework                 |
| P0          | Unclear response hierarchy      | PRD-2 | Three-tier response system               |
| P1          | Fixed positioning blocks fields | PRD-1 | Movable, resizable panel                 |
| P1          | Sources hidden                  | PRD-4 | Citation visibility and deep-links       |
| P1          | Can't verify easily             | PRD-4 | Side-by-side verification architecture   |
| P1          | INN/OON confusion               | PRD-2 | Visual separation and scope intelligence |
| P1          | Generic errors                  | PRD-5 | Diagnostic error classification          |
| P2          | Weak onboarding                 | PRD-6 | First-run tutorial and coachmarks        |
| P2          | Low discoverability             | PRD-6 | Discoverable UI affordances              |
| P2          | Accessibility concerns          | PRD-6 | WCAG 2.1 AA compliance                   |

### Strategic Objective → PRD Mapping

| Strategic KR | Target                                                                          | PRD          | Success Metric                      |
| ------------ | ------------------------------------------------------------------------------- | ------------ | ----------------------------------- |
| KR5 Q2       | Deploy Low-Code UI, 60% disruption reduction                                    | PRD-1        | Workflow disruption -60%            |
| KR5 Q3       | >80% adoption, 45% parsing time reduction                                       | PRD-2, PRD-3 | Adoption >80%, Parsing -45%         |
| KR5 Q4       | >90% utilization, 50% verification reduction                                    | PRD-4, PRD-5 | Utilization >90%, Verification -50% |
| KR5 Q1 2027  | >95% satisfaction, $0.08 cost target | All PRDs | Satisfaction >95%, Cost $0.08 |              |                                     |

### Roadmap → PRD Mapping

| Roadmap Feature            | Quarter | PRD          | Implementation Phase |
| -------------------------- | ------- | ------------ | -------------------- |
| No-code/low-code UI        | Q2      | PRD-1        | Phase 1              |
| Contextual panel           | Q2      | PRD-1        | Phase 1              |
| Real-time guidance         | Q2      | PRD-3, PRD-6 | Phase 1              |
| Progress indicators        | Q2      | PRD-3        | Phase 1              |
| Proactive error prevention | Q2-Q3   | PRD-5        | Phase 1-2            |
| Contextual help            | Q3      | PRD-6        | Phase 2              |
| Agent experience evolution | Q3      | All PRDs     | Phase 2              |

---

## Appendix B: White-Label Configuration Schema Reference

### Theme Configuration Object (JSON)

```json
{
  "customer_id": "blue-shield-ca",
  "product_name": "CSR Chat",
  "theme": {
    "logo_url": "https://cdn.customer.com/logo.png",
    "colors": {
      "primary": "#08285E",
      "secondary": "#436DB3",
      "accent": "#F4454E",
      "text_primary": "#1a1a1a",
      "text_secondary": "#666666",
      "background": "#ffffff",
      "panel_background": "#f8f9fa"
    },
    "typography": {
      "font_family": "'Inter', 'Helvetica Neue', sans-serif",
      "base_size": "16px",
      "heading_weight": "600",
      "body_weight": "400"
    },
    "layout": {
      "default_position": "right-sidebar",
      "default_width": "400px",
      "allow_agent_customization": true,
      "responsive_breakpoints": {
        "tablet": "768px",
        "desktop": "1024px"
      }
    }
  },
  "behavior": {
    "timeout_seconds": 20,
    "default_workspace_mode": "live-call",
    "default_disclosure_mode": "minimal",
    "enable_cancel_control": true,
    "enable_rephrase_suggestions": true,
    "enable_query_history": true
  },
  "integration": {
    "source_system_name": "Nexus",
    "source_system_url": "https://nexus.customer.com",
    "deep_link_pattern": "https://nexus.customer.com/benefits/{plan_id}/{section}",
    "sso_provider": "okta",
    "sso_config": { ... }
  },
  "compliance": {
    "audit_retention_days": 2555,
    "required_disclosure_emphasis": "high",
    "state_specific_rules": ["CA", "NY", "TX"]
  }
}
```

---

## Document Metadata

**Author:** Product Management, Minerva Team**Created:** April 28, 2026**Version:** 1.0**Status:** Proposed for Review**Next Steps:**

1. Stakeholder review (Customer Success, Engineering, UX, Compliance)
2. Prioritization and roadmap alignment
3. Engineering estimation and resource allocation
4. Customer pilot selection for Q2 deployment

---

**END OF PRD PROPOSAL DOCUMENT**
