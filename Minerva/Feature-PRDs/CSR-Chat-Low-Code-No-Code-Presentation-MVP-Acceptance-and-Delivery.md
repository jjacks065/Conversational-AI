# CSR Chat Low-Code/No-Code Presentation MVP — Acceptance & Delivery

**Date:** November 6, 2026  
**Status:** READY FOR REVIEW  
**Parent:** [Feature PRD](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/CSR-Chat-Low-Code-No-Code-Presentation-MVP-Feature-PRD.md)  
**Purpose:** Traceable supporting detail for the four-week presentation-preset and production CDN release. These are future implementation requirements, not reported test results.

## 1. Decision and evidence record

### Confirmed by the user

- Complete means fully deployed to production, SDK available over CDN, and customers able to begin integration within four weeks.
- Capacity across engineering, design, and QA is not an issue.
- Reuse configuration across the standalone app and existing SDK.
- Use Stellarus-managed reusable presets; no new visual administration screen.
- Configure appearance/presentation only: branding, supported theme settings, labels, and existing display options.
- Exclude new Nexus integration.

### Product decisions within that scope

- Prove reuse with two presets and three reference surfaces: standalone, existing React SDK surface, and CDN-loaded Web Component with its reference host.
- Use existing approved Stellarus and customer-brand assets. BSC is the existing SDK customer preset; release only assets cleared for the chosen public distribution.
- Keep managed branding authoritative in managed deployments; preserve allowed personal display preferences separately.
- Versioned releases and explicit assignment are sufficient. Hot reload, a central authoring service, and new storage/administration infrastructure are unnecessary to this outcome.
- CDN delivery is mandatory. An npm-registry launch may be reused if independently ready, but is not a substitute or extra launch objective.
- Customer readiness means the documented SDK journey works with pre-provisioned access. Completing a customer's own application, Nexus workflow, or enterprise rollout is outside the four-week completion boundary.
- Preserve existing SDK APIs and host responsibilities. Engineering owns architecture, producer contracts, placement, and any compatibility-preserving mapping; no new runtime architecture is selected by this PRD.

### Alternatives and tradeoffs

| Alternative | Decision / rationale | Opportunity cost and trigger |
| --- | --- | --- |
| Separate browser-local or per-consumer themes | Superseded for managed assignments: duplicates presentation maintenance and cannot prove shared preset reuse. Existing local demo data remains intact. | Fastest initial setup, but repeated branding work persists. |
| Shared reviewed presets | Selected by user; bounded change that reuses existing settings/SDK and supports release accountability. | New preset changes use the managed release lifecycle; no instant customer editing. |
| Internal/customer visual editor | Explicitly excluded by user. | Faster non-engineer authoring is deferred; revisit only after repeated demand and measured preset-maintenance effort justify it. |
| General assistant/workflow configuration | Explicitly excluded by user; changes product behavior and review obligations beyond presentation. | No prompt/rule/capability authoring in this delivery. |
| Include Nexus/Vermillion migration | Explicitly excluded by user; external integration/design work would expand the release boundary. | Reuse compatible completed assets; track migration separately. |

**Diagnosis → policy → actions:** Existing presentation foundations have separate lifecycles and incomplete evidenced distribution. Share a bounded preset definition, map only supported presentation fields, publish a production CDN release, and prove developer handoff. Measure reuse, integration effort, and assignment effort.

**Confidence:** High in confirmed scope and source observations; medium in delivery timing until Week 1 dependency acceptance. No measured setup-time improvement is asserted.

## 2. Presentation field boundaries — LCNC-01 through LCNC-04

The following catalog is the product boundary. Week 1 engineering/design review must record exact field-to-control mappings, optional/default behavior, allowed values, and applicable states before implementation begins.

