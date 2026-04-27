"""
PhenoTips static site — technical SEO/AEO injection.

Adds:
  - canonical, twitter cards, og:image, robots meta on every page
  - Organization JSON-LD (site-wide) + per-page schema
  - sitemap.xml, robots.txt, llms.txt at /site/

Canonical base: https://phenotips.com (the eventual home).
If you keep canonicals on a staging URL instead, change CANONICAL_BASE.
"""
import re, json, html as htmllib
from pathlib import Path
from datetime import datetime, timezone

ROOT          = Path("/Users/parkerlachance1/Documents/PhenoTips Website2/site")
CANONICAL     = "https://phenotips.com"
SITE_NAME     = "PhenoTips"
TWITTER_HANDLE = "@phenotips"

# ---------- Site-wide Organization schema ----------
ORG = {
    "@context": "https://schema.org",
    "@type":    "Organization",
    "name":     "PhenoTips",
    "alternateName": "PhenoTips Inc.",
    "url":      CANONICAL,
    "logo":     f"{CANONICAL}/assets/logo-phenotips-full.png",
    "description": "PhenoTips is the unified genomics workflow solution — a clinical platform for phenotype capture, pedigree drawing, hereditary risk assessment, and EHR-integrated genetic test requisition. Trusted by 100+ institutions worldwide.",
    "foundingDate": "2012",
    "founder": [
        {"@type": "Person", "name": "Orion Buske", "jobTitle": "Co-founder & CEO"},
        {"@type": "Person", "name": "Pawel Buczkowicz", "jobTitle": "Co-founder & COO"},
        {"@type": "Person", "name": "Michael Brudno", "jobTitle": "Co-founder & Chairman"},
    ],
    "sameAs": [
        "https://www.linkedin.com/company/phenotips/",
        "https://www.youtube.com/@phenotips",
        "https://twitter.com/phenotips",
        "https://bsky.app/profile/phenotips.bsky.social",
    ],
    "contactPoint": [{
        "@type": "ContactPoint",
        "contactType": "Sales",
        "url": f"{CANONICAL}/contact.html",
    }],
    "address": {"@type": "PostalAddress", "addressCountry": "CA"},
}

# ---------- Page metadata catalog ----------
# slug → (path on site, og_path, type, description, schema_builder)
PAGES = [
    # (file, canonical_path, page_title, page_desc, schema_type)
    ("index.html",                            "/",                                "PhenoTips — The Unified Genomics Workflow Solution",                          "PhenoTips gives genetics teams one EHR-integrated platform to capture phenotypes, draw pedigrees, run every risk model, and reach answers — faster.", "WebSite"),
    ("platform.html",                         "/platform",                        "Platform — PhenoTips",                                                        "One end-to-end solution: pedigrees, HPO phenotyping, cancer risk assessment, variant analysis, AI-assisted test ordering, and EHR integration via SMART on FHIR.", "SoftwareApplication"),
    ("roi-calculator.html",                   "/roi-calculator",                  "ROI Calculator — PhenoTips",                                                  "Calculate the full value PhenoTips delivers: reclaimed clinical capacity, fewer duplicate tests, and a shortened diagnostic odyssey.", "WebPage"),
    ("about.html",                            "/about",                           "About — PhenoTips",                                                           "Founded in 2012 at the University of Toronto and SickKids — the first clinical tool to operationalize the Human Phenotype Ontology.", "AboutPage"),
    ("team.html",                             "/team",                            "The Team — PhenoTips",                                                        "Decades of clinical experience: co-founders, leadership, product, engineering, and customer success.", "AboutPage"),
    ("contact.html",                          "/contact",                         "Book a Demo — PhenoTips",                                                     "See PhenoTips in your workflow. Discovery call tailored to your specialty, walkthrough of your current workflow, ROI and implementation roadmap.", "ContactPage"),
    ("press.html",                            "/press",                           "Press & News — PhenoTips",                                                    "Press coverage and news about PhenoTips — funding, partnerships, product launches, and the institutions deploying our platform.", "CollectionPage"),
    ("publications.html",                     "/publications",                    "Publications & Case Studies — PhenoTips",                                     "Peer-reviewed papers, clinical case studies, and press features on PhenoTips.", "CollectionPage"),
    ("webinars.html",                         "/webinars",                        "Webinars & Speaker Series — PhenoTips",                                       "Monthly webinars and a podcast for genetics professionals — featuring leading clinicians, counselors, and researchers in clinical genomics.", "CollectionPage"),
    ("solutions/rare-disease.html",           "/solutions/rare-disease",          "Rare Disease — PhenoTips",                                                    "Reach the right diagnosis 3× faster. Structured HPO phenotyping, auto-drawn pedigrees, and case matching against global rare disease cohorts.", "Service"),
    ("solutions/cancer-genetics.html",        "/solutions/cancer-genetics",       "Cancer Genetics — PhenoTips",                                                 "Automated patient intake. Integrated cancer risk assessment. PhenoTips consolidates pedigrees, all major risk models, and EHR documentation.", "Service"),
    ("solutions/health-systems.html",         "/solutions/health-systems",        "Health Systems — PhenoTips",                                                  "A single solution that unites all genetics teams. PhenoTips connects EPRs, lab hubs, and clinical teams across multi-site networks.", "Service"),
    ("news/gapp-announcement.html",           "/news/gapp-announcement",          "GAPP Announcement — PhenoTips",                                               "A $5.4M Genome Canada GAPP-funded initiative led by PhenoTips and IWK Health, with five Canadian health institutions, brings AI to genomic test requisition.", "NewsArticle"),
    ("case-studies/addenbrooke.html",         "/case-studies/addenbrooke",        "Addenbrooke's Hospital Case Study — PhenoTips",                               "How Addenbrooke's Hospital (Cambridge University Hospitals) modernized its medical genetics department with PhenoTips.", "Article"),
]

