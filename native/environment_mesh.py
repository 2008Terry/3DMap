"""Bake sourced environment and clearly illustrative street life into four meshes."""
from __future__ import annotations

from math import cos, pi, sin, sqrt
from shapely.prepared import prep

from shapely import constrained_delaunay_triangles, make_valid
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

if __package__:
    from .mesh_builder import MeshBuffers, _MeshBuilder
else:
    from mesh_builder import MeshBuffers, _MeshBuilder


def _polygons(geometry):
    if geometry.is_empty:
        return
    if geometry.geom_type == "Polygon":
        yield geometry
    elif hasattr(geometry, "geoms"):
        for child in geometry.geoms:
            yield from _polygons(child)


def _surface(builder, geometry, y, color):
    for polygon in _polygons(geometry):
        for triangle in constrained_delaunay_triangles(polygon).geoms:
            points = list(triangle.exterior.coords)[:3]
            a, b, c = [(x, y, z) for x, z in points]
            # Qt uses counterclockwise front faces when viewed from above.
            cross = (b[2] - a[2]) * (c[0] - a[0]) - (b[0] - a[0]) * (c[2] - a[2])
            builder.triangle((a, b, c) if cross > 0 else (a, c, b), (0.0, 1.0, 0.0), color)


def _quad(builder, a, b, c, d, normal, color):
    builder.triangle((a, b, c), normal, color)
    builder.triangle((a, c, d), normal, color)


def _box(builder, x, y, z, width, height, depth, color):
    left, right = x - width / 2, x + width / 2
    front, back = z - depth / 2, z + depth / 2
    bottom, top = y, y + height
    _quad(builder, (left, top, front), (left, top, back), (right, top, back), (right, top, front), (0, 1, 0), color)
    _quad(builder, (right, bottom, front), (right, top, front), (right, top, back), (right, bottom, back), (1, 0, 0), color)
    _quad(builder, (left, bottom, back), (left, top, back), (left, top, front), (left, bottom, front), (-1, 0, 0), color)
    _quad(builder, (left, bottom, front), (left, top, front), (right, top, front), (right, bottom, front), (0, 0, -1), color)
    _quad(builder, (right, bottom, back), (right, top, back), (left, top, back), (left, bottom, back), (0, 0, 1), color)


def _crown(builder, x, y, z, radius, height, color, segments=6):
    # Two low polygon cones make a solid crown with silhouette from every angle.
    lower = (x, y - height * 0.32, z)
    upper = (x, y + height * 0.68, z)
    for index in range(segments):
        a, b = 2 * pi * index / segments, 2 * pi * (index + 1) / segments
        p = (x + radius * cos(a), y, z + radius * sin(a))
        q = (x + radius * cos(b), y, z + radius * sin(b))
        nx, nz = cos((a + b) / 2), sin((a + b) / 2)
        normal_length = sqrt(1.16)
        normal = (nx / normal_length, 0.4 / normal_length, nz / normal_length)
        shade = tuple(component * (0.89 + (index % 3) * 0.05) for component in color[:3]) + (1.0,)
        builder.triangle((p, upper, q), normal, shade)
        builder.triangle((p, q, lower), (normal[0], -normal[1], normal[2]), shade)


def _extrude(builder, polygon, height, color):
    _surface(builder, polygon, height, tuple(min(1, component * 1.06) for component in color[:3]) + (1.0,))
    for ring in [polygon.exterior, *polygon.interiors]:
        coordinates = list(ring.coords)
        for a, b in zip(coordinates, coordinates[1:]):
            dx, dz = b[0] - a[0], b[1] - a[1]
            length = sqrt(dx * dx + dz * dz)
            if length < 0.01:
                continue
            normal = (dz / length, 0, -dx / length)
            _quad(builder, (a[0], 0, a[1]), (b[0], 0, b[1]),
                  (b[0], height, b[1]), (a[0], height, a[1]), normal, color)


def illustrative_positions(data, buildings, limit=90):
    """Put synthetic people/benches on sourced paths, clear of buildings and roads."""
    blocked = [make_valid(Polygon(part["footprint"])) for building in buildings for part in building.parts]
    blocked.extend(make_valid(Polygon(record["rings"][0], record["rings"][1:])) for record in data["contextBuildings"])
    blocked.extend(LineString(road["points"]).buffer(road["widthMeters"] / 2 + 0.8, quad_segs=1) for road in data["roads"])
    exclusion = unary_union(blocked).buffer(0.4, quad_segs=1)
    positions = []
    occupied = set()
    for path in sorted(data["paths"], key=lambda record: (record["id"], record["points"][0])):
        if path.get("kind") in {"steps", "cycleway"}:
            continue
        line = LineString(path["points"])
        if line.length < 10:
            continue
        for fraction in (0.31, 0.73):
            point = line.interpolate(fraction, normalized=True)
            cell = (round(point.x / 14), round(point.y / 14))
            if cell in occupied or exclusion.covers(point):
                continue
            positions.append((point.x, point.y))
            occupied.add(cell)
            if len(positions) >= limit:
                return positions
    return positions


