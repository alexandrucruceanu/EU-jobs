# Roadmap

## Completed

### Phase 1: Research & Planning ✅
- Analyzed `karpathy/jobs` architecture and US BLS data pipeline
- Selected ESCO API + ISCO-08 hierarchies as primary EU data source
- Mapped EU fields to existing BLS schema

### Phase 2: EU Scraper & Parser ✅
- Built `scrape_eu.py` for ESCO taxonomy download (436 ISCO-08 Unit Groups)
- Built `process_eu.py` for Markdown page generation
- Built `make_csv_eu.py` with EU-adapted structured data

### Phase 3: LLM Scoring Pipeline ✅
- Adapted `score.py` for Gemini 3.1 Flash-Lite with rate-limit handling
- Generated AI exposure scores (0–10) for all 436 occupations
- Moved API keys to `.env` (removed all hardcoded secrets)

### Phase 4: Frontend Visualization ✅
- Migrated `index.html` to EU terminology (ESCO, €, ISCO codes)
- Canvas-based treemap with 4 color layers (Growth, Pay, Education, AI Exposure)

### Phase 5: Multilingual i18n ✅
- Built `translate_ui.py` to translate UI into 23 additional EU languages
- Created `inject_native_titles.py` for official ESCO job titles
- Dynamic language switcher in the header (all 24 official EU languages)

### Phase 6: Real Eurostat Data ✅
- Integrated Eurostat 2023 census employment figures (198M total jobs)
- Built `fetch_eurostat.py` for ISCO 2-digit broadgroup employment data

### Phase 7: Methodology Transparency ✅
- Added data methodology disclaimer explaining imputed vs. exact metrics
- Translated disclaimer across all 24 languages

### Phase 8: Advanced Search ✅
- Added real-time search bar filtered by job title or 4-digit ISCO code
- Visual highlighting and dimming of matching/non-matching tiles

### Phase 9: Sector Domain Grouping ✅
- Created ISCO 2-digit → 19 BLS-style sector mapping in `build_site_data.py`
- Rendered domain borders and sector labels on the treemap canvas
- Translated all 19 sector labels across 24 languages

### Phase 10: Repo Cleanup & Publishing ✅
- Archived original US BLS pipeline files to `.archive/`
- Security audit: removed hardcoded API key, created `.env` + `.env.example`
- Published to GitHub: `alexandrucruceanu/EU-jobs`
- Deployed to GitHub Pages via Actions workflow

### Phase 11: Mobile Optimization ✅
- Implemented vertical stacking of categories for narrow viewports
- Added dynamic canvas height adjustment for better mobile scrolling
- Improved job title rendering logic to ensure visibility in significant cells

### Phase 12: Per-Country Breakdowns ✅
- Expanded `fetch_eurostat.py` to fetch employment data for all 27 EU member states
- Updated `make_csv_eu.py` with job scaling factors and wage level indices
- Dynamic region selection in the frontend with per-country JSON data files
- Fixed job inflation bug for small countries (e.g., Luxembourg: 4M → 307K)
- Fixed pay data to reflect country-specific wage levels

### Phase 13: Interactive Map View ✅
- Built `site/map.html` with choropleth map of Europe using Natural Earth 110m GeoJSON
- 4 metric toggles: Total Employment, Growth Outlook, Median Pay, AI Exposure
- Sorted country sidebar with color swatches and metric values
- Hover tooltips and click-to-treemap navigation
- Bidirectional map ↔ treemap navigation

### Phase 14: Localization & UI Parity ✅
- Migrated 15 "sad-funny" job market quotes to `i18n/*.json` (24 languages)
- Built dynamic quote randomization engine in `shared.js`
- Implemented glassmorphism cookie consent banner
- Corrected map projection and tiny-state positions (Malta)
- Unified header/footer styling across all views
- Added `robots.txt` for SEO

### Phase 15: Uncodixfy Portfolio Alignment ✅
- Adjusted CSS border-radii across map and treemap views to strict 8px
- Updated all UI transitions to a snappy 150ms ease
- Created `portfolio-meta.json` with multi-language elevator pitches and Tech Stack tags
- Created `portfolio-meta.json` with multi-language elevator pitches and Tech Stack tags
- Generated and embedded `logo-eu-jobs.png` and `preview-eu-jobs.png` for external portfolio rendering