| Field group | Standalone CSR Chat | SDK / reference host | Validation and boundary |
| --- | --- | --- | --- |
| **Preset identity/version** | Explicit assigned preset/version. | Explicit preset/version selected through documented application configuration. | Stable identifiers; unknown or incompatible explicit versions produce a configuration error. No implicit other-customer fallback. |
| **Brand labels** | Portal label, workspace title, assistant label. | Assistant title and accessible labels use existing SDK copy inputs. Portal/workspace labels remain host-owned and are rendered by the reference host. | Plain presentation text; preserve current length limits. No raw HTML, executable text, legal/disclosure edits, or changes to answer content. |
| **Brand images** | Portal/assistant images with existing light/dark variants. | Approved image references available for the reference host; generic SDK panel keeps its current logo responsibilities. | Approved public assets only; documented fallback for missing images. No new upload workflow or arbitrary runtime URL-fetching service. |
| **Semantic colors** | Map approved roles into existing application styling. | Reuse existing SDK theme roles. | Accent/hover/text, links, surfaces/panel/header, main/muted text, borders, inputs, user/assistant bubbles, and error colors. Validate supported values and contrast. |
| **Typography and shape** | Apply supported matching roles to affected chat surfaces. | Existing font-family/weight, radii, and shadow inputs. | Approved existing font stacks/assets and bounded values; no new font licensing/distribution project or arbitrary CSS. Mapping can preserve surface layout differences. |
| **Color profile selection** | Existing supported profiles and allowed personal preference. | Use the named mode/style explicitly supported by the selected released preset; no new theme-mode switcher is required. | Conformance covers each variant actually released in both surfaces; do not advertise an unsupported variant. |
| **Conversation presentation, context sidebar, application footer** | Set defaults for the two existing presentations and sidebar/footer switches; valid existing personal choices may override these defaults. | Standalone-only defaults are identified as not applicable to the generic SDK. They do not create structured response, plan-selection, sidebar, or footer components inside it. | No silent claim of cross-surface parity for host-owned or absent controls. |
| **Existing generic display copy** | Only corresponding existing visible/accessibility labels are mapped. | Existing title, composer label/placeholder, empty-state and generic error presentation. | Backend error meanings, auth failures, disclosure language, and answer generation remain unchanged. |

**Parity definition:** Common fields resolve to the approved values and accessible presentation in every applicable surface. Host-only fields remain available to the host; standalone-only fields are declared as such. Screens need not have identical layout or rendering engines. The released applicability matrix is part of the integration contract.

**Precedence and compatibility:**

1. Managed preset branding, labels, assets, and tokens win over legacy browser-local branding/token overrides in managed standalone deployments.
2. Valid saved personal conversation style/sidebar/footer choices override preset defaults for those existing controls; absent or invalid personal values use the preset's documented defaults. Color selection uses only a variant supported by the assigned preset.
3. Existing local records remain intact. No automatic promotion of local demo preferences into shared presets; no credentials, transcript, or full plan data added to preference storage.
4. Existing unassigned demo behavior remains supported through an explicit documented compatibility mode. An unknown explicit managed preset cannot silently enter that mode.
5. An intentionally omitted optional field uses its documented neutral/default value. Failure to resolve an explicit preset/version is different from optional-field omission.
6. Preset selection is presentation configuration. Identity, tenant, plan authorization, backend selection, and entitlement are independently enforced by the existing approved path.

## 3. Acceptance examples and validation traceability

Engineering must map these requirement/acceptance IDs to stable Behavior IDs and tests before changing observable behavior, following repository behavior-first rules. No automated execution is claimed here.