OG_IMAGE = f"{CANONICAL}/assets/og-default.png"

def build_page_schema(file_path, canonical_url, title, description, schema_type):
    """Return per-page JSON-LD as a dict, or None."""
    if schema_type == "WebSite":
        return {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "url": canonical_url,
            "name": SITE_NAME,
            "description": description,
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": CANONICAL},
        }
    if schema_type == "SoftwareApplication":
        return {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "PhenoTips",
            "url": canonical_url,
            "applicationCategory": "HealthApplication",
            "applicationSubCategory": "Clinical genomics platform",
            "operatingSystem": "Web-based · SMART on FHIR",
            "description": description,
            "offers": {"@type": "Offer", "url": f"{CANONICAL}/contact"},
            "featureList": [
                "HPO phenotyping",
                "Pedigree drawing (auto-generated from patient questionnaire)",
                "Cancer risk assessment (CanRisk, Tyrer-Cuzick, BRCAPRO, Gail, PREMM5)",
                "Variant analysis with phenotype context",
                "AI-assisted genomic test requisition",
                "Clinical report generation",
                "EHR integration via SMART on FHIR (Epic, Oracle Health/Cerner)",
            ],
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": CANONICAL},
        }
    if schema_type == "Service":
        # Solution pages
        return {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": title.split(" — ")[0],
            "url": canonical_url,
            "description": description,
            "provider": {"@type": "Organization", "name": SITE_NAME, "url": CANONICAL},
            "serviceType": "Clinical genomics software",
            "areaServed": ["United States", "Canada", "United Kingdom", "European Union"],
        }
    if schema_type == "NewsArticle":
        return {
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": "U of T Startup PhenoTips, Health Institutions Launch National AI Initiative to Solve Bottleneck in Genomic Medicine",
            "url": canonical_url,
            "datePublished": "2026-04-07",
            "dateModified": "2026-04-07",
            "image": [f"{CANONICAL}/assets/news/gapp-hero.png"],
            "author": {"@type": "Organization", "name": "U of T Entrepreneurs", "url": "https://entrepreneurs.utoronto.ca/"},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": CANONICAL,
                          "logo": {"@type": "ImageObject", "url": f"{CANONICAL}/assets/logo-phenotips-full.png"}},
            "description": description,
            "about": [
                {"@type": "Thing", "name": "Clinical Intelligence for Phenotyping and Genomics Research (CIPHER) network"},
                {"@type": "Thing", "name": "SmartRequisition"},
                {"@type": "Thing", "name": "Genomic Applications Partnership Program (GAPP)"},
            ],
        }
    if schema_type == "Article":
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "Pedigree Software Revolutionizes Medical Genetics Department",
            "url": canonical_url,
            "datePublished": "2023-12-11",
            "dateModified": "2023-12-11",
            "image": [f"{CANONICAL}/assets/case-studies/addenbrooke-hero.png"],
            "author": {"@type": "Organization", "name": SITE_NAME, "url": CANONICAL},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "url": CANONICAL,
                          "logo": {"@type": "ImageObject", "url": f"{CANONICAL}/assets/logo-phenotips-full.png"}},
            "description": description,
            "about": {"@type": "Thing", "name": "Cambridge University Hospitals NHS Foundation Trust"},
            "mentions": [
                {"@type": "Person", "name": "Marc Tischkowitz", "jobTitle": "Consultant Clinical Geneticist"},
            ],
        }
    if schema_type == "AboutPage":
        return {
            "@context": "https://schema.org",
            "@type": "AboutPage",
            "url": canonical_url,
            "name": title.split(" — ")[0],
            "description": description,
            "mainEntity": {"@type": "Organization", "name": SITE_NAME, "url": CANONICAL},
        }
    if schema_type == "ContactPage":
        return {
            "@context": "https://schema.org",
            "@type": "ContactPage",
            "url": canonical_url,
            "name": title.split(" — ")[0],
            "description": description,
            "mainEntity": {"@type": "Organization", "name": SITE_NAME, "url": CANONICAL},
        }
    if schema_type == "CollectionPage":
        return {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "url": canonical_url,
            "name": title.split(" — ")[0],
            "description": description,
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": CANONICAL},
        }
    if schema_type == "WebPage":
        return {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "url": canonical_url,
            "name": title.split(" — ")[0],
            "description": description,
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": CANONICAL},
        }
    return None


