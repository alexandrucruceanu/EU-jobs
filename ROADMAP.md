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

---

## Future Ideas

- [ ] Historical trend comparisons (2019 vs. 2023 employment shifts)
- [ ] ESCO skills/competences overlay on the treemap
- [ ] Dark/light theme toggle
- [ ] Custom LLM prompt builder for community scoring layers
- [ ] Fix Eurostat earnings API fetch (currently returns 0 records)
- [ ] Regional (NUTS-2) sub-national breakdowns
