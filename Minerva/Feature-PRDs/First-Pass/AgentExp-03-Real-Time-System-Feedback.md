# 🧩 Project Name: Agent Experience: Real-Time System Feedback & Agent Control Framework

**PDLC Phase:** Define  
**Authored Date:** April 29, 2026  
**Status:** DRAFT  

---

## 🎯 Problem Statement

Silent loading states and lack of progress visibility create awkward silence during member calls, eroding agent confidence and member trust. Agents cannot predict response latency, cancel in-progress queries, or rephrase problematic requests. The absence of system state feedback forces agents to compensate by switching to legacy tools, abandoning queries, or creating uncomfortable call pauses.

**Impact:** Unpredictable system behavior drives query abandonment (estimated 40% of failed queries), tool switching, and member dissatisfaction. Agents report awkward silences during calls that damage member experience. Lack of control reduces adoption and creates dependency on legacy tools.

**Evidence from UX Evaluation:**
- "Can't predict latency; compensates by switching tools" (P0 Priority - Roadmap Phase 2 Alignment)
- "Silent skeleton bars provide no meaningful system status" (P0 Priority)
- "While loading, agents can't interrupt a bad query" (P0 Priority - No stop/cancel control)
- CASTLE Framework: "Task Efficiency = Poor (3/3)" due to unpredictable system behavior
- Agent quote: "I've had members like, 'are you still there?'… it does take a bit of time"
- Agent quote: "I'm like waiting and waiting for it to respond"

---

## 💡 Proposed Solution

Implement a **Real-Time System Feedback & Agent Control Framework** that provides intelligent progress indicators, context-aware loading messaging, and agent control mechanisms (cancel, rephrase, fallback). Enable transparent system state visibility and cost-aware processing optimization while maintaining <15 second response time perception.

**Key Components:**
1. **Intelligent Progress Indicators:** Four-phase progressive feedback system with context-aware messaging
2. **Agent Control Framework:** Cancel, rephrase, and fallback controls with keyboard shortcuts
3. **System State Visibility:** Connection status, service health, session context dashboard
4. **Cost-Aware Processing:** Efficient resource allocation and monitoring while maintaining responsiveness

---

## 👥 Target Users

**Primary Users:**
- **Contact Center Agents:** Need predictable system behavior, visible progress indication, and control over in-progress queries during live member calls
- **Agent Supervisors:** Need visibility into system performance and agent experience with loading/response times

**Secondary Users:**
- **Engineering Teams:** Benefit from agent-visible feedback loop for performance issues and "felt slow" reports
- **Customer Members:** Experience better call quality when agents confidently manage system processing without awkward silences

---

## ✅ Success Metrics

### Agent Experience Metrics
- **Silence Reduction:** "Awkward silence" reports reduced by 70% (tracked via agent feedback and quality monitoring)
- **Agent Confidence:** Confidence scores for system predictability improve from 2.8/5 to 4.0/5
- **Perceived Performance:** Agent-reported satisfaction with response speed >4.0/5 even when actual response times vary
- **Control Usage:** >60% of agents utilize cancel/rephrase controls within first 30 days of availability

### Operational Metrics
- **Query Abandonment:** Abandonment rate reduced by 40% (measured via incomplete query analytics)
- **Tool Switching:** Frequency of mid-query tool switching reduced by 50% (measured via session analytics)
- **Timeout Rate:** Timeout errors reduced to near-zero through better control and fallback mechanisms

### Performance Alignment
- **Response Time Perception:** Agent satisfaction with response speed maintained >4.0/5 even during periods of elevated latency
- **Roadmap Alignment:** Supports Q2 2026 target "63% response times reduction (40s→15s)" and "Increase Concurrency / Eliminate timeouts"

---

## 📦 Scope

**What's included in this release?**

### A. Intelligent Progress Indicators & Loading States

**Progressive Feedback System:**

**Phase 1: Query Submission (0-500ms)**
- Visual State: Immediate feedback on query receipt
- Message: "Processing your question..."
- Indicator: Animated pulse on query input with customer brand color
- User Perception: System responsiveness and acknowledgment

