# Security policy and safe use

This repository contains an educational checklist and a small passive baseline utility; it is not a managed scanning service.

- Assess only domains and systems you own or have explicit written permission to assess.
- Define scope, test window, routes, environments, test accounts and exclusions.
- The utility makes bounded read-only GET requests, does not follow redirects, authenticate, crawl, fuzz or exploit.
- Do not use it as a public multi-tenant URL scanner without additional SSRF controls, isolation, abuse prevention and operational safeguards.
- Never test DoS, request smuggling, destructive payloads or private-network access against third-party production systems.
- Do not publish secrets, tokens, cookies, personal data or exploitable details in public issues. Use private vulnerability reporting where enabled.
