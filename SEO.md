# SEO + AEO Guide

This document explains the technical SEO/AEO setup of the PhenoTips static site and the recurring audit workflow that replaces what Yoast did on WordPress.

> **AEO** = Answer Engine Optimization. The new layer on top of SEO that makes content appear in AI overviews — ChatGPT search, Perplexity, Google AI Overviews, Claude, Gemini.

---

## What's already in place

Every page in `site/` ships with the following technical SEO baked in:

| Layer | Tag / file | Purpose |
|---|---|---|
| Crawl control | `robots.txt` | Allows `*` plus explicit allow rules for GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended, CCBot, OAI-SearchBot, Perplexity-User, Bytespider, Amazonbot, meta-externalagent, cohere-ai, facebookexternalhit |
| Discoverability | `sitemap.xml` | All 14 URLs, priorities, last-modified dates |
| AI ingestion | `llms.txt` | Markdown summary of the site for LLM training/retrieval — emerging AEO standard |
| Per-page meta | `<title>`, `<meta name="description">` | Titles + descriptions on every page |
| Canonicalization | `<link rel="canonical">` | Tells engines `phenotips.com` is the source-of-truth URL |
| Robots meta | `<meta name="robots">` | `index,follow,max-image-preview:large` |
| Open Graph | `og:title`, `og:description`, `og:image`, `og:url`, `og:site_name` | LinkedIn / Slack / iMessage previews |
| Twitter cards | `twitter:card=summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image` | X/Twitter previews |
| Brand image | `assets/og-default.png` | 1200×630 branded social preview |
| Site-wide schema | `Organization` JSON-LD | On every page — feeds knowledge panels in Google + AI engines |
| Per-page schema | `WebSite`, `SoftwareApplication`, `Service`, `Article`, `NewsArticle`, `AboutPage`, `ContactPage`, `CollectionPage`, `WebPage` | Page-type-aware structured data |
| Breadcrumbs | `BreadcrumbList` JSON-LD | On all sub-pages |

---

## Canonical URL note

All canonicals currently point to `https://phenotips.com/<path>` — the eventual home of this redesign. Until the redesign goes live there, search engines may treat the staging deploys (`polite-speculoos-e4e0a4.netlify.app`, `parkerrl-91.github.io/PhenoTipsWebsite/`) as duplicates of the canonical phenotips.com pages.

If you want to canonicalize to a staging URL instead while previewing, edit `CANONICAL` in `/tmp/seo.py` (or its committed copy) and re-run.

---

## Page → schema map

| Page | Schema(s) |
|---|---|
| `/` | Organization · WebSite |
| `/platform` | Organization · SoftwareApplication |
| `/roi-calculator` | Organization · WebPage |
| `/about` | Organization · AboutPage |
| `/team` | Organization · AboutPage |
| `/contact` | Organization · ContactPage |
| `/press` | Organization · CollectionPage |
| `/publications` | Organization · CollectionPage |
| `/webinars` | Organization · CollectionPage |
| `/solutions/rare-disease` | Organization · Service · BreadcrumbList |
| `/solutions/cancer-genetics` | Organization · Service · BreadcrumbList |
| `/solutions/health-systems` | Organization · Service · BreadcrumbList |
| `/news/gapp-announcement` | Organization · NewsArticle · BreadcrumbList |
| `/case-studies/addenbrooke` | Organization · Article · BreadcrumbList |

---

## Audit workflow (replaces Yoast)

### One-time setup