def build_breadcrumb(file_path, canonical_url, title):
    """Optional BreadcrumbList for sub-pages."""
    parts = file_path.split("/")
    if len(parts) < 2:
        return None  # Root pages — no breadcrumb
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": CANONICAL + "/"}]
    accum = ""
    for i, p in enumerate(parts[:-1], start=2):
        accum += "/" + p
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": p.replace("-", " ").title(),
            "item": CANONICAL + accum,
        })
    items.append({
        "@type": "ListItem",
        "position": len(parts) + 1,
        "name": title.split(" — ")[0],
        "item": canonical_url,
    })
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def inject_into_page(file_path, canonical_path, title, description, schema_type):
    full_path = ROOT / file_path
    if not full_path.exists():
        print(f"  ✗ {file_path}: NOT FOUND")
        return False

    txt = full_path.read_text()
    canonical_url = CANONICAL + canonical_path
    desc_safe = htmllib.escape(description, quote=True)
    title_safe = htmllib.escape(title, quote=True)

    # Build the SEO block to inject before </head>
    seo_block_lines = [
        f'  <link rel="canonical" href="{canonical_url}">',
        f'  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
        f'  <meta property="og:url" content="{canonical_url}">',
        f'  <meta property="og:site_name" content="PhenoTips">',
        f'  <meta property="og:image" content="{OG_IMAGE}">',
        f'  <meta property="og:image:width" content="1200">',
        f'  <meta property="og:image:height" content="630">',
        f'  <meta property="og:locale" content="en_US">',
        f'  <meta name="twitter:card" content="summary_large_image">',
        f'  <meta name="twitter:site" content="{TWITTER_HANDLE}">',
        f'  <meta name="twitter:title" content="{title_safe}">',
        f'  <meta name="twitter:description" content="{desc_safe}">',
        f'  <meta name="twitter:image" content="{OG_IMAGE}">',
        '',
        f'  <!-- SEO: site-wide Organization schema -->',
        '  <script type="application/ld+json">' + json.dumps(ORG, separators=(",", ":")) + '</script>',
    ]

    page_schema = build_page_schema(file_path, canonical_url, title, description, schema_type)
    if page_schema:
        seo_block_lines.append('  <!-- SEO: per-page schema -->')
        seo_block_lines.append('  <script type="application/ld+json">' + json.dumps(page_schema, separators=(",", ":")) + '</script>')

    breadcrumb = build_breadcrumb(file_path, canonical_url, title)
    if breadcrumb:
        seo_block_lines.append('  <!-- SEO: breadcrumb schema -->')
        seo_block_lines.append('  <script type="application/ld+json">' + json.dumps(breadcrumb, separators=(",", ":")) + '</script>')

    seo_block = "\n".join(seo_block_lines) + "\n"

    # Strip any previous SEO block we added (so re-runs are idempotent)
    txt = re.sub(
        r'\s*<link rel="canonical"[^>]*>.*?<!-- SEO:.*?</script>\s*\n',
        "\n",
        txt,
        flags=re.S,
    )
    # Strip duplicate canonical or twitter cards that might exist
    txt = re.sub(r'\s*<link rel="canonical"[^>]*>\n', "\n", txt)
    txt = re.sub(r'\s*<meta name="robots" content="index,follow[^"]*">\n', "\n", txt)
    txt = re.sub(r'\s*<meta property="og:url"[^>]*>\n', "\n", txt)
    txt = re.sub(r'\s*<meta property="og:site_name"[^>]*>\n', "\n", txt)
    txt = re.sub(r'\s*<meta property="og:image[^"]*"[^>]*>\n', "\n", txt)
    txt = re.sub(r'\s*<meta property="og:locale"[^>]*>\n', "\n", txt)
    txt = re.sub(r'\s*<meta name="twitter:[^"]+"[^>]*>\n', "\n", txt)
    txt = re.sub(r'\s*<script type="application/ld\+json">[^<]*</script>\n', "\n", txt)

    # Insert just before </head>
    if "</head>" not in txt:
        print(f"  ✗ {file_path}: no </head> tag")
        return False
    txt = txt.replace("</head>", seo_block + "</head>", 1)
    full_path.write_text(txt)
    return True


