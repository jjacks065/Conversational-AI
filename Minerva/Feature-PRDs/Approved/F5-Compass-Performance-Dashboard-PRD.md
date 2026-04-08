# 🧩 Project Name: Compass Performance Dashboard

**PDLC Phase:** Define
**Authored Date:** March 18, 2026
**Status:** DRAFT

## 🎯 Problem Statement

Stellarus operations and engineering teams lack real-time visibility into the operational performance of Compass and the business impact across customer deployments, creating blind spots in service quality monitoring, cost optimization, and continuous improvement planning. Without comprehensive performance analytics, teams cannot proactively identify service degradation, optimize resource allocation, or demonstrate ROI to stakeholders across multiple lines of business.

**Impact:** Risk of undetected service issues affecting customer operations and end-user experience; inability to optimize operational costs across deployments; lack of data-driven insights for future release planning and multi-customer expansion strategies.

## 💡 Proposed Solution

Create a comprehensive, real-time Performance Analytics Dashboard that provides operational teams with actionable insights into Compass and the performance across response times, usage patterns, accuracy metrics, and cost efficiency. The dashboard will integrate with existing telemetry and provide both real-time monitoring and historical trending capabilities.

## 👥 Target Users

**Customer Authenticated Users (Customer-Facing Metrics Only):**

* **Customer Operations Teams:** Need visibility into their deployment's performance, uptime, and service quality metrics
* **Customer IT Leadership:** Require service level monitoring and performance trending for their specific Compass instance
* **Customer Success Managers:** Need usage analytics and accuracy metrics to demonstrate value and identify optimization opportunities

**Stellarus Authenticated Users (Full Internal + Customer Metrics):**

* **Stellarus Operations Team:** Need comprehensive system health monitoring and alerting across all customer deployments
* **Stellarus Product Managers:** Require usage analytics and accuracy trends across all customers to inform future release roadmap
* **Stellarus Customer Success Leadership:** Need business impact metrics to measure ROI and service quality improvements across customer base
* **Stellarus Technical Support:** Need diagnostic data to troubleshoot customer-reported issues across all deployments
* **Stellarus Finance Team:** Require cost tracking and efficiency metrics for budget planning and pricing optimization
* **Stellarus Sales Engineering:** Need performance metrics to support customer expansion discussions and new customer onboarding

## ✅ Success Metrics

How will we measure success in reporting accurate system and product health? Include 2–3 quantifiable KPIs focused on data trust and reliability.

* **Data Accuracy & Reliability:** Achieve <1% variance between dashboard metrics and source system data across all performance indicators, validated through weekly automated reconciliation checks
* **System Health Detection Accuracy:** Dashboard correctly identifies and reports 100% of known system issues within 2 minutes of occurrence, with zero false positive alerts during 30-day measurement period
* **Cross-System Data Integrity:** Maintain 99.9% data freshness SLA with all telemetry sources feeding dashboard metrics no more than 30 seconds behind real-time, measured continuously across all customer deployments

## 📦 Scope

**Performance Metrics Implementation:**

**Customer-Facing Metrics (Visible to Customer Authenticated Users):**

* **Response Time Analytics:** Real-time and historical tracking for customer's deployment (Min, Max, Avg, Median, Standard Deviation)
* **Usage Analytics:** Session counting and trending for customer's instance by Day/Week/Month/Quarter
* **Session Quality Metrics:** Questions per session analytics for customer's deployment
* **Application Health Dashboard:** System uptime and availability trending for customer's instance
* **Quality Assurance:** Question accuracy rate monitoring with confidence scoring for customer's deployment
* **Product Pipeline Analytics:** Total plan products successfully ingested with historical tracking; product update frequency by Day/Week/Month/Quarter; product ingest failure rate percentage with trending and alerting capabilities

**Internal + Customer Metrics (Stellarus Users Only):**

* **Cost Management:** Per-question and per-session cost tracking with trend analysis and forecasting across all customers
* **Infrastructure Monitoring:** API error rate tracking, resource utilization, and capacity planning metrics
* **Business Intelligence:** Revenue per customer, churn risk indicators, and expansion opportunity analysis

**Dashboard Features:**

