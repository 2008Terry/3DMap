# Native Campus Map

This is a local Windows desktop application built with PySide6 and Qt Quick. It loads the Central and North Campus footprints from the repository's existing JSON data.

## Run

From the repository root, run:

```powershell
.\native\run.ps1
```

The first run creates `native/.venv` and installs the pinned Python requirements. To select a Python 3.12 interpreter, set `LOCAL_PYTHON` to its `python.exe` path before running `native/setup.ps1`.

The application reads its data from `src/campusBuildings.json`, `src/campusBuildingFootprints.json`, `native/featured_details.json`, `native/building_references.json`, and `native/assets/campus_environment.json`. Gesture recognition uses the bundled `native/assets/gesture_recognizer.task` model and the local MediaPipe Tasks package; the running app makes no network requests. The camera starts only after selecting **启动手势**. If camera access or model initialization fails, mouse navigation stays available. The app does not start a web server or open a browser.

## Current gesture controls (2026-10-13)

Use **启动手势**, **暂停控制** and **手势设置** in the map's persistent toolbar.

Stopping the camera stops gesture controls immediately and releases the camera
and recognizer on their worker thread. The UI shows **正在停止…** and prevents
restart until that thread finishes. Initialization checks for cancellation
before creating the recognizer or opening the camera. Application exit waits
for cleanup after leaving the GUI event loop; driver-dependent shutdown time
has not been measured.
Settings include a camera index (six choices, without opening devices to scan
them), sensitivity, a smaller pointing reach, dwell selection, and pointing-center
calibration. For calibration, hold an index finger comfortably, then click
**此位置设为中心** within three seconds. **恢复中心** restores the default.
Settings apply for this session. The skeleton panel shows mirrored landmarks,
the recognized pose and confirmation progress; the map overlay stays visible
when the sidebar is scrolled or a building is open.

| Input | Campus / structure | Inside |
| --- | --- | --- |
| Index finger | Point, then pinch to confirm; optional 850 ms dwell; select rooms in all structure modes | Select schematic space |
| Thumb/index pinch | Confirm the recent pointer (up to 800 ms old); drag to pan, or adjust the cut, floor spread or shell opacity in the matching mode | Look around |
| Open palm and move | Pan at a scale based on current camera distance | Look around |
| V / two fingers and move | Orbit the map or building; open/close the two fingers to zoom in/out | Look around |
| Thumb up/down, held | Continuous zoom; floor changes every 800 ms in structure mode | Continuous forward/backward movement, default 2 m/s |
| Fist, held 550 ms | Open selected building, then release/reissue to enter | Return to dollhouse |
| Thumb toward screen-right, held 600 ms | Open selected building, then release/reissue to enter | Return to dollhouse |
| Index/middle/ring fingers, held 650 ms | Cycle dollhouse, section, x-ray, exploded and floor modes | Switch to dollhouse |
| Thumb toward screen-left, held 600 ms | Return from structure to the saved campus view | Return to dollhouse |
| Thumb/index/little fingers extended, held 850 ms | Pause/resume gesture control, including while control is paused | Same |

In section mode, pinch-drag horizontally for X, vertically for Y/Z. In exploded
mode, drag upward to increase floor spacing. In x-ray mode, drag upward to make
the shell more transparent. The open palm continues to pan in these modes.
Changing structure modes in the same building preserves orbit and zoom;
switching buildings/wings resets the view. R explicitly resets the current view.
An interrupted observation stops movement but does not rearm a held confirmation;
use a different stable pose or briefly remove the hand before repeating it.

**V no longer resets the view.** Use R or **重置视角** to reset, and Esc or
the side thumb to go back. Open palm, pinch and V are clutched: establish a pose,
move, then relax to stop. One-Euro-style adaptive filtering stabilizes slow
motion and responds more quickly to fast motion. A candidate needs 120 ms
stability before control; discrete actions need the longer holds above and
release before repeating. Pinch uses palm-normalized close/open hysteresis.
These are design defaults, not independently validated accuracy thresholds.

