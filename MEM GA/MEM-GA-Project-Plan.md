# Blue Shield CA Generative Agent Chat Interface

## Project Plan - BSC Member Pilot Launch

**Version:** 1.0
**Date:** March 17, 2026
**Prepared by:** Julie Hughes
**For Review:** Stellarus Team

---

## Executive Summary

Build a generative agent (GA)) chat interface within the **Blue Shield CA member portal** **focused exclusively on benefits support**, with initial pilot launch to **BSC employees who have BSC insurance**. Future expansion to other lines of business and use cases will take place through 2027.

**Key Scope Decisions:**

- **Benefits support only** (excludes claims, billing, other use cases)
- **BSC members who are employees** as pilot group
- **Member portal/Genesys integration**
- **Sierra.ai** for managing the GA
- **End of Q2 2026** target launch with BSC Employees (strech goal, not required by the MEM team)

---

## Project Phases Overview- PROPOSAL

| Phase                                                   | Duration | Dates*         | Key Activities                                                     | Dependencies             |
| ------------------------------------------------------- | -------- | -------------- | ------------------------------------------------------------------ | ------------------------ |
| **Phase 0: Business Foundation**                  | 6 weeks  | Mar 9-Apr 17   | Contract finalization, pricing, governance                         | Contract negotiations    |
| **Phase 1: Product Discovery**                    | 3 weeks  | Mar 9-27       | MEM and Stellarus team requirements discussions                    |                          |
| **Phase 2: Technical Planning and architecture**  | 3 weeks  | Mar 23- Apr 13 | Engineering kickoff and requirements review, architecture          | NOT dependent on phase 0 |
| **Phase 3: UX Design**                            | 4 weeks  | Apr 6- May 4   | UX design, interface mockups, user flow optimization               | Phase 1 complete         |
| **Phase 4: Core EVP Development**                 | 6 weeks  | Apr 13- May 22 | Tech spec, Chat interface, loading knowledge, Sierra configuration | Phase 1 complete         |
| **Phase 5: QA & UAT**                             | 4 weeks  | May 25-Jun 19  | Testing, security validation, performance                          | Partial Phase 4 overlap  |
| **Phase 6: Pilot Preparation/Business Readiness** | 3 weeks  | May 25- Jun 12 | Documentation, training, pilot setup, dashboards                   | Phase 5 complete         |
| **Phase 7: BSC Member Pilot**                     | Ongoing  | Jun 22         | Pilot launch, monitoring, feedback collection                      | Phase 5 and 6 complete   |
| **Phase 8: Iteration and Tuning**                 | Ongoing  | July 20+       | Performance tuning, expansion planning                             | Phase 7 complete         |

**Total Timeline:** ~20-25 weeks (achievable for Q2 2026 end target)

---

## Detailed Phase Breakdown

### Phase 0: Business Foundation (6 weeks) - Mar 9-Apr 17

1. Finalize contract between Blue Shield and Stellarus
2. Complete pricing negotiations and agreements
3. Establish project governance and stakeholder communication plan
4. Confirm resource allocation and team assignment

### Phase 1: Product Discovery (2 weeks) - Mar 9-27

**MEM and Stellarus team requirements alignment**

5. **Requirements discussions** between MEM and Stellarus teams
6. **User needs discovery** of BSC members
7. **Scope validation** and success criteria alignment
8. **Stakeholder alignment** on product vision and objectives

### Phase 2: Technical Planning and Architecture (3 weeks) - Mar 23-Apr 13

**Critical foundation for development phases** (*NOT dependent on Phase 0*)

9. **Engineering kickoff** with full Stellarus team
10. **Architecture deep dive** and technical specification refinement
11. **Linear stories creation** and development planning
12. **Technical design review** and approval

### Phase 3: UX Design (4 weeks) - Apr 6-May 4

**User experience design and interface optimization**

15. **User persona refinement** for BSC employee members and benefits use cases
16. **Chat interface wireframes** and user flow design (*parallel with Phase 4 development*)
17. **Member portal integration UX** design and navigation flow
18. **Accessibility compliance** review and design adjustments
19. **Design system alignment** with existing BSC member portal standards
20. **Early employee feedback planning** and validation strategy development for BSC employee pilot group

### Phase 4: Core EVP Development (6 weeks) - Apr 13-May 22

**Foundation chat interface capabilities**

21. **Project kick offs** - Broader BSC team, Stellarus GTM, and BSC GTM alignments and milestone launch
22. **Development environment setup** and CI/CD pipeline establishment
23. **Core chat interface implementation** within member portal (*parallel with step 24*)
24. **Loading knowledge** and data integration (*parallel with step 23*)
25. **Sierra configuration** and system setup
26. **Member portal/Genesys integration** for chat and session management
27. **Resolve critical gaps** (*parallel with steps 23-26*):
    - Define generative agent training methodology for BSC member benefits use cases
    - Design error handling and customer service escalation workflows
    - Establish member portal/Genesys authentication and BSC member identification
28. **Initial generative agent training** for BSC-specific benefits use cases

