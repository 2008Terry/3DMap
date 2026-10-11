import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    visible: true
    width: 1320
    height: 820
    minimumWidth: 980
    minimumHeight: 640
    title: "Michigan Campus Map"
    color: "#111820"

    Rectangle {
        anchors.fill: parent
        color: "#111820"

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 32
            spacing: 20

            Label {
                text: "MICHIGAN · CAMPUS EXPLORER"
                color: "#f3f4f0"
                font.pixelSize: 27
                font.weight: Font.DemiBold
            }

            Label {
                text: "Native desktop map · Central Campus and North Campus"
                color: "#aab6bd"
                font.pixelSize: 15
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: 18
                color: "#18232d"
                border.color: "#293845"

                Column {
                    anchors.centerIn: parent
                    spacing: 12

                    Label {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: campusBuildings.length + " buildings loaded"
                        color: "#f3f4f0"
                        font.pixelSize: 22
                        font.weight: Font.Medium
                    }

                    Label {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "Central Campus · North Campus"
                        color: "#91a3ad"
                        font.pixelSize: 14
                    }
                }
            }
        }
    }
}
