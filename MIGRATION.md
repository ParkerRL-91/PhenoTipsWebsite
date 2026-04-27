# PhenoTips WordPress → Static Site Migration Plan

> One artifact. Follow it on launch day.
>
> Last URL inventory pulled: **2026-04-27**, from `phenotips.com/sitemap_index.xml` (All-in-One SEO).
> Total legacy URLs found: **115** (98 mapped to redirects, 13 plugin junk Disallow'd, 4 already handled).

---

## Goal

Move from WordPress (`phenotips.com`) to this static site **without losing search rankings, backlinks, or branded SERP placement.**

---

## Pre-launch ✅ (already complete)

- [x] Full URL inventory pulled from current sitemap
- [x] 301 redirect map built and committed to `netlify.toml`
- [x] Pattern catch-alls for `/blog/*`, `/speaker-series/*`, `/press/*`, `/casestudies/*`, `/case-studies/*`
- [x] `404.html` page with friendly fallback + console logging
- [x] `js/migration-tracker.js` — beacon-ready logger for legacy 301 arrivals
- [x] Stub pages for `/privacy-policy.html`, `/cloud-terms.html`, `/cloud-privacy.html`
- [x] `robots.txt` Disallows for WordPress plugin junk URLs
- [x] Site-wide canonical URLs → `https://phenotips.com/<path>`
- [x] Sitemap, schema, OG image, Twitter cards (see `SEO.md`)

---

## Pre-launch (still to do — owner: Parker)

- [ ] **Verify Google Search Console** for `phenotips.com` (if not already)
- [ ] **Verify Bing Webmaster Tools** for `phenotips.com`
- [ ] **Replace stub legal pages** with real legal content reviewed by counsel
  - `site/privacy-policy.html`
  - `site/cloud-terms.html`
  - `site/cloud-privacy.html`
- [ ] **Decide host for production phenotips.com** (recommendation: **Netlify** — see "Host decision" below)
- [ ] **Lower DNS TTL on `phenotips.com` A/CNAME records to 5 minutes**, **24 hours before launch**
- [ ] **Take a full WordPress backup** (database export + `wp-content/uploads/` + active theme) — keep for 6 months
- [ ] **Pick launch window** (recommendation: Sunday morning ET, low traffic)
- [ ] **Set `MIGRATION_BEACON_URL`** if you want server-side 301-arrival logging (see `js/migration-tracker.js`)
- [ ] **Verify HubSpot tracking + form ID** if wiring HubSpot before launch (separate workstream)

---

## Host decision

| | Netlify (current preview at `polite-speculoos-e4e0a4.netlify.app`) | GitHub Pages (current preview at `parkerrl-91.github.io/PhenoTipsWebsite/`) |
|---|---|---|
| Redirects (301 / pattern) | ✅ via `netlify.toml` | ❌ not supported |
| Forms | ✅ Netlify Forms or HubSpot embed | ❌ would need HubSpot or 3rd-party |
| Custom domain | ✅ free, auto-SSL | ✅ free, auto-SSL |
| Build time | ~10 sec (no build) | ~20 sec (Actions) |

**Recommendation: Netlify.** Without redirect support, GitHub Pages would 404 every legacy URL on launch day — unacceptable.

---

## Launch day — 30-minute runbook

> Pick a Sunday morning ET window. Do this in one focused sitting.

### T-30 min · Pre-flight

1. Confirm DNS TTL is **5 min or lower** on `phenotips.com` records
2. Open **two browser tabs**: GSC and Netlify dashboard
3. Open **terminal** with this repo checked out
4. Confirm latest commit is deployed to Netlify staging (`polite-speculoos-e4e0a4.netlify.app`) and renders correctly

### T-0 · DNS cutover

1. **At your DNS provider** (registrar or Cloudflare), change records on `phenotips.com`:
   ```
   A     phenotips.com           → 75.2.60.5     (Netlify ALB)
   CNAME www.phenotips.com       → polite-speculoos-e4e0a4.netlify.app
   ```
   (Or, easier: use Netlify-managed DNS — point your domain's nameservers at Netlify and they handle the rest.)
2. **In the Netlify dashboard** for the site:
   Site settings → Domain management → Add custom domain → `phenotips.com` → Verify → Provision SSL

### T+5 · Verification

1. `curl -I https://phenotips.com` → should be 200, served by Netlify (header `Server: Netlify`)
2. `curl -I https://phenotips.com/our-story/` → should be 301 → `/about.html`
3. `curl -I https://phenotips.com/speaker-series/business-cases/` → should be 301 → `/webinars.html`
4. `curl -I https://phenotips.com/some-nonexistent-page` → should be 404 with our friendly page
5. Run the smoke test below

### T+10 · Tell search engines

1. **Google Search Console** → Property `phenotips.com`:
   - Sitemaps → Submit `https://phenotips.com/sitemap.xml`
   - URL Inspection → paste `https://phenotips.com/` → "Request Indexing"
   - Repeat URL Inspection for the top 10-20 pages by traffic
2. **Bing Webmaster Tools** → same: submit sitemap + request indexing for top pages
3. **Update sameAs links** anywhere external (LinkedIn company page, Twitter bio, etc.) so they all point to `phenotips.com` (no change needed since domain stays the same — but verify the URL paths still work after redirects)

### T+30 · Tail logs

In Netlify dashboard → Site → Functions → Live logs (or Analytics → Bandwidth):
- Watch for 404 spikes for the next 4 hours
- Any URL repeatedly 404ing → add a `[[redirects]]` entry to `netlify.toml`, commit, push, Netlify auto-redeploys in ~30 seconds

### T+24 hours

- Raise DNS TTL back to 1 hour or longer
- Confirm Search Console "Indexed" count is stable or growing (not crashing)

---

## Smoke test (run after cutover)

```bash
# Test 30 critical redirects in one shot
SITE="https://phenotips.com"
for url in \
  "/our-story/" \
  "/team/" \
  "/contact/" \
  "/book-a-demo/" \
  "/rare-disease/" \
  "/cancer-genetics/" \
  "/health-systems/" \
  "/phenotips-pedigree-maker-tool/" \
  "/core-genomic-health-record/" \
  "/cancer-risk-assessment/" \
  "/patient-questionnaire/" \
  "/blog/" \
  "/speaker-series/" \
  "/press/" \
  "/papers/" \
  "/casestudies/" \
  "/blog/single-parent-pedigree/" \
  "/blog/genomic-health-records/" \
  "/speaker-series/business-cases/" \
  "/speaker-series/ai-in-genomics/" \
  "/press/smartrequisition/" \
  "/press/best-startup-employer/" \
  "/casestudies/case-study-addenbrookes/" \
  "/case-studies/addenbrooke-case-study/" \
  "/category/blog/" \
  "/category/speaker-series/" \
  "/pricing/" \
  "/nps-thank-you/" \
  "/demo-thank-you/" \
  "/some-page-that-does-not-exist"
do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SITE$url")
  FINAL=$(curl -s -o /dev/null -w "%{redirect_url}" -L "$SITE$url")
  printf "%-55s → %s  %s\n" "$url" "$CODE" "$FINAL"
done
```

Expected:
- All redirected URLs return **301** with a `Location:` header pointing to the right destination
- The "does not exist" URL returns **404** and serves `404.html`

---

## First 14 days (daily, 5 min/day)

| Day | Action |
|---|---|
| **D+1, D+2** | GSC → Pages → "Why pages aren't indexed" → look for new errors |
| **D+1 to D+7** | Brand search ("PhenoTips") on Google + Bing — confirm position #1 |
| **D+1 to D+14** | Netlify Analytics → 4xx errors per day. Goal: ≤ 1% of traffic |
| **D+3, D+7, D+14** | Search Console → Performance → compare clicks/impressions to pre-launch baseline |

**Red flags during this period:**
- 404 rate > 5% of traffic → check Netlify logs for the offending URLs, add redirects
- Brand search drops below #1 → check redirects on `/`, `/about`, `/contact`
- Total impressions drop > 30% over 7 days → check Search Console index coverage; may have a blanket noindex by mistake

---

## First 90 days (weekly review)

- Search Console → Performance → top queries — track ranking position for top 10 keywords
- Search Console → Coverage → "Page with redirect" should grow as Google processes the 301s
- Ahrefs Webmaster Tools → check for new 404s from external backlinks

---

## Re-running the URL inventory

Whenever you want to re-check current WordPress URLs (e.g., during the parallel period before cutover):

```bash
python3 tools/build_redirects.py
```

Outputs a fresh redirect map. If new URLs have appeared on WordPress, they'll show in the "uncovered" list — add them to `SPECIFIC` or a `PATTERNS` rule.

---

## Files reference

| File | Purpose |
|---|---|
| `netlify.toml` | All redirects + headers (28 specific + 5 patterns + pretty-URL rewrites) |
| `site/404.html` | Friendly fallback + console logging |
| `site/js/migration-tracker.js` | Logs legacy 301-arrival on every page; sends beacon if `MIGRATION_BEACON_URL` is set |
| `site/privacy-policy.html`, `site/cloud-terms.html`, `site/cloud-privacy.html` | Stubs — replace with real legal content before launch |
| `site/robots.txt` | Disallow rules for WordPress plugin junk URLs |
| `tools/build_redirects.py` | Re-run to refresh the redirect map from current WordPress sitemap |
| `SEO.md` | Technical SEO setup + audit workflow (companion doc) |

---

## Rollback plan (in case of disaster)

If traffic drops > 50% in the first 24 hours and you need to revert:

1. **At DNS provider:** revert `phenotips.com` records to the original WordPress server's IP
2. **TTL is 5 min**, so revert propagates in ~5-10 minutes
3. **Restore from backup** if WordPress files were touched
4. **In Search Console:** verify the old site is back to 200; resubmit old sitemap if needed

The static site continues to live at `polite-speculoos-e4e0a4.netlify.app` regardless — you can keep iterating there before re-cutting over.

---

*Generated 2026-04-27. Update launch date and any new URLs before cutover.*
