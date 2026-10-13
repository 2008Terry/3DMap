"""Batched, inferred facade decoration; no photographed or surveyed geometry.

Windows and doors suggest architectural scale. Their positions and floor count
are procedural and must not be treated as verified entrances or floor plans.
"""

from __future__ import annotations

from math import hypot
from typing import Sequence
from zlib import crc32

from shapely.geometry import Polygon

if __package__:
    from .campus_data import Building
    from .mesh_builder import MeshBuffers, _MeshBuilder, _rgba
else:
    from campus_data import Building
    from mesh_builder import MeshBuffers, _MeshBuilder, _rgba


def _quad(builder, points, normal, color):
    builder.triangle((points[0], points[1], points[2]), normal, color)
    builder.triangle((points[0], points[2], points[3]), normal, color)


def _panel(builder, edge, start, width, bottom, top, offset, color):
    x, z, dx, dz, length, nx, nz, _height = edge
    tx, tz = dx / length, dz / length
    a = (x + tx * start + nx * offset, bottom, z + tz * start + nz * offset)
    b = (a[0] + tx * width, bottom, a[2] + tz * width)
    c, d = (b[0], top, b[2]), (a[0], top, a[2])
    # Keep front-face winding consistent for either footprint orientation.
    cross_x, cross_z = -dz, dx
    points = (a, b, c, d) if cross_x * nx + cross_z * nz > 0 else (b, a, d, c)
    _quad(builder, points, (nx, 0.0, nz), color)


def _edges(building):
    edges = []
    for part in building.parts:
        polygon = Polygon(part["footprint"])
        height = float(part["height_m"])
        if not polygon.is_valid or polygon.is_empty or polygon.area < 18 or height < 3:
            continue
        ring = list(polygon.exterior.coords)
        direction = 1 if polygon.exterior.is_ccw else -1
        for a, b in zip(ring, ring[1:]):
            dx, dz = b[0] - a[0], b[1] - a[1]
            length = hypot(dx, dz)
            if length >= 1.5:
                # Ring orientation works for concave outlines, unlike a centroid test.
                edges.append((a[0], a[1], dx, dz, length,
                              direction * dz / length, -direction * dx / length, height))
    return edges


def build_facade_mesh(buildings: Sequence[Building]) -> MeshBuffers:
    """Return one opaque vertex-color batch with at most 96 windows per building.

    All dimensions are in the same meter coordinates as the campus shell mesh.
    Caller can submit subsets for district culling; no Qt objects or I/O are used.
    """
    builder = _MeshBuilder()
    frame = (0.28, 0.31, 0.30, 1.0)
    glass = ((0.15, 0.25, 0.29, 1.0), (0.22, 0.34, 0.38, 1.0),
             (0.31, 0.40, 0.42, 1.0), (0.42, 0.43, 0.36, 1.0))
    for building in buildings:
        edges = _edges(building)
        if not edges:
            continue
        base = _rgba(building.color)
        trim = tuple(min(1.0, component * 0.85 + 0.12) for component in base[:3]) + (1.0,)
        roof = tuple(component * 0.65 for component in base[:3]) + (1.0,)
        eligible = [edge for edge in edges if edge[4] >= 4.2 and edge[7] >= 4.0]
        weights = [edge[4] * min(6, max(1, int(edge[7] / 3.8))) for edge in eligible]
        total_weight = sum(weights) or 1
        seed = crc32(building.id.encode("utf-8"))
        for edge in edges:
            x, z, dx, dz, length, nx, nz, height = edge
            _panel(builder, edge, 0, length, height - 0.23, height + 0.04, 0.055, trim)
            # A narrow horizontal parapet cap catches light without repainting the roof.
            a = (x + nx * 0.055, height + 0.045, z + nz * 0.055)
            b = (x + dx + nx * 0.055, height + 0.045, z + dz + nz * 0.055)
            c, d = (b[0] - nx * 0.32, b[1], b[2] - nz * 0.32), (a[0] - nx * 0.32, a[1], a[2] - nz * 0.32)
            # Explicitly order upward faces, including clockwise footprint rings.
            cap = (a, d, c, b) if dx * nz - dz * nx < 0 else (a, b, c, d)
            _quad(builder, cap, (0.0, 1.0, 0.0), roof)

        for edge_index, (edge, weight) in enumerate(zip(eligible, weights)):
            height, length = edge[7], edge[4]
            rows = min(6, max(1, int(height / 3.8)))
            allowance = int(96 * weight / total_weight)
            columns = min(int(length / 3.3), allowance // rows)
            if not columns:
                continue
            step_x, step_y = length / columns, height / rows
            width = min(1.65, step_x * 0.5)
            for row in range(rows):
                bottom = row * step_y + max(0.9, step_y * 0.25)
                top = min(height - 0.55, bottom + min(2.15, step_y * 0.54))
                for column in range(columns):
                    start = (column + 0.5) * step_x - width / 2
                    _panel(builder, edge, start - 0.08, width + 0.16, bottom - 0.08, top + 0.08, 0.07, frame)
                    tint = glass[(seed + edge_index * 7 + row * 3 + column) % len(glass)]
                    _panel(builder, edge, start, width, bottom, top, 0.085, tint)

        entry = max(edges, key=lambda edge: edge[4])
        if entry[4] >= 5:
            width = min(2.4, entry[4] * 0.23)
            start = (entry[4] - width) / 2
            _panel(builder, entry, start - 0.16, width + 0.32, 0.02, 2.75, 0.095, trim)
            _panel(builder, entry, start, width, 0.03, 2.52, 0.11, glass[0])
            _panel(builder, entry, entry[4] / 2 - 0.045, 0.09, 0.03, 2.52, 0.12, frame)

    if not builder.indices:
        return MeshBuffers((), (), (), (), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    return builder.finish()
