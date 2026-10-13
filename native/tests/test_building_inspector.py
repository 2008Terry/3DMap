from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QThread
from shapely.geometry import Point

from native.building_inspector import BuildingInspector
from native.campus_data import load_buildings
from native.gesture_worker import GestureWorker
from native.map_controller import MapController

ROOT = Path(__file__).resolve().parents[2]


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
