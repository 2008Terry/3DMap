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
data = {"schema_version": 1, "accessed": "2026-10-12", "buildings": profiles,
        "asset_license": {"attribution": "University of Michigan Library", "license": "CC-BY 4.0",
                          "url": "https://creativecommons.org/licenses/by/4.0/",
                          "policy": "https://lib.umich.edu/about-us/policies/copyright-policy/",
                          "modifications": "PDFs unchanged; PNG floor plans rasterized for local reference viewer"}}
(NATIVE / "building_references.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Catalogued {len(profiles)} building profiles and {sum(len(p['floors']) for p in profiles.values())} floor entries")
