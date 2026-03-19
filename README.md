# European Job Market Visualizer

A research tool for visually exploring **European Skills, Competences, Qualifications and Occupations (ESCO)** data, specifically adapted from the US BLS framework to cover the entire European Union labor market.

**Live demo: [http://localhost:8000](http://localhost:8000)** (run locally)

## What's here

This repository adapts the original `karpathy/jobs` visualizer to the **European Market**. We scrape **436 ISCO-08 Unit Groups (Level 4)** from the ESCO API, covering every major sector of the European economy. 

The interactive treemap visualization shows each occupation where the **area** is proportional to total employment and **color** shows the selected metric — toggle between European growth outlook, median pay (in Euros), education requirements, and AI exposure.

**Multilingual Support**: The frontend natively supports **all 24 official EU languages** using a dynamic i18n switcher powered by LLM-translated dictionary files.

## LLM-powered coloring

The repo includes scrapers, parsers, and a pipeline for writing custom LLM prompts to score and color occupations by any criteria. You write a prompt, the LLM scores each occupation, and the treemap colors accordingly. The "Digital AI Exposure" layer is one example — it estimates how much current AI (which is primarily digital) will reshape each occupation. 

> **API Note:** Scoring the 436 occupations is securely powered by Google's **Gemini 3.1 Flash-Lite** model via the `google-genai` SDK, fully refactored to handle aggressive API rate limits elegantly.

## Data pipeline

1. **Scrape** (`scrape_eu.py`) — Directly pulls raw JSON data and structural hierarchies from the official ESCO taxonomy into `raw_eu/`.
2. **Parse** (`process_eu.py`) — Extracts rich, broad definitions and lists of narrower occupations into clean Markdown files in `pages_eu/`.
3. **Tabulate** (`make_csv_eu.py`) — Adapts EU descriptors into structured BLS-compatible schema (pay, education, job count equivalents) and updates `occupations_eu.csv`.
4. **Score** (`score.py`) — Sends each European occupation's Markdown description to the Gemini API with a strict JSON format prompt. Results uniquely cached to `scores_eu.json`.
5. **Translate UI** (`translate_ui.py`) — A Gemini-powered automated translation pipeline for adapting the core English interface (`site/i18n/en.json`) into 23 other European languages.
6. **Build site data** (`build_site_data.py`) — Merges CSV stats and AI exposure scores into a neat `site/data.json` payload for the frontend rendering.

## Key files

| File | Description |
|------|-------------|
| `occupations_eu.csv` | Summary stats: simulated pay, education, job volumes |
| `scores_eu.json` | AI exposure scores (0-10) with rationales for all 436 EU occupations |
| `prompt.md` | Aggregate prompt summarizing the entire dataset for easy paste-to-LLM |
| `raw_eu/` | Raw JSON payload responses straight from the ESCO API |
| `pages_eu/` | Clean Markdown interpretations of the ISCO hierarchy |
| `site/` | Static website containing the dynamic `d3.treemap` engine |
| `site/i18n/` | 24 JSON language dictionaries for true European localization |

## Usage
Ensure you have the Gemini API Key set up in your environment:
```bash
export GEMINI_API_KEY=your_key_here
```

```bash
# Process all data from scratch
python scrape_eu.py
python process_eu.py
python make_csv_eu.py
python score.py

# Build new frontend payload
python build_site_data.py

# To regenerate the translation files from the master english dictionary:
python translate_ui.py

# Serve the site locally
python -m http.server 8000 --directory site
```