* **Multi-Tenant Authentication:** Role-based access control with customer vs Stellarus user authentication and authorization
* **Contextual Data Views:** Automatic data filtering based on authenticated user role and customer assignment
* **Real-time Data Visualization:** Live updating charts and KPI cards with last-updated timestamps
* **Historical Trending:** 7-day, 30-day, 90-day views with YoY comparison capabilities where applicable
* **Role-Based Alerting:** Configurable thresholds for key metrics with customer-specific vs global notification capabilities
* **Secure Data Export:** CSV/Excel export functionality with appropriate data filtering based on user permissions

## 🚫 Out-of-Scope

**Explicitly excluded from this iteration:**

###### Cross Customer Analytics:

* **Cross-Customer Analytics:** Aggregated performance metrics across all customer deployments with customer segmentation
* **Cross-Customer Data Sharing:** Customer users will not see aggregated data or metrics from other customer deployments

###### General Scope:

* **End-User Level Analytics:** Individual end-user usage patterns and PII-related metrics (requires additional privacy governance per customer)
* **Advanced AI/ML Insights:** Predictive analytics, anomaly detection algorithms, or machine learning-powered recommendations
* **Customer-Specific System Integration:** Customer proprietary system correlation or external health monitoring integrations
* **White-Label Customization:** Customer-branded dashboard themes or custom UI modifications
* **Advanced RBAC:** Granular permissions beyond customer vs Stellarus user roles (department-level, project-level access)

## ⚠️ Risks & Dependencies

**High-Risk Technical Dependencies:**

* **Customer SSO Integration Complexity:** Each customer deployment may require unique SSO configuration (SAML, OAuth2, LDAP) with varying identity provider implementations, potentially extending authentication integration timeline by 2-4 weeks per customer type
* **Data Isolation Architecture:** Multi-tenant data segregation requires bulletproof customer boundary enforcement at database, API, and UI layers; single misconfiguration could result in data leakage incident requiring immediate system shutdown
* **Compass Telemetry System Dependencies:** Dashboard relies on existing Compass telemetry infrastructure for real-time metrics; any telemetry system outages or schema changes will directly impact dashboard data accuracy and availability

**Medium-Risk Integration Dependencies:**

* **Authentication System Dependencies:** Integration with Stellarus internal identity management system for employee access; changes to corporate authentication policies or system upgrades could break internal user access
* **Customer Onboarding Process:** New customer provisioning requires coordination between Customer Success, IT Security, and Engineering teams; manual steps in onboarding process create risk of access delays or misconfigurations
* **Third-Party Monitoring Tools:** Chart visualization and real-time data refresh depend on integrated monitoring stack; vendor API changes or service outages could impact dashboard functionality

**Business & Operational Risks:**

* **Customer Data Privacy Compliance:** Multi-tenant architecture must comply with varying customer data residency and privacy requirements (GDPR, HIPAA, SOC2); compliance violations could result in customer contract breaches
* **Performance at Scale:** Dashboard performance degradation as customer count increases; inadequate load testing could result in system slowdowns affecting all customers during peak usage
* **Security Audit Timeline:** Required security review for multi-tenant data access may extend launch timeline if vulnerabilities are discovered requiring architectural changes

**Risk Mitigation Strategies:**

* Implement phased rollout starting with pilot customers having standard SSO configurations
* Establish automated testing for data isolation boundaries with continuous monitoring
* Create fallback data sources and graceful degradation for telemetry system dependencies
* Develop comprehensive security testing protocol and schedule security review early in development cycle

## 🏁 Definition of Done

**Functional Completion Criteria:**

* **Authentication System Validation** : Multi-tenant authentication system tested successfully beteween customer and Stellarus SSO integrations. Evidence: Test execution report with pass/fail results, error logs, and performance metrics.
* **Customer Dashboard Functionality** : Customer-facing metrics dashboard validated with 100% successful data filtering tests for 10 representative customer datasets. Evidence: Test cases execution results, screenshots of filtered vs unfiltered data views, data validation report.
* **Internal Dashboard Functionality** : Full internal dashboard tested with 100% access to all metric categories and cross-customer data views for Stellarus authenticated users. Evidence: Feature checklist validation, role-based access matrix verification, test user validation results.
* **Role-Based Access Controls** : Data access permissions tested across 20 user scenarios with 0 unauthorized access incidents. Evidence: Penetration testing report, access control matrix validation, security audit findings.
* **Historical Data Visualization** : Time range selection (7/30/90 days) validated with accurate data retrieval from source systems with <1% variance. Evidence: Data accuracy validation report, automated test suite results, cross-system data comparison.
* **Alerting System Validation** : Role-based alerts tested for 10 threshold scenarios with 100% delivery success rate. Evidence: Alert delivery logs, notification testing results, escalation workflow validation.
* **Data Export Security** : CSV export functionality tested with permissions-based filtering validated across 15 user scenarios. Evidence: Export test results, data filtering validation, permissions audit report.

