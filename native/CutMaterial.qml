import QtQuick
import QtQuick3D

CustomMaterial {
    property int sectionAxis: 0
    property real sectionPosition: 0
    property real materialAlpha: 1
    shadingMode: CustomMaterial.Shaded
    cullMode: CustomMaterial.NoCulling
    sourceBlend: materialAlpha < 0.99 ? CustomMaterial.SrcAlpha : CustomMaterial.NoBlend
    destinationBlend: materialAlpha < 0.99 ? CustomMaterial.OneMinusSrcAlpha : CustomMaterial.NoBlend
    vertexShader: "shaders/section.vert"
    fragmentShader: "shaders/section.frag"
}
