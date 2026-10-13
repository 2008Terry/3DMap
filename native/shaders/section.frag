VARYING vec4 surfaceColor;
void MAIN() {
    float coordinate = sectionAxis == 1 ? VAR_WORLD_POSITION.y
                     : sectionAxis == 2 ? VAR_WORLD_POSITION.x : VAR_WORLD_POSITION.z;
    if (sectionAxis > 0 && sectionAxis < 4 && coordinate > sectionPosition)
        discard;
    if (sectionAxis == 4 && VAR_WORLD_POSITION.x > 0.0 && VAR_WORLD_POSITION.z > 0.0)
        discard;
    BASE_COLOR = vec4(surfaceColor.rgb, materialAlpha);
    if (sectionAxis > 0 && sectionAxis < 4 && abs(coordinate - sectionPosition) < 0.09)
        BASE_COLOR.rgb = mix(BASE_COLOR.rgb, vec3(0.95, 0.58, 0.16), 0.7);
    ROUGHNESS = 0.78;
    METALNESS = 0.0;
}