**Quality and Performance Gates:**

* **Performance Benchmarks** : Dashboard load time ≤3 seconds validated across 100 test scenarios with 95% success rate. Evidence: Performance testing report, load time metrics dashboard, optimization recommendations.
* **Uptime Requirements** : 99.9% uptime target with comprehensive monitoring and alerting system deployed. Evidence: Monitoring dashboard configuration, SLA tracking setup, incident response procedures.
* **Data Accuracy Validation** : Cross-system data validation automated testing with <1% variance tolerance across all metric categories. Evidence: Data validation test suite, variance analysis report, discrepancy tracking system.
* **Security Compliance** : Security review passed with 0 high-severity findings and multi-tenant data segregation validated. Evidence: Security audit report, penetration testing results, compliance certification.
* **Integration Testing** : Customer SSO and Stellarus authentication integration tested with 100% success rate across target authentication providers. Evidence: Integration test results, authentication flow validation, error handling verification.

**Business Readiness:**

* **Training Completion** : Operations team training completed with 100% stakeholder certification and documented competency validation. Evidence: Training completion certificates, competency assessment results, stakeholder sign-off documentation.
* **Documentation Delivery** : Complete documentation package delivered including user guides (≥90% user satisfaction score), admin procedures (validated by operations team), and troubleshooting playbooks (tested against 10 common issues). Evidence: Documentation review approval, user feedback survey results, troubleshooting validation report.
* **Success Metrics Foundation** : Baseline metrics established with automated tracking implementation and first 48-hour operational validation completed. Evidence: Metrics dashboard validation, baseline measurement report, automated tracking verification results.

---

## 📊 Dashboard Wireframe Mockup

### Header Section

```
[STELLARUS COMPASS PERFORMANCE DASHBOARD]          [Last Updated: 3/18/26 2:45 PM]
[👤 Customer Admin - ACME Corp]                    [AUTO-REFRESH: ON] [⚙️ Settings]
[7 Days] [30 Days] [90 Days] [Custom Range]                    [📊 Export Data]
```

### Key Performance Indicators (Top Row)

```
┌─── SYSTEM STATUS ────┐  ┌─── RESPONSE TIME ────┐  ┌─── ACCURACY RATE ────┐
│     🟢 ONLINE        │  │     2.3s AVG         │  │      98.7%           │  
│    99.8% Uptime      │  │   (↑0.2s from 7d)    │  │    (↑0.3% from 7d)   │
│                      │  │                      │  │                      │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
┌─── TOTAL PRODUCTS ───┐  ┌─── SESSIONS TODAY ───┐  ┌─── API ERROR RATE ───┐
│       2,847          │  │       1,247          │  │      0.12%           │  
│   (↑156 from 7d)     │  │   (↑15% from 7d)     │  │   (↓0.05% from 7d)   │
│                      │  │                      │  │                      │
└──────────────────────┘  └──────────────────────┘  └──────────────────────┘
```

### Main Analytics Section (Middle Row)

```
┌─ RESPONSE TIME DISTRIBUTION ─────────────────────────────────────────────┐
│                                                                          │
│ [Line Chart showing Min/Max/Avg/Median/StdDev over selected time period] │
│                                                                          │
│   Min: 0.8s  │  Max: 12.3s  │  Median: 2.1s  │  95th: 4.2s  │ 99th: 7.8s │
└──────────────────────────────────────────────────────────────────────────┘
┌─ SESSION ANALYTICS ──────────────────┐  ┌── QUESTIONS PER SESSION ──────┐
│                                      │  │                               │
│  [Bar Chart: Sessions by Day/Week]   │  │  [Histogram: Question Dist.]  │
│                                      │  │                               │
│  Daily: 1,247 │ Weekly: 8,329        │  │ Min: 1  │ Avg: 3.2  │ Max: 15 │
│  Monthly: 32,156 │ Quarterly: 95,468 │  │  Median: 3  │ StdDev: 2.1     │
└──────────────────────────────────────┘  └───────────────────────────────┘
```

### Detailed Metrics Section (Bottom Row)

