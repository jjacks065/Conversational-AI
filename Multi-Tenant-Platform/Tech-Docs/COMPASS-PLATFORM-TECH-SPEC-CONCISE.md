# Compass Platform — Technical Specification (Concise)

> **Trimming policy**: Narrative preambles, Quick-navigation blocks, Trigger-for-revisit prose, and cross-reference paragraphs removed. All 55 mermaid diagrams, all tables, all clause IDs (INV-N / SEQ-N / WI-* / IP-N), Key Constraints & Rules bullets, and Decisions Still Open tables kept verbatim.
>
> **Source**: `docs/compass-platform/COMPASS-PLATFORM-TECH-SPEC.md` (commit `3f9a0d32`, 4,879 lines)
>
> **Branch**: `feat/compass-platform-requirements`

---


## 1. Overview & Vision

The Compass Platform is Stellarus's reusable, multi-tenant conversational AI platform — the Stellarus-owned primitives through which any customer surface reaches a conversational AI runtime. It is owned by Jason Jackson. Its first customer is BSC member chat; its MVP gate is September 1, 2026; its platform horizon is December 31, 2026.

The platform is the suite of primitives — the Stellarus SDK and API, the Thin-Router Broker, the Tenant/Auth Spine, Benefits grounding, Escalation, and Telemetry — that together let a customer surface (today BSC member chat; tomorrow IVR, CSR-assist, or a partner-embedded widget) hold a grounded, governed conversation without that surface ever knowing the name of the runtime behind it. Compass owns the trust boundary, the tenant identity, the conversation record, and the observability; the external runtime is a swappable detail behind an adapter.

**Compass Platform is not a Sierra integration and it is not a Genesys integration.** Sierra.ai is runtime-only — reached exclusively through `SierraAdapter`, never a hardcoded broker dependency, and its native session storage is **not** the authoritative conversation record. The Benefits Service is the governed source of truth for plan and benefits data, reached through `RestBenefitsAdapter` under the `benefits.query` capability. Genesys Cloud CCaaS receives escalation handoffs only through `GenesysAdapter`. Every external system the platform touches sits behind a Stellarus-owned adapter, registered by YAML, so that the platform — not the vendor — owns the contract.

### 1.1 The strategic thesis (all three analysts agree)

- **Do NOT ship BSC member chat as a one-off Sierra/Genesys integration.** Ship it through Stellarus primitives. A direct Sierra/Genesys wiring would deliver one customer and zero platform.
- **SDK + Broker ownership is the platform moat.** The value Stellarus captures is the reusable surface (`@stellarus/chat-client`) and the capability-neutral router (`agentic-broker-api`), not the conversation a single vendor happens to power this quarter.
- **Any Sierra-direct data fetch is temporary debt.** It is permitted only with a named owner, explicit exit criteria, and a removal date. Debt without those three attributes is a constitutional violation of the thesis, not a pragmatic shortcut.

The structural enforcement of this thesis lives in the broker. The **Thin-Router Broker** exposes exactly ONE HTTP endpoint — `POST /dispatch` — and never knows semantic names; it resolves an opaque `(capability, customer_slug)` pair to a `DataSourceAdapter` via YAML (INV-01, INV-02, INV-11). Because there is structurally nowhere to add a named semantic route, there is nowhere for business logic to accumulate, and there is no path by which a "quick Sierra call" becomes load-bearing.

### 1.2 What the platform owns and does NOT own

Compass Platform **owns**:

- the edge trust boundary and tenant identity — the **Context token** issued by **CCS**, validated by **ContextTokenGuard**, carrying the immutable `customer_slug`
- the conversational SDK surface (`@stellarus/chat-client`) consumed by customer developers
- the capability-neutral routing contract (`POST /dispatch`) and the adapter registry
- the authoritative, durable conversation record (`PostgresConversationAdapter`, per-tenant Postgres schema isolation — INV-06, INV-07)
- the PII/PHI redaction gate that scrubs all content before it leaves Stellarus
- the launch telemetry, SLOs, and go/no-go launch gates

Compass Platform does **not** own:

- the conversational AI model itself — Sierra.ai is runtime-only, behind `SierraAdapter`
- the live-agent contact center — Genesys Cloud CCaaS, behind `GenesysAdapter`
- human authentication — Auth0 authenticates humans via PKCE; CCS does not authenticate humans
- the plan/benefits data of record — the Benefits Service is the governed source of truth

### 1.3 The canonical runtime path

```text
Customer surface
  -> Stellarus SDK/API (@stellarus/chat-client)
    -> Stellarus Broker (POST /dispatch, capability-neutral)
      -> Sierra.ai (chat.completion via SierraAdapter)
      (+ Benefits grounding   — benefits.query   via RestBenefitsAdapter)
      (+ Escalation / CCaaS    — escalation.initiate via GenesysAdapter)
      (+ Telemetry             — structured logs -> Loki -> Grafana SLO panels)
```

```mermaid
flowchart LR
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef sierra fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000

    surface["Customer surface (BSC member chat)"]:::client
    sdk["Stellarus SDK (@stellarus/chat-client)"]:::client
    apim["APIM (Azure API Management)"]:::edge
    bff["BFF (agentic-broker-chat)"]:::backend
    broker["Thin-Router Broker (POST /dispatch)"]:::backend
    sierra["Sierra.ai (chat.completion)"]:::sierra
    benefits["Benefits Service (benefits.query)"]:::store
    genesys["Genesys CCaaS (escalation.initiate)"]:::sierra
    telemetry["Telemetry (Loki -> Grafana SLOs)"]:::store

    surface -->|"useChat.chat()"| sdk
    sdk -->|"Bearer JWT to /chat"| apim
    apim -->|"x-context-token + x-correlation-id"| bff
    bff -->|"{ capability, payload }"| broker
    broker -->|"SierraAdapter.stream()"| sierra
    broker -.->|"RestBenefitsAdapter.query()"| benefits
    broker -.->|"GenesysAdapter (P5)"| genesys
    broker -.->|"structured JSON logs"| telemetry
```

The path maps directly onto the manifest sequence clauses: the SDK acquires the Auth0 Bearer JWT before any fetch (SDK-A1-SEQ-2); APIM validates it, calls CCS `POST /validate/token`, and injects `x-context-token` plus a fresh `x-correlation-id` (TENANT-D1-SEQ-1, SEQ-3, SEQ-4); the BFF translates surface semantics into a capability string and dispatches (BROKER-B1B2-SEQ-1); the broker checks the per-tenant rate limit before resolving (BROKER-B1B2-SEQ-2), resolves to the adapter (SEQ-3), and propagates `x-correlation-id` onward (SEQ-7).

### 1.4 First customer, MVP gate, and platform horizon

| Milestone | Value | Meaning |
|---|---|---|
| First customer | BSC member chat | the first surface to ride the platform end to end |
| MVP gate | September 1, 2026 | Release Candidate go/no-go for BSC member chat (Jason signs the F1 launch gates) |
| Platform horizon | December 31, 2026 | the date by which the primitives are reusable beyond BSC |

### 1.5 The six-project platform map

| Project | Primitive | Lead | Target | Cross-team gate |
|---|---|---|---|---|
| **P1** | SDK / API (`@stellarus/chat-client`) | Julie Hughes | Aug 15 | SDK v2 (A5) blocked on E1 (escalation) |
| **P2** | Thin-Router Broker (`agentic-broker-api`) | Jason | Aug 15 | — |
| **P3** | Benefits Grounding (`RestBenefitsAdapter`, Benefits Service) | Jason | Aug 15 | **Jun 28** (C1/C2 Benefits LoB) |
| **P4** | Tenant Context / Auth Spine (CCS context-token contract) | Jason | Jul 15 | **Jun 28** (D1 token contract) — everything downstream blocks here |
| **P5** | Escalation / CCaaS (`GenesysAdapter`, PII/PHI Redactor) | Julie Hughes | Aug 15 | E1 mechanics BLOCKED on BSC/PTP |
| **P6** | Launch Telemetry (Loki -> Grafana SLOs, launch gates) | Jason | Aug 25 | F1 thresholds blocked on ACT-JASON |

The two **June 28 cross-team gates** are the spine of the schedule. **P4 (D1)** — the CCS context-token contract — gates everything downstream: the SDK cannot lock its surface, the broker cannot enforce `@RequireScopes('chat')`, and Benefits cannot perform production RS256 verification until the token contract and the `chat` scope (WI-D1-A, IRREVERSIBLE) are settled. **P3 (C1/C2)** — Benefits LoB coverage and fallback — gates the grounding answer quality the MVP is judged on. SDK v2 (A5), which carries the escalation event shape, is blocked on **E1** (Genesys API mechanics), which is itself BLOCKED on BSC/PTP.

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef sierra fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000

    p4["P4 Tenant / Auth Spine (D1)<br/>Lead: Jason — Jul 15<br/>Jun 28 gate: token contract"]:::edge
    p3["P3 Benefits Grounding (C1/C2)<br/>Lead: Jason — Aug 15<br/>Jun 28 gate: Benefits LoB"]:::store
    p1["P1 SDK / API (A1)<br/>Lead: Julie Hughes — Aug 15"]:::client
    p2["P2 Thin-Router Broker (B1/B2)<br/>Lead: Jason — Aug 15"]:::backend
    p5["P5 Escalation / CCaaS (E1/E2)<br/>Lead: Julie Hughes — Aug 15"]:::sierra
    p6["P6 Launch Telemetry (F1/F2)<br/>Lead: Jason — Aug 25"]:::store

    p4 -->|"chat scope + RS256 verify (INV-12)"| p2
    p4 -->|"context token + scopes"| p1
    p4 -->|"benefits:read RS256 verify"| p3
    p3 -->|"grounding data (benefits.query)"| p2
    p2 -->|"conversation.history store"| p5
    p1 -->|"escalation event shape (SDK v2 / A5)"| p5
    p2 -->|"canonical F2 log fields"| p6
    p3 -->|"plan-fetch log fields"| p6
    p5 -->|"escalation SLO logs"| p6
```

### 1.6 As-built reality (the starting line)

| Tier | State | What exists |
|---|---|---|
| **`main` (as-built today)** | merged, running | the `@stellarus/resolver` package — `(capability, customer_slug) -> DataSourceAdapter` via YAML with chokidar hot-reload — plus the `@stellarus/chat-client` core, `RestBenefitsAdapter`, and the BFF-side Plan Validation Gate (PVG) |
| **Unmerged feature branches** | written, not merged | the SDK surface (`StellarusProvider`/`useChat`/`fetchPlan`), the broker plan endpoint, JWKS rotation handling, and the whitelabel brand-slug resolver |
| **Compass Platform itself** | requirements only | the six requirements manifests — zero implementation code. This is the work this spec scopes. |

The **Resolver (`@stellarus/resolver`)** is on `main` and is the structural foundation the broker thin-router pattern depends on — it is distinct from the broker's `brand-slug.resolver.ts`. But the broker MVP gap (replacing `POST /v2/chat` with `POST /dispatch`, the `SierraAdapter`, the `PostgresConversationAdapter`, the `stream()` seam — WI-B1-A through WI-B1-F) is **to-be-built**. The SDK surface is written on a branch but the v1 surface lock is not merged. The Compass Platform primitives that this document specifies exist today only as the requirements manifests that source it.

### 1.7 Critical-path ordering and rework risk

1. **CCS token contract + Tenant/Auth Spine (P4 / D1)** — the `chat` scope, the context-token claim set, the RS256 verification path. Everything downstream consumes the verified `customer_slug` and `scopes`.
2. **Benefits LoB coverage / fallback (P3 / C1/C2)** — the grounding the answer quality is judged on.
3. **SDK v1 surface (P1 / A1)** — the surface lock customers build against.
4. **Broker contract + alpha (P2 / B1/B2)** — `POST /dispatch`, the adapters, the conversation store.
5. **Escalation contract for SDK v2 (P5 / E1/E2)** — the typed escalation event shape and the Genesys handoff.
6. **Telemetry / launch gates (P6 / F1/F2)** — the SLOs and the go/no-go evidence chain.

**Rework risk is concentrated in two slips.** If **(1) the D1 token contract slips**, every downstream consumer — SDK scope expectations, broker `@RequireScopes('chat')`, Benefits RS256 verification — was built against a contract that then moved, forcing rework across P1, P2, and P3 simultaneously. If **(2) the C1/C2 Benefits LoB coverage slips**, the grounding data the SLO answer-quality gate measures is incomplete, and either the launch gate fails on real evidence (F1F2 INV-04 forbids "we believe") or the quality bar is silently lowered. Both are June 28 cross-team gates precisely because a late slip there is the most expensive failure the schedule can absorb.

### 1.8 Key Constraints & Rules

- **Ship through Stellarus primitives, never a vendor one-off.** BSC member chat reaches Sierra and Genesys only through Stellarus-owned adapters. A direct integration delivers one customer and zero platform.
- **The broker exposes exactly one endpoint.** `POST /dispatch` is capability-neutral; any named semantic HTTP endpoint on `agentic-broker-api` is a detectable contract violation (BROKER-B1B2 INV-01, INV-11). All semantic routing lives in BFF apps (INV-05).
- **Capabilities are opaque and YAML-registered.** The broker never references `chat`, `conversation`, or `benefits` by name in routing logic (INV-02); a new capability is a dropped YAML file in `RESOLVER_CONFIG_DIR`, never a broker code change (INV-03).
- **Sierra is runtime-only.** It is never a hardcoded broker dependency, and its native session storage is **not** the authoritative conversation record — `PostgresConversationAdapter` is (INV-06).
- **The Benefits Service is the governed source of truth** for plan/benefits data, reached via `RestBenefitsAdapter` under `benefits.query`.
- **Any Sierra-direct data fetch is temporary debt** requiring a named owner, explicit exit criteria, and a removal date. Debt missing any of the three is a thesis violation.
- **Tenant identity is resolved at the edge, never client-supplied.** `customer_slug` travels in the verified context token from APIM/CCS and drives all tenant scoping (TENANT-D1 INV-06, INV-07).
- **Distinguish as-built from to-be-built.** `main` = resolver + chat-client core + PVG; branches = SDK surface, broker plan endpoint, JWKS rotation, brand-slug; Compass Platform = requirements manifests only.

### 1.9 Decisions Still Open

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 1 | `chat` scope persona grants (member + employee — exact grants TBD) | ACT-CCS / Ketema (WI-D1-A) | IRREVERSIBLE CCS migration `0003_chat_scopes.sql`; gates `@RequireScopes('chat')` on `/dispatch` |
| 2 | Benefits LoB coverage + fallback completeness (C1/C2) | Jason / Data + App team | Jun 28 cross-team gate; the grounding the answer-quality SLO is judged on |
| 3 | Genesys API mechanics, routing metadata, SLA, PII allow-list (E1-Z1..Z4) | Julie Hughes + BSC/PTP | BLOCKED; gates SDK v2 (A5) escalation event shape and `GenesysAdapter` |
| 4 | SLO threshold values + composite weights (F1-Z1, F2-Z4) | ACT-JASON | blocks all dashboard build and the F1 launch-gate evidence chain |

**The single biggest blocking decision is the D1 token contract (June 28).** It is the one input that, if it slips, forces simultaneous rework across the SDK, the broker, and Benefits Grounding — the rest of the schedule is built on the assumption that the `customer_slug`, `scopes`, and RS256 verification path are frozen by then.

## 2. Scope (In / Out for the September MVP)

### In Scope (Sep 1 MVP)

- BSC member chat via SDK v1 — Auth0 PKCE, `StellarusProvider`, `useChat`, `fetchPlan` (A1, `@stellarus/chat-client` surface-lock, SDK-A1-SEQ-1 through SEQ-7)
- `StellarusProvider` PKCE entry point — owns token lifecycle, checks the `?code=` callback at mount (SDK-A1-SEQ-6; INV-11/12 keep Auth0 domain/audience/`useRefreshTokens` internal)
- `useChat` streaming state machine — `chat(opts)` + `abort()`, aborts in-flight SSE on unmount (SDK-A1-SEQ-7)
- `fetchPlan` three-state result — `PLAN_STATUS_NOT_FOUND` (404) / `PLAN_STATUS_OUTAGE` (503), never throws (SDK INV-06)
- broker `POST /dispatch` capability-neutral routing — the broker's only endpoint, `{ capability, payload }` plus `x-context-token` and `x-correlation-id` (B1B2 INV-01/02/11; replaces `POST /v2/chat`, WI-B1-F)
- the three live MVP capabilities — `chat.completion`, `benefits.query`, `conversation.history`, each resolved by YAML, never by broker code change (B1B2 INV-03)
- CCS context-token contract extension — the new **`chat` scope** (resource=chat, action=all), no send/receive split, gating `@RequireScopes('chat')` on `/dispatch` (WI-D1-A, IRREVERSIBLE; migration `0003_chat_scopes.sql`)
- `ContextTokenGuard` verification path — RS256 against CCS JWKS, `iss`/`aud`/`exp`, scope enforcement (TENANT-D1-SEQ-5/6/7; INV-06/07)
- `x-correlation-id` propagation — APIM-generated UUIDv4, stripped inbound, threaded BFF → broker → adapters → every log line (TENANT-D1-SEQ-3/4, BROKER-B1B2-SEQ-7, F1F2 INV-06)
- `PostgresConversationAdapter` per-tenant durable store — authoritative conversation history under `conversation.history`, `conversation-bsca.yaml` (new), per-tenant schema isolation (WI-B1-E; INV-06/07; Sierra native storage is NOT the source of truth)
- `SierraAdapter` wired via YAML — streaming adapter under `chat.completion`, `sierra-bsca.yaml`, absorbing token counting + Sierra circuit breaker (WI-B1-B/C; INV-09/10)
- `RestBenefitsAdapter` wired via YAML — `benefits.query`, `benefits-bsca.yaml` (exists), replacing the broker's `PlanHandlerService` direct-HTTP path (WI-B1-D)
- the `stream()` seam on `DataSourceAdapter` — optional `stream(): AsyncIterable<StreamEvent>` splitting query-shaped from streaming-shaped adapters (WI-B1-A, blocker)
- per-feature telemetry instrumentation — broker and benefits emit structured JSON with **exact** canonical F2 field names, no member-identifiable data (WI-F3-A/B; F1F2 INV-01a/01b/02a/02b)
- Grafana SLO panels — threshold-colored (green/yellow/red) per the F2 taxonomy via Loki LogQL, every alert annotated with `runbook_url` (WI-F3-C; F1F2 INV-03/07)
- F1 launch-gate evidence chain — documented go/no-go evidence across quality, security, privacy, support, rollback, signed off by Jason before the RC (TELEMETRY-F1F2-SEQ-6; INV-04)

### Out of Scope / Deferred

- **live Genesys escalation wiring** — the live leg defers (E1 BLOCKED on BSC/PTP: Genesys API shape E1-Z1, routing metadata E1-Z2, PII allow-list E1-Z3, SLA E1-Z4) — **but the contract-and-build-now perimeter does NOT defer:** the PII/PHI Redactor (`packages/redactor`, WI-E2-B), the SDK v2 escalation event shape (`escalation_initiated`/`_succeeded`/`_failed`/`_unavailable`, WI-E2-D), and the escalation BFF route on agentic-broker-chat (WI-E2-E) are all built and contracted this cycle; only the GenesysAdapter's live call to Genesys Cloud waits on the unblocked zones
- `csr` persona — a BSC CSR is NOT a Stellarus employee; DEFERRED to a separate persona (WI-D1-B; not in `VALID_PERSONAS`)
- ENG-286 per-consumer `aud` — referenced as a dependency only; today `aud` is the constant `stellarus-context-token`, Phase 2 per-consumer scoping is out of D1 scope (WI-D1-D)
- multi-agent routing — beyond single-capability dispatch (B6, DEFERRED)
- additional LoB adapters — beyond Sierra/REST-benefits/Postgres-conversation (C5, Q4 2026)
- analytics-app external multi-tenant GA — the BI surface stays internal; the cross-tenant cache/isolation refactor (CRIT-1/2/3, Auth0 `org_id`) is a refactor-not-rebuild backlog item, not a September deliverable
- npm / CDN distribution of the SDK — v1 ships internally; public package + CDN deferred (A6)
- legacy `POST /chat` deletion — kept for backward-compat until the BFF fully migrates to `/dispatch` (WI-B1-I, DEFERRED)
- `RateLimiterService` guard/interceptor refactor — the limiter stays as inline broker edge middleware for MVP; the NestJS guard refactor is cosmetic and deferred (WI-B1-H, DEFERRED)
- `SnowflakeBenefitsAdapter` — scaffolded-but-stub demo/future path (`benefits-bsca-snowflake.yaml`); v1 `benefits.query` is REST-only
- `system`-persona `mode` / API-key path — `live`/`test` keys are out of the human member-chat MVP surface

> **BLOCKED — C1/C2 Benefits LoB coverage & fallback.** No manifest exists for the
> Benefits Grounding coverage/fallback slice (EOC-PDF ingestion and the "what does the CRI
> agent answer from" data loop, C-Z1–C-Z4, GitHub #13). Because there is no requirements
> artifact, C1/C2 is **out of this spec's contract scope** — `RestBenefitsAdapter`
> transports `benefits.query`, but the governed completeness of the underlying benefits
> data is undefined. **Decision for v1:** ship the adapter transport, name the data-coverage
> gap explicitly. This remains a named **critical-path risk** (MVP critical-path step 2: Benefits LoB
> coverage/fallback) even though it is not contracted here.

#### September MVP Scope Boundary

```mermaid
flowchart LR
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000
    classDef straddle fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000

    subgraph inscope["In Scope — Sep 1 MVP"]
        sdk["SDK v1 (PKCE, useChat, fetchPlan)"]:::backend
        dispatch["broker POST /dispatch"]:::backend
        caps["chat.completion / benefits.query / conversation.history"]:::backend
        scope["CCS chat scope (@RequireScopes)"]:::backend
        conv[("PostgresConversationAdapter")]:::store
        telem["telemetry + Grafana SLO panels"]:::backend
    end

    subgraph deferred["Out of Scope / Deferred"]
        genesys["live Genesys leg (E1 BLOCKED)"]:::boundary
        csr["csr persona"]:::boundary
        eng286["ENG-286 per-consumer aud"]:::boundary
        multi["multi-agent routing (B6)"]:::boundary
        analytics["analytics-app multi-tenant GA"]:::boundary
        npm["npm / CDN distribution (A6)"]:::boundary
    end

    redactor["PII/PHI Redactor (packages/redactor)"]:::straddle
    sdkv2["SDK v2 escalation event shape"]:::straddle

    sdk -->|"Auth0 Bearer JWT"| dispatch
    dispatch -->|"YAML resolve"| caps
    scope -->|"gates"| dispatch
    caps -->|"persist turns"| conv
    dispatch -->|"x-correlation-id"| telem

    redactor -.->|"contract-now, wire-later"| genesys
    sdkv2 -.->|"contract-now, wire-later"| genesys
    caps -.->|"escalation.initiate (route built, leg deferred)"| redactor
```

### Slice taxonomy (elicitation discipline)

| Category | Meaning | Elicitation depth | Examples this cycle |
|---|---|---|---|
| **SEAM** | integration boundary already contracted | reference the existing contract, do not re-spec | Auth0 M2M APIM shim (`62f5cad5`), ENG-257 CCS JWKS, `@stellarus/resolver` |
| **IRREVERSIBLE** | lasting consequences | full `/req-elicit` before touching | `chat` scope (WI-D1-A), `POST /dispatch` contract, `PostgresConversationAdapter` store, SDK v1 surface-lock |
| **SLICE-LOCAL** | implementation detail | thin contract, no discovery dialogue | `InternalContextClaims`/`ContextTokenPayload` alignment (WI-D1-E), correlation-id threading |
| **DEFERRED** | valid but not this cycle | explicit backlog note, no contract | legacy `/chat` delete (WI-B1-I), RateLimiter refactor (WI-B1-H), `csr` persona (WI-D1-B), npm distribution (A6) |

## 3. Architecture Position

### Platform Architecture Position

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef identity fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef external fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    client["Browser / SDK (@stellarus/chat-client)"]:::client
    auth0["Auth0 (stellarus-sb2.us.auth0.com)"]:::identity
    apim["Azure APIM (network trust boundary)"]:::edge

    subgraph aks["AKS cluster (Istio mTLS internal network)"]
        direction LR
        bff["agentic-broker-chat (BFF)"]:::backend
        broker["agentic-broker-api (Thin-Router Broker, POST /dispatch only)"]:::backend
        ccs["Customer Configuration Service (CCS)"]:::ccs
        sierraAd["SierraAdapter (chat.completion)"]:::backend
        benefitsAd["RestBenefitsAdapter (benefits.query)"]:::backend
        convAd["PostgresConversationAdapter (conversation.history)"]:::backend
        genesysAd["GenesysAdapter (escalation.initiate)"]:::backend
        benefitsSvc["benefits-service"]:::backend
        convDb[("Conversation Postgres (per-tenant schema)")]:::store
        benefitsDb[("Benefits Postgres (customer-partitioned)")]:::store
        ccsDb[("CCS Postgres")]:::store
    end

    sierra["Sierra.ai (external AI runtime)"]:::external
    genesys["Genesys Cloud CCaaS (external)"]:::external

    client -->|"(1) Bearer Auth0 JWT to /chat"| apim
    apim -->|"(2) JWKS fetch (cached per iss)"| auth0
    apim -.->|"(3) POST /validate/token (internal)"| ccs
    apim -->|"(4) x-context-token (RS256 JWT), x-correlation-id"| bff
    bff -->|"(5) POST /dispatch { capability, payload }"| broker
    broker -->|"(6) resolve(chat.completion, slug)"| sierraAd
    broker -->|"resolve(benefits.query, slug)"| benefitsAd
    broker -->|"resolve(conversation.history, slug)"| convAd
    broker -->|"resolve(escalation.initiate, slug)"| genesysAd
    sierraAd -->|"(7) SSE stream"| sierra
    sierraAd -->|"(8) persist each turn"| convAd
    convAd --- convDb
    benefitsAd -->|"HTTP benefits.query"| benefitsSvc
    benefitsSvc --- benefitsDb
    genesysAd -->|"redacted context + routingMetadata"| genesys
    ccs --- ccsDb
    broker -.->|"verify context token vs CCS JWKS"| ccs
    benefitsSvc -.->|"verify context token vs CCS JWKS"| ccs
```

### Component Identity & Trust Roles

