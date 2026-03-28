# Changelog

All notable changes to this project are documented in this file.

## [2.4.0] — 2026-03-28

### Added
- **Premium Branding Refinement** — Updated the app icon (`logo-eu-jobs.png`) to reduce background space for a cleaner, edge-to-edge look.
- **Interactive Header Logo** — Integrated the refined premium logo across all views as a clickable link to the homepage, including a 1.05x scale hover effect.
- **Full SEO Optimization** — Implemented `sitemap.xml` for efficient indexing and `manifest.json` for PWA support (installable on mobile).
- **Structured Data Integration** — Added JSON-LD (Schema.org) metadata to `index.html` and `map.html` to improve rich results in search engines.
- **Canonical URL Enforcement** — Consistently applied canonical links to prevent duplicate content indexing.


## [2.3.0] — 2026-03-28

### Added
- **Uncodixfy UI Alignment** — Updated structural components (buttons, dropdowns, cookie banners) to a strict 8px border-radius standard for a premium aesthetic.
- **Snappy Transitions** — Altered all dynamic animation logic across the platform from standard timings to snappy 150ms ease transitions.
- **Portfolio Meta-Data** — Created `portfolio-meta.json` with multi-lingual project descriptions and Tech Stack definitions.
- **Visual Artifacts** — Produced a tailored logo (`logo-eu-jobs.png`) and optimized interactive UI mockup (`preview-eu-jobs.png`), correctly referenced in `README.md`.

## [2.2.0] — 2026-03-25

### Added
- **Eurostat Earnings Data Fix** — Restored real median hourly earnings by fixing indicator codes (`MED_E_EUR`) and implementing a 2018 fallback for missing 2022 aggregate data.
- **ISCO-08 Depth Mapping** — Implemented 1-digit major group to 2nd-digit sub-major group data distribution for earnings metrics.

### Changed
- **Project Structure Reorganization** — Cleaned up the root directory and moved files into professional subfolders: `/data`, `/scripts`, `/docs`, `/raw_data`, and `/pages`.
- **Global Path Update** — Refactored all 14 utility scripts to support the new directory architecture.

## [2.1.0] — 2026-03-24

### Added
- **24-Language Localized Quotes** — 15 "sad-funny" job market quotes translated across all official EU languages, appearing randomly in the footer.
- **Dynamic i18n Quote Management** — Integrated `window.updateFunnyFooter()` into the shared translation engine in `shared.js`.
- **Cookie Consent Banner** — Functional cookie acceptance popup with glassmorphism design on both Treemap and Map views.
- **Search Engine Optimization** — Created `robots.txt` and verified meta tags for better discoverability.

### Fixed
- **Malta Position Correction** — Fixed the geographic coordinates for Malta on the Map view (Albers projection).

### Changed
- **UI Parity** — Unified header and footer styles between `index.html` (Treemap) and `map.html` (Map), ensuring a consistent premium look.

## [2.0.0] — 2026-03-23

### Added
- **27 EU member states** — Per-country data for all EU countries (AT, BE, BG, CY, CZ, DE, DK, EE, EL, ES, FI, FR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK)
- **Interactive map view** (`site/map.html`) — Choropleth map of Europe with 4 metric layers (Employment, Growth, Pay, AI Exposure)
- **Country summary data** (`site/data_summary.json`) — Aggregated statistics per country for map visualization
- **SVG map generator** — Python script to generate EU map paths from Natural Earth 110m GeoJSON
- **Region URL parameter** — `index.html?region=de` loads Germany directly
- **Map ↔ Treemap navigation** — Bidirectional links between map and treemap views

### Fixed
- **Job inflation for small countries** — Heuristic fallback job counts now scale proportionally to each country's real workforce size
- **Pay data not country-specific** — Added wage level indices (Eurostat earn_ses_annual) so pay reflects real country wage levels (e.g., Bulgaria ~€12K, Luxembourg ~€65K)
- **Eurostat earnings key mismatch** — `fetch_eurostat.py` saved as `"earnings_annual"` but CSV builder read `"earnings"` — fixed
- **Double ×2080 conversion** — Removed duplicate hourly-to-annual pay conversion in fetch script

### Changed
- `fetch_eurostat.py` — Expanded to fetch all 27 EU country codes; fixed earnings storage key
- `make_csv_eu.py` — Dynamic region processing with job scaling and wage level indices
- `build_site_data.py` — Generates per-country JSON files and `data_summary.json` with weighted averages
- `index.html` — Region selector with all 27 countries; dynamic data loading; map navigation link
- `i18n/en.json` and `i18n/es.json` — Added translation keys for all 27 EU member states

## [1.1.0] — 2026-03-20

### Added
- **Mobile-responsive layout** — Treemap categories stack vertically on small screens (<768px)
- **Enhanced label visibility** — Largest job cells in each category now prioritize title display
- **Dynamic canvas scaling** — Treemap height adjusts to fit vertical stacking on mobile

## [1.0.0] — 2026-03-19

### Added
- **436 ISCO-08 occupations** scraped from the official ESCO taxonomy API
- **Real Eurostat 2023 census data** — 198M total EU27 employment figures
- **AI exposure scoring** — Gemini 3.1 Flash-Lite scores (0–10) for every occupation
- **24-language support** — Full UI translation with official ESCO job titles
- **19 sector domain grouping** — Treemap organized by industry (Healthcare, Technology, Construction, etc.)
- **Real-time search** — Filter by job title or 4-digit ISCO code with visual highlighting
- **Methodology disclaimer** — Transparent data sourcing note in all languages
- **GitHub Pages deployment** — Auto-deploy via Actions workflow
- **Security hardening** — API keys moved to `.env`, `.env.example` template provided

### Changed
- Forked from [karpathy/jobs](https://github.com/karpathy/jobs) (US BLS data)
- Replaced US BLS scraper/parser with EU ESCO/ISCO-08 pipeline
- `score.py` refactored for Gemini API with rate-limit handling and UTF-8 support
- `build_site_data.py` now computes sector categories from ISCO 2-digit codes
- `index.html` rewritten for EU terminology (€, ESCO, ISCO codes, multilingual header)
- Currency display changed from USD ($) to EUR (€)

### Removed
- Original US BLS scraper, parser, and data files (moved to `.archive/`)
- Hardcoded API keys from source files

## [0.0.0] — 2024-xx-xx (Original)

Initial release by [Andrej Karpathy](https://github.com/karpathy/jobs) — US BLS occupational data with AI exposure treemap.