| ID / requirement | Given / When / Then | Required evidence |
| --- | --- | --- |
| **AC-01 · LCNC-01/02/03/04** | **Given** either approved preset and its supported version, **when** selected in standalone, React SDK, and CDN Web Component/reference host, **then** all applicable fields render approved values, host/standalone-only fields follow the matrix, and M1 passes. | Producer/consumer contract checks; browser comparisons; Design review; release and preset IDs. |
| **AC-02 · LCNC-01/02/04** | **Given** an unknown preset/version, unsupported field, invalid value, or an injected answer/auth setting, **when** a release is validated or an explicit preset is resolved, **then** validation rejects it with a safe actionable error and no silent customer fallback. Omitted optional fields use documented defaults. | Boundary/negative tests for validation and resolution; no sensitive rejected values in diagnostics. |
| **AC-03 · LCNC-02/03/04** | **Given** legacy browser branding and valid personal display choices, **when** an assigned preset loads or changes, **then** managed branding wins, allowed personal choices follow the precedence rules, and active turns/draft/validated plan remain unchanged. | Legacy-state characterization and integration tests; hydration and navigation scenarios. |
| **AC-04 · LCNC-02/03/04** | **Given** a missing/failed logo or absent approved font, **when** the UI renders, **then** documented neutral image/font fallback remains readable, emits a safe diagnostic, and does not change identity, customer access, or chat state. Invalid assets cannot be accepted at release validation. | Asset failure fixtures, font fallback review, keyboard/contrast checks. |
| **AC-05 · LCNC-03/04/07** | **Given** missing, expired, or wrong-customer authorization, or unvalidated plan context, **when** appearance changes or the SDK submits, **then** the existing path denies/blocks as required. Choosing a public preset never changes permissions. | Existing auth/plan/tenant regression checks plus production-shaped integration negatives. |
| **AC-06 · LCNC-04/05** | **Given** a fresh external-origin browser with no SDK checkout, package-registry credentials, or customer build step, **when** the documented pinned CDN SDK/CSS/assets load with integrity metadata, **then** the sample initializes without undeclared imports, React runtime in the framework-neutral bundle, or private source/credential leakage. | Browser test of actual release artifacts and production URLs; content inventory; CSS/MIME/CORS and approved CSP instructions. |
| **AC-07 · LCNC-05/08** | **Given** a released CDN version, **when** a conflicting overwrite is attempted, integrity mismatches, or a new version is withdrawn, **then** overwrite controls prevent replacement, integrity failure prevents execution, and operators can restore the approved prior version without changing its contents. | Negative publication check in safe environment; browser integrity check; recorded rollback rehearsal and immutable release evidence. |
| **AC-08 · LCNC-04/06/07** | **Given** pre-provisioned customer test access and an approved existing chat endpoint, **when** an independent developer follows only the integration kit, **then** the CDN sample obtains an authenticated supported answer and demonstrates loading, safe service error, and reset/cancel where already supported. Each developer meets M2; no fabricated success. | Two timed independent rehearsals; actual endpoint and release identities; safe result/correlation evidence. |
| **AC-09 · LCNC-03/04/07** | **Given** each released preset/variant, **when** exercised in the supported browser/accessibility matrix, **then** keyboard/focus/labels/status/contrast pass and host styles remain unaffected by SDK theme scope. Preset application meets the performance budget. | Packaged-browser/a11y checks, manual focus review, controlled performance runs and baseline. |
| **AC-10 · LCNC-02/03/04/06** | **Given** an existing approved preset/version, **when** Implementation assigns it to the reference surfaces three times, **then** each run meets M3 with no bespoke customer UI change. SDK bootstrap/preset selection follows documented configuration. | Three step/timing logs with waiting time separated; changed configuration and release references. |
| **AC-11 · LCNC-05/06/08** | **Given** the release candidate passes prior gates, **when** standalone is deployed and its SDK version is published to production CDN, **then** the approved production test identity can complete the existing authenticated chat journey and support can identify/restore the serving app, SDK, and preset versions. | Production URL/release proof, authenticated smoke result, monitoring and named operational signoff. |

### Quality and operational gates

