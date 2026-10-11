"""Upload packed mesh buffers to a Qt Quick 3D custom geometry."""

from __future__ import annotations

import struct

from PySide6.QtCore import QByteArray
from PySide6.QtGui import QVector3D
from PySide6.QtQuick3D import QQuick3DGeometry

if __package__:
    from .mesh_builder import MeshBuffers
else:
    from mesh_builder import MeshBuffers


class _CampusGeometry(QQuick3DGeometry):
    def __init__(self, buffers: MeshBuffers):
        super().__init__()
        self.setStride(40)
        self.setPrimitiveType(QQuick3DGeometry.PrimitiveType.Triangles)
        self._attribute(QQuick3DGeometry.Attribute.Semantic.PositionSemantic, 0, 3)
        self._attribute(QQuick3DGeometry.Attribute.Semantic.NormalSemantic, 12, 3)
        self._attribute(QQuick3DGeometry.Attribute.Semantic.ColorSemantic, 24, 4)
        self._attribute(QQuick3DGeometry.Attribute.Semantic.IndexSemantic, 0, 1, index=True)
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
