"""Generates a fictional 4W (Who's doing What, Where, When) activity dataset
tied to the synthetic site assessments, for the Phase R5 dashboard.

All partner organization names below are invented for this demonstration and
do not refer to any real organization. Deterministic (fixed seed).

Run: python3 scripts/generate_4w_data.py
Output: data/fictional_4w_activities.csv
"""

import csv
import random

random.seed(7)

SITES_CSV = "data/synthetic_site_assessments.csv"
OUT_CSV = "data/fictional_4w_activities.csv"

# Entirely fictional partner names -- not real organizations.
PARTNERS_BY_SECTOR = {
    "shelter": ["Riverside Relief Network", "Shelter First Initiative"],
    "wash": ["Bay Area Humanitarian Trust", "Clearwater Response Group"],
    "health": ["Horizon Aid Collective", "Frontline Health Partners"],
    "protection": ["Community Response Alliance", "Safe Haven Network"],
    "food_security": ["Unity Field Partners", "Harvest Relief Initiative"],
    "education": ["Bright Path Learning Trust", "Unity Field Partners"],
    "livelihoods": ["Horizon Aid Collective", "Community Response Alliance"],
    "nutrition": ["Frontline Health Partners", "Harvest Relief Initiative"],
}

STATUSES = ["ongoing", "ongoing", "planned", "completed"]


def read_sites():
    with open(SITES_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    sites = read_sites()
    rows = []
    activity_id = 1
    for site in sites:
        sectors = {
            site["priority_needs/top_priority_1"],
            site["priority_needs/top_priority_2"],
        }
        for sector in sectors:
            partner = random.choice(PARTNERS_BY_SECTOR.get(sector, ["Community Response Alliance"]))
            rows.append({
                "activity_id": f"ACT-{activity_id:03d}",
                "partner_org": partner,
                "sector": sector,
                "site_id": site["site_id"],
                "site_name": site["metadata/site_name"],
                "upazila": site["location/upazila"],
                "district": site["location/district"],
                "status": random.choice(STATUSES),
                "start_date": f"2026-0{random.randint(1,9)}-{random.randint(1,28):02d}",
            })
            activity_id += 1

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} fictional activities to {OUT_CSV}")


if __name__ == "__main__":
    main()