- **Browsers:** Current supported desktop Chrome and Edge are release gates; preserve any additional browser support already contracted by an existing consumer. Additional Vue/Angular host-specific integration is not implied by framework-neutral Web Component support.
- **Accessibility:** WCAG 2.2 AA for changed UI, including normal-text contrast at least 4.5:1, large-text/UI contrast as applicable, keyboard access, visible focus, accessible names, and status/error announcement. Test all released preset variants, narrow host containers, and 200% zoom without blocking clipping.
- **Performance:** After approved assets are available, p95 preset application adds no more than 50 ms over the same surface without preset resolution, across at least 30 runs on the recorded desktop/browser profile. Record first-load/CDN payload and timing separately; appearance changes must not restart transport or introduce an extra request on each chat turn.
- **Compatibility:** Existing headless/React/Web Component entrypoints and current supported consumer usage pass regression tests. Keep CSS/theme changes scoped to the SDK surface. Document preset-schema and SDK-version compatibility.
- **CDN delivery:** HTTPS, correct JavaScript/CSS/image MIME types, asset CORS suitable for cross-origin module/integrity loading, immutable version URLs, long-lived versioned caching, integrity/version manifest, publishing permissions, and safe rollback. Production samples pin versions; mutable “latest” is not an acceptance dependency.
- **Security/privacy:** Public artifacts contain presentation-only data and approved public assets. Tokens/keys remain outside presets; existing authentication and tenant enforcement stay independent. CDN asset CORS policy does not relax protected chat API origin policy.
- **Observability:** Allowlisted events/records cover release/preset validation, assignment, application/configuration error, and integration failure with SDK/preset/app version, surface, timestamp, result code, and approved correlation identifier. Existing authorized monitoring may supply these records; no new analytics service is required. Exclude prompts, transcripts, plan/member data, credentials, arbitrary configuration payloads, and raw errors.
- **UCAF handoff:** DEV must establish Behavior IDs, SPECIFY → RED → GREEN → REFACTOR evidence, applicable regression/build/static checks, and required changed-code coverage under the repository policy. The PM artifact makes no claim that these future checks have passed.

## 4. Delivery packages, dependencies, and owners

Indicative estimates below are planning assumptions for one owner per work package; engineering must validate them at kickoff. They fit the skill's one-to-five-day work-package boundary and may be decomposed further. Capacity is user-confirmed as available.

| Package | Indicative owner effort | Owner / predecessor | Exit |
| --- | --- | --- | --- |
| **LCNC-01** | 2–3 days | Apps/SDK + Design; begins Week 1 | Field/default/validation/applicability/precedence and compatibility contract accepted. |
| **LCNC-02** | 2–3 days | Apps/SDK + Design; LCNC-01 | Two presets and approved assets; repeatable review/release checks. |
| **LCNC-03** | 3–5 days | Standalone Apps; LCNC-01/02 | Assigned preset, preference compatibility, existing chat regression proof. |
| **LCNC-04** | 3–5 days | SDK Apps; LCNC-01/02 | Existing React/Web Component surfaces and host example consume presets. |
| **LCNC-05** | 3–5 days | SDK release owner + Platform; CDN provisioned | Browser-ready production artifact pipeline and release/rollback evidence. Platform provisioning tracked separately. |
| **LCNC-06** | 2–3 days | Apps/SDK + Customer Success; follows working examples | Integration kit verified by fresh consumers. |
| **LCNC-07** | 3–5 days | QA + Design; cases start in Week 1, full candidate in Week 3 | AC-01 through AC-10 and metric rehearsals pass; blockers resolved. |
| **LCNC-08** | 1–2 days | Apps/Platform + QA; all prior exits | Production deployment/CDN/authenticated acceptance and operational handoff. |

Standalone and SDK integration proceed in parallel after the shared contract. Platform CDN and endpoint readiness proceed from Day 1. The estimates total 19–31 owner-days across parallel workstreams, excluding separately owned infrastructure provisioning; they are not a staffing allocation or evidence of completed estimation.

