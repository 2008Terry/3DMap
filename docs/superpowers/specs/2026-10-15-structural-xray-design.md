# Structural interior readability

The user authorized research, design and implementation with minimal discussion. Work in the primary D: checkout and preserve the exterior campus presentation.

## Research and decisions

- Qt CustomMaterial supports separate RGB and alpha blend factors since 6.7. The existing material reuses SrcAlpha for alpha, producing alpha squared in the View3D texture. Use One / OneMinusSrcAlpha for alpha and retain SrcAlpha / OneMinusSrcAlpha for RGB. Reference: https://doc.qt.io/qt-6.8/qml-qtquick3d-custommaterial.html
- Qt's built-in OIT is introduced in 6.11; the app pins 6.8.3. Do not upgrade the application to fix this scene. Reference: https://doc.qt.io/qt-6/qml-qtquick3d-sceneenvironment.html#oitMethod-prop
- Weighted blended OIT addresses ordering, but cannot make many overlapping slabs semantically readable. Reference: McGuire and Bavoil, 2013, https://jcgt.org/published/0002/02/09/
- Prefer focus plus context: current level has readable partitions and a lightly translucent floor; other levels have faint surfaces and structural outlines. Furniture appears on the current level in xray. Other inspection modes retain all-level furniture behavior.
- Indoor geometry and navigation topology are distinct. Preserve source identity independently of inferred walls and furniture; no routing claims. Reference: OGC IndoorGML 2.0 (2025), https://www.ogc.org/announcement/ogc-publishes-indoorgml-2-0-part-1-conceptual-model-standard/
- Shapiro officially has basement plus levels 1-4. Official floor maps are reference truth, approximate registered room zones remain schematic. https://www.lib.umich.edu/visit-and-study/floor-plans/shapiro-library-floors/
- Burton's tenth floor bell chamber is documented by the Regents (2010). Basement plus ten levels is the user's supplied correction; distinguish that catalog basis from surveyed floor geometry. https://regents.umich.edu/files/meetings/06-10/2010-6-IX-6.pdf and https://smtd.umich.edu/facilities/burton-memorial-tower/

## Alternatives

1. Fix blend factors only: smallest patch, but stacked double-sided floors still obscure interior hierarchy.
2. OIT/renderer upgrade: better per-pixel ordering, much larger compatibility and delivery scope; not selected.
3. Correct blending plus selected-level emphasis and structure outlines: selected for readability on the current runtime. Sorting is still approximate; this is an architectural inspection view, not physically accurate glass.

## Geometry and behavior

Separate slab, space zones, partitions, furniture, ceiling and structural outlines. Remove duplicate coincident wall runs by constructing their union. Subtract the corridor from approximate zones, avoid overlap between zones, and keep open study/collection/lounge/cafe zones open rather than enclosing every semantic region. Closed rooms keep doors and walls. No unsupported official stair locations or room dimensions.

Xray uses low-opacity context surfaces and outlines, with current-floor emphasis. Existing cut shaders continue to clip all geometry, including outlines. Room picking in xray targets only the current floor; hidden/context floors must not intercept it.

Change floors without changing the current inspection mode, for keyboard, buttons and gestures. Inside gestures retain walking. Refit exploded views when entering the mode, changing separation, or resizing. Use actual vertical range, footprint bounds, vertical FOV and aspect ratio, including a margin. Orbit orientation and indoor walking remain available.

Use a separate matte ceiling geometry and convert mesh sRGB colors to linear in the custom shader; reduce inspection lighting without changing campus lighting.

## Acceptance

Capture native Windows GPU before/after images and renderer identity. Verify transparent surfaces reveal the interior and do not become white; inspect Shapiro, Union, Burton and both Hatcher wings. Verify Burton extreme separation at landscape and portrait aspect ratios. Test catalog labels, room/corridor disjointness, non-overlapping regions, valid spawn/collision, floor changes in all modes and gesture/keyboard parity. Run the complete native suite and web build. Commit and push the focused changes; report any remaining schematic data or hardware limitations.
