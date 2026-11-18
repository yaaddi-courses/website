"""List every sentence on the site that makes a promise worth verifying.

It cannot decide whether a claim is true; it finds candidates (absolutes, superlatives, numbers,
guarantees, legal-sounding words) so a reviewer can check each against the app's source. The
website-review skill does the checking.

Run from the Website folder:   python tools/scan_claims.py
Options:  --json
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PATTERNS = {
    "absolute": r"\b(always|never|every|all|any|no one|nothing|nobody|everyone|only|completely|fully|entirely|100%)\b",
    "superlative": r"\b(best|fastest|easiest|simplest|most|leading|top|ultimate|perfect|unmatched)\b",
    "guarantee": r"\b(guarantee[sd]?|proven|proves|certified|official|secure|safe|safest|anonymous|private|encrypted)\b",
    "number": r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|twenty|dozen|dozens|hundreds?|thousands?)\s+(\w+\s+)?(courses?|decks?|cards?|questions?|types?|users?|languages?|algorithms?|days?|minutes?|MB)\b",
    "comparison": r"\b(better than|faster than|unlike|instead of|than other|compared to)\b",
    "money_or_time": r"\b(free|forever|lifetime|no cost|instantly|in seconds|in one tap|immediately)\b",
    "result": r"\b(will|helps? you|makes? you|lets? you|so you can|master)\b",
}
SKIP_TAGS = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.S | re.I)


def sentences(page_html):
    text = SKIP_TAGS.sub(" ", page_html)
    text = re.sub(r"<(h[1-6]|p|li|dt|dd|summary|figcaption|td)[^>]*>", "\n", text, flags=re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    for line in text.split("\n"):
        for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", line).strip()):
            if len(s) > 12:
                yield s


def scan_text(page_html):
    hits = []
    for s in sentences(page_html):
        kinds = [k for k, p in PATTERNS.items() if re.search(p, s, re.I)]
        if kinds:
            hits.append((kinds, s))
    return hits


def main():
    out = []
    for page in sorted(ROOT.rglob("*.html")):
        if "tools" in page.parts or ".git" in page.parts or page.name == "404.html":
            continue
        for kinds, s in scan_text(page.read_text(encoding="utf-8")):
            out.append({"page": page.relative_to(ROOT).as_posix(), "kinds": kinds, "sentence": s})
    if "--json" in sys.argv:
        print(json.dumps(out, indent=2))
    else:
        current = None
        for h in out:
            if h["page"] != current:
                current = h["page"]
                print(f"\n== {current}")
            print(f"  [{', '.join(h['kinds'])}] {h['sentence']}")
        print(f"\n{len(out)} candidate claims. Verify each against the app source; fix or soften the ones it does not support.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