| Dependency / evidence | Accountability and needed-by | Trigger / response |
| --- | --- | --- |
| **CDN origin, DNS/TLS, route, publish identity** — PE-1152 is In Review, with a November 12 due-date field and November 20 requested date in its body at source review. | Platform; existing assignee Brenden Owens coordinates. Confirm acceptance criteria and availability in Week 1; usable release-candidate path by Week 2. | If the dates/path are unconfirmed by Week 1 end, Product + Platform record production impact and resolution. A tracker status is not availability evidence. |
| **Existing authenticated production chat path** — source and issue records have conflicting readiness signals. | Apps/SDK + Identity/Platform; name runtime owner, approved endpoint, customer access and origin-onboarding process in Week 1. | Missing acceptance is a critical-path item. Resolve within the four-week work or escalate an explicit scope/date decision; do not label a download-only SDK integration-ready. |
| **Approved branding/assets/fonts** — reuse current catalog/brand materials. | Design + Product; Week 1. | Use only existing distribution-cleared assets; resolve approval before releasing the customer preset. |
| **Independent integration reviewers and test access** | Customer Success + QA; reserve in Week 1, ready for Week 3. | Track access/provisioning delays separately; they still affect release readiness. |
| **Existing consumers and browser compatibility baseline** | Apps/SDK + QA; identify in Week 1. | A material breaking change requires explicit Product/consumer decision; preserve current interfaces by default. |
| **Registry distribution PE-1153** — Backlog/unassigned at source review. | Platform; separate workstream unless the selected existing consumption path requires it. | CDN acceptance must work without package-registry credentials; registry delay alone cannot justify dropping CDN. |
| **Nexus SDK/design/edge tickets** | Separate owners; not MVP predecessors merely because the SDK is shared. | Import only demonstrated reusable assets; new Nexus route, design-system migration, and PE-1158 Nexus extension remain excluded. |

## 5. Measurement, risks, and release decisions

### Baseline and instrumentation plan

In Week 1, QA/Implementation use the closest existing supported approach for three timed preset/branding assignments and one current SDK integration dry run. Record exact surfaces, versions, access prerequisites, manual steps, hands-on/elapsed/wait time, defects, and support interventions. If the current method cannot complete a task, record the unsuccessful attempt and reason; do not invent a duration or treat zero successful attempts as zero effort.

M1 uses the declared-field/acceptance matrix as its denominator. A “not applicable” field must be specified before testing, with a host/surface rationale. M2 timing starts with provisioned access and the quickstart; M3 starts with approved existing preset assets/version, so neither includes creating a new brand or customer application. Production waits and failures are reported separately, not discarded.

QA records results in a release evidence pack. Product confirms target feasibility by Week 1 end; any approved adjustment retains the original target and rationale. Customer Success repeats measurement on actual assignments/integrations during the first 30 days. The four-week launch gate uses the pre-release rehearsals and production proof; it does not wait 30 days for adoption data.

| Risk / scenario | Mitigation and owner | Decision trigger |
| --- | --- | --- |
| Different standalone/SDK rendering capabilities are mistaken for missing parity. | Design + SDK publish common/host-only/standalone-only mapping; compare declared values and supported behavior. | A request needs a new renderer/page component: exclude or seek explicit scope change. |
| Legacy browser overrides hide the assigned brand or erase personal choices. | Apps characterize legacy storage and enforce explicit precedence without deleting local records. | Any cross-profile brand leak, silent overwrite, or chat reset blocks release. |
| CDN asset delivery works but customer chat fails. | Platform + SDK verify the actual existing authenticated endpoint and external-origin journey, independently of CDN HTTP checks. | No accepted path by Week 1 end: publish the owner/action/date impact; no silent pilot downgrade. |
| Unsafe or inaccessible presets pass review. | Design + QA validate bounded fields, approved assets, contrast, focus, and negative cases. | Any material accessibility/privacy/authorization regression blocks release. |
| Preset/application/SDK versions drift. | SDK release owner publishes compatibility metadata, pins sample versions, and retains previous immutable artifacts. | A consumer resolves an incompatible version: fail clearly; recover using approved prior compatible versions. |
| Broad configuration or integration requests expand the timebox. | Product enforces the confirmed presentation-only boundary and two-preset release catalog. | Prompt/agent/rule authoring, new visual admin, Nexus migration, or new platform runtime requires a separate decision. |

