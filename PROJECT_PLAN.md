# PhenoTips Website Rebuild — Project Plan

> **Goal:** Rebuild PhenoTips.com as a clean, outcome-first, persona-driven website that leads with what customers accomplish — not with features. Inspired by Nest Genomics' clean design language, powered by the PhenoTips Design System.

---

## 1. Site Architecture

```
/                          → Home
/solutions/rare-disease    → Rare Disease
/solutions/cancer-genetics → Cancer Genetics
/solutions/health-systems  → Health Systems
/platform                  → Platform Overview (all features)
/roi-calculator            → ROI Calculator
/about                     → About / Our Story
/publications              → Case Studies + Papers
/resources                 → Blog + Speaker Series + Docs
/contact                   → Contact + Book Demo
```

---

## 2. Design System

### Foundation
- **CSS File:** `Design Reference/colors_and_type.css` — import first on every page
- **Icons:** Lucide via CDN (`https://unpkg.com/lucide@latest`)
- **Fonts:** IBM Plex Sans (headings, body), IBM Plex Serif (pull quotes), IBM Plex Mono (HPO codes, variants)
- **Logo:** `Design Reference/logo-phenotips-full.png`
- **Background asset:** `Design Reference/bg-lightblue-gradient.png`
- **Logo strip:** `Design Reference/logo-strip-lightblue.png`

### Color Principles
- Hero/section backgrounds: `--bg-sky-gradient` (diagonal) or `--bg-sky-gradient-soft` (vertical)
- Primary CTA: `--bg-brand` (`--pheno-500`)
- Headings: `--fg-brand` (`--pheno-700`)
- Body: `--fg-2` (`--neutral-700`)
- White-first surfaces everywhere
- Never: purple, pink, orange gradients

### Typography Rules
- Display headings: `--fw-light` (open, editorial)
- UI headings: `--fw-semibold`
- Eyebrow labels: ALL CAPS, `--ls-eyebrow: 0.14em`, `--fg-brand`
- Body: sentence case, `--fs-base` / `--fs-md`
- HPO codes: `ds-hpo` chip class, IBM Plex Mono

### Layout Rules
- 12-column grid, 24px gutter
- Max content width: 1200px (marketing), 72ch (reading blocks)
- Generous whitespace — match brochure breathing room
- Fixed nav: 64px height, frosted glass on scroll
- Cards: `--radius-lg` (12px), `--shadow-sm`, white bg, 24px padding
- No left-border-only card pattern

### Motion
- Duration: 120–360ms (`--dur-base: 200ms`)
- Easing: `--ease-out` for entrances
- Fades + 4–8px translates only
- No bouncy springs

### Do Not
- No purple/pink/orange gradients
- No repeating pedigree-motif backgrounds (deprecated)
- No cartoon illustrations or hand-drawn figures
- No emoji anywhere
- No exclamation marks
- No "revolutionary", "game-changing", "seamless" without proof

---

## 3. Navigation Structure

```
[Logo]    Solutions ▾    Platform    ROI Calculator    Publications    Resources    [Book a Demo]  [Login]
```

**Solutions dropdown:**
- Rare Disease
- Cancer Genetics
- Health Systems

**Platform:** Single page — full feature breakdown

**Sticky on scroll:** frosted glass nav (`backdrop-filter: blur(12px)`, `rgba(255,255,255,0.72)`)

---

## 4. Page Blueprints

### 4.1 Home (`index.html`)

| Section | Content |
|---|---|
| **Hero** | Sky gradient bg · Eyebrow: "THE GENOMIC HEALTH RECORD" · H1: "Shorten the diagnostic odyssey." · Subhead: "PhenoTips gives genetics teams a single, EHR-integrated platform to capture phenotypes, draw pedigrees, assess risk, and reach answers — faster." · CTAs: "Book a Demo" + "See How It Works" |
| **Social proof bar** | Logo strip: SickKids, Children's Mercy, CHU Sainte-Justine, Cambridge, BC Children's, Great Ormond Street, GOSH, Ambry Genetics |
| **Outcome pillars** (3 cards) | "Diagnose faster" · "Eliminate redundant data entry" · "Scale genomics across your network" |
| **Solutions nav** (3 persona tiles) | Rare Disease · Cancer Genetics · Health Systems |
| **Stats bar** | 30x faster diagnosis · 50% efficiency gain · 95% pedigree satisfaction · 100+ institutions |
| **Platform preview** | Short feature walkthrough — tabbed or scrolled |
| **Testimonials** | 3 rotating quotes w/ role + institution |
| **CTA section** | Dark brand bg · "Start shortening the diagnostic odyssey." · "Book a Demo" |
| **Footer** | Full sitemap + compliance chips + integrations |

