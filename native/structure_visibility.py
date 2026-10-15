"""Read-only interior adapter for linked projections, cuts and structural paths."""
from __future__ import annotations

from heapq import heappop, heappush
from math import cos, hypot, radians, sin

import numpy as np

from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtGui import QVector3D
from shapely.geometry import LineString, Point
from shapely.prepared import prep

if __package__:
    from .geometry_provider import geometry_from_buffers
    from .interior_mesh import polygons, prism, build_room_highlight
    from .mesh_builder import _MeshBuilder
else:
    from geometry_provider import geometry_from_buffers
    from interior_mesh import polygons, prism, build_room_highlight
    from mesh_builder import _MeshBuilder


def _regions(geometry):
    return [{"outer": [list(p) for p in part.exterior.coords],
             "holes": [[list(p) for p in ring.coords] for ring in part.interiors]}
            for part in polygons(geometry)]


def _circulation(floor):
    free = floor["walkable"].difference(floor["collision"].buffer(0.23))
    halls = polygons(free.intersection(floor["corridor"]))
    if not halls:
        return free, None, None
    core = max(halls, key=lambda p: p.area).representative_point()
    component = next((p for p in polygons(free) if p.covers(core)), None)
    return free, component, core


def build_floor_graph(floor, index):
    _, component, core = _circulation(floor)
    rooms = []
    for number, room in enumerate(floor["rooms"]):
        parts = polygons(room["polygon"])
        for part_index, part in enumerate(parts):
            point = part.representative_point()
            reachable = part.intersection(component) if component is not None else None
            rooms.append({"id": f"{index}:{number}:{part_index}", "index": len(rooms), "floor": index,
                          "room_index": number, "part_index": part_index,
                          "name": room["name"] + (f" · 区域 {part_index + 1}" if len(parts) > 1 else ""),
                          "kind": room.get("kind", "room"),
                          "x": point.x, "z": point.y, "bounds": list(part.bounds),
                          "regions": _regions(part), "mapping": room.get("mapping", "schematic"),
                          "connected": reachable is not None and reachable.area > 0.1})
    return {"rooms": rooms, "core": {"x": core.x, "z": core.y} if core else {},
            "walls": _regions(floor["collision"]), "corridor": _regions(floor["corridor"])}


def room_route(floor, room):
    """Shortest visibility-graph path in the actual wall-clearance polygon."""
    _, component, core = _circulation(floor)
    if component is None:
        return []
    target = room["polygon"].intersection(component)
    if target.area <= 0.1:
        return []
    end = target.representative_point()
    start, goal = (core.x, core.y), (end.x, end.y)
    allowed = prep(component.buffer(1e-7))
    if allowed.covers(LineString((start, goal))):
        return [start, goal]
    vertices = [start, goal]
    for ring in [component.exterior, *component.interiors]:
        vertices.extend(list(ring.coords)[:-1])
    vertices = list(dict.fromkeys(vertices))
    distances, parents = {0: 0.0}, {}
    queue = [(hypot(start[0] - goal[0], start[1] - goal[1]), 0)]
    visited = set()
    while queue:
        _, current = heappop(queue)
        if current in visited:
            continue
        if current == 1:
            path = [goal]
            while current:
                current = parents[current]
                path.append(vertices[current])
            return list(reversed(path))
        visited.add(current)
        a = vertices[current]
        for nxt, b in enumerate(vertices):
            if nxt in visited or nxt == current:
                continue
            candidate = distances[current] + hypot(a[0] - b[0], a[1] - b[1])
            if candidate >= distances.get(nxt, float("inf")):
                continue
            if not allowed.covers(LineString((a, b))):
                continue
            distances[nxt], parents[nxt] = candidate, current
            heappush(queue, (candidate + hypot(b[0] - goal[0], b[1] - goal[1]), nxt))
    return []


def nearest_visible_hit(meshes, origin, direction, lens, cut_enabled, yaw):
    """Intersect actual triangles; Qt custom-geometry pickAll only tests bounds."""
    origin, direction = np.asarray(origin), np.asarray(direction)
    result, closest = {}, float("inf")
    for surface, triangles in meshes.items():
        edge1, edge2 = triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]
        p = np.cross(direction, edge2)
        determinant = np.einsum("ij,ij->i", edge1, p)
        valid = np.abs(determinant) > 1e-9
        inverse = np.zeros_like(determinant)
        inverse[valid] = 1 / determinant[valid]
        distance = origin - triangles[:, 0]
        u = np.einsum("ij,ij->i", distance, p) * inverse
        q = np.cross(distance, edge1)
        v = np.einsum("j,ij->i", direction, q) * inverse
        t = np.einsum("ij,ij->i", edge2, q) * inverse
        valid &= (u >= -1e-7) & (v >= -1e-7) & (u + v <= 1 + 1e-7) & (t > 1e-7) & (t < closest)
        for candidate in np.flatnonzero(valid)[np.argsort(t[valid])]:
            point = origin + direction * t[candidate]
            dx, dz = point[0] - lens["x"], point[2] - lens["z"]
            if surface == "walls" and cut_enabled and point[1] > 0.72 and hypot(dx, dz) < lens["radius"] and (
                    dx * sin(radians(yaw)) + dz * cos(radians(yaw)) > -lens["radius"] * 0.25):
                continue
            closest = float(t[candidate])
            result = {"x": float(point[0]), "y": float(point[1]), "z": float(point[2]),
                      "distance": closest, "surface": surface}
            break
    return result


