# Contributing

1. Describe the control, affected technology and primary source reference.
2. Make every check testable: precondition, method, expected result and remediation.
3. Label conditional controls clearly (for example, GraphQL only when GraphQL is deployed).
4. Use local fixtures or an explicitly authorised staging environment; do not add third-party production exploit instructions.
5. Add or update unit tests for code changes.
6. Keep dependencies minimal and pin GitHub Actions to reviewed immutable commit SHAs.
7. Never commit credentials, real customer data, production logs or private endpoints.
8. Explain limitations. Do not claim a passive check proves a control that requires authenticated or source-level evidence.
