from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QMessageBox

from campus_data import load_buildings
from geometry_provider import SelectionOverlay, geometry_from_buffers
from mesh_builder import build_campus_mesh, build_featured_mesh, build_selection_mesh
from map_controller import MapController
from gesture_worker import GestureWorker


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    app = QApplication(sys.argv)
    app.setApplicationName("Michigan Campus Map")

    try:
        buildings, extent = load_buildings(repo_root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        QMessageBox.critical(None, "Campus data could not be loaded", str(error))
        return 1

    generic_buildings = [building for building in buildings if not building.featured]
    central_geometry = geometry_from_buffers(build_campus_mesh([
        building for building in generic_buildings if building.campus == "Central Campus"
    ]))
    north_geometry = geometry_from_buffers(build_campus_mesh([
        building for building in generic_buildings if building.campus == "North Campus"
    ]))
    featured_geometries = [
        geometry_from_buffers(build_featured_mesh(building))
        for building in buildings if building.featured
    ]
    map_controller = MapController(buildings, extent)
    gesture_worker = GestureWorker(repo_root / "native" / "assets" / "gesture_recognizer.task")
    selection_overlay = SelectionOverlay()
    buildings_by_id = {building.id: building for building in buildings}

    def update_selection(building_id: str) -> None:
        building = buildings_by_id.get(building_id)
        geometry = geometry_from_buffers(build_selection_mesh(building)) if building else None
        selection_overlay.setGeometry(geometry)

    map_controller.selectionChanged.connect(update_selection)
    gesture_worker.status_changed.connect(map_controller.set_gesture_status)
    gesture_worker.gesture_changed.connect(map_controller.handle_gesture)
    app.aboutToQuit.connect(gesture_worker.stop)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("campusBuildings", [building.to_qml() for building in buildings])
    engine.rootContext().setContextProperty("geometryCentral", central_geometry)
    engine.rootContext().setContextProperty("geometryNorth", north_geometry)
    engine.rootContext().setContextProperty("geometryFeatured", featured_geometries)
    engine.rootContext().setContextProperty("mapControllerObject", map_controller)
    engine.rootContext().setContextProperty("selectionOverlayState", selection_overlay)
    engine.rootContext().setContextProperty("gestureWorkerObject", gesture_worker)
    engine.rootContext().setContextProperty("campusBounds", {
        "centerX": extent.center_x,
        "centerZ": extent.center_z,
        "width": extent.width,
        "depth": extent.depth,
    })
    qml_path = Path(__file__).with_name("Main.qml")
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    if not engine.rootObjects():
        QMessageBox.critical(None, "Campus map could not start", f"Could not load {qml_path}")
        return 1
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
