import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root
    property var building: null

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Label {
            Layout.fillWidth: true
            text: root.building ? root.building.name : "Building details"
            color: "#f3f4f0"
            font.pixelSize: 19
            font.weight: Font.DemiBold
            wrapMode: Text.WordWrap
        }
        Label {
            Layout.fillWidth: true
            visible: !!root.building
            text: root.building ? root.building.campus + " · " + root.building.facility_id : ""
            color: "#96a6af"
            font.pixelSize: 12
        }
        Label {
            Layout.fillWidth: true
            visible: !!root.building
            text: root.building ? root.building.description : "Choose a building from search or the map."
            color: "#cad1d0"
            font.pixelSize: 13
            wrapMode: Text.WordWrap
        }
        Label {
            Layout.fillWidth: true
            visible: !!root.building
            text: root.building ? "Extrusion estimate: " + root.building.heightMeters.toFixed(1) + " m · city average-height data" : ""
            color: "#cad1d0"
            font.pixelSize: 12
        }
        Label {
            Layout.fillWidth: true
            visible: !!root.building && !!root.building.floors
            text: root.building ? root.building.floors : ""
            color: "#aebbbd"
            font.pixelSize: 12
            wrapMode: Text.WordWrap
        }

        Repeater {
            model: root.building ? root.building.facts : []
            delegate: Label {
                required property string modelData
                Layout.fillWidth: true
                text: "• " + modelData
                color: "#e5e8e3"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
            }
        }

        Label {
            Layout.fillWidth: true
            visible: !!root.building && root.building.sources.length > 0
            text: "Sources"
            color: "#96a6af"
            font.pixelSize: 11
            font.weight: Font.DemiBold
        }
        Repeater {
            model: root.building ? root.building.sources : []
            delegate: Label {
                required property var modelData
                Layout.fillWidth: true
                text: "↗ " + modelData.label
                color: "#82b9c7"
                font.pixelSize: 11
                wrapMode: Text.WordWrap
            }
        }

        Item { Layout.fillHeight: true }
    }
}
