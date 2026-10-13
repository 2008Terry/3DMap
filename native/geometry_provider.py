"""Upload packed mesh buffers to a Qt Quick 3D custom geometry."""

from __future__ import annotations

import struct
import zlib

from PySide6.QtCore import QByteArray, QObject, Property, Signal, Slot
from PySide6.QtGui import QVector3D
from PySide6.QtQuick3D import QQuick3DGeometry

if __package__:
    from .mesh_builder import MeshBuffers
else:
    from mesh_builder import MeshBuffers


class _CampusGeometry(QQuick3DGeometry):
    def __init__(self, buffers: MeshBuffers = None, packed: bytes = None):
        super().__init__()
        self.setStride(40)
        self.setPrimitiveType(QQuick3DGeometry.PrimitiveType.Triangles)
        self._attribute(QQuick3DGeometry.Attribute.Semantic.PositionSemantic, 0, 3)
        self._attribute(QQuick3DGeometry.Attribute.Semantic.NormalSemantic, 12, 3)
        self._attribute(QQuick3DGeometry.Attribute.Semantic.ColorSemantic, 24, 4)
        self._attribute(QQuick3DGeometry.Attribute.Semantic.IndexSemantic, 0, 1, index=True)
        if packed is not None:
            if packed[:8] != b"CAMPUSM1":
                raise ValueError("Invalid compiled campus geometry")
            bounds = struct.unpack_from("<6f", packed, 8)
            vertex_size, index_size = struct.unpack_from("<2I", packed, 32)
            if len(packed) != 40 + vertex_size + index_size or vertex_size % 40 or index_size % 4:
                raise ValueError("Truncated compiled campus geometry")
            self.setVertexData(QByteArray(packed[40:40 + vertex_size]))
            self.setIndexData(QByteArray(packed[40 + vertex_size:]))
            self.setBounds(QVector3D(*bounds[:3]), QVector3D(*bounds[3:]))
        else:
            self.setVertexData(QByteArray(struct.pack(f"<{len(buffers.positions) + len(buffers.normals) + len(buffers.colors)}f", *self._interleave(buffers))))
            self.setIndexData(QByteArray(struct.pack(f"<{len(buffers.indices)}I", *buffers.indices)))
            self.setBounds(QVector3D(*buffers.bounds_min), QVector3D(*buffers.bounds_max))

    def _attribute(self, semantic, offset: int, component_count: int, index: bool = False):
        attribute = QQuick3DGeometry.Attribute()
        attribute.semantic = semantic
        attribute.componentType = (
            QQuick3DGeometry.Attribute.ComponentType.U32Type
            if index else QQuick3DGeometry.Attribute.ComponentType.F32Type
        )
        attribute.offset = offset
        self.addAttribute(attribute)

    @staticmethod
    def _interleave(buffers: MeshBuffers) -> tuple[float, ...]:
        vertices = len(buffers.positions) // 3
        packed: list[float] = []
        for index in range(vertices):
            packed.extend(buffers.positions[index * 3:index * 3 + 3])
            packed.extend(buffers.normals[index * 3:index * 3 + 3])
            packed.extend(buffers.colors[index * 4:index * 4 + 4])
        return tuple(packed)


def geometry_from_buffers(buffers: MeshBuffers) -> QQuick3DGeometry:
    return _CampusGeometry(buffers)


def geometry_from_asset(path):
    return _CampusGeometry(packed=zlib.decompress(path.read_bytes()))


def write_geometry_asset(buffers, path):
    vertices = _CampusGeometry._interleave(buffers)
    vertex_data = struct.pack(f"<{len(vertices)}f", *vertices)
    index_data = struct.pack(f"<{len(buffers.indices)}I", *buffers.indices)
    header = b"CAMPUSM1" + struct.pack("<6f2I", *buffers.bounds_min, *buffers.bounds_max,
                                     len(vertex_data), len(index_data))
    path.write_bytes(zlib.compress(header + vertex_data + index_data, level=6))


class SelectionOverlay(QObject):
    geometryChanged = Signal()

    def __init__(self):
        super().__init__()
        self._geometry = None

    @Property(QObject, notify=geometryChanged)
    def geometry(self):
        return self._geometry

    @Slot(QObject)
    def setGeometry(self, geometry):
        self._geometry = geometry
        self.geometryChanged.emit()
