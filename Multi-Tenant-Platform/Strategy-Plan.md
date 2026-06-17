
# Updated Compass Conversational AI Platform Plan

## Summary

Update the prior plan to treat **Compass Conversational AI Platform** as both a product platform and a **runtime transition program**. The current live Nexus Benefits application is a Databricks App with Lakebase, MLflow, APIM, FastAPI, and KPI telemetry. The Kubernetes work is a rebuild off the **Databricks App runtime** onto shared AKS, but it still depends on Databricks Lakebase and MLflow during migration.

This changes the plan: the platform roadmap must now include **runtime portability, parity validation, cutover/rollback readiness, and data-plane transition governance** as first-class platform outcomes.

## Key Updates

- **Add a Runtime Plane to the platform model:** Separate the platform into conversation orchestration, domain data planes, runtime/deployment plane, telemetry/evaluation plane, and customer/compliance control plane.
- **Treat Kubernetes migration as Q2 2026 platform foundation:** The June 1, 2026 cutover path should become a platform milestone, not just an app migration.
- **Clarify “off Databricks”:** The near-term move is off Databricks App hosting to Kubernetes. Lakebase, MLflow, and Databricks reporting remain active dependencies until a later data/telemetry migration decision.
- **Promote parity evidence into platform KPIs:** K8s readiness should be measured by dev/qa/stage/prod smoke pass, APIM route health, representative answer success, telemetry-row creation, 8769 plan-record availability, and rollback readiness.
- **Add a data-plane rationalization track:** Decide how Lakebase-backed plan JSON, `benefits-service` customer-schema Postgres, and future domain data planes converge or coexist.

## Updated Roadmap

- **Q2 2026, through June 30:** Complete Kubernetes runtime cutover readiness, dual-run parity, smoke/regression evidence, APIM route validation, telemetry isolation via `_kubernetes` tables, and rollback path to Databricks App.
- **Q3 2026:** Stabilize Kubernetes as primary runtime, integrate platform tenant-context standards, define domain data-plane contracts, align Lakebase/benefits-service responsibilities, and create per-customer/per-runtime KPI dashboards.
- **Q4 2026:** Add self-adapting quality workflows, ground-truth/evaluation harnesses, domain adapter registry, data drift monitoring, and governance for migrating or retiring Databricks App-era paths.
- **Q1 2027:** Scale the platform across additional enterprise chat capabilities with Kubernetes-native operations, reusable domain adapters, platform SLOs, cost controls, and standardized product onboarding.

## KPI Additions

- **Migration readiness:** all target environments pass smoke/regression; representative chat returns a valid answer; telemetry lands in the expected runtime table.
- **Runtime resilience:** Kubernetes pod health, APIM route success rate, model-list/chat availability, rollback time, and post-cutover incident rate.
- **Data-plane integrity:** plan count parity, table-suffix isolation during migration, no mixed-runtime telemetry, no cross-customer data access.
- **Cost and throughput:** RPM, TPM, token cost, cached-token impact, model failover/circuit-breaker events, and cost per successful answer.
- **Platform maturity:** number of capabilities migrated to platform contracts, number of reusable adapters, onboarding time for a new domain/product, and percentage of traffic served by platform-standard runtime.

## Assumptions

- Kubernetes becomes the preferred application runtime, but Databricks Lakebase/MLflow remain valid platform dependencies until explicitly replaced.
- CSR/Nexus Benefits remains the first reference implementation for Compass platform governance.
- `_kubernetes` tables are migration isolation artifacts, not the final long-term tenant isolation model.
- The platform plan should preserve rollback to Databricks until Kubernetes parity and production evidence are accepted.
- Future PRD authoring should use the required PM template; this output is a revised initiative plan, not a PRD.

## Evidence

- **F:** Current Databricks runtime and KPI source: [README.md](/Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-quote/README.md:3), [Nexus app README](/Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-quote/databricks/src/nexus-benefits-app/README.md:3), [ML platform KPI pack](/Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-quote/databricks/sql/README_minerva_ml_platform_focus_dev.md:12). Kubernetes runtime/cutover: [Kubernetes README](/Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/README.md:3), [runtime parity](/Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/docs/aia-170-runtime-parity.md:1), [cutover readiness](/Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/docs/aia-176-cutover-readiness.md:10).
- **T:** Non-mutating repo/document inspection only.
- **C:** The prior platform plan remains directionally valid, but now requires an explicit runtime migration and data-plane transition track.
- **O:** Inspected Databricks app docs, KPI SQL docs, Kubernetes README, parity report, cutover readiness plan, and runtime entrypoints.
