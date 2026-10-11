import QtQuick
import QtQuick3D
import QtQuick3D.Helpers

Item {
    id: root

    property var campusExtent
    property var centralGeometry
    property var northGeometry
    property var featuredGeometries
    property var campusPicker
    signal buildingPicked(string buildingId)

    View3D {
        id: view
        anchors.fill: parent
        camera: mapCamera
        environment: SceneEnvironment {
            backgroundMode: SceneEnvironment.Color
            clearColor: "#dbe5e4"
            fog: Fog {
                enabled: true
                color: "#dbe5e4"
                depthEnabled: true
                depthNear: Math.max(root.campusExtent.width, root.campusExtent.depth) * 0.7
                depthFar: Math.max(root.campusExtent.width, root.campusExtent.depth) * 1.9
            }
        }

        Node {
            id: world

            Node {
                id: cameraOrigin
                position: Qt.vector3d(root.campusExtent.centerX, 0, root.campusExtent.centerZ)

                PerspectiveCamera {
                    id: mapCamera
                    position: Qt.vector3d(0, Math.max(root.campusExtent.width, root.campusExtent.depth) * 0.78,
                                          Math.max(root.campusExtent.width, root.campusExtent.depth) * 0.82)
                    eulerRotation.x: -42
                    clipNear: 1
                    clipFar: 12000
                    fieldOfView: 48
                }
            }

            DirectionalLight {
                eulerRotation: Qt.vector3d(-38, -30, 0)
                color: "#fff7e6"
                brightness: 1.35
            }
            DirectionalLight {
                eulerRotation: Qt.vector3d(145, 25, 0)
                color: "#bfd3e2"
                brightness: 0.45
            }

            Model {
                source: "#Cube"
                position: Qt.vector3d(root.campusExtent.centerX, -1, root.campusExtent.centerZ)
                scale: Qt.vector3d(root.campusExtent.width * 1.08 / 100, 0.012,
                                   root.campusExtent.depth * 1.08 / 100)
                materials: PrincipledMaterial {
                    baseColor: "#dfe5dc"
                    roughness: 1
                }
            }

            Model {
                geometry: root.centralGeometry
                pickable: true
                materials: PrincipledMaterial {
                    baseColor: "#ffffff"
                    vertexColorsEnabled: true
                    roughness: 0.91
                    cullMode: PrincipledMaterial.NoCulling
                }
            }
            Model {
                geometry: root.northGeometry
                pickable: true
                materials: PrincipledMaterial {
                    baseColor: "#ffffff"
                    vertexColorsEnabled: true
                    roughness: 0.91
                    cullMode: PrincipledMaterial.NoCulling
                }
            }

            Repeater3D {
                model: root.featuredGeometries.length
                delegate: Model {
                    required property int index
                    geometry: root.featuredGeometries[index]
                    pickable: true
                    materials: PrincipledMaterial {
                        baseColor: "#ffffff"
                        vertexColorsEnabled: true
                        roughness: 0.88
                        cullMode: PrincipledMaterial.NoCulling
                    }
                }
            }
        }

        OrbitCameraController {
            origin: cameraOrigin
            camera: mapCamera
            panEnabled: true
            xSpeed: 0.18
            ySpeed: 0.18
        }

        TapHandler {
            acceptedButtons: Qt.LeftButton
            onTapped: function(eventPoint) {
                const hit = view.pick(eventPoint.position.x, eventPoint.position.y)
                if (!hit.objectHit)
                    return
                const point = hit.scenePosition
                const id = root.campusPicker.selectAt(point.x, point.y, point.z)
                if (id.length > 0)
                    root.buildingPicked(id)
            }
        }
    }
}
