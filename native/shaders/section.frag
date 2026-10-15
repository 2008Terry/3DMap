VARYING vec4 surfaceColor;
void MAIN() {
    float coordinate = sectionAxis == 1 ? VAR_WORLD_POSITION.y
                     : sectionAxis == 2 ? VAR_WORLD_POSITION.x : VAR_WORLD_POSITION.z;
    if (sectionAxis > 0 && sectionAxis < 4 && coordinate > sectionPosition)
        discard;
    if (sectionAxis == 4 && VAR_WORLD_POSITION.x > 0.0 && VAR_WORLD_POSITION.z > 0.0)
        discard;
    // Mesh colors are authored in sRGB; lighting operates in linear space.
    vec3 rgb = surfaceColor.rgb;
    rgb = rgb * (rgb * (rgb * 0.305306011 + 0.682171111) + 0.012522878);
    BASE_COLOR = vec4(rgb, materialAlpha);
    if (sectionAxis > 0 && sectionAxis < 4 && abs(coordinate - sectionPosition) < 0.09)
        BASE_COLOR.rgb = mix(BASE_COLOR.rgb, vec3(0.95, 0.58, 0.16), 0.7);
    ROUGHNESS = 0.78;
    SPECULAR_AMOUNT = 0.12;
    METALNESS = 0.0;
}