**Phase 2: Processing (500ms-5s)**
- Visual State: Determinate progress bar (if time predictable) or indeterminate spinner
- Message: Context-aware status labels
  - "Searching benefit information..." (0-2s)
  - "Analyzing plan details..." (2-5s)
  - "Generating response..." (5s+)
- Additional Context: Display estimated time remaining (e.g., "Typically ~3-5 seconds")

**Phase 3: Extended Processing (5s-15s)**
- Visual State: Enhanced feedback acknowledging longer-than-expected wait
- Message: "Still working on it... Complex benefit requires detailed analysis"
- Agent Support: Display suggested interim actions:
  - "Let your member know you're getting detailed information"
  - Suggested phrase: "I'm pulling up comprehensive details for you—just a moment"

**Phase 4: Timeout Approach (15s+)**
- Visual State: Warning state indicating approaching timeout
- Message: "Taking longer than expected. You can cancel and try rephrasing."
- Agent Controls: Prominent "Cancel" button; suggested alternative phrasing
- Escalation Path: "Contact support" option if repeated timeouts occur

**Context-Aware Loading Messaging:**
- First Query in Session: "Initializing benefits engine... ~5 seconds"
- Formulary Query: "Checking drug coverage and formulary... ~8 seconds"
- Complex Multi-Part Query: "Analyzing multiple benefits... ~10 seconds"
- Follow-Up Query: "Quick follow-up search... ~2 seconds"

**Visual Design Principles:**
- Brand Consistency: Loading indicators use customer brand colors and styling
- Attention Management: Subtle animation that indicates activity without being distracting
- Accessibility: Loading states announced to screen readers; focus management for keyboard users
- Performance Budget: Loading indicators must render in <100ms to maintain perceived responsiveness

### B. Agent Control Framework: Cancel, Rephrase, and Fallback

**Cancel Control:**
- Visual Placement: Prominent "Cancel" button adjacent to progress indicator (always visible during processing)
- Interaction: Single-click cancellation with immediate feedback
- Behavior on Cancel:
  - Halt Minerva API request (server-side abort if possible)
  - Display cancellation confirmation: "Query canceled. Ready for new question."
  - Preserve query text in input field for easy editing
  - Log cancellation event for analytics

**Use Cases:**
- Agent realizes query is poorly phrased mid-processing
- Member changes their question before response arrives
- Response taking too long; agent needs to fall back to legacy tool
- Accidental query submission

**Rephrase Control:**
- Visual Placement: "Rephrase" link or button near cancel control
- Interaction: Click to cancel current query and activate input field with original query text pre-populated for editing
- Smart Suggestions: If timeout or error occurs, system suggests rephrase options:
  - "Try asking about specific benefit categories (e.g., 'What's the copay for office visits?')"
  - "Break complex questions into separate queries"
  - "Verify plan ID and member eligibility are correct"

**Fallback Mechanisms:**
- Quick Escape Hatch: "Use Nexus Instead" button that deep-links to relevant Nexus section
- Partial Results: If query partially completed, offer: "Show what we found so far" option
- Alternative Query Suggestions: Based on original query, suggest simpler or related queries more likely to succeed

**Keyboard Shortcuts:**
- Esc Key: Cancel current query
- Cmd/Ctrl + R: Rephrase (cancel and re-focus input)
- Cmd/Ctrl + N: New query (clear input and start fresh)

### C. System State Visibility & Transparency

**Status Dashboard (Minimal, Non-Intrusive):**

**Connection Status:**
- Green indicator: "Connected"
- Yellow: "Slow Connection"
- Red: "Connection Issues"

**Service Health:**
- Green: "All systems operational"
- Yellow: "Experiencing delays" (with estimated delay context)
- Red: "Service degraded" (with fallback recommendations)

**Session Context:**
- Current plan ID and member context (if applicable)
- Query count in current session
- Last successful query timestamp

