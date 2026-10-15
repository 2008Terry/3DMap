import QtQuick
import QtQuick3D

CustomMaterial {
    property bool revealEnabled: false
    property real focusX: 0
    property real focusZ: 0
    property real focusRadius: 20
    property real directionX: 0
    property real directionZ: 1
    property real sillHeight: 0.72
    shadingMode: CustomMaterial.Shaded
    cullMode: CustomMaterial.NoCulling
    vertexShader: "shaders/reveal.vert"
    fragmentShader: "shaders/reveal.frag"
}