def illustrative_canopy(data, buildings):
    """Fill mapped grass with clearly inferred vegetation, not a tree inventory."""
    blocked = [Polygon(part["footprint"]) for b in buildings for part in b.parts]
    blocked.extend(Polygon(r["rings"][0], r["rings"][1:]) for r in data["contextBuildings"])
    blocked.extend(LineString(r["points"]).buffer(r["widthMeters"] / 2 + 1) for r in data["roads"] + data["paths"])
    blocked.extend(Point(*t["position"]).buffer(5) for t in data["trees"])
    exclusion = prep(unary_union(blocked))
    areas = [Polygon(r["rings"][0], r["rings"][1:]) for r in data["surfaces"]
             if r["source"] == "osm" and r["kind"] == "grass"]
    areas.sort(key=lambda p: min(p.centroid.distance(Point(0, 0)), p.centroid.distance(Point(1850, -1650))))
    counts = [0, 0]
    occupied = set()
    positions = []
    for area in areas:
        a, b, c, d = area.bounds
        for x in range(int(a) + 8, int(c), 23):
            for z in range(int(b) + 8, int(d), 23):
                district = 0 if z > -800 else 1
                point = Point(x, z)
                cell = (round(x / 18), round(z / 18))
                if counts[district] >= 80 or cell in occupied or not area.buffer(-2).covers(point) or exclusion.covers(point):
                    continue
                occupied.add(cell)
                counts[district] += 1
                positions.append((x, z))
    return positions


def build_environment_meshes(data: dict, buildings) -> dict[str, MeshBuffers]:
    surfaces, trees, street_props, context = [_MeshBuilder() for _ in range(4)]
    colors = {"parks": (0.38, 0.48, 0.29, 1), "woodlands": (0.24, 0.37, 0.24, 1),
              "wood": (0.25, 0.38, 0.26, 1), "forest": (0.25, 0.38, 0.26, 1),
              "grass": (0.44, 0.55, 0.31, 1), "recreation_ground": (0.42, 0.54, 0.31, 1),
              "water": (0.22, 0.40, 0.49, 1)}
    for record in data["surfaces"]:
        polygon = make_valid(Polygon(record["rings"][0], record["rings"][1:]))
        _surface(surfaces, polygon, 0.02 if record["source"] != "osm" else 0.035, colors.get(record["kind"], colors["grass"]))
    for road in data["roads"]:
        line = LineString(road["points"])
        width = road["widthMeters"]
        _surface(surfaces, line.buffer(width / 2 + 0.65, quad_segs=2), 0.05, (0.63, 0.63, 0.57, 1))
        _surface(surfaces, line.buffer(width / 2, quad_segs=2), 0.07, (0.24, 0.26, 0.27, 1))
        # Lane marks are illustrative styling of the measured centerline.
        if width >= 7.4:
            for distance in range(5, int(line.length) - 4, 14):
                a, b = line.interpolate(distance), line.interpolate(distance + 4)
                _surface(surfaces, LineString([a, b]).buffer(0.09, cap_style=2), 0.085, (0.82, 0.76, 0.46, 1))
    for path in data["paths"]:
        line = LineString(path["points"])
        _surface(surfaces, line.buffer(path["widthMeters"] / 2, quad_segs=2), 0.11, (0.71, 0.69, 0.60, 1))
    for record in data["contextBuildings"]:
        shade = 0.80 + (int(record["id"]) % 9) * 0.022
        color = (0.68 * shade, 0.64 * shade, 0.55 * shade, 1)
        geometry = make_valid(Polygon(record["rings"][0], record["rings"][1:]))
        for polygon in _polygons(geometry):
            _extrude(context, polygon, record["heightMeters"], color)
    for tree in data["trees"]:
        x, z = tree["position"]
        height = tree["displayHeightMeters"]
        radius = max(1.3, min(4.8, height * 0.31))
        _box(trees, x, 0, z, 0.28, height * 0.57, 0.28, (0.32, 0.27, 0.20, 1))
        variant = int(tree["id"]) % 5
        color = (0.22 + variant * 0.025, 0.36 + variant * 0.021, 0.19 + variant * 0.012, 1)
        _crown(trees, x, height * 0.64, z, radius, height * 0.54, color)
    for index, (x, z) in enumerate(illustrative_canopy(data, buildings)):
        height = 7 + index % 4
        _box(trees, x, 0, z, 0.25, height * 0.57, 0.25, (0.32, 0.27, 0.20, 1))
        _crown(trees, x, height * 0.64, z, 2.3, height * 0.54, (0.26, 0.42, 0.24, 1))
    for index, stop in enumerate(data["busStops"]):
        x, z = stop["position"]
        _box(street_props, x, 0, z, 0.1, 2.9, 0.1, (0.34, 0.36, 0.36, 1))
        _box(street_props, x, 2.05, z, 0.63, 0.66, 0.12, (0.02, 0.17, 0.31, 1))
        _box(street_props, x, 2.51, z - 0.07, 0.48, 0.1, 0.02, (1.0, 0.79, 0.04, 1))
    positions = illustrative_positions(data, buildings)
    for index, (x, z) in enumerate(positions):
        if index % 7 == 0:
            # This schematic bench is a scale cue, not a sourced seating location.
            _box(street_props, x, 0.47, z, 1.6, 0.11, 0.48, (0.43, 0.32, 0.20, 1))
            _box(street_props, x, 0.64, z + 0.22, 1.6, 0.47, 0.10, (0.43, 0.32, 0.20, 1))
            for offset in (-0.57, 0.57):
                _box(street_props, x + offset, 0.08, z, 0.08, 0.40, 0.35, (0.19, 0.22, 0.22, 1))
        else:
            color = ((0.13, 0.29, 0.39, 1), (0.61, 0.33, 0.21, 1), (0.72, 0.59, 0.22, 1))[index % 3]
            _box(street_props, x, 0.77, z, 0.39, 0.62, 0.24, color)
            for offset in (-0.10, 0.10):
                _box(street_props, x + offset, 0.12, z, 0.13, 0.67, 0.16, (0.19, 0.22, 0.25, 1))
            _crown(street_props, x, 1.56, z, 0.15, 0.32, (0.63, 0.47, 0.35, 1), segments=4)
    return {name: builder.finish() for name, builder in (
        ("surfaces", surfaces), ("trees", trees), ("streetProps", street_props), ("contextBuildings", context)
    ) if builder.indices}
