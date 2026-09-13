"""Builds the multi-sector rapid site assessment XLSForm.

Structure follows the IOM DTM Site Assessment / REACH MSNA convention:
metadata -> location -> site profile -> shelter -> WASH -> health ->
protection -> priority needs -> closing, each module gated by `relevant`
skip logic where it depends on an earlier answer. Bangla and English labels
are both included (label::English (en), label::Bangla (bn)).

Run: python3 scripts/build_xlsform.py
Output: forms/rapid_assessment_form.xlsx
"""

import openpyxl

OUT_PATH = "forms/rapid_assessment_form.xlsx"

SURVEY_HEADER = [
    "type", "name", "label::English (en)", "label::Bangla (bn)",
    "hint::English (en)", "required", "relevant", "constraint",
    "constraint_message::English (en)", "choice_filter", "appearance", "default",
]

SURVEY_ROWS = [
    ("start", "start", "", "", "", "", "", "", "", "", "", ""),
    ("end", "end", "", "", "", "", "", "", "", "", "", ""),
    ("today", "today", "", "", "", "", "", "", "", "", "", ""),
    ("deviceid", "deviceid", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "metadata", "Assessment metadata", "মূল্যায়ন তথ্য", "", "", "", "", "", "", "", ""),
    ("text", "enumerator_name", "Enumerator name", "গণনাকারীর নাম", "", "yes", "", "", "", "", "", ""),
    ("text", "enumerator_id", "Enumerator ID", "গণনাকারীর আইডি", "", "yes", "", "", "", "", "", ""),
    ("date", "assessment_date", "Assessment date", "মূল্যায়নের তারিখ", "", "yes", "", "", "", "", "", "${today}"),
    ("text", "site_id", "Site code", "সাইট কোড", "Unique site identifier", "yes", "", "", "", "", "", ""),
    ("text", "site_name", "Site name", "সাইটের নাম", "", "yes", "", "", "", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "location", "Location", "অবস্থান", "", "", "", "", "", "", "", ""),
    ("select_one division", "division", "Division", "বিভাগ", "", "yes", "", "", "", "", "", ""),
    ("select_one district", "district", "District", "জেলা", "", "yes", "", "", "", "division=${division}", "", ""),
    ("select_one upazila", "upazila", "Upazila", "উপজেলা", "", "yes", "", "", "", "district=${district}", "", ""),
    ("geopoint", "gps_point", "Site location (GPS)", "সাইটের অবস্থান (জিপিএস)", "Capture at the site's central point", "yes", "", "", "", "", "", ""),
    ("geoshape", "site_boundary", "Site boundary (optional)", "সাইটের সীমানা (ঐচ্ছিক)", "Trace the outer boundary if mapping the full site", "no", "", "", "", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "site_profile", "Site profile", "সাইট প্রোফাইল", "", "", "", "", "", "", "", ""),
    ("select_one site_type", "site_type", "Site type", "সাইটের ধরন", "", "yes", "", "", "", "", "", ""),
    ("select_one site_status", "site_status", "Site status", "সাইটের অবস্থা", "", "yes", "", "", "", "", "", ""),
    ("integer", "hh_estimate", "Estimated number of households", "আনুমানিক পরিবারের সংখ্যা", "", "yes", "", ". >= 0", "Must be zero or more", "", "", ""),
    ("integer", "pop_estimate", "Estimated population", "আনুমানিক জনসংখ্যা", "", "yes", "", ". >= ${hh_estimate}", "Population cannot be less than household count", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "shelter", "Shelter", "আশ্রয়", "", "", "", "", "", "", "", ""),
    ("select_one yes_no", "disaster_context", "Is this site affected by a recent disaster (flood/cyclone/fire)?", "এই সাইটটি কি সাম্প্রতিক দুর্যোগে (বন্যা/ঘূর্ণিঝড়/অগ্নিকাণ্ড) ক্ষতিগ্রস্ত?", "", "yes", "", "", "", "", "", ""),
    ("select_multiple disaster_type", "disaster_type", "Disaster type(s)", "দুর্যোগের ধরন", "", "yes", "${disaster_context}='yes'", "", "", "", "", ""),
    ("select_one shelter_type", "shelter_type_majority", "Majority shelter type", "অধিকাংশ আশ্রয়ের ধরন", "", "yes", "", "", "", "", "", ""),
    ("select_one damage_pct_range", "shelter_damage_pct", "% of shelters damaged or destroyed", "ক্ষতিগ্রস্ত বা ধ্বংসপ্রাপ্ত আশ্রয়ের শতাংশ", "", "yes", "${disaster_context}='yes'", "", "", "", "", ""),
    ("select_one yes_no", "shelter_priority_need", "Is shelter assistance a priority need at this site?", "এই সাইটে আশ্রয় সহায়তা কি একটি অগ্রাধিকার প্রয়োজন?", "", "yes", "", "", "", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "wash", "WASH", "ওয়াশ", "", "", "", "", "", "", "", ""),
    ("select_one water_source", "water_source_type", "Main water source", "প্রধান পানির উৎস", "", "yes", "", "", "", "", "", ""),
    ("select_one functionality_status", "water_functionality", "Water source functionality", "পানির উৎসের কার্যকারিতা", "", "yes", "", "", "", "", "", ""),
    ("select_one latrine_ratio_range", "latrine_ratio", "Persons per functional latrine", "প্রতি কার্যকর ল্যাট্রিনে ব্যক্তির সংখ্যা", "", "yes", "", "", "", "", "", ""),
    ("select_one yes_no", "wash_priority_need", "Is WASH assistance a priority need at this site?", "এই সাইটে ওয়াশ সহায়তা কি একটি অগ্রাধিকার প্রয়োজন?", "", "yes", "", "", "", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "health", "Health", "স্বাস্থ্য", "", "", "", "", "", "", "", ""),
    ("select_one yes_no", "health_facility_onsite", "Is there a functioning health facility on-site?", "সাইটে কি কার্যকর স্বাস্থ্যসেবা কেন্দ্র আছে?", "", "yes", "", "", "", "", "", ""),
    ("decimal", "health_facility_distance_km", "Distance to nearest health facility (km)", "নিকটতম স্বাস্থ্যসেবা কেন্দ্রের দূরত্ব (কিমি)", "", "yes", "${health_facility_onsite}='no'", ". >= 0", "Must be zero or more", "", "", ""),
    ("select_multiple health_concerns", "health_key_concerns", "Key health concerns reported", "প্রধান স্বাস্থ্য সমস্যা", "", "yes", "", "", "", "", "", ""),
    ("select_one yes_no", "health_priority_need", "Is health assistance a priority need at this site?", "এই সাইটে স্বাস্থ্য সহায়তা কি একটি অগ্রাধিকার প্রয়োজন?", "", "yes", "", "", "", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "protection", "Protection", "সুরক্ষা", "Site-level aggregate observations only. Do not record individual names, ages, or other identifying details.", "", "", "", "", "", "", ""),
    ("note", "protection_note", "Aggregate, site-level indicators only — no individually identifying information.", "শুধুমাত্র সামগ্রিক, সাইট-স্তরের তথ্য — কোনো ব্যক্তিগত পরিচয়সূচক তথ্য নয়।", "", "", "", "", "", "", "", ""),
    ("select_multiple protection_concerns", "protection_concerns", "Protection concerns observed or reported at this site", "সাইটে পরিলক্ষিত বা রিপোর্টকৃত সুরক্ষা সমস্যা", "", "yes", "", "", "", "", "", ""),
    ("select_one yes_no_unknown", "gbv_referral_pathway", "Is a GBV referral pathway known to be available?", "জিবিভি রেফারেল পথ কি জানা আছে?", "", "yes", "", "", "", "", "", ""),
    ("select_one yes_no", "child_friendly_space_present", "Is a child-friendly space present at this site?", "সাইটে কি শিশুবান্ধব স্থান আছে?", "", "yes", "", "", "", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "priority_needs", "Priority needs ranking", "অগ্রাধিকার চাহিদার ক্রম", "", "", "", "", "", "", "", ""),
    ("select_one sector_list", "top_priority_1", "1st priority sector", "প্রথম অগ্রাধিকার খাত", "", "yes", "", "", "", "", "", ""),
    ("select_one sector_list", "top_priority_2", "2nd priority sector", "দ্বিতীয় অগ্রাধিকার খাত", "", "yes", "", "${top_priority_2} != ${top_priority_1}", "Must differ from 1st priority", "", "", ""),
    ("select_one sector_list", "top_priority_3", "3rd priority sector", "তৃতীয় অগ্রাধিকার খাত", "", "yes", "", "${top_priority_3} != ${top_priority_1} and ${top_priority_3} != ${top_priority_2}", "Must differ from 1st and 2nd priority", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),

    ("begin group", "closing", "Closing", "সমাপ্তি", "", "", "", "", "", "", "", ""),
    ("text", "enumerator_remarks", "Enumerator remarks", "গণনাকারীর মন্তব্য", "", "no", "", "", "", "", "multiline", ""),
    ("image", "site_photo", "Site photo (optional)", "সাইটের ছবি (ঐচ্ছিক)", "", "no", "", "", "", "", "", ""),
    ("end group", "", "", "", "", "", "", "", "", "", "", ""),
]

