"""Build the help center, the website-privacy page and the sitemap from tools/help_content.py.

Run from the Website folder:   python tools/build_help.py
Output is plain static HTML committed to the repository (help/, privacy/, sitemap.xml, llms.txt),
so deployment stays "push to main". After running, run:   python tools/check_site.py
"""
import html
import json
import re
from pathlib import Path

from help_content import ARTICLES, BY_SLUG, CATEGORIES, PLAY

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://yaaddi.com"
SITE_UPDATED = "2026-11-18"  # bump when the hub, privacy page or home page content changes

# One policy for every page. Google domains are allowed so analytics can run once a Measurement ID is
# set in assets/analytics.js; while it is empty nothing contacts them.
CSP = (
    "default-src 'none'; "
    "img-src 'self' https://www.googletagmanager.com https://*.google-analytics.com; "
    "script-src 'self' https://www.googletagmanager.com; "
    "connect-src https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com; "
    "style-src 'self'; base-uri 'none'; form-action 'none'"
)

AUTHOR = {"@id": f"{SITE}/#author"}
OG_IMAGE = f"{SITE}/assets/img/og-image.png"


def esc(text):
    return html.escape(text, quote=True)


def plain(markup):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", markup))).strip()


def trim(text, limit=158):
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "…"


def jsonld(data):
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/") + "\n  </script>"


def head(*, title, description, path, up, schema, og_type="website", robots="index, follow, max-image-preview:large"):
    url = f"{SITE}{path}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="Mohammad Reza Mahdiani">
  <meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#111827" media="(prefers-color-scheme: dark)">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">

  <link rel="icon" type="image/png" sizes="32x32" href="{up}assets/img/favicon-32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="{up}assets/img/icon-192.png">
  <link rel="apple-touch-icon" href="{up}assets/img/apple-touch-icon.png">

  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Yaaddi">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Yaaddi logo with the text: Free learning app with ready-made courses">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{OG_IMAGE}">

  <link rel="stylesheet" href="{up}assets/style.css">
  {jsonld(schema)}
  <script src="{up}assets/analytics.js" data-privacy="{up}privacy/" defer></script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap bar">
      <a class="brand" href="{up or './'}" aria-label="Yaaddi home">
        <img src="{up}assets/img/logo-96.webp" width="40" height="40" alt="">
        <span>Yaaddi</span>
      </a>
      <nav aria-label="Main">
        <a href="{up}#features">Features</a>
        <a href="https://courses.yaaddi.com/" data-where="header" rel="noopener">Courses</a>
        <a class="keep" href="{up}help/">Help</a>
        <a class="btn btn-small" href="{PLAY}" data-where="header" rel="noopener">Get the app</a>
      </nav>
    </div>
  </header>
"""


def foot(up):
    return f"""
  <footer class="site-footer">
    <div class="wrap foot">
      <p>&copy; 2026 Yaaddi. Built by <a href="https://www.linkedin.com/in/mohammad-reza-mahdiani/" rel="noopener me">Mohammad Reza Mahdiani</a>.</p>
      <nav aria-label="Footer">
        <a href="{up}help/">Help</a>
        <a href="https://courses.yaaddi.com/" data-where="footer" rel="noopener">Courses</a>
        <a href="{up}privacy/">Privacy</a>
        <a href="https://courses.yaaddi.com/terms/" rel="noopener">Terms</a>
        <a href="mailto:support@yaaddi.com" data-where="footer">Contact</a>
      </nav>
      <p class="small">Google Play is a trademark of Google LLC. Yaaddi is not affiliated with or endorsed by Google.</p>
    </div>
  </footer>