**Performance Expectations Setting:**
- First-Time User Onboarding: Brief tooltip on first query: "Most queries return in 3-8 seconds"
- Persistent Performance Context: After first query, display: "Average response time today: 5.2s" (dynamically updated)
- Transparency During Issues: If system experiencing degraded performance: "Response times currently 2x normal due to high volume"

**Error State Visibility:**
- Immediate Error Feedback: Display diagnostic error message (see PRD-5 for detailed error handling)
- Historical Error Context: If agent experiences repeated errors: "You've had 3 errors in this session—contact support if this continues"

### D. Cost-Aware Processing & Resource Optimization

**Intelligent Resource Allocation:**
- Quick Response Prioritization: Simple queries (e.g., copay lookups) prioritized in processing queue
- Complexity-Based Routing: Complex queries routed to optimized processing pipelines
- Caching Intelligence: Frequently asked questions served from cache with <1s response time
- Predictive Pre-Loading: Based on session context, anticipate likely follow-up queries and pre-warm cache

**Cost-Efficient Progress Indication:**
- Client-Side Rendering: All progress indicators rendered client-side to minimize server load
- Efficient Polling: If progress updates require server polling, use exponential backoff to minimize API calls
- Streaming Responses: Where possible, stream response chunks for incremental display (reducing perceived latency)

**Performance Monitoring & Optimization:**
- Real-Time Latency Tracking: Monitor p50, p95, p99 response times per customer
- Automatic Escalation: If latency exceeds thresholds, trigger engineering alerts
- Agent-Visible Feedback Loop: Allow agents to report "felt slow" for qualitative performance tracking

---

## 🚫 Out-of-Scope

**What's explicitly out of scope?**

- Advanced streaming responses for incremental display (Phase 2 - Q3 performance optimization)
- Predictive pre-loading and caching intelligence (Phase 2 - Q3-Q4 roadmap)
- Detailed performance analytics dashboard (separate PRD: Performance Dashboard)
- Mobile-optimized progress indicators (desktop-first priority)
- Advanced retry logic with caching and alternative routing (Phase 2)
- Multi-error recovery tracking and proactive assistance (Phase 2)

---

## 🔗 Dependencies & Risks

### Critical Dependencies
- **Minerva API Cancellation Support:** Requires server-side query abort capability to properly terminate in-progress requests
- **Real-Time System Health Monitoring:** Requires infrastructure for service health status and latency tracking
- **Performance Data Pipeline:** Requires data collection and reporting for latency metrics
- **PRD-1 Platform Foundation:** Requires UI framework for controls and status indicators

### Key Risks

**Risk 1: Cancel Behavior Not Terminating Server Processing**
- **Impact:** Medium - Risk of canceled requests continuing to incur computational costs on server
- **Mitigation:** Implement proper API abort handling; track canceled query costs; set abort timeout limits; server-side monitoring and alerts

**Risk 2: Progress Indicator Accuracy**
- **Impact:** Low - Risk of progress indicators being inaccurate if processing time unpredictable
- **Mitigation:** Use indeterminate indicators for unpredictable operations; calibrate time estimates based on historical data; conservative estimates to under-promise and over-deliver

**Risk 3: Excessive Warnings Eroding Confidence**
- **Impact:** Medium - Risk of too many warnings/alerts eroding confidence in system reliability
- **Mitigation:** Calibrate thresholds carefully; focus on actionable feedback; test messaging with agent focus groups; track sentiment and adjust

**Risk 4: Performance Budget Impact**
- **Impact:** Low - Risk of progress indication framework adding latency to perceived performance
- **Mitigation:** Client-side rendering; performance budgets (<100ms for indicators); continuous monitoring; optimization iterations

---

## 🏁 Definition of Done

**Task list of statements that define when implementation of this PRD would be considered complete:**

