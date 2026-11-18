"""Check the site before pushing: SEO basics, links, images, structured data, CSP and the sitemap.

Run from the Website folder:   python tools/check_site.py
Exits with 1 when any check fails. Warnings do not fail the run.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_help import CSP, SITE, stale  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
errors, warnings = [], []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta, self.links, self.refs, self.h1, self.jsonld = {}, [], [], 0, []
        self.imgs_without_alt = []
        self.short_alts = []
        self.headings = []
        self._ld = False
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property") or a.get("http-equiv")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "link":
            self.links.append(a)
            if a.get("href"):
                self.refs.append(a["href"])
        elif tag == "a" and a.get("href"):
            self.refs.append(a["href"])
        elif tag in ("img", "script") and a.get("src"):
            self.refs.append(a["src"])
            if tag == "img" and "alt" not in a:
                self.imgs_without_alt.append(a["src"])
            elif tag == "img" and a["alt"] and len(a["alt"]) < 25:
                self.short_alts.append(a["src"])
        elif tag == "h1":
            self.h1 += 1
        if tag in ("h1", "h2", "h3", "h4"):
            self.headings.append(int(tag[1]))
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True
            self.jsonld.append("")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._ld:
            self.jsonld[-1] += data


def fail(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def target_for(page_path, ref):
    ref = unquote(urldefrag(ref)[0])
    if ref.startswith("/"):
        candidate = ROOT / ref.lstrip("/")
    else:
        candidate = (page_path.parent / ref).resolve()
    return candidate / "index.html" if candidate.is_dir() else candidate


def main():
    for rel in stale():
        fail(f"{rel} is out of date with tools/help_content.py or build_help.py: run python tools/build_help.py")
    pages = sorted(p for p in ROOT.rglob("*.html") if "tools" not in p.parts and ".git" not in p.parts)
    titles, descs, canonicals = {}, {}, {}
    parsed = {}
    for path in pages:
        rel = path.relative_to(ROOT).as_posix()
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        parsed[path] = page
        indexable = "noindex" not in page.meta.get("robots", "")
        if page.meta.get("Content-Security-Policy") != CSP:
            fail(f"{rel}: CSP differs from build_help.CSP")
        if page.h1 != 1:
            fail(f"{rel}: expected one h1, found {page.h1}")
        if page.imgs_without_alt:
            fail(f"{rel}: images without alt: {page.imgs_without_alt}")
        if page.short_alts:
            warn(f"{rel}: very short alt text (describe the picture) on {page.short_alts}")
        for before, after in zip(page.headings, page.headings[1:]):
            if after > before + 1:
                warn(f"{rel}: heading level jumps from h{before} to h{after}")
                break
        for raw in page.jsonld:
            try:
                json.loads(raw)
            except ValueError as e:
                fail(f"{rel}: invalid JSON-LD ({e})")
        if not indexable:
            continue
        title, desc = page.title.strip(), page.meta.get("description", "")
        if not title:
            fail(f"{rel}: missing title")
        elif len(title) > 70:
            warn(f"{rel}: title is {len(title)} characters (aim for 70 or fewer)")
        if not 50 <= len(desc) <= 165:
            warn(f"{rel}: description is {len(desc)} characters (aim for 50-165)")
        if title in titles:
            fail(f"{rel}: duplicate title with {titles[title]}")
        if desc in descs:
            fail(f"{rel}: duplicate description with {descs[desc]}")
        titles[title], descs[desc] = rel, rel
        canon = next((l["href"] for l in page.links if l.get("rel") == "canonical"), None)
        expected = SITE + "/" + ("" if rel == "index.html" else rel.removesuffix("index.html"))
        if canon != expected:
            fail(f"{rel}: canonical {canon!r} should be {expected!r}")
        canonicals[canon] = rel
        for key in ("og:title", "og:description", "og:url", "og:image", "twitter:card"):
            if key not in page.meta:
                fail(f"{rel}: missing {key}")

    # Internal links and assets must exist (external and mailto links are skipped).
    for path, page in parsed.items():
        rel = path.relative_to(ROOT).as_posix()
        for ref in page.refs:
            parsed_url = urlparse(ref)
            if parsed_url.scheme in ("http", "https", "mailto", "data") or ref.startswith("#") or not ref:
                if parsed_url.scheme == "http":
                    fail(f"{rel}: insecure link {ref}")
                continue
            if not target_for(path, ref).exists():
                fail(f"{rel}: broken link {ref}")
        for ref in page.refs:
            if "#" in ref and urlparse(ref).scheme == "" and not ref.startswith("#"):
                base, frag = ref.split("#", 1)
                other = target_for(path, base or ".") if base else path
                if other in parsed and frag and frag not in parsed[other].ids:
                    fail(f"{rel}: link {ref} points to a missing anchor")

    # The sitemap must list exactly the indexable pages.
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    listed = set(re.findall(r"<loc>([^<]+)</loc>", sitemap))
    missing, extra = set(canonicals) - listed, listed - set(canonicals)
    if missing:
        fail(f"sitemap.xml is missing {sorted(missing)}")
    if extra:
        fail(f"sitemap.xml lists unknown pages {sorted(extra)}")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    for url in canonicals:
        if "/help/" in url and url != SITE + "/help/" and url not in llms:
            fail(f"llms.txt does not list {url}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "Sitemap: " + SITE + "/sitemap.xml" not in robots:
        fail("robots.txt does not point to the sitemap")

    ga = re.search(r"var GA_ID = '([^']*)'", (ROOT / "assets" / "analytics.js").read_text(encoding="utf-8"))
    if not ga:
        fail("analytics.js: GA_ID line not found")
    elif ga.group(1) and not re.fullmatch(r"G-[A-Z0-9]{6,}", ga.group(1)):
        fail(f"analytics.js: GA_ID {ga.group(1)!r} is not a GA4 Measurement ID")
    else:
        print("analytics:", "ON " + ga.group(1) if ga.group(1) else "OFF (no Measurement ID set yet)")

    for w in warnings:
        print("warning:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{len(pages)} pages checked, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