### Phase 16: Premium Branding & SEO Optimization ✅
- Refined the premium logo (`logo-eu-jobs.png`) with a tighter, more professional crop
- Integrated a clickable header logo across all pages with interactive hover effects
- Implemented `sitemap.xml` for comprehensive search engine indexing
- Added `manifest.json` for PWA features and "Add to Home Screen" support
- Injected Schema.org JSON-LD structured data for improved rich search results
- Consistently applied canonical URL meta tags across the application

### Phase 17: Advanced Analytics & UX Suite ✅
- **2D Scatter Matrix & Quadrant Analysis** — 2D canvas visualization plotting AI Exposure (0-10) vs. Median Annual Pay (€) across 4 categorized quadrants with employment-scaled bubbles.
- **Faceted Multi-Dimensional Filters** — Real-time filtering by Sector Domain, Minimum AI Exposure slider, and Education levels.
- **Live Occupational Rankings** — Instant "Top 5 AI-Exposed" vs. "Most AI-Resilient" leaderboards updated dynamically on filter change.
- **ESCO Detail Drawer & Benchmark** — Glassmorphic slide-in profile featuring AI exposure rationale, national employment share, and dynamic salary benchmark comparisons vs. the EU27 average.
- **Dark & Light Mode** — Native theme toggle with responsive CSS custom variables, adaptive canvas rendering, and persistent storage.
- **High-Res PNG Export** — 2x resolution branded visual snapshot generator with title, country, view, and date tags.

### Phase 18: Personal AI Career Impact Calculator & Social Cards ✅
- **Interactive Career Quiz (`?quiz=1`)** — Instant career exposure assessment with live percentile ranking, wage comparison, and tailored vulnerability rationale.
- **1200x630 Canvas Share Card Generator** — Dynamic Canvas 2D engine rendering branded career impact cards with direct PNG download and 1-click social share intents (LinkedIn, X).

### Phase 19: AI Semantic Occupation Matcher & Suggestions Grid ✅
- **Freeform Job Title AI Matcher** — Client-side token, synonym, and Gemini rationale similarity scoring engine for modern or non-standard titles (e.g., "Prompt Engineer", "Growth Hacker", "Data Scientist").
- **Top 4 Selection Cards Grid** — Interactive selection modal displaying match confidence badges (e.g., `✨ 96% Match`) and AI exposure indicators mapping cleanly to official ISCO-08 roles.

### Phase 20: Embeddable Interactive Widget & Generator Modal ✅
- **Standalone Embed View (`site/embed.html`)** — Lightweight, responsive iframe visualizer supporting Treemap and Matrix views with country switching and layer controls.
- **In-App Embed Modal (`</> Embed`)** — Embed code generator with customizable dimensions, live interactive preview, and 1-click clipboard copy.
- **Universal Iframe CSP Headers** — Configured Nginx with `frame-ancestors *` and permissive embedding policies for media publishers and blogs.

### Phase 21: Country-vs-Country Side-by-Side Labor Benchmark Mode ✅
- **Comparative Dashboard (`⚖️ Compare Countries` / `?compare=1`)** — Dual country selectors comparing any two EU member states (e.g. Spain vs. Germany).
- **Real-Time Comparative KPIs** — Workforce population, weighted average annual pay, aggregate AI exposure index, and wages at AI risk with percentage deltas.
- **Sector Salary Benchmark Table** — Side-by-side wage ranking across all 19 ESCO sectors with color-coded wage gap badges.
- **Dual-Country 1200x630 Social Comparison Card Generator** — High-impact share card canvas engine with country flags, wage gap highlights, and social share links.
---

## Future Ideas

- [ ] Historical trend comparisons (2019 vs. 2024 employment shifts)
- [ ] ESCO skills/competences granular taxonomy graph overlay
- [ ] Scenario simulator for 2030 generative AI labor adoption
- [ ] Export filtered dataset to CSV / JSON in 1-click
- [x] Embeddable `<iframe />` widget for external blogs and news media
- [x] Side-by-side country-vs-country labor benchmark mode
- [x] AI Semantic Matcher for non-standard occupation titles
- [x] Personal AI Job Exposure quiz & 1200x630 share card generator
- [x] Dark/light theme toggle
- [x] Fix Eurostat earnings API fetch and multi-country scaling