</body>
</html>
"""


def breadcrumb_schema(trail):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{SITE}{path}"}
            for i, (name, path) in enumerate(trail)
        ],
    }


def crumbs_html(trail, up):
    items = []
    for i, (name, path) in enumerate(trail):
        if i == len(trail) - 1:
            items.append(f'<li aria-current="page">{esc(name)}</li>')
        else:
            href = up + path.lstrip("/") if path != "/" else (up or "./")
            items.append(f'<li><a href="{href}">{esc(name)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


def category_title(key):
    return next(t for k, t, _ in CATEGORIES if k == key)


def article_page(a):
    up = "../../"
    path = f"/help/{a['slug']}/"
    page_title = f"{a['title']} | Yaaddi Help"
    description = trim(plain(a["summary"]))
    trail = [("Yaaddi", "/"), ("Help", "/help/"), (a["title"], path)]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "@id": f"{SITE}{path}#article",
                "headline": a["title"],
                "description": description,
                "url": f"{SITE}{path}",
                "mainEntityOfPage": f"{SITE}{path}",
                "inLanguage": "en",
                "datePublished": a.get("published", a["updated"]),
                "dateModified": a["updated"],
                "image": OG_IMAGE,
                "author": AUTHOR,
                "publisher": AUTHOR,
                "about": {"@id": f"{SITE}/#app"},
                "isPartOf": {"@id": f"{SITE}/#website"},
            },
            breadcrumb_schema(trail),
        ],
    }
    out = [head(title=page_title, description=description, path=path, up=up, schema=schema, og_type="article")]
    out.append('\n  <main id="main">\n    <article class="wrap narrow article">\n      <div class="help-head">\n')
    out.append(f"        {crumbs_html(trail, up)}\n        <h1>{esc(a['title'])}</h1>\n")
    out.append(f'        <p class="summary"><strong>Short answer</strong>{a["summary"]}</p>\n')
    out.append(f'        <p class="meta">{esc(category_title(a["category"]))} · Last updated {a["updated"]} · For the Yaaddi Android app</p>\n      </div>\n')

    if a.get("steps"):
        out.append("      <h2>Steps</h2>\n      <ol class=\"steps\">\n")
        for text, image in a["steps"]:
            fig = ""
            if image:
                file, alt = a["images"][image]
                fig = (f'\n        <figure class="help-shot"><img src="{up}assets/img/help/{file}" width="480" height="1039" '
                       f'loading="lazy" decoding="async" alt="{esc(alt)}"></figure>')
            out.append(f"        <li><p>{text}</p>{fig}</li>\n")
        out.append("      </ol>\n")

    for heading, body in a.get("sections", []):
        out.append(f"      <h2>{esc(heading)}</h2>\n      {body}\n")

    if a.get("notes"):
        out.append("      <h2>Good to know</h2>\n      <ul class=\"notes\">\n")
        out.extend(f"        <li>{n}</li>\n" for n in a["notes"])
        out.append("      </ul>\n")

    if a.get("faq"):
        out.append("      <h2>Common questions</h2>\n")
        for q, ans in a["faq"]:
            out.append(f'      <div class="faq-item"><h3>{esc(q)}</h3><p>{ans}</p></div>\n')

    out.append("      <h2>Related help</h2>\n      <div class=\"related\">\n")
    for slug in a["related"]:
        out.append(f'        <a href="../{slug}/">{esc(BY_SLUG[slug]["title"])}</a>\n')
    out.append("      </div>\n")
    out.append('      <aside class="stuck"><p><strong>Still stuck?</strong> Tell us what you tried and what you saw, and we will do our best to help.</p>'
               '<p><a class="btn btn-small" href="mailto:support@yaaddi.com" data-where="help-article">Email support@yaaddi.com</a></p></aside>\n')
    out.append("    </article>\n  </main>\n")
    out.append(foot(up))
    return "".join(out)


QUICK = [
    ("Is Yaaddi free?", "Yes. Yaaddi and its courses are free on Google Play, with no ads.", "is-yaaddi-free"),
    ("Does Yaaddi work offline?", "Yes, once a course is installed. Only the library and updates need the internet.", "use-offline"),
    ("How do I move Yaaddi to a new phone?", "Create a backup on the old phone and restore it on the new one.", "backup-and-restore"),
    ("Which spaced-repetition algorithm is best?", "The default suits most people. You can switch to FSRS, SM-2, ACT-R, HLR or Fibonacci.", "change-spaced-repetition-algorithm"),
    ("How do I keep my streak?", "Study once a day. Streak freezes and a weekly grace day cover missed days.", "streaks-freezes-coins"),
    ("Can I skip what I already know?", "Yes. The \"What do you know?\" check marks known decks so you study only what is new.", "skip-what-you-know"),
]


def hub_page():
    up = "../"
    path = "/help/"
    title = "Yaaddi Help Center: how-to guides for the learning app"
    description = "Step-by-step guides for Yaaddi: install and create courses, change the spaced-repetition algorithm, set reminders, back up, take exams and more."
    trail = [("Yaaddi", "/"), ("Help", path)]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": f"{SITE}{path}#page",
                "name": "Yaaddi Help Center",
                "description": description,
                "url": f"{SITE}{path}",
                "inLanguage": "en",
                "isPartOf": {"@id": f"{SITE}/#website"},
                "about": {"@id": f"{SITE}/#app"},
                "mainEntity": {
                    "@type": "ItemList",
                    "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "name": a["title"], "url": f"{SITE}/help/{a['slug']}/"}
                        for i, a in enumerate(ARTICLES)
                    ],
                },
            },
            breadcrumb_schema(trail),
        ],
    }
    out = [head(title=title, description=description, path=path, up=up, schema=schema)]
    out.append('\n  <main id="main">\n    <div class="wrap article">\n      <div class="help-head">\n')
    out.append(f"        {crumbs_html(trail, up)}\n        <h1>Yaaddi Help Center</h1>\n")
    out.append('        <p class="lead">Short, step-by-step answers for everything you can do in Yaaddi, written from the app itself.</p>\n      </div>\n')
    out.append('      <h2>Quick answers</h2>\n')
    for q, ans, slug in QUICK:
        out.append(f'      <div class="faq-item"><h3>{esc(q)}</h3><p>{esc(ans)}</p><a class="more" href="{slug}/">{esc(BY_SLUG[slug]["title"])} →</a></div>\n')
    out.append('      <div class="cat-grid">\n')
    for key, name, blurb in CATEGORIES:
        out.append(f'        <section class="card" aria-labelledby="c-{key}"><h2 id="c-{key}">{esc(name)}</h2><p>{esc(blurb)}</p><ul>\n')
        for a in ARTICLES:
            if a["category"] == key:
                out.append(f'          <li><a href="{a["slug"]}/">{esc(a["title"])}</a></li>\n')
        out.append("        </ul></section>\n")
    out.append("      </div>\n")
    out.append('      <aside class="stuck"><p><strong>Cannot find your answer?</strong> Write to us and your question may become a new guide.</p>'
               '<p><a class="btn btn-small" href="mailto:support@yaaddi.com" data-where="help-hub">Email support@yaaddi.com</a></p></aside>\n')
    out.append("    </div>\n  </main>\n")
    out.append(foot(up))
    return "".join(out)


def privacy_page():
    up = "../"
    path = "/privacy/"
    title = "Privacy and analytics | Yaaddi"
    description = "How yaaddi.com uses optional Google Analytics, what it collects, and how to change your choice. The Yaaddi app itself has no analytics."
    trail = [("Yaaddi", "/"), ("Privacy", path)]
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{SITE}{path}#page",
                "name": "Privacy and analytics",
                "description": description,
                "url": f"{SITE}{path}",
                "inLanguage": "en",
                "dateModified": SITE_UPDATED,
                "isPartOf": {"@id": f"{SITE}/#website"},
            },
            breadcrumb_schema(trail),
        ],
    }
    body = f"""
  <main id="main">
    <article class="wrap narrow article">
      <div class="help-head">
        {crumbs_html(trail, up)}
        <h1>Privacy and analytics</h1>
        <p class="summary"><strong>In short</strong>The Yaaddi app keeps your courses and progress on your phone and has no analytics or ads. This website, yaaddi.com, can use Google Analytics, but only if you click Accept.</p>
        <p class="meta">Last updated {SITE_UPDATED}</p>
      </div>

      <h2>The Yaaddi app</h2>
      <p>Your courses, progress, streaks and settings stay on your phone, and the app contains no analytics or crash-reporting tools. The full text is in the <a href="https://courses.yaaddi.com/privacy/" rel="noopener">app privacy policy</a>. For a plain-language version, see <a href="../help/privacy-and-your-data/">Where does Yaaddi store my data?</a></p>

      <h2>This website</h2>
      <h3>Your choice</h3>
      <p>If analytics is switched on for this site, a small banner asks you once. Your choice is saved in your browser, and your browser's Do Not Track or Global Privacy Control signal counts as Decline. Your current choice: <strong data-consent-status>declined</strong>.</p>
      <p><button type="button" class="btn btn-small" data-consent-settings hidden>Change my choice</button></p>

      <h3>What happens if you accept</h3>
      <ul>
        <li>The page loads Google's analytics script and sets cookies named <code>_ga</code> and <code>_ga_</code> followed by an ID.</li>
        <li>Google Analytics 4 records which pages you view, how you arrived (for example from a search engine), your approximate location such as country and city, your browser and device type, and clicks on our links to Google Play, courses.yaaddi.com and support email. Google Analytics 4 does not store IP addresses.</li>
        <li>Advertising features, Google signals and ad personalization are turned off. We do not use the data for advertising and we do not sell it.</li>
        <li>Analytics data is kept for no longer than 14 months.</li>
      </ul>

      <h3>What happens if you decline</h3>
      <p>Nothing is sent to Google and no Google script is loaded. The site works the same.</p>

      <h3>Why we measure</h3>
      <p>To see which help pages answer people's questions and which questions are missing, so we can improve them.</p>

      <h3>Hosting</h3>
      <p>This site is hosted by GitHub Pages. As with any web host, GitHub may process your IP address and request details to serve the pages, under <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub's privacy statement</a>.</p>

      <h2>Contact</h2>
      <p>Questions about privacy: <a href="mailto:support@yaaddi.com">support@yaaddi.com</a>.</p>
    </article>
  </main>
