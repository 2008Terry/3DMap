import importlib.util
import sys
from pathlib import Path

import pytest
from PySide6.QtGui import QGuiApplication
from shapely.geometry import Polygon

from native.campus_data import Building


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "native" / "mesh_builder.py"
_APP = QGuiApplication.instance() or QGuiApplication([])


def load_mesh_builder():
    assert MODULE_PATH.is_file(), "native campus mesh builder has not been implemented"
    sys.path.insert(0, str(ROOT / "native"))
    spec = importlib.util.spec_from_file_location("mesh_builder", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_concave_building_top_is_fully_triangulated():
    builder = load_mesh_builder()
    ring = [(0, 0), (4, 0), (4, 1), (1, 1), (1, 4), (0, 4), (0, 0)]
    building = Building(
        id="concave", facility_id="test", name="Concave", campus="Central Campus",
        parts=[{"object_id": "part-1", "footprint": ring, "height_m": 6.0}],
        height_m=6.0,
    )

    mesh = builder.build_campus_mesh([building])

    roof_area = 0.0
    for offset in range(0, len(mesh.indices), 3):
        triangle_indices = mesh.indices[offset:offset + 3]
        if all(mesh.normals[index * 3 + 1] > 0.99 for index in triangle_indices):
            a, b, c = (mesh.positions[index * 3:index * 3 + 3] for index in triangle_indices)
            roof_area += abs((b[0] - a[0]) * (c[2] - a[2]) - (b[2] - a[2]) * (c[0] - a[0])) / 2

    assert roof_area == pytest.approx(Polygon(ring).area)
    assert mesh.bounds_min[1] == pytest.approx(0)
    assert mesh.bounds_max[1] == pytest.approx(6)


def test_geometry_provider_uploads_position_normal_color_and_indices():
    from native.geometry_provider import geometry_from_buffers

    builder = load_mesh_builder()
    building = Building(
        id="box", facility_id="test", name="Box", campus="Central Campus",
        parts=[{"object_id": "part-1", "footprint": [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)], "height_m": 4.0}],
        height_m=4.0,
    )
    geometry = geometry_from_buffers(builder.build_campus_mesh([building]))

    assert geometry.stride() == 40
    assert geometry.attributeCount() == 4
    assert geometry.indexData()
    assert geometry.vertexData()


def test_featured_angell_mesh_contains_sourced_columns_and_window_bays():
    from native.campus_data import load_buildings

    builder = load_mesh_builder()
    buildings, _ = load_buildings(ROOT)
    angell = next(building for building in buildings if building.id == "angell-hall")

    mesh = builder.build_featured_mesh(angell)

    colors = {tuple(round(value, 2) for value in mesh.colors[offset:offset + 4])
              for offset in range(0, len(mesh.colors), 4)}
    assert (0.13, 0.2, 0.24, 1.0) in colors
    assert len(mesh.indices) > 500


def test_selection_overlay_is_a_thin_surface_above_the_building_roof():
    builder = load_mesh_builder()
    building = Building(
        id="selected", facility_id="test", name="Selected", campus="Central Campus",
        parts=[{"object_id": "part-1", "footprint": [(0, 0), (3, 0), (3, 2), (0, 2), (0, 0)], "height_m": 5.0}],
        height_m=5.0,
    )

    overlay = builder.build_selection_mesh(building)

    assert overlay.bounds_min[1] > building.height_m
    assert overlay.bounds_max[1] < building.height_m + 0.5
    assert overlay.indices
