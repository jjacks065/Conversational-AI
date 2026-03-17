# 🧩 Project Name: Minerva Portfolio Coverage Expansion — LG & Custom Plans

**PDLC Phase:** Planning
**Authored Date:** March 17, 2026
**Status:** DRAFT
**Template:** Linear-1-Pager
**Time Box:** 8 - 12 weeks

## 🎯 Problem Statement

Customer Experience teams currently have limited benefit intelligence coverage for Large Group (LG) and Custom plan inquiries, forcing agents to rely on manual processes with mid-80s% accuracy rates and +2 minute handle time increases for these plan types. With Minerva's proven >98% accuracy for IFP/SG plans and 4 million member calls annually where benefit inquiries represent ~30% of contact volume, the lack of LG/Custom support creates operational inefficiency and member experience gaps for approximately 65% of BSC's total covered lives.

**Impact:** ~2,500 LG/Custom plans remain unsupported, resulting in inconsistent quote accuracy, extended handle times, and reduced agent confidence for the majority of member benefit inquiries.

## 💡 Proposed Solution

Extend Minerva's proven benefit intelligence engine to support comprehensive Large Group and Custom plan coverage by integrating expanded plan data sources, enhancing the query processing logic for complex plan structures, and enabling accurate benefit quoting for the full BSC product portfolio. This builds directly on the validated MVP foundation while scaling to enterprise-level plan complexity and volume.

## 👥 Target Users

**Primary Users:**

* **Customer Experience Agents:** BSC contact center representatives handling benefit inquiries who need accurate, real-time plan information for LG and Custom plans to maintain service quality and reduce handle time
* **QA Supervisors:** Quality assurance teams responsible for maintaining >95% accuracy standards across all plan types and monitoring agent performance consistency

**Secondary Users:**

* **Member Experience Teams:** Internal stakeholders measuring member satisfaction and first-call resolution rates for benefit-related interactions
* **Product Operations:** Teams responsible for plan data management and ensuring system reliability across expanded coverage scope

## ✅ Success Metrics

How will we measure success? Include 2–3 quantifiable KPIs.

- **Portfolio Coverage:** Achieve 100% coverage of in-scope LG and Custom plans (2,500+ plans) with automated data synchronization by Q3 2026
- **Accuracy Maintenance:** Sustain >95% accuracy rate for LG/Custom benefit quotes measured through QA audit and automated validation systems
- **Agent Adoption:** Reach 80% adoption rate among trained agents for LG/Custom benefit calls within 4 weeks of deployment

## 📦 Scope

What's included in this release?

- **Enhanced Data Integration:** Nexus API expansion to ingest LG and Custom plan structures with complex benefit hierarchies and employer-specific configurations
- **Query Processing Enhancement:** Updated natural language processing to handle LG-specific terminology (group numbers, benefit elections, tiered coverage) and Custom plan variables
- **Plan Lookup Expansion:** Extended search and matching algorithms to support group-level benefit variations and custom plan identifiers
- **Quality Validation Framework:** Automated testing capabilities for LG/Custom plan accuracy validation and continuous monitoring
- **Agent Training Materials:** Updated training resources and workflow documentation for LG/Custom plan support
- **Performance Dashboard Updates:** Enhanced monitoring to track accuracy, usage, and performance metrics across expanded plan portfolio

## 🚫 Out-of-Scope

What's explicitly out of scope?

- Pharmacy formulary integration (planned for Q4 2026 delivery)
- Provider network data integration with Facets/Experience Cube (Q4 2026 scope)
- Member-specific benefit utilization or claims history (maintains product-level vs. member-level boundary)
- Medicare, Medi-Cal, and FEP plan types (require separate governance approval)
- Real-time benefit authorization or claims adjudication capabilities
- Integration with external provider portals or member-facing digital channels

## 🔄 User Journey & Experience Changes

**Current State (IFP/SG Only):**
1. Agent receives benefit inquiry call
2. If LG/Custom plan → manual lookup process (mid-80s% accuracy, +2 min handle time)
3. Member receives potentially incomplete or delayed quote information

**Target State (Full Portfolio):**
1. Agent receives benefit inquiry call
2. Queries Minerva for any BSC plan type → consistent >95% accuracy across all plans
3. Member receives accurate, timely benefit information regardless of plan complexity

## 💻 Technical Requirements

**Data Architecture:**
- Expand Nexus integration to support LG plan hierarchies and Custom plan configurations
- Implement automated data refresh pipelines for 2,500+ additional plan documents
- Enhance plan matching logic to handle group-specific benefit variations

**Platform Performance:**
- Maintain <3 second response time for benefit queries across expanded plan volume
- Ensure >99.5% platform availability during business hours
- Support concurrent query volume scaling for full agent adoption

**Quality Assurance:**
- Automated accuracy validation for new plan types using HVT/UAT methodology
- Continuous quality monitoring with LLM-as-judge evaluation framework
- Quality gates preventing production deployment until >95% accuracy threshold

## 📊 Definition of Done

**Feature Functionality:**
- [ ] All in-scope LG and Custom plans (2,500+) successfully ingested and queryable
- [ ] Natural language query processing handles LG-specific terminology and Custom plan variables
- [ ] Automated data synchronization maintains plan currency without manual intervention
- [ ] Quality validation demonstrates >95% accuracy across representative test scenarios

**User Experience:**
- [ ] Agent workflow integration requires no additional steps vs. current IFP/SG process
- [ ] Response accuracy and speed match or exceed IFP/SG baseline performance
- [ ] Training materials enable agents to achieve 80% adoption within 4 weeks

**Performance & Quality:**
- [ ] Platform response time <3 seconds for 95th percentile of LG/Custom queries
- [ ] System availability >99.5% during business hours measured over 30-day period
- [ ] Automated quality monitoring alerts on accuracy degradation below 93% threshold

**Analytics & Measurement:**
- [ ] Enhanced dashboard tracking accuracy, adoption, and performance by plan type
- [ ] Quality audit pipeline updated to include LG/Custom plan validation
- [ ] Baseline metrics captured for handle time and member satisfaction comparison

**Go-Live Readiness:**
- [ ] Hypercare monitoring protocol established for initial 2-week deployment period
- [ ] Rollback procedures documented and tested for quality or performance regression
- [ ] Agent training completion verified for pilot group before full deployment

## ⚠️ Risks & Dependencies

**Key Dependencies:**
- Continued Nexus API availability and data quality for expanded plan portfolio
- QA team capacity for expanded scope validation and ongoing monitoring
- Customer Experience leadership support for agent training and adoption acceleration

**Primary Risks:**
- Plan data complexity for LG/Custom may impact query processing accuracy
- Integration timeline dependencies could affect Q3 2026 delivery target
- Agent adoption resistance for new plan types during transition period

**Mitigation Strategies:**
- Staged deployment with IFP/SG expansion first, then LG/Custom introduction
- Parallel operation capabilities to maintain manual backup during transition
- Enhanced training and change management support for adoption acceleration

## 🗓️ Key Milestones

**Week 2-4:** Nexus integration expansion and data architecture updates
**Week 5-8:** Query processing enhancement and testing infrastructure  
**Week 9-10:** Quality validation and accuracy testing across plan portfolio
**Week 11-12:** Agent training, deployment, and hypercare monitoring
**Week 13+:** Full adoption measurement and success metrics validation