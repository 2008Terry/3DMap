from shapely.geometry import Polygon

from native.campus_data import Building
from native.interior_mesh import build_interior


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
