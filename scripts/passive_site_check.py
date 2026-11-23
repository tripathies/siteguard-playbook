#!/usr/bin/env python3
"""Bounded, read-only baseline checks for a site you own or may assess.

This is not a vulnerability scanner or penetration test. It does not crawl,
follow redirects, authenticate, submit forms, fuzz inputs, scan ports or exploit.
"""
from __future__ import annotations
import argparse, http.client, ipaddress, json, socket, ssl, sys, urllib.parse
from dataclasses import asdict, dataclass
from html.parser import HTMLParser

USER_AGENT = "SiteGuard-Playbook/1.0 (passive-read-only)"
MAX_BODY = 512_000
TIMEOUT = 8

@dataclass
class Finding:
    check: str
    status: str
    evidence: str
    recommendation: str = ""

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.description = False
        self.noindex = False
        self.canonical = False
        self.ga4 = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title": self.in_title = True
        if tag == "meta":
            name = (a.get("name") or "").lower()
            if name == "description" and a.get("content"): self.description = True
            if name == "robots" and "noindex" in (a.get("content") or "").lower(): self.noindex = True
        if tag == "link" and "canonical" in (a.get("rel") or "").lower(): self.canonical = True
        if tag == "script" and ("googletagmanager.com/gtag/js" in (a.get("src") or "") or "G-" in (a.get("src") or "")): self.ga4 = True
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data.strip()

def validate_url(raw: str):
    if "://" not in raw: raw = "https://" + raw
    p = urllib.parse.urlsplit(raw)
    if p.scheme not in ("http", "https") or not p.hostname: raise ValueError("Use an http(s) URL with a hostname.")
    if p.username or p.password or p.query or p.fragment: raise ValueError("Credentials, query strings and fragments are not accepted.")
    if p.port not in (None, 80, 443): raise ValueError("Only default HTTP/HTTPS ports are allowed.")
    host = p.hostname.encode("idna").decode("ascii").lower()
    try:
        ip = ipaddress.ip_address(host)
        if not ip.is_global: raise ValueError("Non-public IP address is not allowed.")
        raise ValueError("Use a DNS hostname rather than an IP literal.")
    except ValueError as e:
        if str(e).startswith("Non-public") or str(e).startswith("Use a DNS"): raise
    return p._replace(netloc=host)

def resolve_public(host, port):
    rows = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    ips = sorted({r[4][0] for r in rows})
    if not ips: raise ValueError("Hostname did not resolve.")
    for value in ips:
        if not ipaddress.ip_address(value).is_global: raise ValueError("DNS resolved to a non-public address; refusing request.")
    return ips[0]

class PinnedHTTP(http.client.HTTPConnection):
    def __init__(self, host, ip, port, timeout):
        super().__init__(host, port, timeout=timeout); self.ip = ip
    def connect(self): self.sock = socket.create_connection((self.ip, self.port), self.timeout)

class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, host, ip, port, timeout):
        super().__init__(host, port, timeout=timeout, context=ssl.create_default_context()); self.ip = ip
    def connect(self):
        raw = socket.create_connection((self.ip, self.port), self.timeout)
        self.sock = self._context.wrap_socket(raw, server_hostname=self.host)

def get(url):
    p = validate_url(url); host = p.hostname; port = 443 if p.scheme == "https" else 80
    ip = resolve_public(host, port)
    cls = PinnedHTTPS if p.scheme == "https" else PinnedHTTP
    conn = cls(host, ip, port, TIMEOUT)
    path = urllib.parse.urlunsplit(("", "", p.path or "/", "", ""))
    try:
        conn.request("GET", path, headers={"Host": host, "User-Agent": USER_AGENT, "Accept": "text/html,application/xml,text/plain"})
        res = conn.getresponse()
        body = res.read(MAX_BODY + 1)[:MAX_BODY]
        return res.status, {k.lower(): v for k, v in res.getheaders()}, body
    finally: conn.close()

def assess(url):
    findings = []
    status, headers, body = get(url)
    p = validate_url(url)
    findings.append(Finding("HTTPS", "PASS" if p.scheme == "https" else "FAIL", f"URL scheme: {p.scheme}", "Serve the entire site over HTTPS and redirect HTTP to HTTPS."))
    for h, label in [("content-security-policy","CSP"),("strict-transport-security","HSTS"),("x-content-type-options","X-Content-Type-Options"),("referrer-policy","Referrer-Policy"),("permissions-policy","Permissions-Policy")]:
        findings.append(Finding(label, "OBSERVED" if h in headers else "NOT OBSERVED", headers.get(h, "Header absent; review against application needs.")))
    for cookie in [v for k,v in headers.items() if k == "set-cookie"]:
        low = cookie.lower()
        findings.append(Finding("Cookie flags", "REVIEW", cookie.split(";",1)[0] + "; Secure=" + str("secure" in low) + "; HttpOnly=" + str("httponly" in low) + "; SameSite=" + str("samesite" in low)))
    if "text/html" in headers.get("content-type","").lower():
        parser = MetaParser(); parser.feed(body.decode("utf-8","replace"))
        findings.extend([
            Finding("HTML title", "PASS" if parser.title else "NOT OBSERVED", parser.title or "No title found."),
            Finding("Meta description", "PASS" if parser.description else "NOT OBSERVED", str(parser.description)),
            Finding("Meta noindex", "REVIEW" if parser.noindex else "NOT OBSERVED", str(parser.noindex), "Confirm intended indexability; also inspect X-Robots-Tag."),
            Finding("Canonical link", "OBSERVED" if parser.canonical else "NOT OBSERVED", str(parser.canonical)),
            Finding("GA4 marker", "OBSERVED" if parser.ga4 else "NOT OBSERVED", "Client-side marker only; does not prove account ownership or event collection.")
        ])
    for path in ("/robots.txt", "/sitemap.xml"):
        try:
            s, h, b = get(urllib.parse.urlunsplit((p.scheme,p.netloc,path,"","")))
            findings.append(Finding(path, "PASS" if s == 200 else "REVIEW", f"HTTP {s}; content-type={h.get('content-type','unknown')}; bytes={len(b)}"))
        except Exception as e: findings.append(Finding(path, "ERROR", str(e)))
    return {"target": p.geturl(), "http_status": status, "checks": [asdict(f) for f in findings],
            "limitations": ["Passive baseline only; no crawling, auth, redirects, exploit tests or private application verification."]}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url"); ap.add_argument("--i-own-or-have-permission", action="store_true", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try: result = assess(args.url)
    except Exception as exc: print(f"Refused or failed safely: {exc}", file=sys.stderr); return 2
    print(json.dumps(result, indent=2) if args.json else "\n".join(f"{x['check']}: {x['status']} — {x['evidence']}" for x in result["checks"]))
    return 0
if __name__ == "__main__": raise SystemExit(main())
