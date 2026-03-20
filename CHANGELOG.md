# Changelog

All notable changes to this project are documented in this file.

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