# ---------- Run page injection ----------
print("=== Injecting SEO into pages ===")
for file_path, canonical_path, title, description, schema_type in PAGES:
    ok = inject_into_page(file_path, canonical_path, title, description, schema_type)
    print(f"  {'✓' if ok else '✗'}  {file_path}  ({schema_type})")

# ---------- sitemap.xml ----------
print("\n=== Generating sitemap.xml ===")
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
priorities = {
    "/": "1.0",
    "/platform": "0.9",
    "/solutions/rare-disease": "0.9",
    "/solutions/cancer-genetics": "0.9",
    "/solutions/health-systems": "0.9",
    "/contact": "0.9",
    "/roi-calculator": "0.8",
    "/about": "0.7",
    "/team": "0.7",
    "/webinars": "0.7",
    "/publications": "0.7",
    "/press": "0.7",
    "/news/gapp-announcement": "0.6",
    "/case-studies/addenbrooke": "0.6",
}
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for _, canonical_path, _, _, _ in PAGES:
    pr = priorities.get(canonical_path, "0.5")
    sitemap.append(f"  <url>")
    sitemap.append(f"    <loc>{CANONICAL}{canonical_path}</loc>")
    sitemap.append(f"    <lastmod>{today}</lastmod>")
    sitemap.append(f"    <changefreq>monthly</changefreq>")
    sitemap.append(f"    <priority>{pr}</priority>")
    sitemap.append(f"  </url>")
