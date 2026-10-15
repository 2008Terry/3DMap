import QtQuick
import QtQuick3D
import QtQuick.Controls

Item {
    id: root
    required property var state
    required property var inspector
    property bool overview: true
    property int floorIndex: state.floor_index
    property real yaw: overview ? 32 : -45
    property real pitch: overview ? 38 : 63
    property real zoom: 1
    readonly property string graphicsApi: view.renderStats.graphicsApiName
    readonly property real fps: view.renderStats.fps
    property int projectionRevision: 0

    function reset() { yaw = overview ? 32 : -45; pitch = overview ? 38 : 63; zoom = 1 }
    function projectPoint(x, y, z) { return view.mapFrom3DScene(Qt.vector3d(x, y, z)) }
    function fit() {
        const b = overview ? state.bounds : inspector.bounds
        const h = overview ? b.height : 3.6
        const half = 24 * Math.PI / 180
        const horizontal = Math.atan(Math.tan(half) * Math.max(1, width) / Math.max(1, height))
        const cy = Math.cos(yaw * Math.PI / 180), sy = Math.sin(yaw * Math.PI / 180)
        const cp = Math.cos(pitch * Math.PI / 180), sp = Math.sin(pitch * Math.PI / 180)
        let distance = 1
        for (let x of [-b.width / 2, b.width / 2])
            for (let y of [-h / 2, h / 2])
                for (let z of [-b.depth / 2, b.depth / 2]) {
                    const vx = x * cy - z * sy, vz = x * sy + z * cy
                    const vy = y * cp - vz * sp, toward = y * sp + vz * cp
                    distance = Math.max(distance, toward + Math.abs(vx) / Math.tan(horizontal),
                                        toward + Math.abs(vy) / Math.tan(half))
                }
        return distance * 1.1 * zoom
    }
    function pick(px, py) {
        const nearPoint = view.mapTo3DScene(Qt.vector3d(px, py, 0))
        const farPoint = view.mapTo3DScene(Qt.vector3d(px, py, 1000))
        const hit = state.ray_hit(nearPoint, farPoint.minus(nearPoint), overview, floorIndex, yaw)
        if (hit.floor === undefined) return
        state.select_floor(hit.floor)
        if (hit.surface !== "walls") state.pick_plan(hit.x, hit.z)
    }
    View3D {
        id: view
        anchors.fill: parent
        camera: camera
        renderStats.extendedDataCollectionEnabled: true
        environment: SceneEnvironment {
            backgroundMode: SceneEnvironment.Color
            clearColor: "#e2e8e3"
            antialiasingMode: SceneEnvironment.MSAA
            antialiasingQuality: SceneEnvironment.Medium
        }
        Node {
            id: origin
            position: root.overview ? Qt.vector3d(root.state.bounds.centerX || 0, root.state.bounds.centerY || 0, 0)
                                    : Qt.vector3d(0, 1.5, 0)
            eulerRotation.y: root.yaw
            PerspectiveCamera {
                id: camera
                clipNear: 0.05
                clipFar: 12000
                fieldOfView: 48
                readonly property real distance: root.fit()
                position: Qt.vector3d(0, distance * Math.sin(root.pitch * Math.PI / 180),
                                       distance * Math.cos(root.pitch * Math.PI / 180))
                eulerRotation.x: -root.pitch
            }
        }
        DirectionalLight {
            eulerRotation: Qt.vector3d(-45, -25, 0)
            brightness: 0.9
            ambientColor: "#b7c5bf"
        }
        StructureScene {
            state: root.state
            overview: root.overview
            floorIndex: root.floorIndex
            viewYaw: root.yaw
        }
    }
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        property real downX
        property real downY
        property real lastX
        property real lastY
        onPressed: function(mouse) { downX = lastX = mouse.x; downY = lastY = mouse.y }
        onPositionChanged: function(mouse) {
            if (pressed) {
                root.yaw += (mouse.x - lastX) * 0.35
                root.pitch = Math.max(16, Math.min(85, root.pitch + (mouse.y - lastY) * 0.25))
                lastX = mouse.x; lastY = mouse.y
            }
        }
        onReleased: function(mouse) { if (Math.hypot(mouse.x - downX, mouse.y - downY) < 5) root.pick(mouse.x, mouse.y) }
        onWheel: function(wheel) { root.zoom = Math.max(0.25, Math.min(2.5, root.zoom * Math.exp(-wheel.angleDelta.y / 1200))) }
        onDoubleClicked: root.reset()
    }
    FrameAnimation {
        running: root.visible && root.overview && root.state.active
        onTriggered: root.projectionRevision++
    }
    Repeater {
        model: root.overview ? root.state.floors : []
        delegate: Button {
            required property var modelData
            readonly property var projected: {
                const revision = root.projectionRevision, bounds = root.state.bounds
                const p = root.state.floor_position(modelData.index)
                return view.mapFrom3DScene(Qt.vector3d(p.x - root.inspector.bounds.width / 2, p.y + 0.3, 0))
            }
            x: Math.max(4, Math.min(root.width - width - 4, projected.x - width))
            y: Math.max(4, Math.min(root.height - height - 4, projected.y - height / 2))
            visible: projected.z > 0
            text: modelData.label.replace("Basement", "B") + " 层"
            width: 48; height: 24
            font.pixelSize: 11
            highlighted: modelData.index === root.state.floor_index
            onClicked: root.state.select_floor(modelData.index)
        }
    }
}