```
┌─ APPLICATION HEALTH ─────────────────────────────────────────────────────┐
│                                                                          │
│  [Multi-line chart: Uptime %, API Error Rate %, Response Time Trend]     │
│                                                                          │
│  Current Uptime: 99.8%  │  Avg Error Rate: 0.12%  │  SLA Target: 99.5%   │
└──────────────────────────────────────────────────────────────────────────┘
┌─ COST ANALYSIS ──────────────────────┐  ┌─ ACCURACY TRENDS ────────────┐
│                                      │  │                              │
│  [Stacked Chart: Cost per Question   │  │  [Line Chart: Daily/Weekly   │
│   vs. Cost per Session over time]    │  │   Accuracy Rate Trending]    │
│                                      │  │                              │
│  Cost/Question: $0.15                │  │  Current: 98.7%              │
│  Cost/Session: $0.48                 │  │  7-day avg: 98.4%            │
│  Monthly Total: $15,234              │  │  Target: >98%                │
└──────────────────────────────────────┘  └──────────────────────────────┘
┌─ PRODUCT PIPELINE ANALYTICS ───────────────────────────────────────────────────────┐
│                                                                                    │
│  [Dual Chart: Success vs Failure Rates + Update Frequency Trending]                │
│                                                                                    │
│  Your Products Ingested: 2,847  │  Daily Updates: 156      │  Failure Rate: 1.2%   │
│  Weekly Updates: 892            │  Monthly Updates: 3,421  │  Success Rate: 98.8%  │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### Alert Status Footer

```
🔔 ACTIVE ALERTS (2):  ⚠️ Response time exceeded 5s threshold (12:30 PM)  
                      ℹ️ Question volume 25% above normal (1:15 PM)
          
