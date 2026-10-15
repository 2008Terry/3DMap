from pathlib import Path
from math import cos, radians, sin, tan
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QThread
from shapely.geometry import Point

from native.building_inspector import BuildingInspector
from native.campus_data import load_buildings
from native.gesture_worker import GestureWorker
from native.map_controller import MapController

ROOT = Path(__file__).resolve().parents[2]


def test_burton_catalog_and_expanded_bounds():
    app = QGuiApplication.instance() or QGuiApplication([])
    buildings, _ = load_buildings(ROOT)
    inspector = BuildingInspector(buildings, ROOT)
    inspector.select("burton-memorial-tower")
    inspector.open()
    assert [floor["label"] for floor in inspector.floors] == ["B"] + [str(i) for i in range(1, 11)]
    inspector.set_mode("explode")
    inspector.set_spread(24)
    bounds = inspector.view_bounds
    assert bounds["height"] >= 11 * 3.6 + 10 * 24
    assert bounds["centerY"] > inspector.bounds["height"] / 2
    for width, height in ((900, 700), (400, 1000)):
        fit = inspector.fit_view(width, height, 48)
        distance = (fit["y"] ** 2 + fit["z"] ** 2) ** 0.5
        for x in (-bounds["width"] / 2, bounds["width"] / 2):
            for y in (-bounds["height"] / 2, bounds["height"] / 2):
                for z in (-bounds["depth"] / 2, bounds["depth"] / 2):
                    camera_depth = distance - y * sin(radians(38)) - z * cos(radians(38))
                    screen_y = y * cos(radians(38)) - z * sin(radians(38))
                    assert abs(screen_y) / camera_depth < tan(radians(24))
                    assert abs(x) / camera_depth < tan(radians(24)) * width / height


def test_thumb_floor_navigation_preserves_structure_view():
    from native.gesture_input import HandFrame
    app = QGuiApplication.instance() or QGuiApplication([])
    buildings, extent = load_buildings(ROOT)
    inspector = BuildingInspector(buildings, ROOT)
    inspector.select("shapiro-undergraduate-library")
    inspector.open()
    controller = MapController(buildings, extent, inspector)
    for mode in ("dollhouse", "section", "xray", "explode", "floor"):
        inspector.set_floor(1)
        inspector.set_mode(mode)
        controller._last_floor_at = 0
        controller._last_frame_at = __import__("time").monotonic()
        controller._frame = HandFrame("Thumb_Up", 0.5, True, (0.5, 0.5), (0.5, 0.5), True, 0.2)
        controller._gesture_tick()
        assert inspector.selected_floor == 2
        assert inspector.mode == mode


def test_floor_changes_preserve_all_inspection_modes():
    app = QGuiApplication.instance() or QGuiApplication([])
    buildings, _ = load_buildings(ROOT)
    inspector = BuildingInspector(buildings, ROOT)
    inspector.select("shapiro-undergraduate-library")
    inspector.open()
    for mode in inspector.MODES:
        inspector.set_floor(1)
        inspector.set_mode(mode)
        inspector.change_floor(1)
        assert inspector.mode == mode
        assert inspector.selected_floor == 2
        inspector.change_floor(100)
        assert inspector.selected_floor == len(inspector.floors) - 1
        inspector.change_floor(-100)
        assert inspector.selected_floor == 0


def test_official_floor_assets_wings_and_collision():
    app = QGuiApplication.instance() or QGuiApplication([])
    buildings, _ = load_buildings(ROOT)
    inspector = BuildingInspector(buildings, ROOT)
    inspector.select("shapiro-undergraduate-library")
    assert not inspector.floors
    inspector.open()
    assert inspector.active
    assert inspector.current_floor["label"] == "1"
    assert inspector.plan_url.endswith("shapiro-floor-1.png")
    assert any(room["name"] == "Bert's Cafe" for room in inspector.rooms)
    floor = inspector._layout.floors[inspector.selected_floor]
    x, z = floor["start"]
    assert not floor["collision"].covers(Point(x, z))
    assert not floor["furniture_collision"].covers(Point(x, z))
    assert not inspector.can_walk(x, z, 100000, 100000)
    obstacle = floor["furniture_collision"].representative_point()
    assert not inspector.can_walk(x, z, obstacle.x, obstacle.y)
    inspector.select("hatcher-graduate-library")
    assert inspector.wings == ["North", "South"]
    inspector.set_wing("South")
    assert len(inspector.floors) == 8
    assert inspector.plan_url.endswith("hatcher-south-floor-1.png")
    inspector.set_floor(99)
    assert inspector.selected_floor == 7
    inspector.close()
    assert not inspector.active


def test_worker_signal_reaches_controller_on_gui_thread():
    app = QGuiApplication.instance() or QGuiApplication([])
    buildings, extent = load_buildings(ROOT)
    controller = MapController(buildings, extent)
    worker = GestureWorker(ROOT / "native/assets/gesture_recognizer.task")
    worker.gesture_changed.connect(controller.handle_recognition)
    events = []
    controller.zoomRequested.connect(lambda value: events.append((value, QThread.currentThread())))

    class Emitter(QThread):
        def run(self):
            worker.gesture_changed.emit("Thumb_Up", "拇指向上", 0.95, [])
    emitter = Emitter()
    emitter.start()
    emitter.wait()
    app.processEvents()
    assert events == [(0.82, app.thread())]
