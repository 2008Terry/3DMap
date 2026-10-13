import QtQuick
import QtQuick3D

Node {
    id: root
    required property var inspector
    property string mode: inspector.mode
    property int axis: mode === "dollhouse" ? 4 : mode === "section"
                       ? (inspector.cut_axis === "y" ? 1 : inspector.cut_axis === "x" ? 2 : 3) : 0
    property real positionOnAxis: inspector.cut_axis === "y" ? inspector.cut * inspector.bounds.height
                                 : (inspector.cut - 0.5) * (inspector.cut_axis === "x" ? inspector.bounds.width : inspector.bounds.depth)

    Model {
        geometry: root.inspector.shell
        visible: root.mode !== "floor" && root.mode !== "inside" && root.mode !== "explode"
        pickable: false
        materials: CutMaterial {
            sectionAxis: root.axis
            sectionPosition: root.positionOnAxis
            materialAlpha: root.mode === "xray" ? root.inspector.shell_opacity : 1
        }
    }
    Model {
        geometry: root.inspector.facade
        visible: root.mode !== "floor" && root.mode !== "inside" && root.mode !== "explode"
        materials: CutMaterial {
            sectionAxis: root.axis
            sectionPosition: root.positionOnAxis
            materialAlpha: root.mode === "xray" ? root.inspector.shell_opacity : 1
        }
    }
    Repeater3D {
        model: root.inspector.floors
        delegate: Node {
            id: level
            required property var modelData
            required property int index
            y: modelData.elevation + (root.mode === "explode" ? index * root.inspector.spread : 0)
            visible: (root.mode !== "floor" && root.mode !== "inside") || index === root.inspector.selected_floor
            Model {
                geometry: level.modelData.slab
                pickable: true
                materials: CutMaterial {
                    sectionAxis: root.axis
                    sectionPosition: root.positionOnAxis
                    materialAlpha: root.mode === "xray" ? 0.32 : 1
                }
            }
            Model {
                geometry: level.modelData.walls
                pickable: true
                materials: CutMaterial {
                    sectionAxis: root.axis
                    sectionPosition: root.positionOnAxis
                    materialAlpha: root.mode === "xray" ? 0.25 : 1
                }
            }
            Model {
                geometry: level.modelData.slab
                y: level.modelData.height
                visible: root.mode === "inside"
                materials: CutMaterial { }
            }
            Model {
                geometry: level.modelData.furniture
                visible: root.inspector.show_furniture
                pickable: true
                materials: CutMaterial {
                    sectionAxis: root.axis
                    sectionPosition: root.positionOnAxis
                }
            }
        }
    }
    Model {
        visible: root.mode === "section"
        source: "#Cube"
        position: root.axis === 1 ? Qt.vector3d(0, root.positionOnAxis, 0)
                 : root.axis === 2 ? Qt.vector3d(root.positionOnAxis, root.inspector.bounds.height / 2, 0)
                 : Qt.vector3d(0, root.inspector.bounds.height / 2, root.positionOnAxis)
        scale: Qt.vector3d(root.axis === 2 ? 0.0008 : root.inspector.bounds.width * 1.1 / 100,
                           root.axis === 1 ? 0.0008 : root.inspector.bounds.height / 100,
                           root.axis === 3 ? 0.0008 : root.inspector.bounds.depth * 1.1 / 100)
        materials: PrincipledMaterial {
            baseColor: "#f6b353"
            opacity: 0.10
            alphaMode: PrincipledMaterial.Blend
            lighting: PrincipledMaterial.NoLighting
            cullMode: PrincipledMaterial.NoCulling
        }
    }
}
