# Native Campus Map Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Build a Windows desktop 3D map for Central and North Campus that runs locally without a browser or WebView and preserves one-hand gesture controls.

**Architecture:** Add a Python/PySide6 application under native/. Qt Quick 3D renders campus buildings in a small number of static geometry batches; Shapely indexes building footprints for search and picking. A background Python worker captures one webcam hand and runs the local MediaPipe Tasks model.

**Tech Stack:** Python 3.12.7, PySide6 6.8.3, Qt Quick 3D, Shapely 2.1.0, OpenCV 4.12.0, MediaPipe Tasks.

**Spec:** docs/superpowers/specs/2026-10-11-native-campus-map-design.md

## Global Constraints

- The application runs as a Windows desktop app without a browser or WebView.
- Runtime building data, MediaPipe model, and model runtime files are local; no runtime CDN or cloud requests.
- The map includes Central Campus and North Campus using the existing 623-building data.
- The eight featured buildings retain their sourced facts and architectural details.
- Generic building heights remain labeled as inferred from the City average-height field.
- Leave the React/Vite prototype unchanged.
- Keep all code, documentation, and commits on the local codex/local-performance-map branch; do not push.

## Review Focus

- Missing or malformed local building data should produce a readable startup error instead of a blank scene — Task 1 checks the current input files and the error path.
- Concave and multi-part footprints must extrude without holes or gaps — Task 2 inspects generated bounds and the Central/North mesh in the native app.
- Overlapping and multipart footprints must select the building represented by the visible hit position — Task 2 manually checks featured and generic building selection.
- Camera permission or MediaPipe initialization failure must leave mouse navigation available and show a clear status — Task 4 runs with camera unavailable.
- Closing during recognition must stop the camera and worker cleanly — Task 4 starts and stops the gesture worker and confirms the process exits.

---

### Task 1: Native application bootstrap and local data model

**Files:**
- Create: native/main.py
- Create: native/Main.qml
- Create: native/campus_data.py
- Create: native/featured_details.json
- Create: native/requirements.txt
- Create: native/setup.ps1
- Create: native/run.ps1
- Create: native/README.md
- Create: native/tests/test_campus_data.py

**Interfaces:**
- campus_data.load_buildings(repo_root: Path) -> tuple[list[Building], CampusExtent]
- `Building` is a dataclass with `id`, `facility_id`, `name`, `campus`, `parts`, `height_m`, `featured`, `facts`, `sources`, `category`, `description`, `floors`, `color`, and `facade_details`; each part has `object_id` and one closed local-coordinate footprint ring.
- `CampusExtent` is a dataclass with `center_x`, `center_z`, `width`, and `depth`, computed from all loaded rings.
- Read `src/campusBuildings.json` (`buildings[]`, `parts[].heightFeet`, `parts[].footprint`) and `src/campusBuildingFootprints.json` (featured footprint/source fields); preserve curated facade/detail facts from the existing building data source.
- main.py loads local data, exposes the controller and data to QML, and reports startup errors in a desktop dialog.
- setup.ps1 creates native/.venv using the local Python 3.12 interpreter and installs native/requirements.txt. run.ps1 launches with that environment.

- [ ] Create the native package entry point and dependency manifest using the local Python/Qt versions.
- [ ] Implement load_buildings() for the curated and campus-wide JSON files; merge duplicate campus parts by building id and preserve source metadata.
- [ ] Add a minimal Main.qml and setup/run scripts. Keep the venv inside native/ and exclude it from Git.
- [ ] Run setup.ps1 and run.ps1; confirm a native window opens and reports 623 buildings loaded. Confirm malformed JSON shows a desktop error.

### Task 2: Batched campus geometry and indexed selection

**Files:**
- Create: native/mesh_builder.py
- Create: native/geometry_provider.py
- Create: native/MapScene.qml
- Create: native/tests/test_mesh_builder.py
- Modify: native/main.py
- Modify: native/campus_data.py
- Modify: native/Main.qml

**Interfaces:**
- mesh_builder.build_campus_mesh(buildings: Sequence[Building]) -> MeshBuffers
- mesh_builder.build_featured_mesh(building: Building) -> MeshBuffers
- campus_data.pick_building(hit_position: tuple[float, float, float]) -> Building | None
- geometry_provider.geometry_from_buffers(buffers: MeshBuffers) -> QQuick3DGeometry
- `MeshBuffers` is a dataclass containing packed position floats, packed normal floats, packed RGBA color floats, triangle indices, and a 3D bounding box; vertices are emitted in Qt Quick 3D coordinates from local x/z footprints and height in meters.
- `pick_building` queries the STRtree by hit x/z, filters candidates to polygons covering that point and hit y within the building's base-to-top bounds, then returns the highest matching building or `None`.

