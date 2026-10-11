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
    property var searchResults: []
    property var selectedBuilding: null

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
                    Layout.preferredWidth: 330
                    Layout.minimumWidth: 280
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
                    TextField {
                        id: searchField
                        Layout.fillWidth: true
                        placeholderText: "Search building or Facility ID"
                        selectByMouse: true
                        onTextChanged: window.searchResults = mapController.search(text)
                    }
                    ListView {
                        id: searchList
                        Layout.fillWidth: true
                        Layout.preferredHeight: searchField.text.length > 0 ? 200 : 0
                        clip: true
                        model: window.searchResults
                        spacing: 3
                        delegate: Rectangle {
                            required property var modelData
                            width: searchList.width
                            height: 48
                            radius: 7
                            color: resultMouse.containsMouse ? "#263641" : "#1a252e"
                            Column {
                                anchors.left: parent.left
                                anchors.right: parent.right
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.leftMargin: 10
                                anchors.rightMargin: 10
                                spacing: 3
                                Label {
                                    width: parent.width
                                    text: modelData.name
                                    color: "#eef0ed"
                                    elide: Text.ElideRight
                                    font.pixelSize: 12
                                }
                                Label {
                                    width: parent.width
                                    text: modelData.campus + " · " + modelData.facility_id
                                    color: "#93a3ac"
                                    elide: Text.ElideRight
                                    font.pixelSize: 10
                                }
                            }
                            MouseArea {
                                id: resultMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                onClicked: {
                                    window.selectedBuilding = mapController.select_building(modelData.id)
                                    window.searchResults = []
                                    searchField.text = ""
                                }
                            }
                        }
                    }
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 1
                        color: "#293845"
                    }
                    Label {
                        text: "Drag to orbit · Ctrl-drag to pan · wheel to zoom"
                        color: "#e1e6e3"
                        font.pixelSize: 11
                        wrapMode: Text.WordWrap
                        Layout.fillWidth: true
                    }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 6
                        Button { text: "−"; onClicked: mapControllerObject.zoom_by(1.2) }
                        Button { text: "+"; onClicked: mapControllerObject.zoom_by(0.82) }
                        Button { text: "Reset view"; Layout.fillWidth: true; onClicked: mapControllerObject.reset_camera() }
                    }
                    Label {
                        Layout.fillWidth: true
                        text: mapControllerObject ? mapControllerObject.gesture_status : ""
                        color: "#91a8ad"
                        font.pixelSize: 11
                        wrapMode: Text.WordWrap
                    }
                    BuildingDetails {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        building: window.selectedBuilding
                    }
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
                        mapController: mapControllerObject
                        selectionOverlay: selectionOverlayState
                        onBuildingPicked: function(buildingId) {
                            window.selectedBuilding = mapController.select_building(buildingId)
                        }
                    }
                }
            }
        }
    }
}