The interpreter now uses the recognizer's existing 3D world-landmark estimates
for finger angles, pinch distance and finger spread. Screen coordinates still
control pointing, dragging and directional thumb gestures. If valid world
landmarks are unavailable, image geometry is used; changing geometry sources
requires a fresh stable pose. These monocular estimates are not measured hand
depth or calibrated 3D positions. A model pose needs confidence 0.60 to start;
an established pose can persist at 0.45, stopping below that threshold.

Keyboard, while the map has focus: hold WASD/arrows to walk/turn indoors or
orbit outdoors; hold +/- to zoom; E enters; M cycles modes; PageUp/PageDown
changes floors; Esc returns; R resets; Space pauses/resumes gesture control.
Plus and equals share one held-key entry so releasing Shift before the zoom
key does not leave zoom active.
Mouse: left drag orbits; right/middle drag or Ctrl-left drag pans; right drag
looks around indoors; wheel zooms or walks. Double-click enters a selected
building. Qt-supported touchpad/touch pinch, rotation and translation are also
wired to the same controls. Physical touchpad gestures have not been exercised.

Manual input takes priority while a key, mouse button or touch contact is held,
including when it is stationary. A native touchpad gesture keeps priority from
its begin event to its end event. After release, a 600 ms handover delay and a
new stable hand pose precede camera control. Keyboard auto-repeat releases do
not end the held-key state; text composition also renews manual priority.
Changing the building wing or floor establishes a new hand-drag baseline.
Room picking reads the hit model's floor index, so slab undersides and exploded
levels do not rely on height rounding. A selected schematic room has a yellow
floor overlay, with the same cuts and floor spread as the structure. Pinch,
dwell and mouse selection show the selected building/room or a missed-target
message for 1.8 seconds. Repeating a floor change at the top/bottom keeps the
current selection and viewing mode.
Losing window
activation or opening the reference-plan dialog stops gesture movement;
manual input holds are cleared on window deactivation. Walking still uses the existing
collision check. Gesture navigation stops when the latest observation reaches
250 ms of age from camera-read completion, on the next GUI tick/delivery; rejected poses stop motion
immediately. Smoothing and pose holds use observation timestamps, not GUI
delivery times; duplicate/out-of-order results are ignored. A stream timeout
clears the cached pointer and stops movement without treating the interruption
as a physical hand release or rearming a held confirmation.

The model weights are unchanged. MediaPipe runs single-hand LIVE_STREAM
tracking with a 640x480 camera target at 30 Hz, dropping frames when inference
is busy. Its callback writes one latest-result mailbox; GUI polling discards
results more than 250 ms old, avoiding queued old actions after an expensive
UI operation. DirectShow falls back to MSMF. The camera buffer-size request
depends on the driver and is not a guarantee that the driver has no buffering.
Pinch, three fingers and side thumb use landmark geometry, not new trained
classes or fabricated model confidence scores.
If the driver returns a different resolution, frames are reduced to fit within
640x480 while preserving their aspect ratio, with no upscaling. Geometry and
the skeleton preview use the actual image aspect ratio.

The displayed Hz measures inference-result updates, not rendering FPS.
The displayed milliseconds are a smoothed camera-read-completion-to-callback
duration, including image preprocessing and recognition. They exclude
camera-driver capture delay, GUI delivery, and rendering.
The 30 Hz target is not a measured throughput claim.

The first update was checked for Python syntax and opened in the native app
without startup errors. A subsequent run of the existing suite had 16 passes
and two failures in tests that still expect the old immediate-trigger gesture
mapping. After the user's instruction to prioritize implementation, no further
tests were run for the additions above. No real-hand recognition, error-rate,
latency comparison or fatigue study was conducted. The 2026-10-12 test count
below is historical and does not validate these new controls.
See [design and HCI sources](../docs/research/2026-10-13-gesture-design.md)
and [native UI screenshot](../docs/research/previews/gesture-controls.png).

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
3. For sections, select X/Y/Z and move the cut slider or pinch-drag the cut.
   Pinch-drag also adjusts exploded floor spacing and x-ray shell opacity;
   the sliders remain available. The index finger always points/selects.
