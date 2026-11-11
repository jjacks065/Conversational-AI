# CSR Chat Low-Code/No-Code MVP — discovery and source reconciliation

**Date:** 2026-11-06 (America/Los_Angeles)  
**Status:** Source discovery complete; user scope confirmed; replacement PRD prepared for review  
**Method:** feature-prd v1.1; required PRD template inspected: Feature-1-Pager-PRD.md v2.0.  
**Task boundary:** Create a new four-week MVP PRD based on the existing standalone CSR Chat. Product implementation and external publication are outside this request.

## Evidence basis and limits

FACT means directly observed in the named source or tool response. INFERENCE means an assessment derived from that evidence. ASSUMPTION means an unconfirmed condition. Source implementation, a tracker status, and a successful customer deployment are different evidence levels.

- **FACT — user direction:** Both legacy PRDs are stale; the delivered standalone app is the starting point; the delivery goal is four weeks; scope is to be confirmed interactively.
- **FACT — Linear source:** [Agent Experience: Low-Code/No-Code UI Foundation & Configuration Framework](https://linear.app/stellarus/document/agent-experience-low-codeno-code-ui-foundation-and-configuration-7ef5e9915240), document UUID `8c1b1371-43ce-4bb7-9b95-8b1b88962aad`, authored April 29, 2026; last updated at retrieval `2026-11-06T22:50:33.006Z`. [Extracted Markdown snapshot](../Minerva/Feature-PRDs/Sources/AgentExp-01-Linear-Requirements-2026-11-06.md) preserves the returned content, strikethrough, and inline comment markers.
- **FACT — original authoring:** [Original AgentExp-01](../Minerva/Feature-PRDs/First-Pass/AgentExp-01-Low-Code-Platform-Foundation.md), April 29, 2026. It remains unchanged.
- **FACT — app checkout:** `stellarus-apps` HEAD `d31302b658e7a01abd1d14915f575d343ececcbf`; scoped Git status was clean for CSR Chat, Customer Product Portal/API, and chat-client when inspected.
- **LIMIT:** No authenticated deployment or runtime acceptance was exercised. Existing capabilities below are supported by source, contracts, and test definitions, plus the user's statement that standalone CSR Chat has been delivered. Tests were inspected, not executed.
- **FACT — user follow-up:** Capacity across engineering, design, and QA is not an issue. Four-week completion means fully deployed to production, SDK available through a CDN, and a customer able to begin integration. Configuration must be reusable by the standalone app and existing SDK; new Nexus integration is excluded.
- **LIMIT:** No current customer setup-duration, engineering-effort, adoption, or support-volume baseline was supplied. Historical targets and cost claims are not current measurements. Functional capacity is confirmed; implementation estimates and dependency acceptance still require accountable engineering/platform owners.

## What changed between the legacy documents

| Requirement area | Original authored version | Linear version at retrieval | Implication for new scope discussion |
| --- | --- | --- | --- |
| Contextual panels | Movable, resizable, collapsible; multiple docking positions | Section A struck out; contextual panels explicitly excluded | Do not carry this forward as an assumed requirement. |
| Configuration portal | Visual builder, live preview, validation, save required in DoD | That DoD item struck out | A new administration surface needs an explicit product decision. |
| Residual panel requirements | Position/size persistence and agent workspace modes | Some related DoD items remain active despite panel exclusion | Legacy acceptance criteria are internally inconsistent. |
| Branding | Names, logos, colors, fonts, light/dark, header/footer | Broadly retained | Compare each item against the implemented settings rather than treating all as new work. |
| Integration | Nexus, embedding SDK, framework libraries, context synchronization | Broadly retained | Reconcile with current SDK delivery and the separate Nexus backlog. |
| Success metrics | Six targets across workflow, satisfaction, adoption, support, and training | Broadly retained | Replace with two or three metrics tied to the confirmed MVP workflow; establish actual baselines. |

The old $50K–$100K deployment cost, 60% disruption reduction, 50% support reduction, and training/adoption claims lack a current measurement basis in the inspected evidence. They must not become established facts or automatic release gates.

## Current capabilities to reuse

All application references below are under `/Users/jjacks20/jjacks/stellarus-dev/stellarus-apps/`.

| Capability | Observed evidence | Boundary |
| --- | --- | --- |
| Standalone CSR workflow | `apps/csr-demo-ui/README.md:3`; `src/app/page.tsx`; app behavior contract | Sign-in, service-validated plan context, and broker-backed chat already have an application foundation. Configuration must preserve these controls. |
| Branding labels and four logo slots | `apps/csr-demo-ui/src/features/csr-demo/types.ts:36`; `src/app/settings/page.tsx:109` | Portal/workspace/assistant labels; portal and assistant logo variants for light/dark contexts. |
| Logo editing and upload validation | `apps/csr-demo-ui/src/features/csr-demo/components/DemoEnvironmentCard.tsx:330`; `types.ts:103` | Existing URL/upload controls, previews, per-image 256 KiB and total 512 KiB upload limits. Shared assets would need an explicitly selected lifecycle. |
| Presentation controls | `apps/csr-demo-ui/src/features/csr-demo/types.ts:24`; `src/app/settings/page.tsx:116` | Three color profiles; two conversation presentations; context-sidebar and page-footer switches; color-token overrides. |
| Preference persistence | `apps/csr-demo-ui/src/features/csr-demo/browserPreferences.ts:23`; `docs/contracts/csr-demo-ui-contract.md:370` | Browser-local only; not a customer-wide shared record. Storage errors remain visible. Credentials/transcripts/full plan data must not enter preference storage. |
| Runtime icon mapping | `apps/csr-demo-ui/docs/contracts/csr-demo-ui-contract.md:360` | Public deployment configuration; environment rollout/restart, without an image rebuild. This is different from instant shared publishing. |
| Existing chat SDK | `packages/chat-client/README.md:59`; `README.md:96` | Headless client, controlled React surface, framework-neutral Web Component, themes/presets already exist. Page branding, plans, disclosure rendering, and authentication remain host-owned. |
| Platform customer/product administration | `apps/customer-product-portal/README.md:25`; `apps/customer-product-portal-api/README.md:115` | Existing customer identity mapping, product enablement, customer-logo media, and audit foundations. Reuse suitability for CSR configuration is not yet an approved architecture or live-readiness claim. |
| Identity and rollout controls | `apps/csr-demo-ui/README.md:3`; current flow/contract documentation | Verified-context preparation includes a traffic hold and independent acceptance prerequisites. A UI configuration PRD cannot assume identity cutover is complete. |

The app settings explicitly tell users: configuration is for this browser and is not shared with other browsers or runtime instances. That is a concrete product boundary, separate from whether a broader configuration platform exists elsewhere.

**INFERENCE — candidate problem:** Presentation customization exists, but repeatable configuration across operators, browsers, and customer launches may still depend on browser-local setup or managed deployment inputs. The degree of operational pain and desired persistence model need user confirmation.

**Confidence:** High in the observed source boundaries and legacy-document inconsistencies; moderate in the candidate operational problem; insufficient evidence for a four-week staffing commitment or quantitative business benefit.

## Current Linear work to reconcile

[No-Code/Low-Code CSR Chat project](https://linear.app/stellarus/project/no-codelow-code-csr-chat-aa4bc5fdd2bf), project `P-COMPASS-670`, is led by Jason Jackson and recorded as Build & Integrate. It still shows October 14–30 dates; those are historical tracker fields, not the new four-week commitment.

The issue query returned 23 issues with `hasNextPage=false`:

- [COMPASS-885](https://linear.app/stellarus/issue/COMPASS-885): Nexus-integrated CSR design using Vermillion; In Progress.
- [COMPASS-886](https://linear.app/stellarus/issue/COMPASS-886) and [COMPASS-887](https://linear.app/stellarus/issue/COMPASS-887): Nexus viewport work and design primitives; In Progress.
- COMPASS-888 through COMPASS-899 cover design components, error states, and usability work, mostly Todo.
- [COMPASS-39](https://linear.app/stellarus/issue/COMPASS-39): publish the private chat SDK; Done. Tracker completion is not independent verification of consumer installation.
- [COMPASS-833](https://linear.app/stellarus/issue/COMPASS-833), [COMPASS-834](https://linear.app/stellarus/issue/COMPASS-834), [COMPASS-839](https://linear.app/stellarus/issue/COMPASS-839), and [COMPASS-832](https://linear.app/stellarus/issue/COMPASS-832): additional Nexus SDK phases; Backlog.
- [COMPASS-840](https://linear.app/stellarus/issue/COMPASS-840): Nexus API/SDK approach; In Progress. [COMPASS-841](https://linear.app/stellarus/issue/COMPASS-841): external integration documentation; Todo.
- [COMPASS-193](https://linear.app/stellarus/issue/COMPASS-193): determine integration into Vue-based Nexus; Backlog.

Issue list descriptions for some SDK items were truncated by Linear. These observations use their titles/statuses and returned summaries; they do not assert full technical acceptance.

## Material alternatives for the scope conversation

These are options to confirm, not approved requirements or engineering estimates.

| Option | User outcome | Tradeoff and opportunity cost | Reversibility / decision trigger |
| --- | --- | --- | --- |
| Portable managed presets | Internal operators reuse a validated configuration through an explicit transfer/import workflow. | Smaller persistence boundary, but per-browser application can remain manual; less value if the primary pain is customer-wide publishing. | Can evolve toward shared distribution; reject if users require one update to reach every CSR. |
| Shared configuration for the standalone app | An authorized operator edits, previews, and applies a customer experience consistently across sessions/browsers. | Adds configuration ownership, authorization, distribution, version recovery, and asset dependencies; leaves Nexus integration for another workstream. | Scope the editable fields narrowly; reconsider if shared storage/runtime dependencies cannot be ready in Week 1. |
| Customer self-service | Customer admins own supported changes within their own customer boundary. | Adds customer-facing permissions, guidance, support, and acceptance needs; uses capacity that could prove the internal workflow first. | Defer external access if internal operation alone solves the initial need. |
| Configuration plus Nexus integration | Deliver a configured experience inside Nexus as well as the standalone app. | Adds external workflow, design, integration, and authentication dependencies to the same four-week commitment. | Require named owners, ready interfaces, and an explicitly reduced capability set before treating the date as credible. |

The selection criteria are: actual operator/customer pain, independence from engineering, propagation requirements, reuse of existing product/platform capabilities, external dependency readiness, and fit with confirmed delivery capacity.

## Confirmed decisions

User-confirmed delivery decisions:

1. **Release outcome:** Fully deployed to production within four weeks; SDK available through a CDN; customers able to begin integration.
2. **Capacity:** Capacity across engineering, design, and QA is not an issue.
3. **Reuse:** Configuration must work with both the standalone app and the existing SDK.
4. **Exclusion:** New Nexus integration is outside this MVP.

The user subsequently confirmed:

5. **Authoring workflow:** Stellarus-managed reusable presets selected by standalone and SDK; no new visual administration screen.
6. **Configuration domains:** Appearance/presentation only: branding, supported theme settings, labels, and existing display options.

These decisions resolve the blocking scope questions. Product acceptance targets, field/default/precedence rules, and four-week sequencing are proposed in the new PRD. Unknown current business baselines remain explicit and require Week 1 measurement; no values were inferred from silence.

Replacement artifacts:

- [Feature PRD](../Minerva/Feature-PRDs/CSR-Chat-Low-Code-No-Code-Presentation-MVP-Feature-PRD.md).
- [Acceptance and delivery details](../Minerva/Feature-PRDs/CSR-Chat-Low-Code-No-Code-Presentation-MVP-Acceptance-and-Delivery.md).

## SDK/CDN follow-up evidence

- **FACT:** The inspected SDK manifest still declares `private: true`. Existing build targets emit packaged SDK entrypoints and CSS. A separate publicly fetchable, browser-ready CDN release was not evidenced in the inspected local workflows/build targets.
- **FACT:** Full [COMPASS-39](https://linear.app/stellarus/issue/COMPASS-39) details are more qualified than its Done status: the description says approved private-registry publication is blocked on Platform prerequisites and retains a versioned tarball stopgap. Do not infer actual registry or CDN publication from the status.
- **FACT:** Full [COMPASS-839](https://linear.app/stellarus/issue/COMPASS-839) includes CDN script packaging, SRI hashes, immutable version uploads, and framework/browser fixtures. It remains Backlog. Its historical estimate is not the estimate for this new MVP.
- **FACT:** [PE-1152](https://linear.app/stellarus/issue/PE-1152) covers CDN origin, Front Door, DNS/TLS, immutable version paths, CORS/content types, publishing identity, and logging. It is In Review, assigned to Brenden Owens, with a due-date field of November 12. Its body separately requests November 20. Neither date nor status proves accepted production availability.
- **FACT:** [PE-1153](https://linear.app/stellarus/issue/PE-1153) covers registry/publish identity/consumer access; it is Backlog and unassigned. CDN distribution is explicitly required by the user; a new package-registry launch has not been added as an independent MVP requirement.
- **INFERENCE:** Production CDN delivery and a customer integration rehearsal must be explicit acceptance gates. Existing SDK source/package availability alone cannot satisfy the confirmed outcome.
- **ASSUMPTION TO VALIDATE:** Existing approved identity, tenant/context, and chat endpoints can support the chosen production integration path. Authentication and real service acceptance must be evidenced before release; this PRD must not promise a replacement identity platform or Nexus integration.
- **FACT:** [COMPASS-137](https://linear.app/stellarus/issue/COMPASS-137) is Done, while its description retains an unresolved production proxy operating-model decision. [PE-1158](https://linear.app/stellarus/issue/PE-1158), Returned to Requester, asserts that a Stellarus-managed transitional edge is established and requests extension to Nexus-specific routes. The records conflict about accepted operating readiness; neither resolves live production acceptance for this MVP.
- **BOUNDARY:** The Nexus-specific API/edge extension in PE-1158 is not imported into the new MVP merely because it references the same SDK. The selected existing chat route still needs its own production owner, customer onboarding instructions, and authenticated integration evidence.
- **PROPOSED RELEASE PROOF:** A fresh external-origin sample loads the pinned production SDK and CSS from the CDN, applies the approved shared presentation settings, and completes an authenticated supported chat journey through the selected existing backend path. A CDN file returning HTTP 200 or a fixture-only demo would not by itself prove customers can begin integration. Detailed acceptance remains pending the configuration-domain decision.

## Artifact and validation evidence

- **F:** This discovery record and the extracted Linear source snapshot were created; legacy PRDs and all product source remain unchanged.
- **T:** No executable product behavior changed; product tests/builds do not apply to source extraction. Artifact checks verify snapshot equality against the connector response, required provenance, and local Markdown links.
- **C:** Preserve contradictory legacy requirements as historical evidence; identify reuse and scope alternatives before making a new commitment. Scope delta: none.
- **O:** Linear get_document → project/resources/milestones → full project issue listing → related-document search; local skill/template, legacy PRDs, app/settings/preferences/contracts, SDK, and Portal documentation reads; read-only Git status/HEAD inspection; Markdown extraction and discovery recording.

This record preserves source discovery and the resolved interactive decisions. The linked replacement PRD is a review-ready planning artifact; it does not attest product implementation or production deployment.