**Release authority:** Product accepts scope/outcomes; Apps/SDK owns implementation/compatibility; Platform accepts CDN and runtime operations; QA accepts evidence; Design accepts brand/accessibility; Customer Success accepts integration/support handoff. Security reviews changed distribution/authorization boundaries through the existing release process. Named responsible owners and production approvers are recorded at kickoff; no approval is represented as already obtained.

**Rollback:** Retain prior compatible app/SDK/preset versions. Revert the selected version through the existing authorized deployment/configuration process; never overwrite an immutable CDN URL. Rehearse both presentation regression recovery and CDN release withdrawal, keep serving clients on a known approved version, and record failure trigger, owner, verification, and customer communication route.

## 6. Sources and artifact validation

**PM artifact validation performed November 6, 2026:** All seven required v2.0 template sections are present in order. Eight scope requirements trace to eleven Given/When/Then acceptance examples, three metrics, and four weekly milestones. All nineteen local artifact/source links and cited line bounds resolve. Eight work-package estimates stay within one-to-five owner-days and sum to 19–31 owner-days across parallel tracks. Confirmed user decisions, exclusions, baseline limitations, and production dependencies were checked for consistency. These are document checks; no product test/build, deployment, publication, or production acceptance was executed.

- [Linear source extraction](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/Sources/AgentExp-01-Linear-Requirements-2026-11-06.md); [original authored PRD](/Users/jjacks20/jjacks/Conversational-AI/Minerva/Feature-PRDs/First-Pass/AgentExp-01-Low-Code-Platform-Foundation.md).
- [Discovery and current-state/source reconciliation](/Users/jjacks20/jjacks/Conversational-AI/reports/CSR-Chat-Low-Code-No-Code-MVP-Discovery-2026-11-06.md), including confirmed user decisions and tracker limitations.
- [Standalone settings](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/apps/csr-demo-ui/src/app/settings/page.tsx:109), [preference provider](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/apps/csr-demo-ui/src/features/csr-demo/BrowserPreferencesProvider.tsx:77), [behavior contract](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/apps/csr-demo-ui/docs/contracts/csr-demo-ui-contract.md:358).
- [SDK guide](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/packages/chat-client/README.md:96), [preset registry](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/packages/chat-client/src/chat-panel-presets.ts:7), [theme/copy contract](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/packages/chat-client/src/chat-panel-contract.ts:9), [distribution manifest](/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/packages/chat-client/package.json:1).
- [PE-1152 CDN dependency](https://linear.app/stellarus/issue/PE-1152), [PE-1153 registry dependency](https://linear.app/stellarus/issue/PE-1153), [COMPASS-839 packaging scope](https://linear.app/stellarus/issue/COMPASS-839), [COMPASS-39 qualified publication status](https://linear.app/stellarus/issue/COMPASS-39), [COMPASS-137 operating-model record](https://linear.app/stellarus/issue/COMPASS-137). These records were read as planning evidence, not deployment certification.

**F:** Parent PRD and this acceptance/delivery artifact are the new planning deliverables; source extraction and discovery record preserve provenance. Product source and historical PRDs remain unchanged.  
**T:** Document validation covers required-template structure, requirement/acceptance/metric traceability, estimates, links, and confirmed scope. Executable product tests are not applicable to this PM-only artifact change. Future implementation tests remain required.  
**C:** User-selected managed presentation presets, shared standalone/SDK reuse, production/CDN/customer readiness, and a four-week timebox govern the proposed requirements. Architecture remains engineering-owned.  
**O:** User decisions, Linear document/project/dependency reads, local source/contract inspection, artifact construction, and document checks support this handoff.