| Component | Diagram class | Trust role |
|---|---|---|
| Browser / SDK (`@stellarus/chat-client`) | client (blue) | Untrusted. Holds an Auth0 access JWT only; never sees a context token, broker URL, or internal service name (SDK INV-01/09). |
| Auth0 (`stellarus-sb2.us.auth0.com`) | identity (orange) | Authenticates humans via PKCE; issues access JWTs carrying the `https://stellarus.com/persona` custom claim. |
| Azure APIM | edge (red) | The network trust boundary. The only ingress; validates external credentials, injects trusted headers, strips untrusted ones. |
| agentic-broker-chat (BFF) | backend (green) | Owns all semantic routes for the chat surface; acquires the context token via APIM; dispatches capabilities. |
| agentic-broker-api (broker) | backend (green) | Capability-neutral router. One endpoint, `POST /dispatch`; resolves `(capability, customer_slug)` to an adapter; owns rate limiting. |
| SierraAdapter / RestBenefitsAdapter / PostgresConversationAdapter / GenesysAdapter | backend (green) | Each owns one downstream and its circuit breaker; registered by YAML, instantiated by the resolver. |
| CCS (`customer-configuration-service`) | ccs / internal-trust (teal) | The authoritative issuer/signer/validator of context tokens; owns the scope + persona registry. |
| Postgres stores (conversation, benefits, CCS) | store (purple) | Per-tenant / customer-partitioned durable state. |
| Sierra.ai, Genesys Cloud CCaaS | external (grey) | External runtimes, reachable only through their dedicated adapter. |

### owns / does NOT own

**APIM owns:**
- validating external caller credentials (Auth0 JWT signature, issuer, expiry)
- calling CCS `POST /validate/token` and injecting the resulting `x-context-token`
- generating one UUIDv4 `x-correlation-id` per request and stripping any inbound one (TENANT-D1-INV-04)

APIM does **not** own:
- customer-resolution rules themselves — those live in CCS
- context-token signing — CCS signs, APIM only carries
- any semantic routing decision — that is the BFF's

**The broker owns:**
- resolving `(capability, customer_slug)` to a `DataSourceAdapter` via the resolver
- per-tenant rate limiting as cross-cutting edge middleware, on `customer_slug` from the verified token (BROKER-B1B2-INV-08)
- propagating `x-correlation-id` to the adapter (BROKER-B1B2-SEQ-7)

The broker does **not** own:
- semantic routing — it never references `chat`, `conversation`, or `benefits` by name (BROKER-B1B2-INV-02)
- any HTTP endpoint other than `POST /dispatch` (BROKER-B1B2-INV-01, INV-11 drift guard)
- provider-specific logic — no `SierraClientService` import, no token counting, no circuit breaker (BROKER-B1B2-INV-04/09/10)

**CCS owns:**
- issuing and signing RS256 context tokens (`TokenService.sign()`)
- the scope registry (14 scopes + the new `chat` scope) and persona registry (`member`, `employee`, `provider`, plus `system`)
- exposing `POST /validate/token` and (ENG-257) `/.well-known/jwks.json`

CCS does **not** own:
- authenticating humans — Auth0 does; CCS validates an already-authenticated persona
- embedding `correlation_id` in the signed token (TENANT-D1-INV-02) — that is header-only, APIM-generated

**Each adapter owns** its downstream's failure state machine: Sierra's circuit
breaker lives in `SierraAdapter`, Genesys's in `GenesysAdapter`
(BROKER-B1B2-INV-09). No adapter owns another's downstream, and `GenesysAdapter`
is the **only** component permitted to call the Genesys API (E1E2-INV-05).

### The Two-Token Reality

| Token | Issuer | Signature | Carries | Travels as | Verified by / where |
|---|---|---|---|---|---|
| Auth0 access JWT | Auth0 (`stellarus-sb2.us.auth0.com`) | Auth0 JWKS (per-issuer) | human identity + `https://stellarus.com/persona` | `Authorization: Bearer <jwt>` | APIM, at the edge — against Auth0 JWKS |
| Context token | CCS (`TokenService.sign()`) | RS256, CCS JWKS | `iss`, `aud`, `exp`, `iat`, `sub`, `customer_id`, `customer_slug`, `principal_id`, `persona`, `scopes[]`, optional `mode` | `x-context-token` header | `ContextTokenGuard` in each internal service — against CCS JWKS |

The Auth0 JWT is the external credential and never crosses the edge inward — APIM
strips it from the trust surface and replaces it with the context token. The
context token is the **internal** credential: it is what every AKS service trusts,
and `ContextTokenGuard` re-verifies its RS256 signature, `iss`, `aud`, and `exp`
on every hop (TENANT-D1-INV-06) before enforcing `@RequireScopes()`
(TENANT-D1-INV-07). The `correlation_id` is in neither token — it is an
observability-only HTTP header (TENANT-D1-INV-05), and `mode`
appears only in `system`-persona API-key tokens (TENANT-D1-INV-09).

The shared verification path is `ContextTokenGuard` from
`@stellarus/auth/internal/nest`. It is the platform's single intended way to
verify a context token — and the source of the central divergence below.

### Central Divergence — Broker Auth & Session Convergence

```mermaid
flowchart LR
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    subgraph current["broker-api — current (as-built)"]
        direction TB
        curGuard["local jose JWT guard (src/auth/*.guard.ts)"]:::boundary
        curStore["in-memory session store (NoOp, lost on restart)"]:::boundary
        curNote["does NOT consume packages/auth or packages/db"]:::boundary
        curGuard --- curStore --- curNote
    end

    subgraph target["broker-api — target (MVP)"]
        direction TB
        tgtGuard["ContextTokenGuard from @stellarus/auth/internal/nest"]:::backend
        tgtStore["PostgresConversationAdapter (per-tenant schema, @stellarus/db)"]:::backend
        tgtNote["same spine as benefits-service"]:::backend
        tgtGuard --- tgtStore --- tgtNote
    end

    current -->|"convergence (retire local duplication)"| target
```

The convergence is two coordinated moves: replace the local `jose` guard with
the shared `ContextTokenGuard` (verifying against CCS JWKS per TENANT-D1-INV-06,
falling back to a static PEM only on transport failure until ENG-257 lands, then
never — INV-12a), and replace the in-memory store with
`PostgresConversationAdapter` registered via `conversation-bsca.yaml`
(BROKER-B1B2-INV-06/07, work item WI-B1-E). Retiring this duplication is the
single most consequential structural change between the current platform and the
MVP target.

### Trust Boundaries

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000

    ext["External clients (Browser / SDK) — UNTRUSTED"]:::client
    apim["APIM — TRUST BOUNDARY"]:::edge
    internal["Internal AKS services (BFF, broker, CCS, adapters) — TRUSTED NETWORK"]:::backend

    ext -->|"must pass through APIM — no direct service access; Auth0 JWT validated vs JWKS"| apim
    apim -->|"strips untrusted x-* headers; injects signed x-context-token + fresh x-correlation-id"| internal
    internal -->|"Istio mTLS verifies peer identity; ContextTokenGuard re-verifies RS256 token vs CCS JWKS"| internal
