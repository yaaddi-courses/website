# Yaaddi website

The landing page for [Yaaddi](https://yaaddi.com), a free learning app on Google Play. Plain static HTML and CSS. No build step on deploy and no external requests, except optional Google Analytics that loads only after a visitor clicks Accept.

Courses live in a separate site: [courses.yaaddi.com](https://courses.yaaddi.com).

## Structure

| Path | Purpose |
|---|---|
| `index.html` | The page: content, metadata, structured data (JSON-LD) |
| `assets/style.css` | Styles (light and dark follow the system setting) |
| `assets/img/` | Icons, social preview image and screenshots |
| `help/` | Help center: a hub and one how-to article per page (generated, see below) |
| `privacy/` | Website privacy and analytics page (generated) |
| `assets/analytics.js` | Consent banner and Google Analytics 4 (off until a Measurement ID is set) |
| `404.html` | Not-found page (`noindex`) |
| `robots.txt`, `sitemap.xml`, `llms.txt` | Crawler files (the sitemap and `llms.txt` are generated) |
| `CNAME` | Custom domain for GitHub Pages: `yaaddi.com` |
| `tools/make_assets.py` | Regenerates the landing-page images from the app's source assets |
| `tools/help_content.py` | The text of every help article (edit here) |
| `tools/build_help.py` | Builds `help/`, `privacy/`, `sitemap.xml` and `llms.txt` from the content |
| `tools/capture_help_shots.cjs`, `tools/make_help_images.py` | Capture help screenshots from the running app, convert to WebP |
| `tools/check_site.py` | Pre-push checks: titles, descriptions, canonicals, links, alt text, JSON-LD, CSP, sitemap |
| `tools/check_links_live.py`, `tools/scan_claims.py` | Live link check (follows redirects, shows final page titles) and a scan for promises to verify |

## Edit and preview

```bash
python -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765/>. You can also open `index.html` directly in a browser: the page uses relative paths, so it works both ways. Only `404.html` uses root paths (`/assets/...`), because it is served from any URL depth on the live site.

When the page content changes, update `lastmod` in `sitemap.xml`. If the FAQ text changes, change the matching `FAQPage` entries in the JSON-LD in `index.html`; Google expects the structured data to match what visitors see.

The Content-Security-Policy is identical on every page and defined once in `tools/build_help.py`; `check_site.py` fails if a page drifts.

## Help center workflow

1. Edit the article in `tools/help_content.py` and bump its `updated` date. Check every instruction against the app first.
2. For new screenshots: start the app (`npx expo start --web --port 8081` in the app folder), run `node tools/capture_help_shots.cjs`, then `python tools/make_help_images.py`.
3. `python tools/build_help.py`, then `python tools/check_site.py`. Commit the generated files.

Write each article as one task or question, with the short answer first and numbered steps. Google no longer shows FAQ or How-to rich results for most sites, so the structured data is `TechArticle` plus breadcrumbs, and the ranking work is done by clear titles, plain answers and internal links.

Run the whole review (links, over-promising, SEO and LLM checks, accuracy against the app) with the `website-review` skill (kept local, not published).

## Google Analytics 4

Analytics is off until a Measurement ID is set. No banner, cookies or requests happen while it is empty.

1. In [Google Analytics](https://analytics.google.com/), create a property, then a **Web** data stream for `https://yaaddi.com`. Copy the Measurement ID (`G-XXXXXXXXXX`).
2. Admin → Data collection and modification → Data retention: set event data retention to **14 months** (the privacy page promises no more than that). Leave Google signals off.
3. Put the ID in `GA_ID` in `assets/analytics.js`, run `python tools/check_site.py`, commit and push.
4. Confirm: open the site, accept the banner, and look for your visit in Reports → Realtime. Events sent after consent: `play_store_click`, `courses_site_click`, `support_email_click` (each with `link_location`). In Admin → Events, mark `play_store_click` as a key event.
5. Link Search Console to the property (Admin → Product links) to see which searches lead to help pages.

Visitors who decline, or whose browser sends Do Not Track or Global Privacy Control, are not measured, so expect GA numbers to be lower than real traffic. `courses.yaaddi.com/privacy/` describes the app only; add a one-line pointer to `yaaddi.com/privacy/` there if you want the two linked.

## Deploy

Pushing to `main` publishes the site through GitHub Pages (Settings → Pages → Deploy from a branch → `main`, `/ (root)`).

## One-time setup

### 1. DNS (Porkbun)

In Porkbun, open the `yaaddi.com` DNS records and:

1. Delete only the existing web records for the bare domain (host blank): the A or ALIAS record that points at Porkbun's parking page. **Keep the MX and TXT records.** They run the `support@yaaddi.com` email forwarding and its SPF record.
2. Add these four **A** records, host blank:
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. Optional **AAAA** records, host blank:
   `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`
4. Replace the `www` record with a **CNAME**: host `www`, answer `yaaddi-courses.github.io`.

Do not change the name servers or the `courses` CNAME.

### 2. GitHub Pages

1. Repository → Settings → Pages. Source: **Deploy from a branch**, branch `main`, folder `/ (root)`.
2. Custom domain: `yaaddi.com` (already set by the `CNAME` file). Wait for the DNS check to pass.
3. Tick **Enforce HTTPS** once it becomes available (can take up to an hour after DNS is correct).

Recommended: verify the domain for the organization (Organization settings → Pages → Add a domain, then add the TXT record GitHub shows). It stops anyone else from using the domain with GitHub Pages.

### 3. Google Search Console

1. Add the property `https://yaaddi.com/` (a Domain property with a TXT record is best because it covers `www` and `courses`).
2. Submit `https://yaaddi.com/sitemap.xml`.
3. Use URL Inspection on the home page and request indexing.

### 4. Link it everywhere

Use the same one-line description and the link `https://yaaddi.com/` in the Google Play listing, the GitHub organization profile, and the author's DEV, Hashnode, Medium, LinkedIn and GitHub profiles. Consistent naming and links help search engines connect them.

## Checks before publishing a change

- One `<h1>`, title under 60 characters, description under 160.
- Every image has `alt` text and `width`/`height`.
- JSON-LD parses; FAQ text matches the page.
- Claims match the app and its privacy policy (free, no ads, no account, offline after install).
- No inline scripts or styles (the page sets a strict Content-Security-Policy).
