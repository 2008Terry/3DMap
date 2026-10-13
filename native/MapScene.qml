import QtQuick
import QtQuick3D
import QtQuick.Controls

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
    property var gestureWorker
    property bool showStats: false
    property bool pointerSelected: false
    property real pointerAnchorX: 0
    property real pointerAnchorY: 0
    property real pointerProgress: 0
    property double dwellStarted: 0
    property var heldKeys: ({})
    property var campusViewState: null
    property bool wasInspecting: false
    property string inspectionViewKey: ""
    property string walkViewKey: ""
    property string selectionMessage: ""
    readonly property int drawCalls: view.renderStats.drawCallCount
    readonly property int fps: view.renderStats.fps
    readonly property string graphicsApi: view.renderStats.graphicsApiName
    signal buildingPicked(string buildingId)
    signal gestureSettingsRequested()

    function resetCampus() {
        cameraOrigin.eulerRotation = Qt.vector3d(0, 0, 0)
        cameraOrigin.position = Qt.vector3d(campusExtent.centerX, 0, campusExtent.centerZ)
        const size = Math.max(campusExtent.width, campusExtent.depth)
        mapCamera.position = Qt.vector3d(0, size * 0.78, size * 0.82)
        mapCamera.eulerRotation = Qt.vector3d(-42, 0, 0)
    }
    function resetWalkView() {
        const floor = root.inspector.current_floor
        walkCamera.position = Qt.vector3d(floor.startX, floor.elevation + 1.65, floor.startZ)
        walkCamera.eulerRotation = Qt.vector3d(0, floor.startYaw, 0)
        walkCamera.fieldOfView = 67
        root.walkViewKey = root.inspector.inspection_key + ":" + root.inspector.selected_floor
    }
    function syncInspectionHeight() {
        if (!root.inspector.active || !root.wasInspecting ||
            root.inspectionViewKey !== root.inspector.inspection_key || root.inspector.mode === "inside") return
        const b = root.inspector.bounds
        const height = root.inspector.mode === "floor" ? root.inspector.current_floor.elevation :
            b.height / 2 + (root.inspector.mode === "explode" ?
            root.inspector.spread * Math.max(0, root.inspector.floors.length - 1) / 2 : 0)
        cameraOrigin.y = height
    }
    function resetInspectionView() {
        if (root.inspector.mode === "inside") { root.resetWalkView(); return }
        const b = root.inspector.bounds
        const distance = Math.max(35, b.width, b.depth, b.height) *
            (root.inspector.mode === "explode" ? 2.1 : 1.6)
        cameraOrigin.position = Qt.vector3d(0, 0, 0)
        cameraOrigin.eulerRotation = Qt.vector3d(0, 0, 0)
        mapCamera.position = Qt.vector3d(0, distance * 0.85, distance)
        mapCamera.eulerRotation = Qt.vector3d(-38, 0, 0)
        root.syncInspectionHeight()
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
            Math.max(-70, Math.min(70, walkCamera.eulerRotation.x - dy)),
            walkCamera.eulerRotation.y - dx, 0)
    }
    function orbit(dx, dy) {
        cameraOrigin.eulerRotation = Qt.vector3d(
            Math.max(-25, Math.min(30, cameraOrigin.eulerRotation.x + dy)),
            cameraOrigin.eulerRotation.y + dx, 0)
    }
    function panScreen(dx, dy) {
        const yaw = cameraOrigin.eulerRotation.y * Math.PI / 180
        cameraOrigin.position = cameraOrigin.position.plus(Qt.vector3d(
            dx * Math.cos(yaw) + dy * Math.sin(yaw), 0,
            -dx * Math.sin(yaw) + dy * Math.cos(yaw)))
    }
    function keyboardStep(dt) {
        root.mapController.manual_input()
        const forward = (heldKeys[Qt.Key_W] || heldKeys[Qt.Key_Up] ? 1 : 0) -
                        (heldKeys[Qt.Key_S] || heldKeys[Qt.Key_Down] ? 1 : 0)
        const turn = (heldKeys[Qt.Key_D] || heldKeys[Qt.Key_Right] ? 1 : 0) -
                     (heldKeys[Qt.Key_A] || heldKeys[Qt.Key_Left] ? 1 : 0)
        if (inspector.active && inspector.mode === "inside") {
            root.walk(forward * dt * 2)
            root.look(turn * dt * 80, 0)
        } else {
            root.orbit(turn * dt * 80, -forward * dt * 45)
        }
        const zoom = (heldKeys[Qt.Key_Plus] || heldKeys[Qt.Key_Equal] ? 1 : 0) -
                     (heldKeys[Qt.Key_Minus] ? 1 : 0)
        if (zoom) root.mapController.zoom_by(Math.exp(-zoom * dt * 0.65))
    }
    onActiveFocusChanged: if (!activeFocus) heldKeys = ({})
    Connections {
        target: root.mapController
        function onGestureControlsChanged() {
            if (!root.mapController.dwell_enabled) { dwell.stop(); root.pointerProgress = 0 }
        }
    }
    function selectAtScreen(px, py) {
        const hits = view.pickAll(px, py)
        for (let i = 0; i < hits.length; i++) {
            const point = hits[i].scenePosition
            if (inspector.active) {
                const model = hits[i].objectHit
                if (!model || typeof model.inspectionFloor !== "number") continue
                const mode = inspector.mode
                const b = inspector.bounds
                if (mode === "section" &&
                    ((inspector.cut_axis === "x" && point.x > (inspector.cut - 0.5) * b.width) ||
                     (inspector.cut_axis === "z" && point.z > (inspector.cut - 0.5) * b.depth) ||
                     (inspector.cut_axis === "y" && point.y > inspector.cut * b.height)))
                    continue
                if (mode === "dollhouse" && point.x > 0 && point.z > 0)
                    continue
                if (inspector.select_room(model.inspectionFloor, point.x, point.z).length > 0)
                    return true
                continue
            }
            const id = mapController.select_at(point.x, point.y, point.z)
            if (id.length > 0) {
                root.buildingPicked(id)
                return true
            }
        }
        return false
    }

    function confirmAtScreen(px, py) {
        const selected = root.selectAtScreen(px, py)
        root.selectionMessage = selected ?
            (root.inspector.active ? root.inspector.current_floor.label + " 层 · " + root.inspector.room_name :
             "已选中 · " + root.mapController.selected_details.name) :
            "未选中目标 · 移到建筑或房间上再确认"
        selectionFeedbackTimer.restart()
    }

    Keys.onPressed: function(event) {
        if (event.isAutoRepeat) { event.accepted = true; return }
        if (event.key === Qt.Key_F3) {
            root.showStats = !root.showStats
            event.accepted = true
        } else if (event.key === Qt.Key_Space) {
            root.mapController.set_gestures_enabled(!root.mapController.gestures_enabled)
            event.accepted = true
        } else if ([Qt.Key_Escape, Qt.Key_R, Qt.Key_E, Qt.Key_M,
                    Qt.Key_PageUp, Qt.Key_PageDown].indexOf(event.key) >= 0) {
            root.mapController.manual_input()
            if (event.key === Qt.Key_Escape) root.mapController.go_back()
            else if (event.key === Qt.Key_R) root.mapController.reset_camera()
            else if (event.key === Qt.Key_E) root.mapController.enter_structure()
            else if (event.key === Qt.Key_M) root.mapController.cycle_structure_mode()
            else if (inspector.active) inspector.change_floor(event.key === Qt.Key_PageUp ? 1 : -1)
            event.accepted = true
        } else if ([Qt.Key_W, Qt.Key_A, Qt.Key_S, Qt.Key_D, Qt.Key_Up, Qt.Key_Down,
                    Qt.Key_Left, Qt.Key_Right, Qt.Key_Plus, Qt.Key_Equal, Qt.Key_Minus].indexOf(event.key) >= 0) {
            heldKeys = Object.assign({}, heldKeys, { [event.key]: true })
            event.accepted = true
        }
    }
    Keys.onReleased: function(event) {
        if (!event.isAutoRepeat) {
            const next = Object.assign({}, heldKeys)
            delete next[event.key]
            heldKeys = next
        }
    }
    FrameAnimation {
        running: root.activeFocus && Object.keys(root.heldKeys).length > 0
        onTriggered: root.keyboardStep(Math.min(0.05, frameTime))
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
                objectName: "cameraOrigin"
                position: Qt.vector3d(root.campusExtent.centerX, 0, root.campusExtent.centerZ)
                Behavior on y {
                    enabled: root.inspector.active && root.inspector.mode !== "inside"
                    NumberAnimation { duration: 180; easing.type: Easing.OutCubic }
                }
                PerspectiveCamera {
                    id: mapCamera
                    objectName: "mapCamera"
                    position: Qt.vector3d(0, Math.max(root.campusExtent.width, root.campusExtent.depth) * 0.78,
                                           Math.max(root.campusExtent.width, root.campusExtent.depth) * 0.82)
                    eulerRotation.x: -42
                    clipNear: 0.1
                    clipFar: 12000
                    fieldOfView: 48
                    onZChanged: root.mapController.set_navigation_span(Math.max(8, z) * 1.2)
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
        Connections {
            target: root.mapController
            function onResetCameraRequested() {
                if (root.inspector.active) root.resetInspectionView()
                else root.resetCampus()
            }
            function onPanRequested(dx, dz) {
                root.panScreen(dx, dz)
            }
            function onZoomRequested(factor) {
                if (root.inspector.active && root.inspector.mode === "inside") {
                    walkCamera.fieldOfView = Math.max(30, Math.min(90, walkCamera.fieldOfView * factor))
                    return
                }
                const distance = Math.max(root.inspector.active ? 8 : 300,
                                          Math.min(11000, mapCamera.position.z * factor))
                const ratio = distance / mapCamera.position.z
                mapCamera.position = Qt.vector3d(mapCamera.position.x,
                    mapCamera.position.y * ratio, distance)
            }
            function onFocusRequested(x, z, distance) {
                cameraOrigin.eulerRotation = Qt.vector3d(0, 0, 0)
                cameraOrigin.position = Qt.vector3d(x, 0, z)
                mapCamera.position = Qt.vector3d(0, distance * 0.8, distance)
                mapCamera.eulerRotation = Qt.vector3d(-42, 0, 0)
            }
            function onLookRequested(dx, dy) { root.look(dx, dy) }
            function onWalkRequested(distance) { root.walk(distance) }
            function onOrbitRequested(dx, dy) { root.orbit(dx, dy) }
            function onSelectRequested(x, y) {
                dwell.stop()
                root.confirmAtScreen(x * root.width, y * root.height)
                root.pointerSelected = true
            }
            function onPointingChanged(x, y, valid) {
                if (!valid) {
                    pointer.visible = false; root.pointerSelected = false; dwell.stop()
                    root.pointerProgress = 0; return
                }
                const px = x * root.width, py = y * root.height
                const moved = !pointer.visible || Math.hypot(px - root.pointerAnchorX, py - root.pointerAnchorY) > 24
                pointer.x = px - 13; pointer.y = py - 13; pointer.visible = true
                if (moved) {
                    root.pointerAnchorX = px; root.pointerAnchorY = py
                    root.pointerSelected = false; root.pointerProgress = 0
                    root.dwellStarted = Date.now()
                    if (root.mapController.dwell_enabled) dwell.restart()
                }
                else if (!root.pointerSelected && !dwell.running && root.mapController.dwell_enabled) {
                    root.dwellStarted = Date.now(); dwell.restart()
                }
            }
        }
        Connections {
            target: root.inspector
            function onChanged() { root.syncInspectionHeight() }
            function onViewRequested() {
                root.heldKeys = ({})
                root.selectionMessage = ""
                selectionFeedbackTimer.stop()
                if (!root.inspector.active) {
                    if (root.wasInspecting && root.campusViewState) {
                        cameraOrigin.position = root.campusViewState.origin
                        cameraOrigin.eulerRotation = root.campusViewState.rotation
                        mapCamera.position = root.campusViewState.camera
                        mapCamera.eulerRotation = root.campusViewState.pitch
                    } else root.resetCampus()
                    root.wasInspecting = false
                    root.inspectionViewKey = ""
                    root.walkViewKey = ""
                    return
                }
                const newBuilding = !root.wasInspecting || root.inspectionViewKey !== root.inspector.inspection_key
                if (!root.wasInspecting) {
                    root.campusViewState = {origin: cameraOrigin.position,
                        rotation: cameraOrigin.eulerRotation, camera: mapCamera.position,
                        pitch: mapCamera.eulerRotation}
                    root.wasInspecting = true
                }
                if (newBuilding) {
                    root.inspectionViewKey = root.inspector.inspection_key
                    root.walkViewKey = ""
                    root.resetInspectionView()
                }
                if (root.inspector.mode === "inside") {
                    if (root.walkViewKey !== root.inspector.inspection_key + ":" + root.inspector.selected_floor)
                        root.resetWalkView()
                } else root.syncInspectionHeight()
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton | Qt.MiddleButton
        hoverEnabled: false
        property real lastX: 0
        property real lastY: 0
        property real pressX: 0
        property real pressY: 0
        onPressed: function(mouse) {
            lastX = pressX = mouse.x; lastY = pressY = mouse.y
            root.forceActiveFocus(); root.mapController.manual_input()
        }
        onPositionChanged: function(mouse) {
            if (!pressed) return
            root.mapController.manual_input()
            const dx = mouse.x - lastX, dy = mouse.y - lastY
            if (root.inspector.active && root.inspector.mode === "inside") {
                if (mouse.buttons & Qt.RightButton) root.look(dx * 0.2, dy * 0.2)
            } else if ((mouse.buttons & (Qt.RightButton | Qt.MiddleButton)) || (mouse.modifiers & Qt.ControlModifier)) {
                root.panScreen(-dx / root.width * mapCamera.z, -dy / root.height * mapCamera.z)
            } else root.orbit(-dx * 0.18, -dy * 0.18)
            lastX = mouse.x; lastY = mouse.y
        }
        onReleased: function(mouse) {
            if (mouse.button === Qt.LeftButton && Math.hypot(mouse.x - pressX, mouse.y - pressY) < 8)
                root.confirmAtScreen(mouse.x, mouse.y)
        }
        onDoubleClicked: function(mouse) {
            if (mouse.button === Qt.LeftButton) root.mapController.enter_structure()
        }
        onWheel: function(wheel) {
            root.forceActiveFocus(); root.mapController.manual_input()
            const delta = wheel.pixelDelta.y || wheel.angleDelta.y
            if (root.inspector.active && root.inspector.mode === "inside")
                root.walk(Math.max(-0.8, Math.min(0.8, delta * 0.004)))
            else root.mapController.zoom_by(Math.exp(-Math.max(-240, Math.min(240, delta)) * 0.0015))
        }
    }
    PinchHandler {
        target: null
        onActiveChanged: if (active) { root.forceActiveFocus(); root.mapController.manual_input() }
        onScaleChanged: function(delta) {
            root.mapController.manual_input()
            root.mapController.zoom_by(1 / delta)
        }
        onRotationChanged: function(delta) {
            root.mapController.manual_input()
            if (root.inspector.active && root.inspector.mode === "inside") root.look(-delta, 0)
            else root.orbit(-delta, 0)
        }
        onTranslationChanged: function(delta) {
            root.mapController.manual_input()
            if (root.inspector.active && root.inspector.mode === "inside") root.look(delta.x * 0.2, delta.y * 0.2)
            else root.panScreen(-delta.x / root.width * mapCamera.z, -delta.y / root.height * mapCamera.z)
        }
    }
    Rectangle {
        id: pointer
        visible: false
        width: 26; height: 26; radius: 13
        color: "#00000000"; border.width: 3; border.color: "#ffcc4c"
        Canvas {
            id: pointerRing
            anchors.fill: parent
            onPaint: {
                const c = getContext("2d")
                c.clearRect(0, 0, width, height)
                c.strokeStyle = "#faffec"; c.lineWidth = 3
                c.beginPath(); c.arc(13, 13, 10, -Math.PI / 2,
                    -Math.PI / 2 + root.pointerProgress * Math.PI * 2); c.stroke()
            }
            Connections { target: root; function onPointerProgressChanged() { pointerRing.requestPaint() } }
        }
    }
    Timer {
        id: dwell
        interval: 850
        onTriggered: if (pointer.visible) {
            root.confirmAtScreen(pointer.x + 13, pointer.y + 13)
            root.pointerSelected = true
            root.pointerProgress = 1
        }
    }
    Timer {
        id: selectionFeedbackTimer
        interval: 1800
        onTriggered: root.selectionMessage = ""
    }
    Timer {
        interval: 32; repeat: true; running: dwell.running
        onTriggered: root.pointerProgress = Math.min(1, (Date.now() - root.dwellStarted) / dwell.interval)
    }
    Rectangle {
        anchors.left: parent.left; anchors.bottom: parent.bottom; anchors.margins: 14
        width: Math.min(root.width - 28, 430); height: root.selectionMessage ? 84 : 64; radius: 8
        color: "#dc182c37"
        Text {
            anchors.fill: parent; anchors.margins: 10
            color: "#fff4d8"; font.pixelSize: 12; elide: Text.ElideRight
            text: (!root.mapController.gestures_enabled ? "手势暂停 · 空格恢复 · 键鼠可用" :
                   root.mapController.gesture_feedback.label) + "\n" + root.mapController.gesture_status +
                  (root.selectionMessage ? "\n" + root.selectionMessage : "")
        }
        Rectangle {
            anchors.left: parent.left; anchors.bottom: parent.bottom; height: 3; radius: 2
            width: parent.width * (root.mapController.gesture_feedback.progress || 0)
            color: "#ffce78"
        }
    }
    Row {
        anchors.left: parent.left; anchors.top: parent.top; anchors.margins: 14; spacing: 8
        Button {
            text: root.gestureWorker.running ? "停止摄像头" : "启动手势"
            onClicked: {
                root.gestureWorker.running ? root.gestureWorker.stop() : root.gestureWorker.start()
                root.forceActiveFocus()
            }
        }
        Button {
            text: root.mapController.gestures_enabled ? "暂停控制" : "恢复控制"
            onClicked: {
                root.mapController.set_gestures_enabled(!root.mapController.gestures_enabled)
                root.forceActiveFocus()
            }
        }
        Button { text: "手势设置"; onClicked: root.gestureSettingsRequested() }
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