sitemap.append("</urlset>")
(ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n")
print(f"  ✓ sitemap.xml ({len(PAGES)} URLs)")

# ---------- robots.txt ----------
print("\n=== Generating robots.txt ===")
robots = f"""# PhenoTips robots.txt
# Tells search engines and AI engines what they can crawl.

User-agent: *
Allow: /
Disallow: /assets/team/   # block bulk team-photo scraping; pages still index
Disallow: /uploads/       # ignore any leftover Claude Design artifacts

# Explicitly allow major AI crawlers — supports AEO (Answer Engine Optimization).
# These bots feed content to ChatGPT, Claude, Perplexity, Google AI Overviews, etc.

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: Amazonbot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: cohere-ai
Allow: /

User-agent: facebookexternalhit
Allow: /

# Sitemap
Sitemap: {CANONICAL}/sitemap.xml
"""
(ROOT / "robots.txt").write_text(robots)
print(f"  ✓ robots.txt")

# ---------- llms.txt (AEO standard, draft spec by Jeremy Howard / Answer.AI) ----------
print("\n=== Generating llms.txt ===")
llms = f"""# PhenoTips

> The Unified Genomics Workflow Solution. PhenoTips gives genetics teams one EHR-integrated platform to capture phenotypes, draw pedigrees, run every cancer risk model, assist with genomic test ordering, and reach diagnostic answers — faster.

## About PhenoTips

PhenoTips is a clinical genomics platform used at 100+ institutions worldwide, including SickKids (Toronto), Children's Mercy (Kansas City), CHU Sainte-Justine (Montreal), BC Children's Hospital, Cambridge University Hospitals NHS Trust, and Great Ormond Street Hospital NHS Trust. The company was founded in 2012 as a research collaboration between the University of Toronto and SickKids Hospital — and was the first clinical tool to operationalize the Human Phenotype Ontology (HPO).

The platform integrates with Epic and Oracle Health (Cerner) as a SMART on FHIR app, and is HIPAA, GDPR, DSPT, SOC2, and CE+ compliant.

## Key outcomes

- 3× faster to a differential diagnosis (vs. unstructured workflows; published outcomes data)
- 50% efficiency gain on first-patient encounters (with pre-visit questionnaire)
- 30 minutes saved per cancer risk assessment (running CanRisk, Tyrer-Cuzick, BRCAPRO, Gail, PREMM5 from one shared pedigree)
- Right data on every genetic test requisition the first time (digital, standardized pedigrees)

## Product capabilities

- HPO-based phenotype capture (concept recognition from clinical notes)
- Auto-drawn pedigrees (from pre-visit patient questionnaire)
- Hereditary cancer risk assessment (5 models from one pedigree)
- Variant analysis with phenotype context
- AI-assisted genomic test recommendation (SmartRequisition / CIPHER network)
- Clinical report generation
- EHR integration (Epic, Oracle Health/Cerner) via SMART on FHIR
- Multi-site network rollout for health systems

## Solutions

- [Rare Disease]({CANONICAL}/solutions/rare-disease): Reach the right diagnosis 3× faster.
- [Cancer Genetics]({CANONICAL}/solutions/cancer-genetics): Automated intake. Integrated risk assessment.
- [Health Systems]({CANONICAL}/solutions/health-systems): A single solution that unites all genetics teams.

## Recent news

- [National AI Initiative for Genomic Medicine (CIPHER / SmartRequisition)]({CANONICAL}/news/gapp-announcement) — April 7, 2026. $5.4M Genome Canada GAPP-funded initiative led by PhenoTips and IWK Health, with five Canadian health institutions.

## Case studies

- [Cambridge — Addenbrooke's Hospital]({CANONICAL}/case-studies/addenbrooke): How Addenbrooke's Hospital modernized its medical genetics department with PhenoTips.

## Resources

- [Speaker Series (webinars)]({CANONICAL}/webinars) — 30+ episodes on clinical genetics and genomic medicine.
- [Publications]({CANONICAL}/publications) — Peer-reviewed papers and case studies.
- [Press]({CANONICAL}/press) — Press coverage and announcements.

## Contact

- [Book a Demo]({CANONICAL}/contact) — Tailored discovery call + walkthrough + ROI.
- Web: {CANONICAL}
- LinkedIn: https://www.linkedin.com/company/phenotips/
- YouTube: https://www.youtube.com/@phenotips

## Optional

- [Sitemap (XML)]({CANONICAL}/sitemap.xml)
- [Privacy Policy]({CANONICAL}/privacy-policy)
- [Terms of Use]({CANONICAL}/terms-of-use)
"""
(ROOT / "llms.txt").write_text(llms)
print(f"  ✓ llms.txt")
print("\n=== Done ===")