[View All Alerts] [Configure Alerts] [Download Report]
```

---

## 📋 Linear Development Issues

*Following the Linear Method, these issues are written as actionable, scoped technical tasks rather than user stories.*

### Project: Dashboard Foundation & Data Layer

#### [CPD-01] Scaffold Next.js Application and CI/CD Pipeline
**Context:** A foundational repository is required to establish the frontend tooling, routing, and deployment processes so parallel engineering can begin.
**Scope:**
- Initialize Next.js 14+ (App Router) with TypeScript and Tailwind CSS.
- Setup Prettier, ESLint, and Husky pre-commit hooks.
- Configure GitHub Actions pipeline to run tests, lint checks, and deploy a skeleton build to the staging environment.
**Acceptance Criteria:**
- Repository is accessible and runs locally without errors.
- Pushing to `main` triggers a successful CI/CD deployment to staging.

#### [CPD-02] Implement Databricks & MLflow Connection Utilities
**Context:** The dashboard requires backend access to real-time performance telemetry housed in Databricks and MLflow.
**Scope:**
- Implement server-side client wrappers utilizing the Databricks SQL Connector and MLflow REST APIs.
- Establish a caching layer (e.g., node-cache or Redis) with a 30-second TTL to support real-time polling without overloading the data stores.
**Acceptance Criteria:**
- Utility methods successfully return raw performance data from both Databricks and MLflow.
- Repeated requests within the 30-second TTL correctly serve data from the cache.

#### [CPD-03] Implement Multi-Tenant Authentication (NextAuth)
**Context:** We need to authenticate two separate groups: Customer Operations (via their respective SSO) and Internal Stellarus users.
**Scope:**
- Configure `NextAuth.js` with SAML/OAuth2 providers for customers and internal corporate providers for Stellarus.
- Map and append custom claims to the JWT session: `role` (customer | stellarus) and `tenant_id`.
**Acceptance Criteria:**
- Users are successfully redirected to their respective SSO log-in and securely authenticated.
- The application session exposes accurate `tenant_id` and `role` properties.

#### [CPD-04] Enforce Tenant Data Isolation Middleware
**Context:** Misconfigured API routes risk leaking data across customer bounds. Isolation must be handled systematically before data is fetched.
**Scope:**
- Create a Next.js server-side utility/middleware that intercepts data fetches and injects `WHERE tenant_id = ?` into Databricks queries.
- Reject any cross-tenant query request automatically unless the user has the `stellarus` role.
**Acceptance Criteria:**
- Customer API requests explicitly return only data scoped to their `tenant_id`.
- Test coverage confirms requests for arbitrary tenant IDs by customer roles return a 403 Forbidden.

### Project: Customer-Facing Analytics

#### [CPD-05] Build Real-Time KPI Cards Component
**Context:** Users need an at-a-glance visualization of core health metrics at the top of the dashboard.
**Scope:**
- Build the reusable `<KpiCard />` React component.
- Implement SWR/React Query hooks to poll the backend data endpoints every 30 seconds.
- Implement frontend logic to calculate the (↑/↓) change from a 7-day trailing average.
**Acceptance Criteria:**
- 6 KPI cards render accurately according to the wireframes.
- Values auto-refresh on screen without page reloads.
- Components render loading skeleton states during data fetches.

#### [CPD-06] Develop Response Time & Health Distribution Charts
**Context:** Deep-dive line charts are needed to evaluate historical application performance.
**Scope:**
- Integrate charting library (e.g., Recharts or Chart.js).
- Build the "Response Time Distribution" line chart charting Min/Max/Avg/Median/StdDev.
- Build the "Application Health" multi-line chart charting Uptime % and Error Rates.
**Acceptance Criteria:**
- Charts handle 1000+ data points cleanly without UI lag.
- Tooltips on hover expose the exact timestamps and metric values.
- Time Range toggles (7/30/90 Days) dynamically update the chart data.

#### [CPD-07] Implement Session & Product Pipeline Analytics
**Context:** Dashboards require visibility into customer usage patterns and product pipeline ingestion success metrics.
**Scope:**
- Build the "Session Analytics" bar chart and "Questions per Session" histogram.
- Develop the dual-chart interface for Product Pipeline analytics (Success vs Failure rates).
**Acceptance Criteria:**
- Data automatically groups into daily/weekly/monthly buckets based on the selected time range.
- Numerical axes format cleanly (e.g., 1.2K instead of 1200).

### Project: Internal Stellarus Analytics

#### [CPD-08] Build Internal Cost Management Dashboard
**Context:** The Stellarus finance and operations teams require a view to monitor infrastructure cost efficiency.
**Scope:**
- Build a stacked bar chart mapping Cost per Question vs. Cost per Session.
- Implement the aggregation logic across all tenants (Internal access only).
**Acceptance Criteria:**
- Logged in `stellarus` users can view the global, cross-tenant Cost Analysis chart.
- Requests from `customer` users to this view/API immediately return 403 Forbidden.

#### [CPD-09] Build Business Intelligence Module (Churn & Growth)
**Context:** We must automatically flag at-risk and high-growth accounts based on their telemetry data.
**Scope:**
- Write the backend Databricks queries that calculate relative session velocity across a 30-day window.
- Render a tabulated "Customer Health" data table summarizing Revenue, Usage Deltas, and Risk Scores.
**Acceptance Criteria:**
- Customers with >25% drop in sessions are explicitly highlighted as "Churn Risk".
- Table allows sorting by Risk Score and Expansion Opportunity.

### Project: Alerting & Exporting

#### [CPD-10] Implement Secure CSV Data Export Endpoint
**Context:** Operations personnel require raw data extracts for use in external compliance/reporting tools.
**Scope:**
- Build an API endpoint `/api/export` that generates a streamed CSV from the telemetry queries.
- Strictly enforce the existing Data Isolation logic within the export generation.
**Acceptance Criteria:**
- Download button successfully yields a well-formatted CSV matching the user's dashboard view.
- Customer CSV exports never contain rows belonging to another `tenant_id`.

#### [CPD-11] Build Custom Alert Configuration UI
**Context:** Teams need to be notified when performance degrades past customized thresholds.
**Scope:**
- Build a settings UI form allowing users to select a metric, an operator (>, <), and a threshold value.
- Provide a multi-select for Notification preferences (Email, UI, Slack).
**Acceptance Criteria:**
- Configurations persist to the database.
- Users can edit, disable, or delete existing alert thresholds.

#### [CPD-12] Implement Background Alert Evaluation Worker
**Context:** Alert rules need to run constantly without depending on an active browser session.
**Scope:**
- Build a standalone Node.js cron/worker that polls the Databricks/MLflow data layer every 2 minutes.
- If threshold logic is breached, generate a database alert record and trigger the appropriate email/Slack integrations.
**Acceptance Criteria:**
- Deliberately spiked data in the staging environment triggers an alert notification within the 2-minute SLA.
- Triggered alerts surface on the Dashboard's UI footer.
