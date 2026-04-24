# PhenoTips Website

A clean, outcome-first redesign of phenotips.com. Persona-led, evidence-anchored, and built on the PhenoTips Design System (IBM Plex + PhenoBlue palette).

## Site structure

```
site/
├── index.html                     ← Home
├── platform.html                  ← Platform overview (all features)
├── roi-calculator.html            ← Three-stream ROI model
├── webinars.html                  ← Speaker Series
├── publications.html              ← Case studies + peer-reviewed papers
├── about.html                     ← Our story
├── team.html                      ← The team
├── contact.html                   ← Book a demo
├── solutions/
│   ├── rare-disease.html
│   ├── cancer-genetics.html
│   └── health-systems.html
├── css/
│   ├── design-tokens.css          ← Design system foundation
│   └── site.css                   ← Layout, components, motion
├── js/
│   └── main.js                    ← Nav, tabs, ROI calculator, scroll-reveal
└── assets/
    ├── logo-phenotips-full.png
    ├── bg-lightblue-gradient.png
    └── logos/                     ← Customer + integration partner SVGs
```

## Local preview

It's pure HTML/CSS/JS — no build step. From the repo root:

```sh
cd site
python3 -m http.server 8000
# open http://localhost:8000
```

Or open `site/index.html` directly in a browser.

## Stack

- Pure HTML / CSS / JS, no framework, no build
- IBM Plex Sans / Serif / Mono via Google Fonts CDN
- Lucide icons via CDN
- CSS custom properties (design tokens) as the single source of truth
- Mobile-first responsive — breakpoints at 768px and 1024px
- Respects `prefers-reduced-motion`

## Reference

- [`PROJECT_PLAN.md`](PROJECT_PLAN.md) — site architecture, design system, agent coordination
- [`CONTENT_OUTLINE.md`](CONTENT_OUTLINE.md) — page-by-page content spec, persona matrix, voice rules
- `Design Reference/` — design system source: tokens, brand guidelines, logo
- `site/assets/logos/README.md` — customer and integration logo conventions

## Outstanding before launch

- `contact.html` form `action` needs a real backend (HubSpot, Formspree, etc.)
- `Login` link → real app URL
- Privacy / Terms pages
- Real product screenshots (current pages use stylized mockups)
- Replace placeholder customer SVGs with official institutional logos when available