"""
    return head(title=title, description=description, path=path, up=up, schema=schema) + body + foot(up)


def write(rel, content):
    target = ROOT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def sitemap():
    entries = [("/", SITE_UPDATED), ("/help/", SITE_UPDATED)]
    entries += [(f"/help/{a['slug']}/", a["updated"]) for a in ARTICLES]
    entries.append(("/privacy/", SITE_UPDATED))
    rows = "".join(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n" for p, d in entries)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{rows}</urlset>\n'


def llms_txt():
    lines = [
        "# Yaaddi",
        "",
        "> Yaaddi is a free spaced-repetition learning app for Android with ready-made courses, short questions, no ads and no account. Courses and progress stay on the phone.",
        "",
        "Get the app: " + PLAY,
        "",
        "## Help center",
        "",
    ]
    lines += [f"- [{a['title']}]({SITE}/help/{a['slug']}/): {plain(a['summary'])}" for a in ARTICLES]
    lines += ["", "## Other", "", f"- [Courses](https://courses.yaaddi.com/): every free course with its list of decks", f"- [Privacy]({SITE}/privacy/)", ""]
    return "\n".join(lines)


def outputs():
    """Every generated file as {relative path: content}."""
    files = {f"help/{a['slug']}/index.html": article_page(a) for a in ARTICLES}
    files["help/index.html"] = hub_page()
    files["privacy/index.html"] = privacy_page()
    files["sitemap.xml"] = sitemap()
    files["llms.txt"] = llms_txt()
    return files


def stale():
    """Generated files that differ from the content source, plus help folders no article owns."""
    files = outputs()
    bad = [rel for rel, text in files.items()
           if not (ROOT / rel).exists() or (ROOT / rel).read_text(encoding="utf-8") != text]
    owned = {f"help/{a['slug']}/index.html" for a in ARTICLES}
    bad += [p.relative_to(ROOT).as_posix() for p in (ROOT / "help").glob("*/index.html")
            if p.relative_to(ROOT).as_posix() not in owned]
    return bad


def main():
    files = outputs()
    for rel, text in files.items():
        write(rel, text)
    print(f"built {len(ARTICLES)} articles, the hub, the privacy page, sitemap.xml and llms.txt")


if __name__ == "__main__":
    main()
