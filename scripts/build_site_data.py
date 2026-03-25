"""
Build a compact JSON for the website by merging CSV stats with AI exposure scores.

Reads occupations_eu.csv (for stats) and scores_eu.json (for AI exposure).
Writes site/data.json.

Usage:
    uv run python build_site_data.py
"""

import csv
import json
import os


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


def build_data(csv_path, scores, output_json):
    """Merge CSV stats with scores and write to JSON."""
    # Load CSV stats
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Skipping.")
        return

    with open(csv_path, encoding="utf-8") as f:
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
            "pay": int(float(row["median_pay_annual"])) if row["median_pay_annual"] else None,
            "jobs": int(row["num_jobs_2024"]) if row["num_jobs_2024"] else None,
            "outlook": int(row["outlook_pct"]) if row["outlook_pct"] else None,
            "outlook_desc": row["outlook_desc"],
            "education": row["entry_education"],
            "exposure": score.get("exposure"),
            "exposure_rationale": score.get("rationale"),
            "url": row.get("url", ""),
            "code": soc_code,
        })

    os.makedirs("site", exist_ok=True)
    with open(output_json, "w") as f:
        json.dump(data, f)

    print(f"Wrote {len(data)} occupations to {output_json}")
    valid_jobs = [d for d in data if d["jobs"]]
    total_jobs = sum(d["jobs"] for d in valid_jobs)
    print(f"Total jobs represented: {total_jobs:,}")
    
    # Calculate weighted averages
    avg_growth = sum(d["outlook"] * d["jobs"] for d in valid_jobs if d["outlook"] is not None) / total_jobs if total_jobs > 0 else 0
    avg_pay = sum(d["pay"] * d["jobs"] for d in valid_jobs if d["pay"] is not None) / total_jobs if total_jobs > 0 else 0
    avg_exposure = sum(d["exposure"] * d["jobs"] for d in valid_jobs if d["exposure"] is not None) / total_jobs if total_jobs > 0 else 0

    return {
        "total_jobs": total_jobs,
        "avg_growth": avg_growth,
        "avg_pay": avg_pay,
        "avg_exposure": avg_exposure
    }


def main():
    # Load AI exposure scores
    if not os.path.exists("data/json/scores_eu.json"):
        print("data/json/scores_eu.json not found. Please run score_eu.py first.")
        return

    with open("data/json/scores_eu.json") as f:
        scores_list = json.load(f)
    scores = {s["slug"]: s for s in scores_list}

    # Build data for all regions
    summary = {}
    import glob
    csv_files = glob.glob("data/csv/occupations_*.csv")
    for csv_path in csv_files:
        region_code = os.path.basename(csv_path).replace("occupations_", "").replace(".csv", "").lower()
        output_json = f"site/data_{region_code}.json"
        stats = build_data(csv_path, scores, output_json)
        summary[region_code] = stats

    # Write summary data
    with open("site/data_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("Wrote site/data_summary.json")

    # Legacy / Default data.json (alias for EU)
    import shutil
    if os.path.exists("site/data_eu.json"):
        shutil.copy("site/data_eu.json", "site/data.json")
        print("Copied data_eu.json to site/data.json (default)")

if __name__ == "__main__":
    main()
