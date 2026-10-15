"""Build the indoor catalogue from the reviewed U-M Library map manifest."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "native"
manifest = json.loads((NATIVE / "assets/references/floorplan_manifest.json").read_text(encoding="utf-8"))

# Names come from official map labels; rectangles are hand-estimated reference zones.
# They are never claimed as surveyed walls, measured rooms, or routing geometry.
spaces = {
    "shapiro-basement": ["Student Parent and Caregiver Study Room", "Compact Shelving", "CAEN Laboratory", "Reflection Room"],
    "shapiro-floor-1": [
        {"name": "Bert's Study Lounge", "kind": "lounge", "rect": [0.02, 0.15, 0.24, 0.38]},
        {"name": "Bert's Cafe", "kind": "cafe", "rect": [0.49, 0.10, 0.92, 0.26]},
        {"name": "Media Production Rooms 1136-1138", "kind": "studio", "rect": [0.02, 0.58, 0.15, 0.68]},
        {"name": "Design Lab Workshop 1128", "kind": "lab", "rect": [0.02, 0.70, 0.15, 0.82]},
        {"name": "Video Production Room 1074", "kind": "studio", "rect": [0.83, 0.78, 0.98, 0.86]},
        {"name": "Design Lab PIE Space", "kind": "lab", "rect": [0.52, 0.89, 0.81, 0.99]},
        {"name": "Computing / Printing Study Space", "kind": "study", "rect": [0.20, 0.60, 0.73, 0.82]},
    ],
    "shapiro-floor-2": ["Askwith Media Library", "Knox Adaptive Technology Center", "Group Study Rooms 2122-2144", "Sweetland Peer Writing Center", "Book Stacks P-Z", "Computing and Printing"],
    "shapiro-floor-3": ["Conference Rooms 3178 and 3180 (nonpublic)", "Digital Scholarship (nonpublic)", "Study Room 3042", "Study Room 3046", "Shapiro Reading Room", "Shapiro Gallery", "Wellbeing Room"],
    "shapiro-floor-4": ["Turkish American Friendship Room (nonpublic)", "Computer and Video Game Archive", "Shapiro 4059", "Science Book Stacks", "Study Space", "Michigan Publishing (nonpublic)"],
    "duderstadt-basement": ["Fabrication Studio", "Multipurpose Space", "Computing Site", "Carillon Practice Room", "AAEL Special Collections"],
    "duderstadt-floor-1": [
        {"name": "Mujo Cafe", "kind": "cafe", "rect": [0.34, 0.04, 0.46, 0.16]},
        {"name": "Duderstadt Center Information Desk", "kind": "desk", "rect": [0.38, 0.27, 0.44, 0.33]},
        {"name": "Study Space", "kind": "study", "rect": [0.51, 0.40, 0.64, 0.57]},
        {"name": "Duderstadt Center Space", "kind": "study", "rect": [0.50, 0.10, 0.77, 0.33]},
    ],
    "duderstadt-floor-2": ["Materials Collection", "Book Arts Studio", "VizHubs", "East Collaboration Rooms", "Southeast Collaboration Rooms", "Computing Site", "Book Stacks"],
    "duderstadt-floor-3": ["Computing Site", "Study Spaces", "Book Stacks A-N and N-NA", "Non-library Duderstadt Center Spaces"],
    "hatcher-north-floor-1": ["Hatcher Gallery Exhibit Room", "Hatcher Gallery Event Space", "Humanities Collaboratory", "Gallery Lab", "International Studies Reading Room", "Book Stacks AC-AZ and PN"],
    "hatcher-north-floor-2": ["Reference Reading Room", "Hatcher 206", "Study Space 212a", "Serials and Microforms", "Computing and Printing"],
    "hatcher-south-floor-1": ["Information Services Desk"],
    "hatcher-south-floor-2": ["Clark Library", "Atlas Cases", "Map Cases", "Clark Library Presentation Space", "Computing Site", "Study Space"],
    "hatcher-south-floor-6": ["Special Collections Research Center", "Reading Room", "Classroom Space", "Study Carrels"],
    "hatcher-south-floor-7": ["Staff Space (nonpublic)"],
    "hatcher-south-floor-8": ["Conference Room 806 (nonpublic)", "Papyrology (nonpublic)", "Library Administration (nonpublic)"],
}

# Reviewed against the bundled official map images on 2026-10-15. Coordinates
# describe coarse semantic regions, not traced or measured architectural walls.
spaces.update({
    "shapiro-floor-2": [
        {"name": "Askwith Media Library 2002", "kind": "collection", "rect": [0.27, 0.0, 0.59, 0.25]},
        {"name": "Learning Programs and Initiatives 2178 (nonpublic)", "kind": "office", "rect": [0.03, 0.15, 0.24, 0.25]},
        {"name": "Conference Room 2166 (nonpublic)", "kind": "room", "rect": [0.03, 0.25, 0.24, 0.39]},
        {"name": "Sweetland Center for Writing 2160", "kind": "office", "rect": [0.03, 0.39, 0.24, 0.57]},
        {"name": "Group Study Rooms 2122-2144", "kind": "room", "rect": [0.03, 0.57, 0.24, 0.85]},
        {"name": "PC Campus Computing Site 2054", "kind": "computing", "rect": [0.73, 0.55, 0.97, 0.70]},
        {"name": "Knox Adaptive Technology Center 2064", "kind": "room", "rect": [0.73, 0.70, 0.97, 0.90]},
        {"name": "Mac Campus Computing Site 2000A", "kind": "computing", "rect": [0.50, 0.56, 0.69, 0.66]},
        {"name": "Book Stacks and Current Periodicals", "kind": "stacks", "rect": [0.28, 0.43, 0.69, 0.85]},
        {"name": "Study Space", "kind": "study", "rect": [0.25, 0.85, 0.73, 0.94]},
    ],
    "shapiro-floor-3": [
        {"name": "Conference Rooms 3178 and 3180 (nonpublic)", "kind": "room", "rect": [0.10, 0.01, 0.35, 0.14]},
        {"name": "Digital Scholarship and Michigan Publishing 3020 (nonpublic)", "kind": "office", "rect": [0.49, 0.01, 0.72, 0.17]},
        {"name": "Deep Blue Repository and Research Data Services (nonpublic)", "kind": "office", "rect": [0.72, 0.17, 0.96, 0.30]},
        {"name": "Shapiro Gallery 3060", "kind": "gallery", "rect": [0.03, 0.37, 0.25, 0.48]},
        {"name": "Wellbeing Room 3021", "kind": "room", "rect": [0.45, 0.43, 0.61, 0.48]},
        {"name": "Study Room 3042", "kind": "room", "rect": [0.79, 0.43, 0.89, 0.47]},
        {"name": "Study Room 3046", "kind": "room", "rect": [0.87, 0.47, 0.97, 0.52]},
        {"name": "Open Study Space", "kind": "study", "rect": [0.05, 0.50, 0.95, 0.85]},
        {"name": "Shapiro Reading Room 3100", "kind": "reading", "rect": [0.20, 0.86, 0.73, 0.99]},
    ],
    "shapiro-floor-4": [
        {"name": "Turkish American Friendship Room 4004 (nonpublic)", "kind": "room", "rect": [0.49, 0.0, 0.67, 0.14]},
        {"name": "Michigan Publishing and University of Michigan Press 4190 (nonpublic)", "kind": "office", "rect": [0.02, 0.12, 0.24, 0.37]},
        {"name": "Study Space", "kind": "study", "rect": [0.27, 0.18, 0.63, 0.28]},
        {"name": "Science Oversize Book Stacks S-Z", "kind": "stacks", "rect": [0.65, 0.20, 0.88, 0.31]},
        {"name": "Book Stacks AC-QE", "kind": "stacks", "rect": [0.08, 0.40, 0.27, 0.84]},
        {"name": "Book Stacks QL-S", "kind": "stacks", "rect": [0.74, 0.40, 0.92, 0.46]},
        {"name": "Computer and Video Game Archive 4041", "kind": "computing", "rect": [0.72, 0.48, 0.94, 0.69]},
        {"name": "Shapiro 4059", "kind": "room", "rect": [0.72, 0.69, 0.94, 0.85]},
        {"name": "Book Stacks QE-QL", "kind": "stacks", "rect": [0.29, 0.86, 0.72, 0.94]},
    ],
})
groups = {
    "shapiro": {"id": "shapiro-undergraduate-library", "name": "Shapiro Library", "facility_ids": ["BLD-034816"]},
    "duderstadt": {"id": "city-BLD-034963", "name": "Duderstadt Center", "facility_ids": ["BLD-034963", "BLD-037733"]},
    "hatcher": {"id": "hatcher-graduate-library", "name": "Hatcher Library", "facility_ids": ["BLD-034813"]},
}
profiles = {}
for group, metadata in groups.items():
    records = [r for r in manifest if r["group"].startswith(group) and "group-study" not in r["key"]]
    def level_key(record):
        level = record["level"]
        if level.startswith("basement"):
            return -2 if level == "basement" else -1
        return int(level.split("-")[-1].rstrip("a")) + (0.5 if level.endswith("a") else 0)
    records.sort(key=lambda r: (r["group"], level_key(r)))
    floors = []
    for record in records:
        names = spaces.get(record["key"], [])
        if not names:
            description = record["description"].lower()
            names = (["Book Stacks", "Study Space"] if "book stacks" in description else ["Study Space"])
        floor = {k: record[k] for k in ("source_url", "pdf_url", "plan_asset", "plan_pdf")}
        floor.update(label=record["label"].replace("Floor ", ""), name=record["label"],
                     mapping="approximate source zones; walls and furniture inferred",
                     spaces=[v if isinstance(v, dict) else {"name": v, "kind": "stacks" if "Stack" in v or "Shelving" in v else "study"} for v in names])
        if group == "hatcher":
            floor["wing"] = "North" if "north" in record["group"] else "South"
        floors.append(floor)
    photos = []
    candidates = json.loads((NATIVE / "assets/references/photo_sources.json").read_text(encoding="utf-8"))
    # Official staff-authored images with no identifiable people; all others retain source links only.
    for candidate in candidates:
        if candidate["building"] == group:
            photo = {k: candidate[k] for k in ("source_url", "image_url", "alt")}
            if candidate["key"] in ("shapiro-photo-0", "shapiro-photo-3", "duderstadt-photo-0"):
                photo["asset"] = candidate["asset"]
            photos.append(photo)
    profile = {**metadata, "evidence_level": "official floor maps with approximate 3D registration",
               "mapping_status": "schematic walls, circulation, stairs and furniture",
               "floors": floors, "photos": photos,
               "sources": [{"label": "University of Michigan Library floor plans", "url": records[0]["source_url"]},
                           {"label": "U-M Library CC-BY copyright policy", "url": "https://lib.umich.edu/about-us/policies/copyright-policy/"}]}
    profiles[metadata["id"]] = profile
profiles["city-BLD-035111"] = {
    "name": "Michigan Union", "facility_ids": ["BLD-035111", "BLD-036687"],
    "evidence_level": "official floor labels and selected named spaces; schematic 3D",
    "sources": [{"label": "Michigan Union floor plans", "url": "https://uunions.umich.edu/union/"},
                {"label": "Michigan Union tour", "url": "https://uunions.umich.edu/michigan-union-walking-tour/"}],
    "floors": [
        {"label": "G", "name": "Ground Floor", "spaces": [{"name": "MUTO G002", "kind": "office"}]},
        {"label": "1", "name": "First Floor", "spaces": [{"name": "Campus Information Center", "kind": "desk"}]},
        {"label": "2", "name": "Second Floor", "spaces": [{"name": "IdeaHub", "kind": "study"}]},
        {"label": "3", "name": "Third Floor", "spaces": []},
        {"label": "4", "name": "Fourth Floor", "spaces": [{"name": "Reflection Room 4302", "kind": "lounge"}]},
    ],
}
for floor in profiles["city-BLD-035111"]["floors"]:
    floor["source_url"] = "https://uunions.umich.edu/union/"
profiles["city-BLD-034968"] = {
    "name": "Beyster Building", "facility_ids": ["BLD-034968"],
    "evidence_level": "official first-floor room labels; other levels inferred",
    "sources": [{"label": "CSE Beyster floor map", "url": "https://cse.engin.umich.edu/wp-content/uploads/sites/3/2019/03/beyster_map.pdf"},
                {"label": "CSE meeting and event facilities", "url": "https://cse.engin.umich.edu/about/our-facilities/scheduling-for-meetings-and-events/"}],
    "floors": [{"label": "1", "name": "First Floor", "source_url": "https://cse.engin.umich.edu/wp-content/uploads/sites/3/2019/03/beyster_map.pdf",
                "spaces": [{"name": n, "kind": k} for n, k in [("Tishman Hall 1665", "lounge"), ("Classroom 1690", "classroom"), ("Classroom 1670", "classroom"), ("Student Orgs 1648-1648D", "office"), ("CAEN Lab East 1620", "lab"), ("CAEN Lab West 1695", "lab"), ("Learning Center 1637-1637B", "study"), ("Student Projects 1625", "lab")]]}],
}
profiles["city-BLD-034968"]["floors"].extend(
    {"label": str(i), "name": f"示意 {i} 层（未核实）", "basis": "inferred", "spaces": []}
    for i in range(2, 5)
)
profiles["burton-memorial-tower"] = {
    "name": "Burton Memorial Tower", "facility_ids": ["BLD-000825"],
    "evidence_level": "official tenth-floor bell chamber; basement and catalog from user review",
    "mapping_status": "schematic heights, rooms and circulation; no surveyed floor plans",
    "interior_notice": "B + 1–10 层目录按测试反馈修正 · 官方资料确认 10 层钟室；地下室待独立核实，室内结构为示意",
    "sources": [
        {"label": "U-M Regents: tenth-floor bell chamber (2010)",
         "url": "https://regents.umich.edu/files/meetings/06-10/2010-6-IX-6.pdf"},
        {"label": "SMTD Burton Memorial Tower", "url": "https://smtd.umich.edu/facilities/burton-memorial-tower/"},
    ],
    "floors": [{"label": label, "name": "地下室（目录待独立核实）" if label == "B" else
                "钟室 · 10 层" if label == "10" else f"{label} 层（室内示意）",
                "basis": "inferred", "catalog_basis": "user-reviewed basement plus ten floors",
                "catalog_source_url": "https://regents.umich.edu/files/meetings/06-10/2010-6-IX-6.pdf",
                "spaces": []} for label in ["B"] + [str(i) for i in range(1, 11)]],
}

data = {"schema_version": 1, "accessed": "2026-10-15", "buildings": profiles,
        "asset_license": {"attribution": "University of Michigan Library", "license": "CC-BY 4.0",
                          "url": "https://creativecommons.org/licenses/by/4.0/",
                          "policy": "https://lib.umich.edu/about-us/policies/copyright-policy/",
                          "modifications": "PDFs unchanged; PNG floor plans rasterized for local reference viewer"}}
(NATIVE / "building_references.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Catalogued {len(profiles)} building profiles and {sum(len(p['floors']) for p in profiles.values())} floor entries")
