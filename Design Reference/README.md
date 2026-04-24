# PhenoTips Design System

> A design system for **PhenoTips** — the world's first Genomic Health Record.
> Evolved from the PhenoTips visual language captured in the 2024 slide template
> and brochure set. Keeps the signature deep teal-blue mark and the soft sky
> aesthetic; drops the previous illustration library in favour of a cleaner,
> more clinical-minimal foundation.

---

## Who is PhenoTips?

PhenoTips is a clinical genomics platform used by genetics programs at
100+ institutions globally, including SickKids, BC Children's, Children's Mercy
Kansas City, and three NHS Trusts in the UK. It was founded in 2011 at BC
Children's Hospital and was the first clinical tool to implement the Human
Phenotype Ontology (HPO).

The product bundles a **Genomic Health Record**, pre-visit patient
questionnaires that auto-generate pedigrees, HPO phenotyping, embedded cancer
risk models (CanRisk V2, Tyrer-Cuzick, PREMM5, Gail), variant analysis, and
report generation. It's EHR-integrated (Epic, Cerner/Oracle, HL7-FHIR) and
certified HIPAA / GDPR / DSPT / CE+.

### Products represented

- **PhenoTips (core platform)** — the Genomic Health Record: patient records,
  pedigrees, HPO capture, variant review, report generation.
- **Pre-Visit Patient Questionnaire (PPQ)** — a patient-facing form that feeds
  the clinical record. Has specialty variants (Cardiac PPQ, General Genetics).
- **Research Cloud** — de-identified genomic research storage + collaboration,
  sold as Shared and Private tiers.

### Source materials

All source files live under `uploads/` and extracted intermediaries under
`scraps/` and `assets/pptx-raw/`:

- `uploads/2024 PhenoTips Slide Template2.pptx` — 77-slide AE sales toolkit +
  brand template. Theme colors and Arial baseline came from here.
- `uploads/BROCHURE PhenoTips Catalogue General.pdf` — the 20-page overview
  catalog. Primary source for product voice and positioning.
- `uploads/BROCHURE PPQ Overview.pdf` + `Cardiac PPQ.pdf` — PPQ-specific
  detail and specialty variant.
- `uploads/BROCHURE General Genetics.pdf`, `Rare Disease.pdf`,
  `Research Cloud.pdf` — specialty one-pagers.
- `phenotips.com` — public website, referenced for tone.

---

## Index

- `README.md` — you are here. Context, content fundamentals, visual foundations,
  iconography.
- `SKILL.md` — agent skill front-matter (for use in Claude Code).
- `colors_and_type.css` — **the foundation file.** CSS variables for all
  colors, type, spacing, radii, shadows, and motion. Import this first.
- `assets/` — logos, background textures, raw PPTX media.
- `preview/` — Design System tab cards (swatches, specimens, token previews).
- `slides/` — deck slide templates (title, section, content, quote, impact…).
- `ui_kits/phenotips/` — web-app UI kit: screens and components for the core
  product.
- `ui_kits/ppq/` — patient-facing Pre-Visit Questionnaire kit.

---

## CONTENT FUNDAMENTALS

### Voice

**Clinical, confident, unadorned.** The brand writes like a senior genetic
counselor: precise, evidence-led, and a little dry. Never breezy, never
startup-cutesy. Claims are backed by numbers or named institutions.

### Tone knobs

| Attribute | Setting | Example |
|---|---|---|
| Formality | Professional, not stiff | *"Deliver precision medicine"* — never *"Bring the future of medicine"* |
| Person | **Third person for product**, **second person for customer** | *"PhenoTips digitizes…"* + *"your patients"* / *"your workflow"* |
| Contractions | Sparingly used | *"it's"*, *"you're"* are fine; prefer full forms in headers |
| Emoji | **Never.** | — |
| Exclamation | **Never.** | — |

### Casing

- **Headings and slide titles use Title Case:**
  *"The Complete Genomic Health Record"*, *"Cancer Risk Assessment"*,
  *"Trusted by Leading Centers"*.
