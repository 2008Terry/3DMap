"""Create indexed, batched campus meshes from local footprint rings."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin
from typing import Sequence

from shapely import constrained_delaunay_triangles
from shapely.geometry import Polygon

if __package__:
    from .campus_data import Building
else:
    from campus_data import Building


@dataclass(frozen=True)
class MeshBuffers:
    positions: tuple[float, ...]
    normals: tuple[float, ...]
    colors: tuple[float, ...]
    indices: tuple[int, ...]
    bounds_min: tuple[float, float, float]
    bounds_max: tuple[float, float, float]


class _MeshBuilder:
    def __init__(self):
        self.positions: list[float] = []
        self.normals: list[float] = []
        self.colors: list[float] = []
        self.indices: list[int] = []
        self._vertex_indices: dict[tuple, int] = {}

    def triangle(self, points, normal, color):
        triangle_indices = []
        for point in points:
            key = (tuple(point), tuple(normal), tuple(color))
            index = self._vertex_indices.get(key)
            if index is None:
                index = len(self.positions) // 3
                self._vertex_indices[key] = index
                self.positions.extend(point)
                self.normals.extend(normal)
                self.colors.extend(color)
            triangle_indices.append(index)
        self.indices.extend(triangle_indices)

    def finish(self) -> MeshBuffers:
        vertices = [self.positions[offset:offset + 3] for offset in range(0, len(self.positions), 3)]
        return MeshBuffers(
            positions=tuple(self.positions),
            normals=tuple(self.normals),
            colors=tuple(self.colors),
            indices=tuple(self.indices),
            bounds_min=tuple(min(point[axis] for point in vertices) for axis in range(3)),
            bounds_max=tuple(max(point[axis] for point in vertices) for axis in range(3)),
        )


def _rgba(hex_color: str) -> tuple[float, float, float, float]:
    color = hex_color.lstrip("#")
    return tuple(int(color[offset:offset + 2], 16) / 255 for offset in (0, 2, 4)) + (1.0,)


def _add_polygon(builder: _MeshBuilder, ring, height: float, color):
    polygon = Polygon(ring)
    if polygon.is_empty or not polygon.is_valid or polygon.area <= 0:
        return
    center = polygon.centroid

    for triangle in constrained_delaunay_triangles(polygon).geoms:
        points = list(triangle.exterior.coords)[:3]
        top = [(x, height, z) for x, z in points]
        builder.triangle((top[0], top[2], top[1]), (0.0, 1.0, 0.0), color)
        bottom = [(x, 0.0, z) for x, z in points]
        builder.triangle((bottom[0], bottom[1], bottom[2]), (0.0, -1.0, 0.0), color)

    coordinates = list(polygon.exterior.coords)
    for start, end in zip(coordinates, coordinates[1:]):
        dx = end[0] - start[0]
        dz = end[1] - start[1]
        length = (dx * dx + dz * dz) ** 0.5
        if length == 0:
            continue
        nx, nz = dz / length, -dx / length
        midpoint_x = (start[0] + end[0]) / 2
        midpoint_z = (start[1] + end[1]) / 2
        if nx * (midpoint_x - center.x) + nz * (midpoint_z - center.y) < 0:
            nx, nz = -nx, -nz
        normal = (nx, 0.0, nz)
        a = (start[0], 0.0, start[1])
        b = (end[0], 0.0, end[1])
        c = (end[0], height, end[1])
        d = (start[0], height, start[1])
        builder.triangle((a, b, c), normal, color)
        builder.triangle((a, c, d), normal, color)


def _add_column(builder: _MeshBuilder, x: float, z: float, radius: float, height: float, color, segments: int = 12):
    dark_color = tuple(component * 0.88 if index < 3 else component for index, component in enumerate(color))
    for segment in range(segments):
        a = 2 * pi * segment / segments
        b = 2 * pi * (segment + 1) / segments
        p0 = (x + radius * cos(a), 0.0, z + radius * sin(a))
        p1 = (x + radius * cos(b), 0.0, z + radius * sin(b))
        p2 = (p1[0], height, p1[2])
        p3 = (p0[0], height, p0[2])
        normal = (cos((a + b) / 2), 0.0, sin((a + b) / 2))
        builder.triangle((p0, p1, p2), normal, dark_color)
        builder.triangle((p0, p2, p3), normal, dark_color)
        builder.triangle(((x, 0.0, z), p1, p0), (0.0, -1.0, 0.0), dark_color)
        builder.triangle(((x, height, z), p3, p2), (0.0, 1.0, 0.0), color)


def _add_facade_details(builder: _MeshBuilder, building: Building, color):
    details = building.facade_details
    if not details or not building.parts:
        return
    target_id = details.get("targetFacilityId")
    part = next((item for item in building.parts if item.get("facility_id") == target_id), building.parts[0])
    ring = part["footprint"]
    xs = [point[0] for point in ring]
    zs = [point[1] for point in ring]
    min_x, max_x = min(xs), max(xs)
    min_z, max_z = min(zs), max(zs)
    height = part["height_m"]
    side = details.get("side")

    columns = int(details.get("columns", 0))
    if columns > 0:
        radius = max(0.28, min(max_x - min_x, max_z - min_z) * 0.025)
        inset = radius * 1.8
        for index in range(columns):
            fraction = (index + 0.5) / columns
            if side in ("east", "west"):
                x = max_x - inset if side == "east" else min_x + inset
                z = min_z + fraction * (max_z - min_z)
            else:
                x = min_x + fraction * (max_x - min_x)
                z = max_z - inset if side == "south" else min_z + inset
            _add_column(builder, x, z, radius, height * 0.78, color)

    if details.get("windowBays", 0) and side in ("east", "west"):
        window_color = (0.13, 0.20, 0.24, 1.0)
        bays = int(details["windowBays"])
        x = max_x - 0.06 if side == "east" else min_x + 0.06
        for index in range(bays):
            center = min_z + (index + 0.5) * (max_z - min_z) / bays
            half_width = (max_z - min_z) / bays * 0.25
            low, high = height * 0.3, height * 0.65
            a, b = (x, low, center - half_width), (x, low, center + half_width)
            c, d = (x, high, center + half_width), (x, high, center - half_width)
            normal = (1.0 if side == "east" else -1.0, 0.0, 0.0)
            builder.triangle((a, b, c), normal, window_color)
            builder.triangle((a, c, d), normal, window_color)

    stringcourses = details.get("stringcourses", [])
    band_color = tuple(component * 1.08 if index < 3 else component for index, component in enumerate(color))
    for fraction in stringcourses:
        y = height * float(fraction)
        band_height = max(0.12, height * 0.008)
        for start, end in zip(ring, ring[1:]):
            polygon = Polygon(ring)
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            dx, dz = end[0] - start[0], end[1] - start[1]
            length = (dx * dx + dz * dz) ** 0.5 or 1.0
            nx, nz = dz / length, -dx / length
            if nx * (midpoint[0] - polygon.centroid.x) + nz * (midpoint[1] - polygon.centroid.y) < 0:
                nx, nz = -nx, -nz
            a = (start[0], y, start[1])
            b = (end[0], y, end[1])
            c = (end[0], y + band_height, end[1])
            d = (start[0], y + band_height, start[1])
            builder.triangle((a, b, c), (nx, 0.0, nz), band_color)
            builder.triangle((a, c, d), (nx, 0.0, nz), band_color)


def _build_mesh(buildings: Sequence[Building], featured_details: bool) -> MeshBuffers:
    builder = _MeshBuilder()
    for building in buildings:
        color = _rgba(building.color)
        for part in building.parts:
            _add_polygon(builder, part["footprint"], float(part["height_m"]), color)
        if featured_details:
            _add_facade_details(builder, building, color)
    return builder.finish()


def build_campus_mesh(buildings: Sequence[Building]) -> MeshBuffers:
    return _build_mesh(buildings, featured_details=False)


def build_featured_mesh(building: Building) -> MeshBuffers:
    return _build_mesh([building], featured_details=True)


def build_selection_mesh(building: Building) -> MeshBuffers:
    builder = _MeshBuilder()
    highlight = (0.14, 0.58, 0.95, 0.82)
    for part in building.parts:
        polygon = Polygon(part["footprint"])
        top_y = float(part["height_m"]) + 0.16
        bottom_y = float(part["height_m"]) + 0.08
        if polygon.is_empty or not polygon.is_valid or polygon.area <= 0:
            continue
        for triangle in constrained_delaunay_triangles(polygon).geoms:
            points = list(triangle.exterior.coords)[:3]
            top = [(x, top_y, z) for x, z in points]
            bottom = [(x, bottom_y, z) for x, z in points]
            builder.triangle((top[0], top[2], top[1]), (0.0, 1.0, 0.0), highlight)
            builder.triangle((bottom[0], bottom[1], bottom[2]), (0.0, -1.0, 0.0), highlight)
        coordinates = list(polygon.exterior.coords)
        for start, end in zip(coordinates, coordinates[1:]):
            dx, dz = end[0] - start[0], end[1] - start[1]
            length = (dx * dx + dz * dz) ** 0.5 or 1.0
            nx, nz = dz / length, -dx / length
            midpoint = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            if nx * (midpoint[0] - polygon.centroid.x) + nz * (midpoint[1] - polygon.centroid.y) < 0:
                nx, nz = -nx, -nz
            a = (start[0], bottom_y, start[1])
            b = (end[0], bottom_y, end[1])
            c = (end[0], top_y, end[1])
            d = (start[0], top_y, start[1])
            builder.triangle((a, b, c), (nx, 0.0, nz), highlight)
            builder.triangle((a, c, d), (nx, 0.0, nz), highlight)
    return builder.finish()
