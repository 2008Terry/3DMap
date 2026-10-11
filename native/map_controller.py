"""Search, selection, and camera commands shared by QML and gestures."""

from __future__ import annotations

import time
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

    def __init__(self, buildings: list[Building], extent: CampusExtent):
        super().__init__()
        self._buildings = buildings
        self._by_id = {building.id: building for building in buildings}
        self._extent = extent
        self._selected_id = ""
        self._gesture_status = "Gesture camera inactive"
        self._previous_palm: tuple[float, float] | None = None
        self._last_gesture_key = ""
        self._last_discrete_action_at = 0.0

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
        self.selectionChanged.emit(building.id)
        return building.to_qml()

    @Slot(float, float, float, result=str)
    def select_at(self, x: float, y: float, z: float) -> str:
        building = pick_building((x, y, z))
        if building is None:
            return ""
        self.select_building(building.id)
        return building.id

    @Slot()
    def reset_camera(self) -> None:
        self.resetCameraRequested.emit()

    @Slot(float, float)
    def pan_by(self, delta_x: float, delta_y: float) -> None:
        self.panRequested.emit(delta_x, delta_y)

    @Slot(float)
    def zoom_by(self, factor: float) -> None:
        self.zoomRequested.emit(factor)

    @Slot(str, float, "QVariant")
    def handle_gesture(self, key: str, confidence: float, landmarks: Any) -> None:
        if confidence < 0.68 or not key:
            self._previous_palm = None
            self._last_gesture_key = ""
            self.set_gesture_status("Waiting for a hand gesture")
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
                scale = max(self._extent.width, self._extent.depth) * 1.2
                self.pan_by(-delta_x * scale, delta_y * scale)
            self._previous_palm = position
            self._last_gesture_key = key
            self.set_gesture_status("Open Palm · move the map")
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
            self.zoom_by(0.82 if key == "Thumb_Up" else 1.22)
            self.set_gesture_status("Thumb Up · zoom in" if key == "Thumb_Up" else "Thumb Down · zoom out")
        elif key == "Victory":
            self.reset_camera()
            self.set_gesture_status("Victory · view reset")
        else:
            self.set_gesture_status("Recognized: " + key)
