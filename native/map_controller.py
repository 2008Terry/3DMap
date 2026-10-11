"""Search, selection, and camera commands shared by QML and gestures."""

from __future__ import annotations

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
