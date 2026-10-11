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

            RowLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                spacing: 24

                ColumnLayout {
                    Layout.preferredWidth: 270
                    Layout.fillHeight: true
                    spacing: 16

                    Label {
                        text: "MICHIGAN · CAMPUS EXPLORER"
                        color: "#f3f4f0"
                        font.pixelSize: 21
                        font.weight: Font.DemiBold
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    Label {
                        text: campusBuildings.length + " buildings · Central + North Campus"
                        color: "#aab6bd"
                        font.pixelSize: 14
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 1
                        color: "#293845"
                    }
                    Label {
                        text: "Select a building in the map"
                        color: "#aab6bd"
                        font.pixelSize: 13
                    }
                    Label {
                        id: selectionLabel
                        text: "Drag to orbit · Ctrl-drag to pan · wheel to zoom"
                        color: "#e1e6e3"
                        font.pixelSize: 15
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    Item { Layout.fillHeight: true }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.minimumWidth: 560
                    radius: 18
                    color: "#dbe5e4"
                    clip: true

                    MapScene {
                        anchors.fill: parent
                        campusExtent: campusBounds
                        centralGeometry: geometryCentral
                        northGeometry: geometryNorth
                        featuredGeometries: geometryFeatured
                        campusPicker: campusDataPicker
                        onBuildingPicked: function(buildingId) {
                            const building = campusBuildings.find(item => item.id === buildingId)
                            selectionLabel.text = building ? building.name + " · " + building.id : buildingId
                        }
                    }
                }
            }
        }
    }
}
