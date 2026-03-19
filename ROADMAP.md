# EU Jobs Data Adaptation Roadmap

## Phase 1: Research and Planning
- [x] Analyze the `karpathy/jobs` architecture and data pipeline.
- [x] Identify the current US BLS dependencies (`scrape.py`, `process.py`, `parse_detail.py`).
- [x] Research and select the primary EU data source (ESCO API targeting ISCO-08 hierarchies).
- [x] Map the chosen EU data source fields to the existing US BLS fields (Title, Pay, Employment Count, Education, SOC code equivalent).

## Phase 2: Building the Scraper & Parser
- [x] Create a new scraping script (`scrape_eu.py`) to download 436 ISCO-08 broad economy group data.
- [x] Develop a new parsing script (`process_eu.py`) to clean and format the raw JSON into Markdown pages.
- [x] Update `make_csv_eu.py` to extract structured data and simulate EU weights for complete visualization.

## Phase 3: Adapting the LLM Pipeline
- [x] Modify `prompt.md` and `make_prompt.py` to reflect EU data terminology and specific labor frameworks.
- [x] Rearchitect `score.py` using Gemini 3.1 Flash-Lite with robust API rate limiting and UTF-8 console crash-proofing.
- [x] Run `score.py` to compute "AI Exposure" scores for 436 European ISCO-08 groups.

## Phase 4: Frontend Visualization & Launch
- [x] Adjust `build_site_data.py` to merge the EU CSV stats and the generated LLM scores into `site/data.json`.
- [x] Modify `site/index.html` to update any hardcoded text referring to US data, BLS, or USD ($) to instead refer to the EU, ESCO, and Euros (€).

## Phase 5: Global i18n Adaptation
- [x] Build an automatic translation layer (`translate_ui.py`) leveraging the Gemini API.
- [x] Distil all generic UI labels into an `en.json` primary dictionary.
- [x] Generate 23 additional European language JSON files and inject a dynamic header switcher into the `index.html`.

## Phase 6: Final Delivery
- [x] Complete a full 100% economy scrape (436 occupations).
- [x] Verify API robustness and multi-language switching perfectly mirrors the original repo functionality.
- [x] Finalized Documentation (`README.md`, `ROADMAP.md`).
