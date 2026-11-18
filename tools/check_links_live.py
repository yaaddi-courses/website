"""Check every external link on the site against the live web.

For each distinct http(s) link it follows redirects and reports the status, the redirect chain, the
final URL and the final page title, next to the link text and the pages that use it. A link fails when
the final status is an error. A redirect that changes host or path is flagged for a human (or the
website-review skill) to judge whether the destination is what the link text promises.

Run from the Website folder:   python tools/check_links_live.py
Options:  --json            machine-readable output
Exit code 1 when any link is broken. Needs network access. Uses only the standard library.
"""
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (compatible; yaaddi-site-review/1.0)"
MAX_HOPS = 8
BOT_BLOCKED = {999}  # LinkedIn answers bots with 999; open those links by hand


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.found, self._href, self._text = [], None, ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._href, self._text = dict(attrs).get("href"), ""

    def handle_data(self, data):
        if self._href is not None:
            self._text += data

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.found.append((self._href, re.sub(r"\s+", " ", self._text).strip()))
            self._href = None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with OPENER.open(req, timeout=20) as r:
            return r.status, dict(r.headers), r.read(200_000)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), b""
    except Exception as e:  # network errors are reported, not raised
        return 0, {"error": str(e)}, b""


def title_of(body):
    m = re.search(rb"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    return re.sub(r"\s+", " ", m.group(1).decode("utf-8", "replace")).strip() if m else ""


def normalize(url):
    p = urlparse(url)
    return (p.netloc.lower().removeprefix("www."), p.path.rstrip("/") or "/")


def classify(start, final, status):
    """Return 'broken', 'unverified' (site blocks bots), 'moved' (host or path changed) or 'ok'."""
    if status in BOT_BLOCKED:
        return "unverified"
    if status == 0 or status >= 400:
        return "broken"
    return "ok" if normalize(start) == normalize(final) else "moved"


def follow(url):
    chain, current = [], url
    for _ in range(MAX_HOPS):
        status, headers, body = fetch(current)
        if status in (301, 302, 303, 307, 308) and headers.get("Location"):
            nxt = urljoin(current, headers["Location"])
            chain.append((status, nxt))
            current = nxt
            continue
        return {"status": status, "final": current, "chain": chain, "title": title_of(body), "error": headers.get("error", "")}
    return {"status": 0, "final": current, "chain": chain, "title": "", "error": "too many redirects"}


def collect():
    uses = {}
    for page in sorted(ROOT.rglob("*.html")):
        if "tools" in page.parts or ".git" in page.parts:
            continue
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for href, text in parser.found:
            if urlparse(href).scheme in ("http", "https"):
                uses.setdefault(urldefrag(href)[0], []).append((page.relative_to(ROOT).as_posix(), text))
    return uses


def main():
    results = []
    for url, where in collect().items():
        r = follow(url)
        r.update(url=url, verdict=classify(url, r["final"], r["status"]),
                 texts=sorted({t for _, t in where if t}), pages=sorted({p for p, _ in where}))
        results.append(r)
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
    else:
        for r in sorted(results, key=lambda r: r["verdict"]):
            flag = {"ok": "OK    ", "moved": "MOVED ", "broken": "BROKEN", "unverified": "MANUAL"}[r["verdict"]]
            print(f"{flag} {r['status']} {r['url']}")
            if r["verdict"] == "ok":
                print(f"       title: {r['title']!r}   link text: {r['texts']}")
            else:
                print(f"       -> {r['final']}   title: {r['title']!r}   {r['error']}")
                print(f"       link text: {r['texts']}   used on: {', '.join(r['pages'][:4])}")
        bad = sum(r["verdict"] == "broken" for r in results)
        moved = sum(r["verdict"] == "moved" for r in results)
        manual = sum(r["verdict"] == "unverified" for r in results)
        print(f"{len(results)} links, {bad} broken, {moved} redirected to a different page, {manual} to open by hand")
    return 1 if any(r["verdict"] == "broken" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