### Phase 5: QA & UAT (4 weeks) - May 25-Jun 19

**Comprehensive validation and user acceptance testing**

29. **Comprehensive testing suite** development and execution
30. **Security validation** and member data protection testing (*parallel with step 29*)
31. **Performance testing** and optimization for member portal load
32. **User acceptance testing** with stakeholder (BSC Ops/CE) validation
33. **Integration testing** with existing member portal systems

### Phase 6: Pilot Preparation/Business Readiness (3 weeks) - May 25-Jun 12

**Pilot launch readiness and business preparation**

34. **Member-facing documentation** and help guides
35. **Customer service team training** on GA chat support processes
36. **Internal BSC employee communication** about pilot program
37. **Dashboards and monitoring setup** for pilot tracking
38. **Early testing with select BSC employee members** (*validates Phase 5 outcomes*)

### Phase 7: BSC Member Pilot (3 weeks) - Jun 22-Jul 17

**Controlled pilot rollout**

39. **Phased rollout** to BSC employees with BSC insurance
40. **Real-time monitoring** and customer support during pilot
41. **Member feedback collection** and immediate issue resolution
42. **Pilot success validation** and expansion readiness review

### Phase 8: Iteration and Tuning (Ongoing) - July 20+

**Continuous improvement and future planning**

43. **Performance monitoring** and model tuning for BSC member benefits accuracy
44. **BSC member feedback analysis** and feature iteration
45. **Expansion planning** for other lines of business members

---

## Technical Architecture Context

**Based on existing MEM GA planning decisions:**

### Data Sources

- **Primary:** Nexus platform (80% JSON format, benefits data repository)
- **Secondary:** Facets system (plan customizations, specialty benefits)
- **Supplementary:** SharePoint/portal (desktop procedures, PDFs)

### Integration Points

- **Member Portal/Genesys:** Existing authentication and session management
- **Customer Service:** Escalation workflows and support processes
- **Monitoring:** Performance tracking and feedback collection systems

### Training Approach

- **BSC-Specific:** Unique training required for BSC member benefits use cases
- **Iterative:** Ongoing tuning to prevent model drift
- **Compliance:** 7-year transcript storage, bias avoidance protocols

---

## Success Criteria & Validation

### Phase Gates

Each phase requires stakeholder approval and success criteria met before proceeding

### Critical Checkpoints

1. **Phase 2:** BSC member benefits training methodology validated, member portal/Genesys integration approach confirmed
2. **Phase 5:** Member data protection validated, performance benchmarks met, UAT completed
3. **Phase 6:** Customer service teams trained, pilot group identified and prepared, dashboards operational
4. **Phase 7:** Pilot group feedback scores >7/10, escalation rate <5%

### Launch Readiness Criteria

- All integration tests passing ✅
- Security validation complete ✅
- Customer service teams trained on GA support ✅
- BSC member pilot group onboarded ✅
- Real-time monitoring systems operational ✅

---

## Risk Mitigation & Considerations

### Primary Risks

1. **Contract Timeline:** If negotiations extend beyond 4 weeks, leverage Phase 2 parallel technical planning (NOT dependent on Phase 0)
2. **Member Portal/Genesys Integration:** Early validation of integration approach in Phase 2 critical
3. **BSC Member Engagement:** Leverage insider knowledge for detailed feedback, but ensure member perspective maintained

### Technical Considerations for Engineering Review

1. **Performance Requirements:** Member portal load patterns and response time expectations
2. **Security Requirements:** Member data protection and authentication integration approach
3. **Scalability Planning:** Architecture decisions for future lines of business expansion
4. **Monitoring Strategy:** Real-time performance tracking and issue detection during pilot

### Future Expansion Path

- **Phase 9+:** Core/Premier member segments based on BSC pilot success metrics
- **Scope Expansion:** Claims and billing functionality (separate future project)
- **Technology Evolution:** Voice agent integration (referenced in existing planning sessions)

---

## Engineering Team Feedback Requested

**Please review and provide feedback on:**

1. **Technical Architecture:** Are the integration approaches (member portal/Genesys, Nexus, Facets, Sierra) feasible with our current capabilities?
2. **Timeline Reality Check:** Are the 5-6 week Core EVP Development phases realistic for the described scope?
3. **Resource Requirements:** What team size and skill mix is needed for parallel development tracks?
4. **Risk Assessment:** What technical risks or dependencies are we missing?
5. **Testing Strategy:** Are the QA phases adequate for member-facing production launch?
6. **Scalability Concerns:** How should we prepare the architecture for future lines of business expansion?

---

## Next Steps

1. **Engineering team review** and feedback incorporation
2. **Revised plan presentation** to BSC MEM team
3. **Contract finalization** and Phase 0 execution
4. **Phase 2 engineering kickoff** planning

---

*This document builds on existing MEM GA planning sessions from March 2026 and incorporates Stellarus team capabilities and constraints. For detailed background context, see supporting documentation in Sierra/MEM GA/Background/ folder.*
