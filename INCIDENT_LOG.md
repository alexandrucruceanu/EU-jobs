# Incident Log

Notable issues encountered during development and their resolutions.

---

### INC-001: Gemini API Rate Limiting
**Date:** 2026-03-18  
**Severity:** Medium  
**Symptom:** `score.py` would fail mid-batch with `429 Too Many Requests` after ~30 occupations.  
**Root Cause:** Gemini Flash-Lite enforces aggressive per-minute rate limits on free-tier API keys.  
**Resolution:** Added exponential backoff with jitter and batch-level retry logic to `score.py`. Scores are cached to `scores_eu.json` so partial runs resume without re-scoring.

---

### INC-002: Translation Quota Exhaustion
**Date:** 2026-03-19  
**Severity:** Medium  
**Symptom:** `translate_ui.py` would fail after translating ~10 of 23 languages, returning `ResourceExhausted` errors.  
**Root Cause:** Each language file contains 450+ keys; translating all 23 languages in one pass exceeds the Gemini free-tier quota.  
**Resolution:** Implemented `inject_native_titles.py` as a fallback — it injects official ESCO-provided job titles from the EU multilingual classification, bypassing the LLM for the 436 job title keys. Static UI keys are translated via Gemini in smaller batches.

---

### INC-003: UTF-8 Console Crash on Windows
**Date:** 2026-03-18  
**Severity:** Low  
**Symptom:** `score.py` would crash with `UnicodeEncodeError` when printing non-ASCII occupation titles (e.g., German, French characters) to the Windows console.  
**Root Cause:** Windows PowerShell defaults to `cp1252` encoding, which cannot represent all EU characters.  
**Resolution:** Wrapped all print statements with `errors='replace'` and used `sys.stdout.reconfigure(encoding='utf-8')` at script startup.

---

### INC-004: Stale UI Text After Language Switch
**Date:** 2026-03-19  
**Severity:** Medium  
**Symptom:** Header text, buttons, and disclaimers remained in English when switching to other EU languages via the language dropdown.  
**Root Cause:** `inject_native_titles.py` was using the English dictionary as a base template for all languages, overwriting previously translated static UI keys with their English values.  
**Resolution:** Modified the injection workflow: (1) purge corrupted language files, (2) re-run `translate_ui.py` to generate fresh static UI translations, (3) then run `inject_native_titles.py` to overlay only job title keys without touching static UI keys.

---

### INC-005: Hardcoded API Key in Source
**Date:** 2026-03-19  
**Severity:** High  
**Symptom:** A Gemini API key was hardcoded as fallback default in `score.py` and `translate_ui.py`.  
**Root Cause:** Original development convenience pattern — `os.environ.get("KEY", "fallback_value")`.  
**Resolution:** Created `.env` file (gitignored), added `.env.example` template, and refactored both scripts to require the environment variable with a clear error message if missing. Key recommended for rotation.
---

### INC-006: Mobile Treemap Layout for better UX
**Date:** 2026-03-20  
**Severity:** Low  
**Symptom:** On narrow screens, the original squarified category layout made labels illegible and cells too small.  
**Root Cause:** The squarify algorithm targets a square aspect ratio, which doesn't scroll well on mobile phones.  
**Resolution:** Replaced the global category squarification with a vertical stack for viewports <768px. Ensured the largest cell in each category forces its title to be visible.