- **Eyebrow labels use ALL CAPS** with loose letter-spacing:
  `TARGETED QUESTIONNAIRES`, `EHR INTEGRATION`, `INCLUSIVITY & REPRESENTATION`.
- **Body uses sentence case.**
- **Proper product names are not tokenized:** write *"PhenoTips"* and
  *"Pre-Visit Patient Questionnaire"* (or *"PPQ"* after first use) as-is.

### Structural patterns

Copy tends to follow a three-beat rhythm:

1. **Capability verb + outcome noun** — *"Streamline test requisition with…"*
2. **Product feature** — *"Next Generation Phenotyping"*
3. **Bulleted proof** — *"Simple capture with: Predictive search /
   Suggestions / NLP of free text"*

Marketing pages and brochures use terse eyebrow + heading + bullet stacks,
not paragraph prose. Sales slides carry more connective text, but stay tight.

### Terminology to use verbatim

- *Genomic Health Record* (the product category claim; capitalized)
- *HPO* / *Human Phenotype Ontology* (expanded on first use)
- *pedigree* (never "family tree")
- *diagnostic odyssey* (the industry term for delayed diagnosis)
- *phenotyping*, *variant analysis*, *report generation* (workflow stages)
- Compliance reads as a run-together chip: `HIPAA | GDPR | DSPT | CE+`

### Examples — real copy

> **Pre-visit Patient Questionnaire**
> Send your patients a digital pre-visit questionnaire that automatically
> draws their pedigree before they arrive.

> **The Complete Genomic Health Record**
> Capture and harness structured, curated, and interoperable genomic data.

> **PhenoTips: Trusted by Leading Centers**
> Founded 2011 at BC Children's Hospital — born from clinical need.
> 100+ clinical institutions across North America, Europe, and beyond.

Note: short, declarative, evidence-anchored. No hype words ("revolutionary",
"game-changing", "seamless" is used sparingly and always paired with proof).

---

## VISUAL FOUNDATIONS

The brand's identity sits on three things: a **deep teal-blue mark**, a
**soft sky gradient** as the brand atmosphere, and **a lot of white space**.
Everything else is restraint.

### Colors

- **PhenoBlue** (`--pheno-700` = `#0E4368`) is the signature ink color —
  sampled directly from the logo mark. It appears as headings, the logo, and
  the "strong" brand surface.
- **Sky wash** (`--sky-200` → `--sky-400`) is the atmospheric background —
  soft, gradient-friendly, used on hero surfaces and slide headers.
- **Neutrals** are slightly blue-tinted grays so they sit comfortably against
  the blues.
- **Semantic colors are muted** — brick-red for danger, honey for warn,
  calm forest-green for success. Never neon; this is clinical software.

All tokens live in `colors_and_type.css`.

### Typography

- **IBM Plex Sans** for all UI, headings, and body. Modern, technical,
  medical-adjacent; a good successor to the brand's Arial baseline.
- **IBM Plex Serif** for editorial pull quotes and report-style contexts.
- **IBM Plex Mono** for IDs, HPO terms (*HP:0001250*), variants, and codes —
  a constant visual motif in the product.

> **Substitution flag:** the PPTX uses Arial. IBM Plex is the substitute —
> it's free from Google Fonts, reads clinical, and distinguishes the
> refreshed system. **If you need to revert to Arial**, swap
> `--font-sans` in `colors_and_type.css` and flag to the user.

Type scale is modular (see CSS). Display headings are `--fw-light` for that
wide-open editorial feel; UI headings are `--fw-semibold`.

### Backgrounds

- **White-first.** Most UI surfaces are pure white on a very faint neutral
  app-background (`--bg-2`).
- **Branded sections use a sky gradient** — `--bg-sky-gradient` diagonally,
  or `--bg-sky-gradient-soft` vertically. Never use it full-bleed on a
  dense content screen; reserve for heroes, dividers, and empty states.