---

### 4.2 Rare Disease (`solutions/rare-disease.html`)

| Section | Content |
|---|---|
| **Hero** | Eyebrow: "RARE DISEASE" · H1: "Reach the right diagnosis — years sooner." · Stat: "30x faster to a differential diagnosis" |
| **The challenge** | Pain: average 4–7 year diagnostic odyssey, patients touching 8 specialists |
| **How PhenoTips helps** | 4 outcome blocks: Capture every phenotype · Build the pedigree in minutes · Uncover the differential · Collaborate across institutions |
| **Feature deep-dives** | HPO capture, automated pedigrees, PhenomeCentral research sharing, EHR integration |
| **Proof** | Quotes from SickKids, Children's Mercy, Care4Rare |
| **CTA** | "Book a Demo" |

---

### 4.3 Cancer Genetics (`solutions/cancer-genetics.html`)

| Section | Content |
|---|---|
| **Hero** | Eyebrow: "CANCER GENETICS" · H1: "Run every risk model. Enter data once." · Stat: "Save 30 minutes per patient encounter" |
| **The challenge** | Pain: duplicate data entry across tools, risk models siloed, pedigrees redrawn |
| **How PhenoTips helps** | 4 outcome blocks: Patient enters data before arrival · Pedigree draws itself · All risk models in one click · Report generated automatically |
| **Feature deep-dives** | Pre-visit PPQ, CanRisk/IBIS/PREMM5/Gail/Tyrer-Cuzick, EHR-native workflow |
| **Proof** | GOSH, Cambridge, 95% pedigree satisfaction stat |
| **CTA** | "Book a Demo" |

---

### 4.4 Health Systems (`solutions/health-systems.html`)

| Section | Content |
|---|---|
| **Hero** | Eyebrow: "HEALTH SYSTEMS" · H1: "Unite every genetics team under one record." · Stat: "3 NHS Trusts. One platform." |
| **The challenge** | Pain: fragmented tools, siloed trusts, no shared view of a patient's genomic history |
| **How PhenoTips helps** | 4 outcome blocks: Connect EPRs and lab hubs · Standardize phenotyping across teams · Route WGS orders automatically · Report across the network |
| **Feature deep-dives** | FHIR/HL7 integration, Epic/Cerner embedding, multi-trust data model |
| **Proof** | Dr. Ajith Kumar (GOSH), Marc Tischkowitz (Cambridge) |
| **CTA** | "Book a Demo" |

---

### 4.5 Platform (`platform.html`)

| Section | Content |
|---|---|
| **Hero** | Eyebrow: "THE PLATFORM" · H1: "One end-to-end workflow. Nothing bolted on." |
| **Feature grid** | Genomic Health Record · Pedigree Maker · HPO Phenotyping · Pre-Visit Questionnaire · Cancer Risk Assessment · Variant Analysis · Report Generation · EHR Integration · Research Cloud |
| **Integration logos** | Epic, Cerner/Oracle, HL7 FHIR |
| **Compliance strip** | `HIPAA | GDPR | DSPT | SOC2 | CE+` |
| **CTA** | "Book a Demo" |

---

### 4.6 ROI Calculator (`roi-calculator.html`)

See Section 6 for full spec.

---

### 4.7 About (`about.html`)

| Section | Content |
|---|---|
| **Origin** | Founded 2011 at BC Children's Hospital · First clinical HPO implementation |
| **Mission** | "End the diagnostic odyssey for every patient." |
| **Team** | Key leadership cards |
| **Milestones** | 2011 founding → HPO → 100 institutions → NHS → Research Cloud |
| **Certifications** | HIPAA · GDPR · DSPT · SOC2 · CE+ |

---

## 5. Content Principles (All Pages)

### Voice
- **Clinical, confident, unadorned.** Like a senior genetic counselor: precise, evidence-led.
- Third person for product (`PhenoTips digitizes…`), second person for customer (`your patients`, `your workflow`)
- No exclamation marks. No emoji. No hype.

### Copy Structure (per section)
1. **Eyebrow** — ALL CAPS, `--ls-eyebrow`
2. **Outcome headline** — verb-first: "Diagnose faster", "Eliminate redundant entry", "Unite your network"
3. **Proof** — stat, quote, or named institution
4. **CTA** — "Book a Demo" or "See [specific outcome]"

### Verbs to lead with
`Accomplish · Diagnose · Eliminate · Streamline · Capture · Uncover · Unite · Deliver · Scale · Reduce · Generate · Connect`

---

## 6. ROI Calculator Spec

