# Tech Stack

## Data Collection & Processing

| Technology | Purpose |
|:--|:--|
| **Python 3.13** | All backend scripts (scraping, parsing, scoring, translation) |
| **ESCO REST API** | Source for 436 ISCO-08 Unit Group occupation data |
| **Eurostat API** | Official EU27 2023 census employment statistics |
| **Google Gemini 3.1 Flash-Lite** | AI exposure scoring and UI translation via `google-genai` SDK |
| **python-dotenv** | Secure environment variable management |

## Frontend

| Technology | Purpose |
|:--|:--|
| **Vanilla HTML/CSS/JS** | Zero-dependency static site |
| **Canvas API** | Squarified treemap rendering with domain grouping |
| **Custom i18n engine** | 24-language JSON dictionaries loaded dynamically |
| **CSS Custom Properties** | Dark theme design tokens |

## Infrastructure

| Technology | Purpose |
|:--|:--|
| **GitHub Actions** | CI/CD — auto-deploys `site/` to GitHub Pages on push |
| **GitHub Pages** | Static site hosting |
| **Git** | Version control |

## Data Standards

| Standard | Usage |
|:--|:--|
| **ISCO-08** | International Standard Classification of Occupations (4-digit codes) |
| **ESCO** | European Skills, Competences, Qualifications and Occupations framework |
| **NACE Rev. 2** | EU statistical classification of economic activities (via Eurostat) |

## File Formats

| Format | Files |
|:--|:--|
| JSON | `data.json`, `scores_eu.json`, `occupations_eu.json`, `i18n/*.json` |
| CSV | `occupations_eu.csv` |
| Markdown | `prompt.md`, `pages_eu/*.md` |
| HTML | `site/index.html` |
