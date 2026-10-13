"""Schematic interiors clipped to real footprints; official maps remain separate references."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, hypot

from shapely import constrained_delaunay_triangles
from shapely.affinity import translate
from shapely.geometry import LineString, Polygon, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

if __package__:
    from .mesh_builder import _MeshBuilder
else:
    from mesh_builder import _MeshBuilder


def polygons(geometry):
    if geometry.is_empty:
        return []
    if geometry.geom_type == "Polygon":
        return [geometry]
    return [part for part in getattr(geometry, "geoms", []) if part.geom_type == "Polygon"]


def prism(builder, geometry, base, height, color):
    """Extrude valid polygons including courtyard holes with outward wall normals."""
    for raw in polygons(geometry):
        polygon = orient(raw, sign=1.0)
        for triangle in constrained_delaunay_triangles(polygon).geoms:
            points = list(triangle.exterior.coords)[:3]
            top = [(x, base + height, z) for x, z in points]
            bottom = [(x, base, z) for x, z in points]
            builder.triangle((top[0], top[2], top[1]), (0, 1, 0), color)
            builder.triangle(bottom, (0, -1, 0), color)
        for ring in [polygon.exterior, *polygon.interiors]:
            for (x0, z0), (x1, z1) in zip(ring.coords, list(ring.coords)[1:]):
                length = hypot(x1 - x0, z1 - z0)
                if length < 1e-6:
                    continue
                normal = ((z1 - z0) / length, 0, -(x1 - x0) / length)
                a, b = (x0, base, z0), (x1, base, z1)
                c, d = (x1, base + height, z1), (x0, base + height, z0)
                builder.triangle((a, c, b), normal, color)
                builder.triangle((a, d, c), normal, color)


def _cube(builder, x, y, z, width, height, depth, color):
    left, right = x - width / 2, x + width / 2
    front, back = z - depth / 2, z + depth / 2
    top = y + height
    faces = [
        (((left, top, front), (left, top, back), (right, top, back), (right, top, front)), (0, 1, 0)),
        (((left, y, back), (left, y, front), (right, y, front), (right, y, back)), (0, -1, 0)),
        (((right, y, front), (right, top, front), (right, top, back), (right, y, back)), (1, 0, 0)),
        (((left, y, back), (left, top, back), (left, top, front), (left, y, front)), (-1, 0, 0)),
        (((left, y, front), (left, top, front), (right, top, front), (right, y, front)), (0, 0, -1)),
        (((right, y, back), (right, top, back), (left, top, back), (left, y, back)), (0, 0, 1)),
    ]
    for points, normal in faces:
        builder.triangle(points[:3], normal, color)
        builder.triangle((points[0], points[2], points[3]), normal, color)


def _finish(builder):
    return builder.finish() if builder.indices else None


@dataclass
class Interior:
    footprint: object
    floors: list[dict]
    shell: object
    bounds: tuple
    height: float
    scope: str


def floor_catalog(building, profile):
    floors = profile.get("floors", [])
    scope = ""
    wings = [floor.get("wing") for floor in floors if floor.get("wing")]
    if wings:
        # Do not stack two wings on top of each other as if they were consecutive levels.
        wing = wings[0]
        floors = [floor for floor in floors if floor.get("wing") == wing]
        scope = f"{wing} 楼翼目录 · 外轮廓配准为示意"
    if not floors:
        count = min(12, max(1, round(building.height_m / 3.6)))
        floors = [{"label": str(i + 1), "name": f"示意 {i + 1} 层", "spaces": []} for i in range(count)]
    return floors[:18], scope


def _room_zones(footprint, floor):
    min_x, min_z, max_x, max_z = footprint.bounds
    width, depth = max_x - min_x, max_z - min_z
    along_x = width >= depth
    half = min(2.0, min(width, depth) * 0.13)
    corridor_box = (box(min_x, -half, max_x, half) if along_x
                    else box(-half, min_z, half, max_z))
    corridor = footprint.intersection(corridor_box)
    source_spaces = [space for space in floor.get("spaces", []) if space.get("name")]
    mapped = [space for space in source_spaces if len(space.get("rect", [])) == 4]
    zones = []
    if mapped:
        for space in mapped:
            u0, v0, u1, v1 = space["rect"]
            area = box(min_x + u0 * width, min_z + v0 * depth,
                       min_x + u1 * width, min_z + v1 * depth).intersection(footprint)
            if area.area > 5:
                zones.append((area, space))
    else:
        length = width if along_x else depth
        count = max(1, min(6, ceil(length / 13)))
        for side in (-1, 1):
            for i in range(count):
                low = (min_x if along_x else min_z) + length * i / count
                high = (min_x if along_x else min_z) + length * (i + 1) / count
                if along_x:
                    cell = box(low, min_z if side < 0 else half, high, -half if side < 0 else max_z)
                else:
                    cell = box(min_x if side < 0 else half, low, -half if side < 0 else max_x, high)
                area = cell.intersection(footprint)
                if area.area > 10:
                    space = source_spaces[len(zones)] if len(zones) < len(source_spaces) else {
                        "name": f"示意空间 {len(zones) + 1}", "kind": "study"}
                    zones.append((area, space))
    if corridor.is_empty:
        point = footprint.representative_point()
        corridor = point.buffer(min(2, max(0.5, min(width, depth) / 5))).intersection(footprint)
    return zones, corridor


def _walls_and_door(builder, polygon, corridor, height):
    segments = []
    for region in polygons(polygon):
        coords = list(region.exterior.coords)
        edges = [LineString((a, b)) for a, b in zip(coords, coords[1:])]
        candidates = [edge for edge in edges if edge.length > 2]
        door_edge = min(candidates, key=lambda edge: edge.distance(corridor), default=None)
        for edge in edges:
            runs = [edge]
            if edge is door_edge:
                gap = min(1.5, edge.length * 0.4)
                a, b = edge.interpolate((edge.length - gap) / 2), edge.interpolate((edge.length + gap) / 2)
                runs = [LineString((edge.coords[0], a.coords[0])), LineString((b.coords[0], edge.coords[-1]))]
                for point in (a, b):
                    _cube(builder, point.x, 0.12, point.y, 0.18, 2.15, 0.18, (0.42, 0.30, 0.17, 1))
                lintel = LineString((a.coords[0], b.coords[0])).buffer(0.09, cap_style=2)
                prism(builder, lintel, 2.15, 0.12, (0.42, 0.30, 0.17, 1))
            for run in runs:
                solid = run.buffer(0.09, cap_style=2)
                segments.append(solid)
                prism(builder, solid, 0.12, height - 0.30, (0.86, 0.85, 0.79, 1))
    return segments


def _furnish(builder, area, kind):
    usable = area.buffer(-1.1)
    if usable.is_empty:
        return []
    min_x, min_z, max_x, max_z = usable.bounds
    book_area = any(word in kind.lower() for word in ("stack", "book", "collection", "书"))
    positions = []
    for u in (0.25, 0.65):
        for v in (0.3, 0.7):
            x, z = min_x + (max_x - min_x) * u, min_z + (max_z - min_z) * v
            if area.covers(box(x - 0.9, z - 1.2, x + 0.9, z + 1.2)):
                positions.append((x, z))
    for x, z in positions:
        if book_area:
            _cube(builder, x, 0.14, z, 1.7, 1.8, 0.45, (0.45, 0.33, 0.19, 1))
            for shelf in range(4):
                for i in range(6):
                    _cube(builder, x - 0.65 + i * 0.24, 0.26 + shelf * 0.4, z - 0.25,
                          0.17, 0.28, 0.09, ((0.19, 0.37, 0.46, 1) if i % 2 else (0.68, 0.37, 0.23, 1)))
        elif "cafe" in kind.lower():
            from shapely.geometry import Point
            prism(builder, Point(x, z).buffer(0.65, quad_segs=3), 0.8, 0.07, (0.73, 0.57, 0.34, 1))
            _cube(builder, x, 0.12, z, 0.14, 0.68, 0.14, (0.3, 0.33, 0.33, 1))
            for dz in (-0.85, 0.85):
                _cube(builder, x, 0.46, z + dz, 0.45, 0.08, 0.44, (0.22, 0.38, 0.39, 1))
        elif "lounge" in kind.lower():
            _cube(builder, x, 0.25, z, 1.6, 0.33, 0.65, (0.26, 0.38, 0.36, 1))
            _cube(builder, x, 0.4, z + 0.27, 1.6, 0.5, 0.14, (0.26, 0.38, 0.36, 1))
            _cube(builder, x, 0.45, z - 0.9, 0.95, 0.07, 0.5, (0.62, 0.42, 0.24, 1))
        else:
            _cube(builder, x, 0.86, z, 1.6, 0.09, 0.85, (0.68, 0.48, 0.27, 1))
            for dx in (-0.65, 0.65):
                for dz in (-0.3, 0.3):
                    _cube(builder, x + dx, 0.14, z + dz, 0.07, 0.72, 0.07, (0.24, 0.28, 0.29, 1))
            _cube(builder, x, 0.48, z + 0.72, 0.52, 0.09, 0.52, (0.18, 0.35, 0.39, 1))
            _cube(builder, x, 0.5, z + 0.95, 0.52, 0.47, 0.06, (0.18, 0.35, 0.39, 1))
            _cube(builder, x, 0.96, z, 0.48, 0.03, 0.32, (0.11, 0.17, 0.20, 1))
            if "lab" in kind.lower() or "comput" in kind.lower():
                _cube(builder, x, 1.04, z - 0.15, 0.06, 0.3, 0.07, (0.22, 0.25, 0.25, 1))
                _cube(builder, x, 1.15, z - 0.15, 0.57, 0.36, 0.05, (0.06, 0.12, 0.17, 1))
    return [box(x - 0.9, z - (0.3 if book_area else 1.2),
                x + 0.9, z + (0.3 if book_area else 1.2)) for x, z in positions]


def build_interior(building, profile=None):
    profile = profile or {}
    raw = unary_union([Polygon(part["footprint"]) for part in building.parts])
    min_x, min_z, max_x, max_z = raw.bounds
    footprint = translate(raw, -(min_x + max_x) / 2, -(min_z + max_z) / 2)
    catalogue, scope = floor_catalog(building, profile)
    floor_height = 3.6
    height = len(catalogue) * floor_height
    shell = _MeshBuilder()
    for part in polygons(footprint):
        prism(shell, part.boundary.buffer(0.16, join_style=2), 0, height, (0.72, 0.68, 0.59, 1))
    floors = []
    colors = [(0.85, 0.85, 0.78, 1), (0.77, 0.84, 0.79, 1), (0.84, 0.81, 0.72, 1)]
    for index, source_floor in enumerate(catalogue):
        slab, walls, furnishings = _MeshBuilder(), _MeshBuilder(), _MeshBuilder()
        prism(slab, footprint, -0.12, 0.22, colors[index % len(colors)])
        zones, corridor = _room_zones(footprint, source_floor)
        prism(slab, corridor, 0.105, 0.02, (0.72, 0.64, 0.47, 1))
        room_records, collision, furniture_collision = [], [], []
        for room_index, (area, space) in enumerate(zones):
            tint = ((0.78, 0.82, 0.79, 1), (0.83, 0.79, 0.69, 1), (0.79, 0.81, 0.83, 1))[room_index % 3]
            prism(slab, area, 0.10, 0.025, tint)
            collision.extend(_walls_and_door(walls, area, corridor, floor_height))
            furniture_collision.extend(_furnish(furnishings, area, space.get("kind", "") + " " + space["name"]))
            point = area.representative_point()
            room_records.append({"name": space["name"], "kind": space.get("kind", "study"),
                                 "x": point.x, "z": point.y, "polygon": area,
                                 "source_named": not space["name"].startswith("示意"),
                                 "mapping": "approximate source zone" if space.get("rect") else "schematic placement"})
        # Illustrative circulation core. Its location is never presented as an official stair/elevator.
        point = corridor.representative_point()
        for step in range(10):
            stair = box(point.x - 1, point.y - 1.5 + step * 0.3,
                        point.x + 1, point.y - 1.2 + step * 0.3)
            prism(furnishings, stair.intersection(footprint), 0.12, (step + 1) * 0.18, (0.48, 0.54, 0.53, 1))
            furniture_collision.append(stair.intersection(footprint))
        # Spawn away from the illustrative stair so the eye-level view opens into free space.
        all_collision = unary_union(collision + furniture_collision).buffer(0.3)
        spawn_area = corridor.difference(point.buffer(3)).difference(all_collision).intersection(footprint.buffer(-0.3))
        start = spawn_area.representative_point() if not spawn_area.is_empty else corridor.representative_point()
        width = footprint.bounds[2] - footprint.bounds[0]
        depth = footprint.bounds[3] - footprint.bounds[1]
        start_yaw = (90 if start.x > 0 else -90) if width >= depth else (0 if start.y > 0 else 180)
        floors.append({"label": str(source_floor.get("label", index + 1)),
                       "name": source_floor.get("name", f"Level {index + 1}"),
                       "elevation": index * floor_height, "height": floor_height,
                       "slab": _finish(slab), "walls": _finish(walls), "furniture": _finish(furnishings),
                       "rooms": room_records, "walkable": footprint.buffer(-0.25),
                       "collision": unary_union(collision), "furniture_collision": unary_union(furniture_collision),
                       "start": (start.x, start.y), "start_yaw": start_yaw,
                       "reference": source_floor})
    return Interior(footprint, floors, _finish(shell), footprint.bounds, height, scope)
