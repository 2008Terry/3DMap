"""Capture the production native inspection scene using the active Windows GPU.

Run: python scripts/validate_native_interiors.py --output .superpowers/interior-validation/before
"""
import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
# QTest.qWait holds Python while the threaded render loop reads Python properties.
os.environ.setdefault("QSG_RENDER_LOOP", "basic")

from PySide6.QtCore import QPointF, QUrl, Qt
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QImage
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
import numpy as np

from native.building_inspector import BuildingInspector
from native.campus_data import load_buildings
from native.map_controller import MapController
from native.gesture_worker import GestureWorker


def main():
    print("Initializing native renderer", flush=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--narrow", action="store_true", help="Validate a narrow inspection viewport")
    parser.add_argument("--upper", action="store_true", help="Capture Shapiro upper floors using PageUp")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    QQuickStyle.setStyle("Fusion")
    app = QApplication([])
    print("Application created", flush=True)
    buildings, extent = load_buildings(ROOT)
    inspector = BuildingInspector(buildings, ROOT)
    controller = MapController(buildings, extent, inspector)
    worker = GestureWorker(ROOT / "native/assets/gesture_recognizer.task")
    engine = QQmlApplicationEngine()
    context = engine.rootContext()
    values = dict(campusBuildings=[], geometryCentral=None, geometryNorth=None,
                  geometryFeatured=[], geometryEnvironment=[], geometryFacades=None,
                  environmentSummary="", mapControllerObject=controller,
                  inspectorObject=inspector, selectionOverlayState=None,
                  gestureWorkerObject=worker,
                  campusBounds=dict(centerX=extent.center_x, centerZ=extent.center_z,
                                    width=extent.width, depth=extent.depth))
    for key, value in values.items():
        context.setContextProperty(key, value)
    engine.load(QUrl.fromLocalFile(str(ROOT / "native/Main.qml")))
    print("Production QML loaded", flush=True)
    if not engine.rootObjects():
        raise RuntimeError("Production QML failed to load")
    window = engine.rootObjects()[0]
    window.setMinimumWidth(720)
    window.setWidth(720 if args.narrow else 1280)
    window.setHeight(1100 if args.narrow else 900)
    from PySide6.QtCore import QObject
    scene = window.findChild(QObject, "mapScene")
    captures = []
    upper_captures = []
    camera = window.findChild(QObject, "mapCamera")
    ids = ["shapiro-undergraduate-library", "burton-memorial-tower"]
    if args.full:
        ids += ["city-BLD-035111", "hatcher-graduate-library"]
    for building_id in ids:
        print(f"Capturing {building_id}", flush=True)
        controller.select_building(building_id)
        inspector.open()
        print("Inspection geometry ready", flush=True)
        wings = inspector.wings or [""]
        for wing in wings:
            if wing:
                inspector.set_wing(wing)
            modes = ["xray", "explode", "inside"] if not args.full else list(inspector.MODES)
            for mode in modes:
                inspector.set_mode(mode)
                if building_id == "burton-memorial-tower" and mode == "explode":
                    inspector.set_spread(24)
                # Do not force reset: production viewRequested must fit the scene.
                print(f"Rendering {mode}", flush=True)
                QTest.qWait(900)
                filename = f"{building_id}-{wing or 'main'}-{mode}.png"
                frame = window.grabWindow()
                if frame.isNull() or not frame.save(str(args.output / filename)):
                    raise RuntimeError(f"Capture failed: {filename}")
                rgba = frame.convertToFormat(QImage.Format_RGBA8888)
                pixels = np.frombuffer(rgba.bits(), dtype=np.uint8).reshape(rgba.height(), rgba.bytesPerLine())
                pixels = pixels[:, :rgba.width() * 4].reshape(rgba.height(), rgba.width(), 4)
                ratio = rgba.width() / window.width()
                origin = scene.mapToScene(QPointF(0, 0))
                left, top = int(origin.x() * ratio), int(origin.y() * ratio)
                right = left + int(scene.property("width") * ratio)
                bottom = top + int(scene.property("height") * ratio)
                viewport = pixels[top:bottom, left:right, :3]
                white_fraction = float(np.mean(np.all(viewport > 245, axis=2)))
                if mode == "xray" and white_fraction > 0.005:
                    raise AssertionError(f"Xray white-surface regression: {white_fraction:.3%}")
                captures.append(dict(file=filename, mode=mode, floors=len(inspector.floors),
                                     bounds=inspector.view_bounds,
                                     white_fraction=white_fraction,
                                     camera=str(camera.property("position"))))
        if args.upper and building_id == "shapiro-undergraduate-library":
            inspector.set_floor(1)
            inspector.set_mode("floor")
            scene.forceActiveFocus()
            for floor_index in (2, 3, 4):
                QTest.keyClick(window, Qt.Key_PageUp)
                assert inspector.selected_floor == floor_index and inspector.mode == "floor"
                QTest.qWait(900)
                filename = f"shapiro-level-{floor_index}.png"
                assert window.grabWindow().save(str(args.output / filename))
                upper_captures.append(filename)
    metadata = dict(graphics_api=scene.property("graphicsApi"), captures=captures,
                    upper_captures=upper_captures)
    (args.output / "capture.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Captured {len(captures)} frames using {metadata['graphics_api']}")
    window.close()
    app.processEvents()


if __name__ == "__main__":
    main()
