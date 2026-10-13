# Native campus environment and building inspection

The user authorized autonomous implementation, including inferred interiors, after requesting broad source research and few questions. This supersedes the older prohibition on schematic interiors. Runtime remains local and native. The current repository instructions require committing and pushing the completed feature branch.

## Experience

The campus scene keeps Central and North Campus footprints and adds source-backed roads, paths, green areas, tree inventory and bus stops. Decorative people and street furniture are illustrative. Facades gain original procedural windows, roof edges and entrances; these are visual approximations, not surveyed architecture.

Selecting a building opens its source catalogue and a dedicated inspection mode. Every building can be inspected using an explicitly schematic interior. Where official public floor plans exist, retain official floor names and space names, show the original reference image locally, and use approximate normalized zones when the plan has been visually interpreted. Do not claim those zones are calibrated room geometry. No invented official room identifiers.

Building inspection supports dollhouse, horizontal/vertical sections, semantic transparency, continuous floor explosion, individual floors, and an eye-level walkthrough. Floors, room boundaries, furniture and circulation make the structure legible. Walkthrough is a conceptual preview, not a routing or accessibility guarantee.

## Interaction

Mouse navigation remains available. Open palm pans the campus and rotates the interior camera; pointing selects buildings by a visible cursor and dwell, or scrubs the cut plane in section mode. Closed fist opens the selected building or toggles eye-level view. Thumbs zoom outdoors, change floors in building overview, and move forward/backward at eye level. Victory returns to campus. Require confidence and debounce for discrete actions. Display current action and controls.

## Data and performance

Keep sources, access date, reuse notes, and schematic status with the local data. Google Earth/Maps and competitors inform visual treatment, but their protected imagery/tiles are not extracted into the offline scene. Public library maps with explicit reuse permission can be bundled with attribution. Other sources remain linked references.

Outdoor objects are batched. Detailed indoor geometry is built only for the selected building and reused while sliders change transforms/uniforms. Use Qt render statistics and a sustained camera animation for timing; do not equate an on-demand redraw interval with GPU frame time. No camera starts automatically.

## Acceptance

- Both campuses show actual street/environment context and explicit attribution.
- Public plans are viewable for available library floors; source and inferred information are visually distinguished.
- Enter a Central and a North building, change floors, move a section plane, spread floors, and walk inside with working mouse controls.
- The real worker signal reaches the controller with the correct argument order; automated gesture sequences exercise entry, floor changes and exit.
- Invalid/unavailable source data is reported; runtime needs neither a browser nor a network service.
- Inspect native screenshots and report measured timings and remaining accuracy limitations, then commit and push the isolated branch.
