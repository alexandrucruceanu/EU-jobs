"""
Scrape ISCO-08 Level 4 Unit Groups (European broad occupations) via API.

Saves raw JSON to raw_eu/<slug>.json as the source of truth.
Run process_eu.py afterwards to derive pages_eu/<slug>.md.

Usage:
    uv run python scrape_eu.py
    uv run python scrape_eu.py --limit 400
    uv run python scrape_eu.py --force

Caching: skips any occupation where raw_eu/<slug>.json already exists.
"""

import argparse
import json
import os
import time
import re
import requests

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def main():
    parser = argparse.ArgumentParser(description="Scrape EU ISCO Level 4 groups")
    parser.add_argument("--limit", type=int, default=10000, help="Number of items to fetch initially (use 10000 for all)")
    parser.add_argument("--force", action="store_true", help="Re-scrape even if cached")
    parser.add_argument("--delay", type=float, default=0.2, help="Seconds between requests")
    args = parser.parse_args()

    os.makedirs("raw_data", exist_ok=True)

    print("Fetching ISCO-08 Unit Groups from ESCO API...")
    search_url = f"https://ec.europa.eu/esco/api/search?language=en&type=concept&limit={args.limit}"
    
    resp = requests.get(search_url)
    resp.raise_for_status()
    
    data = resp.json()
    items = data.get("_embedded", {}).get("results", [])

    if not items:
        # Fallback if the API structure is slightly different
        items = data if isinstance(data, list) else []

    # Filter strictly for ISCO Level 4 (Unit Groups)
    # Their URIs look like 'http://data.europa.eu/esco/isco/C2411' (length after split is 5: 'C' + 4 digits)
    occupations = []
    for item in items:
        uri = item.get("uri", "")
        if 'isco/C' in uri and len(uri.split('/')[-1]) == 5:
            title = item.get("title", "Unknown")
            slug = slugify(title)
            occupations.append({
                "title": title,
                "slug": slug,
                "uri": uri,
                "url": uri # Store uri in url field for mapping pipeline equivalence
            })

    # Sort them by title or code for deterministic ordering
    occupations.sort(key=lambda x: x["title"])
    
    with open("data/json/occupations_eu.json", "w", encoding="utf-8") as f:
        json.dump(occupations, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(occupations)} ISCO-08 Level 4 groups to data/json/occupations_eu.json")

    # Fetch detailed data
    for i, occ in enumerate(occupations):
        slug = occ["slug"]
        uri = occ["uri"]
        json_path = f"raw_data/{slug}.json"
        
        if not args.force and os.path.exists(json_path):
            print(f"  [{i+1}/{len(occupations)}] CACHED {occ['title']}")
            continue

        print(f"  [{i+1}/{len(occupations)}] {occ['title']}...", end=" ", flush=True)

        try:
            # Note: For ISCO concept, the resource endpoint is /resource/concept
            detail_url = f"https://ec.europa.eu/esco/api/resource/concept?uri={uri}&language=en"
            detail_resp = requests.get(detail_url)
            detail_resp.raise_for_status()

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(detail_resp.json(), f, ensure_ascii=False, indent=2)

            print(f"OK")
            time.sleep(args.delay)
            
        except Exception as e:
            print(f"ERROR: {e}")

    cached = len([f for f in os.listdir("raw_data") if f.endswith(".json")])
    print(f"\nDone. {cached}/{len(occupations)} JSON files cached in raw_data/")

if __name__ == "__main__":
    main()