class StructureVisibility(QObject):
    changed = Signal()
    activeChanged = Signal()

    def __init__(self, inspector):
        super().__init__()
        self.inspector = inspector
        self._active = False
        self._unfold = 0.65
        self._cut = True
        self._furniture = False
        self._graphs = []
        self._floors = []
        self._pick_meshes = []
        self._space = -1
        self._selection_key = None
        self._route = []
        self._route_geometry = None
        self._highlight = None
        inspector.geometryChanged.connect(self._rebuild)
        inspector.changed.connect(self._sync)
        self._rebuild()

    def _rebuild(self):
        layout = self.inspector._layout
        self._graphs = [build_floor_graph(f, i) for i, f in enumerate(layout.floors)] if layout else []
        self._pick_meshes = []
        for floor in layout.floors if layout else []:
            meshes = {}
            for surface in ("slab", "zones", "walls"):
                mesh = floor[surface]
                if mesh:
                    vertices = np.asarray(mesh.positions, dtype=float).reshape(-1, 3)
                    meshes[surface] = vertices[np.asarray(mesh.indices).reshape(-1, 3)]
            self._pick_meshes.append(meshes)
        self._floors = [{**model, "index": i, "core": self._graphs[i]["core"]}
                        for i, model in enumerate(self.inspector.floors)]
        self._clear_space()
        self._selection_key = None
        self.changed.emit()

    def _clear_space(self):
        self._space = -1
        self._route = []
        self._route_geometry = None
        self._highlight = None

    def _sync(self):
        key = (self.inspector.inspection_key, self.inspector.selected_floor)
        if key != self._selection_key:
            self._clear_space()
            self._selection_key = key
        if self._active and not self.inspector.active:
            self._active = False
            self.activeChanged.emit()
        self.changed.emit()

    @Property(bool, notify=activeChanged)
    def active(self):
        return self._active

    @Property("QVariantList", notify=changed)
    def floors(self):
        return self._floors

    @Property(int, notify=changed)
    def floor_index(self):
        return self.inspector.selected_floor

    @Property("QVariantList", notify=changed)
    def spaces(self):
        return self._graphs[self.floor_index]["rooms"] if self._graphs else []

    @Property("QVariantMap", notify=changed)
    def selected_space(self):
        return self.spaces[self._space] if 0 <= self._space < len(self.spaces) else {}

    @Property("QVariantMap", notify=changed)
    def plan(self):
        if not self._graphs:
            return {}
        return {**self._graphs[self.floor_index], "footprint": _regions(self.inspector._layout.footprint),
                "bounds": list(self.inspector._layout.bounds), "route": self._route}

    @Property("QVariantMap", notify=changed)
    def lens(self):
        space = self.selected_space
        if space:
            a, b, c, d = space["bounds"]
            return {"x": (a + c) / 2, "z": (b + d) / 2, "radius": hypot(c - a, d - b) / 2 + 2}
        core = self._graphs[self.floor_index]["core"] if self._graphs else {}
        return {"x": core.get("x", 0), "z": core.get("z", 0),
                "radius": self.context_radius}

    @Property(float, notify=changed)
    def context_radius(self):
        return max(self.inspector.bounds["width"], self.inspector.bounds["depth"]) * 0.65

    @Property(float, notify=changed)
    def unfold(self):
        return self._unfold

    @Property(bool, notify=changed)
    def cut_enabled(self):
        return self._cut

    @Property(bool, notify=changed)
    def furniture(self):
        return self._furniture

    @Slot(int, result="QVariantMap")
    def floor_position(self, index):
        if not 0 <= index < len(self._floors):
            return {"x": 0.0, "y": 0.0, "z": 0.0}
        span = max(self.inspector.bounds["width"], self.inspector.bounds["depth"])
        return {"x": self.inspector.bounds["width"] * 0.8 * self._unfold if index == self.floor_index else 0.0,
                "y": self._floors[index]["elevation"] + index * span * 0.32 * self._unfold, "z": 0.0}

    @Property("QVariantMap", notify=changed)
    def bounds(self):
        if not self._floors:
            return {"width": 100.0, "height": 20.0, "depth": 100.0, "centerX": 0.0, "centerY": 10.0}
        width, depth = self.inspector.bounds["width"], self.inspector.bounds["depth"]
        positions = [self.floor_position(i) for i in range(len(self._floors))]
        low_x, high_x = min(p["x"] for p in positions) - width / 2, max(p["x"] for p in positions) + width / 2
        high_y = max(p["y"] + f["height"] for p, f in zip(positions, self._floors))
        return {"minX": low_x, "maxX": high_x, "maxY": high_y, "width": high_x - low_x,
                "height": high_y + 0.12, "depth": depth, "centerX": (low_x + high_x) / 2,
                "centerY": (high_y - 0.12) / 2}

    @Property("QVariantList", notify=changed)
    def links(self):
        links = []
        for i in range(len(self._floors) - 1):
            a, b = self._graphs[i]["core"], self._graphs[i + 1]["core"]
            if not a or not b:
                continue
            pa, pb = self.floor_position(i), self.floor_position(i + 1)
            links.append({"fromFloor": i, "toFloor": i + 1,
                          "a": [pa["x"] + a["x"], pa["y"] + 0.4, a["z"]],
                          "b": [pb["x"] + b["x"], pb["y"] + 0.4, b["z"]]})
        return links

    @Property("QVariantList", notify=changed)
    def portals(self):
        if not self._floors:
            return []
        i = self.floor_index
        other = i + 1 if i + 1 < len(self._floors) else i - 1
        result = [{"floor": i, "yaw": -45.0, "title": "当前层 · 反向视线"}]
        if other >= 0:
            result.append({"floor": other, "yaw": 45.0, "title": "相邻层 · 连接去向"})
        return result

    @Property("QVariantList", notify=changed)
    def route_points(self):
        return self._route

    @Property(QObject, notify=changed)
    def route_geometry(self):
        return self._route_geometry

    @Property(QObject, notify=changed)
    def highlight(self):
        return self._highlight

    @Slot()
    def open(self):
        if not self.inspector.active:
            self.inspector.open()
        if self.inspector.active:
            self._active = True
            self._sync()
            self.activeChanged.emit()

    @Slot()
    def close(self):
        self._active = False
        self.activeChanged.emit()

    @Slot(int)
    def select_floor(self, index):
        if 0 <= index < len(self._floors):
            self.inspector.set_floor(index)

    @Slot(int)
    def select_space(self, index):
        if not 0 <= index < len(self.spaces):
            return
        floor = self.inspector._layout.floors[self.floor_index]
        space = self.spaces[index]
        source_room = floor["rooms"][space["room_index"]]
        room = {**source_room, "polygon": polygons(source_room["polygon"])[space["part_index"]]}
        self._space = index
        self._route = room_route(floor, room)
        self._highlight = geometry_from_buffers(build_room_highlight(room["polygon"]))
        self._route_geometry = None
        if len(self._route) > 1:
            builder = _MeshBuilder()
            prism(builder, LineString(self._route).buffer(0.16, cap_style=2), 0.18, 0.045, (0.95, 0.50, 0.12, 1))
            self._route_geometry = geometry_from_buffers(builder.finish())
        self.changed.emit()

    @Slot(float, float, result=bool)
    def pick_plan(self, x, z):
        if not self._graphs or not self.inspector._layout.footprint.covers(Point(x, z)):
            return False
        floor = self.inspector._layout.floors[self.floor_index]
        for space in self.spaces:
            room = floor["rooms"][space["room_index"]]
            if polygons(room["polygon"])[space["part_index"]].covers(Point(x, z)):
                self.select_space(space["index"])
                return True
        self._clear_space()
        self.changed.emit()
        return True

    @Slot(QVector3D, QVector3D, bool, int, float, result="QVariantMap")
    def ray_hit(self, origin, direction, overview, floor_index, yaw):
        closest, result = float("inf"), {}
        for i, meshes in enumerate(self._pick_meshes):
            if not overview and i != floor_index:
                continue
            offset = self.floor_position(i) if overview else {"x": 0, "y": 0, "z": 0}
            core = self._graphs[i]["core"]
            lens = self.lens if i == self.floor_index else {
                "x": core.get("x", 0), "z": core.get("z", 0), "radius": self.context_radius}
            hit = nearest_visible_hit(meshes, (origin.x() - offset["x"], origin.y() - offset["y"], origin.z()),
                                      (direction.x(), direction.y(), direction.z()), lens, self._cut, yaw)
            if hit and hit["distance"] < closest:
                closest, result = hit["distance"], {**hit, "floor": i}
        return result

    @Slot(float)
    def set_unfold(self, amount):
        self._unfold = max(0.0, min(1.0, float(amount)))
        self.changed.emit()

    @Slot(bool)
    def set_cut(self, enabled):
        self._cut = enabled
        self.changed.emit()

    @Slot(bool)
    def set_furniture(self, enabled):
        self._furniture = enabled
        self.changed.emit()
