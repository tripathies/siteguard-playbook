# Website Security — 25-point checklist

For each control record: applicability, scope, test method, evidence, status, severity, owner, remediation and retest. Use a test tenant and staging environment for active tests.

| # | Control | What to implement | Verification |
|---:|---|---|---|
| 01 | OAuth/OIDC/SAML | Validate signature, issuer, audience, redirect URI, state, nonce and claims. | Negative auth tests; replay and redirect validation in staging. |
| 02 | MFA / 2FA | Single-use OTP/recovery codes, throttling and secure recovery. | Reuse a test OTP; verify rejection and rate limits. |
| 03 | JWT / sessions | Pin allowed algorithms; validate issuer, audience, expiry; rotate/revoke sessions. | Test tampered, expired, wrong-audience and revoked test tokens. |
| 04 | Authorization / IDOR / BOLA | Enforce object- and tenant-level authorization server-side on every operation. | Cross-user and cross-tenant access matrix. |
| 05 | Input / Unicode identity | Normalize consistently; enforce length and uniqueness after canonicalization. | Test Unicode confusables, normalization variants and boundary lengths. |
| 06 | Injection | Parameterized queries; avoid shell concatenation and unsafe interpreters. | SAST, code review and safe staging negative tests. |
| 07 | XSS / template injection | Contextual output encoding; sanitize allowed rich text; avoid unsafe template evaluation. | Review sinks and test stored/reflected/DOM cases in staging. |
| 08 | CSRF / CORS | CSRF defenses for cookie-authenticated mutations; explicit trusted origins. | Cross-origin negative tests and cookie review. |
| 09 | SSRF | Restrict URL fetches; block loopback, private, link-local and metadata ranges; re-check redirects and DNS. | Unit tests with mocked DNS and controlled staging endpoints. |
| 10 | File uploads | Validate content signature, type, size and storage isolation; malware scan where appropriate. | Upload benign invalid-type and oversized fixtures; verify rejection. |
| 11 | DoS / resource exhaustion | Edge protection, quotas, concurrency caps, body limits and timeouts. | Review WAF/CDN configuration; load test only with written scope. |
| 12 | GraphQL | Bound depth, complexity, aliases, batching and pagination; authorize resolvers. | Query-limit and resolver authorization tests. |
| 13 | ReDoS | Avoid catastrophic regex patterns; bound input and execution. | Static review and bounded worst-case tests. |
| 14 | HTTP request smuggling | Ensure CDN, proxy and origin parse framing consistently; patch edge components. | Vendor configuration review and approved staging assessment only. |
| 15 | Proxy/IP headers | Trust forwarding headers only from known proxies; derive client identity at edge. | Spoof headers in staging; verify application ignores untrusted values. |
| 16 | Cache poisoning/leakage | Correct cache keys; do not shared-cache personalized responses; control Vary and cache directives. | Compare responses across test users and header variants. |
| 17 | Timing / cryptography / padding oracle | CSPRNG for secrets; vetted crypto; constant-time secret comparison; uniform error handling. | Code review and crypto-library tests; avoid timing claims from casual probes. |
| 18 | Prototype pollution / deserialization | Validate object shape; avoid unsafe merges and untrusted deserialization. | Static review and safe unit fixtures. |
| 19 | XXE | Disable external entities and unsafe DTD resolution where XML is parsed. | Parser configuration review and benign local XML fixtures. |
| 20 | WebSocket security | Authenticate handshake; validate Origin; authorize each message; bound payload and connection count. | Origin/auth/message authorization tests in staging. |
| 21 | Security headers | Intentional CSP, HSTS, nosniff, framing, Referrer-Policy and Permissions-Policy. | Inspect headers and validate browser behaviour; presence alone is not proof. |
| 22 | TLS / DNS / domain | Valid TLS, HTTPS redirect, renewal, CAA, registrar MFA/lock and no dangling records. | TLS/DNS inspection and account-owner evidence. |
| 23 | Data / database security | Least privilege, tenant isolation, encryption, retention and managed identity where supported. | Permission review and cross-tenant tests. |
| 24 | Secrets / supply chain / CI | Secret scanning, dependency updates, pinned actions, least-privilege workflow tokens and protected deploys. | Repository settings, CI logs and dependency/SBOM review. |
| 25 | Logging / monitoring / recovery | Alert on security events; redact secrets; protect logs; test backup restoration and incident playbooks. | Alert exercise, restore drill and runbook evidence. |

## Important applicability notes
SAML, GraphQL, XML, WebSockets and file uploads apply only when those features exist. A 52-character username is not inherently a vulnerability; inconsistent normalization/uniqueness is the risk. RLS bypass is database-specific, not a universal web-app check. HTTP/2 Rapid Reset is an infrastructure/edge concern. A passive scan cannot prove authentication, authorization, database isolation, cryptographic correctness or backup recoverability.

## Record each result
Use `examples/finding-template.md`. Distinguish **PASS**, **FAIL**, **NEEDS MANUAL VERIFICATION**, **NOT TESTED** and **NOT APPLICABLE**. Keep severity and confidence separate.
