# Combined structural visibility

The user approved implementation of the researched combination: multiperspective projection, expanded floors, and local wall removal, with real-GPU validation. Work is on `codex/structure-visibility`, based on `3c5b76b`, in the primary D: checkout. The gesture branch is left unchanged; no new worktree or gesture mappings.

## Design

A dedicated Structural Explorer opens from the building inspector. An expanded overview places each floor at a readable height and pulls the selected floor sideways. Colored connectors preserve the correspondence between the illustrative circulation cores as floors move. Labels select floors without estimating a floor from rendered height.

The overview is combined with independently projected live views: the current floor from an opposing direction and an adjacent floor. This is a portal-style multiperspective composite with explicit floor identity, not a claim to implement the Graph Camera paper's general bent-ray camera. It trades a single global projection for inspectable interiors. All views share floor/room identity, selection, and local cut state.

Opaque walls are selectively removed above a low sill inside the selected room/circulation lens on its camera-facing side. Cut edges are orange; the far-side walls and wall footprints remain readable. No global transparency is needed. A floor-plan inset provides complete room boundaries and clickable room correspondence. The selected room's structurally walkable connection to the circulation core is displayed and reported only if present in the generated geometry.

The existing geometry remains schematic. Source-backed names do not certify wall/door/stair locations. Vertical links are explicitly illustrative and are not certified navigation or accessibility routes. Disconnected spaces receive no invented connection. Furniture is an optional detail and not part of the structural connectivity calculation.

## Isolation

New geometry/connection logic and state live in `native/structure_visibility.py`; new QML components and shaders own rendering. Existing `BuildingInspector` is consumed without changing its gesture contracts. `main.py` supplies the new context object. `Main.qml` supplies entry/exit and suspends the underlying controller while the explorer is active, preserving its enabled preference. No changes to `gesture_input.py`, `gesture_worker.py`, `map_controller.py`, `MapScene.qml`, or existing inspection modes.

## Acceptance

- Every catalogue floor is accessible, including Burton B plus 1–10 and both Hatcher wings; all expanded bounds include the pulled floor and connection geometry.
- Selecting a floor or room updates all projections and the plan; clicks use explicit object/floor identity.
- Local wall removal reveals interiors with opaque materials and visible wall footprints; disabling the cut restores complete walls.
- Structural paths stay within the walkable free-space polygon, and disconnected rooms do not receive a false path.
- Floor spread, narrow windows, multiple buildings, wing switches, exit/reopen, keyboard selection and underlying gesture-state suspension have regression coverage.
- Capture the production QML using D3D11 on Intel Iris Xe, retain adapter/backend logs, screenshots and timing. No WARP/offscreen/software result counts as hardware verification.

## Approach decision

A full bent-ray Graph Camera would require a new projection/picking pipeline. A transparency-only change would not solve structural legibility. The first implementation uses explicit linked projective portals, expanded geometry and target-driven cuts, which preserves identifiable original geometry and can be verified on the current native renderer. A later continuous projection can replace the portals without changing semantic IDs.
