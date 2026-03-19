"""
Build a compact JSON for the website by merging CSV stats with AI exposure scores.

Reads occupations_eu.csv (for stats) and scores_eu.json (for AI exposure).
Writes site/data.json.

Usage:
    uv run python build_site_data.py
"""

import csv
import json


# ── ISCO 2-digit → BLS-style sector mapping ────────────────────────────
# Maps the first two digits of a 4-digit ISCO-08 code to a human-readable
# industry sector, mirroring the category slugs used in the original
# karpathy/jobs BLS visualizer.
ISCO2_TO_SECTOR = {
    # Armed forces
    "01": "protective-service",
    "02": "protective-service",
    "03": "protective-service",
    # Managers
    "11": "management",
    "12": "management",
    "13": "management",
    "14": "management",
    # Professionals
    "21": "architecture-and-engineering",
    "22": "healthcare",
    "23": "education-training-and-library",
    "24": "business-and-financial",
    "25": "computer-and-information-technology",
    "26": "arts-design-media-and-legal",
    # Technicians and associate professionals
    "31": "life-physical-and-social-science",
    "32": "healthcare",
    "33": "business-and-financial",
    "34": "arts-design-media-and-legal",
    "35": "computer-and-information-technology",
    # Clerical support workers
    "41": "office-and-administrative-support",
    "42": "office-and-administrative-support",
    "43": "office-and-administrative-support",
    "44": "office-and-administrative-support",
    # Service and sales workers
    "51": "personal-care-and-service",
    "52": "sales",
    "53": "personal-care-and-service",
    "54": "protective-service",
    # Skilled agricultural, forestry and fishery workers
    "61": "farming-fishing-and-forestry",
    "62": "farming-fishing-and-forestry",
    "63": "farming-fishing-and-forestry",
    # Craft and related trades workers
    "71": "construction-and-extraction",
    "72": "installation-maintenance-and-repair",
    "73": "production",
    "74": "installation-maintenance-and-repair",
    "75": "food-preparation-and-serving",
    # Plant and machine operators, and assemblers
    "81": "production",
    "82": "production",
    "83": "transportation-and-material-moving",
    # Elementary occupations
    "91": "building-and-grounds-cleaning",
    "92": "farming-fishing-and-forestry",
    "93": "construction-and-extraction",
    "94": "food-preparation-and-serving",
    "95": "sales",
    "96": "building-and-grounds-cleaning",
}


def isco_to_sector(code):
    """Map a 4-digit ISCO-08 code to a BLS-style sector slug."""
    return ISCO2_TO_SECTOR.get(code[:2], "other")


def main():
    # Load AI exposure scores
    with open("scores_eu.json") as f:
        scores_list = json.load(f)
    scores = {s["slug"]: s for s in scores_list}

    # Load CSV stats
    with open("occupations_eu.csv") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Merge
    data = []
    for row in rows:
        slug = row["slug"]
        score = scores.get(slug, {})
        soc_code = row["soc_code"]
        data.append({
            "title": row["title"],
            "slug": slug,
            "category": isco_to_sector(soc_code),
            "pay": int(row["median_pay_annual"]) if row["median_pay_annual"] else None,
            "jobs": int(row["num_jobs_2024"]) if row["num_jobs_2024"] else None,
            "outlook": int(row["outlook_pct"]) if row["outlook_pct"] else None,
            "outlook_desc": row["outlook_desc"],
            "education": row["entry_education"],
            "exposure": score.get("exposure"),
            "exposure_rationale": score.get("rationale"),
            "url": row.get("url", ""),
            "code": soc_code,
        })

    import os
    os.makedirs("site", exist_ok=True)
    with open("site/data.json", "w") as f:
        json.dump(data, f)

    print(f"Wrote {len(data)} occupations to site/data.json")
    total_jobs = sum(d["jobs"] for d in data if d["jobs"])
    print(f"Total jobs represented: {total_jobs:,}")


if __name__ == "__main__":
    main()