CHOICES_HEADER = ["list_name", "name", "label::English (en)", "label::Bangla (bn)", "division"]

CHOICES_ROWS = [
    ("yes_no", "yes", "Yes", "হ্যাঁ", ""),
    ("yes_no", "no", "No", "না", ""),

    ("yes_no_unknown", "yes", "Yes", "হ্যাঁ", ""),
    ("yes_no_unknown", "no", "No", "না", ""),
    ("yes_no_unknown", "unknown", "Unknown", "অজানা", ""),

    ("division", "chattogram", "Chattogram", "চট্টগ্রাম", ""),
    ("division", "dhaka", "Dhaka", "ঢাকা", ""),
    ("division", "sylhet", "Sylhet", "সিলেট", ""),

    ("district", "coxs_bazar", "Cox's Bazar", "কক্সবাজার", "chattogram"),
    ("district", "bandarban", "Bandarban", "বান্দরবান", "chattogram"),
    ("district", "chattogram_sadar", "Chattogram", "চট্টগ্রাম", "chattogram"),
    ("district", "sunamganj", "Sunamganj", "সুনামগঞ্জ", "sylhet"),

    ("upazila", "ukhiya", "Ukhiya", "উখিয়া", "coxs_bazar"),
    ("upazila", "teknaf", "Teknaf", "টেকনাফ", "coxs_bazar"),
    ("upazila", "coxs_bazar_sadar", "Cox's Bazar Sadar", "কক্সবাজার সদর", "coxs_bazar"),
    ("upazila", "ramu", "Ramu", "রামু", "coxs_bazar"),
    ("upazila", "chakaria", "Chakaria", "চকরিয়া", "coxs_bazar"),
    ("upazila", "naikhongchhari", "Naikhongchhari", "নাইক্ষ্যংছড়ি", "bandarban"),

    ("site_type", "spontaneous_settlement", "Spontaneous settlement", "স্বতঃস্ফূর্ত বসতি", ""),
    ("site_type", "planned_camp", "Planned camp", "পরিকল্পিত ক্যাম্প", ""),
    ("site_type", "collective_center", "Collective center", "সমষ্টিগত কেন্দ্র", ""),
    ("site_type", "host_community", "Host community", "আশ্রয়দাতা সম্প্রদায়", ""),
    ("site_type", "transit_center", "Transit center", "ট্রানজিট কেন্দ্র", ""),

    ("site_status", "existing", "Existing", "বিদ্যমান", ""),
    ("site_status", "new", "New", "নতুন", ""),
    ("site_status", "closed", "Closed", "বন্ধ", ""),

    ("disaster_type", "flood", "Flood", "বন্যা", ""),
    ("disaster_type", "cyclone", "Cyclone", "ঘূর্ণিঝড়", ""),
    ("disaster_type", "fire", "Fire", "অগ্নিকাণ্ড", ""),
    ("disaster_type", "landslide", "Landslide", "ভূমিধস", ""),
    ("disaster_type", "riverbank_erosion", "Riverbank erosion", "নদীভাঙন", ""),
    ("disaster_type", "other", "Other", "অন্যান্য", ""),

    ("shelter_type", "makeshift", "Makeshift", "অস্থায়ী", ""),
    ("shelter_type", "tarpaulin", "Tarpaulin", "ত্রিপল", ""),
    ("shelter_type", "semi_pucca", "Semi-pucca", "আধা-পাকা", ""),
    ("shelter_type", "pucca", "Pucca (permanent)", "পাকা (স্থায়ী)", ""),
    ("shelter_type", "damaged_no_shelter", "Damaged / no shelter", "ক্ষতিগ্রস্ত / আশ্রয়হীন", ""),

    ("damage_pct_range", "none", "None (0%)", "কোনোটি নয় (০%)", ""),
    ("damage_pct_range", "low_1_25", "1-25%", "১-২৫%", ""),
    ("damage_pct_range", "moderate_26_50", "26-50%", "২৬-৫০%", ""),
    ("damage_pct_range", "high_51_75", "51-75%", "৫১-৭৫%", ""),
    ("damage_pct_range", "severe_76_100", "76-100%", "৭৬-১০০%", ""),

    ("water_source", "tubewell", "Tubewell", "নলকূপ", ""),
    ("water_source", "piped_supply", "Piped supply", "পাইপলাইন সরবরাহ", ""),
    ("water_source", "pond_river", "Pond / river", "পুকুর / নদী", ""),
    ("water_source", "water_trucking", "Water trucking", "পানি সরবরাহ ট্রাক", ""),
    ("water_source", "other", "Other", "অন্যান্য", ""),

    ("functionality_status", "functional", "Fully functional", "সম্পূর্ণ কার্যকর", ""),
    ("functionality_status", "partially_functional", "Partially functional", "আংশিক কার্যকর", ""),
    ("functionality_status", "non_functional", "Non-functional", "অকার্যকর", ""),

    ("latrine_ratio_range", "lt_20", "Fewer than 20 persons per latrine", "২০ জনের কম প্রতি ল্যাট্রিনে", ""),
    ("latrine_ratio_range", "20_50", "20-50 persons per latrine", "২০-৫০ জন প্রতি ল্যাট্রিনে", ""),
    ("latrine_ratio_range", "50_100", "50-100 persons per latrine", "৫০-১০০ জন প্রতি ল্যাট্রিনে", ""),
    ("latrine_ratio_range", "gt_100", "More than 100 persons per latrine", "১০০ জনের বেশি প্রতি ল্যাট্রিনে", ""),

    ("health_concerns", "diarrhea", "Diarrheal disease", "ডায়রিয়া", ""),
    ("health_concerns", "respiratory_infection", "Respiratory infection", "শ্বাসতন্ত্রের সংক্রমণ", ""),
    ("health_concerns", "malnutrition", "Malnutrition", "অপুষ্টি", ""),
    ("health_concerns", "skin_disease", "Skin disease", "চর্মরোগ", ""),
    ("health_concerns", "maternal_health", "Maternal health issues", "মাতৃস্বাস্থ্য সমস্যা", ""),
    ("health_concerns", "mental_health", "Mental health concerns", "মানসিক স্বাস্থ্য সমস্যা", ""),
    ("health_concerns", "other", "Other", "অন্যান্য", ""),

    ("protection_concerns", "child_labor", "Child labor", "শিশুশ্রম", ""),
    ("protection_concerns", "early_marriage", "Early marriage", "বাল্যবিবাহ", ""),
    ("protection_concerns", "gbv_risk", "GBV risk", "জেন্ডারভিত্তিক সহিংসতার ঝুঁকি", ""),
    ("protection_concerns", "family_separation", "Family separation", "পরিবার বিচ্ছিন্নতা", ""),
    ("protection_concerns", "unsafe_shelter_lighting", "Unsafe shelter / lack of lighting", "অনিরাপদ আশ্রয় / আলোর অভাব", ""),
    ("protection_concerns", "documentation_issues", "Documentation issues", "প্রামাণ্য নথিপত্র সমস্যা", ""),
    ("protection_concerns", "other", "Other", "অন্যান্য", ""),

    ("sector_list", "shelter", "Shelter", "আশ্রয়", ""),
    ("sector_list", "wash", "WASH", "ওয়াশ", ""),
    ("sector_list", "health", "Health", "স্বাস্থ্য", ""),
    ("sector_list", "protection", "Protection", "সুরক্ষা", ""),
    ("sector_list", "food_security", "Food security", "খাদ্য নিরাপত্তা", ""),
    ("sector_list", "education", "Education", "শিক্ষা", ""),
    ("sector_list", "livelihoods", "Livelihoods", "জীবিকা", ""),
    ("sector_list", "nutrition", "Nutrition", "পুষ্টি", ""),
]

SETTINGS_HEADER = ["form_title", "form_id", "default_language", "version", "style"]
SETTINGS_ROWS = [
    ("Multi-Sector Rapid Site Assessment", "rapid_site_assessment_v1", "English (en)", "2026091301", "pages"),
]


def write_sheet(wb, title, header, rows):
    ws = wb.create_sheet(title)
    ws.append(header)
    for row in rows:
        ws.append(list(row))
    return ws


def main():
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    write_sheet(wb, "survey", SURVEY_HEADER, SURVEY_ROWS)
    write_sheet(wb, "choices", CHOICES_HEADER, CHOICES_ROWS)
    write_sheet(wb, "settings", SETTINGS_HEADER, SETTINGS_ROWS)
    wb.save(OUT_PATH)
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
