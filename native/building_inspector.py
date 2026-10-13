"""Lazy native building inspection state shared by the UI and one-hand gestures."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from PySide6.QtCore import QObject, Property, QUrl, Signal, Slot
from shapely.geometry import LineString, Point

if __package__:
    from .geometry_provider import geometry_from_buffers
    from .interior_mesh import build_interior, build_room_highlight
else:
    from geometry_provider import geometry_from_buffers
    from interior_mesh import build_interior, build_room_highlight


class BuildingInspector(QObject):
    changed = Signal()
    geometryChanged = Signal()
    viewRequested = Signal()
    MODES = ("dollhouse", "section", "xray", "explode", "floor", "inside")

    def __init__(self, buildings, repo_root):
        super().__init__()
        self._by_id = {building.id: building for building in buildings}
        self._native = Path(repo_root) / "native"
        path = self._native / "building_references.json"
        self._references = json.loads(path.read_text(encoding="utf-8")).get("buildings", {}) if path.exists() else {}
        self._selected = None
        self._profile = {}
        self._active = False
        self._mode = "dollhouse"
        self._floor = 0
        self._cut = 0.55
        self._axis = "y"
        self._spread = 8.0
        self._opacity = 0.16
        self._furniture = True
        self._layout = None
        self._floor_models = []
        self._shell = None
        self._facade = None
        self._room = ""
        self._selected_room = None
        self._room_geometry = None
        self._built_id = ""
        self._wing = ""

    def select(self, building_id):
        self._selected = self._by_id.get(building_id)
        if not self._selected:
            return
        self._profile = self._references.get(building_id, {})
        if not self._profile:
            self._profile = next((p for p in self._references.values()
                                  if self._selected.facility_id in p.get("facility_ids", [])), {})
        self._wing = next((f["wing"] for f in self._profile.get("floors", []) if f.get("wing")), "")
        if self._active:
            self.open()
        self.changed.emit()

    @Property(bool, notify=changed)
    def active(self):
        return self._active

    @Property(str, notify=geometryChanged)
    def inspection_key(self):
        return self._built_id

    @Property(str, notify=changed)
    def mode(self):
        return self._mode

    @Property(int, notify=changed)
    def selected_floor(self):
        return self._floor

    @Property(float, notify=changed)
    def cut(self):
        return self._cut

    @Property(str, notify=changed)
    def cut_axis(self):
        return self._axis

    @Property(float, notify=changed)
    def spread(self):
        return self._spread

    @Property(float, notify=changed)
    def shell_opacity(self):
        return self._opacity

    @Property(bool, notify=changed)
    def show_furniture(self):
        return self._furniture

    @Property(str, notify=changed)
    def room_name(self):
        return self._room

    @Property(QObject, notify=changed)
    def room_geometry(self):
        return self._room_geometry

    @Property(str, notify=changed)
    def name(self):
        return self._selected.name if self._selected else "选择一栋建筑"

    @Property(str, notify=changed)
    def evidence(self):
        if self._layout and self._layout.floors[self._floor]["reference"].get("basis") == "inferred":
            return "本层为设计示意 · 本建筑仅部分楼层有官方资料"
        if self._profile.get("floors"):
            return "楼层/空间名称参考官方资料 · 三维房间、家具及配准为示意"
        return "室内为设计示意 · 楼层数、房间、楼梯及家具未经核实"

    @Property("QVariantList", notify=changed)
    def wings(self):
        return list(dict.fromkeys(f["wing"] for f in self._profile.get("floors", []) if f.get("wing")))

    @Property(str, notify=changed)
    def wing(self):
        return self._wing

    @Property(str, notify=changed)
    def photo_url(self):
        photo = next((p for p in self._profile.get("photos", []) if p.get("asset")), {})
        path = self._native / photo.get("asset", "")
        return QUrl.fromLocalFile(str(path.resolve())).toString() if path.is_file() else ""

    @Property("QVariantList", notify=geometryChanged)
    def floors(self):
        return self._floor_models

    @Property(QObject, notify=geometryChanged)
    def shell(self):
        return self._shell

    @Property(QObject, notify=geometryChanged)
    def facade(self):
        return self._facade

    @Property("QVariantMap", notify=geometryChanged)
    def bounds(self):
        if not self._layout:
            return {"width": 100.0, "depth": 100.0, "height": 20.0, "scope": ""}
        a, b, c, d = self._layout.bounds
        return {"width": c - a, "depth": d - b, "height": self._layout.height, "scope": self._layout.scope}

    @Property("QVariantList", notify=changed)
    def rooms(self):
        if not self._layout:
            return []
        return [{key: room[key] for key in ("name", "kind", "source_named", "mapping")}
                for room in self._layout.floors[self._floor]["rooms"]]

    @Property("QVariantMap", notify=changed)
    def current_floor(self):
        if not self._layout:
            return {}
        floor = self._layout.floors[self._floor]
        return {"label": floor["label"], "name": floor["name"], "elevation": floor["elevation"],
                "startX": floor["start"][0], "startZ": floor["start"][1], "startYaw": floor["start_yaw"]}

    @Property(str, notify=changed)
    def plan_url(self):
        if not self._layout:
            return ""
        asset = self._layout.floors[self._floor]["reference"].get("plan_asset", "")
        path = self._native / asset
        return QUrl.fromLocalFile(str(path.resolve())).toString() if asset and path.is_file() else ""

    @Property(str, notify=changed)
    def plan_source(self):
        if not self._layout:
            return ""
        return self._layout.floors[self._floor]["reference"].get("source_url", "")

    @Property("QVariantList", notify=changed)
    def sources(self):
        return self._profile.get("sources", [])

    @Slot()
    def open(self):
        if self._selected is None:
            return
        build_key = self._selected.id + ":" + self._wing
        if self._built_id != build_key:
            profile = self._profile
            if self._wing:
                profile = {**profile, "floors": [f for f in profile.get("floors", []) if f.get("wing") == self._wing]}
            layout = build_interior(self._selected, profile)
            models = []
            for floor in layout.floors:
                model = {key: floor[key] for key in ("label", "name", "elevation", "height")}
                for key in ("slab", "walls", "furniture"):
                    model[key] = geometry_from_buffers(floor[key]) if floor[key] else None
                models.append(model)
            self._layout = layout
            self._floor_models = models
            self._shell = geometry_from_buffers(layout.shell) if layout.shell else None
            self._facade = self._make_facade(layout)
            self._built_id = build_key
            self._floor = next((i for i, f in enumerate(layout.floors) if f["label"] == "1"), 0)
            self._room = ""
            self._selected_room = None
            self._room_geometry = None
            self.geometryChanged.emit()
        self._active = True
        self._mode = "dollhouse"
        self.changed.emit()
        self.viewRequested.emit()

    @Slot(str)
    def set_wing(self, wing):
        if wing in self.wings and wing != self._wing:
            self._wing = wing
            self.open()

    def _make_facade(self, layout):
        if __package__:
            from .facade_mesh import build_facade_mesh
        else:
            from facade_mesh import build_facade_mesh
        points = [point for part in self._selected.parts for point in part["footprint"]]
        cx = (min(p[0] for p in points) + max(p[0] for p in points)) / 2
        cz = (min(p[1] for p in points) + max(p[1] for p in points)) / 2
        parts = [{**part, "footprint": [(x - cx, z - cz) for x, z in part["footprint"]],
                  "height_m": layout.height * part["height_m"] / max(1, self._selected.height_m)}
                 for part in self._selected.parts]
        mesh = build_facade_mesh([replace(self._selected, parts=parts, height_m=layout.height)])
        return geometry_from_buffers(mesh) if mesh and mesh.indices else None

    @Slot()
    def close(self):
        self._active = False
        self.changed.emit()
        self.viewRequested.emit()

    @Slot(str)
    def set_mode(self, mode):
        if mode in self.MODES and self._active:
            self._mode = mode
            self.changed.emit()
            self.viewRequested.emit()

    @Slot(int)
    def set_floor(self, index):
        if not self._layout:
            return
        index = max(0, min(len(self._layout.floors) - 1, index))
        if index == self._floor:
            return
        self._floor = index
        self._room = ""
        self._selected_room = None
        self._room_geometry = None
        self.changed.emit()
        if self._mode in ("floor", "inside"):
            self.viewRequested.emit()

    @Slot(int)
    def change_floor(self, delta):
        self.set_floor(self._floor + delta)

    @Slot(float)
    def set_cut(self, value):
        value = max(0.02, min(0.98, float(value)))
        if value != self._cut:
            self._cut = value
            self.changed.emit()

    @Slot(str)
    def set_cut_axis(self, axis):
        if axis in ("x", "y", "z"):
            self._axis = axis
            self.changed.emit()

    @Slot(float)
    def set_spread(self, value):
        value = max(0, min(24, float(value)))
        if value != self._spread:
            self._spread = value
            self.changed.emit()

    @Slot(float)
    def set_shell_opacity(self, value):
        value = max(0.03, min(0.5, float(value)))
        if value != self._opacity:
            self._opacity = value
            self.changed.emit()

    @Slot(bool)
    def set_furniture(self, visible):
        self._furniture = visible
        self.changed.emit()

    @Slot(float, float, float, result=str)
    def pick_room(self, x, y, z):
        if not self._layout:
            return ""
        index = self._floor if self._mode in ("floor", "inside") else max(
            0, min(len(self._layout.floors) - 1, int((y + 0.1) / (3.6 + (self._spread if self._mode == "explode" else 0)))))
        return self.select_room(index, x, z)

    @Slot(int, float, float, result=str)
    def select_room(self, index, x, z):
        if not self._layout or not 0 <= index < len(self._layout.floors):
            return ""
        floor = self._layout.floors[index]
        if not self._layout.footprint.covers(Point(x, z)):
            return ""
        room = next((room for room in floor["rooms"] if room["polygon"].covers(Point(x, z))), None)
        if self._floor == index and self._selected_room is room and self._room:
            return self._room
        self._floor = index
        self._selected_room = room
        self._room = room["name"] if room else "示意公共通道"
        self._room_geometry = geometry_from_buffers(build_room_highlight(room["polygon"])) if room else None
        self.changed.emit()
        return self._room

    @Slot(float, float, float, float, result=bool)
    def can_walk(self, x, z, next_x, next_z):
        if not self._layout:
            return False
        floor = self._layout.floors[self._floor]
        path = LineString(((x, z), (next_x, next_z))).buffer(0.2)
        return bool(floor["walkable"].covers(path) and not floor["collision"].intersects(path)
                    and (not self._furniture or not floor["furniture_collision"].intersects(path)))
