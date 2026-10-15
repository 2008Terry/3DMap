import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    objectName: "structureExplorer"
    required property var state
    required property var inspector
    color: "#102b35"
    visible: state.active
    focus: visible
    readonly property string graphicsApi: overview.graphicsApi
    readonly property real fps: overview.fps
    onVisibleChanged: if (visible) forceActiveFocus()
    // Empty-space input must not reach the covered campus sidebar.
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.AllButtons
        onWheel: function(wheel) { wheel.accepted = true }
    }
    Keys.onPressed: function(event) {
        if (event.key === Qt.Key_Escape) { state.close(); event.accepted = true }
        else if (event.key === Qt.Key_PageUp) { state.select_floor(Math.min(state.floors.length - 1, state.floor_index + 1)); event.accepted = true }
        else if (event.key === Qt.Key_PageDown) { state.select_floor(Math.max(0, state.floor_index - 1)); event.accepted = true }
        else if (event.key === Qt.Key_R) { overview.reset(); event.accepted = true }
    }

    RowLayout {
        id: heading
        anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right
        anchors.margins: 16
        height: 48
        spacing: 16
        Button { text: "← 返回建筑"; onClicked: root.state.close() }
        Column {
            Layout.fillWidth: true
            spacing: 3
            Label { text: root.inspector.name + " · 结构透视"; font.pixelSize: 21; color: "#f2f1e8" }
            Label { text: "展开楼层 / 局部开墙 / 同屏不同视线"; color: "#97bdbe"; font.pixelSize: 12 }
        }
        ComboBox {
            visible: root.inspector.wings.length > 1
            model: root.inspector.wings
            currentIndex: root.inspector.wings.indexOf(root.inspector.wing)
            onActivated: root.inspector.set_wing(currentText)
        }
        Label { text: "同一结构 · 不同视线"; color: "#91aeb2"; font.pixelSize: 11 }
    }
    RowLayout {
        anchors.top: heading.bottom; anchors.bottom: notice.top
        anchors.left: parent.left; anchors.right: parent.right
        anchors.margins: 16
        spacing: 14
        Rectangle {
            Layout.preferredWidth: 250
            Layout.fillHeight: true
            color: "#183c47"; radius: 10
            ColumnLayout {
                anchors.fill: parent; anchors.margins: 12
                spacing: 8
                Label { text: "楼层与连接"; color: "#e8f1eb"; font.pixelSize: 16 }
                Flow {
                    Layout.fillWidth: true
                    Layout.preferredHeight: childrenRect.height
                    spacing: 4
                    Repeater {
                        model: root.state.floors
                        delegate: Button {
                            required property var modelData
                            text: modelData.label.replace("Basement", "B")
                            width: 38; height: 29
                            font.pixelSize: 11
                            highlighted: root.state.floor_index === modelData.index
                            onClicked: root.state.select_floor(modelData.index)
                        }
                    }
                }
                Label {
                    text: (root.inspector.current_floor.label || "") + " 层 · " + root.state.spaces.length + " 个空间"
                    color: "#e7bd6b"; font.pixelSize: 13
                }
                Rectangle {
                    Layout.fillWidth: true; Layout.preferredHeight: Math.min(225, root.height * 0.25)
                    color: "#e3ebe3"; radius: 5; clip: true
                    StructurePlan { anchors.fill: parent; state: root.state }
                }
                Label {
                    Layout.fillWidth: true
                    text: "蓝绿：通道与竖向连接\n橙色：选中空间的可走连接"
                    color: "#a3c5c5"; font.pixelSize: 11
                }
                Label {
                    Layout.fillWidth: true
                    text: root.state.selected_space.name || "点平面图或空间，查看连接"
                    color: "#f1cc7e"; font.pixelSize: 13; wrapMode: Text.WordWrap
                }
                Label {
                    Layout.fillWidth: true
                    visible: root.state.selected_space.id !== undefined
                    text: root.state.route_points.length > 1 ? "可走区域连通 · 路线已绕开墙体" : "未找到连通路径"
                    color: root.state.route_points.length > 1 ? "#9ed4c6" : "#f1a47a"
                    font.pixelSize: 11; wrapMode: Text.WordWrap
                }
                ListView {
                    Layout.fillWidth: true; Layout.fillHeight: true
                    clip: true; spacing: 3
                    model: root.state.spaces
                    ScrollBar.vertical: ScrollBar { }
                    delegate: ItemDelegate {
                        required property var modelData
                        width: ListView.view.width
                        height: 42
                        highlighted: root.state.selected_space.id === modelData.id
                        text: (modelData.index + 1) + ". " + modelData.name
                        font.pixelSize: 11
                        contentItem: Label {
                            text: parent.text
                            color: parent.highlighted ? "#253638" : "#dbe9e5"
                            font: parent.font
                            wrapMode: Text.WordWrap
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                        }
                        onClicked: root.state.select_space(modelData.index)
                    }
                }
            }
        }
        ColumnLayout {
            Layout.fillWidth: true; Layout.fillHeight: true
            spacing: 10
            RowLayout {
                Layout.fillWidth: true
                Label { text: "展开"; color: "#bed7d1"; font.pixelSize: 12 }
                Slider {
                    Layout.preferredWidth: 150; from: 0; to: 1; value: root.state.unfold
                    onMoved: root.state.set_unfold(value)
                }
                CheckBox { text: "局部切壁"; checked: root.state.cut_enabled; onToggled: root.state.set_cut(checked) }
                CheckBox { text: "家具"; checked: root.state.furniture; onToggled: root.state.set_furniture(checked) }
                Item { Layout.fillWidth: true }
                Button { text: "复位"; onClicked: overview.reset() }
            }
            Rectangle {
                Layout.fillWidth: true; Layout.fillHeight: true
                Layout.preferredHeight: 500
                color: "#e2e8e3"; radius: 8; clip: true
                StructureViewport {
                    id: overview
                    objectName: "structureOverview"
                    anchors.fill: parent
                    state: root.state; inspector: root.inspector
                    overview: true
                }
                Rectangle {
                    anchors.top: parent.top; anchors.left: parent.left; anchors.margins: 10
                    width: overviewCaption.width + 16; height: 26; radius: 5; color: "#e91d3d46"
                    Label { id: overviewCaption; anchors.centerIn: parent; text: "全楼 · 蓝绿线保留层间对应"; font.pixelSize: 11; color: "#dcebe6" }
                }
                Label {
                    anchors.bottom: parent.bottom; anchors.right: parent.right; anchors.margins: 10
                    text: "拖动旋转 · 滚轮缩放 · 双击复位"; font.pixelSize: 11; color: "#526d6b"
                }
            }
            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: Math.max(200, root.height * 0.27)
                spacing: 10
                Repeater {
                    model: root.state.portals
                    delegate: Rectangle {
                        required property var modelData
                        Layout.fillWidth: true; Layout.fillHeight: true
                        color: "#e2e8e3"; radius: 8; clip: true
                        StructureViewport {
                            objectName: modelData.floor === root.state.floor_index ? "structurePortalCurrent" : "structurePortalAdjacent"
                            anchors.fill: parent; anchors.topMargin: 30
                            state: root.state; inspector: root.inspector
                            overview: false
                            floorIndex: modelData.floor
                            yaw: root.inspector.bounds.depth > root.inspector.bounds.width
                                 ? (modelData.yaw < 0 ? -85 : 85) : modelData.yaw
                        }
                        Rectangle {
                            anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right
                            height: 30; color: "#24515b"
                            Label {
                                anchors.left: parent.left; anchors.leftMargin: 10; anchors.verticalCenter: parent.verticalCenter
                                text: (root.state.floors[modelData.floor] || {}).label + " 层 · " + modelData.title
                                color: "#deede6"; font.pixelSize: 11
                            }
                            MouseArea { anchors.fill: parent; onClicked: root.state.select_floor(modelData.floor) }
                        }
                    }
                }
            }
        }
    }
    Label {
        id: notice
        anchors.left: parent.left; anchors.right: parent.right; anchors.bottom: parent.bottom
        anchors.margins: 16
        text: root.inspector.evidence + " · 连接依据示意墙体的可走区域；蓝绿竖线为示意楼梯连接。PgUp/PgDn 换层，Esc 返回。"
        color: "#d5bc83"; font.pixelSize: 11; wrapMode: Text.WordWrap
    }
}
