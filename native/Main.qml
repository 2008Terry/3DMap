import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 1440
    height: 900
    minimumWidth: 1050
    minimumHeight: 660
    title: "Michigan Campus Atlas · 本地 3D"
    color: "#111a20"
    font.pixelSize: 14
    palette.window: "#182630"
    palette.windowText: "#e7efeb"
    palette.button: "#29434f"
    palette.buttonText: "#f0f3ed"
    palette.base: "#10212b"
    palette.text: "#f0f3ed"
    palette.highlight: "#d4a749"
    palette.highlightedText: "#13212a"
    property var searchResults: []
    property var selectedBuilding: mapControllerObject.selected_details
    property var modes: [
        {key: "dollhouse", name: "剖开"},
        {key: "section", name: "切片"},
        {key: "xray", name: "透视"},
        {key: "explode", name: "拆层"},
        {key: "floor", name: "单层"},
        {key: "inside", name: "进入"}
    ]
    onActiveChanged: {
        mapControllerObject.set_window_active(active && !planDialog.visible)
        if (!active) mapScene.heldKeys = ({})
    }

    RowLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 18
        Rectangle {
            Layout.preferredWidth: 342
            Layout.fillHeight: true
            radius: 14
            color: "#182630"
            border.color: "#344a55"
            Flickable {
                id: sidebarScroll
                anchors.fill: parent
                anchors.margins: 17
                clip: true
                contentWidth: width
                contentHeight: panel.height
                ScrollBar.vertical: ScrollBar { }
                Column {
                    id: panel
                    width: parent.width
                    spacing: 11
                    Label {
                        width: parent.width
                        text: "MICHIGAN · CAMPUS ATLAS"
                        font.pixelSize: 19
                        font.weight: Font.DemiBold
                        color: "#f5f1e8"
                        wrapMode: Text.WordWrap
                    }
                    Label {
                        width: parent.width
                        text: campusBuildings.length + " 栋建筑 · Central + North · 离线运行"
                        color: "#afc4c8"
                        font.pixelSize: 12
                    }
                    Row {
                        spacing: 6
                        Button { text: "Central"; onClicked: mapControllerObject.focus_campus("Central") }
                        Button { text: "North"; onClicked: mapControllerObject.focus_campus("North") }
                        Button {
                            text: "全校"
                            onClicked: { inspectorObject.close(); mapControllerObject.reset_camera() }
                        }
                    }
                    TextField {
                        id: searchField
                        width: parent.width
                        placeholderText: "搜索楼名或 Facility ID"
                        color: "#eef3ef"
                        placeholderTextColor: "#9baeb5"
                        onTextChanged: window.searchResults = mapControllerObject.search(text)
                    }
                    ListView {
                        id: searchList
                        width: parent.width
                        height: searchField.text.length > 0 ? Math.min(180, count * 44) : 0
                        clip: true
                        model: window.searchResults
                        delegate: ItemDelegate {
                            required property var modelData
                            width: searchList.width
                            height: 44
                            text: modelData.name + " · " + modelData.campus
                            onClicked: {
                                mapControllerObject.focus_building(modelData.id)
                                searchField.text = ""
                            }
                        }
                    }
                    Rectangle { width: parent.width; height: 1; color: "#3a4d56" }
                    Label {
                        width: parent.width
                        text: inspectorObject.active ? inspectorObject.name
                             : Object.keys(window.selectedBuilding).length ? window.selectedBuilding.name : "选择一栋建筑"
                        color: "#fff8e6"
                        font.pixelSize: 17
                        font.weight: Font.DemiBold
                        wrapMode: Text.WordWrap
                    }
                    BuildingDetails {
                        width: parent.width
                        height: !inspectorObject.active && Object.keys(window.selectedBuilding).length ? 250 : 0
                        visible: height > 0
                        building: Object.keys(window.selectedBuilding).length ? window.selectedBuilding : null
                    }
                    Button {
                        width: parent.width
                        text: inspectorObject.active ? "返回校园" : "打开建筑结构"
                        enabled: inspectorObject.active || Object.keys(window.selectedBuilding).length > 0
                        onClicked: inspectorObject.active ? inspectorObject.close() : inspectorObject.open()
                    }
                    Image {
                        width: parent.width
                        height: inspectorObject.photo_url ? 140 : 0
                        visible: height > 0
                        source: inspectorObject.photo_url
                        fillMode: Image.PreserveAspectFit
                        asynchronous: true
                    }
                    Label {
                        text: "参考照片：University of Michigan Library · CC-BY"
                        visible: inspectorObject.photo_url.length > 0
                        color: "#a7bdc4"
                        font.pixelSize: 10
                    }
                    Repeater {
                        model: window.selectedBuilding.nearbyStops || []
                        delegate: Label {
                            required property var modelData
                            width: panel.width
                            text: "公交 · " + modelData.name + " · " + modelData.routes.join(", ") +
                                  " · 直线约 " + modelData.distance + " m（静态站点资料）"
                            color: "#b2c5c8"
                            font.pixelSize: 11
                            wrapMode: Text.WordWrap
                        }
                    }
                    Column {
                        width: parent.width
                        spacing: 9
                        visible: inspectorObject.active
                        Label {
                            width: parent.width
                            text: inspectorObject.evidence
                            color: "#f6c777"
                            font.pixelSize: 11
                            wrapMode: Text.WordWrap
                        }
                        Flow {
                            width: parent.width
                            spacing: 5
                            Repeater {
                                model: window.modes
                                delegate: Button {
                                    required property var modelData
                                    text: modelData.name
                                    highlighted: inspectorObject.mode === modelData.key
                                    onClicked: inspectorObject.set_mode(modelData.key)
                                }
                            }
                        }
                        ComboBox {
                            width: parent.width
                            visible: inspectorObject.wings.length > 1
                            model: inspectorObject.wings
                            currentIndex: inspectorObject.wings.indexOf(inspectorObject.wing)
                            onActivated: inspectorObject.set_wing(currentText)
                        }
                        Row {
                            spacing: 6
                            Button { text: "上一层"; onClicked: inspectorObject.change_floor(1) }
                            Label {
                                text: inspectorObject.current_floor.label || ""
                                color: "#f3f3ed"
                                anchors.verticalCenter: parent.verticalCenter
                            }
                            Button { text: "下一层"; onClicked: inspectorObject.change_floor(-1) }
                        }
                        Label {
                            width: parent.width
                            text: (inspectorObject.current_floor.name || "") +
                                  (inspectorObject.bounds.scope ? " · " + inspectorObject.bounds.scope : "")
                            color: "#bed2d0"
                            wrapMode: Text.WordWrap
                            font.pixelSize: 11
                        }
                        Row {
                            spacing: 5
                            visible: inspectorObject.mode === "section" || inspectorObject.mode === "dollhouse"
                            Label { text: "切面"; color: "#f1eee4" }
                            ComboBox {
                                width: 72
                                model: ["y", "x", "z"]
                                onActivated: inspectorObject.set_cut_axis(currentText)
                            }
                            Slider {
                                width: 170
                                from: 0.02; to: 0.98
                                value: inspectorObject.cut
                                onMoved: inspectorObject.set_cut(value)
                            }
                        }
                        Row {
                            spacing: 6
                            visible: inspectorObject.mode === "explode" || inspectorObject.mode === "xray"
                            Label {
                                text: inspectorObject.mode === "explode" ? "层距" : "外壳"
                                color: "#f1eee4"
                            }
                            Slider {
                                width: 224
                                from: inspectorObject.mode === "explode" ? 0 : 0.03
                                to: inspectorObject.mode === "explode" ? 24 : 0.5
                                value: inspectorObject.mode === "explode"
                                       ? inspectorObject.spread : inspectorObject.shell_opacity
                                onMoved: inspectorObject.mode === "explode"
                                         ? inspectorObject.set_spread(value)
                                         : inspectorObject.set_shell_opacity(value)
                            }
                        }
                        CheckBox {
                            text: "显示家具"
                            checked: inspectorObject.show_furniture
                            onToggled: inspectorObject.set_furniture(checked)
                        }
                        Label {
                            width: parent.width
                            text: inspectorObject.room_name
                            color: "#ffcc74"
                            wrapMode: Text.WordWrap
                        }
                        Image {
                            width: parent.width
                            height: inspectorObject.plan_url ? 170 : 0
                            visible: height > 0
                            source: inspectorObject.plan_url
                            fillMode: Image.PreserveAspectFit
                            asynchronous: true
                        }
                        Button {
                            text: "放大官方楼层图"
                            visible: inspectorObject.plan_url.length > 0
                            onClicked: planDialog.open()
                        }
                        Label {
                            width: parent.width
                            text: inspectorObject.plan_source ? "官方楼层图：" + inspectorObject.plan_source : ""
                            visible: text.length > 0
                            color: "#a9c0c6"
                            font.pixelSize: 10
                            wrapMode: Text.WrapAnywhere
                        }
                        Repeater {
                            model: inspectorObject.rooms
                            delegate: Label {
                                required property var modelData
                                width: panel.width
                                text: "• " + modelData.name +
                                      (modelData.source_named ? " · 官方名称" : " · 示意")
                                color: "#d7e0dc"
                                font.pixelSize: 11
                                wrapMode: Text.WordWrap
                            }
                        }
                    }
                    Rectangle { width: parent.width; height: 1; color: "#3a4d56" }
                    Row {
                        spacing: 5
                        Button { text: "−"; onClicked: mapControllerObject.zoom_by(1.2) }
                        Button { text: "+"; onClicked: mapControllerObject.zoom_by(0.82) }
                        Button { text: "重置视角"; onClicked: mapControllerObject.reset_camera() }
                    }
                    Column {
                        id: gestureSettings
                        width: parent.width
                        spacing: 9
                        ComboBox {
                            width: parent.width
                            model: ["摄像头 1", "摄像头 2", "摄像头 3", "摄像头 4", "摄像头 5", "摄像头 6"]
                            enabled: !gestureWorkerObject.running
                            currentIndex: gestureWorkerObject.camera_index
                            onActivated: gestureWorkerObject.set_camera_index(currentIndex)
                        }
                        Row {
                            spacing: 6
                            Button {
                                text: "启动手势"
                                enabled: !gestureWorkerObject.running
                                onClicked: gestureWorkerObject.start()
                            }
                            Button {
                                text: gestureWorkerObject.stopping ? "停止中" : "停止"
                                enabled: gestureWorkerObject.running && !gestureWorkerObject.stopping
                                onClicked: gestureWorkerObject.stop()
                            }
                            Button {
                                text: mapControllerObject.gestures_enabled ? "暂停控制" : "恢复控制"
                                onClicked: mapControllerObject.set_gestures_enabled(!mapControllerObject.gestures_enabled)
                            }
                        }
                        Rectangle {
                            width: parent.width; height: 146; radius: 9
                            color: "#10212b"; border.color: "#36515a"
                            Canvas {
                                id: handPreview
                                anchors.fill: parent; anchors.margins: 12
                                property var points: mapControllerObject.gesture_feedback.points || []
                                onPointsChanged: requestPaint()
                                onPaint: {
                                    const ctx = getContext("2d")
                                    ctx.clearRect(0, 0, width, height)
                                    if (points.length !== 21) {
                                        ctx.fillStyle = "#b0c4c9"; ctx.font = "12px sans-serif"
                                        ctx.fillText("手放在镜头前 · 普通摄像头 · 单手", 6, height / 2)
                                        return
                                    }
                                    const edges = [[0,1,2,3,4],[0,5,6,7,8],[5,9,10,11,12],
                                                   [9,13,14,15,16],[13,17,18,19,20],[17,0]]
                                    const aspect = mapControllerObject.gesture_feedback.imageAspect || 0.75
                                    const imageWidth = Math.min(width, height / aspect)
                                    const imageHeight = imageWidth * aspect
                                    const offsetX = (width - imageWidth) / 2
                                    const offsetY = (height - imageHeight) / 2
                                    ctx.strokeStyle = "#77b9b8"; ctx.lineWidth = 2
                                    for (let e of edges) {
                                        ctx.beginPath()
                                        for (let j = 0; j < e.length; j++) {
                                            const p = points[e[j]]
                                            if (!j) ctx.moveTo(offsetX + p.x * imageWidth, offsetY + p.y * imageHeight)
                                            else ctx.lineTo(offsetX + p.x * imageWidth, offsetY + p.y * imageHeight)
                                        }
                                        ctx.stroke()
                                    }
                                    ctx.fillStyle = "#ffcd77"
                                    for (let p of points) {
                                        ctx.beginPath(); ctx.arc(offsetX + p.x * imageWidth, offsetY + p.y * imageHeight, 2.6, 0, Math.PI*2); ctx.fill()
                                    }
                                }
                            }
                        }
                        Label {
                            width: parent.width
                            text: mapControllerObject.gesture_feedback.label || "等待手势"
                            color: "#ffce78"; font.pixelSize: 13
                        }
                        ProgressBar {
                            width: parent.width
                            value: mapControllerObject.gesture_feedback.progress || 0
                        }
                        Label {
                            width: parent.width
                            text: "识别更新 " + (gestureWorkerObject.metrics.fps || 0) + " Hz · 处理约 " +
                                  (gestureWorkerObject.metrics.latencyMs || 0) + " ms"
                            color: "#9fb8bf"; font.pixelSize: 10
                        }
                        Label {
                            width: parent.width
                            text: mapControllerObject.gesture_status
                            color: "#a4c0c5"
                            font.pixelSize: 11
                            wrapMode: Text.WordWrap
                        }
                        Label {
                            width: parent.width
                            text: inspectorObject.mode === "inside"
                                  ? "手掌/双指环顾 · 拇指持续走动 · Esc 返回"
                                  : inspectorObject.mode === "section" && inspectorObject.active
                                  ? "食指选房间 · 捏合拖动切面 · 双指旋转/张合缩放"
                                  : inspectorObject.mode === "explode" && inspectorObject.active
                                  ? "食指选房间 · 捏合上下调层距 · 双指旋转/张合缩放"
                                  : inspectorObject.mode === "xray" && inspectorObject.active
                                  ? "食指选房间 · 捏合上下调透视 · 双指旋转/张合缩放"
                                  : "食指指向 + 捏合确认 · 手掌/捏合拖动 · 双指旋转/张合缩放"
                            color: "#9eafad"
                            font.pixelSize: 10
                            wrapMode: Text.WordWrap
                        }
                        Label {
                            width: parent.width
                            text: "握拳/拇指向右停留：进入 · 三指：切换视图\n拇指向左停留：返回 · 拇指上下：缩放/换层\n拇指+食指+小指停留：暂停/恢复控制\n空格：暂停 · E：进入 · M：视图 · R：复位\nWASD/方向键持续操作 · PgUp/PgDn 换层"
                            color: "#bbccc9"; font.pixelSize: 11; wrapMode: Text.WordWrap
                        }
                        CheckBox {
                            text: "食指停留也可选择"
                            checked: mapControllerObject.dwell_enabled
                            onToggled: mapControllerObject.set_dwell_enabled(checked)
                        }
                        Label { text: "移动灵敏度"; color: "#b2c7ca"; font.pixelSize: 11 }
                        Slider {
                            width: parent.width; from: 0.5; to: 1.75
                            value: mapControllerObject.gesture_sensitivity
                            onMoved: mapControllerObject.set_gesture_sensitivity(value)
                        }
                        Label { text: "指向操作范围（小范围减少伸手）"; color: "#b2c7ca"; font.pixelSize: 11 }
                        Slider {
                            width: parent.width; from: 0.55; to: 1
                            value: mapControllerObject.comfort_range
                            onMoved: mapControllerObject.set_comfort_range(value)
                        }
                        Row {
                            spacing: 6
                            Button { text: "此位置设为中心"; onClicked: mapControllerObject.calibrate_pointer() }
                            Button { text: "恢复中心"; onClicked: mapControllerObject.reset_pointer_center() }
                        }
                    }
                    Label {
                        width: parent.width
                        text: environmentSummary + " · F3 查看性能"
                        color: "#8fa3a5"
                        font.pixelSize: 10
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 15
            color: "#dbe5e4"
            clip: true
            MapScene {
                id: mapScene
                anchors.fill: parent
                campusExtent: campusBounds
                centralGeometry: geometryCentral
                northGeometry: geometryNorth
                featuredGeometries: geometryFeatured
                environmentGeometries: geometryEnvironment
                facadeGeometry: geometryFacades
                mapController: mapControllerObject
                selectionOverlay: selectionOverlayState
                inspector: inspectorObject
                gestureWorker: gestureWorkerObject
                onGestureSettingsRequested: sidebarScroll.contentY = Math.min(gestureSettings.y,
                    Math.max(0, sidebarScroll.contentHeight - sidebarScroll.height))
            }
        }
    }
    Dialog {
        id: planDialog
        title: "官方参考图 · University of Michigan Library"
        modal: true
        anchors.centerIn: parent
        width: Math.min(window.width - 60, 1000)
        height: window.height - 70
        standardButtons: Dialog.Close
        onVisibleChanged: mapControllerObject.set_window_active(window.active && !visible)
        contentItem: Flickable {
            clip: true
            contentWidth: width * 1.6
            contentHeight: height * 1.6
            Image {
                width: parent.contentWidth
                height: parent.contentHeight
                source: inspectorObject.plan_url
                fillMode: Image.PreserveAspectFit
            }
            ScrollBar.vertical: ScrollBar { }
            ScrollBar.horizontal: ScrollBar { }
        }
    }
}
