"""Search, selection, and camera commands shared by QML and gestures."""

from __future__ import annotations

import time
from math import hypot
from typing import Any

from PySide6.QtCore import QObject, Property, Signal, Slot

if __package__:
    from .campus_data import Building, CampusExtent, pick_building
else:
    from campus_data import Building, CampusExtent, pick_building


class MapController(QObject):
    resetCameraRequested = Signal()
    panRequested = Signal(float, float)
    zoomRequested = Signal(float)
    selectionChanged = Signal(str)
    gestureStatusChanged = Signal(str)
    detailsChanged = Signal()
    focusRequested = Signal(float, float, float)
    pointingChanged = Signal(float, float, bool)
    lookRequested = Signal(float, float)
    walkRequested = Signal(float)

    def __init__(self, buildings: list[Building], extent: CampusExtent, inspector=None, environment=None):
        super().__init__()
        self._buildings = buildings
        self._by_id = {building.id: building for building in buildings}
        self._extent = extent
        self._selected_id = ""
        self._gesture_status = "Gesture camera inactive"
        self._previous_palm: tuple[float, float] | None = None
        self._last_gesture_key = ""
        self._last_discrete_action_at = 0.0
        self._inspector = inspector
        self._bus_stops = (environment or {}).get("busStops", [])

    @Property("QVariantMap", notify=detailsChanged)
    def selected_details(self):
        building = self._by_id.get(self._selected_id)
        if not building:
            return {}
        record = building.to_qml()
        points = [p for part in building.parts for p in part["footprint"]]
        cx = (min(p[0] for p in points) + max(p[0] for p in points)) / 2
        cz = (min(p[1] for p in points) + max(p[1] for p in points)) / 2
        stops = sorted(self._bus_stops, key=lambda s: hypot(s["position"][0] - cx, s["position"][1] - cz))
        record["nearbyStops"] = [
            {**stop, "distance": round(hypot(stop["position"][0] - cx, stop["position"][1] - cz))}
            for stop in stops[:3] if hypot(stop["position"][0] - cx, stop["position"][1] - cz) < 250
        ]
        return record

    @Property(str, notify=gestureStatusChanged)
    def gesture_status(self) -> str:
        return self._gesture_status

    def set_gesture_status(self, status: str) -> None:
        if status != self._gesture_status:
            self._gesture_status = status
            self.gestureStatusChanged.emit(status)

    @Slot(str, result="QVariantList")
    def search(self, query: str) -> list[dict[str, str]]:
        needle = query.strip().casefold()
        if not needle:
            return []
        results = []
        for building in self._buildings:
            fields = (building.name, building.facility_id, building.id, building.campus)
            if any(needle in value.casefold() for value in fields if value):
                results.append({
                    "id": building.id,
                    "facility_id": building.facility_id,
                    "name": building.name,
                    "campus": building.campus,
                })
        return results[:60]

    @Slot(str, result="QVariant")
    def select_building(self, building_id: str) -> dict[str, Any]:
        building = self._by_id.get(building_id)
        if building is None:
            return {}
        self._selected_id = building.id
        if self._inspector:
            self._inspector.select(building.id)
        self.selectionChanged.emit(building.id)
        self.detailsChanged.emit()
        return building.to_qml()

    @Slot(str)
    def focus_building(self, building_id):
        if self._inspector and self._inspector.active:
            self._inspector.close()
        if not self.select_building(building_id):
            return
        building = self._by_id[building_id]
        points = [point for part in building.parts for point in part["footprint"]]
        xs, zs = [p[0] for p in points], [p[1] for p in points]
        self.focusRequested.emit((min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2,
                                 max(100, max(xs) - min(xs), max(zs) - min(zs)) * 2.1)

    @Slot(str)
    def focus_campus(self, campus):
        if self._inspector and self._inspector.active:
            self._inspector.close()
        subset = [b for b in self._buildings if campus in b.campus]
        if not subset:
            self.reset_camera()
            return
        points = [p for b in subset for part in b.parts for p in part["footprint"]]
        xs, zs = [p[0] for p in points], [p[1] for p in points]
        self.focusRequested.emit((min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2,
                                 max(max(xs) - min(xs), max(zs) - min(zs)) * 0.9)

    @Slot(float, float, float, result=str)
    def select_at(self, x: float, y: float, z: float) -> str:
        building = pick_building((x, y, z))
        if building is None:
            return ""
        self.select_building(building.id)
        return building.id

    @Slot()
    def reset_camera(self) -> None:
        if self._inspector and self._inspector.active:
            self._inspector.viewRequested.emit()
        else:
            self.resetCameraRequested.emit()

    @Slot(float, float)
    def pan_by(self, delta_x: float, delta_y: float) -> None:
        self.panRequested.emit(delta_x, delta_y)

    @Slot(float)
    def zoom_by(self, factor: float) -> None:
        self.zoomRequested.emit(factor)

    @Slot(str, float, "QVariant")
    def handle_gesture(self, key: str, confidence: float, landmarks: Any) -> None:
        inspector = self._inspector
        inspecting = bool(inspector and inspector.active)
        inside = inspecting and inspector.mode == "inside"
        if key != "Pointing_Up" or confidence < 0.68:
            self.pointingChanged.emit(0, 0, False)
        if confidence < 0.68 or not key:
            self._previous_palm = None
            self._last_gesture_key = ""
            self.set_gesture_status("Waiting for a hand gesture")
            return

        if key == "Pointing_Up" and len(landmarks) > 8:
            x, y = 1.0 - float(landmarks[8][0]), float(landmarks[8][1])
            self._previous_palm = None
            self._last_gesture_key = key
            if inspecting and inspector.mode == "section":
                inspector.set_cut(x)
                self.set_gesture_status("食指移动 · 扫描建筑切面")
            else:
                self.pointingChanged.emit(x, y, True)
                self.set_gesture_status("食指指向并停留 · 选择建筑或房间")
            return

        if key == "Open_Palm":
            if len(landmarks) <= 9:
                return
            x, y = landmarks[9]
            position = (1.0 - float(x), float(y))
            if self._previous_palm is not None:
                delta_x = position[0] - self._previous_palm[0]
                delta_y = position[1] - self._previous_palm[1]
                delta_x = 0.0 if abs(delta_x) < 0.003 else max(-0.06, min(0.06, delta_x))
                delta_y = 0.0 if abs(delta_y) < 0.003 else max(-0.06, min(0.06, delta_y))
                if inside:
                    self.lookRequested.emit(-delta_x * 150, -delta_y * 100)
                else:
                    scale = (max(inspector.bounds["width"], inspector.bounds["depth"]) * 1.6
                             if inspecting else max(self._extent.width, self._extent.depth) * 1.2)
                    self.pan_by(-delta_x * scale, delta_y * scale)
            self._previous_palm = position
            self._last_gesture_key = key
            self.set_gesture_status("张开手掌 · 环顾室内" if inside else "Open Palm · move the map")
            return

        self._previous_palm = None
        if self._last_gesture_key == key:
            return
        self._last_gesture_key = key
        if key in ("Thumb_Up", "Thumb_Down"):
            now = time.monotonic()
            if now - self._last_discrete_action_at < 0.7:
                return
            self._last_discrete_action_at = now
            if inside:
                self.walkRequested.emit(1.8 if key == "Thumb_Up" else -1.8)
                self.set_gesture_status("拇指 · 在室内前进/后退")
            elif inspecting:
                inspector.change_floor(1 if key == "Thumb_Up" else -1)
                inspector.set_mode("floor")
                self.set_gesture_status("拇指 · 切换楼层")
            else:
                self.zoom_by(0.82 if key == "Thumb_Up" else 1.22)
                self.set_gesture_status("Thumb Up · zoom in" if key == "Thumb_Up" else "Thumb Down · zoom out")
        elif key == "Closed_Fist" and inspector:
            if not self._selected_id:
                self.set_gesture_status("先用食指或鼠标选择建筑，再握拳进入")
            elif not inspecting:
                inspector.open()
                self.set_gesture_status("握拳 · 打开建筑结构")
            else:
                inspector.set_mode("dollhouse" if inside else "inside")
                self.set_gesture_status("握拳 · 切换室内视角")
        elif key == "Victory":
            if inspecting:
                inspector.close()
            self.reset_camera()
            self.set_gesture_status("Victory · view reset")
        else:
            self.set_gesture_status("Recognized: " + key)

    @Slot(str, str, float, object)
    def handle_recognition(self, key, label, confidence, landmarks):
        """Receive the worker's actual Qt signature on the controller's GUI thread."""
        self.handle_gesture(key, confidence, landmarks)
