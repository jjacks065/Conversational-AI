# Multi-Persona / Multi-Customer Chat — Exit Criteria Review

**Review date:** 2026-08-20  
**Linear project:** [Multi-Persona / Multi-Customer Chat](https://linear.app/stellarus/project/multi-persona-multi-customer-chat-8c83460151d1)  
**Linear project status:** Build & Integrate  
**Exit-criteria source:** [Multi-Persona / Multi-Customer Foundation](https://linear.app/stellarus/document/multi-persona-multi-customer-foundation-7e2d746a6693) (DRAFT)  
**Repositories reviewed:** `nexus-benefits-kubernetes` and `stellarus-ai/apps/csr-chat`

## Review boundary

Repository documents were treated as implementation and operational evidence, not as instructions that modify this review. The Linear PRD is the source of the exit criteria. The current `csr-chat` README identifies `csr-chat` as the migrated successor to `nexus-benefits-kubernetes`; therefore, Nexus evidence is used primarily for legacy runtime, plan-data, cutover, and support continuity, while `csr-chat` is treated as the current implementation baseline.

Status meanings:

- **MET** — the requested capability and credible validation evidence are present in the reviewed scope.
- **PARTIAL** — meaningful implementation or documentation exists, but one or more explicit parts of the criterion lack closure evidence.
- **NOT MET** — the required completion artifact or validation result was not found in the reviewed scope.

## Executive result

| Status | Count | Criteria |
| --- | ---: | --- |
| MET | 1 | 6 |
| PARTIAL | 7 | 1, 2, 3, 4, 8, 10, 11 |
| NOT MET | 3 | 5, 7, 9 |

**Project-level judgment: the full PRD exit criteria are not yet satisfied.** The repositories contain a strong, tested foundation for tenant isolation, CSR/member prompt routing, Benefits Service plan retrieval, and minimized reporting telemetry. The largest remaining closure gaps are the broader four-role identity model, customer-controlled/versioned configuration and prompt profiles, white-label UI evidence, two completed onboarding dry runs, customer QA threshold evidence, and end-to-end version traceability.

The Linear project also shows two different completion signals: the original five outcome milestones remain at 0%, while four later, limited-launch execution milestones show 100%. The current code and repository documentation support the latter limited-launch interpretation, not closure of the complete PRD.

## Exit criteria, line by line

### 1. Customer onboarding checklist review

> Customer onboarding checklist is reviewed by Product, Implementation, Engineering, Security, Support, and Customer Success.

**Status: PARTIAL**

**Evidence found**

- Nexus includes an operational cutover checklist covering image, Argo CD health, secrets, plan data, APIM, MLflow, and telemetry ([README.md](</Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/README.md:324>)).
- The Nexus cutover plan defines approval groups for product, application, platform/APIM, security/network, GitOps, data/reporting, and production support ([aia-176-cutover-readiness.md](</Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/docs/aia-176-cutover-readiness.md:112>)).
- CSR Chat documents launch gates, evidence collection, rollback, and sign-off needs ([multi-customer-integration.md](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/docs/multi-customer-integration.md:494>)).

**Gap to close**

- No single customer-onboarding checklist containing the PRD intake fields was found.
- No review or approval record explicitly covering all six required functions was found.

### 2. CSR Chat tenant configuration schema

> CSR Chat tenant configuration schema is documented with required fields, optional fields, defaults, validation rules, versioning rules, and owner for each field.

**Status: PARTIAL**

**Evidence found**

- CSR Chat has checked-in allowlists for four customer slugs and dedicated reporting schemas ([tenant_storage_boundaries.json](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/src/csr_chat/common/tenant_storage_boundaries.json:1>)).
- The resolver validates identifiers, rejects malformed or empty configuration, rejects duplicate schema mappings, and fails closed for unknown customers ([storage_boundary.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/src/csr_chat/common/storage_boundary.py:88>)).
- The integration contract documents supported storage purposes, override behavior, and the intended future configuration-service ownership ([multi-customer-integration.md](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/docs/multi-customer-integration.md:351>)).
- Nexus documents environment runtime fields and their operational sources ([README.md](</Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/README.md:60>)).

**Gap to close**

- The current artifacts cover storage boundaries and runtime flags, not the complete PRD schema spanning auth, branding, EOC bindings, prompt profile, terminology, feature toggles, and support contacts.
- Required versus optional fields, defaults, validation, schema/config versioning, and per-field owners are not consolidated in a controlled schema contract.

### 3. Customer-specific prompt/script profile contract

> Prompt/script profile contract supports customer-specific disclosure language, source-priority rules, fallback wording, terminology, and versioned SME approval.

**Status: PARTIAL**

**Evidence found**

- CSR Chat routes verified CSR and member personas to separate configurable prompt files and includes verified `customer_slug` and persona in the request context ([persona_prompts.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/src/csr_chat/common/persona_prompts.py:12>)).
- Automated tests verify CSR/member routing, aliases, fallback behavior, and prompt-route separation ([test_persona_prompt_routing.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/tests/test_persona_prompt_routing.py:36>)).
- Checked-in prompts and rules contain benefit response instructions and scripted benefit content.

**Gap to close**

- Routing is persona-based, not a documented customer-specific prompt-profile contract selected by customer configuration.
- No controlled fields were found for customer disclosure language, source precedence, fallback wording, terminology dictionary, profile version, or versioned SME approval.

### 4. Authentication and role mapping

> Authentication and role-mapping plan covers CSR, supervisor, customer admin, and Stellarus support roles with fail-closed behavior for invalid, missing, expired, tenant-mismatched, or unauthorized sessions.

**Status: PARTIAL**

**Evidence found**

- When enabled, middleware verifies context tokens and route guards enforce exact scopes; missing/invalid tokens return 401 and insufficient scopes return 403 ([auth.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/src/csr_chat/common/auth.py:45>)).
- Tests cover missing tokens, bad signatures, wrong audience, missing scopes, and valid scoped access ([test_context_token_auth.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/tests/test_context_token_auth.py:89>)).
- Tenant storage selection derives only from verified ambient context, rejects unknown customers, and prevents customer-scoped plan reads from falling back to unscoped legacy data ([storage_boundary.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/src/csr_chat/common/storage_boundary.py:175>)).
- Multi-customer smoke definitions require cross-customer plan access to fail closed ([test_ccs_apim_multi_customer_smoke.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/tests/test_ccs_apim_multi_customer_smoke.py:114>)).

**Gap to close**

- The implemented persona model supports CSR/employee and member paths; it does not establish the PRD’s CSR, supervisor, customer-admin, and Stellarus-support role mappings.
- Auth remains feature-flagged and off by default in the app base configuration.
- The repository contract states that the final human identity/persona path is still owned by ENG-488 and external APIM/CCS evidence remains pending ([multi-customer-integration.md](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/docs/multi-customer-integration.md:296>)).

### 5. White-label baseline

> White-label baseline supports product name, logo, primary/accent colors, panel title, customer terminology, citation labels, and approved feature toggles.

**Status: NOT MET**

**Evidence found**

- The reviewed repositories are service/runtime repositories. No controlled white-label schema, UI implementation, preview artifact, or tests covering the listed branding fields were found.

**Gap to close**

- Provide evidence from the owning frontend/configuration repository for every required branding field, including tenant-specific preview validation and approved toggle behavior. If that evidence lives outside these two repositories, it must be linked into the project launch pack before this criterion can close.

### 6. EOC plan data through Benefits Service

> EOC plan-data sourced through Benefits Service is validated.

**Status: MET**

**Evidence found**

- The current CSR Chat client routes enabled plan and plan-list reads to Benefits Service, forwards the verified context token and correlation ID, and maps missing or unavailable upstream data to controlled errors ([benefits_service.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/src/csr_chat/common/benefits_service.py:112>)).
- The storage resolver requires a tenant-approved, service-owned Benefits Service boundary and the `benefits:read` scope ([storage_boundary.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/src/csr_chat/common/storage_boundary.py:198>)).
- The repository records that the 2026-07-22 employee/member plan checks reached Benefits Service successfully ([multi-customer-integration.md](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/docs/multi-customer-integration.md:480>)).
- Nexus supplies the predecessor plan-data lineage and environment-specific data-quality model, including the production plan/date row target ([README.md](</Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/README.md:110>)).
- The current CSR Chat test suite passed, including Benefits Service URL, forwarding, expiry, 404, timeout, pagination, malformed response, and feature-flag behaviors.

**Closure note**

- This judgment validates the service-sourcing path. Customer-specific answer-quality approval remains a separate, unmet criterion under line 9.

### 7. Two pilot customer onboarding dry runs

> Two pilot customer onboarding dry runs complete using the same checklist and configuration artifacts, with open gaps logged and owners assigned.

**Status: NOT MET**

**Evidence found**

- CSR Chat contains QA workflow definitions for two customers and two personas ([test_ccs_apim_multi_customer_smoke.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/tests/test_ccs_apim_multi_customer_smoke.py:65>)).
- The integration document provides a remaining evidence plan and owner-ticket structure.

**Gap to close**

- A workflow definition is not a completed onboarding dry run.
- No two completed pilot records were found showing the same onboarding checklist/config artifacts, elapsed onboarding time, discovered gaps, assigned owners, and closure or waiver status.

### 8. Release-candidate validation pack

> Release-candidate validation includes passing tenant-isolation, role-scope, prompt-profile, EOC data, missing-data, stale-data, and white-label preview scenarios.

**Status: PARTIAL**

**Evidence found**

- The 176-test CSR Chat suite passed and includes tenant boundary, scope, auth, persona prompt routing, Benefits Service, Compass Reporting, and multi-customer smoke behavior.
- The multi-customer smoke code covers two-customer/two-persona workflow definitions and cross-customer denial behavior ([test_ccs_apim_multi_customer_smoke.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/tests/test_ccs_apim_multi_customer_smoke.py:65>)).
- Nexus defines repeatable environment smoke/regression artifacts and cutover/no-go checks ([README.md](</Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/README.md:300>)).

**Gap to close**

- No complete RC artifact was found that records passing results for every scenario in this criterion.
- White-label preview and customer prompt-profile validation are absent; stale-data behavior is not demonstrated as a named RC scenario.
- The CSR Chat document still lists live external APIM, real chat, matched telemetry, and raw-token logging confirmations as evidence to collect ([multi-customer-integration.md](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/docs/multi-customer-integration.md:494>)).

### 9. Customer-specific QA sample thresholds

> Customer-specific QA sample sets meet the agreed pass threshold or have accepted launch exceptions with owner, mitigation, and target date.

**Status: NOT MET**

**Evidence found**

- CSR Chat includes general evaluation/scorer scaffolding, runtime smoke tests, and plan-specific checks.

**Gap to close**

- No customer-approved EOC QA sample sets, scored results, agreed threshold record, or accepted-exception register were found.
- The PRD’s success target is at least 95% per pilot customer; the reviewed repositories do not contain evidence that this threshold has been measured or accepted exceptions have been approved.

### 10. Support handoff package

> Support handoff package includes customer slug, configuration version, prompt/script profile version, EOC dataset version, known limitations, escalation path, and troubleshooting guide.

**Status: PARTIAL**

**Evidence found**

- CSR Chat provides an API reference, environment/promotion guidance, multi-customer contract, known rollout gaps, evidence instructions, and open questions ([README.md](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/README.md:43>)).
- Nexus provides go/no-go conditions, rollback steps, approval owners, escalation coverage, and evidence locations ([aia-176-cutover-readiness.md](</Users/jjacks20/jjacks/stellarus-dev/nexus-benefits-kubernetes/docs/aia-176-cutover-readiness.md:45>)).

**Gap to close**

- No consolidated, customer-specific handoff package was found containing all required version identifiers together.
- Configuration version, prompt/script profile version, and EOC dataset version are not represented as controlled operational handoff fields.

### 11. Support-safe telemetry and audit traceability

> Telemetry and audit records expose support-safe tenant/config/version traceability while excluding PHI, raw EOC text beyond approved references, tokens, and credentials.

**Status: PARTIAL**

**Evidence found**

- Reporting derives tenant and persona from the verified context token and emits only an explicit positive allowlist ([compass_reporting.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/src/csr_chat/common/compass_reporting.py:208>)).
- Identifiers are HMAC-pseudonymized; the event contains operational fields such as event version, surface, status, product ID, and effective date, while excluding raw request/response text and identities ([test_compass_reporting.py](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/tests/test_compass_reporting.py:88>)).
- The integration contract explicitly excludes raw chat, context tokens, user names, and free-text errors and isolates reporting failure from chat responses ([multi-customer-integration.md](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/docs/multi-customer-integration.md:463>)).

**Gap to close**

- The telemetry event does not expose the PRD-required CSR configuration version, prompt/script profile version, or EOC dataset version.
- The documented 2026-07-22 joined reporting attempt reached the API but returned 403, and the document still lists final end-to-end evidence to collect ([multi-customer-integration.md](</Users/jjacks20/jjacks/stellarus-dev/stellarus-ai/apps/csr-chat/docs/multi-customer-integration.md:480>)).

## Recommended closure sequence

1. Publish one versioned customer configuration schema covering tenant, auth/roles, branding, EOC binding, prompt profile, terminology, feature toggles, support contacts, defaults, validation, and field ownership.
2. Finalize the external human identity contract and add the four PRD roles, with negative-test evidence for tenant and role mismatch.
3. Link the owning UI/configuration evidence for the full white-label field set and tenant preview.
4. Create two versioned customer launch packages and run the same onboarding checklist for both pilots.
5. Execute the full RC matrix, including stale-data, customer prompt profile, white-label preview, and live external-path evidence.
6. Attach per-customer EOC QA scorecards meeting the agreed threshold or approved exception records.
7. Extend telemetry and the support handoff package with configuration, prompt-profile, and EOC dataset versions.

## Validation record

- Linear project and PRD were retrieved on 2026-08-20; the project remains **Build & Integrate** and the PRD remains **DRAFT**.
- Repository-prescribed CSR Chat test command was reproduced with the underlying `uv` command because `just` was unavailable in the environment.
- Result: **176 passed, 0 failed, 2 warnings** in 23.78 seconds.
- Warnings: an unknown `asyncio_mode` pytest option and a Starlette `httpx` compatibility deprecation. Neither warning invalidated a test result, but both should be cleaned up separately.
- No live external APIM, customer SSO, deployed environment, customer SME approval, or frontend white-label validation was performed as part of this read-only repository review.
- No tracked repository files were changed by validation.