```

| Layer | Trust level | Verification |
|---|---|---|
| External clients (Browser / SDK) | Untrusted | Must pass through APIM — no direct service access. Auth0 JWT validated against Auth0 JWKS. |
| APIM | Trust boundary | Validates external credentials; strips untrusted inbound `x-*` headers (notably any forged `x-correlation-id`, TENANT-D1-INV-04); injects the signed `x-context-token`. |
| Internal AKS services | Trusted network | Istio mTLS verifies peer service identity; `ContextTokenGuard` independently re-verifies the context token's RS256 signature, `iss`, `aud`, `exp` on every request (TENANT-D1-INV-06). |

### As-Built Today vs To-Be-Built for MVP

| Concern | As-built today | To-be-built for MVP |
|---|---|---|
| Broker endpoint | semantic `POST /v2/chat`, `POST /chat` | capability-neutral `POST /dispatch` only (WI-B1-F) |
| Broker token verification | local `jose` guard in `src/auth/*.guard.ts` | shared `ContextTokenGuard` from `@stellarus/auth/internal` |
| Conversation store | in-memory NoOp (lost on restart) | `PostgresConversationAdapter`, per-tenant schema (WI-B1-E) |
| Sierra | hardcoded `SierraClientService` dependency | `SierraAdapter` (streaming) via `sierra-bsca.yaml` (WI-B1-B) |
| Benefits | broker `PlanHandlerService` direct HTTP | `RestBenefitsAdapter` via `benefits-bsca.yaml` (merged on main, WI-B1-D) |
| Circuit breaker / token counting | `CircuitBreakerService` + `TokenCounterService` in broker | moved into `SierraAdapter` (WI-B1-C) |
| `chat` scope gate | none | `@RequireScopes('chat')` on `/dispatch` (CCS migration `0003_chat_scopes.sql`, WI-D1-A) |
| CCS JWKS | broker falls back to static `CONTEXT_TOKEN_PUBLIC_KEY` | `/.well-known/jwks.json` (ENG-257); static fallback forbidden in prod (INV-12a/b) |
| Escalation / GenesysAdapter | none | `escalation.initiate` via `genesys-bsca.yaml` (P5/E2 scope) |

The resolver (`@stellarus/resolver`) and `RestBenefitsAdapter` are already merged
to main; the rest of the right column is the broker convergence work. None of it
adds a named broker endpoint — every new capability arrives as a YAML file in
`RESOLVER_CONFIG_DIR` (BROKER-B1B2-INV-03), which is exactly why the thin-router
contract is the structural guard against the drift this section documents.

## 4. The Thin-Router Broker

### 4.2 Scope

#### In Scope

- the single `POST /dispatch` endpoint and its request/response contract
- `(capability, customer_slug)` -> adapter resolution via `@stellarus/resolver` YAML
- per-tenant rate limiting at the edge on the verified `customer_slug`
- the `stream()` seam on `DataSourceAdapter` and the split into streaming vs query adapters
- `x-correlation-id` propagation from broker into every adapter call
- the drift-guard rule (INV-11) that keeps the broker capability-neutral
- the gap between the as-built broker and the target router, plus the work items that close it

#### Out of Scope

- semantic routing, surface vocabulary, and conversation-retrieval endpoints — owned by BFF apps (§4.5; A1/BFF spec)
- the CCS context-token contract, scope registry, and `ContextTokenGuard` internals — owned by the Tenant/Auth Spine (D1 spec)
- adapter-internal mechanics of Sierra streaming, Genesys handoff, and benefits HTTP — owned by each adapter contract (§4.6)
- the PII/PHI Redactor and escalation flow — owned by the Escalation spec (E1/E2)
- SLO taxonomy and Grafana panels — owned by the Telemetry spec (F1/F2); the broker only emits canonical log fields

### 4.3 Architecture Position

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    sdk["Customer SDK (@stellarus/chat-client)"]:::client
    apim["Azure APIM (edge / trust boundary)"]:::edge
    ccs["CCS (context token)"]:::ccs
    bff["BFF (agentic-broker-chat) — owns semantic routes"]:::backend
    broker["Thin-Router Broker (agentic-broker-api) — POST /dispatch only"]:::backend
    resolver["@stellarus/resolver"]:::backend
    sierra["SierraAdapter"]:::backend
    benefits["RestBenefitsAdapter"]:::backend
    conv["PostgresConversationAdapter"]:::backend
    db[("Per-tenant Postgres (conversation history)")]:::store

    sdk -->|"Bearer JWT"| apim
    apim -->|"POST /validate/token"| ccs
    apim -->|"x-context-token, x-correlation-id"| bff
    bff -->|"POST /dispatch { capability, payload }"| broker
    broker -->|"resolve(capability, slug)"| resolver
    broker -->|"stream() or query()"| sierra
    broker --> benefits
    broker --> conv
    conv --- db
```

### 4.4 The `POST /dispatch` Contract

| Element | Value |
|---|---|
| Method + path | `POST /dispatch` |
| Body | `{ capability: string, payload: unknown }` |
| Required headers | `x-context-token` (signed JWT, carries `customer_slug`), `x-correlation-id` (UUIDv4 from APIM) |
| Scope gate | `@RequireScopes('chat')` via `ContextTokenGuard` (D1 WI-D1-A) |
| Streaming response | `AsyncIterable<StreamEvent>` (when the resolved adapter implements `stream()`) |
| Query response | `ResolverResponse` (when the resolved adapter implements only `query()`) |
| Contract authority | `apps/agentic-broker-api/contracts/dispatch.contract.ts` (new) |

The request body fields:

| Field | Type | Required | Description |
|---|---|---|---|
| `capability` | `string` | yes | opaque `{domain}.{action}` — resolved via YAML, never branched on by name (INV-02) |
| `payload` | `unknown` | yes | adapter-specific body; the broker forwards it verbatim without inspection |

```mermaid
flowchart TB
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    dispatch["POST /dispatch { capability, payload }"]:::backend
    rl["RateLimiter.check(slug, tokens)"]:::backend
    resolve["Resolver.resolve(capability, slug)"]:::backend
    decide{"adapter shape?"}:::backend
    stream["adapter.stream() — AsyncIterable<StreamEvent>"]:::backend
    query["adapter.query() — ResolverResponse"]:::backend
    yaml[("RESOLVER_CONFIG_DIR (YAML registry, chokidar hot-reload)")]:::store

    dispatch -->|"BROKER-B1B2-SEQ-2"| rl
    rl -->|"BROKER-B1B2-SEQ-3"| resolve
    resolve -->|"BROKER-B1B2-SEQ-4 (streaming)"| decide
    decide -->|"streaming"| stream
    decide -->|"query"| query
    yaml -.->|"feeds class registry"| resolve
```

Per-endpoint failure modes (also centralized in §4.11):

| Status | Condition |
|---|---|
| `401` | missing/invalid `x-context-token`, or RS256 verification fails (INV-06, D1) |
| `403` | verified token lacks the `chat` scope (`@RequireScopes('chat')`, D1 SEQ-7) |
| `404` | no YAML registration for `(capability, customer_slug)` |
| `429` | `RateLimiter.check` rejects the per-tenant token budget (INV-08) |
| `502/503` | resolved adapter's downstream failed; the adapter's circuit breaker governs (INV-09) |

### 4.5 The BFF Surface Rule (load-bearing)

| Scenario | BFF assignment |
|---|---|
| BSC member chat | `agentic-broker-chat` (the v1 BFF) |
| Genesys escalation **from** the chat UI | `agentic-broker-chat` (same surface) -> `{ capability: "escalation.initiate", payload: { conversationId, reason } }` |
| Standalone IVR / phone routing | new BFF: `agentic-broker-ivr` / `agentic-broker-call` |
| Future CSR assist tool | new BFF: `agentic-broker-csr` |
| Customer-embedded widget (non-BSC) | new BFF per customer surface |

### 4.6 Capability Registry and Adapters

| Capability | Adapter class | YAML file | Shape | Status |
|---|---|---|---|---|
| `chat.completion` | `SierraAdapter` | `sierra-bsca.yaml` | streaming (`stream()`) | to-be-built (WI-B1-B), replaces hardcoded `SierraClientService` |
| `benefits.query` | `RestBenefitsAdapter` | `benefits-bsca.yaml` (exists) | query (`query()`) | on `main`; replaces `PlanHandlerService` (WI-B1-D) |
| `conversation.history` | `PostgresConversationAdapter` | `conversation-bsca.yaml` (new) | query (`query()`) | to-be-built (WI-B1-E); replaces in-memory `SessionStore` |
| `escalation.initiate` | `GenesysAdapter` | `genesys-bsca.yaml` | query (`query()`) | P5/E2 scope — NOT in broker MVP (owned by E1/E2) |
| `benefits.query` (Snowflake) | `SnowflakeBenefitsAdapter` | `benefits-bsca-snowflake.yaml` | query (`query()`) | scaffolded stub; demo/future only, REST-only for v1 |

```mermaid
flowchart LR
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000

    cap1["chat.completion"]:::backend
    cap2["benefits.query"]:::backend
    cap3["conversation.history"]:::backend
    cap4["escalation.initiate"]:::backend

    ad1["SierraAdapter"]:::backend
    ad2["RestBenefitsAdapter"]:::backend
    ad3["PostgresConversationAdapter"]:::backend
    ad4["GenesysAdapter"]:::backend

    y1[("sierra-bsca.yaml")]:::store
    y2[("benefits-bsca.yaml")]:::store
    y3[("conversation-bsca.yaml")]:::store
    y4[("genesys-bsca.yaml")]:::store

    cap1 -->|"resolve(slug)"| ad1 --> y1
    cap2 -->|"resolve(slug)"| ad2 --> y2
    cap3 -->|"resolve(slug)"| ad3 --> y3
    cap4 -->|"resolve(slug)"| ad4 --> y4
```

#### The `stream()` seam

`DataSourceAdapter` today exposes only `query()`. WI-B1-A (a blocker) adds an optional `stream(): AsyncIterable<StreamEvent>`, splitting adapters into query-shaped (`DataSourceAdapter`) and streaming-shaped (`StreamingDataSourceAdapter`). This is the seam that lets `SierraAdapter` stream SSE without the broker owning streaming logic. The broker chooses `stream()` vs `query()` on the shape the resolver returns (BROKER-B1B2-SEQ-4) — it does not branch on the capability name.

### 4.7 Dispatch Sequence — `chat.completion`

```mermaid
sequenceDiagram
    participant BFF as BFF (agentic-broker-chat)
    participant BR as Broker (/dispatch)
    participant RL as RateLimiter
    participant RES as Resolver
    participant SA as SierraAdapter
    participant CA as ConversationAdapter

    BFF->>BR: POST /dispatch (chat.completion) [SEQ-1]
    BR->>BR: propagate x-correlation-id [SEQ-7]
    BR->>RL: check(slug, estimated_tokens) [SEQ-2]
    BR->>RES: resolve(chat.completion, slug) [SEQ-3]
    RES-->>BR: SierraAdapter
    BR->>SA: stream(slug, payload) [SEQ-4]
    SA->>CA: persist turn (session_id, role, content, ts, correlation_id) [SEQ-5]
    SA-->>BR: StreamEvents
    BR-->>BFF: AsyncIterable StreamEvent [SEQ-6]
```

### 4.8 Why the Broker Keeps Drifting — and the Second Pipeline to Dismantle

The accreted second pipeline to dismantle, named explicitly:

- `SierraClientService` — provider-specific Sierra client wired directly into the broker
- `RateLimiter` — stays (it is genuinely edge), but moves from inline to guard (WI-B1-H)
- `CircuitBreaker` — per-provider failure state living in the broker
- `TokenCounter` — LLM token counting (tiktoken) in the broker
- `SessionStore` — in-memory NoOp conversation store
- `SSEWriter` — broker-owned SSE serialization
- `PlanHandler` — direct-HTTP benefits path in the broker (`PlanHandlerService`)

### 4.9 B1 Gap Table — As-Built vs Target

| Concern | Current (as-built) | Required (target) | Priority |
|---|---|---|---|
| Endpoint | `POST /v2/chat`, `POST /chat` (semantic) | `POST /dispatch` only (capability-neutral) | Core (WI-B1-F) |
| Sierra | `SierraClientService` hardcoded | `SierraAdapter` via `sierra-bsca.yaml` as `chat.completion` | Core (WI-B1-B) |
| Adapter shape | only `query()` | add `stream(): AsyncIterable<StreamEvent>` | Blocker (WI-B1-A) |
| Benefits | `PlanHandlerService` direct HTTP | `RestBenefitsAdapter` via `benefits-bsca.yaml` (`benefits.query`) | Core (WI-B1-D) |
| Session/conversation | in-memory `SessionStore` (NoOp) | `PostgresConversationAdapter` via `conversation-bsca.yaml` (`conversation.history`) | Core (WI-B1-E) |
| Circuit breaker | `CircuitBreakerService` in broker | moves into `SierraAdapter` (each adapter owns its downstream) | Refactor (WI-B1-C) |
| Token counter | `TokenCounterService` in broker | moves into `SierraAdapter` (Sierra-specific) | Refactor (WI-B1-C) |
| Rate limiter | inline in `ChatHandlerService` | **stays in the broker** as edge middleware; refactor inline -> NestJS guard | Deferred (WI-B1-H) |
| Conversation retrieval | none | `GET /api/conversations/{sessionId}` on the **BFF**, dispatching `conversation.history` | P5 (WI-B1-G) |
| `chat` scope gate | none | `@RequireScopes('chat')` on `/dispatch` (D1 WI-D1-A) | D1 dep |
| `correlation_id` | not threaded through SSE error events | broker propagates `x-correlation-id` to adapters (SEQ-7) | D1 alignment |
| Legacy `/chat` | backward-compat route | deleted after BFF migrates | Deferred (WI-B1-I) |

#### Edge ordering (normative)

`RateLimiter.check` runs **BEFORE** `Resolver.resolve` runs **BEFORE** adapter dispatch:

```text
RateLimiter.check(slug, tokens)            # BROKER-B1B2-SEQ-2
  -> Resolver.resolve(capability, slug)     # BROKER-B1B2-SEQ-3
    -> adapter.stream() | adapter.query()    # BROKER-B1B2-SEQ-4
```

```mermaid
flowchart TB
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    subgraph CUR["Current Broker (drifted)"]
        direction TB
        scs["SierraClientService"]:::backend
        ss["SessionStore (in-memory)"]:::backend
        ph["PlanHandler"]:::backend
        tc["TokenCounter"]:::backend
        cb["CircuitBreaker"]:::backend
        sse["SSEWriter"]:::backend
        rl0["RateLimiter (inline)"]:::backend
        ep["/v2/chat + /chat (named routes)"]:::boundary
    end

    subgraph TGT["Target Thin Router (INV-11 drift guard)"]
        direction TB
        disp["POST /dispatch (only endpoint)"]:::backend
        res["Resolver + YAML registry"]:::backend
        sa["SierraAdapter (owns SSE, tokens, breaker)"]:::backend
        ca["PostgresConversationAdapter"]:::store
        ba["RestBenefitsAdapter"]:::backend
        rl1["RateLimiter (retained at edge)"]:::backend
    end

    scs --> sa
    tc --> sa
    cb --> sa
    sse --> sa
    ss --> ca
    ph --> ba
    rl0 --> rl1
    ep --> disp
```

### 4.10 Hard Invariants (MUST / MUST-NOT)

| ID | Obligation |
|---|---|
| INV-01 | The broker MUST NOT expose any HTTP endpoint other than `POST /dispatch`; all semantic routes live in BFF apps. |
| INV-02 | The broker MUST NOT reference "chat", "conversation", "benefits", or any capability name in routing logic; capabilities are opaque strings resolved via YAML. |
| INV-03 | A new capability MUST be registered by dropping YAML in `RESOLVER_CONFIG_DIR` — never by modifying broker source. |
| INV-04 | The broker MUST NOT import `SierraClientService`, `SierraClientModule`, or any AI-provider-specific code. |
| INV-06 | `PostgresConversationAdapter` MUST be the authoritative conversation-history store; Sierra native session storage MUST NOT be the source of truth. |
| INV-07 | `PostgresConversationAdapter` MUST use per-tenant Postgres schema isolation; it MUST NOT allow cross-tenant conversation reads. |
| INV-08 | `RateLimiter` MUST operate on `customer_slug` from the verified context token; it MUST NOT operate on IP addresses or API keys alone. |
| INV-09 | The broker MUST NOT own the Sierra circuit breaker; `SierraAdapter` owns its own, and every future adapter owns its downstream's. |
| INV-10 | The broker MUST NOT count LLM tokens; token counting is Sierra-specific and lives in `SierraAdapter`. |
| INV-11 | **Drift guard.** Any PR adding a named HTTP endpoint (other than `/dispatch`) to `agentic-broker-api` MUST be rejected at review as an architectural violation of INV-01. |

### 4.11 Failure Handling

#### Dispatch request failures

| Condition | Response |
|---|---|
| Missing/invalid `x-context-token` | `401` |
| RS256 verification fails against CCS JWKS | `401` (INV-06, D1) |
| Verified token lacks `chat` scope | `403` (D1 SEQ-7) |
| No YAML registration for `(capability, customer_slug)` | `404` |
| Per-tenant token budget exhausted | `429` (INV-08) |

#### Adapter / downstream failures

After resolution, the resolved adapter owns its downstream's failure handling. The Sierra circuit breaker lives in `SierraAdapter` (INV-09); the broker does not re-interpret adapter failures, it surfaces them. A tripped breaker presents as `503` from the adapter; the broker propagates the `x-correlation-id` (SEQ-7) so the failure is traceable end to end.

### 4.12 Observability

`{ event, customer_slug, latency_ms, status, capability, correlation_id }`

### 4.13 Work Items

| WI | Description | Priority |
|---|---|---|
| WI-B1-A | add `stream(): AsyncIterable<StreamEvent>` to `DataSourceAdapter` (the streaming seam) | Blocker |
| WI-B1-B | implement `SierraAdapter` wrapping `SierraClientService`; register `sierra-bsca.yaml` | Core |
| WI-B1-C | move `TokenCounterService` + `CircuitBreakerService` into `SierraAdapter` | Core |
| WI-B1-D | implement `RestBenefitsAdapter` replacing `PlanHandlerService`; `benefits-bsca.yaml` | Core |
| WI-B1-E | implement `PostgresConversationAdapter` (per-tenant schema); `conversation-bsca.yaml` | Core (escalation dep) |
| WI-B1-F | replace `POST /v2/chat` with `POST /dispatch`; update BFF to call `/dispatch` | Core |
| WI-B1-G | add `GET /api/conversations/{sessionId}` to the **BFF**, dispatching `conversation.history` | P5 |
| WI-B1-H | refactor `RateLimiterService` inline -> NestJS guard/interceptor (stays at edge) | Deferred |
| WI-B1-I | delete legacy `POST /chat` after BFF migration | Deferred |

### 4.14 Decisions Still Open

**WI-B1-H — RateLimiter placement.**
**Decision for v1: keep `RateLimiterService` inline in the dispatch path.**
**Trigger for revisit:** the edge surface grows (a second cross-cutting edge concern appears, or the limiter needs to be shared across more than the dispatch handler) — at that point refactor it to a NestJS guard/interceptor. It stays *in the broker* either way; only its wiring shape changes.

**WI-B1-I — legacy `/chat` deletion.**
**Decision for v1: leave `POST /chat` in place as a backward-compat route, deferred for deletion.**
**Trigger for revisit:** the BFF (`agentic-broker-chat`) has fully migrated to dispatching through `/dispatch` and no caller hits `/chat`. Until then the route is tolerated debt, explicitly tracked, and exempt from INV-11 only as a named pre-existing exception — no *new* named endpoint qualifies.

### 4.15 New Contracts

| Contract | Location |
|---|---|
| streaming adapter seam | `packages/resolver/src/contracts/streaming-adapter.contract.ts` |
| dispatch endpoint | `apps/agentic-broker-api/contracts/dispatch.contract.ts` |
| Sierra adapter | `apps/agentic-broker-api/adapters/sierra-adapter.contract.ts` |
| conversation adapter | `apps/agentic-broker-api/adapters/conversation-adapter.contract.ts` |

### 4.16 Key Constraints & Rules

- **One endpoint, forever.** The broker exposes `POST /dispatch` and nothing else (INV-01). The drift guard (INV-11) makes a named route a review-blocking architectural violation.
- **Capabilities are opaque.** The broker never branches on a semantic name; YAML resolves `(capability, customer_slug)` to an adapter (INV-02/03).
- **Adapters own their downstreams.** Circuit breaker and token counter live in the adapter, not the broker (INV-09/10).
- **The rate limiter stays at the edge.** Token-budget semantics require tenant context; the limiter operates on the verified `customer_slug`, never IP or API key (INV-08).
- **Postgres is the authoritative conversation record.** Sierra native session storage is never the source of truth (INV-06); per-tenant schema isolation forbids cross-tenant reads (INV-07).
- **The cure for drift is structural, not procedural.** With no semantic endpoints, there is nowhere for business logic to accumulate — that is why the contract, not a code-review reminder, is the enforcement.

## 5. The BFF Layer & Surface Rule

### The Surface Rule

> **Same user surface = same BFF. Different surface = new BFF.**

`agentic-broker-chat` owns:

- all semantic HTTP routes for the chat surface (`/api/chat`, `/api/plan`, `/api/conversations/{sessionId}`)
- translating chat-surface semantics into capability strings (`chat.completion`, `benefits.query`, `conversation.history`, `escalation.initiate`)
- acquiring the CCS context token via `acquireCcsContextToken` (OAuth client-credentials)
- propagating `x-correlation-id` to all downstream calls (D1 SEQ-8, B1B2 SEQ-7)

`agentic-broker-chat` does **not** own:

- capability→adapter resolution (the [Resolver](04-thin-router-broker.md) owns it via YAML)
- rate limiting (stays in the broker as edge middleware — B1B2 INV-08)
- any direct call to Sierra, Benefits Service, Postgres, or Genesys (adapters own those — §4)

### BFF Surface Topology

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000

    chatui["Chat UI (BSC member chat)"]:::client
    ivr["IVR / phone line"]:::client
    csr["CSR assist tool"]:::client
    widget["Customer-embedded widget (non-BSC)"]:::client

    bffchat["agentic-broker-chat (BFF)"]:::backend
    bffivr["agentic-broker-ivr (BFF)"]:::backend
    bffcsr["agentic-broker-csr (BFF)"]:::backend
    bffwidget["widget-BFF (per customer)"]:::backend

    broker["agentic-broker-api — POST /dispatch (capability-neutral)"]:::edge
    adapters["DataSourceAdapters (resolved via YAML)"]:::store

    chatui -->|"/api/chat, /api/plan, /api/conversations"| bffchat
    ivr -->|"surface-specific routes"| bffivr
    csr -->|"surface-specific routes"| bffcsr
    widget -->|"surface-specific routes"| bffwidget

    bffchat -->|"POST /dispatch { capability }"| broker
    bffivr -->|"POST /dispatch { capability }"| broker
    bffcsr -->|"POST /dispatch { capability }"| broker
    bffwidget -->|"POST /dispatch { capability }"| broker

    broker -->|"resolve(capability, customer_slug)"| adapters
```

### 5.1 Surface → BFF Assignment Table

| Scenario | BFF |
|---|---|
| Genesys escalation FROM chat UI | `agentic-broker-chat` (same surface) → `{ capability: "escalation.initiate", payload: { conversationId, reason } }` |
| Standalone IVR / phone routing | New BFF: `agentic-broker-ivr` / `agentic-broker-call` |
| Future CSR assist tool | New BFF: `agentic-broker-csr` |
| Customer-embedded widget (non-BSC) | New BFF per customer surface |

### Surface → BFF Assignment Rule (decision flow)

```mermaid
flowchart LR
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    start(["New behavior to expose"]):::client
    q{"Same user surface as an existing BFF?"}:::boundary
    reuse["Reuse that BFF — add a capability dispatch"]:::backend
    create["Create a new BFF for the surface"]:::backend

    esc["e.g. Genesys escalation FROM chat UI"]:::client
    newsurf["e.g. standalone IVR / CSR / customer widget"]:::client

    start --> q
    q -->|"Yes"| reuse
    q -->|"No"| create
    esc -.->|"same surface"| reuse
    newsurf -.->|"different surface"| create
```

### 5.2 Route Inventory — `agentic-broker-chat`

| Route | Capability dispatched | Status | Purpose |
|---|---|---|---|
| `POST /api/chat` | `chat.completion` | as-built (`main`) | Streaming chat turn; translates the chat-send verb, acquires the context token, dispatches to the broker, streams SSE back (Flow A) |
| `GET /api/plan` | `benefits.query` (via [PVG](#the-plan-validation-gate-pvg)) | as-built (`main`) | Plan Validation Gate: fetches plan data from CCS via the context token, gates users from querying plans they have not attested to |
| `GET /api/conversations/{sessionId}` | `conversation.history` | **to-be-built (MVP, WI-B1-G)** | Conversation retrieval; the escalation context-retrieval entry point (§10) |

#### The Plan Validation Gate (PVG)

The PVG's SDK-facing read path is `fetchPlan`, which returns a three-state
`PlanResult` and **never throws** for 404/503: `PLAN_STATUS_NOT_FOUND` (404) or
`PLAN_STATUS_OUTAGE` (503), per A1 INV-06.

#### `GET /api/conversations/{sessionId}` — conversation retrieval (WI-B1-G)

**Decision for MVP (B-NEW-Z2): conversation retrieval lives in the BFF, not as a
broker endpoint.**

### 5.3 Structural Enforcement — Why The Broker Cannot Hold A Named Route

```text
POST /dispatch
body:    { capability: string, payload: unknown }
headers: x-context-token, x-correlation-id
```

| Mechanism | Enforces | Clause |
|---|---|---|
| `POST /dispatch` is the broker's only endpoint | No named semantic route can be added without a visible new endpoint | B1B2 INV-01 |
| Body is `{ capability, payload }` only | Nowhere to encode an endpoint name in the request | §4 contract |
| Capabilities are opaque strings resolved via YAML | Broker never references chat/conversation/benefits by name | B1B2 INV-02 |
| PR review drift guard | Any new named endpoint on the broker is rejected | B1B2 INV-11 |
| BFF owns all semantic routes for its surface | Semantic logic has a home that is *not* the broker | B1B2 INV-05 |

### 5.4 Request Translation — Semantic To Capability

```mermaid
sequenceDiagram
    participant SDK as StellarusClient (SDK)
    participant BFF as agentic-broker-chat
    participant Broker as agentic-broker-api
    participant Adapter as SierraAdapter

    SDK->>BFF: POST /api/chat (Bearer JWT, x-context-token, body)
    BFF->>BFF: acquireCcsContextToken (OAuth client-credentials)
    BFF->>BFF: translate chat semantics to capability "chat.completion"
    BFF->>Broker: POST /dispatch { capability, payload } (x-context-token, x-correlation-id)
    Broker->>Adapter: resolve(capability, customer_slug) then stream(slug, payload)
    Adapter-->>Broker: AsyncIterable<StreamEvent>
    Broker-->>BFF: stream (SSE)
    BFF-->>SDK: SSE (typed stream events)
```

### 5.5 Failure Handling

| Condition | Response |
|---|---|
| Missing/invalid Bearer JWT at APIM edge | `401` (rejected before reaching BFF) |
| Context token acquisition (`acquireCcsContextToken`) fails | `5xx` — BFF cannot dispatch without a context token |
| `@RequireScopes('chat')` not satisfied on `/dispatch` | `403` (enforced by `ContextTokenGuard`, D1 INV-07) |
| Per-tenant rate limit exceeded | `429` (broker edge middleware, B1B2 INV-08) — SDK surfaces `RateLimitError` |
| Plan not attested / not found (PVG `/api/plan`) | `404` → `fetchPlan` returns `PLAN_STATUS_NOT_FOUND` (never throws, A1 INV-06) |
| Benefits Service outage | `503` → `fetchPlan` returns `PLAN_STATUS_OUTAGE` (A1 INV-06) |
| Conversation not found (`/api/conversations/{sessionId}`) | `404` — escalation handoff aborts before redaction (§10) |
| Adapter/broker stream error | passes through as a typed SSE error event; BFF does not re-interpret business failures |

### 5.6 Key Constraints & Rules

- **One BFF per surface.** Same user surface = same BFF; different surface = new BFF. This is the load-bearing rule (B1B2 INV-05).
- **The BFF owns ALL semantic routes for its surface.** `/api/chat`, `/api/plan`, `/api/conversations/{sessionId}` live in `agentic-broker-chat`, never on the broker (B1B2 INV-01/INV-05).
- **The broker has nowhere to hold a named route.** `POST /dispatch` takes `{ capability, payload }` only; any named semantic endpoint on the broker is a detectable contract violation (B1B2 INV-11).
- **The BFF is the semantic-to-capability translator.** It acquires the CCS context token (`acquireCcsContextToken`, OAuth client-credentials) and maps surface verbs to capability strings.
- **The BFF propagates `x-correlation-id` to all downstream calls.** Unbroken trace chain SDK→BFF→broker→adapter (D1 SEQ-8, B1B2 SEQ-7, F1F2 INV-06).
- **Conversation retrieval lives in the BFF (B-NEW-Z2), not as a broker endpoint.** `GET /api/conversations/{sessionId}` dispatches `conversation.history`; it is the escalation context-retrieval entry point consumed by §10.
- **The Plan Validation Gate lives in the BFF.** `/api/plan` fetches plan data from CCS via the context token and gates un-attested plan queries; the branch-only broker-side `GET /api/plan` is a violation to be removed (WI-B1-F).

## 6. Tenant Context & Auth Spine

### Architecture Position

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef identity fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000

    client["Customer app (SDK / StellarusProvider)"]:::client
    auth0["Auth0 (stellarus-sb2.us.auth0.com)"]:::identity
    apim["Azure APIM (network trust boundary)"]:::edge
    ccs["CCS (Customer Configuration Service)"]:::ccs
    jwks["CCS JWKS (/.well-known/jwks.json, ENG-257)"]:::ccs
    bff["BFF (agentic-broker-chat)"]:::backend
    broker["Thin-Router Broker (POST /dispatch)"]:::backend
    benefits["benefits-service"]:::backend
    db[("CCS PostgreSQL (scope + persona registry)")]:::store

    client -->|"Bearer Auth0 JWT (persona claim)"| apim
    apim -->|"(1) JWKS fetch (cached per iss)"| auth0
    apim -->|"(2) POST /validate/token (persona + customer context)"| ccs
    ccs --- db
    ccs -->|"(3) signed context token (RS256 JWT)"| apim
    apim -->|"(4) x-context-token + x-correlation-id"| bff
    bff -->|"x-context-token + x-correlation-id"| broker
    broker -.->|"ContextTokenGuard verify (RS256 vs JWKS)"| jwks
    benefits -.->|"ContextTokenGuard verify (RS256 vs JWKS)"| jwks
```

CCS owns:

- issuing and RS256-signing context tokens via `TokenService.sign()` (jose)
- the scope registry (14 scopes today + the new `chat` scope) and persona registry
- `POST /validate/token` and (ENG-257) `GET /.well-known/jwks.json`

CCS does **not** own:

- authenticating humans — Auth0 validates credentials and issues access tokens
- the network trust boundary — APIM validates external JWTs and injects trusted headers
- scope **enforcement** at the call site — ContextTokenGuard does that inside each service

APIM owns:

- validating external Auth0 JWTs (JWKS cached per issuer)
- calling CCS `POST /validate/token` and injecting `x-context-token`
- generating one UUIDv4 `x-correlation-id` per request and stripping inbound `x-*` headers

### 6.1 The Context Token

| Claim | Type | Description |
|---|---|---|
| `iss` | `text` | Token issuer — CCS. Validated by ContextTokenGuard (INV-06). |
| `aud` | `text` | Audience — platform-wide `stellarus-context-token` constant for v1 (see ENG-286). MUST be present and non-empty (INV-03). |
| `exp` | `number` | Expiry (epoch seconds). Validated before claims attach (TENANT-D1-SEQ-6). |
| `iat` | `number` | Issued-at (epoch seconds). |
| `sub` | `uuid` | Subject — the resolved principal. |
| `customer_id` | `uuid` | Tenant primary key. |
| `customer_slug` | `text` | Immutable tenant identifier (e.g. `bsca`) — drives ALL tenant scoping downstream. |
| `principal_id` | `text` | Identity of the calling principal within the tenant. |
| `persona` | `text` | Identity class — one of `member`, `employee`, `provider` for human flows. |
| `scopes` | `text[]` | Granted permission strings in `{resource}:{action}` format. |
| `mode` | `text` (optional) | `live` \| `test` — present ONLY in `system`-persona (API-key) tokens (INV-09). |

`correlation_id` is **not** in this list and never will be — `TokenService.sign()` takes
`Omit<ContextTokenClaims, 'correlation_id'>` by design (INV-02). See §6.5.

The signing path is fixed by `TENANT-D1-SEQ-2`: `TokenService.sign()` MUST emit `iss`,
`aud`, `exp`, `iat`, `sub`, `customer_id`, `customer_slug`, `principal_id`, `persona`, and
`scopes` before returning the token to APIM. A token missing `aud` is a malformed token
that the downstream guard rejects (INV-03, the ENG-251 fix, referenced as applied).

### 6.2 Claims, Scope, and Persona Registry (Data Model)

```mermaid
erDiagram
    context_token ||--|| persona : "carries"
    persona ||--o{ persona_scopes : "grants"
    scopes ||--o{ persona_scopes : "granted via"

    context_token {
        uuid sub "subject principal"
        uuid customer_id "tenant FK"
        text customer_slug UK "immutable tenant id (e.g. bsca)"
        text persona "member | employee | provider | system"
        text_array scopes "granted permission strings"
        text mode "live | test (system persona only)"
    }
    scopes {
        text resource "claims | members | providers | customers | benefits | documents | jobs | images | chat"
        text action "read | write | manage | delete | provision | all"
    }
    persona_scopes {
        text persona "member | employee | provider"
        text scope "resource:action"
    }
```

#### context_token

| Column | Type | Constraints |
|---|---|---|
| `sub` | `uuid` | NOT NULL — resolved principal, mirrors `principal_id` context |
| `customer_id` | `uuid` | NOT NULL — tenant FK to CCS customers |
| `customer_slug` | `text` | NOT NULL, UNIQUE per tenant — immutable; drives PostgresConversationAdapter schema, benefits-service partition, RateLimiter budget, analytics cache key. Resolved at the APIM/CCS boundary, never client-supplied. |
| `persona` | `text` | NOT NULL — for human flows validated against `VALID_PERSONAS` (INV-01) |
| `scopes` | `text[]` | NOT NULL — enforced by ContextTokenGuard via `@RequireScopes()` (INV-07) |
| `mode` | `text` | NULLABLE — `live` \| `test`; present only in `system`-persona tokens (INV-09); verifier throws `InvalidContextTokenError` if present but not `live`\|`test` |

#### scopes

| Column | Type | Constraints |
|---|---|---|
| `resource` | `text` | NOT NULL — left side of `{resource}:{action}` |
| `action` | `text` | NOT NULL — right side of `{resource}:{action}` |

`ACT-MAINTAINER` SHALL NOT register a scope that deviates from `{resource}:{action}` format (INV-11). The `chat` scope is the documented exception in shape (`resource=chat`, `action=all`).

#### persona_scopes

| Column | Type | Constraints |
|---|---|---|
| `persona` | `text` | NOT NULL, CHECK `persona IN ('member','employee','provider')` |
| `scope` | `text` | NOT NULL — references a registered scope; default grants per persona |

#### Scope Registry (as-built: 14 scopes, migrations 0000 + 0002)

| Scope | Resource | Action | Default persona grants |
|---|---|---|---|
| `claims:read` | claims | read | member, employee, provider |
| `claims:write` | claims | write | employee |
| `members:read` | members | read | member, employee, provider |
| `providers:manage` | providers | manage | employee, provider |
| `customers:manage` | customers | manage | employee (requires `customer_slug='stellarus'`, INV-10) |
| `benefits:read` | benefits | read | employee |
| `benefits:write` | benefits | write | employee |
| `documents:read` | documents | read | employee, member |
| `documents:write` | documents | write | employee |
| `documents:delete` | documents | delete | employee |
| `jobs:read` | jobs | read | employee |
| `jobs:write` | jobs | write | employee |
| `images:read` | images | read | employee |
| `customers:provision` | customers | provision | none — operator-only (INV-08) |

`customers:provision` is the one scope `ACT-MAINTAINER` SHALL NOT grant to any default
persona — it is operator-only (INV-08). `customers:manage` is granted to `employee` but
gated by tenant: CCS SHALL NOT grant CCS admin access unless `persona === 'employee'`
**and** `customer_slug === 'stellarus'` (INV-10).

#### New scope for MVP (to-be-built): `chat`

| Scope | Resource | Action | Default persona grants |
|---|---|---|---|
| `chat` | chat | all | member TBD, employee TBD, provider —, system per-key |

**Decision for v1: single `chat` scope, no action delineation.** A `chat:send` /
`chat:receive` split adds two registry rows and two guard checks for a boundary the
product does not yet draw.

**This migration is IRREVERSIBLE** (per the Slice taxonomy) — once `0003_chat_scopes.sql`
lands and tokens are minted with `chat`, the grant matrix is in production identity tokens
and cannot be silently rescinded without breaking live callers. The persona grant decision
(member-only vs member+employee) MUST be settled before the migration is written.

### 6.3 Persona Model

| Persona | Source | In `VALID_PERSONAS`? | Notes |
|---|---|---|---|
| `member` | Auth0-federated human | yes | default scopes: `claims:read`, `members:read`, `documents:read` |
| `employee` | Auth0-federated human (Stellarus staff) | yes | broadest grants; `customers:manage` only when `customer_slug='stellarus'` (INV-10) |
| `provider` | Auth0-federated human | yes | scopes: `claims:read`, `members:read`, `providers:manage` |
| `system` | API-key path only (`validate.service.ts`) | **no** | NOT JWT-validated; the ONLY persona that carries `mode` |
| `csr` | (BSC contact-center role) | **DEFERRED** | a BSC CSR is NOT a Stellarus employee — separate persona needed (WI-D1-B) |

### 6.4 Issuance & Verification Path

```mermaid
sequenceDiagram
    participant C as Client (SDK)
    participant APIM
    participant Auth0
    participant CCS
    participant Service as Service (Guard)

    C->>APIM: Bearer Auth0 JWT (persona claim)
    APIM->>APIM: Extract iss from unverified token
    APIM->>Auth0: JWKS fetch for tenant (cached per iss)
    APIM->>APIM: Validate JWT signature, expiry
    APIM->>CCS: POST /validate/token (persona + customer context)
    CCS->>CCS: TokenService.sign() emit iss, aud, exp, iat, sub, customer_id, customer_slug, principal_id, persona, scopes
    CCS-->>APIM: signed context token (RS256 JWT)
    APIM->>APIM: Strip inbound x-*, generate UUIDv4, inject x-context-token + x-correlation-id
    APIM->>Service: x-context-token (signed JWT), x-correlation-id (UUID)
    Service->>Service: ContextTokenGuard verify RS256 vs CCS JWKS
    Service->>Service: Validate iss, aud, exp; attach claims
    Service->>Service: Enforce @RequireScopes('chat') against verified scopes claim
```

#### Scope Enforcement Decision

```mermaid
flowchart LR
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    req["Request with verified context token (persona + scopes[])"]:::backend
    gate{"@RequireScopes('chat'): ALL declared scopes present in verified scopes claim?"}:::edge
    persona["persona default grants (member TBD, employee TBD for chat — WI-D1-A)"]:::boundary
    handler["Dispatch handler (POST /dispatch)"]:::backend
    deny["403 Forbidden (unpermissioned persona)"]:::edge

    req --> gate
    persona -.->|"determines which scopes the token carries"| gate
    gate -->|"Yes — all present"| handler
    gate -->|"No — any missing"| deny
```

Enforcement is all-or-nothing: a request reaches the handler only if **every** scope
declared by `@RequireScopes()` is present in the verified `scopes[]` claim (INV-07). A
partial match is a denial. The scopes a token carries are determined upstream by the
persona's default grants at issuance — which is why the `chat` persona-grant decision
(WI-D1-A) is load-bearing: if `member` is not granted `chat`, member chat is dead on
arrival at the guard regardless of any code change in the broker or BFF.

### 6.5 correlation_id (Definitive)

- **NOT in the JWT.** `TokenService.sign()` takes `Omit<ContextTokenClaims, 'correlation_id'>`
  by design (INV-02). The signed token cannot carry it.
- **APIM-generated.** APIM generates a fresh UUIDv4 per request (INV-04).
- **Inbound stripped.** APIM strips any inbound `x-correlation-id` from external callers
  before injecting its own (TENANT-D1-SEQ-4, INV-04) — forged correlation ids are impossible.
- **Header-only.** It travels as the `x-correlation-id` HTTP header, is propagated
  server-side by the BFF and broker to adapters, and appears in every structured log event.
- **Not a security claim.** Consumers SHALL NOT treat `x-correlation-id` as a security
  claim — it is observability metadata only (INV-05).

The `correlation_id?` field that appears in the broker's `ContextTokenPayload` interface is
vestigial passthrough — it is never populated from the signed token and must not be relied
on as an authenticated value.

### 6.6 mode (Definitive)

- value is `live` | `test`
- present ONLY in `system`-persona tokens (the API-key path); omitted from
  `member`/`employee`/`provider` tokens (INV-09)
- the key-prefix convention is `sk_live_` / `sk_test_`
- the verifier throws `InvalidContextTokenError` if `mode` is present but is not `live`
  or `test`

The invariant is one-directional and absolute: **CCS SHALL NOT embed `mode` in any
human-flow token (INV-09).** A `mode` claim appearing on a `member`/`employee`/`provider`
token is a malformed token, not a feature.

### 6.7 Three-Interface Alignment (WI-D1-E)

```mermaid
flowchart TB
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    ccsLocal["ContextTokenClaims (CCS-local, context-token.interface.ts): customer_id, customer_slug, principal_id, persona, scopes[], +mode?, +correlation_id?"]:::ccs
    internal["InternalContextClaims (packages/auth/src/internal/types.ts): customer_id, customer_slug, principal_id, persona, scopes[], +mode?, iat?/nbf?/exp? — NO correlation_id"]:::backend
    broker["ContextTokenPayload (broker, context-token-payload.ts): +iss/aud/exp/iat/sub, customer_id, customer_slug, principal_id, persona, scopes[], +mode?, +correlation_id?"]:::boundary

    ccsLocal -. "correlation_id divergence" .-> internal
    internal -. "correlation_id divergence" .-> broker
    ccsLocal -->|"WI-D1-E align onto shared InternalContextClaims"| internal
    broker -->|"WI-D1-E align onto shared InternalContextClaims"| internal
```

| Interface | Location | Has `correlation_id`? | Has `iss`/`aud`/`exp`? |
|---|---|---|---|
| `ContextTokenClaims` | `apps/customer-configuration-service` (`context-token.interface.ts`) | yes (optional) | no |
| `InternalContextClaims` | `packages/auth/src/internal/types.ts` | **no** | partial (`iat?`/`nbf?`/`exp?`) |
| `ContextTokenPayload` | `apps/agentic-broker-api` (`context-token-payload.ts`) | yes (optional) | yes |

### 6.8 Auth0 Facts

- **Tenant:** `stellarus-sb2.us.auth0.com`.
- **Flow:** Authorization Code + PKCE (Auth0 PKCE), handled inside the SDK via
  `@auth0/auth0-react`. The removed `apiKey` config was a security hole; `StellarusProvider`
  is now the exclusive PKCE entry point (INV-03 of the SDK slice).
- **Persona custom claim:** `https://stellarus.com/persona` — Auth0 injects the persona
  into the access JWT (SDK-A1-SEQ flow, step 2 of Flow B) before APIM forwards it to CCS
  `/validate/token`.
- **Session lifetime — INVESTIGATION_MARKER SDK-INV-14.** `ACT-STELLARUS` SHALL NOT
  configure the Auth0 tenant session lifetime beyond the healthcare compliance ceiling, and
  SHALL verify the policy before GA. **Do not lock the session lifetime until the
  compliance ceiling is verified** — locking it first risks shipping a non-compliant
  default that is then load-bearing for live members.

### 6.9 Failure Handling

#### Context Token Verification Failures

| Condition | Response |
|---|---|
| Missing `x-context-token` header | `401` |
| RS256 signature does not verify against CCS JWKS | `401` |
| `iss` mismatch | `401` |
| `aud` missing, empty, or mismatched | `401` (INV-03) |
| `exp` in the past | `401` |
| `@RequireScopes()` scope not present in verified `scopes[]` | `403` (INV-07) |
| `mode` present but not `live`\|`test` | `InvalidContextTokenError` (rejected, INV-09) |

#### Token Issuance Failures (CCS `/validate/token`)

| Condition | Response |
|---|---|
| `persona` not in `VALID_PERSONAS` for a human flow | issuance refused (INV-01) |
| `aud` cannot be resolved | issuance refused — no token without `aud` (INV-03) |
| Auth0 JWT invalid at APIM | `401` at edge — CCS never called |

### 6.10 Security Model

#### Trust Boundaries

| Layer | Trust level | Verification |
|---|---|---|
| External clients | Untrusted | Must pass through APIM — no direct service access |
| Auth0 | Identity provider | Authenticates humans; issues access JWT with persona claim |
| APIM | Trust boundary | Validates Auth0 JWT via JWKS; strips inbound `x-*`; injects `x-context-token` + `x-correlation-id` |
| CCS | Authoritative issuer | RS256-signs context tokens; owns scope + persona registry |
| Internal services | Trusted network | ContextTokenGuard verifies context token RS256 vs CCS JWKS |

#### Header Security

APIM is the only component permitted to set `x-context-token` and `x-correlation-id` on
the trusted side. Any inbound `x-*` header from an external caller is stripped before
APIM injects its own (INV-04). Services treat these headers as trusted **only because**
they arrive from inside the APIM boundary and the context token's signature verifies.

#### Scope Enforcement

Scope enforcement is the responsibility of the ContextTokenGuard at the call site, not of
CCS. CCS decides which scopes a persona is granted at issuance; the guard decides whether
the verified token satisfies a route's `@RequireScopes()` declaration (INV-07). The two
must not be conflated — over-granting at issuance is contained at the route only if both
sides are correct.

#### Key Material (JWKS)

Production RS256 verification depends on the **CCS JWKS endpoint** at
`/.well-known/jwks.json` (**ENG-257**, owner Jordan Ramos, draft PR open). Consumers verify
context-token signatures against the published key set, prefer reachable JWKS keys, and
refresh on a rotated `kid`. A static `CONTEXT_TOKEN_PUBLIC_KEY` PEM is permitted only as a
transport-failure fallback today.

**Decision for v1: static-key fallback stays only until ENG-257 lands.** Once ENG-257 is
complete, neither the broker nor benefits-service SHALL fall back to a static
`CONTEXT_TOKEN_PUBLIC_KEY` in production (INV-12a, INV-12b).

### 6.11 Decisions Still Open

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 1 | `chat` persona grants — member-only vs member+employee (WI-D1-A) | Ketema / D1 | IRREVERSIBLE migration `0003_chat_scopes.sql`; wrong grant matrix is in live identity tokens |
| 2 | `csr` persona definition (WI-D1-B) | cross-team (BSC + Stellarus) | a BSC CSR is not a Stellarus employee; reusing `employee` over-grants a third party |
| 3 | CCS JWKS endpoint completion (ENG-257) | Jordan Ramos | blocks production RS256 verification (INV-12a/b); removes static-key fallback |
| 4 | Per-consumer `aud` scoping (ENG-286) | Bharath | today `aud` is one constant for all tokens, cross-service replay risk |
| 5 | Auth0 session lifetime vs healthcare ceiling (SDK-INV-14) | ACT-STELLARUS | must verify compliance ceiling before GA; do not lock lifetime first |

### 6.12 Key Constraints & Rules

- **CCS is the authoritative source of truth for context tokens.** It issues, signs, and
  validates them and owns the scope + persona registry. No other service mints a context token.
- **The context token is RS256-signed and verified against CCS JWKS.** Never accept claims
  from an unverified token (INV-06).
- **`correlation_id` is never in the JWT.** It is an APIM-generated, header-only,
  observability-only value (INV-02, INV-04, INV-05).
- **`mode` appears only in `system`-persona tokens.** Never in a human-flow token (INV-09).
- **`customer_slug` is resolved at the APIM/CCS boundary, never client-supplied.** It drives
  all tenant scoping downstream.
- **Scope strings are `{resource}:{action}`, convention-enforced.** Do not register a scope
  that deviates from the format (INV-11); `chat` (`chat:all`) is the documented exception.
- **`customers:provision` is operator-only.** Never granted to a default persona (INV-08).
- **Extend the 36-clause SEAM contract, never replace it.** `tenant-context.contract.ts`
  plus `InternalContextClaims` is the authority for this slice; the only additive behavior
  for MVP is the `chat` scope, the correlation-id discipline, and the WI-D1-E interface
  alignment.

## 7. The SDK (@stellarus/chat-client)

### Build state — as-built vs to-be-built

| Artifact | State | Notes |
|---|---|---|
| `stellarus-client.ts`, `use-chat.ts`, `react/index.ts` | on branch `feat/stellarus-chat-sdk` only — **NOT merged** | 155/155 tests passing on the branch |
| `stellarus_client_contract.ts` + `use_chat_contract.ts` | **new, authoritative** | the v1 surface lock; the source of truth |
| PR #421 | open, **predates this v1 contract** | MUST be validated against the contract below, not treated as source of truth |
| `apiKey` config field | **removed** (security fix) | replaced by Auth0 PKCE via `StellarusProvider` |

**Decision for v1: the contract files are authoritative; PR #421 is a candidate implementation.**
Any divergence between #421 and the two contract files is a defect in #421, not a contract
amendment.

### 7.1 What the SDK is, and is not

The SDK owns:

- the customer-facing PKCE login + token lifecycle (`StellarusProvider`)
- the streaming chat state machine and per-send abort (`useChat`)
- the APIM call mechanics, SSE-parse delegation, and `sessionId` capture (`StellarusClient`, internal)
- the three-state plan lookup that never throws (`fetchPlan`)
- a small, versioned set of typed error classes

The SDK does **not** own and SHALL NOT expose:

- any internal service name — `broker`, `sierra`, `agentic`, `ccs`, `benefits` — in any public
  type, method, error class, or thrown string (INV-01)
- any internal routing URL — broker URL, BFF URL — in config, error, or docs (INV-09)
- any direct call to CCS from a customer-facing code path (INV-02)
- any raw API key surface; Auth0 PKCE is the only authentication path (INV-03)
- BSC/benefits vocabulary (`planQuery`, `planData`, `planValidationStatus`) in any public type (INV-10)
- the Auth0 `domain`, `audience`, or `useRefreshTokens` toggle as customer-configurable knobs (INV-11, INV-12)

The generic vocabulary that replaces all BSC-specific terms is **`contextQuery` / `contextStatus`
/ `contextData`** (INV-10). The SDK forwards `contextData` to APIM **verbatim, never mutated** (INV-07).

### 7.2 Public Surface & Internal Boundary

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef identity fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    customer["Customer React App"]:::client

    subgraph public["Public Surface — generic vocabulary only"]
        provider["StellarusProvider (clientId, baseUrl?)"]:::client
        hook["useChat() — chat(opts), abort()"]:::client
        plan["fetchPlan(planId, opts?) — PlanResult"]:::client
        errs["Error classes: ChatAuthError, RateLimitError, ChatNetworkError, ChatAbortError, StellarusConfigError"]:::client
        vocab["contextQuery / contextStatus / contextData"]:::client
    end

    bnd["BOUNDARY — INV-01 no internal service names / INV-09 no internal URLs / INV-10 no BSC vocabulary cross here"]:::boundary

    subgraph internal["Internal Mechanics — never imported by customer"]
        sclient["StellarusClient — chat(), fetchPlan(), endConversation()"]:::backend
        sse["createSSEStreamReader (DRY, INV-08)"]:::backend
        apim["APIM /chat, /plan (Bearer JWT)"]:::edge
    end

    auth0["Auth0Provider (@auth0/auth0-react) — PKCE, silent refresh"]:::identity

    customer --> provider
    provider -->|"wraps, owns token lifecycle (useRefreshTokens:true hardcoded)"| auth0
    customer --> hook
    customer --> plan
    hook --> bnd
    plan --> bnd
    bnd --> sclient
    sclient -->|"getAccessTokenSilently()"| auth0
    sclient --> sse
    sclient -->|"Authorization: Bearer jwt"| apim
```

### 7.3 Config shape

```text
StellarusProvider config:
{
  clientId: string,        // REQUIRED — the customer's Auth0 application client id
  baseUrl?: string,        // OPTIONAL — APIM base; defaults to the Stellarus platform edge
  onRedirectCallback?: (appState?) => void   // OPTIONAL escape hatch for post-login routing
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `clientId` | `string` | yes | the customer's Auth0 application client id — the *only* credential-adjacent value the customer supplies |
| `baseUrl` | `string` | no | APIM edge base URL; never a broker or BFF URL (INV-09) |
| `onRedirectCallback` | `function` | no | escape hatch invoked after PKCE code exchange so the customer app controls post-login navigation |

What is **not** in the config is the contract:

- no `apiKey` — removed; it was a security hole (INV-03)
- no Auth0 `domain` / `audience` — internal Stellarus constants, maintained by the platform team (INV-12)
- no `useRefreshTokens` — hardcoded `true` inside `StellarusProvider`, never customer-configurable (INV-11)
- no broker URL, BFF URL, or any internal routing URL (INV-09)

### 7.4 Auth-model change — apiKey removed, Auth0 PKCE only

**Decision for v1: PKCE-in-the-SDK, zero customer credential handling.** The customer's only
secret-shaped input is a public Auth0 client id, which is not a secret. **Trigger for revisit:**
SDK-INV-14 (below) — Auth0 tenant session lifetime must be verified against the healthcare
compliance ceiling before GA.

### 7.5 Public methods

| Symbol | Kind | Signature | Behavior |
|---|---|---|---|
| `StellarusProvider` | React component | `({ clientId, baseUrl?, onRedirectCallback? })` | wraps `Auth0Provider`; owns token lifecycle; PKCE entry point (SDK-A1-SEQ-1, SEQ-6) |
| `useChat` | React hook | `() => { chat, abort, status, ... }` | streaming state machine + per-send `AbortController`; aborts on unmount (SDK-A1-SEQ-7); throws if no provider mounted |
| `useChat.chat` | method | `chat(opts) => AsyncIterable<StreamEvent>` | acquires Bearer JWT via `getAccessTokenSilently()` before any fetch (SDK-A1-SEQ-2) |
| `useChat.abort` | method | `abort() => void` | aborts the in-flight SSE stream for the current send |
| `getAccessTokenSilently` | re-export | `() => Promise<string>` | Auth0 silent token acquisition (IP-1) |
| `StellarusClient.fetchPlan` | method (internal class) | `fetchPlan(planId, opts?) => Promise<PlanResult>` | three-state result; never throws for 404/503 (INV-06) |
| `StellarusClient.endConversation` | method (internal class) | `endConversation() => void` | ends the current conversation; clears captured `sessionId` |

#### `fetchPlan(planId, opts?)` — the three-state, no-throw contract

`fetchPlan` calls APIM `/plan` with the Bearer JWT and a `planId` query param (IP-7), and returns a
`PlanResult` that **never throws** for the two expected non-200 outcomes (INV-06, SDK-PLAN-PRE-1):

| Upstream status | `PlanResult` state | Meaning |
|---|---|---|
| `200` | data state — `contextData` payload | plan found |
| `404` | `PLAN_STATUS_NOT_FOUND` | plan does not exist for this member; not an error |
| `503` | `PLAN_STATUS_OUTAGE` | benefits path temporarily unavailable; retry later |

### 7.6 useChat streaming lifecycle

```mermaid
sequenceDiagram
    participant H as useChat
    participant SC as StellarusClient
    participant A0 as Auth0
    participant AP as APIM

    H->>SC: chat(opts)
    SC->>A0: getAccessTokenSilently()
    A0-->>SC: Bearer JWT
    SC->>AP: POST /chat (Authorization Bearer, body message + optional sessionId/contextQuery/contextStatus/contextData)
    AP-->>SC: 200 SSE stream
    SC->>SC: createSSEStreamReader.parse() (INV-08)
    SC->>SC: capture sessionId from session SSE event, store to private field (INV-05)
    Note over SC: turns greater than 1 thread the non-null sessionId
    SC->>AP: POST /chat (thread sessionId in body)
    AP-->>SC: 200 SSE stream
    H->>H: on unmount abortController.abort()
```

### 7.7 Error classes

| Class | When | Carries |
|---|---|---|
| `ChatAuthError` | APIM rejects the Bearer JWT (`401`), or token acquisition fails | no token, no credential (INV-04a/b) |
| `RateLimitError` | per-tenant rate limit exceeded (`429`) | `retryAfter` (seconds) |
| `ChatNetworkError` | transport failure reaching APIM, or non-handled `5xx` | no internal URL (INV-09) |
| `ChatAbortError` | the send was aborted via `abort()` or unmount | — (suppressed at the hook level, see SDK-UXV-1) |
| `StellarusConfigError` | invalid/missing config (e.g. no `clientId`, provider not mounted) | no credential |

### 7.8 useChat status state machine

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> streaming: chat()
    streaming --> done: stream complete
    streaming --> error: ChatAuthError / ChatNetworkError / RateLimitError
    streaming --> aborted: abort() or unmount (ChatAbortError suppressed)
    done --> streaming: chat() next turn
    error --> streaming: chat() retry
    aborted --> streaming: chat() new send
    done --> [*]
```

### 7.9 Integration points

| # | Source -> Target | Handoff | Clause |
|---|---|---|---|
| IP-1 | `useChat` -> `getAccessTokenSilently()` | Auth0 Bearer JWT string | SDK-CHAT-PRE-1 |
| IP-2 | `StellarusClient.chat()` -> APIM `/chat` | `Authorization: Bearer <jwt>`, body `message` + optional `sessionId`/`contextQuery`/`contextStatus`/`contextData` | SDK-CHAT-PRE-1, SDK-CHAT-SEQ-1 |
| IP-3 | APIM -> CCS (internal) | shared secret -> context token | internal; customer never touches (INV-02) |
| IP-4 | APIM -> broker (internal) | context token in forwarded headers | internal; customer never touches |
| IP-5 | broker SSE -> APIM -> `StellarusClient` -> `createSSEStreamReader` | raw SSE text stream | SDK-CHAT-POST-1 |
| IP-6 | `StellarusClient` -> `useChat` | `AsyncIterable<StellarusStreamEvent>` | SDK-CHAT-POST-1 -> POST-4 |
| IP-7 | `StellarusClient.fetchPlan()` -> APIM `/plan` | `Authorization: Bearer <jwt>`, `planId` query param | SDK-PLAN-PRE-1 |

### 7.10 Failure Handling

#### Chat request failures
| Condition | Surfaced as |
|---|---|
| Bearer JWT rejected / token acquisition failed | `ChatAuthError` |
| Rate limit exceeded (`429`) | `RateLimitError` with `retryAfter` |
| Transport failure / unhandled `5xx` | `ChatNetworkError` |
| Send aborted (`abort()` or unmount) | `ChatAbortError` — suppressed at hook level, `status = aborted` |
| Missing/invalid config (no `clientId`, no provider) | `StellarusConfigError` |

#### Plan lookup outcomes (do NOT throw)
| Upstream status | Returned `PlanResult` |
|---|---|
| `404` | `PLAN_STATUS_NOT_FOUND` |
| `503` | `PLAN_STATUS_OUTAGE` |

### 7.11 Observability — what the SDK must NOT record

The SDK SHALL NOT record, in any error, `console` output, or thrown string:

- the Auth0 access token or refresh token (INV-04a/b)
- any raw API key (there is none in v1, but the prohibition stands — INV-03)
- the signed context token (the SDK never sees it; it is injected at APIM)
- internal service names or routing URLs (INV-01, INV-09)

### 7.12 Key Constraints & Rules

- **No internal service names anywhere public.** `broker`, `sierra`, `agentic`, `ccs`, `benefits`
  appear in no public type, method, error class, or string (INV-01).
- **No direct CCS call.** No customer-facing code path calls CCS; the SDK reaches CCS only
  transitively through APIM (INV-02).
- **No raw API key — Auth0 PKCE only.** `apiKey` config is removed; the customer authenticates
  exclusively through Auth0 PKCE via `StellarusProvider` (INV-03).
- **No credentials in errors/logs/throws.** Neither `StellarusClient` (INV-04a) nor `useChat`
  (INV-04b) emits a token or credential.
- **No client-side conversationId.** `sessionId` is captured ONLY from a `session` SSE event; the
  SDK never generates one (INV-05).
- **fetchPlan never throws for 404/503.** It returns `PLAN_STATUS_NOT_FOUND` / `PLAN_STATUS_OUTAGE`
  (INV-06).
- **contextData forwarded verbatim.** `StellarusClient` never mutates `contextData` before
  forwarding to APIM (INV-07).
- **All SSE parsing delegated.** Parsing goes through `createSSEStreamReader`, never re-implemented
  (INV-08, DRY).
- **No internal routing URLs exposed.** No broker/BFF/internal URL in config, error, or docs (INV-09).
- **No BSC/benefits vocabulary public.** `planQuery`/`planData`/`planValidationStatus` never appear
  in public types; the generic `contextQuery`/`contextStatus`/`contextData` are used instead (INV-10).
- **useRefreshTokens not customer-configurable.** Hardcoded `true` in `StellarusProvider` (INV-11).
- **Auth0 domain/audience are internal constants.** Not customer-configurable; maintained by the
  platform team (INV-12).
- **No public export removed/renamed/re-signed without a MAJOR bump.** The surface is frozen at v1
  semver granularity (INV-13).

### 7.13 Decisions Still Open

| # | Marker | Decision for v1 | Trigger to revisit |
|---|---|---|---|
| 1 | **SDK-INV-14** — Auth0 tenant session lifetime vs healthcare compliance ceiling | do NOT lock the session lifetime in the contract until the policy is verified; treat it as platform-owned config | **verify the tenant session-lifetime policy against the healthcare compliance ceiling before GA** — `ACT-STELLARUS` SHALL NOT configure a lifetime beyond the ceiling (INV-14) |
| 2 | **SDK-UXV-1** — stream abort/unmount UX | suppress `ChatAbortError` at the hook level; surface `status = aborted` rather than an error state | **real-world UX validation required before ship** — confirm with human testing that suppressing the abort error is the right member experience; do not ship on assumption alone |

## 8. Data Source Adapters

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    bff["BFF (agentic-broker-chat)"]:::client
    broker["Thin-Router Broker (POST /dispatch)"]:::edge
    resolver["Resolver (@stellarus/resolver)"]:::ccs

    subgraph adapters["DataSourceAdapter layer (owns provider concerns)"]
        direction LR
        sierra["SierraAdapter (stream)"]:::backend
        rest["RestBenefitsAdapter (query)"]:::backend
        conv["PostgresConversationAdapter (query)"]:::backend
        genesys["GenesysAdapter (query)"]:::backend
    end

    sierraDown["Sierra.ai (SSE)"]:::boundary
    benefitsDown["Benefits Service"]:::boundary
    pg[("Per-tenant Postgres")]:::store
    genesysDown["Genesys Cloud CCaaS"]:::boundary

    bff -->|"{ capability, payload } + x-context-token + x-correlation-id"| broker
    broker -->|"resolve(capability, customer_slug)"| resolver
    resolver -->|"adapter instance"| broker
    broker -->|"stream() or query()"| adapters
    sierra -->|"SSE open + token count + circuit breaker"| sierraDown
    sierra -->|"persist turn"| conv
    rest -->|"HTTP benefits.query"| benefitsDown
    conv --- pg
    genesys -->|"escalation handoff + circuit breaker"| genesysDown
```

The interface as built today exposes a single method, `query()`. The MVP work adds the optional `stream(): AsyncIterable<StreamEvent>` method (**WI-B1-A**, 🔴 blocker), which splits the type into two shapes:

- **`DataSourceAdapter`** — exposes `query(slug, payload)`, returns a single `ResolverResponse`. The query-shaped adapter.
- **`StreamingDataSourceAdapter`** — extends `DataSourceAdapter` and adds `stream(slug, payload): AsyncIterable<StreamEvent>`. The streaming-shaped adapter.

The broker selects the method from the resolved adapter's shape: streaming capabilities call `stream()`, query capabilities call `query()` (BROKER-B1B2-SEQ-4). The seam exists so that `SierraAdapter` can stream Sierra's SSE response without the broker owning any streaming logic — the broker just pipes the `AsyncIterable<StreamEvent>` back to the BFF (IP-6).

```mermaid
classDiagram
    class DataSourceAdapter {
        <<interface>>
        +query(slug, payload) ResolverResponse
    }
    class StreamingDataSourceAdapter {
        <<interface>>
        +stream(slug, payload) AsyncIterable~StreamEvent~
    }
    class SierraAdapter {
        +stream(slug, payload) AsyncIterable~StreamEvent~
        -tokenCounter
        -circuitBreaker_OWNS
        -parseSSE()
        -persistTurn()
    }
    class RestBenefitsAdapter {
        +query(slug, payload) ResolverResponse
    }
    class PostgresConversationAdapter {
        +query(slug, payload) ResolverResponse
        +getAll(conversationId)
        +persist(turn)
    }
    class GenesysAdapter {
        +query(slug, payload) ResolverResponse
        -circuitBreaker_OWNS_startsCLOSED
    }
    class SnowflakeBenefitsAdapter {
        +query(slug, payload) ResolverResponse
    }

    DataSourceAdapter <|-- StreamingDataSourceAdapter : extends
    StreamingDataSourceAdapter <|.. SierraAdapter : implements
    DataSourceAdapter <|.. RestBenefitsAdapter : implements
    DataSourceAdapter <|.. PostgresConversationAdapter : implements
    DataSourceAdapter <|.. GenesysAdapter : implements
    DataSourceAdapter <|.. SnowflakeBenefitsAdapter : implements
```

- **Circuit breaker** moves OUT of the broker and INTO the adapter that owns the downstream (INV-09). Sierra's circuit breaker lives in `SierraAdapter`; Genesys's lives in `GenesysAdapter`. A future adapter brings its own.
- **Token counter** (tiktoken / LLM token counting) is Sierra-specific and lives in `SierraAdapter`, never in the broker (INV-10). It feeds the cost-per-answer SLO via the `token_cost` log field (§11).
- **SSE parsing** for the Sierra stream lives in `SierraAdapter`. The broker pipes the resulting `AsyncIterable<StreamEvent>` without interpreting it.
- **Secret retrieval** is per-adapter. `GenesysAdapter` resolves credentials from Azure Key Vault via Managed Identity, never env vars (INV-07).

### The Four MVP Adapters

| Capability | Adapter | Shape | YAML file | Status | Owns |
|---|---|---|---|---|---|
| `chat.completion` | `SierraAdapter` | `stream()` | `sierra-bsca.yaml` | to-be-built (WI-B1-B/C) | token counter, Sierra circuit breaker, SSE parsing |
| `benefits.query` | `RestBenefitsAdapter` | `query()` | `benefits-bsca.yaml` (exists) | on `main` (WI-B1-D) | HTTP call to Benefits Service |
| `conversation.history` | `PostgresConversationAdapter` | `query()` | `conversation-bsca.yaml` (new) | to-be-built (WI-B1-E) | per-tenant Postgres schema, authoritative store |
| `escalation.initiate` | `GenesysAdapter` | `query()` | `genesys-bsca.yaml` | to-be-built (P5/E2, §10) | Genesys circuit breaker, Key Vault creds |
| `benefits.query` (Snowflake) | `SnowflakeBenefitsAdapter` | `query()` | `benefits-bsca-snowflake.yaml` | stub — scaffolded, not live | nothing live (demo/future) |

**Owns:** Sierra circuit breaker (INV-09), token counter (INV-10), SSE parsing, per-turn conversation persist (BROKER-B1B2-SEQ-5).

It is **implemented on `main`** today: this is the one MVP adapter that is as-built, not to-be-built. The `query()` path makes an HTTP call to the Benefits Service, which retrieves plan data from its customer-partitioned Postgres. The SDK-facing `fetchPlan` variant maps `404` → `PLAN_STATUS_NOT_FOUND` and `503` → `PLAN_STATUS_OUTAGE` rather than throwing (SDK INV-06); the broker-side `query()` returns the `ResolverResponse` unchanged (Flow C, BROKER-B1B2-SEQ-4).

- **Per-tenant Postgres schema isolation** — same pattern as `benefits-service`; cross-tenant conversation reads are forbidden (INV-07). Scoping is driven by `customer_slug` from the verified context token, never client-supplied.
- **Authoritative store** — Sierra native session storage is NOT the source of truth (INV-06). The Postgres record is.
- **Compressed and indexed**, **durable across broker restarts** — the in-memory store lost history on restart and broke escalation handoff; the Postgres store does not.
- **The escalation prerequisite** — §10 escalation sources its full conversation context exclusively from this adapter (Flow D, SEQ-2; E1E2 INV-09). Without it, the redactor receives nothing to scrub.

Its circuit breaker starts **CLOSED**; credentials come from Azure Key Vault via Managed Identity, never env vars (INV-07). It is the ONLY component permitted to call the Genesys API (INV-05). E1 integration mechanics (API shape, routing metadata fields, SLA) are BLOCKED on BSC/PTP — see §10.

**Decision for v1: REST-only for benefits.** `RestBenefitsAdapter` is the live `benefits.query` path; `SnowflakeBenefitsAdapter` stays a stub.

```mermaid
sequenceDiagram
    participant B as Broker
    participant SA as SierraAdapter
    participant S as Sierra
    participant CA as PostgresConversationAdapter

    B->>SA: stream(slug, payload)
    SA->>SA: circuit breaker check (Sierra)
    SA->>S: open SSE stream
    loop per Sierra chunk
        S-->>SA: chunk (SSE)
        SA->>SA: parse SSE + count tokens
        SA->>CA: persist turn (session_id, role, content, timestamp, correlation_id)
        CA-->>SA: ack
        SA-->>B: StreamEvent
    end
    S-->>SA: stream end
    SA-->>B: stream complete
```

The persisted turn carries exactly: `session_id`, `role`, `content` (text), `timestamp`, `correlation_id`.

```mermaid
flowchart TB
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    subgraph cfg["RESOLVER_CONFIG_DIR"]
        y1["sierra-bsca.yaml"]:::store
        y2["benefits-bsca.yaml"]:::store
        y3["conversation-bsca.yaml"]:::store
        y4["genesys-bsca.yaml"]:::store
    end

    loader["config-loader (chokidar watch)"]:::ccs
    registry["ADAPTER_CLASS_REGISTRY (class name to impl)"]:::ccs

    subgraph inst["instantiated adapters bound to (capability, customer_slug)"]
        a1["SierraAdapter to (chat.completion, bsca)"]:::backend
        a2["RestBenefitsAdapter to (benefits.query, bsca)"]:::backend
        a3["PostgresConversationAdapter to (conversation.history, bsca)"]:::backend
        a4["GenesysAdapter to (escalation.initiate, bsca)"]:::backend
    end

    nocode["zero broker code change (INV-03)"]:::boundary

    cfg -->|"file add/change event"| loader
    loader -->|"resolve class name"| registry
    registry -->|"instantiate"| inst
    nocode -.->|"adding a YAML is the ONLY step"| cfg
```

### As-Built Today vs To-Be-Built for MVP

| Item | As-built today | To-be-built for MVP | Work item |
|---|---|---|---|
| Adapter interface | `query()` only | add optional `stream(): AsyncIterable<StreamEvent>` | WI-B1-A 🔴 |
| Sierra access | `SierraClientService` hardcoded in broker | `SierraAdapter` via `sierra-bsca.yaml` | WI-B1-B 🔴 |
| Token counter + circuit breaker | `TokenCounterService` + `CircuitBreakerService` in broker | moved INTO `SierraAdapter` | WI-B1-C 🔴 |
| Benefits access | `RestBenefitsAdapter` (replaces `PlanHandlerService`) | already on `main` | WI-B1-D ✅ |
| Conversation store | in-memory `SessionStore` NoOp | `PostgresConversationAdapter`, per-tenant, `conversation-bsca.yaml` | WI-B1-E 🔴 |
| Escalation adapter | none | `GenesysAdapter`, `genesys-bsca.yaml` (P5/E2) | §10 / WI-E2-C 🔴 |
| Snowflake benefits | scaffolded stub | stays stub until demo path needed | — |
| Resolver | implemented, merged to `main` | — | ✅ |

### Failure Handling

| Condition | Response |
|---|---|
| Resolver finds no adapter for `(capability, customer_slug)` | broker returns `404` capability-not-found (no adapter dispatch) |
| Sierra circuit breaker OPEN | `SierraAdapter` short-circuits without calling Sierra; emits `circuit_breaker_open` log (§11); broker surfaces error StreamEvent |
| `PostgresConversationAdapter` persist fails mid-stream | persist failure is logged with `correlation_id`; stream continues (history gap is observable, not silent) |
| `RestBenefitsAdapter` Benefits Service `404`/`503` | `query()` returns the `ResolverResponse`; SDK `fetchPlan` maps to `PLAN_STATUS_NOT_FOUND` / `PLAN_STATUS_OUTAGE`, never throws (SDK INV-06) |
| `GenesysAdapter` circuit breaker OPEN / Genesys unreachable | handoff result `unavailable`; SDK surfaces `escalation_unavailable` (§10, E2-Z2) |
| Malformed / unknown adapter class name in YAML | config-loader rejects the file; existing bindings unchanged (hot-reload is additive-safe) |

### New Contracts

| Contract file | Defines | Shared with |
|---|---|---|
| `packages/resolver/src/contracts/streaming-adapter.contract.ts` | `stream(): AsyncIterable<StreamEvent>` seam, `StreamEvent` shape | §6, §7 |
| `apps/agentic-broker-api/adapters/sierra-adapter.contract.ts` | `SierraAdapter` stream + persist + token-count + circuit-breaker obligations | §6 |
| `apps/agentic-broker-api/adapters/conversation-adapter.contract.ts` | `PostgresConversationAdapter` per-tenant isolation, authoritative-store, `getAll()` | §6, §10 |
| `apps/agentic-broker-api/adapters/genesys-adapter.contract.ts` | `GenesysAdapter` handoff, Key Vault creds, circuit breaker | §10 |

### Key Constraints & Rules

- **The broker never names a downstream.** Every provider is reached through one adapter; the broker calls only `query()` or `stream()` on an opaque resolved object (INV-02, INV-04).
- **Each adapter owns its downstream's concerns.** Circuit breaker (INV-09), token counting (INV-10), SSE parsing, and secret retrieval (INV-07) live in the adapter, never the broker.
- **Postgres is the authoritative conversation record.** Sierra native session storage is NOT the source of truth (INV-06); `PostgresConversationAdapter` is, with per-tenant schema isolation (INV-07).
- **`SierraAdapter` persists every turn.** `session_id, role, content, timestamp, correlation_id` after each Sierra chunk (BROKER-B1B2-SEQ-5) — the escalation handoff depends on it.
- **Registration is YAML-only.** Adding or reconfiguring an adapter is dropping a YAML file in `RESOLVER_CONFIG_DIR`; the resolver hot-reloads via chokidar against `ADAPTER_CLASS_REGISTRY` (INV-03). No broker code change, ever.
- **`GenesysAdapter` is the only Genesys caller.** INV-05; credentials from Azure Key Vault via Managed Identity only (INV-07).

### Decisions Still Open

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 1 | Genesys API shape (REST / SDK / Widget) for `GenesysAdapter` | Julie Hughes + BSC/PTP | Blocks `GenesysAdapter` implementation (E1-Z1) |
| 2 | Routing-metadata fields in `escalation.initiate` payload | Julie Hughes + BSC | Blocks adapter payload contract (E1-Z2) |
| 3 | Conversation compression/index scheme for `PostgresConversationAdapter` | Ketema (platform) | Storage cost + retrieval latency under multi-turn load |
| 4 | When the Snowflake `benefits.query` demo path activates | Platform + demo stakeholders | Trigger to fill the `SnowflakeBenefitsAdapter` stub |

The single biggest blocking decision is **#1 (Genesys API shape)** — it gates the entire escalation adapter and, transitively, the escalation-success SLO in §11.

## 9. End-to-End Data Flows

### 9.1 Flow participants

The five flows share one participant vocabulary. Names match the canonical
glossary exactly.

| Alias | Component | Glossary role |
|---|---|---|
| `Customer` | Customer app (`StellarusProvider`-wrapped) | host application embedding the SDK |
| `Member` | BSC member (end user) | human initiating escalation handoff |
| `useChat` | `useChat` hook | streaming state machine, abort-on-unmount |
| `Client` | `StellarusClient` | APIM calls, SSE-parse delegation, sessionId capture |
| `Provider` | `StellarusProvider` | PKCE entry point, token-lifecycle owner |
| `Auth0` | Auth0 (`stellarus-sb2.us.auth0.com`) | human authentication, persona claim |
| `APIM` | Azure APIM | edge trust boundary, header injection/strip |
| `CCS` | Customer Configuration Service | context-token issuer/signer |
| `Guard` | `ContextTokenGuard` | RS256 verify, scope enforcement |
| `BFF` | `agentic-broker-chat` | semantic routes, capability translation |
| `Broker` | `agentic-broker-api` | capability-neutral `POST /dispatch` router |
| `RateLimiter` | `RateLimiterService` | per-tenant token-bucket edge middleware |
| `Resolver` | `@stellarus/resolver` | `(capability, customer_slug)` → adapter |
| `SierraAdapter` | `SierraAdapter` | streaming adapter for Sierra AI |
| `Sierra` | Sierra.ai | external conversational AI runtime |
| `ConvStore` | `PostgresConversationAdapter` | authoritative per-tenant conversation store |
| `BenefitsAdapter` | `RestBenefitsAdapter` | HTTP adapter for Benefits Service |
| `Benefits` | Benefits Service | governed plan/benefits source of truth |
| `Redactor` | PII/PHI Redactor (`packages/redactor`) | mandatory fail-closed scrub gate |
| `GenesysAdapter` | `GenesysAdapter` | sole caller of Genesys Cloud |
| `Genesys` | Genesys Cloud CCaaS | external contact-center handoff target |
| `Loki` | Grafana Loki | log aggregation, LogQL metric derivation |
| `Grafana` | Grafana | threshold-colored SLO panels |
| `QA` | QA reviewer | weekly answer-quality sampling |
| `Jason` | Jason Jackson (P6 Lead) | F2 taxonomy approval, F1 gate sign-off |

### 9.2 Flow A — Customer Chat Request

```mermaid
sequenceDiagram
    participant Customer
    participant useChat
    participant Client as StellarusClient
    participant Auth0
    participant APIM
    participant BFF
    participant Broker
    participant RateLimiter
    participant Resolver
    participant SierraAdapter
    participant Sierra
    participant ConvStore as PostgresConversationAdapter

    Customer->>useChat: chat(message)
    useChat->>Auth0: getAccessTokenSilently() [SDK-A1-SEQ-2]
    Auth0-->>useChat: Bearer JWT
    useChat->>Client: chat({ message, sessionId? })
    Client->>APIM: POST /chat (Bearer, contextData verbatim) [SDK-A1-SEQ-1, INV-07]
    APIM->>APIM: validate JWT, resolve tenant, inject x-context-token + x-correlation-id
    APIM->>BFF: route /api/chat (x-context-token, x-correlation-id)
    BFF->>Broker: POST /dispatch { capability: chat.completion } [BROKER-B1B2-SEQ-1]
    Broker->>RateLimiter: check(customer_slug, estimated_tokens) [BROKER-B1B2-SEQ-2]
    RateLimiter-->>Broker: within budget
    Broker->>Resolver: resolve(chat.completion, customer_slug) [BROKER-B1B2-SEQ-3]
    Resolver-->>Broker: SierraAdapter
    Broker->>SierraAdapter: stream(slug, payload) + x-correlation-id [BROKER-B1B2-SEQ-4, BROKER-B1B2-SEQ-7]
    SierraAdapter->>Sierra: open SSE stream
    Sierra-->>SierraAdapter: StreamEvent chunks
    SierraAdapter->>ConvStore: persist turn (session_id, role, content, ts, correlation_id) [BROKER-B1B2-SEQ-5]
    SierraAdapter-->>Broker: AsyncIterable&lt;StreamEvent&gt;
    Broker-->>BFF: piped stream [BROKER-B1B2-SEQ-6]
    BFF-->>Client: SSE (200)
    Client->>Client: createSSEStreamReader().parse() [SDK-A1-SEQ-3]
    Client->>Client: capture sessionId from session event [SDK-A1-SEQ-4]
    Client-->>useChat: AsyncIterable&lt;StellarusStreamEvent&gt;
    Client->>APIM: thread non-null sessionId on turns > 1 [SDK-A1-SEQ-5]
    useChat->>useChat: abortController.abort() on unmount [SDK-A1-SEQ-7]
```

### 9.3 Flow B — Auth & Tenant Resolution

```mermaid
sequenceDiagram
    participant Provider as StellarusProvider
    participant Auth0
    participant useChat
    participant APIM
    participant CCS
    participant Guard as ContextTokenGuard
    participant BFF

    Provider->>Provider: check URL for ?code= at mount [SDK-A1-SEQ-6]
    Provider->>Auth0: exchange auth code (PKCE)
    Auth0-->>Provider: access token + persona claim (https://stellarus.com/persona)
    useChat->>Auth0: getAccessTokenSilently() [SDK-A1-SEQ-2]
    Auth0-->>useChat: Bearer JWT
    useChat->>APIM: POST /chat (Bearer)
    APIM->>APIM: validate Auth0 JWT (JWKS cached per iss)
    APIM->>CCS: POST /validate/token (persona + customer + target_audience ENG-286) [TENANT-D1-SEQ-1]
    CCS->>CCS: TokenService.sign() emit iss/aud/exp/iat/sub/customer_id/customer_slug/principal_id/persona/scopes [TENANT-D1-SEQ-2]
    CCS-->>APIM: signed context token (RS256)
    APIM->>APIM: generate UUIDv4 x-correlation-id [TENANT-D1-SEQ-3]
    APIM->>APIM: strip inbound x-correlation-id from external caller [TENANT-D1-SEQ-4]
    APIM->>Guard: forward x-context-token + x-correlation-id
    Guard->>Guard: verify RS256 signature vs CCS JWKS [TENANT-D1-SEQ-5]
    Guard->>Guard: validate iss / aud / exp [TENANT-D1-SEQ-6]
    Guard->>Guard: enforce @RequireScopes('chat') against verified scopes [TENANT-D1-SEQ-7]
    Guard-->>BFF: attach verified ContextTokenPayload
    BFF->>BFF: propagate x-correlation-id to all downstream calls [TENANT-D1-SEQ-8]
```

### 9.4 Flow C — Benefits Enrichment

```mermaid
sequenceDiagram
    participant BFF
    participant Broker
    participant RateLimiter
    participant Resolver
    participant BenefitsAdapter as RestBenefitsAdapter
    participant Benefits as Benefits Service

    BFF->>Broker: POST /dispatch { capability: benefits.query } [BROKER-B1B2-SEQ-1]
    Broker->>RateLimiter: check(customer_slug) [BROKER-B1B2-SEQ-2]
    RateLimiter-->>Broker: within budget
    Broker->>Resolver: resolve(benefits.query, customer_slug) [BROKER-B1B2-SEQ-3]
    Resolver-->>Broker: RestBenefitsAdapter
    Broker->>BenefitsAdapter: query(slug, payload) [BROKER-B1B2-SEQ-4]
    BenefitsAdapter->>Benefits: HTTP fetch plan data (customer-partitioned Postgres)
    Benefits-->>BenefitsAdapter: plan data (404 / 503 mapped by SDK fetchPlan)
    BenefitsAdapter-->>Broker: ResolverResponse
    Broker-->>BFF: ResolverResponse [BROKER-B1B2-SEQ-6]
```

### 9.5 Flow D — Escalation Handoff

```mermaid
sequenceDiagram
    participant Member
    participant Client as StellarusClient
    participant BFF
    participant ConvStore as PostgresConversationAdapter
    participant Redactor
    participant Broker
    participant GenesysAdapter
    participant Genesys

    Member->>Client: trigger escalation
    Client->>Client: emit escalation_initiated [ESCALATION-E1E2-SEQ-1]
    Client->>BFF: escalation action { conversationId, reason }
    BFF->>ConvStore: getAll(conversationId) [ESCALATION-E1E2-SEQ-2]
    ConvStore-->>BFF: ALL turns (all roles, all tool calls, no truncation)
    BFF->>Redactor: scrub(fullConversation) — MANDATORY fail-closed gate [ESCALATION-E1E2-SEQ-3]
    Redactor-->>BFF: redactedContext + redaction-confirmation flag
    BFF->>Broker: POST /dispatch { capability: escalation.initiate, payload } [ESCALATION-E1E2-SEQ-4]
    Broker->>GenesysAdapter: resolve(escalation.initiate, customer_slug) + dispatch
    GenesysAdapter->>Genesys: API call (routingMetadata + redactedContext) [ESCALATION-E1E2-SEQ-5]
    Genesys-->>GenesysAdapter: handoff result
    GenesysAdapter-->>BFF: { status: succeeded|failed|unavailable, handoffId? }
    BFF-->>Client: typed escalation result event [ESCALATION-E1E2-SEQ-6]
    BFF->>BFF: write escalation audit record (incl. redaction-confirmation) [ESCALATION-E1E2-SEQ-7]
```

### 9.6 Flow E — Telemetry

```mermaid
sequenceDiagram
    participant Jason
    participant Broker
    participant Benefits as Benefits Service
    participant Loki
    participant Grafana
    participant QA

    Jason->>Grafana: approve F2 metric taxonomy + thresholds [TELEMETRY-F1F2-SEQ-1]
    Broker->>Loki: structured JSON { event, customer_slug, latency_ms, status, capability, correlation_id } [TELEMETRY-F1F2-SEQ-2]
    Benefits->>Loki: structured JSON { event, customer_slug, plan_id, latency_ms, scope, status } [TELEMETRY-F1F2-SEQ-3]
    Grafana->>Loki: LogQL query (datasource uid P8E80F9AEF21F6940)
    Loki-->>Grafana: time-series results
    Grafana->>Grafana: render threshold-colored SLO panels + runbook_url [TELEMETRY-F1F2-SEQ-4]
    QA->>QA: weekly answer-quality scorecard { sampled_count, pass_count, pass_rate, rubric_version, reviewer } [TELEMETRY-F1F2-SEQ-5]
    Jason->>Jason: sign off each F1 launch gate with documented evidence [TELEMETRY-F1F2-SEQ-6]
```

### 9.7 Master Data-Flow Overlay

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef identity fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    customer["Customer app (StellarusProvider)"]:::client
    sdk["StellarusClient / useChat"]:::client
    auth0["Auth0 (PKCE)"]:::identity
    apim["Azure APIM"]:::edge
    ccs["CCS (context token)"]:::ccs
    guard["ContextTokenGuard"]:::ccs
    bff["BFF (agentic-broker-chat)"]:::backend
    broker["Broker (POST /dispatch)"]:::backend
    ratelimiter["RateLimiterService"]:::boundary
    resolver["Resolver (YAML)"]:::backend
    sierraAdapter["SierraAdapter"]:::backend
    sierra["Sierra.ai"]:::identity
    convstore[("PostgresConversationAdapter")]:::store
    restAdapter["RestBenefitsAdapter"]:::backend
    benefits["Benefits Service"]:::backend
    redactor["PII/PHI Redactor (fail-closed)"]:::boundary
    genesysAdapter["GenesysAdapter"]:::backend
    genesys["Genesys Cloud CCaaS"]:::identity
    loki[("Grafana Loki")]:::store
    grafana["Grafana SLO panels"]:::backend
    jason["Jason — F1 gate / F2 taxonomy"]:::boundary

    customer -->|"(2) ?code= PKCE"| auth0
    customer -->|"(1) chat()"| sdk
    sdk -->|"(1) POST /chat (Bearer)"| apim
    auth0 -->|"(2) access token + persona"| apim
    apim -->|"(2) POST /validate/token"| ccs
    ccs -->|"(2) signed context token"| apim
    apim -->|"(1)(2) x-context-token + x-correlation-id"| guard
    guard -->|"(2) @RequireScopes(chat)"| bff
    bff -->|"(1) /dispatch chat.completion"| broker
    bff -->|"(3) /dispatch benefits.query"| broker
    bff -->|"(4) /dispatch escalation.initiate"| broker
    broker -->|"(1)(3) check budget"| ratelimiter
    broker -->|"(1)(3)(4) resolve"| resolver
    broker -->|"(1) stream()"| sierraAdapter
    broker -->|"(3) query()"| restAdapter
    broker -->|"(4) initiate"| genesysAdapter
    sierraAdapter -->|"(1) SSE"| sierra
    sierraAdapter -->|"(1) persist turn"| convstore
    restAdapter -->|"(3) HTTP"| benefits
    bff -->|"(4) getAll turns"| convstore
    bff -->|"(4) scrub (fail-closed)"| redactor
    redactor -->|"(4) redactedContext"| bff
    genesysAdapter -->|"(4) handoff"| genesys
    broker -->|"(5) structured log"| loki
    benefits -->|"(5) structured log"| loki
    grafana -->|"(5) LogQL"| loki
    jason -->|"(5) F1 gate sign-off"| grafana

    linkStyle 1,2,8,11,12,13,16,17 stroke:#1565c0,stroke-width:3px
    linkStyle 0,3,4,5,6,7 stroke:#e65100,stroke-width:3px
    linkStyle 9,14,18 stroke:#1b5e20,stroke-width:3px
    linkStyle 10,15,19,20,21,22 stroke:#b71c1c,stroke-width:3px
    linkStyle 23,24,25,26 stroke:#4a148c,stroke-width:3px
```

## 10. Escalation & CCaaS Handoff

This is a greenfield contract surface (E1E2 ambiguity 5/10, E1 zones unresolved pending BSC/PTP). It composes three already-specified primitives: the SDK surface (§ A1), the Thin-Router Broker dispatch contract (§ B1B2), and the PostgresConversationAdapter durable conversation store (§ B1B2). It does **not** re-specify those — it consumes them.

Escalation owns:
- the member-initiated escalation flow from SDK signal to live-agent connection
- the PII/PHI Redactor (`packages/redactor`) — the mandatory blocking gate
- the GenesysAdapter — the only component that calls the Genesys API
- the versioned, typed SDK escalation event shape
- the BFF escalation route and the conversation-retrieval-for-handoff path
- the escalation audit record (one per attempt) and its writer

Escalation does **not** own:
- the conversation store itself — that is PostgresConversationAdapter (§ B1B2, WI-B1-E), consumed here, not built here
- broker routing logic — the broker resolves `escalation.initiate` to GenesysAdapter via YAML and contains zero Genesys-specific code (INV-05)
- the Genesys API mechanics, routing-metadata field set, PII allow-list, or unavailability SLA — all BLOCKED on BSC/PTP (E1-Z1..Z4)
- Auth0/CCS token issuance (§ D1) or telemetry taxonomy (§ F1F2) — referenced, not owned

### 10.1 Scope

#### In Scope
- member-initiated handoff from chat UI to a Genesys live agent
- the mandatory PII/PHI redaction gate (`packages/redactor`) as the sole path to the external boundary
- retrieval of the full conversation (all turns, all roles, all tool calls) from PostgresConversationAdapter for handoff context
- the versioned, typed SDK escalation event shape (`escalation_initiated` / `succeeded` / `failed` / `unavailable`)
- the BFF escalation route that dispatches `escalation.initiate`
- the GenesysAdapter contract and registration (`genesys-bsca.yaml`), implementation gated on E1
- the escalation audit record written for every attempt
- three new contracts: `genesys-adapter.contract.ts`, `escalation_event.contract.ts`, `pii_redactor.contract.ts`

#### Out of Scope
- Genesys API integration mechanics — REST vs SDK vs widget (E1-Z1, BLOCKED on BSC/PTP)
- the exact routing-metadata field set Genesys requires (E1-Z2, BLOCKED on Julie Hughes + BSC)
- the PII/HIPAA sign-off defining which redacted fields may cross the boundary (E1-Z3, BLOCKED on BSC privacy)
- the Genesys unavailability SLA threshold (E1-Z4, BLOCKED on BSC/PTP ops)
- the product decision for the unavailable-Genesys fallback A/B/C (E2-Z2, owner Julie Hughes, due Jul 12)
- live-agent assignment, queue management, and connection — owned by Genesys, beyond the handoff boundary
- conversation persistence itself — see § B1B2 PostgresConversationAdapter

### 10.2 Architecture Position

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    member["BSC Member (chat UI)"]:::client
    sdk["@stellarus/chat-client SDK"]:::client
    bff["agentic-broker-chat (BFF)"]:::backend
    redactor["PII/PHI Redactor (packages/redactor)"]:::ccs
    conv[("PostgresConversationAdapter")]:::store
    broker["Thin-Router Broker POST /dispatch"]:::edge
    adapter["GenesysAdapter (only Genesys caller)"]:::backend
    genesys["Genesys Cloud CCaaS (external)"]:::boundary
    audit[("Escalation Audit Log")]:::store

    member -->|"escalation action"| sdk
    sdk -->|"escalation_initiated (typed event)"| bff
    bff -->|"getAll(conversationId) — all turns"| conv
    conv -->|"full conversation (raw)"| bff
    bff -->|"scrub() MANDATORY gate"| redactor
    redactor -->|"redactedContext + confirmation flag"| bff
    bff -->|"dispatch escalation.initiate"| broker
    broker -->|"resolve via genesys-bsca.yaml"| adapter
    adapter -->|"routingMetadata + redactedContext"| genesys
    bff -->|"audit record (every attempt)"| audit
```

### 10.3 Actors

| Actor | Role |
|---|---|
| `ACT-MEMBER` | BSC member (end user) — initiates escalation from chat UI; expects uninterrupted handoff to a live agent |
| `ACT-SDK` | `@stellarus/chat-client` — emits typed escalation events to the customer UI; owns the escalation event shape |
| `ACT-BFF` | agentic-broker-chat — receives the escalation action; retrieves conversation; runs the redactor; dispatches `escalation.initiate`; writes the audit record |
| `ACT-BROKER` | agentic-broker-api — routes `escalation.initiate` to GenesysAdapter via YAML; contains no Genesys logic |
| `ACT-GENESYS-ADAPTER` | GenesysAdapter (DataSourceAdapter) — the ONLY component that calls the Genesys API; owns the Genesys circuit breaker |
| `ACT-CONV-ADAPTER` | PostgresConversationAdapter — provides the full conversation history (all turns, all roles, all tool calls) for handoff |
| `ACT-REDACTOR` | PII/PHI Redactor — scrubs all conversation content before it leaves Stellarus to any external system |
| `ACT-GENESYS` | Genesys Cloud CCaaS (external) — receives the handoff; routes to a live agent; owns agent assignment/connection |
| `ACT-AGENT` | Live support agent — receives conversation context; continues without restarting from scratch |
| `ACT-JULIE` | Julie Hughes (Product Lead P5) — owns product decisions; resolves E2-Z2 (fallback) and the E1 zones with BSC |
| `ACT-BSC-PTP` | BSC/PTP business + contact center team — owns Genesys API mechanics, routing-metadata fields, PII/HIPAA sign-off, SLA |
| `ACT-MAINTAINER` | Stellarus platform team — drops YAML configs; cuts SDK releases; governs versioning |

### 10.4 Locked Escalation Flow (ESCALATION-E1E2-SEQ-1..7)

| SEQ | Caller → must invoke | Temporal | Breaks if missing |
|---|---|---|---|
| `SEQ-1` | `ACT-SDK` → emit `escalation_initiated` | BEFORE `ACT-BFF` dispatches | member UI has no feedback escalation started |
| `SEQ-2` | `ACT-BFF` → `ACT-CONV-ADAPTER.getAll(conversationId)` | BEFORE `scrub()` | redactor receives empty/partial context |
| `SEQ-3` | `ACT-BFF` → `ACT-REDACTOR.scrub(fullConversation)` | BEFORE dispatch to broker | unredacted member data reaches Genesys — HIPAA violation |
| `SEQ-4` | `ACT-BFF` → `ACT-BROKER POST /dispatch` (`escalation.initiate`) | AFTER `scrub()` completes | routing to Genesys never happens |
| `SEQ-5` | `ACT-GENESYS-ADAPTER` → Genesys API (routing metadata + redacted context) | AFTER receiving dispatch | handoff fails silently; agent not notified |
| `SEQ-6` | `ACT-BFF` → emit handoff result to `ACT-SDK` | AFTER Genesys response | member gets no feedback |
| `SEQ-7` | `ACT-BFF` → write escalation audit record (incl. redaction confirmation) | DURING `SEQ-5` | no audit trail for compliance review |

```mermaid
sequenceDiagram
    participant M as Member
    participant SDK as SDK
    participant BFF as BFF (agentic-broker-chat)
    participant CONV as PostgresConversationAdapter
    participant RED as PII/PHI Redactor
    participant BR as Broker (/dispatch)
    participant GA as GenesysAdapter
    participant GEN as Genesys Cloud

    M->>SDK: tap "talk to a person"
    SDK->>BFF: escalation_initiated (SEQ-1)
    BFF->>CONV: getAll(conversationId) — all turns/roles/tool-calls (SEQ-2)
    CONV-->>BFF: full conversation (raw, no trimming)
    BFF->>RED: scrub(fullConversation) — MANDATORY gate (SEQ-3)
    RED-->>BFF: redactedContext + redaction-confirmation flag
    BFF->>BR: POST /dispatch escalation.initiate (SEQ-4)
    BR->>GA: resolve via genesys-bsca.yaml
    GA->>GEN: routingMetadata + redactedContext (SEQ-5)
    GEN-->>GA: handoff result (succeeded | failed | unavailable)
    GA-->>BFF: typed result
    BFF->>SDK: escalation_succeeded | _failed | _unavailable (SEQ-6)
    BFF->>BFF: write audit record (SEQ-7)
```

### 10.5 The PII/PHI Redaction Gate

- **It scrubs all conversation content BEFORE anything leaves Stellarus (INV-01).** `ACT-GENESYS-ADAPTER` SHALL NOT transmit any member-identifiable information that has not passed `ACT-REDACTOR`.
- **The BFF never sends raw content to the broker or the GenesysAdapter (INV-02).** `scrub()` MUST complete successfully before IP-4 (the dispatch). There is no code path from the conversation store to the broker that bypasses the redactor.
- **The conversation adapter provides ALL turns (INV-03)** — every role (member, assistant), every tool call, raw content, no summary window — and the BFF SHALL NOT filter or trim before handing to the redactor. A summarized or windowed context is a contract violation: the redactor must see everything in order to scrub everything.
- **The conversation source is exclusively PostgresConversationAdapter (INV-09).** Sierra native session storage is NOT authoritative and SHALL NOT be a source for escalation context. This is the same invariant § B1B2 establishes for the durable store (INV-06), restated here as a hard escalation constraint.

Scrub failure **cancels the escalation and fails fast.** A redactor error is never swallowed, never downgraded to a "best effort" partial send. On `scrub()` failure the BFF:

1. does NOT dispatch `escalation.initiate` (nothing reaches the broker),
2. emits `escalation_failed` to the SDK (the member is told the handoff did not complete),
3. writes an audit record for the cancellation (INV-04) with the redaction-confirmation flag set false.

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    conv[("Conversation (ALL turns, all roles, tool calls)")]:::store
    red["PII/PHI Redactor scrub()"]:::ccs
    decision{"scrub success?"}
    dispatch["dispatch to Genesys (via broker → GenesysAdapter)"]:::backend
    genesys["Genesys Cloud (external boundary)"]:::boundary
    cancel["CANCEL escalation"]:::client
    failevent["emit escalation_failed"]:::client
    auditok[("audit: result=dispatched, redaction-confirmed=true")]:::store
    auditfail[("audit: result=cancelled, redaction-confirmed=false")]:::store

    conv --> red
    red --> decision
    decision -->|"success"| dispatch
    dispatch --> genesys
    dispatch --> auditok
    decision -->|"failure (CL15-A fail-closed)"| cancel
    cancel --> failevent
    cancel --> auditfail
```

**Decision for v1:** ship `packages/redactor` with the contract, the versioned-rule-set scaffolding, the fail-closed `scrub()` semantics, and the confirmation-flag emission. The concrete allow/deny rules are seeded from BSC's E1-Z3 sign-off.

### 10.6 GenesysAdapter

| Property | Specification | Clause |
|---|---|---|
| Capability | `escalation.initiate` | B1B2 capability registry |
| Registration | `genesys-bsca.yaml` in `RESOLVER_CONFIG_DIR` — broker needs no source change | INV-06 |
| Sole caller | the ONLY component permitted to call the Genesys API | INV-05 |
| Credentials | Azure Key Vault via Managed Identity (`DefaultAzureCredential`) — never env vars in production | INV-07 |
| Circuit breaker | per-provider, owned by the adapter, **starts CLOSED** | INV-05 / circuit-breaker-in-adapter |
| Payload in | `{ conversationId, reason, redactedContext, routingMetadata }` | IP-4 |
| Result out | `{ status: succeeded \| failed \| unavailable, handoffId?, agentName? }` | IP-6 |

### 10.7 SDK Escalation Event Shape

| Event | Meaning | Carries |
|---|---|---|
| `escalation_initiated` | handoff in flight | `conversationId` |
| `escalation_succeeded` | live agent connected | `conversationId`, `handoffId` |
| `escalation_failed` | handoff errored (includes redaction failure) | `conversationId` |
| `escalation_unavailable` | Genesys unreachable — surfaced behavior per E2-Z2 fallback (TBD) | `conversationId` |

Hard constraints on the shape:

- **Never exposes Genesys internals.** Queue names, routing metadata fields, and internal Genesys IDs SHALL NOT appear in any event, type, or error string. The customer UI knows only the lifecycle state, the `conversationId`, and the opaque `handoffId`.
- **Carries `conversationId` + `handoffId`** (the latter when available) — and nothing that leaks the contact-center topology.
- **MAJOR-bumped before breaking changes (INV-08).** Removing, renaming, or changing the type signature of any escalation event requires an SDK MAJOR version increment, consistent with the § A1 SDK surface-lock invariant (A1 INV-13).

```mermaid
stateDiagram-v2
    [*] --> initiated: member triggers (SEQ-1)
    initiated --> succeeded: agent connected
    initiated --> failed: errored (incl. redaction failure, CL15-A)
    initiated --> unavailable: Genesys unreachable
    succeeded --> [*]
    failed --> [*]
    unavailable --> [*]
    note right of unavailable
        Surfaced behavior per E2-Z2
        fallback A/B/C — owner Julie Hughes,
        due Jul 12. TBD.
    end note
    note right of initiated
        Versioned event shape.
        MAJOR-bump on breaking change (INV-08).
    end note
```

### 10.8 Escalation Audit Record (INV-04)

| Field | Type | Constraints |
|---|---|---|
| `timestamp` | `timestamptz` | NOT NULL — when the attempt occurred |
| `conversationId` | `uuid` | NOT NULL — the conversation handed off |
| `reason` | `text` | NOT NULL — member-supplied or system escalation reason |
| `result` | `text` | NOT NULL — `succeeded \| failed \| unavailable \| cancelled` |
| `handoffId` | `text` | nullable — present only when Genesys returned one |
| `redaction_confirmed` | `boolean` | NOT NULL — the redactor's confirmation flag (false on scrub failure) |
| `redactor_rule_version` | `text` | NOT NULL — the versioned rule set in force at scrub time |
| `correlation_id` | `text` | nullable, indexed — threaded from `x-correlation-id` for trace correlation |

### 10.9 Blocked Frontier (E1 — BSC/PTP ownership)

| Zone | Blocked item | Owner | Status |
|---|---|---|---|
| `E1-Z1` | Genesys API mechanics — REST? SDK? widget? | Julie Hughes + BSC contact center | BLOCKED |
| `E1-Z2` | routing-metadata fields Genesys requires (queue/skill/priority/identity — exact set TBD) | Julie Hughes + BSC | BLOCKED |
| `E1-Z3` | PII/HIPAA sign-off — which member data may appear in redacted context | BSC privacy + HIPAA | BLOCKED |
| `E1-Z4` | Genesys unavailability SLA — wait-time before declaring unavailable | BSC/PTP ops | BLOCKED |
| `E2-Z2` | unavailability fallback A/B/C (product decision) | Julie Hughes | due Jul 12 |

```mermaid
flowchart LR
    classDef blocked fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef pending fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef green fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000

    subgraph BSC["BLOCKED on BSC/PTP (E1)"]
        z1["E1-Z1 Genesys API mechanics (Julie Hughes + BSC contact center)"]:::blocked
        z2["E1-Z2 routing metadata fields (Julie Hughes + BSC)"]:::blocked
        z3["E1-Z3 PII/HIPAA sign-off (BSC privacy)"]:::blocked
        z4["E1-Z4 unavailability SLA (BSC/PTP ops)"]:::blocked
        z5["E2-Z2 fallback A/B/C (Julie Hughes, Jul 12)"]:::pending
    end

    subgraph STELLARUS["Stellarus-owned — ships now (E2)"]
        b["WI-E2-B Redactor"]:::green
        d["WI-E2-D SDK v2 event shape"]:::green
        e["WI-E2-E BFF escalation route"]:::green
        f["WI-E2-F audit log schema + writer"]:::green
    end

    gc["WI-E2-C GenesysAdapter YAML + impl"]:::pending
    z1 -.->|"unblocks"| gc
    z2 -.->|"unblocks"| gc
    z3 -.->|"seeds rules"| b
```

### 10.10 Work Item Split — Unblocked (ships now) vs Gated

| Work item | Description | Owner | Status |
|---|---|---|---|
| `WI-E2-B` | PII/PHI Redactor design + impl (`packages/redactor`) | Stellarus | unblocked — ships now |
| `WI-E2-D` | SDK v2 escalation event shape | Stellarus (Ketema) | unblocked — ships now |
| `WI-E2-E` | BFF escalation route + dispatch | Stellarus (Ketema) | unblocked — ships now |
| `WI-E2-F` | escalation audit log schema + writer | Stellarus (Ketema) | unblocked — ships now |
| `WI-E2-C` | GenesysAdapter YAML + impl | Stellarus (Ketema) | gated on E1-A/E1-B |
| `WI-E1-A` | Genesys API mechanics discovery | Julie + BSC/PTP | blocker |
| `WI-E1-B` | routing-metadata field definition | Julie + BSC | blocker |
| `WI-E1-C` | PII/HIPAA sign-off | BSC privacy | blocker |
| `WI-E1-D` | Genesys unavailability SLA | Julie + BSC ops | blocker |
| `WI-E2-A` | unavailability fallback A/B/C decision | Julie | Jul 12 |

### 10.11 Decision-for-v1 / Deferred / Trigger

- **Decision for v1: ship the contracts + redactor + SDK v2 event shape.** The escalation slice ships with `genesys-adapter.contract.ts`, `escalation_event.contract.ts`, and `pii_redactor.contract.ts`; the `packages/redactor` gate (fail-closed, versioned, confirmation-flag-emitting); the versioned SDK event shape; the BFF route; and the audit writer. The GenesysAdapter ships as a registered stub that returns `unavailable`.
- **Deferred to E1 unblock: the live Genesys leg.** The GenesysAdapter implementation (`WI-E2-C`) — the actual call into Genesys with real routing metadata — is deferred. It cannot be built correctly without E1-Z1 (API mechanics) and E1-Z2 (routing fields).
- **Trigger for revisit:** BSC/PTP delivers the Genesys API mechanics (E1-Z1) + routing-metadata fields (E1-Z2) + PII/HIPAA sign-off (E1-Z3), AND Julie resolves the unavailability fallback (E2-Z2, due Jul 12). On that trigger, `WI-E2-C` implements the adapter against the now-known API, the redactor rules are loaded from the E1-Z3 allow-list, and the `escalation_unavailable` SDK fallback is wired per the E2-Z2 decision.

### 10.12 Failure Handling

#### Redaction Failures
| Condition | Response |
|---|---|
| `scrub()` throws or returns no confirmation | CANCEL escalation; emit `escalation_failed`; audit `result=cancelled, redaction_confirmed=false` (CL15-A fail-closed) |
| conversation retrieval returns partial/empty | abort before `scrub()`; do not dispatch (INV-03 — redactor must see all turns) |

#### Genesys Handoff Failures
| Condition | Response |
|---|---|
| Genesys returns error | emit `escalation_failed`; audit `result=failed` |
| Genesys unreachable / circuit breaker OPEN | emit `escalation_unavailable`; audit `result=unavailable`; surfaced UI behavior per E2-Z2 (TBD) |
| Genesys exceeds SLA wait threshold | declared `unavailable` per E1-Z4 threshold (BLOCKED — threshold TBD) |

#### Audit Failures
| Condition | Response |
|---|---|
| audit write fails | escalation is not silently un-trailed; the BFF surfaces an internal error and the failure is logged at error level — the compliance trail is mandatory (INV-04) |

### 10.13 Security & Compliance Model

#### Trust Boundaries
| Layer | Trust level | Verification |
|---|---|---|
| SDK / member UI | Untrusted | escalation action carries only `{ conversationId, reason }`; no raw conversation |
| BFF (agentic-broker-chat) | Trust boundary | retrieves authoritative conversation; runs the mandatory redactor gate |
| PII/PHI Redactor | Compliance gate | the single point where member data is scrubbed before egress (INV-01) |
| GenesysAdapter | Egress trust boundary | only caller of Genesys; Managed-Identity creds; transmits only redacted content (INV-05, INV-07) |
| Genesys Cloud | External (untrusted) | receives only `redactedContext` + `routingMetadata`; never raw member data |

- **No raw member data crosses the Stellarus boundary (INV-01/02).** The redactor is the only path out; fail-closed on its failure (CL15-A).
- **GenesysAdapter is the sole Genesys caller (INV-05).** Any other component referencing the Genesys API is a detectable architecture violation.
- **Credentials never in text (CL16, INV-07).** Genesys creds resolve from Azure Key Vault via Managed Identity; no env var, no file, no image layer.
- **No member-identifiable data in logs (F1F2 INV-02a/b).** The GenesysAdapter's SLO log events carry `customer_slug`, `correlation_id`, `status` — never member identity. The redactor rules (CL9) are the referenced authority for what is scrubbed.

### 10.14 New Contracts

| Contract | Location | Governs |
|---|---|---|
| `genesys-adapter.contract.ts` | `apps/agentic-broker-api/adapters/` | GenesysAdapter PRE/POST/INV — sole-caller (INV-05), Managed-Identity creds (INV-07), circuit breaker starts CLOSED, redacted-only payload (INV-01) |
| `escalation_event.contract.ts` | `packages/chat-client/src/contracts/` | versioned SDK event shape — four lifecycle states, no Genesys internals exposed, MAJOR-bump rule (INV-08) |
| `pii_redactor.contract.ts` | `packages/redactor/src/contracts/` | `scrub()` PRE/POST/INV — all-turns input (INV-03), fail-closed (CL15-A), confirmation-flag emission, versioned rule set |

### 10.15 Key Constraints & Rules

- **The redactor is the gate, and it is fail-closed.** All conversation content passes `scrub()` before leaving Stellarus (INV-01); scrub failure cancels the escalation (CL15-A). Nothing bypasses it.
- **The BFF never sends raw content downstream (INV-02).** `scrub()` completes before the dispatch; there is no raw-content path to the broker or GenesysAdapter.
- **The redactor sees everything (INV-03).** All turns, all roles, all tool calls, no summary window; the BFF does not filter or trim first.
- **Conversation source is exclusively PostgresConversationAdapter (INV-09).** Sierra native storage is never authoritative for escalation context.
- **GenesysAdapter is the only Genesys caller (INV-05)** and the broker holds no Genesys logic — routing is YAML (`genesys-bsca.yaml`, INV-06).
- **Genesys creds come from Azure Key Vault via Managed Identity (INV-07, CL16)** — never env vars in production.
- **The SDK event shape is versioned and leak-free (INV-08).** It never exposes Genesys queue names, routing metadata, or internal IDs; breaking changes require a MAJOR bump.
- **Every escalation attempt is audited (INV-04)** — including cancellations — with the redaction-confirmation flag and rule version.
- **Same surface = same BFF.** Escalation from chat lives in agentic-broker-chat; the broker has structurally nowhere to put a named escalation endpoint.

### 10.16 Decisions Still Open

| # | Question | Owner | Why it matters |
|---|---|---|---|
| E1-Z1 | Genesys API mechanics — REST / SDK / widget | Julie Hughes + BSC contact center | blocks `WI-E2-C` GenesysAdapter implementation entirely |
| E1-Z2 | routing-metadata fields Genesys requires | Julie Hughes + BSC | defines the `routingMetadata` payload shape |
| E1-Z3 | PII/HIPAA sign-off on allowed redacted fields | BSC privacy + HIPAA | seeds the redactor's concrete rule set |
| E1-Z4 | Genesys unavailability SLA threshold | BSC/PTP ops | defines when a handoff is declared `unavailable` |
| E2-Z2 | unavailability fallback A/B/C surfaced behavior | Julie Hughes (due Jul 12) | wires the `escalation_unavailable` SDK UI behavior |

## 11. Telemetry, SLOs & Launch Gates

### 11.2 Scope

#### In Scope

- structured JSON log emission from the broker on every chat request, error, and circuit-breaker event (INV-01a, SEQ-2)
- structured JSON log emission from the Benefits Service on every plan fetch and scope-validation failure (INV-01b, SEQ-3)
- `correlation_id` propagated from `x-correlation-id` into every log event (INV-06)
- canonical F2 field-name lock — dashboard owners consume names, never invent them (INV-01a/b)
- the F2 metric taxonomy: five SLO groups plus the Composite Reliability Score (§11.5)
- the Grafana operational dashboard surface (Loki, LogQL, threshold-colored panels) (§11.6)
- the F1 launch-gate evidence shapes (QA scorecard, InfoSec attestation) and sign-off chain (§11.8)
- the SLO threshold table (all values `TBD`), acceptance-criteria checklist, per-SLO operational runbooks, and rollback + RC go/no-go checklist

#### Out of Scope

- the actual SLO threshold *values* — owned by ACT-JASON (F1-Z1, due Jul 15); this section locks names and shapes, not numbers
- the answer-quality rubric criteria/scale — owned by ACT-JASON + ACT-QA (F2-Z2)
- Composite Reliability Score weights — owned by ACT-JASON (F2-Z4)
- bolting Loki into the Analytics Next.js app — explicitly forbidden; the surfaces are disjoint (§11.6)
- a Prometheus deployment — does not exist in `k8s-argocd`, not added in this cycle (YAGNI)
- the Analytics app multi-tenancy refactor — tracked in parallel (WI-F3-D, Pramod), not blocking telemetry emission
- the PII/PHI Redactor rule set itself — owned by the Escalation slice (`packages/redactor`); §11 only references it for log-field privacy

### 11.3 Architecture Position

```mermaid
flowchart TB
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    broker["agentic-broker-api (Thin-Router Broker)"]:::backend
    benefits["benefits-service (Benefits Service)"]:::backend
    genesys["GenesysAdapter (escalation logs)"]:::backend

    loki[("Loki — monitoring.dev.stellarus.com<br/>uid P8E80F9AEF21F6940")]:::store
    grafana["Grafana — ops introspection<br/>threshold-colored SLO panels<br/>owners Grace + Syed"]:::edge

    snow[("Snowflake / aggregated")]:::store
    analytics["Analytics app (apps/analytics)<br/>BI: session volumes, quality, cost<br/>owner Pramod"]:::client

    broker -->|"JSON: event, customer_slug, latency_ms, status, capability, correlation_id"| loki
    benefits -->|"JSON: event, customer_slug, plan_id, latency_ms, scope, status"| loki
    genesys -->|"escalation_succeeded / escalation_failed"| loki
    loki -->|"LogQL time-series"| grafana

    snow --> analytics

    grafana -. "do NOT bridge Loki into the analytics app<br/>(different query language, latency, audience)" .-> analytics
    loki -. "no LogQL leg into Next.js (INV-03 / surface split)" .-> analytics
```

### 11.4 Structured-Log Contracts

#### Broker emission contract

`apps/agentic-broker-api/contracts/telemetry.contract.ts` — emitted on **every** chat request, error, and circuit-breaker event (SEQ-2, IP-1).

| Field | Type | Description |
|---|---|---|
| `event` | `text` | canonical event name (`chat_completed`, `chat_error`, `chat_first_token`, `circuit_breaker_open`, `answer_unsupported`) |
| `customer_slug` | `text` | immutable tenant id from the verified context token — never client-supplied |
| `latency_ms` | `number` | event latency in milliseconds (first-token uses `latency_ms`; end-to-end adds `duration_ms`) |
| `status` | `text` | outcome status (`ok`, `error`, `open`) |
| `capability` | `text` | opaque capability string resolved by the broker (e.g. `chat.completion`) — INV-02 keeps it opaque |
| `correlation_id` | `text` | from `x-correlation-id`, present in **every** event (INV-06) |

#### Benefits Service emission contract

`apps/benefits-service/contracts/telemetry.contract.ts` — emitted on **every** plan fetch and scope-validation failure (SEQ-3, IP-2).

| Field | Type | Description |
|---|---|---|
| `event` | `text` | canonical event name (`plan_fetched`, `plan_fetch_error`, `scope_validation_failed`) |
| `customer_slug` | `text` | immutable tenant id from the verified context token |
| `plan_id` | `text` | anonymized plan reference — **no member-identifiable derivation** (INV-02b) |
| `latency_ms` | `number` | fetch latency in milliseconds |
| `scope` | `text` | the `{resource}:{action}` scope evaluated (e.g. `benefits:read`) |
| `status` | `text` | outcome status (`ok`, `not_found`, `outage`, `denied`) |
| `correlation_id` | `text` | the **same** `correlation_id` propagated from the originating request (INV-06) |

#### Privacy constraints (must NOT record)

Per **INV-02a/b**, CL9, and the §10 PII/PHI Redactor rules, **no member-identifiable data** appears in any log field. Log fields must NOT record:

- member name, DOB, address, or any direct identifier
- raw plan ID beyond an anonymized reference (`plan_id` is a reference, not a member's enrolled plan record)
- raw conversation content, prompts, or model responses
- the signed `x-context-token` value or any Auth0 access/refresh token

`correlation_id` carries **no** integrity or security meaning (INV-05, D1) — it is observability-only metadata, generated as a UUIDv4 by APIM, stripped on inbound from external callers (D1 SEQ-4), and propagated server-side. It is the join key across the broker and Benefits Service log streams, never a claim.

### 11.5 F2 Metric Taxonomy

```mermaid
flowchart LR
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000

    g1["Group 1 — Chat Health<br/>chat_completed vs chat_error<br/>circuit_breaker_open<br/>[threshold TBD]"]:::backend
    g2["Group 2 — Chat Speed<br/>chat_first_token (latency_ms, T)<br/>chat_completed (duration_ms, T2)<br/>[thresholds TBD]"]:::backend
    g3["Group 3 — Answer Quality<br/>ACT-QA weekly sampling<br/>answer_unsupported rate<br/>[threshold TBD]"]:::backend
    g4["Group 4 — Escalation<br/>escalation_succeeded vs<br/>escalation_failed (GenesysAdapter)<br/>[threshold TBD]"]:::backend
    g5["Group 5 — Cost<br/>chat_completed.token_cost (dollars)<br/>cost per answer<br/>[threshold TBD]"]:::backend

    composite["Composite Reliability Score<br/>weighted average of SLO compliance<br/>weights TBD (F2-Z4)"]:::edge

    g1 -->|"compliance rate"| composite
    g2 -->|"compliance rate"| composite
    g3 -->|"compliance rate"| composite
    g4 -->|"compliance rate"| composite
    g5 -->|"compliance rate"| composite
```

| SLO Group | SLI source (canonical events / fields) | Metric | Owner | Threshold |
|---|---|---|---|---|
| **1 — Chat Health** | `chat_completed` vs `chat_error` | Chat Success Rate | ACT-GRACE | `TBD` (F1-Z1) |
| **1 — Chat Health** | `circuit_breaker_open` | Circuit Breaker Health | ACT-GRACE | `TBD` |
| **2 — Chat Speed** | `chat_first_token` · `latency_ms` | First Token Latency (threshold `T`) | ACT-GRACE | `TBD` |
| **2 — Chat Speed** | `chat_completed` · `duration_ms` | End-to-End Latency (threshold `T2`) | ACT-GRACE | `TBD` |
| **3 — Answer Quality** | ACT-QA weekly answer-quality sample | Answer Quality Score | ACT-QA | `TBD` (F2-Z2) |
| **3 — Answer Quality** | `answer_unsupported` | Unsupported Answer Rate | ACT-GRACE | `TBD` |
| **4 — Escalation** | `escalation_succeeded` vs `escalation_failed` | Escalation Success Rate | ACT-GRACE | `TBD` |
| **5 — Cost** | `chat_completed` · `token_cost` (`$`) | Cost per Answer | ACT-SYED | `TBD` (F1-Z3 + finance) |
| **Composite** | weighted average of all five groups | Composite Reliability Score | ACT-JASON | weights `TBD` (F2-Z4) |

### 11.6 Dashboard Surface Split

This is a **load-bearing architecture verdict**, confirmed 2026-06-26 (F2-Z3): **Grafana = ops introspection; Analytics app = business intelligence.** They are intentionally disjoint surfaces.

**Grafana (ops introspection).** Reads Loki via LogQL (datasource uid `P8E80F9AEF21F6940` at `monitoring.dev.stellarus.com`). Renders **threshold-colored SLO status panels** (green/yellow/red) per the F2 taxonomy — **not raw counter panels** (INV-03). Every alert rule is annotated with a `runbook_url` (INV-07); ACT-OPS approves no alert without one. Owners: **Grace + Syed**. Audience: the on-call ops team.

**Analytics app (business intelligence).** `apps/analytics` — session volumes, quality trends, cost — for stakeholders and eventually external customers. Sources data from **Snowflake/aggregated**, not Loki. Owner: **Pramod + platform**. Chart components (`HorizontalStackedBar`, `DashboardPageClient`) extract to `packages/ui-charts` (WI-F3-D, parallel). The app is **not** multi-tenant-ready today — that is a refactor (thread `tenantId` through `@stellarus/db DbClient`), not a rebuild.

| Aspect | Grafana (ops) | Analytics app (BI) |
|---|---|---|
| Data source | Loki (`P8E80F9AEF21F6940`) | Snowflake / aggregated |
| Query language | LogQL | SQL |
| Latency | near-real-time log tail | batch-aggregated |
| Audience | on-call ops team | stakeholders, future external customers |
| Panel style | threshold-colored SLO status (INV-03) | volume/trend/cost charts |
| Owner | Grace + Syed | Pramod + platform |
| Alerting | `runbook_url` on every alert (INV-07) | none |

### 11.7 Structured Log Emission Flow

```mermaid
sequenceDiagram
    participant R as Request (x-correlation-id)
    participant B as Broker
    participant L as Loki
    participant G as Grafana

    R->>B: POST /dispatch (capability, x-correlation-id)
    B->>B: emit chat_completed log<br/>(customer_slug + capability + correlation_id)
    B->>L: structured JSON event (TELEMETRY-F1F2-SEQ-2)
    G->>L: LogQL query (uid P8E80F9AEF21F6940)
    L-->>G: time series (TELEMETRY-F1F2-SEQ-4)
    G->>G: render threshold-colored SLO panel<br/>(green/yellow/red, INV-03)
```

### 11.8 F1 Launch Gates

```mermaid
flowchart LR
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    qa["QA answer-quality scorecard<br/>sampled_count, pass_count,<br/>pass_rate, rubric_version, reviewer"]:::backend
    infosec["InfoSec tenant-isolation attestation<br/>cross_tenant_incidents,<br/>test_evidence, sign_off_date"]:::backend
    support["Support runbook readiness<br/>(per-SLO runbooks, §11.11)"]:::backend
    rollback["Rollback plan<br/>(target under 5 min, §11.12)"]:::backend

    gate{"ACT-JASON gate sign-off<br/>documented evidence required<br/>(INV-04)"}:::edge

    go["Sep 1 2026 RC<br/>GO / NO-GO"]:::store
    blocked["BLOCKED<br/>(no evidence path)"]:::boundary

    qa --> gate
    infosec --> gate
    support --> gate
    rollback --> gate

    gate -->|"all categories evidenced"| go
    gate -. "any category lacks documented evidence" .-> blocked
```

| Gate category | Evidence shape | Evidence owner | Sign-off |
|---|---|---|---|
| Quality | answer-quality scorecard `{ sampled_count, pass_count, pass_rate, rubric_version, reviewer }` (IP-4) | ACT-QA | ACT-JASON |
| Security | tenant-isolation attestation `{ cross_tenant_incidents, test_evidence, sign_off_date }` (IP-5) | ACT-INFOSEC | ACT-JASON |
| Privacy | redaction-confirmation evidence (PII/PHI Redactor rule set + §10 audit flag) | ACT-INFOSEC + BSC compliance | ACT-JASON |
| Support | per-SLO operational runbooks present and `runbook_url`-linked (INV-07, §11.11) | ACT-OPS | ACT-JASON |
| Rollback | rollback plan + RC go/no-go checklist, target < 5 min (§11.12) | ACT-OPS | ACT-JASON |

### 11.9 SLO Threshold Table

| SLO | SLI (canonical field) | Comparator | Threshold | Unit | Owner |
|---|---|---|---|---|---|
| Chat Success Rate | `chat_completed` / (`chat_completed` + `chat_error`) | `>=` | `TBD` | `%` | ACT-JASON |
| Circuit Breaker Health | `circuit_breaker_open` rate | `<=` | `TBD` | `events/hr` | ACT-JASON |
| First Token Latency | `chat_first_token` · `latency_ms` (p95) | `<=` | `T` `TBD` | `ms` | ACT-JASON |
| End-to-End Latency | `chat_completed` · `duration_ms` (p95) | `<=` | `T2` `TBD` | `ms` | ACT-JASON |
| Answer Quality Score | ACT-QA weekly `pass_rate` | `>=` | `TBD` | `%` | ACT-JASON |
| Unsupported Answer Rate | `answer_unsupported` rate | `<=` | `TBD` | `%` | ACT-JASON |
| Escalation Success Rate | `escalation_succeeded` / (`succeeded` + `failed`) | `>=` | `TBD` | `%` | ACT-JASON |
| Cost per Answer | `chat_completed` · `token_cost` (mean) | `<=` | `TBD` | `$` | ACT-JASON |
| Composite Reliability Score | weighted avg of the above | `>=` | `TBD` | `score` | ACT-JASON |

### 11.10 Acceptance Criteria

- [ ] broker emits canonical-named structured JSON on every `chat_completed`, `chat_error`, `chat_first_token`, `circuit_breaker_open`, `answer_unsupported` event (SEQ-2, INV-01a)
- [ ] Benefits Service emits canonical-named structured JSON on every `plan_fetched` / `scope_validation_failed` event (SEQ-3, INV-01b)
- [ ] every emitted event carries `correlation_id` propagated from `x-correlation-id` (INV-06)
- [ ] no log field contains member-identifiable data (INV-02a/b, verified against §10 redactor rules)
- [ ] ACT-JASON has approved the F2 taxonomy + thresholds (SEQ-1) — dashboards built only after (INV-05)
- [ ] Grafana renders threshold-colored SLO panels, no raw counter panels (INV-03)
- [ ] every Grafana alert is annotated with a `runbook_url` (INV-07)
- [ ] QA answer-quality scorecard produced weekly from alpha to RC (SEQ-5)
- [ ] InfoSec tenant-isolation attestation signed with `cross_tenant_incidents` documented
- [ ] per-SLO operational runbooks exist and are `runbook_url`-linked (§11.11)
- [ ] rollback plan validated against the < 5-minute target (§11.12)
- [ ] all five F1 launch gates signed off by ACT-JASON with documented evidence (SEQ-6)

### 11.11 Operational Runbooks

#### 11.11.1 Chat Success Rate breach (`chat_error` spike)

1. Open the Chat Health panel; confirm the breach is `chat_error` rate, not a `circuit_breaker_open` cascade.
2. LogQL-filter `event="chat_error"` by `customer_slug` — single-tenant or platform-wide?
3. Join by `correlation_id` to the originating dispatch to locate the failing capability.
4. If isolated to `chat.completion`, check SierraAdapter circuit-breaker state (`circuit_breaker_open`).
5. If platform-wide, escalate to the rollback runbook (§11.12).

#### 11.11.2 Circuit Breaker open (`circuit_breaker_open`)

1. Identify the adapter — Sierra's breaker lives in SierraAdapter, Genesys's in GenesysAdapter (INV-09).
2. Confirm the downstream is actually unhealthy (the breaker is doing its job) vs a false trip.
3. If downstream healthy, inspect the adapter's failure-threshold config; do not patch the broker.
4. Annotate the incident with the `correlation_id` range affected.

#### 11.11.3 Latency breach (`chat_first_token` `T` / `chat_completed` `T2`)

1. Determine which leg breached — first-token (`latency_ms`) vs end-to-end (`duration_ms`).
2. First-token regression points at Sierra upstream; end-to-end regression points at the conversation persist path (PostgresConversationAdapter).
3. Correlate against the deploy timeline; if a deploy preceded the breach, evaluate rollback (§11.12).

#### 11.11.4 Escalation Success Rate breach (`escalation_failed` spike)

1. LogQL-filter GenesysAdapter `event="escalation_failed"`.
2. Confirm GenesysAdapter is the only caller of Genesys (INV-05) — no out-of-band path.
3. Check Genesys circuit-breaker state and Azure Key Vault credential resolution (INV-07).
4. Verify the PII/PHI Redactor did not fail-closed (a redaction failure cancels the escalation, CL15-A) — that surfaces as `escalation_failed`, not a Genesys outage.

#### 11.11.5 Cost per Answer breach (`token_cost`)

1. LogQL-aggregate `chat_completed.token_cost` by `customer_slug`.
2. Identify whether a single tenant or a prompt-size regression drives the spike.
3. Confirm RateLimiterService is enforcing per-tenant budgets on `customer_slug` (INV-08).

### 11.12 Rollback Plan & RC Go/No-Go Checklist

#### 11.12.1 Rollback runbook (target < 5 minutes)

1. Confirm the breach is deploy-correlated (a §11.11 runbook step pointed here).
2. Re-point the ArgoCD application to the previous known-good image tag (`git-${PREVIOUS_SHA}`).
3. Verify the broker exposes only `POST /dispatch` post-rollback (INV-01/INV-11 drift guard — a rollback must not reintroduce a named semantic endpoint).
4. Confirm structured-log emission resumes with canonical names (INV-01a/b).
5. Verify the Composite Reliability Score panel returns to its green band.
6. Record the rollback in the incident audit trail.


#### 11.12.2 RC go/no-go checklist (Sep 1 2026)

- [ ] all SLO threshold values set by ACT-JASON (F1-Z1) and panels green
- [ ] Composite Reliability Score above its (TBD) threshold
- [ ] all five F1 launch gates signed with documented evidence (INV-04, §11.8)
- [ ] QA scorecard `pass_rate` meets the (TBD) quality threshold for the final sampling week
- [ ] InfoSec attestation: `cross_tenant_incidents = 0` with test evidence
- [ ] rollback validated under 5 minutes (§11.12.1)
- [ ] every alert annotated with `runbook_url` (INV-07)
- [ ] ACT-JASON records the final GO / NO-GO decision

### 11.13 Key Constraints & Rules

- **Telemetry is per-feature, not a cleanup track.** Each slice ships its log contract with its behavior; otherwise the RC has no go/no-go evidence (INV-04).
- **Canonical field names are a hard contract.** Emitters use the exact F2 names; dashboard owners consume them and SHALL NOT invent metric names (INV-01a/b). An invented name is a silently broken SLO.
- **No member-identifiable data in any log field.** CL9 and the §10 PII/PHI Redactor rules apply to logs (INV-02a/b).
- **`correlation_id` in every event.** Propagated from `x-correlation-id` (INV-06); observability-only, never a security claim (INV-05).
- **Loki-only monitoring stack.** No Prometheus exists in `k8s-argocd`; every SLO is a LogQL derivation, not a Prometheus counter.
- **Grafana shows threshold-colored SLO status, never raw counters** (INV-03); every alert carries a `runbook_url` (INV-07).
- **Grafana and the Analytics app are disjoint surfaces.** Do NOT bolt Loki into the Analytics Next.js app — different query languages, latencies, audiences. Ops monitoring requires zero analytics-app work; a second BI DataSource is added only when needed (YAGNI).
- **ACT-JASON gates on documented evidence.** No gate clears on `"we believe"`/`"probably"` (INV-04); sign-off precedes the Sep 1 2026 RC (SEQ-6).
- **Taxonomy approval precedes dashboard build.** Grace/Syed begin only after ACT-JASON approves the F2 taxonomy + thresholds (SEQ-1, INV-05).

### 11.14 Decisions Still Open

| # | Question | Owner | Why it matters |
|---|---|---|---|
| F1-Z1 | SLO threshold values (all rows in §11.9) | ACT-JASON | blocks all dashboard build + every gate; due Jul 15 |
| F1-Z2 | Gate sign-off owners per category | ACT-JASON | quality/security/privacy/support/rollback ownership; due Aug 31 |
| F1-Z3 | Cost gate threshold | ACT-JASON + finance | sets the Cost-per-Answer SLO comparator |
| F2-Z2 | Answer-quality rubric (criteria/scale/frequency) | ACT-JASON + ACT-QA | defines the QA scorecard `pass_rate` and `rubric_version` |
| F2-Z4 | Composite Reliability Score weights | ACT-JASON | turns the composite shape into a value |
| WI-F3-D | Analytics app multi-tenancy readiness | Pramod + platform | parallel refactor; not blocking emission, but blocks external-customer BI |

## 12. Security & Multi-Tenancy

### Architecture Position

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef identity fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000

    subgraph untrusted["Untrusted zone"]
        ext["External client (SDK / browser)"]:::client
    end

    auth0["Auth0 (stellarus-sb2)"]:::identity

    subgraph edge["Trust boundary"]
        apim["APIM — validates Auth0 JWKS, strips inbound x-* headers"]:::boundary
        ccs["CCS — signs RS256 context token (customer_slug)"]:::boundary
    end

    subgraph aks["Trusted AKS network (Istio mTLS)"]
        direction LR
        broker["agentic-broker-api"]:::backend
        benefits["benefits-service"]:::backend
    end

    convdb[("Per-tenant conversation schema")]:::store
    bendb[("Customer-partitioned benefits Postgres")]:::store

    ext -->|"Bearer JWT (no direct service access)"| apim
    apim -->|"(1) JWKS fetch (cached per iss)"| auth0
    apim -->|"(2) POST /validate/token"| ccs
    ccs -->|"(3) x-context-token (signed, carries customer_slug)"| apim
    apim -->|"(4) x-context-token + fresh x-correlation-id"| broker
    apim --> benefits
    broker -->|"customer_slug -> schema"| convdb
    benefits -->|"customer_slug -> partition"| bendb
```

### Trust Boundaries

| Layer | Trust level | Verification |
|---|---|---|
| External clients (SDK, browser) | Untrusted | Must pass through APIM — no direct service access; only an Auth0 Bearer JWT is accepted |
| APIM | Trust boundary | Validates external Auth0 JWTs against Auth0 JWKS (cached per `iss`); calls CCS `POST /validate/token`; injects `x-context-token` + a fresh `x-correlation-id`; strips any inbound `x-*` trust headers from external callers (D1 INV-04) |
| CCS | Trust issuer | Signs the RS256 context token carrying `customer_slug` and `scopes[]`; does NOT authenticate humans (Auth0 does) |
| Internal AKS services | Trusted network | Istio mTLS verifies service identity service-to-service; `ContextTokenGuard` re-verifies the RS256 signature against CCS JWKS before any claim is trusted (D1 INV-06) |

- APIM **MUST** strip inbound `x-context-token` and `x-correlation-id` from external callers
  and generate its own (D1 SEQ-3, SEQ-4, INV-04). A forged `customer_slug` in an external
  request is the single highest-severity attack against tenant isolation; header-strip at the
  edge is the structural defense.
- Internal services **MUST NOT** trust `customer_slug` from anywhere except a context token
  whose RS256 signature, `iss`, `aud`, and `exp` have been verified by `ContextTokenGuard`
  (D1 INV-06). Network position (being inside AKS) is necessary but not sufficient — mTLS
  proves *which service* is calling, the token proves *which tenant* the request is for.

### Two Token Systems

| Token | Issuer / Signing | Carries | Validated by | Travels as |
|---|---|---|---|---|
| Auth0 access JWT | Auth0 (`stellarus-sb2.us.auth0.com`), PKCE | human identity + `https://stellarus.com/persona` custom claim | APIM (against Auth0 JWKS) | `Authorization: Bearer <jwt>` |
| Context token | CCS, RS256 via `jose` | `iss`, `aud`, `exp`, `iat`, `sub`, `customer_id`, `customer_slug`, `principal_id`, `persona`, `scopes[]`, optional `mode` | `ContextTokenGuard` (against CCS JWKS) | `x-context-token` |

The `customer_slug` claim is the immutable tenant identifier (e.g. `bsca`) extracted from the verified context token, and it is the only value any downstream component may use for tenant scoping.

```mermaid
sequenceDiagram
    participant C as Client
    participant A as APIM
    participant Auth0
    participant CCS
    participant G as ContextTokenGuard

    C->>A: Authorization Bearer (Auth0 JWT)
    A->>A: Extract iss from unverified token
    A->>Auth0: JWKS fetch (cached per iss)
    A->>A: Validate JWT signature, expiry
    A->>A: Strip inbound x-context-token, x-correlation-id
    A->>CCS: POST /validate/token (persona, customer context)
    CCS-->>A: signed context token (customer_slug, scopes)
    A->>A: Inject x-context-token, fresh x-correlation-id (UUIDv4)
    A->>G: x-context-token, x-correlation-id
    G->>G: Verify RS256 against CCS JWKS
    G->>G: Validate iss, aud, exp; attach claims
    G->>G: Enforce RequireScopes(chat)
```

### customer_slug -> Per-Tenant Resolution

```mermaid
flowchart LR
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000

    slug["customer_slug (verified context token)"]:::boundary

    conv["PostgresConversationAdapter"]:::backend
    ben["benefits-service"]:::backend
    rate["RateLimiterService"]:::backend
    ana["analytics app"]:::backend

    convs[("per-tenant conversation schema")]:::store
    bens[("customer-partitioned benefits Postgres")]:::store
    budget[("per-tenant token budget")]:::store
    cache[("tenant-keyed analytics cache + qualifyClaimsTable(tenant)")]:::store

    slug --> conv --> convs
    slug --> ben --> bens
    slug --> rate --> budget
    slug --> ana --> cache
```

| Consumer | Resolution from `customer_slug` | Isolation guarantee | Clause |
|---|---|---|---|
| `PostgresConversationAdapter` | per-tenant Postgres schema | no cross-tenant conversation reads | B1B2 INV-07 |
| `benefits-service` | customer-partitioned Postgres | plan/benefits data partitioned per customer | B1B2 (RestBenefitsAdapter), §6 |
| `RateLimiterService` | per-tenant token-bucket budget | one tenant cannot exhaust another's budget; never keyed on IP or API key alone | B1B2 INV-08 |
| `analytics` app | cache key dimension + `qualifyClaimsTable(tenant)` | per-tenant query + cache isolation (TO-BE — see §12.7) | INPUT 6 §6 |

### Per-Tenant Schema Isolation (Data Model)

```mermaid
erDiagram
    tenant ||--o{ conversation_schema : "owns"
    tenant ||--o{ benefits_partition : "owns"

    tenant {
        text customer_slug PK "immutable tenant id (e.g. bsca)"
        uuid customer_id "from verified context token"
    }
    conversation_schema {
        text customer_slug FK "schema selector"
        uuid session_id "conversation continuity id"
        text role "member | assistant"
        text content "turn content (compressed)"
        timestamptz created_at "turn timestamp"
        text correlation_id "observability only"
    }
    benefits_partition {
        text customer_slug FK "partition selector"
        text plan_id "plan reference"
        jsonb plan_data "governed benefits payload"
        timestamptz updated_at "upsert timestamp"
    }
```

#### conversation_schema (per-tenant)

| Column | Type | Constraints |
|---|---|---|
| `customer_slug` | `text` | NOT NULL — selects the tenant schema; never client-supplied (B1B2 INV-07) |
| `session_id` | `uuid` | NOT NULL — captured from a `session` SSE event, never generated client-side (A1 INV-05) |
| `role` | `text` | NOT NULL, `role IN ('member','assistant')` |
| `content` | `text` | NOT NULL — raw turn content, compressed and indexed; authoritative store, not Sierra native storage (B1B2 INV-06) |
| `created_at` | `timestamptz` | NOT NULL, default `now()` |
| `correlation_id` | `text` | nullable, indexed — observability only, NO security meaning (D1 INV-05) |

#### benefits_partition (customer-partitioned)

| Column | Type | Constraints |
|---|---|---|
| `customer_slug` | `text` | NOT NULL — partition selector |
| `plan_id` | `text` | NOT NULL |
| `plan_data` | `jsonb` | NOT NULL — governed source-of-truth benefits payload |
| `updated_at` | `timestamptz` | NOT NULL — upsert timestamp |

### Analytics Multi-Tenancy — Readiness Verdict

`@stellarus/db` already ships a multi-tenant client. `DbClient` takes `TenantDbConfig[]` — an array of per-tenant Snowflake `driverOptions` (`database` / `schema` / `role`) — and resolves the correct tenant connection at query time. The analytics app did not use it. It chose the `createSingleTenantClient` convenience wrapper instead.

#### The 4 CRITICAL blockers

| ID | Blocker | Consequence |
|---|---|---|
| CRIT-1 | No per-tenant isolation in claims queries | every authenticated user sees ALL tenants' claims |
| CRIT-2 | Hardcoded dev schema | queries pinned to one environment's schema regardless of caller |
| CRIT-3 | Cache key has no tenant dimension | cross-tenant PHI disclosure — tenant A's cached result served to tenant B |
| CRIT-4 | `X-Dashboard-Debug` response header leaks server PID / infra detail | internal infrastructure disclosure to any caller |

#### CRIT-1 / CRIT-2 / CRIT-3 collapse into ONE fix

```mermaid
flowchart TB
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000

    subgraph current["AS-BUILT (broken)"]
        single["createSingleTenantClient wrapper"]:::edge
        hard["hardcoded dev schema"]:::edge
        nocache["tenant-less cache key"]:::edge
        debug["X-Dashboard-Debug header (PID leak)"]:::edge
    end

    subgraph target["TO-BE (MVP / external-ready)"]
        org["Auth0 org_id -> StellarusCustomClaims"]:::boundary
        multi["multi-tenant DbClient(TenantDbConfig[])"]:::backend
        qualify["qualifyClaimsTable(tenant)"]:::backend
        tcache[("tenant-keyed cache")]:::store
    end

    single --> org
    hard --> org
    nocache --> org
    org --> multi --> qualify --> tcache
    debug -.->|"parallel fix: remove header"| target
```

Auth0 Organizations is not wired — a `git grep organization` over the workspace is empty.

**Decision for v1:** defer the analytics external-tenant refactor.

### Credential Handling (CL16)

| Secret | Store | Resolution | Consumer |
|---|---|---|---|
| `ccs-apim-shared-secret` | Azure Key Vault | `DefaultAzureCredential` | APIM <-> CCS internal call |
| Genesys API credentials | Azure Key Vault | `DefaultAzureCredential`, Managed Identity | `GenesysAdapter` only — never env vars (E1E2 INV-07) |
| CCS RS256 signing key | Azure Key Vault | `DefaultAzureCredential` | CCS `TokenService.sign()` |

- Services **MUST** resolve secrets at runtime via `DefaultAzureCredential`. No secret value
  appears in source, test files, CI YAML, k8s manifests, or `.env*` files. Base64 encoding is
  not an exemption — scanners match structure, not semantics.
- `GenesysAdapter` **MUST NOT** read Genesys credentials from environment variables in
  production (E1E2 INV-07).
- Tests **MUST** mock the identity-resolution layer (`MagicMock` / `patch` on the
  `SecretClient` / credential), asserting structure, never a credential value.

### Log Redaction

Logs **MUST NOT** record:

- raw Auth0 access or refresh tokens
- signed `x-context-token` values
- CCS RS256 private-key material
- member-identifiable data — name, DOB, or plan ID beyond an anonymized reference
  (F1F2 INV-02a / INV-02b; CL9 / §10 redactor rules apply)

Logs **MUST** record `customer_slug`, `correlation_id`, `capability`, `latency_ms`, and
`status` using the exact canonical F2 field names (F1F2 INV-01a / INV-01b). `correlation_id`
is observability metadata only and carries no integrity or security meaning (D1 INV-05) — a
log line is never an authorization decision.

### Quality Floor for HIPAA External Use

| Metric | Baseline (as measured) | Required floor |
|---|---|---|
| CQI composite | 34.2 / 100 | L3 |
| Theater rate | 41% | < 10% |
| Branch coverage | 54% | 85% |

**Decision for v1: the floor is a release gate for external GA, not for single-customer MVP.**

### Decision-for-v1 Summary

| Concern | Decision for v1 | Trigger for revisit |
|---|---|---|
| Per-customer tenant-cell isolation (D6) | Deferred — MVP is single-customer (BSC) | a second customer, OR external GA |
| Analytics external-tenant refactor (CRIT-1/2/3 + CRIT-4) | Deferred — run single-tenant | second customer / external GA |
| Auth0 Organizations wiring (`org_id -> StellarusCustomClaims`) | Deferred — first WI of the analytics refactor | analytics multi-tenant exposure |
| Analytics CQI / coverage floor | Gate for external GA, not MVP | external GA |
| Static context-token key fallback | Forbidden in production once ENG-257 lands (D1 INV-12a/b) | ENG-257 merge |

### Key Constraints & Rules

- **`customer_slug` is the single source of tenant scoping.** It is resolved at the APIM/CCS
  boundary, never client-supplied, and is the only value any component may scope data by
  (D1, B1B2 INV-07/INV-08).
- **APIM strips inbound trust headers.** Any external `x-context-token` or `x-correlation-id`
  is discarded and regenerated at the edge (D1 INV-04). This is the structural defense against
  a forged `customer_slug`.
- **`ContextTokenGuard` re-verifies inside the trusted network.** mTLS proves the calling
  service; the RS256 signature proves the tenant. Network position alone never authorizes
  (D1 INV-06).
- **The multi-tenant client already exists.** `@stellarus/db` `DbClient(TenantDbConfig[])` is
  the supported path; `createSingleTenantClient` is the root cause of the analytics
  cross-tenant bug and must not be used for any externally-exposed tenant surface.
- **No credential material in any text file or env var in production.** Azure Key Vault +
  Managed Identity (`DefaultAzureCredential`) is the only approved store (CL16; E1E2 INV-07).
- **No raw tokens, keys, or signed context-tokens in logs.** Operational logs follow the
  deny-list above; conversation payloads follow the §10 redactor (E1E2 INV-01/INV-02).
- **INV-12 — no static-key fallback in production once ENG-257 lands.** The broker and
  benefits-service prefer reachable CCS JWKS keys and MUST NOT fall back to a static
  `CONTEXT_TOKEN_PUBLIC_KEY` in production after ENG-257 completes (D1 INV-12a / INV-12b).

### Decisions Still Open

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 1 | `org_id -> StellarusCustomClaims` wiring (Auth0 Organizations) | Platform / packages/auth | Prerequisite for ALL analytics per-tenant isolation; `git grep organization` is currently empty |
| 2 | `chat` scope persona grants (member + employee, exact grants TBD) | Ketema / CCS migration `0003_chat_scopes.sql` | Gates `@RequireScopes('chat')` on `/dispatch`; IRREVERSIBLE (WI-D1-A) |
| 3 | ENG-257 CCS JWKS endpoint merge | Jordan Ramos | Unblocks production RS256 verification; arms INV-12 static-key prohibition |
| 4 | ENG-286 per-consumer `aud` scoping | Bharath | Today `aud` is the same `stellarus-context-token` for all tokens, permitting cross-service replay |

## 13. Capability Registry & Extensibility

### Architecture Position

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    bff["BFF (agentic-broker-chat)"]:::client
    broker["Thin-Router Broker — POST /dispatch"]:::edge
    resolver["@stellarus/resolver — resolve(capability, customer_slug)"]:::ccs
    yaml[("RESOLVER_CONFIG_DIR (*.yaml)")]:::store
    registry["ADAPTER_CLASS_REGISTRY"]:::boundary
    adapter["DataSourceAdapter instance"]:::backend

    bff -->|"{ capability, payload } + x-context-token + x-correlation-id"| broker
    broker -->|"resolve(capability, slug)"| resolver
    resolver -->|"reads YAML (chokidar hot-reload)"| yaml
    resolver -->|"class name -> implementation"| registry
    resolver -->|"instantiated adapter"| adapter
```

### MVP Capability Registry

| Capability | Adapter class | YAML file | Status | Notes |
|---|---|---|---|---|
| `chat.completion` | `SierraAdapter` (streaming) | `sierra-bsca.yaml` | MVP live (new) | wraps `SierraClientService`; owns SSE, token counting, Sierra circuit breaker (WI-B1-B/C) |
| `benefits.query` | `RestBenefitsAdapter` | `benefits-bsca.yaml` | MVP live (exists) | replaces broker `PlanHandlerService` direct-HTTP path (WI-B1-D); already on `main` |
| `conversation.history` | `PostgresConversationAdapter` | `conversation-bsca.yaml` | MVP live (new) | durable per-tenant Postgres store; authoritative record, not Sierra (INV-06); prerequisite for escalation (WI-B1-E) |
| `escalation.initiate` | `GenesysAdapter` | `genesys-bsca.yaml` | Contract-only (P5/E2) | not wired in broker MVP; owns Genesys circuit breaker; creds from Azure Key Vault (INV-07); only caller of Genesys (INV-05) |

```mermaid
flowchart TB
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    dispatch["POST /dispatch (single endpoint)"]:::edge

    subgraph live["MVP live"]
        direction TB
        chat["chat.completion -> SierraAdapter"]:::backend
        chatY[("sierra-bsca.yaml")]:::store
        ben["benefits.query -> RestBenefitsAdapter"]:::backend
        benY[("benefits-bsca.yaml")]:::store
        conv["conversation.history -> PostgresConversationAdapter"]:::backend
        convY[("conversation-bsca.yaml")]:::store
        chat --- chatY
        ben --- benY
        conv --- convY
    end

    subgraph deferred["Contract-only / deferred"]
        direction TB
        esc["escalation.initiate -> GenesysAdapter"]:::boundary
        escY[("genesys-bsca.yaml")]:::store
        snow["benefits.query (Snowflake) -> SnowflakeBenefitsAdapter"]:::boundary
        snowY[("benefits-bsca-snowflake.yaml")]:::store
        callnum["call.number -> future IVR surface"]:::boundary
        lob["additional LoB benefits adapters"]:::boundary
        esc -.- escY
        snow -.- snowY
    end

    dispatch --> chat
    dispatch --> ben
    dispatch --> conv
    dispatch -.-> esc
    dispatch -.-> snow
    dispatch -.-> callnum
    dispatch -.-> lob
```

### Deferred / Future Capabilities — All YAML-Only Additions

| Capability / variant | Adapter | YAML file | Scope tag | Trigger to build |
|---|---|---|---|---|
| `benefits.query` Snowflake variant | `SnowflakeBenefitsAdapter` (scaffold/stub) | `benefits-bsca-snowflake.yaml` | demo/future | a customer needs Snowflake-backed benefits; v1 is REST-only |
| `call.number` | future IVR adapter | per IVR surface | future (B6) | a phone surface ships via a new BFF, `agentic-broker-ivr` |
| multi-CCaaS generalization | per-CCaaS adapters | per-CCaaS slug set | E5 | a second CCaaS beyond Genesys is contracted |
| additional LoB benefits adapters | per-LoB `*BenefitsAdapter` | per-LoB YAML | C5, Q4 2026 | new lines of business need distinct benefits grounding |
| future multi-agent routing | routing adapters | per-route YAML | B6 | Sierra <-> Foundry <-> Member Agent routing is required |

### Naming Convention

- **Capability string:** `{domain}.{action}` — e.g. `chat.completion`,
  `benefits.query`, `conversation.history`, `escalation.initiate`. No internal
  service name (`sierra`, `genesys`, `broker`) ever appears in the capability
  string; that vocabulary lives only in the adapter class and the YAML.
- **Per-customer YAML registration:** slug-suffixed file names. The first
  customer, Blue Shield of California, uses `customer_slug = bsca`, so its files
  are `*-bsca.yaml` (`sierra-bsca.yaml`, `benefits-bsca.yaml`,
  `conversation-bsca.yaml`). Onboarding a new customer is copying the BSC set to
  `*-{newslug}.yaml`, adapting the per-tenant bindings, and dropping the files.
  Same capabilities, new tenant binding, no code change.

`customer_slug` is the immutable tenant identifier carried in the verified
context token and resolved at the APIM/CCS boundary — never client-supplied. The
resolver scopes every lookup by it (INV-08, INV-07 per-tenant isolation on the
conversation store).

### Per-Customer YAML Onboarding

```mermaid
flowchart TB
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    subgraph bsc["Customer: BSC (customer_slug = bsca)"]
        direction TB
        s1[("sierra-bsca.yaml")]:::store
        b1[("benefits-bsca.yaml")]:::store
        c1[("conversation-bsca.yaml")]:::store
    end

    subgraph newc["New customer (customer_slug = newslug)"]
        direction TB
        s2[("sierra-newslug.yaml")]:::store
        b2[("benefits-newslug.yaml")]:::store
        c2[("conversation-newslug.yaml")]:::store
    end

    copy["copy / adapt per-tenant bindings — NO code change"]:::backend
    note["Same capabilities, new tenant binding (multi-tenant reuse = the moat)"]:::boundary

    bsc --> copy
    copy --> newc
    newc --- note
```

### Mechanism — Resolver, chokidar, ADAPTER_CLASS_REGISTRY

1. **`RESOLVER_CONFIG_DIR`** — the directory holding the per-customer YAML. Each
   file declares a `(capability, customer_slug) → adapter-class-name + per-tenant
   config` binding.
2. **config-loader / chokidar** — the loader watches `RESOLVER_CONFIG_DIR` via
   `chokidar` and hot-reloads on file add/change. Dropping a new YAML registers a
   capability live, without a process restart.
3. **`ADAPTER_CLASS_REGISTRY`** — maps the named adapter class (e.g.
   `SierraAdapter`, `RestBenefitsAdapter`, `PostgresConversationAdapter`,
   `GenesysAdapter`) to its implementation. The YAML names a class; the registry
   resolves the class to code; the resolver instantiates it.

```mermaid
flowchart LR
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef ccs fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    dev["Developer: write adapter + CL12 contract"]:::client
    drop[("drop new YAML in RESOLVER_CONFIG_DIR")]:::store
    chok["chokidar detects change"]:::ccs
    load["config-loader registers via ADAPTER_CLASS_REGISTRY"]:::backend
    live["capability LIVE — ZERO broker code change"]:::backend
    nope["edit broker source"]:::boundary

    dev --> drop
    drop --> chok
    chok --> load
    load --> live
    dev -.->|"INV-03 / INV-11: forbidden, no named endpoint to attach to"| nope
    nope -->|"X rejected at review"| live
```

### Drift Guard (INV-11)

- No semantic endpoint exists to attach a named capability to — `POST /dispatch` takes `{ capability: string, payload: unknown }`; any PR adding a named HTTP endpoint (anything other than `/dispatch`) to `agentic-broker-api` is a detectable contract violation rejected at review (INV-01, INV-11).
- With no semantic endpoint, a new capability has only one place to go: a YAML file (INV-03).

### New-Capability Checklist

- [ ] Adapter implementation written, conforming to `DataSourceAdapter`
      (`query()`) or `StreamingDataSourceAdapter` (`stream(): AsyncIterable<StreamEvent>`),
      with its own downstream circuit breaker owned inside the adapter (INV-09).
- [ ] CL12 contract authored for the adapter
      (`apps/agentic-broker-api/adapters/<name>-adapter.contract.ts`), with
      PRE/POST/INV clauses.
- [ ] YAML registered in `RESOLVER_CONFIG_DIR` binding
      `(capability → adapter class → customer_slug)`, with the class present in
      `ADAPTER_CLASS_REGISTRY`.
- [ ] No broker source changed — `git diff` over `agentic-broker-api/src`
      (excluding the YAML directory) is empty; no new named endpoint added
      (INV-03/INV-11).
- [ ] Resolver picks it up — `resolve(capability, customer_slug)` returns the new
      adapter via chokidar hot-reload; a `/dispatch` call with the new capability
      string dispatches to it (BROKER-B1B2-SEQ-3/4).

### Decisions Still Open / Version Scope

- **Decision for v1: ship three live capabilities + escalation contract-only.**
  `chat.completion`, `benefits.query`, and `conversation.history` are wired and
  resolvable for `bsca`; `escalation.initiate` (GenesysAdapter / `genesys-bsca.yaml`)
  is contract-only in the broker MVP, owned by the P5/E2 escalation slice, and
  blocked on BSC/PTP for Genesys API mechanics (E1-Z1..Z4).
- **Decision for v1: REST-only benefits.** `SnowflakeBenefitsAdapter` /
  `benefits-bsca-snowflake.yaml` is scaffolded-but-stub, demo/future only. v1
  benefits resolve only to `RestBenefitsAdapter`.
- **Deferred: platform onboarding / capability-registry documentation (F5).**
  Formal multi-customer onboarding docs are not authored in v1.

### Key Constraints & Rules

- **A capability is a YAML file, never broker source.** New capability = drop a
  YAML in `RESOLVER_CONFIG_DIR`; broker code does not change (INV-03).
- **Capabilities are opaque to the broker.** The broker never references `chat`,
  `conversation`, `benefits`, or any capability by name in routing logic (INV-02).
- **One endpoint, structurally.** `POST /dispatch` is the only broker endpoint;
  any other named HTTP route is a drift violation rejected at review (INV-01/INV-11).
- **Resolution is per-tenant.** The lookup key is the pair `(capability,
  customer_slug)`; the same capability resolves to different adapters per customer
  via slug-suffixed YAML.
- **Adapters own their downstream.** Circuit breaker and provider-specific logic
  (Sierra token counting, Genesys credentials) live in the adapter, never the
  broker (INV-09, INV-10).
- **The conversation store is authoritative.** `PostgresConversationAdapter` under
  `conversation.history` is the source of truth; Sierra native session storage is
  not (INV-06).

## 14. Deployment & Infrastructure

### Scope

#### In Scope
- Azure deployment topology — APIM edge, AKS + Istio mTLS, `k8s-argocd` GitOps
- component-to-runtime mapping for all five deployables and five shared packages
- secret management via Azure Key Vault + Managed Identity (CL16, zero outbound credential)
- the APIM runtime contract — Auth0 JWT validation, CCS `/validate/token`, header injection and stripping, rate-limit named values
- monitoring topology — Grafana + Loki, no Prometheus
- Docker build conventions (per-app Dockerfile, workspace-root build context, ACR build, tag policy)
- local development without APIM — token minting, `curl` legs, BFF-vs-direct-service calls
- CI/CD — Terraform as source of truth, OIDC federated auth, lower→upper promotion with manual approval gate
- the consolidated platform constraint set and open cross-team decisions

#### Out of Scope
- per-step APIM policy XML logic — owned by the companion APIM tech spec (`docs/customer-config-service/apim-tech-spec.md`)
- CCS data model and token issuance internals — owned by the Customer Configuration Service tech spec
- adapter business logic, contract clauses, and capability semantics — owned by §3–§13
- customer-specific Auth0 tenant/IdP configuration inside Auth0
- Snowflake warehouse provisioning and the analytics-app BI pipeline (referenced, not specified here)

### 14.1 Azure Deployment Topology

```mermaid
flowchart TB
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef identity fill:#ffcc80,stroke:#e65100,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef vault fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    client["Customer surface (SDK in browser)"]:::client
    auth0["Auth0 (stellarus-sb2.us.auth0.com)"]:::identity
    apim["Azure APIM (edge / trust boundary)"]:::edge

    subgraph aks["AKS cluster (Istio mTLS internal identity)"]
        direction TB
        bff["agentic-broker-chat (Next.js BFF)"]:::backend
        broker["agentic-broker-api (NestJS/Fastify broker)"]:::backend
        ccs["customer-configuration-service (CCS)"]:::backend
        benefits["benefits-service (NestJS)"]:::backend
    end

    subgraph mon["Observability sidecar"]
        direction TB
        loki["Loki (monitoring.dev.stellarus.com)"]:::store
        grafana["Grafana (SLO panels)"]:::client
    end

    pg[("PostgreSQL (per-tenant schemas)")]:::store
    snow[("Snowflake (analytics / future benefits)")]:::store
    kv["Azure Key Vault"]:::vault

    sierra["Sierra.ai (external runtime)"]:::identity
    genesys["Genesys Cloud CCaaS (external)"]:::identity

    client -->|"Bearer JWT (Auth0)"| apim
    apim -->|"(1) JWKS fetch (cached per issuer)"| auth0
    apim -.->|"(2) POST /validate/token"| ccs
    apim -->|"(3) x-context-token + x-correlation-id"| bff
    bff -->|"POST /dispatch (capability, payload)"| broker
    broker --> benefits
    benefits --- pg
    broker -.->|"conversation.history persist"| pg
    broker -->|"chat.completion (SSE)"| sierra
    broker -->|"escalation.initiate"| genesys

    bff -.->|"DefaultAzureCredential (Managed Identity)"| kv
    broker -.->|"DefaultAzureCredential (Managed Identity)"| kv
    ccs -.->|"DefaultAzureCredential (Managed Identity)"| kv
    benefits -.->|"DefaultAzureCredential (Managed Identity)"| kv

    benefits --- snow
    broker -->|"structured JSON logs"| loki
    benefits -->|"structured JSON logs"| loki
    loki --> grafana
```

### 14.2 Components & Runtimes

| Component | Type | Runtime | Role | Build status |
|---|---|---|---|---|
| `agentic-broker-api` | app (deployable) | NestJS on Fastify | Thin-Router Broker — exposes only `POST /dispatch`, resolves `(capability, customer_slug)` → adapter (INV-01, INV-11) | as-built (drift to converge — WI-B1-F) |
| `agentic-broker-chat` | app (deployable) | Next.js App Router (Node.js, no edge) | BFF for the BSC member chat surface — owns all semantic routes, acquires context token, dispatches to broker | as-built |
| `customer-configuration-service` | app (deployable) | NestJS | CCS — issues/signs/validates context tokens (RS256 via `jose`), owns scope + persona registry, exposes `/validate/token` and (ENG-257) `/.well-known/jwks.json` | as-built; JWKS to-be-built |
| `benefits-service` | app (deployable) | NestJS | Governed source of truth for plan/benefits data; customer-partitioned Postgres | as-built |
| Grafana + Loki | infra (sidecar) | Loki aggregation + Grafana UI | Operational observability — `monitoring.dev.stellarus.com` | as-built (panels to-be-built — WI-F3-C) |
| `@stellarus/resolver` | package (lib) | TypeScript lib | Maps `(capability, customer_slug)` → `DataSourceAdapter` via YAML in `RESOLVER_CONFIG_DIR` (chokidar hot-reload) | merged to main |
| `@stellarus/auth` | package (lib) | TypeScript lib | Shared `ContextTokenGuard` (`@stellarus/auth/internal/nest`), `InternalContextClaims`, `@RequireScopes()` | as-built |
| `@stellarus/db` | package (lib) | TypeScript lib | Multi-tenant `DbClient` (`TenantDbConfig[]`) — per-tenant Postgres/Snowflake scoping | as-built (analytics threading is CRIT-1/2/3 fix) |
| `@stellarus/chat-client` | package (npm) | TypeScript / React | SDK — `StellarusProvider`, `StellarusClient`, `useChat`, `fetchPlan`; published to customers | v1 surface lock (A1) |
| `@stellarus/redactor` | package (lib) | TypeScript lib | Mandatory PII/PHI redactor — fail-closed scrub before any external transmission (CL15-A) | to-be-built (WI-E2-B, blocker) |

### 14.3 APIM Runtime Contract

APIM owns:
- validating the external Auth0 JWT (signature, expiry) against per-issuer JWKS, cached per issuer
- calling CCS `POST /validate/token` to exchange the validated Auth0 identity for a signed context token (D1 SEQ-1, IP-1)
- injecting `x-context-token` (the signed context-token JWT) and a fresh `x-correlation-id` (UUIDv4) before routing inward (D1 SEQ-3, IP-3)
- stripping any inbound `x-correlation-id` from external callers before injecting its own (D1 SEQ-4, INV-04)
- enforcing rate-limit named values at the edge

APIM does **not** own:
- the customer-resolution rules themselves — CCS is the source of truth for tenant context
- generating, embedding, or trusting `correlation_id` as a security claim — it is observability-only (D1 INV-05)
- per-tenant token-budget rate limiting — that is the broker's `RateLimiterService` operating on the verified `customer_slug` (B1B2 INV-08)

| Header | Direction | Content |
|---|---|---|
| `Authorization: Bearer <jwt>` | inbound (external) | Auth0 access JWT; carries `https://stellarus.com/persona` custom claim |
| `x-correlation-id` (inbound) | stripped | any external value is discarded before injection (INV-04) |
| `x-context-token` | injected (internal) | signed context-token JWT from CCS — `iss`, `aud`, `exp`, `iat`, `sub`, `customer_id`, `customer_slug`, `principal_id`, `persona`, `scopes` (D1 SEQ-2) |
| `x-correlation-id` (injected) | injected (internal) | fresh UUIDv4, one per request (D1 SEQ-3) |

### 14.4 Secret Management (CL16)

```mermaid
flowchart TB
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef vault fill:#80cbc4,stroke:#004d40,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000
    classDef forbidden fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000

    pods["AKS pods (broker, BFF, CCS, benefits)"]:::backend
    cred["DefaultAzureCredential (Managed Identity)"]:::boundary
    kv["Azure Key Vault"]:::vault
    s1["ccs-apim-shared-secret"]:::vault
    s2["genesys-creds"]:::vault
    s3["auth0-config (client id / config)"]:::vault

    forbidden["secret in env var / image layer / text file"]:::forbidden

    pods -->|"resolve at runtime"| cred
    cred -->|"workload identity (no outbound secret)"| kv
    kv --> s1
    kv --> s2
    kv --> s3
    pods -.->|"FORBIDDEN (CL16)"| forbidden
```

| Secret | Key Vault name | Consumer | Notes |
|---|---|---|---|
| APIM→CCS shared secret | `ccs-apim-shared-secret` | APIM, CCS | authenticates the `/validate/token` call |
| Genesys credentials | `genesys-creds` | `GenesysAdapter` only | INV-07 — never from env vars; `GenesysAdapter` is the only reader |
| Auth0 client config | `auth0-config` | CCS, BFF (server-side) | Auth0 domain/audience are internal constants (A1 INV-12) — never customer-configurable |

### 14.5 Monitoring Stack (Loki-only)

Grafana + Loki run at `monitoring.dev.stellarus.com`. Loki is the **only**
metrics-derivation path — there is no Prometheus in `k8s-argocd`. Services emit
structured JSON logs; Grafana derives time-series via LogQL against the Loki
datasource (uid `P8E80F9AEF21F6940`) and renders threshold-colored SLO panels
(green/yellow/red), never raw counters (F1F2 INV-03). Every alert rule is
annotated with `runbook_url` (F1F2 INV-07).

The broker emits `{ event, customer_slug, latency_ms, status, capability, correlation_id }`
on every chat request, error, and circuit-breaker event using exact canonical
F2 field names (F1F2 IP-1, INV-01a); benefits-service emits
`{ event, customer_slug, plan_id, latency_ms, scope, status }` propagating the
same `correlation_id` (F1F2 IP-2, INV-06). Neither service writes
member-identifiable data into log fields (INV-02a/b).

### 14.6 Docker Conventions

```text
az acr build --registry <acr> --file apps/{APP}/Dockerfile \
  --image {APP}:dev-latest --image {APP}:git-${GITHUB_SHA} .
```

Every deployable `docker-build` target publishes **both** `dev-latest` and
`git-${GITHUB_SHA}`; CI enforces this with `tools/validate-docker-build-tags.mjs`.
`next.config.js` never sets `turbopack.root` (silent Docker crashes).

For the NestJS/webpack apps (`agentic-broker-api`, `customer-configuration-service`,
`benefits-service`) the builder stage ends with
`pnpm --filter=@stellarus/{APP} --prod --legacy deploy /prod`, then overlays the
webpack output (`cp -a /app/dist/apps/{APP}/. /prod/`); the runner stage is a
single `COPY --from=builder /prod/ ./`. The runner never runs `pnpm install --prod`
(nests deps under `apps/{APP}/node_modules/` where the bundle can't find `tslib` —
`MODULE_NOT_FOUND`), and never uses `--shamefully-hoist`.

### 14.7 Local Development

**Leg A — through the BFF (surface semantics).** Run `agentic-broker-chat`
locally and call its semantic route with an Auth0 Bearer JWT. The BFF acquires
the context token the same way it does in production; you mint the Auth0 JWT
yourself.

```bash
# Mint an Auth0 access token against the Stellarus sandbox tenant (PKCE or M2M).
# The persona is carried as the https://stellarus.com/persona custom claim.
JWT="$(./tools/dev-mint-auth0-token.sh --persona member --slug bsca)"

# Call the BFF semantic route — BFF translates to a capability and dispatches.
curl -sN http://localhost:3000/api/chat \
  -H "Authorization: Bearer ${JWT}" \
  -H "Content-Type: application/json" \
  -d '{ "message": "what does my plan cover for an MRI?" }'
```

**Leg B — direct to a service (skip the BFF).** To exercise the broker
`POST /dispatch` or `benefits-service` directly, you must supply the
`x-context-token` yourself — APIM is not there to inject it. Mint a context
token locally with the dev CCS signing key, then send it as the header.

```bash
# Mint a context token directly from CCS (dev signing key).
CTX="$(./tools/dev-mint-context-token.sh \
  --persona member --slug bsca --scopes 'chat,benefits:read')"

# Dispatch to the broker — capability-neutral body, context token in header.
curl -sN http://localhost:3001/dispatch \
  -H "x-context-token: ${CTX}" \
  -H "x-correlation-id: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d '{ "capability": "chat.completion", "payload": { "message": "hello" } }'
```

In local mode the broker prefers reachable JWKS keys and falls back to the
static `CONTEXT_TOKEN_PUBLIC_KEY` PEM only on JWKS transport failure. **This
fallback is a local-only allowance.** Once ENG-257 lands, INV-12a/b forbid the
static-key fallback in production. You supply your own `x-correlation-id`
locally because no APIM is present to strip-and-inject it; never assume a
local correlation id has any trust meaning (D1 INV-05).

### 14.8 Infrastructure as Code & CI/CD

**Terraform is the source of truth** for every Azure resource (APIM config,
AKS, Key Vault entries, named values). `k8s-argocd` reconciles cluster state
from Git. CI authenticates to Azure via **OIDC federated credentials** — no
long-lived cloud secret is stored in the pipeline (CL16; secrets injected from
GitHub Actions Secrets only where federation cannot reach).

Promotion runs lower→upper with a human gate between the two tiers.

```mermaid
flowchart LR
    classDef client fill:#90caf9,stroke:#1565c0,stroke-width:2px,color:#000
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    pr["PR (feature branch)"]:::client
    tf["Terraform (source of truth)"]:::edge
    acr["ACR build (dev-latest + git-SHA tags)"]:::store
    argocd["argocd sync (OIDC federated auth)"]:::backend
    lower["dev / qa environment"]:::backend
    gate{{"manual approval gate"}}:::boundary
    upper["stg / prd environment"]:::backend

    pr --> tf
    pr --> acr
    tf --> argocd
    acr --> argocd
    argocd --> lower
    lower --> gate
    gate -->|"human approval"| upper
```

**PR validation checklist** (must pass before merge):
- [ ] `nx affected` build + test + lint + typecheck green for affected projects
- [ ] `tools/validate-docker-build-tags.mjs` confirms both `dev-latest` and `git-${GITHUB_SHA}` published
- [ ] no credential pattern in the diff (credential-security gate, CL16)
- [ ] no new named HTTP endpoint added to `agentic-broker-api` (broker drift guard, B1B2 INV-11)
- [ ] every `project.json` declares its `type:` tag; no cross-app import (module boundaries)
- [ ] Terraform plan reviewed; no out-of-band Azure change
- [ ] OIDC federation used for Azure auth — no static cloud credential in the workflow

### 14.9 Critical-Path Decision Gates

```mermaid
flowchart LR
    classDef edge fill:#ef9a9a,stroke:#b71c1c,stroke-width:2px,color:#000
    classDef backend fill:#a5d6a7,stroke:#1b5e20,stroke-width:2px,color:#000
    classDef store fill:#ce93d8,stroke:#4a148c,stroke-width:2px,color:#000
    classDef boundary fill:#cfd8dc,stroke:#455a64,stroke-width:2px,color:#000

    jun28["Jun 28 — D1 CCS token contract + C1/C2 Benefits LoB (cross-team, blocks everything)"]:::edge
    jun30["Jun 30 — A1 SDK v1 surface lock + B1/B2 broker gap & conversation API"]:::backend
    jul12["Jul 12 — E1 Genesys discovery (API/routing/PII/SLA) + E2 fallback"]:::backend
    jul15["Jul 15 — alpha: SDK v1 + broker /dispatch + token scenarios; F1/F2 taxonomy"]:::store
    sep1["Sep 1 — MVP RC go/no-go"]:::boundary

    jun28 --> jun30
    jun30 --> jul12
    jun30 --> jul15
    jul12 --> jul15
    jul15 --> sep1
```

| Milestone | Date | Owner | Gates downstream |
|---|---|---|---|
| D1 CCS token contract + C1/C2 Benefits LoB coverage | Jun 28 | cross-team (Bharath / Jason / Data+App) | blocks ALL downstream engineering |
| A1 SDK v1 surface lock; B1/B2 broker gap + conversation API | Jun 30 | Ketema | blocks alpha integration |
| E1 Genesys discovery; E2 unavailability fallback | Jul 12 | Julie + BSC/PTP | blocks escalation slice (P5) |
| Alpha — SDK v1 + broker route + token scenarios; F1/F2 taxonomy | Jul 15 | Ketema / Jason | blocks RC telemetry + launch gates |
| MVP RC go/no-go | Sep 1 | Jason | release |

---

### Key Constraints & Rules

- **The broker exposes only `POST /dispatch`.** A capability-neutral router has
  nowhere to accumulate business logic; any named HTTP endpoint on
  `agentic-broker-api` is a detectable contract violation rejected at review
  (B1B2 INV-01/INV-11).
- **CCS is the single source of truth for context tokens.** Only CCS issues,
  signs (RS256), and validates context tokens; no service mints or trusts a
  context token CCS did not sign (D1 INV-03/INV-06).
- **`PostgresConversationAdapter` is the authoritative conversation store.**
  Per-tenant Postgres schema isolation is the durable record; Sierra native
  session storage is never the source of truth (B1B2 INV-06/INV-07).
- **The PII/PHI redactor is mandatory before any external transmission.**
  `@stellarus/redactor` is a fail-closed blocking gate — a scrub failure
  cancels the escalation; unredacted member data reaching Genesys is a HIPAA
  violation (E1E2 INV-01/INV-02, CL15-A).
- **Telemetry is instrumented per-feature with canonical field names.** Each
  service emits exact F2 field names with `correlation_id` on every event; no
  invented metric names, no member-identifiable data in logs (F1F2 INV-01a/b,
  INV-02a/b, INV-06).
- **`customer_slug` drives all tenant scoping.** The immutable slug from the
  verified context token selects the Postgres schema, the benefits partition,
  the rate-limit budget, and the analytics cache key — never client-supplied
  (D1 / B1B2 INV-08).
- **Capabilities are added by YAML, never broker source.** A new capability is
  a dropped YAML file in `RESOLVER_CONFIG_DIR`; modifying broker code to add a
  route is an architectural violation (B1B2 INV-03).
- **No credential in any image, env var, or text file.** Every secret resolves
  at runtime from Azure Key Vault via `DefaultAzureCredential`; Genesys creds in
  particular are read only by `GenesysAdapter`, never from env (CL16, E1E2
  INV-07).

### Decisions Still Open

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 1 | ENG-257 — CCS JWKS endpoint (`/.well-known/jwks.json`) | Jordan Ramos | gates production RS256 verification by broker + benefits; static-key fallback forbidden once it lands (INV-12a/b) |
| 2 | ENG-286 — per-consumer `aud` scoping | Bharath | today `aud` is one constant for all tokens — cross-service replay possible; Phase 1 enforce constant, Phase 2 per-consumer |
| 3 | `chat` scope persona grants + `0003_chat_scopes.sql` | Ketema / Jason | IRREVERSIBLE migration; gates `@RequireScopes('chat')` on `/dispatch` (member + employee grants TBD) |
| 4 | `csr` persona definition | cross-team | BSC CSRs are not Stellarus employees; deferred persona blocks any CSR surface |
| 5 | C1/C2 Benefits LoB coverage matrix + fallback A/B/C | Jason + Data/App + BSC liaison | no manifest yet; blocks benefits grounding accuracy and the Jun 28 gate |
| 6 | E1-Z1..Z4 — Genesys API shape / routing metadata / PII allow-list / SLA | Julie + BSC/PTP | all of escalation (P5) is blocked until Genesys integration mechanics are known |
| 7 | E2-Z2 — SDK behavior when Genesys unavailable | Julie | fallback A/B/C undecided; target Jul 12 |
| 8 | F1-Z1 SLO thresholds + F1-Z2 gate owners + F2 rubric/composite weights | Jason | dashboards cannot be built against undefined metrics; target Jul 15 |
| 9 | Auth0 Organizations / `org_id` wiring | analytics (Pramod + platform) | required for analytics per-tenant isolation; `git grep organization` is currently empty |
| 10 | SDK-INV-14 — Auth0 session lifetime vs healthcare compliance ceiling | platform (A1) | session lifetime must be verified against the compliance ceiling before GA |
| 11 | SDK-UXV-1 — abort/unmount UX on stream cancel | platform (A1) | `ChatAbortError` suppression needs real-world UX observation before ship |

**The single biggest blocking decision is the Jun 28 cross-team gate — D1 (CCS
token contract) plus C1/C2 (Benefits LoB coverage).** Everything downstream
blocks here: the SDK surface, the broker `/dispatch` route, the benefits
grounding, the escalation handoff, and the telemetry taxonomy all depend on the
token contract and the LoB matrix being fixed. If Jun 28 slips, every
downstream slice proceeds on assumptions rather than evidence, and the rework
cost compounds toward the Sep 1 RC.

