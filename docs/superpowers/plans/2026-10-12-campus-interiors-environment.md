# Campus environment and interiors implementation plan

> Execution: native implementation with parallel source research and independent final review. The user explicitly delegated design decisions and requested end-to-end execution.

**Goal:** Add a convincing local campus environment and navigable, inspectable building structures with honest source attribution.

**Architecture:** Static outdoor batches; lazy per-building floor meshes; QML inspection state and GPU section planes. Public map assets remain independent of the schematic 3D reconstruction.

**Tech stack:** Python 3.12, PySide6 6.8 / Qt Quick 3D, Shapely 2.1, existing local MediaPipe runtime.

**Spec:** `docs/superpowers/specs/2026-10-12-campus-interiors-environment-design.md`

## Constraints and review focus

- Keep offline runtime and explicit manual camera activation; push the completed branch under current AGENTS instructions.
- No extracted Google meshes/textures; catalogue source rights and approximate geometry.
- Multipart/concave footprints must not spill rooms into empty courtyards.
- Switching floors/buildings must release old geometry and preserve valid selections.
- Shader clipping must affect floor furniture and structure together.
- Gesture signal arity and dwell/cooldown must work across actual Qt signals, not just direct method calls.
- Inferred rooms are visibly labeled; no fabricated official room numbers or live transit status.

## Work items

- [x] Research and bundle permitted floorplan/reference assets (`native/building_references.json`, `native/assets/references/`); refresh competitor report under `docs/research/`.
- [x] Acquire real environment features, implement `load_environment(repo_root) -> dict` and `build_environment_meshes(data, buildings) -> dict[str, MeshBuffers]` in separate environment modules.
- [x] Add `build_facade_mesh(buildings) -> MeshBuffers` for batched procedural architectural detail.
- [x] Implement `build_interior(building, profile)` and `BuildingInspector` with lazy geometry, source plans, floor selection, room picking, section/transparency/explosion modes, and constrained eye-level navigation.
- [x] Connect native QML campus/inspection UI and repair/extend gesture routing in `MapController`/`main.py`.
- [x] Validate geometry/source provenance, real Qt signal routing, and native screenshots in campus/section/floor/explode/walkthrough modes; collect render metrics.
- [x] Review full branch, fix substantive findings, document measured results and limits, commit and push without rewriting remote history.
