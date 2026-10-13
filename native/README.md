# Native Campus Map

This is a local Windows desktop application built with PySide6 and Qt Quick. It loads the Central and North Campus footprints from the repository's existing JSON data.

## Run

From the repository root, run:

```powershell
.\native\run.ps1
```

The first run creates `native/.venv` and installs the pinned Python requirements. To select a Python 3.12 interpreter, set `LOCAL_PYTHON` to its `python.exe` path before running `native/setup.ps1`.

The application reads its data from `src/campusBuildings.json`, `src/campusBuildingFootprints.json`, `native/featured_details.json`, `native/building_references.json`, and `native/assets/campus_environment.json`. Gesture recognition uses the bundled `native/assets/gesture_recognizer.task` model and the local MediaPipe Tasks package; the running app makes no network requests. The camera starts only after selecting **启动手势**. If camera access or model initialization fails, mouse navigation stays available. The app does not start a web server or open a browser.

## Campus and indoor exploration (2026-10-12)

The scene has 623 university building records and 2,174 surrounding building
footprints, 966 road segments, 4,754 path segments, 3,562 recorded trees, and
104 static U-M bus stops. Road/path widths, crowns, roof forms and generic
facades are estimated. Up to 160 additional trees and 90 people/bench props
provide illustrative scale cues on mapped grass and paths. These do not describe
observed tree, furniture or pedestrian locations. Nearby bus route labels are
from a static GTFS snapshot and are not live arrivals.

Five reference profiles cover Shapiro, Duderstadt, Hatcher (both wings),
Michigan Union and Beyster. The bundle has 28 official Library floor-map PDFs
with local PNG previews, and three attributable building/space photographs.
The catalogue has 33 source-backed floor entries plus three explicitly inferred
Beyster levels. All generated walls, floor heights, doors, circulation cores,
furniture and 3D registration remain schematic. The reference diagrams can be
enlarged in a native dialog. Other buildings receive clearly labeled illustrative
interiors clipped to their real external footprint.

1. Search a building or point to it, then click **打开建筑结构** or make a fist.
2. Choose **剖开**, **切片**, **透视**, **拆层**, **单层**, or **进入**.
3. For sections, select X/Y/Z and move the cut slider; an index finger controls
   the cut while the section mode is active. Spread and shell opacity have sliders.
4. Use floor buttons or thumb gestures to switch levels. Hatcher has a wing selector.
5. Inside, use W/S to move, A/D to turn, right drag to look, and wheel to move.
   Palm motion looks around; thumb gestures move forward/backward. Walls,
   furniture and stairs block walking. Victory returns to campus. F3 shows stats.

Pointing selection has an 850 ms dwell and a movement tolerance. The camera
worker's four-argument Qt signal is received by a GUI-thread controller slot;
the gesture keys and visible status share the same actions as the controls.
An actual hand/camera interaction was not exercised in the automated scene check.

The static scene is bundled as 15 compressed mesh assets totaling about 5.75 MB.
Input fingerprints prevent stale compiled geometry after data or mesh edits.
Valid bundles load in about 0.2–0.5 s on this machine, excluding interpreter,
UI and driver startup; the broader measured load ranged to 0.9 s. A first
Shapiro interior load took approximately 3.2 s and is retained while switching
modes. Static geometry rebuilding is an authoring operation:

```powershell
.\native\.venv\Scripts\python.exe scripts\build_native_references.py
.\native\.venv\Scripts\python.exe scripts\compile_native_scene.py
```

The environment refresh script fetches authoring sources and is never invoked
by the application. Its GIS/OSM/GTFS provenance is embedded in the JSON.
See [reference attribution](assets/references/ATTRIBUTION.md) and
[competitor research](../docs/research/2026-10-12-campus-visual-realism.md).

The final native checks used Qt 6.8.3 / D3D11 and a 2160×1350 physical window,
with the camera off. Moving-view readings were about 41–58 FPS for campus,
38–46 FPS for section/single-floor/exploded/x-ray views and 30 FPS indoors;
the initial dollhouse sample was 9 FPS during warm-up. These short render-stat
samples are not a steady-state percentile benchmark or a 60 FPS guarantee.
The scene's draw-call readings were 16 outdoors, 6 for a single floor, 8 inside,
34–35 in dollhouse/section, 30 exploded, and 22 in x-ray.

Eighteen Python tests passed, including actual queued Qt gesture signals,
source-floor previews, wing switching, concave footprints and blocked walking.
Native screenshots confirmed all six inspection modes. The five profiles are
not complete surveyed building interiors or a photogrammetric campus twin.

## Local performance check (2026-10-11)

The scene uses 10 static building geometry batches (two campus-wide meshes plus eight featured buildings), one ground model, and a selection overlay when a building is selected. Reusing vertices with identical positions, normals, and colors reduced the campus buffers from 51,600 to 27,422 vertices for Central and from 24,216 to 13,770 for North; triangle index counts are unchanged.

On this machine, a 1980x1230 QML scene was panned programmatically after a one-second warm-up. Across 73 `frameSwapped` intervals during movement, median frame time was 47.82 ms and p95 was 56.96 ms. This is about 21 FPS in that capture and does not establish a 60 FPS result; the local renderer/driver and interactive desktop load affect the measurement. The synchronous Angell Hall selection lookup measured over 100 calls had a 1.021 ms median and 2.807 ms p95. These are local measurements, not guarantees for other machines.
