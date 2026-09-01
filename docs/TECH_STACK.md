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
| **Vanilla HTML/CSS/JS** | Zero-dependency static site architecture |
| **Canvas API (2D)** | Squarified treemap rendering & 2D Scatter Matrix quadrant engine |
| **Faceted Filter Engine** | Real-time multi-dimensional filtering (Sector, Education, AI Exposure) |
| **Career AI Calculator & Quiz** | Personal exposure evaluator & 1200x630 social card canvas engine |
| **AI Semantic Matcher** | Client-side keyword, synonym, and rationale relevance scorer |
| **Country Compare Engine** | Dual-country benchmark dashboard, KPI metrics, & sector wage gap analysis |
| **Embeddable Widget (`<iframe />`)** | Standalone responsive visualizer (`site/embed.html`) & code generator |
| **Slide-in Detail Drawer** | Glassmorphic occupation profile with EU salary benchmark and AI rationale |
| **Theme Engine** | Light/Dark theme switching via CSS Custom Properties and adaptive Canvas |
| **Visual Export (Offscreen Canvas)** | High-res (2x) branded PNG snapshot generator with metadata banner |
| **Responsive Design** | Vertical category stacking logic for mobile viewports |
| **Custom i18n engine** | 24-language JSON dictionaries loaded dynamically |
| **URL State Sync** | Deep-linking via History API / SearchParams for instant view sharing |
| **Umami Analytics** | Privacy-respecting, zero-cookie traffic analytics via `stats.alexandrucruceanu.com` |

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
| JSON | `site/data*.json`, `data/json/*.json`, `site/i18n/*.json` |
| CSV | `data/csv/occupations_*.csv` |
| Markdown | `prompt.md`, `pages/*.md`, `docs/*.md` |
| HTML | `site/index.html`, `site/map.html` |
| JS | `site/shared.js` (Cookie consent, Localized quotes) |
| XML | `site/sitemap.xml` (Search indexing) |
| JSON | `site/manifest.json` (PWA support) |
| TXT | `site/robots.txt` (SEO) |