- **Never** ship a page with a purple/pink/orange gradient. If you see one,
  it's wrong for this brand.
- No repeating patterns, textures, or photographic noise. The previous
  hand-drawn pedigree-motif backgrounds (circles, diamonds, connecting
  lines) are **deprecated** per user direction — do not recreate them.
- For photography: warm, clinical-realistic, never overly filtered. Use
  sparingly (one per slide deck max). B&W is acceptable for portraits.

### Corner radii

- Cards and panels: `--radius-lg` (12px).
- Buttons, inputs, chips: `--radius-md` (8px).
- Tight chips and tags: `--radius-sm` (4px).
- Status dots, avatars, and HPO badges sometimes use `--radius-pill`.
- **No bubbly 24px+ everywhere** — this isn't a consumer app.

### Shadows

Shadow color is tinted with the brand blue (`rgba(14, 67, 104, …)`) so
elevations feel native to the palette. All shadows are soft, large-radius,
low-opacity. **Avoid hard black shadows.**

- `--shadow-xs` — 1px hairline for subtle elevation
- `--shadow-sm` — resting card
- `--shadow-md` — hovered card / dropdown
- `--shadow-lg` — floating panel / modal
- `--shadow-xl` — high-emphasis modal, command palette
- `--shadow-focus` — 3px blue focus ring, used on all interactive elements

### Borders

- 1px hairlines are the primary separator, not shadows. `--border-1`.
- Use `--border-brand` (`--pheno-300`) only on branded containers — never
  on every card.
- **Never use a colored left-border-only card pattern.** It reads dated and
  isn't in the PhenoTips visual vocabulary.

### Hover and press states

- **Hover**: darken color by one step (e.g., `--pheno-500` → `--pheno-600`),
  OR apply `--shadow-md` to cards. Never change size on hover.
- **Press**: shift color down two steps AND apply `transform: translateY(1px)`.
- **Focus**: `--shadow-focus` ring, never remove the outline.
- **Disabled**: `opacity: 0.5` + `cursor: not-allowed`.

### Motion

- Duration: 120–360ms. Default `--dur-base` (200ms).
- Easing: `--ease-out` for entrances, `--ease-in` for exits, `--ease-inout`
  for state swaps.
- **No bouncy springs, no elastic.** Clinical software doesn't bounce.
- Fades and slight translates (4–8px) are the dominant motion vocabulary.
- Long scroll-triggered animations are inappropriate for the product UI.
  They're acceptable on marketing pages if kept subtle.

### Layout rules

- **12-column grid**, 24px gutter baseline.
- **Generous whitespace** — match the brochures, which breathe a lot.
- Fixed elements: top navigation (64px), sidebar (240px expanded / 64px
  collapsed), slide footer (48px with logo mark, right-aligned).
- Content max-width for reading blocks: **72ch**. For dashboards, 1440px.

### Transparency and blur

Used sparingly. The two accepted uses:
1. **Frosted glass on sticky headers** — `backdrop-filter: blur(12px)` over
   a `rgba(255,255,255,0.72)` surface, with a hairline `--border-1`.
2. **Overlay scrims on images** — linear-gradient from transparent to
   `rgba(5, 33, 58, 0.6)` for ensuring text contrast on photography.

Never glassmorphic panels in the body of the UI. Never gradient-over-solid
card stacking.

### Cards

Default card:
- Background `--bg-1` (white)
- `--radius-lg` (12px)
- `--border-1` (1px `--neutral-200`) OR `--shadow-sm` — not both
- Padding: `--space-5` (24px) minimum

Emphasized/branded card:
- Background `--bg-wash` (`--pheno-50`)
- `--border-brand` hairline
- Same radius and padding

### Illustrations

Per user direction, the previous hand-drawn character illustrations
(clinicians, mothers, patients, pedigree motifs) from the PPTX are **NOT
carried forward**. When an illustration slot is needed:
- **Prefer structured diagrams** — real pedigrees, real HPO trees, real
  product screenshots — over drawn figures.
