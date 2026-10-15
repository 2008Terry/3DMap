"""Exercise production QML on the Windows hardware renderer, with no webcam."""
import json
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["QSG_RHI_BACKEND"] = "d3d11"
os.environ["QSG_INFO"] = "1"
os.environ["QSG_RENDER_LOOP"] = "basic"
os.environ["QT_LOGGING_RULES"] = "qt.rhi.general=true"

from PySide6.QtCore import QObject, QPoint, QPointF, QUrl, Qt, qInstallMessageHandler
from PySide6.QtQml import QQmlApplicationEngine, QQmlExpression, QQmlEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from native.building_inspector import BuildingInspector
from native.campus_data import load_buildings
from native.gesture_worker import GestureWorker
from native.map_controller import MapController
from native.structure_visibility import StructureVisibility


def find_visual_item(item, name):
    if item.objectName() == name:
        return item
    for child in item.childItems():
        found = find_visual_item(child, name)
        if found is not None:
            return found
    return None


def main():
    output = ROOT / ".superpowers/structure-visibility-validation"
    output.mkdir(parents=True, exist_ok=True)
    messages = []

    def log(kind, context, message):
        messages.append(message)
        print(message, flush=True)

    qInstallMessageHandler(log)
    QQuickStyle.setStyle("Fusion")
    app = QApplication([])
    buildings, extent = load_buildings(ROOT)
    inspector = BuildingInspector(buildings, ROOT)
    state = StructureVisibility(inspector)
    controller = MapController(buildings, extent, inspector)
    app.installEventFilter(controller)
    worker = GestureWorker(ROOT / "native/assets/gesture_recognizer.task")
    engine = QQmlApplicationEngine()
    values = dict(campusBuildings=[], geometryCentral=None, geometryNorth=None,
                  geometryFeatured=[], geometryEnvironment=[], geometryFacades=None,
                  environmentSummary="", mapControllerObject=controller,
                  inspectorObject=inspector, structureObject=state, selectionOverlayState=None,
                  gestureWorkerObject=worker,
                  campusBounds=dict(centerX=extent.center_x, centerZ=extent.center_z,
                                    width=extent.width, depth=extent.depth))
    for key, value in values.items():
        engine.rootContext().setContextProperty(key, value)
    engine.load(QUrl.fromLocalFile(str(ROOT / "native/Main.qml")))
    assert engine.rootObjects(), "Production Main.qml could not load"
    window = engine.rootObjects()[0]
    explorer = window.findChild(QObject, "structureExplorer")
    assert explorer is not None, "Combined structural explorer is missing from production UI"
    window.setWidth(1440)
    window.setHeight(880)
    overview = window.findChild(QObject, "structureOverview")
    plan_view = window.findChild(QObject, "structurePlan")
    captures = []
    performance = []
    swaps = []
    window.frameSwapped.connect(lambda: swaps.append(time.monotonic()))
    started = time.monotonic()
    click_checks = []
    for building_id in ("shapiro-undergraduate-library", "city-BLD-035111",
                        "burton-memorial-tower", "hatcher-graduate-library"):
        print("SCENARIO", building_id, flush=True)
        controller.select_building(building_id)
        inspector.open()
        state.open()
        assert not controller._window_active, "Underlying gesture input was not suspended"
        for wing in inspector.wings or [""]:
            if wing:
                inspector.set_wing(wing)
            state.select_floor(min(2, len(state.floors) - 1))
            if state.spaces:
                state.select_space(0)
            state.set_unfold(0.65)
            state.set_cut(True)
            QTest.qWait(1200)
            name = f"{building_id}-{wing or 'main'}"
            frame = window.grabWindow()
            assert not frame.isNull() and frame.save(str(output / f"{name}.png"))
            captures.append({"file": f"{name}.png", "floors": len(state.floors),
                             "room": state.selected_space.get("name"), "routePoints": len(state.route_points),
                             "api": explorer.property("graphicsApi"), "bounds": state.bounds})
            assert explorer.property("graphicsApi") in ("Direct3D 11", "D3D11"), repr(explorer.property("graphicsApi"))
            # Exercise the real plan click path, not only the Python selection slot.
            if len(state.spaces) > 1:
                target = state.spaces[1]
                bounds = state.plan["bounds"]
                px = plan_view.property("originX") + (target["x"] - bounds[0]) * plan_view.property("scaleFactor")
                py = plan_view.property("originY") + (target["z"] - bounds[1]) * plan_view.property("scaleFactor")
                location = plan_view.mapToScene(QPointF(px, py))
                QTest.mouseClick(window, Qt.LeftButton, Qt.NoModifier, QPoint(round(location.x()), round(location.y())))
                assert state.selected_space.get("id") == target["id"]
            # Project actual room points into the live opposite-camera portal.
            QTest.qWait(100)
            portal = find_visual_item(window.contentItem(), "structurePortalCurrent")
            assert portal is not None
            portal.setProperty("pitch", 80.0)
            QTest.qWait(120)
            selected_by_3d = False
            for target in state.spaces:
                core = state.plan["core"]
                state.pick_plan(core["x"], core["z"])
                assert state.selected_space == {}, "3D click test must start without a selection"
                QTest.qWait(50)
                portal = find_visual_item(window.contentItem(), "structurePortalCurrent")
                portal.setProperty("pitch", 80.0)
                QTest.qWait(80)
                expression = QQmlExpression(QQmlEngine.contextForObject(portal), portal,
                    f"projectPoint({target['x']}, 0.16, {target['z']})")
                evaluated = expression.evaluate()
                point = evaluated[0] if isinstance(evaluated, tuple) else evaluated
                assert not expression.hasError(), expression.error().toString()
                location = portal.mapToScene(QPointF(point.x(), point.y()))
                QTest.mouseClick(window, Qt.LeftButton, Qt.NoModifier, QPoint(round(location.x()), round(location.y())))
                if state.selected_space.get("id") == target["id"]:
                    selected_by_3d = True
                    break
            assert selected_by_3d, f"3D projection selection failed: {name}"
            click_checks.append({"building": name, "selected_space": state.selected_space["id"]})
            portal.setProperty("pitch", 63.0)
            # M must not change the underlying inspection mode while covered.
            mode = inspector.mode
            explorer.forceActiveFocus()
            QTest.keyClick(window, Qt.Key_M)
            assert inspector.mode == mode
            if building_id == "shapiro-undergraduate-library":
                state.set_cut(False)
                QTest.qWait(500)
                assert window.grabWindow().save(str(output / "shapiro-walls-restored.png"))
                state.set_cut(True)
                state.set_unfold(0)
                QTest.qWait(500)
                assert window.grabWindow().save(str(output / "shapiro-folded.png"))
            if building_id == "burton-memorial-tower":
                state.set_unfold(1)
                state.select_floor(len(state.floors) - 1)
                window.setWidth(1050)
                QTest.qWait(1000)
                assert window.grabWindow().save(str(output / "burton-narrow-expanded.png"))
                window.setWidth(1440)
            before = len(swaps)
            t0 = time.monotonic()
            for frame_index in range(30):
                overview.setProperty("yaw", 32.0 + frame_index * 0.6)
                QTest.qWait(16)
            duration = time.monotonic() - t0
            performance.append({"building": name, "rendered_frames": len(swaps) - before,
                                "seconds": duration, "updates_per_second": (len(swaps) - before) / duration})
            overview.setProperty("yaw", 32.0)
            explorer.forceActiveFocus()
            current = state.floor_index
            QTest.keyClick(window, Qt.Key_PageDown)
            assert state.floor_index == max(0, current - 1)
            QTest.keyClick(window, Qt.Key_Escape)
            assert not state.active
            state.open()
            QTest.qWait(100)
    state.close()
    errors = [m for m in messages if any(t in m.lower() for t in
              ("referenceerror", "typeerror", "failed to compile", "shader compilation", "binding loop"))]
    assert not errors, errors
    adapter_logs = [m for m in messages if "adapter" in m.lower() or "device" in m.lower()]
    using_index = next((i for i, m in enumerate(messages) if "using this adapter" in m), -1)
    assert using_index > 0 and "Intel" in messages[using_index - 1], "No selected Intel hardware adapter evidence"
    assert not any("using d3d11 warp" in m.lower() for m in messages), "Software renderer is not acceptable"
    result = {"adapter_logs": adapter_logs, "captures": captures, "orbit_updates": performance,
              "3d_click_checks": click_checks,
              "elapsed_s": time.monotonic() - started,
              "qml_errors": errors, "camera_started": worker.isRunning()}
    (output / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "renderer.log").write_text("\n".join(messages), encoding="utf-8")
    print("VERIFIED", json.dumps(result, ensure_ascii=False), flush=True)
    window.close()
    app.processEvents()


if __name__ == "__main__":
    main()