1. **Verify Google Search Console** for `phenotips.com` (and the staging URLs if you want to track them too)
   - https://search.google.com/search-console
   - Use HTML tag verification — paste a `<meta name="google-site-verification">` tag into every page (let me know and I'll add it)
2. **Verify Bing Webmaster Tools**
   - https://www.bing.com/webmasters
   - Bing data feeds **ChatGPT Search**, so this is now first-class for AEO
3. **Add Ahrefs Webmaster Tools** (free tier)
   - https://ahrefs.com/webmaster-tools
4. **Submit sitemap**
   - In Search Console → Sitemaps → Add new sitemap → `sitemap.xml`
   - In Bing Webmaster → Sitemaps → Submit a sitemap → `https://phenotips.com/sitemap.xml`

### Weekly (15 minutes)

| Tool | What to check |
|---|---|
| Google Search Console | New errors, top queries, click-through rates, Core Web Vitals |
| Bing Webmaster | Same metrics for Bing/ChatGPT search |
| HubSpot Reports (when wired) | Page views by source, form submissions, deal influence |

### Per release

1. Push to `main` → both Netlify and GitHub Pages auto-deploy
2. **Run Lighthouse** on the changed page (Chrome DevTools → Lighthouse → Performance + SEO + Accessibility)
3. **Validate schema** at https://search.google.com/test/rich-results
4. **Re-fetch** in Search Console (URL Inspection → Test Live URL → Request Indexing)

### Monthly

| Tool | What to check |
|---|---|
| Screaming Frog SEO Spider (free, ≤500 URLs) | Crawl whole site — broken links, missing meta, redirect chains, schema issues |
| Lighthouse | Run on home + 3 highest-traffic pages — track Core Web Vitals over time |
| Manual: Perplexity / ChatGPT / Claude | Search for "PhenoTips," "genomic health record," "rare disease software," "HPO clinical software" — see if you're cited |
| HubSpot Attribution | Which pages drive deals? Adjust content investment accordingly |

### Quarterly

- Refresh `llms.txt` and `sitemap.xml` lastmod dates
- Audit competitive keywords (Ahrefs / SEMrush — paid)
- Update Organization schema with any new co-founders, social profiles, or contact info

---

## How to re-run the SEO injection

If you add a new page, edit `/tmp/seo.py` (or commit it under `tools/seo.py`) and add a row to the `PAGES` list. Then:

```sh
python3 /tmp/seo.py
```

The script is idempotent — it strips any previous SEO block before injecting the fresh one. Re-running is safe.

---

## AEO-specific tips

LLM search engines (ChatGPT search, Perplexity, Claude, Gemini) reward the same things classical SEO does **plus**:

1. **`llms.txt`** at the site root — a markdown table-of-contents specifically for them. Already in place.
2. **Clean structured data** — JSON-LD with `Organization` + page-type-specific schemas. AI engines parse these heavily. Already in place.
3. **Quotable, factual sentences** — the platform stats ("3× faster," "50% encounter efficiency," "100+ institutions") are written as standalone factual claims. AI engines prefer extractable facts over marketing prose. Already done in copy.
4. **Named entities + dates** — case studies, press releases, and the GAPP announcement all use named institutions, dates, and proper nouns. Already done.
5. **Original research / case studies** — the Addenbrooke case study and GAPP press release are unique content not available elsewhere. AI engines reward original source material.

### What to actively monitor for AEO

| Question | Tool |
|---|---|
| Does ChatGPT cite us? | https://chatgpt.com — search for relevant queries with web search enabled |
| Does Perplexity cite us? | https://www.perplexity.ai — same queries |
| Does Google AI Overview cite us? | Logged-in Google searches with AI Overview enabled (US-first) |
| Which AI bots are crawling us? | Server logs (or Cloudflare AI Audit if you put Cloudflare in front) |
| Paid LLM-tracking tools | Profound, Otterly.ai, AthenaHQ — track mentions across all major LLMs |

---

## What's NOT yet wired (and why)

- **Google Analytics 4** — not added; HubSpot tracking script (when wired) will provide most of the same data + identifies known leads
- **HubSpot tracking script** — pending Hub ID / Portal ID
- **HubSpot embedded forms** — pending form ID
- **HubSpot Meetings embed** — pending meetings link
- **FAQ schema** — not added; would be high-value on the platform page if we add a "Frequently asked questions" section to the body copy

---

## File reference

| File | What it does | Edit when |
|---|---|---|
| `site/sitemap.xml` | URL list for search engines | New page added |
| `site/robots.txt` | Crawler permissions | New AI bot to allow/block |
| `site/llms.txt` | AEO-targeted summary | Major content/positioning changes |
| `site/assets/og-default.png` | 1200×630 social preview | Brand redesign |
| `tools/seo.py` (or `/tmp/seo.py`) | Idempotent injection script | New page or schema change |

*Last updated: 2026-04-27*
