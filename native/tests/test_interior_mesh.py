from shapely.geometry import Polygon
import pytest

from native.campus_data import Building
from native.interior_mesh import build_interior


@pytest.mark.parametrize("building_id,wing", [
    ("shapiro-undergraduate-library", ""), ("city-BLD-035111", ""),
    ("burton-memorial-tower", ""), ("hatcher-graduate-library", "North"),
    ("hatcher-graduate-library", "South"),
])
def test_every_room_has_partition_only_access_from_spawn(building_id, wing):
    import json
    from pathlib import Path
    from shapely.geometry import Point
    from native.campus_data import load_buildings
    from native.interior_mesh import polygons
    root = Path(__file__).resolve().parents[2]
    buildings, _ = load_buildings(root)
    refs = json.loads((root / "native/building_references.json").read_text(encoding="utf-8"))["buildings"]
    profile = refs[building_id]
    if wing:
        profile = {**profile, "floors": [f for f in profile["floors"] if f.get("wing") == wing]}
    building = next(b for b in buildings if b.id == building_id)
    for floor in build_interior(building, profile).floors:
        free = floor["walkable"].buffer(-0.2).difference(floor["collision"].buffer(0.2))
        reachable = next(p for p in polygons(free) if p.covers(Point(floor["start"])))
        for room in floor["rooms"]:
            assert reachable.intersection(room["polygon"]).area > 0.1, (building_id, wing, floor["label"], room["name"])


def test_union_muto_door_remains_connected_after_shared_walls_are_merged():
    import json
    from pathlib import Path
    from shapely.geometry import Point
    from native.campus_data import load_buildings
    from native.interior_mesh import polygons
    root = Path(__file__).resolve().parents[2]
    buildings, _ = load_buildings(root)
    refs = json.loads((root / "native/building_references.json").read_text(encoding="utf-8"))["buildings"]
    building = next(b for b in buildings if b.id == "city-BLD-035111")
    floor = build_interior(building, refs[building.id]).floors[0]
    free = floor["walkable"].buffer(-0.2).difference(floor["collision"].buffer(0.2))
    reachable = next(p for p in polygons(free) if p.covers(Point(floor["start"])))
    room = next(r for r in floor["rooms"] if r["name"] == "MUTO G002")
    assert reachable.intersection(room["polygon"]).area > 0.1


def test_source_regions_do_not_overlap_each_other_or_circulation():
    building = Building(id="test", facility_id="test", name="Test", campus="Central Campus",
                        parts=[{"footprint": [(0, 0), (40, 0), (40, 30), (0, 30)], "height_m": 8}],
                        height_m=8)
    interior = build_interior(building, {"floors": [{"label": "1", "spaces": [
        {"name": "Open reading", "kind": "study", "rect": [0.1, 0.1, 0.8, 0.8]},
        {"name": "Lab", "kind": "lab", "rect": [0.6, 0.1, 0.95, 0.9]},
    ]}]})
    floor = interior.floors[0]
    for i, room in enumerate(floor["rooms"]):
        assert room["polygon"].intersection(floor["corridor"]).area < 1e-6
        for other in floor["rooms"][i + 1:]:
            assert room["polygon"].intersection(other["polygon"]).area < 1e-6
    for key in ("zones", "outline", "ceiling"):
        assert floor[key].indices
    assert floor["ceiling"].bounds_min[1] > 3


def test_rooms_and_walkable_space_stay_within_concave_building():
    building = Building(
        id="example", facility_id="example", name="Example", campus="North Campus",
        parts=[{"footprint": [(0, 0), (30, 0), (30, 10), (10, 10),
                              (10, 30), (0, 30), (0, 0)], "height_m": 11}],
        height_m=11,
    )
    profile = {"floors": [
        {"label": "1", "name": "Ground", "spaces": [
            {"name": "Official named lab", "kind": "lab", "rect": [0.0, 0.0, 0.3, 0.3]}]},
        {"label": "2", "name": "Upper", "spaces": []},
    ]}
    interior = build_interior(building, profile)
    footprint = Polygon(building.parts[0]["footprint"])

    assert len(interior.floors) == 2
    assert interior.floors[0]["rooms"][0]["source_named"]
    for floor in interior.floors:
        for room in floor["rooms"]:
            assert interior.footprint.covers(room["polygon"])
        assert interior.footprint.covers(floor["walkable"])
        assert floor["slab"].indices
        assert footprint.area == interior.footprint.area
