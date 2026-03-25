"""
Process EU (ESCO) raw JSON files into clean Markdown.

Reads from raw_eu/<slug>.json, writes to pages_eu/<slug>.md.

Usage:
    uv run python process_eu.py              # process all JSON files
    uv run python process_eu.py --force      # re-process even if .md exists
"""

import argparse
import json
import os
import re
from bs4 import BeautifulSoup

def clean(text):
    """Clean up formatting and HTML tags from ESCO descriptions."""
    if not text:
        return ""
    # Strip HTML tags
    soup = BeautifulSoup(text, "html.parser")
    cleaned = soup.get_text(separator=' ')
    # Normalize whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def parse_esco_json(json_path, occ_meta):
    """Parse raw ESCO ISCO JSON into a formatted Markdown string."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    md = []

    # --- Title ---
    title = data.get("title") or occ_meta.get("title", "Unknown Occupation")
    md.append(f"# {title.title()}")
    md.append("")

    # --- Source URL ---
    uri = data.get("uri") or occ_meta.get("uri", "")
    if uri:
        md.append(f"**Source:** {uri}")
        md.append("")

    # --- Quick Facts ---
    code = data.get("code", "")
    if code:
        md.append("## Quick Facts")
        md.append("")
        md.append("| Field | Value |")
        md.append("|-------|-------|")
        md.append(f"| ISCO-08 Code | {code} |")
        md.append("")

    # --- Description ---
    desc_obj = data.get("description", {}).get("en", {})
    desc_text = desc_obj.get("literal") or desc_obj.get("literalForm") or ""
    desc = clean(desc_text)
    if desc:
        md.append("## Description")
        md.append("")
        md.append(desc)
        md.append("")

    # --- Granular Occupations Included ---
    links = data.get("_links", {})
    narrower = links.get("narrowerOccupation", [])
    if narrower:
        md.append("## Specific Occupations Included")
        md.append("")
        md.append("This broad category includes the following specific roles:")
        md.append("")
        for occ in narrower:
            stitle = occ.get("title", "")
            if stitle:
                md.append(f"- {stitle.title()}")
        md.append("")

    return "\\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Convert ESCO JSON to Markdown")
    parser.add_argument("--force", action="store_true", help="Re-process even if .md exists")
    args = parser.parse_args()

    os.makedirs("pages", exist_ok=True)

    if not os.path.exists("data/json/occupations_eu.json"):
        print("data/json/occupations_eu.json not found. Run scrape_eu.py first.")
        return

    with open("data/json/occupations_eu.json", "r") as f:
        occupations = json.load(f)

    processed = 0
    skipped = 0
    missing = 0

    for occ in occupations:
        slug = occ["slug"]
        json_path = f"raw_data/{slug}.json"
        md_path = f"pages/{slug}.md"

        if not os.path.exists(json_path):
            missing += 1
            continue

        if not args.force and os.path.exists(md_path):
            skipped += 1
            continue

        md_content = parse_esco_json(json_path, occ)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        processed += 1

    total_json = len([f for f in os.listdir("raw_data") if f.endswith(".json")] if os.path.exists("raw_data") else [])
    total_md = len([f for f in os.listdir("pages") if f.endswith(".md")])
    print(f"Processed: {processed}, Skipped (cached): {skipped}, Missing JSON: {missing}")
    print(f"Total: {total_json} JSON files, {total_md} Markdown files")


if __name__ == "__main__":
    main()