- If a decorative break is required, use a **simple geometric composition**
  in the blue palette: a soft gradient disc, or a lightweight line-art
  pedigree symbol set (square/circle/line vocabulary) rendered in
  `--pheno-200` / `--sky-300`.
- Never cartoon characters, never hand-drawn people.

---

## ICONOGRAPHY

PhenoTips does not ship a proprietary icon font in the materials provided.
The PPTX uses a small set of flat, single-color iconographic glyphs inside
circular badges (clipboard, bar-chart, paper-airplane, people, DNA bars).

### System adopted

**Lucide** (https://lucide.dev) — a clean, consistent, line-style open
icon library. 1.5px stroke by default. Reasons:
- Line style matches PhenoTips' restrained clinical aesthetic
- Broad coverage for healthcare (`activity`, `stethoscope`, `dna`,
  `clipboard-list`, `git-merge` for pedigree branches)
- Trivial to use via CDN (no build step required)

**CDN usage:**

```html
<!-- Load once in <head> -->
<script src="https://unpkg.com/lucide@latest"></script>
<!-- Icons in markup -->
<i data-lucide="dna"></i>
<i data-lucide="clipboard-list"></i>
<!-- Activate after DOM ready -->
<script>lucide.createIcons();</script>
```

Or import individual SVGs directly from `https://unpkg.com/lucide-static/icons/NAME.svg`.

> **Substitution flag:** PhenoTips itself does not publish an icon set in
> the materials I was given. Lucide is the closest match to the existing
> visual weight. If the product's actual icon font/sprite is available,
> swap it in and document its usage here.

### Rules

- **Stroke only**, 1.5–2px. No filled icon sets.
- **Single color**, inherited from `currentColor`. Tint the parent with
  `--pheno-700` for brand, `--fg-3` for neutral UI, `--danger-500` for
  destructive.
- **16 / 20 / 24 px grid sizes.** No odd pixel sizes.
- **Never mix line-style and solid icons** in the same surface.

### Emoji

**Not used.** Emoji are out of vocabulary for PhenoTips. Use a Lucide
icon, a text label, or a colored status dot instead.

### Unicode as icons

Acceptable in very small doses:
- Arrows: `→` `↳` `▸` in headers and breadcrumbs
- Middle dot `·` as a meta separator
- Pipe `|` for compliance runs (`HIPAA | GDPR | DSPT | CE+`)

### Logo

- `assets/logo-phenotips-full.png` — full wordmark lockup (primary).
- `assets/logo-strip-lightblue.png` — horizontal strip with logo on sky
  gradient, for use as slide headers.

The logo is **PhenoBlue** (`#0E4368`) on light. On dark or branded fills,
a white mark should be produced (not provided in the materials — flag to
user for a vector version).

---

## Brochures & sales collateral

Persona-led sales collateral follows a documented 6-panel trifold rhythm —
**Pain → Workflow → Payoff** on the inner spread, with front cover, inner
flap, and back cover on the outside. Full anatomy in
[`brochures/persona-trifold.md`](brochures/persona-trifold.md). Use it
whenever PhenoTips collateral needs to speak to a specific buyer persona
(role, specialty, or service line).

Key conventions lifted from the PhenoTips persona trifolds:
- Section hits in the form `01 — THE DAY TODAY` / `02 — THE PHENOTIPS DAY` / `03 — THE PAYOFF`
- Quantified voice — minutes saved, tools touched, percentages, named vendors
- Quotes attributed to roles and service lines, not named individuals
- Mandatory back-cover strip: trust + compliance + integrations + QR

---

## Previewing the system

Open any file under `preview/` to see the tokens rendered. Each registered
card under the Design System tab shows a single concept (color scale,
type specimen, component state, etc). Slide templates under `slides/` and
UI screens under `ui_kits/*/index.html` are live, interactive previews
of how the system composes.
