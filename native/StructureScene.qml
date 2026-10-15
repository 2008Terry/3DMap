import QtQuick
import QtQuick3D

Node {
    id: root
    required property var state
    property bool overview: true
    property int floorIndex: 0
    property real viewYaw: 35
    readonly property var lens: state.lens

    Repeater3D {
        model: root.state.floors
        delegate: Node {
            id: level
            required property var modelData
            readonly property int floorId: modelData.index
            readonly property bool current: floorId === root.state.floor_index
            readonly property var offset: {
                // Read a notifying property before invoking the position method.
                const revision = root.state.bounds
                return root.overview ? root.state.floor_position(floorId) : ({x: 0, y: 0, z: 0})
            }
            position: Qt.vector3d(offset.x, offset.y, offset.z)
            visible: root.overview || floorId === root.floorIndex
            Model {
                geometry: level.modelData.slab
                materials: RevealMaterial { }
            }
            Model {
                geometry: level.modelData.walls
                materials: RevealMaterial {
                    revealEnabled: root.state.cut_enabled
                    focusX: level.current ? root.lens.x : (level.modelData.core.x || 0)
                    focusZ: level.current ? root.lens.z : (level.modelData.core.z || 0)
                    focusRadius: level.current ? root.lens.radius : root.state.context_radius
                    directionX: Math.sin(root.viewYaw * Math.PI / 180)
                    directionZ: Math.cos(root.viewYaw * Math.PI / 180)
                }
            }
            Model {
                geometry: level.modelData.zones
                materials: RevealMaterial { }
            }
            Model {
                geometry: level.modelData.outline
                materials: RevealMaterial {
                    // Keep the plan outlines; omit high wall-top outlines at cuts.
                    revealEnabled: root.state.cut_enabled
                    focusX: level.current ? root.lens.x : (level.modelData.core.x || 0)
                    focusZ: level.current ? root.lens.z : (level.modelData.core.z || 0)
                    focusRadius: level.current ? root.lens.radius : root.state.context_radius
                    directionX: Math.sin(root.viewYaw * Math.PI / 180)
                    directionZ: Math.cos(root.viewYaw * Math.PI / 180)
                }
            }
            Model {
                geometry: level.modelData.furniture
                visible: root.state.furniture && level.current
                materials: RevealMaterial { }
            }
            Model {
                geometry: root.state.highlight
                visible: level.current && geometry !== null
                materials: RevealMaterial { }
            }
            Model {
                geometry: root.state.route_geometry
                visible: level.current && geometry !== null
                materials: RevealMaterial { }
            }
            Model {
                visible: Object.keys(level.modelData.core).length > 0
                source: "#Cylinder"
                position: Qt.vector3d(level.modelData.core.x || 0, 0.4, level.modelData.core.z || 0)
                scale: Qt.vector3d(0.025, 0.008, 0.025)
                materials: PrincipledMaterial {
                    baseColor: "#168d9d"
                    lighting: PrincipledMaterial.NoLighting
                }
            }
        }
    }
    Repeater3D {
        model: root.overview ? root.state.links : []
        delegate: Model {
            required property var modelData
            readonly property real dx: modelData.b[0] - modelData.a[0]
            readonly property real dy: modelData.b[1] - modelData.a[1]
            readonly property real dz: modelData.b[2] - modelData.a[2]
            readonly property real length: Math.sqrt(dx * dx + dy * dy + dz * dz)
            readonly property real qw: Math.sqrt((1 + dy / Math.max(0.01, length)) / 2)
            source: "#Cylinder"
            position: Qt.vector3d((modelData.a[0] + modelData.b[0]) / 2,
                                  (modelData.a[1] + modelData.b[1]) / 2,
                                  (modelData.a[2] + modelData.b[2]) / 2)
            rotation: Qt.quaternion(qw, dz / (2 * qw * length), 0, -dx / (2 * qw * length))
            scale: Qt.vector3d(0.009, length / 100, 0.009)
            materials: PrincipledMaterial {
                baseColor: "#168d9d"
                lighting: PrincipledMaterial.NoLighting
            }
        }
    }
}
