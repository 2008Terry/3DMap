import importlib.util
import sys
from pathlib import Path

import pytest
from shapely.geometry import Polygon

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "native" / "map_controller.py"


def load_controller():
    assert MODULE_PATH.is_file(), "native map controller has not been implemented"
    sys.path.insert(0, str(ROOT / "native"))
    spec = importlib.util.spec_from_file_location("map_controller", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_search_and_selected_details_cover_featured_and_generic_buildings():
    from native.campus_data import load_buildings

    module = load_controller()
    buildings, extent = load_buildings(ROOT)
    controller = module.MapController(buildings, extent)

    results = controller.search("hArLaN hAtChEr")
    generic_results = controller.search("BLD-000023")
    details = controller.select_building("hatcher-graduate-library")
    generic = next(item for item in buildings if item.id == generic_results[0]["id"])
    point = Polygon(generic.parts[0]["footprint"]).representative_point()
    picked_id = controller.select_at(point.x, generic.height_m / 2, point.y)

    assert results[0]["id"] == "hatcher-graduate-library"
    assert generic_results
    assert generic_results[0]["campus"] == "North Campus"
    assert details["featured"] is True
    assert details["facts"]
    assert details["sources"]
    assert picked_id == generic.id
    assert controller.gesture_status == "Gesture camera inactive"


def test_camera_methods_emit_qml_requests():
    from native.campus_data import load_buildings

    module = load_controller()
    buildings, extent = load_buildings(ROOT)
    controller = module.MapController(buildings, extent)
    events = []
    controller.resetCameraRequested.connect(lambda: events.append(("reset",)))
    controller.panRequested.connect(lambda x, y: events.append(("pan", x, y)))
    controller.zoomRequested.connect(lambda factor: events.append(("zoom", factor)))

    controller.reset_camera()
    controller.pan_by(20, -10)
    controller.zoom_by(0.8)

    assert events == [("reset",), ("pan", 20.0, -10.0), ("zoom", 0.8)]
