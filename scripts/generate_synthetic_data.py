"""Generates a synthetic site-assessment dataset shaped like a KoboToolbox
CSV export of forms/rapid_assessment_form.xlsx — group-prefixed column names,
space-separated select_multiple values, geopoint as "lat lon alt acc".

No real site, camp, or population data. Coordinates are randomly jittered
around public upazila-centre approximations for Cox's Bazar district and are
not derived from any real assessment.

Run: python3 scripts/generate_synthetic_data.py
Output: data/synthetic_site_assessments.csv
"""

import csv
import random

OUT_PATH = "data/synthetic_site_assessments.csv"

random.seed(42)

UPAZILAS = {
    # name: (district, division, approx_lat, approx_lon)
    "ukhiya": ("coxs_bazar", "chattogram", 21.2199, 92.1441),
    "teknaf": ("coxs_bazar", "chattogram", 20.8624, 92.3057),
    "coxs_bazar_sadar": ("coxs_bazar", "chattogram", 21.4272, 91.9711),
    "ramu": ("coxs_bazar", "chattogram", 21.4272, 92.0997),
    "chakaria": ("coxs_bazar", "chattogram", 21.7833, 92.0667),
    "naikhongchhari": ("bandarban", "chattogram", 21.5225, 92.3557),
}

SITE_TYPES = ["spontaneous_settlement", "planned_camp", "collective_center", "host_community", "transit_center"]
SITE_STATUS = ["existing", "existing", "existing", "new"]
DISASTER_TYPES = ["flood", "cyclone", "fire", "landslide", "riverbank_erosion"]
SHELTER_TYPES = ["makeshift", "tarpaulin", "semi_pucca", "pucca", "damaged_no_shelter"]
DAMAGE_RANGES = ["none", "low_1_25", "moderate_26_50", "high_51_75", "severe_76_100"]
WATER_SOURCES = ["tubewell", "piped_supply", "pond_river", "water_trucking"]
FUNCTIONALITY = ["functional", "partially_functional", "non_functional"]
LATRINE_RANGES = ["lt_20", "20_50", "50_100", "gt_100"]
HEALTH_CONCERNS = ["diarrhea", "respiratory_infection", "malnutrition", "skin_disease", "maternal_health", "mental_health"]
PROTECTION_CONCERNS = ["child_labor", "early_marriage", "gbv_risk", "family_separation", "unsafe_shelter_lighting", "documentation_issues"]
YES_NO = ["yes", "no"]
YES_NO_UNKNOWN = ["yes", "no", "unknown"]
SECTORS = ["shelter", "wash", "health", "protection", "food_security", "education", "livelihoods", "nutrition"]

FIELDNAMES = [
    "site_id", "metadata/enumerator_name", "metadata/enumerator_id", "metadata/assessment_date",
    "metadata/site_id", "metadata/site_name",
    "location/division", "location/district", "location/upazila", "location/gps_point",
    "site_profile/site_type", "site_profile/site_status", "site_profile/hh_estimate", "site_profile/pop_estimate",
    "shelter/disaster_context", "shelter/disaster_type", "shelter/shelter_type_majority",
    "shelter/shelter_damage_pct", "shelter/shelter_priority_need",
    "wash/water_source_type", "wash/water_functionality", "wash/latrine_ratio", "wash/wash_priority_need",
    "health/health_facility_onsite", "health/health_facility_distance_km", "health/health_key_concerns",
    "health/health_priority_need",
    "protection/protection_concerns", "protection/gbv_referral_pathway", "protection/child_friendly_space_present",
    "priority_needs/top_priority_1", "priority_needs/top_priority_2", "priority_needs/top_priority_3",
    "closing/enumerator_remarks",
]

ENUMERATORS = [("A. Karim", "ENUM-01"), ("S. Nasrin", "ENUM-02"), ("M. Hossain", "ENUM-03"), ("F. Akter", "ENUM-04")]


def jitter(value, spread=0.03):
    return round(value + random.uniform(-spread, spread), 6)


def pick_priorities():
    return random.sample(SECTORS, 3)


def build_row(i):
    upazila = random.choice(list(UPAZILAS.keys()))
    district, division, lat0, lon0 = UPAZILAS[upazila]
    lat, lon = jitter(lat0), jitter(lon0)
    enumerator = random.choice(ENUMERATORS)
    disaster_context = random.choices(YES_NO, weights=[0.4, 0.6])[0]
    disaster_types = " ".join(random.sample(DISASTER_TYPES, random.randint(1, 2))) if disaster_context == "yes" else ""
    damage_pct = random.choice(DAMAGE_RANGES) if disaster_context == "yes" else ""
    health_onsite = random.choice(YES_NO)
    hh = random.randint(15, 400)
    priorities = pick_priorities()

    return {
        "site_id": f"SITE-{i:03d}",
        "metadata/enumerator_name": enumerator[0],
        "metadata/enumerator_id": enumerator[1],
        "metadata/assessment_date": f"2026-0{random.randint(1,9)}-{random.randint(10,28):02d}",
        "metadata/site_id": f"SITE-{i:03d}",
        "metadata/site_name": f"{upazila.replace('_', ' ').title()} Site {i}",
        "location/division": division,
        "location/district": district,
        "location/upazila": upazila,
        "location/gps_point": f"{lat} {lon} 0 5",
        "site_profile/site_type": random.choice(SITE_TYPES),
        "site_profile/site_status": random.choice(SITE_STATUS),
        "site_profile/hh_estimate": hh,
        "site_profile/pop_estimate": hh * random.randint(4, 6),
        "shelter/disaster_context": disaster_context,
        "shelter/disaster_type": disaster_types,
        "shelter/shelter_type_majority": random.choice(SHELTER_TYPES),
        "shelter/shelter_damage_pct": damage_pct,
        "shelter/shelter_priority_need": random.choice(YES_NO),
        "wash/water_source_type": random.choice(WATER_SOURCES),
        "wash/water_functionality": random.choice(FUNCTIONALITY),
        "wash/latrine_ratio": random.choice(LATRINE_RANGES),
        "wash/wash_priority_need": random.choice(YES_NO),
        "health/health_facility_onsite": health_onsite,
        "health/health_facility_distance_km": "" if health_onsite == "yes" else round(random.uniform(0.5, 12), 1),
        "health/health_key_concerns": " ".join(random.sample(HEALTH_CONCERNS, random.randint(1, 3))),
        "health/health_priority_need": random.choice(YES_NO),
        "protection/protection_concerns": " ".join(random.sample(PROTECTION_CONCERNS, random.randint(0, 2))),
        "protection/gbv_referral_pathway": random.choice(YES_NO_UNKNOWN),
        "protection/child_friendly_space_present": random.choice(YES_NO),
        "priority_needs/top_priority_1": priorities[0],
        "priority_needs/top_priority_2": priorities[1],
        "priority_needs/top_priority_3": priorities[2],
        "closing/enumerator_remarks": "",
    }


def main():
    rows = [build_row(i) for i in range(1, 19)]
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} synthetic site assessments to {OUT_PATH}")


if __name__ == "__main__":
    main()
