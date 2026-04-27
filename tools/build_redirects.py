"""Build a hand-curated redirect map from current phenotips.com URLs to new site."""
import json, re

urls = json.load(open("/tmp/phenotips-urls.json"))

# Hand-mapped 1-to-1 redirects (specific URLs first, patterns last)
SPECIFIC = {
    # ---- About / Company ----
    "/our-story/":                   "/about.html",
    "/team/":                        "/team.html",
    "/contact/":                     "/contact.html",
    "/book-a-demo/":                 "/contact.html",
    "/pricing/":                     "/contact.html",   # no pricing page; book demo

    # ---- Solutions ----
    "/rare-disease/":                "/solutions/rare-disease.html",
    "/cancer-genetics/":             "/solutions/cancer-genetics.html",
    "/health-systems/":              "/solutions/health-systems.html",

    # ---- Features → Platform (consolidated) ----
    "/phenotips-pedigree-maker-tool/":              "/platform.html",
    "/core-genomic-health-record/":                 "/platform.html",
    "/cancer-risk-assessment/":                     "/platform.html",
    "/patient-questionnaire/":                      "/platform.html",
    "/structured-patient-data-and-clinical-insights/":"/platform.html",
    "/seamless-integrations/":                      "/platform.html",

    # ---- Resources ----
    "/papers/":                      "/publications.html",
    "/blog/":                        "/webinars.html",
    "/speaker-series/":              "/webinars.html",
    "/casestudies/":                 "/publications.html",
    "/press/":                       "/press.html",

    # ---- GAPP press release (the only one with a direct equivalent) ----
    "/press/smartrequisition/":      "/news/gapp-announcement.html",

    # ---- Case study with two URL variants → single new page ----
    "/casestudies/case-study-addenbrookes/":         "/case-studies/addenbrooke.html",
    "/case-studies/addenbrooke-case-study/":         "/case-studies/addenbrooke.html",
    "/casestudies/case-study-cmh/":                  "/publications.html",   # no CMH case study yet

    # ---- WordPress category pages ----
    "/category/blog/":               "/webinars.html",
    "/category/speaker-series/":     "/webinars.html",
    "/category/case-studies/":       "/publications.html",

    # ---- Thank-you pages (likely after form submit) → home ----
    "/nps-thank-you/":               "/",
    "/demo-thank-you/":              "/",
}

# Pattern redirects (catch-all for groups)
PATTERNS = [
    # All blog posts → /webinars.html (we don't have a blog yet; closest topical match)
    ("/blog/*",              "/webinars.html",     302),  # 302 so we can swap later when blog exists
    # All speaker-series episodes → /webinars.html (consolidated)
    ("/speaker-series/*",    "/webinars.html",     301),
    # All press releases (other than smartrequisition, handled specifically) → /press.html
    ("/press/*",             "/press.html",        301),
    # Case study legacy URLs → /publications (specific Addenbrooke ones already mapped)
    ("/casestudies/*",       "/publications.html", 301),
    ("/case-studies/*",      "/publications.html", 301),
]

# WordPress plugin/system URLs we want crawlers to ignore — we'll Disallow in robots.txt
# rather than redirect, since they have no SEO value.
NOINDEX_PATTERNS = [
    "/elementskit-content/*",
    "/?elementskit_template=*",
    "/?elementskit_widget=*",
    "/?mas_static_content=*",
]

# ----- Generate netlify.toml redirect block -----
toml_lines = [
    "",
    "# ============================================================",
    "# 301 Migration redirects (legacy WordPress URLs → new static site)",
    "# Generated from phenotips.com sitemap_index.xml on launch.",
    "# Edit tools/build_redirects.py and re-run to regenerate.",
    "# ============================================================",
    "",
]

# Specific 1-to-1 redirects
toml_lines.append("# ---- Specific 1-to-1 mappings ----\n")
for old, new in SPECIFIC.items():
    toml_lines.append("[[redirects]]")
    toml_lines.append(f'  from = "{old}"')
    toml_lines.append(f'  to = "{new}"')
    toml_lines.append("  status = 301")
    toml_lines.append("  force = true")
    toml_lines.append("")

# Pattern redirects
toml_lines.append("# ---- Pattern redirects (catch-all groups) ----\n")
for from_pat, to, status in PATTERNS:
    toml_lines.append("[[redirects]]")
    toml_lines.append(f'  from = "{from_pat}"')
    toml_lines.append(f'  to = "{to}"')
    toml_lines.append(f"  status = {status}")
    toml_lines.append("  force = true")
    toml_lines.append("")

print("\n".join(toml_lines))

# Write a _redirects file too (alternative format Netlify also reads)
redirects_lines = [
    "# 301 Migration redirects (legacy WordPress URLs → new static site)",
    "# This file is read by Netlify in addition to netlify.toml.",
    "",
    "# ---- Specific 1-to-1 mappings ----",
]
for old, new in SPECIFIC.items():
    redirects_lines.append(f"{old:<55} {new:<45} 301!")
redirects_lines.append("")
redirects_lines.append("# ---- Pattern redirects ----")
for from_pat, to, status in PATTERNS:
    redirects_lines.append(f"{from_pat:<55} {to:<45} {status}!")

# Save outputs
with open("/tmp/redirects-toml.txt", "w") as f:
    f.write("\n".join(toml_lines))
with open("/tmp/redirects-file.txt", "w") as f:
    f.write("\n".join(redirects_lines))

# Stats
covered_specific = set(SPECIFIC.keys())
covered_patterns = []
for x in urls:
    p = x["url"].replace("https://phenotips.com", "") or "/"
    if p in covered_specific: continue
    if any(p.startswith(pat[:-1]) for pat, _, _ in PATTERNS):
        covered_patterns.append(p)

uncovered = []
for x in urls:
    p = x["url"].replace("https://phenotips.com", "") or "/"
    if p in covered_specific: continue
    if any(p.startswith(pat[:-1]) for pat, _, _ in PATTERNS): continue
    uncovered.append(p)

print(f"\n=== Coverage stats ===")
print(f"  Specific 1-to-1:  {len(covered_specific)}")
print(f"  Pattern matches:  {len(covered_patterns)}")
print(f"  Uncovered:        {len(uncovered)}")
print()
if uncovered:
    print("Uncovered URLs (will need additional decisions):")
    for u in uncovered:
        print(f"  - {u}")
