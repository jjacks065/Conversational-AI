# DemoProxy Protocol Discovery

## Purpose

This document is the Phase 1 discovery ledger for the local response-transformation proxy. It separates facts supported by repository evidence from assumptions that must not enter proxy configuration or matching logic.

## Scope decisions

- `DemoProxy/` is the project root and containment boundary for all implementation artifacts.
- GitHub workflows and CI integration are excluded from this build.
- The forward-proxy/PAC design is confirmed because the Nexus web application cannot use a configurable API base URL.
- Streaming support will not be implemented unless a real capture confirms SSE or WebSocket traffic.

## Discovery status

| Required fact | Status | Current finding | Evidence or confirmation needed |
| --- | --- | --- | --- |
| Target hostname | Confirmed | `app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net`, using HTTPS on the implicit port `443`. | Supplied Chrome request capture. |
| Endpoint/path | Confirmed | `/api/chatbot/ask`, with no query string in the supplied capture. The strict path expression is `^/api/chatbot/ask$`. | Supplied Chrome request capture. |
| HTTP method | Confirmed | `POST`. | Supplied Chrome request capture. |
| Request marker | Confirmed | Use the browser-controlled `Origin` header with the exact value `https://nexus-cloud-web-stg.bsc.bscal.com`. The matching layer may also require the exact staging `Referer` as defense in depth. Do not match platform-specific client hints or user-agent text. | Supplied Chrome request capture. |
| Response schema | Confirmed | A supplied live response is a JSON object with required string fields `questionId`, `sessionId`, `content`, and `responseId`. Markdown presentation content is held in `content`. | Supplied sanitized structural observation of a live response body. |
| Response content type | Confirmed | `application/json; charset=utf-8`. Matching must compare the normalized media type (`application/json`) while allowing parameters such as `charset`. | Supplied live response headers. |
| Response status | Confirmed | `200 OK` for the captured successful interaction. Matching does not depend on a successful status; non-success responses must remain unchanged and fail open. | Supplied Chrome request details. |
| JSON/SSE/WebSocket | Confirmed | The observed interaction returns one complete JSON response document. SSE and WebSocket support are not required for the captured protocol and remain out of scope unless later evidence changes the protocol. | Supplied live response body. |
| Compression | Confirmed | No `Content-Encoding` header is present in the supplied response headers, so this captured response uses identity/uncompressed representation. The implementation must still fail open for unsupported encodings. | Supplied live response headers. |
| HTTP version | Confirmed | `HTTP/1.1`. The proxy must not make transformation behavior depend on protocol version. | User-provided Chrome Protocol value. |
| Client | Confirmed | The capture was copied from Google Chrome on macOS and originated from the Nexus staging web application. Proxy matching must remain platform-neutral so the equivalent Windows Chrome request also matches. | Supplied Chrome request capture. |
| Certificate pinning | Confirmed boundary | The caller is a Chrome-hosted web application, not a native client with an application certificate-pinning layer. HSTS is present but is not certificate pinning. Acceptance of the generated local CA remains a required runtime trust test; no pinning bypass will be attempted. | Browser architecture and supplied headers; runtime trust validation remains required. |
| Routing model | Confirmed | The Nexus API base URL is not configurable, so use the selective PAC/forward-proxy design rather than the reverse-proxy alternative. | User confirmation. |

## Confirmed request contract

```text
POST https://app-prdsrch-npn-to-bncp-cus-452.azurewebsites.net/api/chatbot/ask
Accept: application/json
Content-Type: application/json
Origin: https://nexus-cloud-web-stg.bsc.bscal.com
```

The JSON request body has the following sanitized structural contract:

```json
{
  "message": "string",
  "userName": "string",
  "userId": "string",
  "sessionId": "string",
  "facetsProductId": "string",
  "effectiveDate": "YYYYMMDD string",
  "questionId": "string"
}
```

The proxy must forward the request bytes and headers without modification. Request bodies and the `authorization` header are sensitive and must never be logged. The platform-specific `sec-ch-ua-platform`, browser-version client hints, and `user-agent` are deliberately excluded from matching so the same rule works on Windows and macOS.

## Confirmed request-header behavior

- Use exact host, port, method, path, normalized request media type, and exact `Origin` for eligibility matching.
- Optionally require the exact staging `Referer` as an additional stable browser-origin check.
- Forward `Authorization`, `Accept-Encoding`, cookies, browser client hints, priority, user-agent, and every unknown request header without modification.
- Never match on or log bearer values, content length, browser version, operating-system hints, user-agent, or request body content.
- Do not recalculate or rewrite request representation headers because the request body is never transformed.

## Confirmed response contract for fixture-driven work

```json
{
  "questionId": "string",
  "sessionId": "string",
  "content": "markdown string",
  "responseId": "string"
}
```

The transformer may target only the `content` value. It must preserve the three identifier fields and every unknown field exactly, must not invent factual content, and must remain deterministic and idempotent.

## Confirmed response-header behavior

- Match `Content-Type` by normalized media type and accept the confirmed `charset=utf-8` parameter.
- Preserve repeated `Set-Cookie` headers exactly; never coalesce them into one header.
- Never log cookie values, affinity tokens, trace identifiers, authorization data, or response bodies.
- Preserve CORS, HSTS, server, trace, date, and unknown response headers unless mitmproxy must recalculate representation metadata after a body change.
- After transformation, allow the proxy response API to recalculate stale `Content-Length` metadata. The captured response has no `Content-Encoding`, so decompression is not needed for this observed path.

## Deferred operational validation

Protocol discovery is complete. The first runnable proxy must still validate operational assumptions that cannot be proven from a direct browser capture:

1. Chrome accepts the per-machine mitmproxy CA after installation in the intended user trust store.
2. The target request succeeds through the selective PAC route on both Windows and macOS.
3. Emergency disable restores direct raw-API behavior without depending on proxy health.

Do not store an unsanitized HAR, credentials, cookies, tokens, prompts, member data, or production response content in this project.

## Phase 1 exit gate

**Status: COMPLETE.** Host, port, method, path, request marker, request and response media types, response schema, buffered JSON transport, compression behavior, HTTP version, client, routing model, and certificate-pinning boundary are confirmed. Phase 2 may use these values without placeholder hostnames, paths, headers, or transport assumptions.
