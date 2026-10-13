import QtQuick
import QtQuick3D
import QtQuick3D.Helpers

Item {
    id: root
    objectName: "mapScene"
    focus: true
    property var campusExtent
    property var centralGeometry
    property var northGeometry
    property var featuredGeometries: []
    property var environmentGeometries: []
    property var facadeGeometry
    property var mapController
    property var selectionOverlay
    property var inspector
    property bool showStats: false
    property bool pointerSelected: false
    property real pointerAnchorX: 0
    property real pointerAnchorY: 0
    readonly property int drawCalls: view.renderStats.drawCallCount
    readonly property int fps: view.renderStats.fps
    readonly property string graphicsApi: view.renderStats.graphicsApiName
    signal buildingPicked(string buildingId)

    function resetCampus() {
        cameraOrigin.position = Qt.vector3d(campusExtent.centerX, 0, campusExtent.centerZ)
        const size = Math.max(campusExtent.width, campusExtent.depth)
        mapCamera.position = Qt.vector3d(0, size * 0.78, size * 0.82)
        mapCamera.eulerRotation = Qt.vector3d(-42, 0, 0)
    }
    function walk(distance) {
        if (!inspector.active || inspector.mode !== "inside")
            return
        const radians = walkCamera.eulerRotation.y * Math.PI / 180
        const nx = walkCamera.position.x - Math.sin(radians) * distance
        const nz = walkCamera.position.z - Math.cos(radians) * distance
        if (inspector.can_walk(walkCamera.position.x, walkCamera.position.z, nx, nz))
            walkCamera.position = Qt.vector3d(nx, walkCamera.position.y, nz)
    }
    function look(dx, dy) {
        walkCamera.eulerRotation = Qt.vector3d(
            Math.max(-70, Math.min(70, walkCamera.eulerRotation.x + dy)),
            walkCamera.eulerRotation.y + dx, 0)
    }
    function selectAtScreen(px, py) {
        const hits = view.pickAll(px, py)
        for (let i = 0; i < hits.length; i++) {
            const point = hits[i].scenePosition
            if (inspector.active) {
                const mode = inspector.mode
                const b = inspector.bounds
                if (mode === "section" &&
                    ((inspector.cut_axis === "x" && point.x > (inspector.cut - 0.5) * b.width) ||
                     (inspector.cut_axis === "z" && point.z > (inspector.cut - 0.5) * b.depth) ||
                     (inspector.cut_axis === "y" && point.y > inspector.cut * b.height)))
                    continue
                if (mode === "dollhouse" && point.x > 0 && point.z > 0)
                    continue
                inspector.pick_room(point.x, point.y, point.z)
                return
            }
            const id = mapController.select_at(point.x, point.y, point.z)
            if (id.length > 0) {
                root.buildingPicked(id)
                return
            }
        }
    }

    Keys.onPressed: function(event) {
        if (event.key === Qt.Key_F3) {
            root.showStats = !root.showStats
            event.accepted = true
        } else if (inspector.active && inspector.mode === "inside") {
            if (event.key === Qt.Key_W || event.key === Qt.Key_Up) root.walk(1.2)
            else if (event.key === Qt.Key_S || event.key === Qt.Key_Down) root.walk(-1.2)
            else if (event.key === Qt.Key_A || event.key === Qt.Key_Left) root.look(-7, 0)
            else if (event.key === Qt.Key_D || event.key === Qt.Key_Right) root.look(7, 0)
            else return
            event.accepted = true
        }
    }

    View3D {
        id: view
        objectName: "campusView"
        anchors.fill: parent
        camera: root.inspector.active && root.inspector.mode === "inside" ? walkCamera : mapCamera
        environment: SceneEnvironment {
            backgroundMode: SceneEnvironment.Color
            clearColor: root.inspector.active ? "#d4d9d5" : "#c8d9dd"
            antialiasingMode: SceneEnvironment.MSAA
            antialiasingQuality: SceneEnvironment.Medium
            fog: Fog {
                enabled: !root.inspector.active
                color: "#c8d9dd"
                depthEnabled: true
                depthNear: Math.max(root.campusExtent.width, root.campusExtent.depth) * 0.8
                depthFar: Math.max(root.campusExtent.width, root.campusExtent.depth) * 2.0
            }
        }
        renderStats.extendedDataCollectionEnabled: root.showStats

        Node {
            Node {
                id: cameraOrigin
                position: Qt.vector3d(root.campusExtent.centerX, 0, root.campusExtent.centerZ)
                PerspectiveCamera {
                    id: mapCamera
                    position: Qt.vector3d(0, Math.max(root.campusExtent.width, root.campusExtent.depth) * 0.78,
                                           Math.max(root.campusExtent.width, root.campusExtent.depth) * 0.82)
                    eulerRotation.x: -42
                    clipNear: 0.1
                    clipFar: 12000
                    fieldOfView: 48
                }
            }
            PerspectiveCamera {
                id: walkCamera
                objectName: "walkCamera"
                clipNear: 0.04
                clipFar: 600
                fieldOfView: 67
            }
            DirectionalLight {
                eulerRotation: Qt.vector3d(-42, -30, 0)
                color: "#fff8e9"
                brightness: 1.4
                ambientColor: "#65716d"
                castsShadow: root.inspector.active
            }
            DirectionalLight {
                eulerRotation: Qt.vector3d(140, 40, 0)
                color: "#b7d0df"
                brightness: 0.55
            }
            PointLight {
                position: walkCamera.position
                visible: root.inspector.active && root.inspector.mode === "inside"
                color: "#fff3dc"
                brightness: 0.3
                quadraticFade: 2
            }
            Node {
                visible: !root.inspector.active
                Model {
                    source: "#Cube"
                    position: Qt.vector3d(root.campusExtent.centerX, -1.2, root.campusExtent.centerZ)
                    scale: Qt.vector3d(root.campusExtent.width * 1.08 / 100, 0.012,
                                       root.campusExtent.depth * 1.08 / 100)
                    materials: PrincipledMaterial { baseColor: "#dfe6dc"; roughness: 1 }
                }
                Model {
                    geometry: root.centralGeometry
                    pickable: true
                    materials: PrincipledMaterial {
                        baseColor: "#ffffff"; vertexColorsEnabled: true; roughness: 0.91
                        cullMode: PrincipledMaterial.NoCulling
                    }
                }
                Model {
                    geometry: root.northGeometry
                    pickable: true
                    materials: PrincipledMaterial {
                        baseColor: "#ffffff"; vertexColorsEnabled: true; roughness: 0.91
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
                            baseColor: "#ffffff"; vertexColorsEnabled: true; roughness: 0.88
                            cullMode: PrincipledMaterial.NoCulling
                        }
                    }
                }
                Repeater3D {
                    model: root.environmentGeometries.length
                    delegate: Model {
                        required property int index
                        geometry: root.environmentGeometries[index]
                        materials: PrincipledMaterial {
                            baseColor: "#ffffff"; vertexColorsEnabled: true; roughness: 1
                            cullMode: PrincipledMaterial.NoCulling
                        }
                    }
                }
                Model {
                    geometry: root.facadeGeometry
                    materials: PrincipledMaterial {
                        baseColor: "#ffffff"; vertexColorsEnabled: true; roughness: 0.72
                        cullMode: PrincipledMaterial.NoCulling
                    }
                }
                Model {
                    geometry: root.selectionOverlay ? root.selectionOverlay.geometry : null
                    visible: !!root.selectionOverlay && root.selectionOverlay.geometry !== null
                    materials: PrincipledMaterial {
                        baseColor: "#ffffff"; vertexColorsEnabled: true; opacity: 0.42
                        alphaMode: PrincipledMaterial.Blend
                        cullMode: PrincipledMaterial.NoCulling
                    }
                }
            }
            InspectionScene {
                id: inspectionScene
                inspector: root.inspector
                visible: root.inspector.active
            }
        }
        OrbitCameraController {
            origin: cameraOrigin
            camera: mapCamera
            enabled: !root.inspector.active || root.inspector.mode !== "inside"
            panEnabled: true
            xSpeed: 0.18
            ySpeed: 0.18
        }
        TapHandler {
            acceptedButtons: Qt.LeftButton
            onTapped: function(eventPoint) {
                root.forceActiveFocus()
                root.selectAtScreen(eventPoint.position.x, eventPoint.position.y)
            }
        }
        Connections {
            target: root.mapController
            function onResetCameraRequested() { root.resetCampus() }
            function onPanRequested(dx, dz) {
                cameraOrigin.position = Qt.vector3d(cameraOrigin.position.x + dx,
                    cameraOrigin.position.y, cameraOrigin.position.z + dz)
            }
            function onZoomRequested(factor) {
                const distance = Math.max(root.inspector.active ? 8 : 300,
                                          Math.min(11000, mapCamera.position.z * factor))
                const ratio = distance / mapCamera.position.z
                mapCamera.position = Qt.vector3d(mapCamera.position.x,
                    mapCamera.position.y * ratio, distance)
            }
            function onFocusRequested(x, z, distance) {
                cameraOrigin.position = Qt.vector3d(x, 0, z)
                mapCamera.position = Qt.vector3d(0, distance * 0.8, distance)
                mapCamera.eulerRotation = Qt.vector3d(-42, 0, 0)
            }
            function onLookRequested(dx, dy) { root.look(dx, dy) }
            function onWalkRequested(distance) { root.walk(distance) }
            function onPointingChanged(x, y, valid) {
                if (!valid) {
                    pointer.visible = false; root.pointerSelected = false; dwell.stop(); return
                }
                const px = x * root.width, py = y * root.height
                const moved = !pointer.visible || Math.hypot(px - root.pointerAnchorX, py - root.pointerAnchorY) > 24
                pointer.x = px - 13; pointer.y = py - 13; pointer.visible = true
                if (moved) {
                    root.pointerAnchorX = px; root.pointerAnchorY = py
                    root.pointerSelected = false; dwell.restart()
                }
                else if (!root.pointerSelected && !dwell.running) dwell.restart()
            }
        }
        Connections {
            target: root.inspector
            function onViewRequested() {
                if (!root.inspector.active) { root.resetCampus(); return }
                const b = root.inspector.bounds
                cameraOrigin.position = Qt.vector3d(0, 0, 0)
                if (root.inspector.mode === "inside") {
                    const floor = root.inspector.current_floor
                    walkCamera.position = Qt.vector3d(floor.startX, floor.elevation + 1.65, floor.startZ)
                    walkCamera.eulerRotation = Qt.vector3d(0, floor.startYaw, 0)
                } else {
                    const distance = Math.max(35, b.width, b.depth, b.height) *
                                     (root.inspector.mode === "explode" ? 2.1 : 1.6)
                    mapCamera.position = Qt.vector3d(0, distance * 0.85, distance)
                    mapCamera.eulerRotation = Qt.vector3d(-38, 0, 0)
                }
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        enabled: root.inspector.active && root.inspector.mode === "inside"
        acceptedButtons: Qt.RightButton
        hoverEnabled: false
        property real lastX: 0
        property real lastY: 0
        onPressed: function(mouse) { lastX = mouse.x; lastY = mouse.y; root.forceActiveFocus() }
        onPositionChanged: function(mouse) {
            if (!pressed) return
            root.look((mouse.x - lastX) * 0.2, (mouse.y - lastY) * 0.2)
            lastX = mouse.x; lastY = mouse.y
        }
        onWheel: function(wheel) { root.walk(wheel.angleDelta.y > 0 ? 1.2 : -1.2) }
    }
    Rectangle {
        id: pointer
        visible: false
        width: 26; height: 26; radius: 13
        color: "#00000000"; border.width: 3; border.color: "#ffcc4c"
    }
    Timer {
        id: dwell
        interval: 850
        onTriggered: if (pointer.visible) {
            root.selectAtScreen(pointer.x + 13, pointer.y + 13)
            root.pointerSelected = true
        }
    }
    Rectangle {
        visible: root.showStats
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 10
        width: 210; height: 54; radius: 5
        color: "#c9213036"
        Text {
            anchors.centerIn: parent
            color: "white"; font.pixelSize: 11
            text: "FPS " + Math.round(view.renderStats.fps) +
                  "  Draw " + view.renderStats.drawCallCount +
                  "\nGPU " + view.renderStats.graphicsApiName
        }
    }
}
