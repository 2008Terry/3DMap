from pathlib import Path

import pytest
import numpy as np
from PySide6.QtGui import QGuiApplication
from shapely.geometry import LineString, Point, box

from native.building_inspector import BuildingInspector
from native.campus_data import load_buildings
from native import structure_visibility as visibility
from native.interior_mesh import polygons

ROOT = Path(__file__).resolve().parents[2]


def test_ray_ignores_discarded_wall_and_never_hits_empty_bounding_box():
    wall = np.array([[[-1, 2, -1], [1, 2, -1], [0, 2, 1]]], dtype=float)
    slab = wall.copy()
    slab[:, :, 1] = 0.1
    meshes = {"walls": wall, "slab": slab}
    lens = {"x": 0, "z": 0, "radius": 3}
    args = (meshes, (0, 5, 0), (0, -1, 0), lens)
    assert visibility.nearest_visible_hit(*args, False, 0)["surface"] == "walls"
    result = visibility.nearest_visible_hit(*args, True, 0)
    assert result["surface"] == "slab" and result["y"] == pytest.approx(0.1)
    assert visibility.nearest_visible_hit(meshes, (0.9, 5, 0.9), (0, -1, 0), lens, True, 0) == {}


def inspector_for(building_id):
    app = QGuiApplication.instance() or QGuiApplication([])
    buildings, _ = load_buildings(ROOT)
    inspector = BuildingInspector(buildings, ROOT)
    inspector.select(building_id)
    inspector.open()
    return app, inspector


def test_disconnected_room_is_not_linked_through_wall():
    floor = {"walkable": box(0, 0, 20, 10), "collision": box(9, 0, 11, 10),
             "corridor": box(1, 1, 4, 9), "rooms": [
                 {"name": "Near", "polygon": box(5, 1, 8, 9), "kind": "room", "mapping": "schematic"},
                 {"name": "Far", "polygon": box(12, 1, 19, 9), "kind": "room", "mapping": "schematic"}]}
    graph = visibility.build_floor_graph(floor, 0)
    assert [r["connected"] for r in graph["rooms"]] == [True, False]
    assert visibility.room_route(floor, floor["rooms"][1]) == []


def test_route_bends_around_wall_and_respects_clearance():
    floor = {"walkable": box(0, 0, 20, 12), "collision": box(8, 0, 10, 9),
             "corridor": box(1, 2, 5, 5), "rooms": [
                 {"name": "Target", "polygon": box(12, 1, 19, 8), "kind": "room", "mapping": "schematic"}]}
    route = visibility.room_route(floor, floor["rooms"][0])
    assert len(route) > 2
    free = floor["walkable"].difference(floor["collision"].buffer(0.23))
    assert free.buffer(1e-6).covers(LineString(route))
    assert floor["corridor"].covers(Point(route[0]))
    assert floor["rooms"][0]["polygon"].covers(Point(route[-1]))


def test_burton_expansion_includes_pulled_floor_and_keeps_all_levels():
    app, inspector = inspector_for("burton-memorial-tower")
    state = visibility.StructureVisibility(inspector)
    state.open()
    assert state.active
    assert [f["label"] for f in state.floors] == ["B"] + [str(i) for i in range(1, 11)]
    state.set_unfold(1)
    state.select_floor(10)
    assert len(state.links) == 10
    assert state.bounds["height"] > inspector.bounds["height"]
    assert state.bounds["width"] > inspector.bounds["width"]
    for f in state.floors:
        position = state.floor_position(f["index"])
        assert state.bounds["minX"] <= position["x"] - inspector.bounds["width"] / 2
        assert position["y"] + 3.6 <= state.bounds["maxY"] + 1e-6
    state.set_unfold(0)
    assert state.floor_position(10) == {"x": 0.0, "y": 36.0, "z": 0.0}


def test_room_selection_syncs_plan_portals_and_connection_then_wing_clears_it():
    app, inspector = inspector_for("shapiro-undergraduate-library")
    state = visibility.StructureVisibility(inspector)
    state.open()
    state.select_floor(2)
    state.select_space(0)
    assert inspector.selected_floor == state.floor_index == 2
    assert state.selected_space["id"] == state.spaces[0]["id"]
    assert state.portals[0]["floor"] == 2
    assert len({p["yaw"] for p in state.portals}) > 1
    if state.selected_space["connected"]:
        assert state.route_points
        free = inspector._layout.floors[2]["walkable"].difference(inspector._layout.floors[2]["collision"].buffer(0.23))
        assert free.buffer(1e-6).covers(LineString(state.route_points))
    inspector.select("hatcher-graduate-library")
    inspector.set_wing("South")
    assert state.selected_space == {}
    assert len(state.floors) == 8
    state.close()
    assert not state.active
    state.open()
    assert state.active
    inspector.close()
    assert not state.active


def test_plan_selection_checks_footprint_and_floor_boundaries():
    app, inspector = inspector_for("city-BLD-035111")
    state = visibility.StructureVisibility(inspector)
    state.open()
    old = state.floor_index
    state.select_floor(999)
    assert state.floor_index == old
    assert not state.pick_plan(1e6, 1e6)
    room = state.spaces[0]
    assert state.pick_plan(room["x"], room["z"])
    assert state.selected_space["id"] == room["id"]


def test_clicking_disconnected_part_of_shapiro_room_does_not_route_to_other_part():
    app, inspector = inspector_for("shapiro-undergraduate-library")
    state = visibility.StructureVisibility(inspector)
    state.open()
    state.select_floor(3)
    floor = inspector._layout.floors[3]
    room = next(r for r in floor["rooms"] if r["name"] == "Wellbeing Room 3021")
    assert len(polygons(room["polygon"])) > 1
    _, component, _ = visibility._circulation(floor)
    disconnected = next(p for p in polygons(room["polygon"]) if p.intersection(component).area < 0.1)
    point = disconnected.representative_point()
    assert state.pick_plan(point.x, point.y)
    assert not state.selected_space["connected"]
    assert state.route_points == []