* [ ] Progressive loading states implemented: Phase 1-4 feedback system with context-aware messaging functional
* [ ] Cancel control operational: Single-click cancellation with server-side abort, immediate feedback, query text preservation
* [ ] Rephrase control working: Click to cancel and re-focus input with original query pre-populated for editing
* [ ] Fallback mechanisms functional: "Use Nexus Instead" deep-link working, partial results display option available
* [ ] Keyboard shortcuts implemented: Esc (cancel), Cmd/Ctrl+R (rephrase), Cmd/Ctrl+N (new query) working
* [ ] System health indicator operational: Connection status, service health, session context displaying correctly
* [ ] Performance expectations setting working: First-time tooltip, average response time display, transparency during issues
* [ ] Client-side progress rendering framework complete: All indicators render in <100ms
* [ ] Cost-aware processing optimizations deployed: Caching intelligence, complexity-based routing operational
* [ ] "Awkward silence" reports reduced by 70% (measured via agent feedback in first 60 days post-deployment)
* [ ] Query abandonment reduced by 40% (measured via incomplete query analytics comparison to baseline)
* [ ] Agent confidence for system predictability >4.0/5 (measured via post-deployment survey)
* [ ] >60% of agents utilize cancel/rephrase controls within first 30 days (tracked via usage analytics)
* [ ] Technical documentation complete: Control framework specification, keyboard shortcuts guide, performance monitoring setup

---

## 📊 Cost-Optimization Contribution

This PRD directly supports primary cost optimization objective ($0.25-$0.27 → $0.08 per query):

1. **Reduced Abandoned Queries:** 40% reduction in abandonment saves wasted API costs (estimated $0.02-0.04 per abandoned query)
2. **Decreased Redundant Queries:** Better control reduces duplicate queries and tool switching (estimated 25% reduction in unnecessary calls)
3. **Efficient Resource Usage:** Intelligent progress indication and cancellation optimize server resource utilization
4. **Training Reduction:** Predictable system behavior reduces training time by 30% (estimated $300-500 per agent savings)
5. **Support Cost Reduction:** Transparent system state reduces "system not responding" support tickets by 60%

**ROI Estimate:** 40% abandonment reduction + 25% redundant query reduction = significant API cost savings; 30% training reduction = $300-500 per agent

---

## 🗓️ Implementation Timeline

**Phase 1 - Q2 2026 (4 weeks):**

**Week 1: Design & Architecture**
- Finalize progressive loading state designs and messaging variants
- Define Minerva API cancellation/abort specification
- Design system health indicator UI

**Weeks 2-3: Core Development**
- Implement progressive loading states (Phase 1-4 feedback system)
- Build cancel control with server-side abort integration
- Develop basic system health indicator
- Create timeout warning state (Phase 4 feedback)

**Week 4: Integration & Testing**
- Complete client-side progress rendering framework
- Implement keyboard shortcuts (Esc, Cmd/Ctrl+R, Cmd/Ctrl+N)
- Browser compatibility testing
- Agent pilot testing and feedback integration

**Phase 2 - Q3 2026 (3 weeks):**
- Rephrase control with smart suggestion engine
- Fallback mechanism integration with customer legacy systems (Nexus deep-links)
- Enhanced status dashboard with session context
- Advanced caching and pre-loading intelligence

---

## 📎 References & Alignment

**Strategic Alignment:**
- **KR5 Q3 2026:** Implement real-time system feedback achieving >80% agent adoption
- **Roadmap Q2 2026:** "Performance and Concurrency Improvements" - "63% response times reduction (40s→15s)" and "Increase Concurrency / Eliminate timeouts" (HyperCare Log ID:19-20)

**Related PRDs:**
- **PRD-1:** Low-Code Platform Foundation (dependency - provides UI framework for controls)
- **PRD-2:** Intelligent Response Architecture (integration - progressive loading during response generation)
- **PRD-5:** Intelligent Error Handling (integration - timeout errors and fallback mechanisms)

**UX Research:**
- Mira UX Evaluation (April 2026) - Addresses P0 priority system feedback and control issues
- CASTLE Framework Assessment - Targets "Task Efficiency = Poor (3/3)" finding

---

**Document Version:** 1.0  
**Last Updated:** April 29, 2026  
**Author:** Product Management, Minerva Team
