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
                            Button { text: "上一层"; onClicked: inspectorObject.change_floor(-1) }
                            Label {
                                text: inspectorObject.current_floor.label || ""
                                color: "#f3f3ed"
                                anchors.verticalCenter: parent.verticalCenter
                            }
                            Button { text: "下一层"; onClicked: inspectorObject.change_floor(1) }
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
                    Row {
                        spacing: 6
                        Button {
                            text: "启动手势"
                            enabled: !gestureWorkerObject.running
                            onClicked: gestureWorkerObject.start()
                        }
                        Button {
                            text: "停止"
                            enabled: gestureWorkerObject.running
                            onClicked: gestureWorkerObject.stop()
                        }
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
                              ? "W/S 移动 · A/D 转向 · 右键拖动环顾 · 拇指前后移动"
                              : "拖动旋转 · 滚轮缩放 · 食指停留选择 · 握拳进入"
                        color: "#9eafad"
                        font.pixelSize: 10
                        wrapMode: Text.WordWrap
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
