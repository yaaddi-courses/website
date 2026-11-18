# Yaaddi website

The landing page for [Yaaddi](https://yaaddi.com), a free learning app on Google Play. Plain HTML and CSS. No build step, no JavaScript, no external requests.

Courses live in a separate site: [courses.yaaddi.com](https://courses.yaaddi.com).

## Structure

| Path | Purpose |
|---|---|
| `index.html` | The page: content, metadata, structured data (JSON-LD) |
| `assets/style.css` | Styles (light and dark follow the system setting) |
| `assets/img/` | Icons, social preview image and screenshots |
| `404.html` | Not-found page (`noindex`) |
| `robots.txt`, `sitemap.xml` | Crawler files |
| `CNAME` | Custom domain for GitHub Pages: `yaaddi.com` |
| `tools/make_assets.py` | Regenerates the images from the app's source assets |

## Edit and preview

```bash
python -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765/>. Paths in the page start with `/`, so serve the folder as the site root.

When the page content changes, update `lastmod` in `sitemap.xml`. If the FAQ text changes, change the matching `FAQPage` entries in the JSON-LD in `index.html`; Google expects the structured data to match what visitors see.

## Deploy

Pushing to `main` publishes the site through GitHub Pages (Settings → Pages → Deploy from a branch → `main`, `/ (root)`).

## One-time setup

### 1. DNS (Porkbun)

In Porkbun, open the `yaaddi.com` DNS records and:

1. Delete the existing records for the bare domain (host blank) that point at Porkbun's parking page.
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
