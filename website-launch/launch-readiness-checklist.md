# Website Launch Readiness — 16-point checklist

Use this before public launch and after material domain, hosting or content changes. Record evidence, owner and date for every item.

| # | Launch area | What to implement | How to verify |
|---:|---|---|---|
| 01 | Domain and DNS | Correct A/AAAA/CNAME records; remove stale and dangling records. | Query authoritative DNS and compare with hosting provider. |
| 02 | HTTPS and TLS | Valid certificate, renewal monitoring and HTTP-to-HTTPS redirect. | Browser and TLS inspection; test renewal ownership. |
| 03 | robots.txt | Publish deliberate crawler instructions at the origin root. | GET /robots.txt; review rules against intended public content. |
| 04 | sitemap.xml | Publish canonical, absolute URLs for indexable pages. | GET /sitemap.xml; validate XML and URL responses. |
| 05 | Indexability | No accidental noindex, password wall or crawler block on intended public pages. | Inspect meta robots, X-Robots-Tag and Search Console URL Inspection. |
| 06 | Google Search Console | Verify domain/property ownership and submit sitemap. | Confirm verified property and successful sitemap processing. |
| 07 | Analytics (GA4) | Configure measurement ID, events and internal-traffic rules. | Realtime/DebugView test with consent state respected. |
| 08 | Privacy and consent | Publish privacy/cookie information and implement consent where required. | Test accept, reject, withdraw and persistence behaviour; review local law. |
| 09 | SEO metadata | Unique titles/descriptions, canonical URLs, social metadata and structured data where appropriate. | Inspect rendered HTML and rich-result validation. |
| 10 | Content and navigation | Working links, clear contact details, useful 404 and no placeholder content. | Crawl owned site with an approved link checker and manual review. |
| 11 | Accessibility | Semantic structure, keyboard access, labels, focus, contrast and alt text. | Automated audit plus manual keyboard and screen-reader spot checks. |
| 12 | Performance | Optimized images/fonts, caching, compression and Core Web Vitals. | Lighthouse and field data where available. |
| 13 | Email/domain reputation | SPF, DKIM and DMARC aligned to actual mail senders. | DNS inspection and test-message authentication headers. |
| 14 | Security headers | CSP, HSTS, nosniff, Referrer-Policy and framing policy. | Inspect production response headers and test compatibility. |
| 15 | Monitoring and support | Uptime, error, certificate and security alerts; clear owner and escalation. | Trigger a test alert and confirm delivery/runbook. |
| 16 | Backup and rollback | Tested backup/restore, deployment rollback and recovery owner. | Restore into a separate environment and record recovery time. |

## Important distinctions
- `robots.txt` is a crawler instruction, **not** access control. Never rely on it to hide admin pages, private URLs or sensitive files.
- A sitemap helps discovery; it does not guarantee indexing or ranking.
- Search Console verification and GA4 configuration require account-owner access. A public HTTP check cannot confirm them.
- Analytics tags should not be treated as proof that consent or privacy obligations are satisfied.
- Google indexing is a process, not a switch: discovery, crawl eligibility, canonical selection and indexing are separate.

## Launch decision
Do not mark the site launch-ready based only on a scanner. Require named owners, evidence for manual controls, tested rollback and an explicit go/no-go decision.