### Inputs (simple, 5 fields)
| Input | Label | Default |
|---|---|---|
| Patients/month | How many patients does your team see per month? | 100 |
| Staff (counselors + geneticists) | How many genetics staff? | 5 |
| Avg. time per new patient (min) | Current time spent per new patient encounter | 60 |
| Avg. time for cancer risk assessment (min) | Time spent per cancer risk assessment today | 45 |
| Cancer risk assessments/month | How many risk assessments per month? | 40 |

### Outputs (calculated live)
| Output | Formula | Display |
|---|---|---|
| Hours saved per month | `(patients × 0.50 × avgTimeNew/60) + (riskAssessments × 0.50 × avgTimeRisk/60)` | `XX hrs/month` |
| Hours saved per year | `hoursPerMonth × 12` | `XX hrs/year` |
| Staff cost saved/year | `hoursPerYear × $85` (avg genetic counselor hourly rate) | `$XXX,XXX/year` |
| Faster time to diagnosis | Fixed stat: "Up to 30x faster differential" | Badge |
| Efficiency gain | Fixed stat: "Up to 50% first-encounter efficiency" | Badge |

### Design
- Sky gradient hero with large calculated number animated on input change
- 2-column layout: inputs left, outputs right (stacked on mobile)
- "Book a Demo to See Your Full ROI" CTA below results

---

## 7. File Structure

```
PhenoTips Website2/
├── PROJECT_PLAN.md              ← this file
├── CONTENT_OUTLINE.md           ← content matrix
├── Design Reference/            ← design assets (existing)
├── site/
│   ├── index.html               ← Home
│   ├── platform.html            ← Platform overview
│   ├── roi-calculator.html      ← ROI Calculator
│   ├── about.html               ← About
│   ├── contact.html             ← Contact / Book Demo
│   ├── solutions/
│   │   ├── rare-disease.html
│   │   ├── cancer-genetics.html
│   │   └── health-systems.html
│   ├── css/
│   │   ├── design-tokens.css    ← copied from Design Reference/colors_and_type.css
│   │   └── site.css             ← global layout, nav, footer, components
│   ├── js/
│   │   └── main.js              ← nav scroll, lucide init, ROI calculator logic
│   └── assets/
│       ├── logo-phenotips-full.png
│       ├── logo-strip-lightblue.png
│       └── bg-lightblue-gradient.png
```

---

## 8. Tech Stack

- **Pure HTML/CSS/JS** — no framework, no build step required
- **CSS custom properties** from design system — single source of truth
- **Lucide icons** via CDN
- **IBM Plex fonts** via Google Fonts CDN
- **Responsive:** mobile-first, breakpoints at 768px and 1200px
- **No external JS dependencies** beyond Lucide

---

## 9. Agent Coordination

| Agent | Responsibility |
|---|---|
| **PM Agent** | Reviews this plan, tracks completion of each page, flags gaps |
| **Coding Agent** | Builds all HTML/CSS/JS files per blueprint specs |
| **Content Writer Agent** | Writes final copy for all pages, persona-specific tone, ROI content |
| **QA Agent** | Reviews each page: design fidelity, content accuracy, mobile responsiveness, link integrity |

### Completion Checklist (PM tracks)
- [ ] `site/css/design-tokens.css` created
- [ ] `site/css/site.css` created (nav, footer, global components)
- [ ] `site/js/main.js` created
- [ ] `site/index.html` complete + reviewed
- [ ] `site/solutions/rare-disease.html` complete + reviewed
- [ ] `site/solutions/cancer-genetics.html` complete + reviewed
- [ ] `site/solutions/health-systems.html` complete + reviewed
- [ ] `site/platform.html` complete + reviewed
- [ ] `site/roi-calculator.html` complete + reviewed
- [ ] `site/about.html` complete + reviewed
- [ ] `site/contact.html` complete + reviewed
- [ ] All pages: mobile responsive tested
- [ ] All pages: nav links functional
- [ ] All pages: CTAs linked to contact.html
- [ ] Design tokens consistent across all pages
- [ ] Copy: outcome-first, verb-led, no hype words

---

## 10. Quality Standards

### Every page must:
1. Use design tokens exclusively (no hardcoded hex values except in design-tokens.css)
2. Have a `<title>`, `<meta description>`, and OG tags
3. Include the compliance strip: `HIPAA | GDPR | DSPT | SOC2 | CE+`
4. Have at least one quote or stat as social proof
5. End with a CTA section leading to demo booking
6. Be readable on mobile (375px min width)
7. Use outcome-first headings (verb + accomplishment)
8. Never use emoji, exclamation marks, or hype words

---

*Last updated: 2026-04-24*