4. Use floor buttons or thumb gestures to switch levels. Hatcher has a wing selector.
5. Inside, use W/S to move, A/D to turn, right drag to look, and wheel to move.
   Palm motion looks around; thumb gestures move forward/backward. Walls,
   furniture and stairs block walking. F3 shows stats. The current gesture
   mapping above replaces the original Victory-to-reset mapping.

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

## Structural inspection update (2026-10-15)

Xray now emphasizes the selected floor with faint context floors and structural
outlines. Floor navigation preserves the current mode for gestures, buttons and
PageUp/PageDown. Exploded camera fitting includes the complete expanded height
and viewport aspect ratio. Room zones, partitions and ceilings are independent
meshes; open study zones are no longer automatically enclosed. Shapiro levels
2-4 have reviewed approximate regions from the bundled official maps. Burton's
catalog is B plus 1-10, with its user-provided basement correction distinguished
from the official tenth-floor bell chamber evidence.

See the [research and screenshot report](../docs/research/2026-10-15-structural-xray-report.html).
Reproduce native inspection captures with:

```powershell
.\native\.venv\Scripts\python.exe scripts\validate_native_interiors.py --output .superpowers/interior-validation/final --full
```

The capture harness uses the production inspection scene and a basic render loop,
without starting the camera or loading campus background meshes. Add `--narrow`
to check a narrow viewport. It checks near-white xray pixels and saves render
backend identity and camera bounds alongside screenshots. This is not a live
hand-recognition or a performance benchmark. Existing legacy gesture tests and
the local MediaPipe/TensorFlow dependency conflict are recorded separately in
the report; they are not fixed by the structural rendering changes.

## Combined structural visibility (2026-10-15)

Open a building, then choose **结构透视 · 展开与连接**. The separate workspace
combines an expanded overview, a current-floor reverse perspective, an adjacent
floor perspective, and a clickable floor plan. Selecting a space synchronizes
the views and shows a wall-clearance path to its illustrative circulation core
when one exists. Disconnected pieces of the same named zone are separate
selectable regions. The unfold slider preserves floor/core correspondence;
local cuts remove camera-facing wall fragments above a low sill, with orange
edges and opaque remaining surfaces. Drag to orbit, scroll to zoom, double-click
or press R to reset, PageUp/PageDown to select a floor, and Escape to return.

This is a linked projective composite, not the general bent-ray Graph Camera.
Walls, doors, cores and vertical links remain schematic. Paths describe the
generated wall geometry, ignore furniture, and are not verified navigation or
accessibility routes. The original gesture modules and five-mode cycle are
unchanged. The underlying map input is suspended while this workspace is open,
without changing the gesture-enabled preference.

Hardware reproduction (no webcam):

```powershell
.\native\.venv\Scripts\python.exe scripts\validate_structure_visibility.py
```

See [implementation, GPU evidence and remaining limits](../docs/research/2026-10-15-structure-visibility-implementation.md).

## Local performance check (2026-10-11)

The scene uses 10 static building geometry batches (two campus-wide meshes plus eight featured buildings), one ground model, and a selection overlay when a building is selected. Reusing vertices with identical positions, normals, and colors reduced the campus buffers from 51,600 to 27,422 vertices for Central and from 24,216 to 13,770 for North; triangle index counts are unchanged.

On this machine, a 1980x1230 QML scene was panned programmatically after a one-second warm-up. Across 73 `frameSwapped` intervals during movement, median frame time was 47.82 ms and p95 was 56.96 ms. This is about 21 FPS in that capture and does not establish a 60 FPS result; the local renderer/driver and interactive desktop load affect the measurement. The synchronous Angell Hall selection lookup measured over 100 calls had a 1.021 ms median and 2.807 ms p95. These are local measurements, not guarantees for other machines.
