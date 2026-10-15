VARYING vec4 structureColor;
VARYING vec3 structurePosition;
void MAIN() {
    vec2 offset = structurePosition.xz - vec2(focusX, focusZ);
    bool lens = length(offset) < focusRadius;
    bool front = dot(offset, vec2(directionX, directionZ)) > -focusRadius * 0.25;
    if (revealEnabled && lens && front && structurePosition.y > sillHeight)
        discard;
    vec3 rgb = structureColor.rgb;
    rgb = rgb * (rgb * (rgb * 0.305306011 + 0.682171111) + 0.012522878);
    BASE_COLOR = vec4(rgb, 1.0);
    if (revealEnabled && lens && front && structurePosition.y > sillHeight - 0.09)
        BASE_COLOR.rgb = vec3(0.95, 0.40, 0.06);
    ROUGHNESS = 0.86;
    SPECULAR_AMOUNT = 0.06;
    METALNESS = 0.0;
}