- [ ] Extrude each footprint ring to its source-derived height; triangulate concave tops with Shapely constrained Delaunay triangulation and emit indexed vertex buffers.
- [ ] Build one shared-material geometry batch for generic Central buildings and one for generic North buildings; build one batch per featured building including its sourced facade details.
- [ ] Build an STRtree over footprint parts and resolve Qt Quick 3D hit positions to building ids, including multipart buildings.
- [ ] In MapScene.qml, add the two campus batches, featured batches, ground, fog, camera, and Qt Quick 3D OrbitCameraController.
- [ ] Run run.ps1; confirm both campus extents render, featured columns/windows appear, clicking a featured or generic building shows the expected id, and city footprints contain no triangulation gaps.

### Task 3: Native map interface and camera controls

**Files:**
- Create: native/BuildingDetails.qml
- Create: native/map_controller.py
- Create: native/tests/test_map_controller.py
- Modify: native/Main.qml
- Modify: native/MapScene.qml
- Modify: native/main.py
- Modify: native/mesh_builder.py
- Modify: native/geometry_provider.py

**Interfaces:**
- MapController.search(query: str) -> list[BuildingSummary]
- MapController.select_building(building_id: str) -> BuildingDetailsData
- MapController.reset_camera() -> None
- MapController.pan_by(delta_x: float, delta_y: float) -> None
- MapController.zoom_by(factor: float) -> None
- `BuildingSummary` contains `id`, `facility_id`, `name`, and `campus`; `BuildingDetailsData` adds `height_m`, `featured`, `facts`, and `sources`.

- [ ] Build a Qt Quick Controls layout with campus title, search input, result list, 3D view, selected-building facts, source names, and recognized-gesture status.
- [ ] Wire search by building name or Facility ID to all 623 buildings and selecting a result to the same details view as map picking.
- [ ] Add pan, orbit, zoom, and reset camera controls; keep selected-building highlighting as a small overlay mesh.
- [ ] Run run.ps1; confirm search returns Central and North results, selection updates details, and the map remains responsive while idle and during camera movement.

### Task 4: Offline one-hand gesture control

**Files:**
- Create: native/gesture_worker.py
- Create: native/assets/gesture_recognizer.task
- Modify: native/Main.qml
- Modify: native/main.py
- Modify: native/requirements.txt

**Interfaces:**
- GestureWorker.start() -> None
- GestureWorker.stop() -> None
- `gesture_changed` emits `(key: str, label: str, confidence: float, landmarks: list[tuple[float, float]])`; `status_changed` emits one readable status string.
- MapController.handle_gesture(key: str, confidence: float, landmarks: object) -> None

- [ ] Add the local MediaPipe Tasks Python runtime and store the compatible gesture model under native/assets/.
- [ ] Capture webcam frames in a QThread using OpenCV at 640x480 and no more than 15 inference frames per second; recognize at most one hand.
- [ ] Map Open_Palm to pan, Thumb_Up to zoom in, Thumb_Down to zoom out, and Victory to reset; preserve the 0.68 confidence threshold and 700 ms discrete-action cooldown.
- [ ] Display recognized gesture, camera state, and model errors in the native UI without requiring a camera preview.
- [ ] Run run.ps1; confirm each gesture action, unavailable-camera fallback, and camera release on application close. Search native/ for remote model or CDN URLs and remove any runtime fetch.

### Task 5: Local runtime and performance review

**Files:**
- Modify: native/README.md
- Modify: native/run.ps1
- Modify: native/Main.qml
- Modify: native/mesh_builder.py

**Interfaces:**
- The standard launch command is .\native\run.ps1.
- Performance reporting distinguishes measured timings from expected structural reductions.

- [ ] Ensure the local launch path starts the native window without opening a browser or network service.
- [ ] Inspect the final render batch count; target two generic campus batches plus the eight featured batches, ground, and selection overlay.
- [ ] Measure map frame time during camera movement and click-response time on this machine; record values only when captured locally.
- [ ] Verify runtime data and model assets resolve from the repository regardless of the process working directory.
- [ ] Review the final UI manually, confirm branch is clean after commit, and keep the work local without pushing.
