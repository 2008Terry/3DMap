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
            materialAlpha: root.mode === "xray" ? root.inspector.shell_opacity * 0.5 : 1
        }
    }
    Model {
        geometry: root.inspector.facade
        visible: root.mode !== "floor" && root.mode !== "inside" && root.mode !== "explode" && root.mode !== "xray"
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
            readonly property bool current: index === root.inspector.selected_floor
            y: modelData.elevation + (root.mode === "explode" ? index * root.inspector.spread : 0)
            visible: (root.mode !== "floor" && root.mode !== "inside") || index === root.inspector.selected_floor
            Model {
                readonly property int inspectionFloor: level.index
                geometry: level.modelData.slab
                pickable: true
                materials: CutMaterial {
                    sectionAxis: root.axis
                    sectionPosition: root.positionOnAxis
                    materialAlpha: root.mode === "xray" ? (level.current ? 0.18 : 0.018) : 1
                }
            }
            Model {
                readonly property int inspectionFloor: level.index
                geometry: level.modelData.walls
                pickable: true
                materials: CutMaterial {
                    sectionAxis: root.axis
                    sectionPosition: root.positionOnAxis
                    materialAlpha: root.mode === "xray" ? (level.current ? 0.60 : 0.035) : 1
                }
            }
            Model {
                readonly property int inspectionFloor: level.index
                geometry: level.modelData.zones
                visible: root.mode !== "xray" || level.current
                pickable: true
                materials: CutMaterial {
                    sectionAxis: root.axis
                    sectionPosition: root.positionOnAxis
                    materialAlpha: root.mode === "xray" ? 0.45 : 1
                }
            }
            Model {
                geometry: level.modelData.outline
                visible: root.mode !== "inside"
                materials: CutMaterial {
                    sectionAxis: root.axis
                    sectionPosition: root.positionOnAxis
                    materialAlpha: root.mode === "xray" && !level.current ? 0.16 : 1
                }
            }
            Model {
                geometry: level.modelData.ceiling
                visible: root.mode === "inside"
                materials: CutMaterial { }
            }
            Model {
                readonly property int inspectionFloor: level.index
                geometry: level.modelData.furniture
                visible: root.inspector.show_furniture && (root.mode !== "xray" || level.current)
                pickable: true
                materials: CutMaterial {
                    sectionAxis: root.axis
                    sectionPosition: root.positionOnAxis
                }
            }
        }
    }
    Model {
        geometry: root.inspector.room_geometry
        visible: geometry !== null
        y: (root.inspector.current_floor.elevation || 0) +
           (root.mode === "explode" ? root.inspector.selected_floor * root.inspector.spread : 0)
        pickable: false
        materials: CutMaterial {
            sectionAxis: root.axis
            sectionPosition: root.positionOnAxis
            materialAlpha: 0.7
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
