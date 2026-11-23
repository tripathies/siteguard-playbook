# SiteGuard Playbook

**Don't just ship. Secure what you build.**

A practical, evidence-led framework for assessing websites and web applications, including AI-assisted and vibe-coded projects. It has two gates:

## 1. Website Security
Use [the 25-point security checklist](website-security/25-point-checklist.md) to review identity, authorization, input handling, APIs, infrastructure, cryptography, data protection, supply chain and monitoring. Controls are conditional: mark them Not Applicable only when the feature is confirmed absent.

## 2. Website Launch Readiness
Use [the launch checklist](website-launch/launch-readiness-checklist.md) for domain/DNS, TLS, robots.txt, sitemap, Google Search Console, analytics, SEO, privacy, accessibility, performance, backups and operations.

## Quick start
Python 3.10+, standard library only:
```bash
python scripts/passive_site_check.py https://example.com --i-own-or-have-permission --json
python -m unittest discover -s tests -v
```
The checker makes a few bounded, read-only GET requests to the supplied origin, /robots.txt and /sitemap.xml. It does not crawl, authenticate, submit forms, follow redirects, fuzz, exploit, scan ports or test private application logic. It is not a penetration test or certification.

## Finding statuses
- **PASS** — test executed and evidence meets expectation.
- **FAIL** — test demonstrated a control gap.
- **NEEDS MANUAL VERIFICATION** — public observation cannot establish the control.
- **NOT TESTED** — no test performed.
- **NOT APPLICABLE** — confirmed outside the system's technology or feature scope.

Keep severity, confidence and status separate. Missing a header does not automatically prove an exploitable vulnerability. Never present an unexplained single security score.

## Safety boundaries
Assess only systems you own or have written permission to test. Define hostnames, routes, environment, test accounts, time window and exclusions. Run active testing only in approved staging environments. Never put credentials, tokens, cookies, personal data or private keys in reports. Do not perform DoS, request-smuggling, destructive or private-network tests against third-party production systems.

## Repository map
- `website-security/` — 25 security controls and verification notes.
- `website-launch/` — launch and discoverability checklist.
- `scripts/` — passive baseline checker.
- `tests/` — unit tests.
- `examples/` — finding template.
- `REFERENCES.md` — primary standards and vendor documentation.
- `AI-SECURITY-REVIEW-PROMPT.md` — source-code review prompt.
- `SECURITY.md` — safe-use and reporting policy.

This independent resource is not an OWASP, NIST, Google or Microsoft product or certification. See [licensing](LICENSE) and [references](REFERENCES.md).
