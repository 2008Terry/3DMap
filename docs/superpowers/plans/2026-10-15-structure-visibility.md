# Structural visibility implementation plan

> Execution: implement inline, with a fresh whole-branch review after hardware verification. The user's instruction to implement the approved combination supplies authorization; no additional approval pause.

**Goal:** Make modeled building interiors and their connections readable through expanded floors, local wall cuts and linked projective views.

**Architecture:** A separate state/geometry adapter consumes BuildingInspector. Reusable scene/viewport components share semantic floor and room IDs; Main integrates entry and exit only.

**Tech stack:** Python, Shapely, PySide6 6.8.3, Qt Quick 3D, GLSL, Direct3D 11.

**Spec:** `docs/superpowers/specs/2026-10-15-structure-visibility-design.md`.

## Global constraints

- Primary D: checkout, `codex/structure-visibility`, no worktree.
- Preserve all existing gesture files and mappings; push only this branch.
- Keep schematic geometry and connectivity explicitly labeled.
- Independent perspective cameras are a composite, not the general Graph Camera algorithm.

## Review focus

- Burton's tallest expanded view and selected-floor sideways offset fit the viewport.
- Disconnected or concave rooms never acquire a straight line through walls.
- Changing building/wing clears stale room IDs and geometry.
- Hidden map input cannot move/reselect the building behind the explorer.
- Discarded wall fragments cannot capture clicks; screen-to-plan mapping handles courtyard holes.

## Task 1: State, topology and layout

Files: `native/structure_visibility.py`, `native/tests/test_structure_visibility.py`.

- [x] Write failing tests for empty state, floor bounds, connected/disconnected rooms and routed free-space containment.
- [x] Implement `build_floor_graph(floor, index)`, `room_route(floor, room)` and `StructureVisibility(inspector)` with semantic IDs, floor/room selection, unfold amount, cut/furniture toggles, explicit bounds, and adjacent portals.
- [x] Verify Burton, Hatcher wing changes, select/close/reopen, and all path points/segments.

## Task 2: Rendering and integration

Files: `native/StructureExplorer.qml`, `native/StructureViewport.qml`, `native/StructureScene.qml`, `native/RevealMaterial.qml`, new reveal shaders; minimal `native/main.py` and `native/Main.qml` integration.

- [x] Add a production-QML hardware harness whose initial load fails until the new component exists.
- [x] Render expanded opaque floors, scene-space core links, local target cuts, independent projective portals, clickable floor plan, room list and floor labels.
- [x] Keep gesture preference intact and suspend underlying map input while active. Check narrow layout, reset/orbit/zoom, keyboard floor selection and exit.

## Task 3: Hardware verification and delivery

Files: `scripts/validate_structure_visibility.py`, verification report and selected previews.

- [x] Run focused and existing native tests; record existing unrelated failures separately if any.
- [x] Capture Shapiro, Union, Burton and both Hatcher wings on hardware D3D11; verify selection sync, geometry bounds, cuts on/off, unfold zero/max, plan picking and exit/reopen.
- [x] Inspect screenshots and fix any visibility, shader, picking or layout failures.
- [x] Fresh whole-branch review; address material findings and recheck affected scenarios.
Delivery: commit and push only the new branch; verify the remote SHA before reporting completion.
