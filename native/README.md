# Native Campus Map

This is a local Windows desktop application built with PySide6 and Qt Quick. It loads the Central and North Campus footprints from the repository's existing JSON data.

## Run

From the repository root, run:

```powershell
.\native\run.ps1
```

The first run creates `native/.venv` and installs the pinned Python requirements. To select a Python 3.12 interpreter, set `LOCAL_PYTHON` to its `python.exe` path before running `native/setup.ps1`.

The application reads its data from `src/campusBuildings.json`, `src/campusBuildingFootprints.json`, and `native/featured_details.json`. Gesture recognition uses the bundled `native/assets/gesture_recognizer.task` model and the local MediaPipe Tasks package; the running app makes no network requests. The camera starts only after selecting **Start hand control**. If camera access or model initialization fails, mouse navigation stays available. The app does not start a web server or open a browser.

## Local performance check (2026-10-11)

The scene uses 10 static building geometry batches (two campus-wide meshes plus eight featured buildings), one ground model, and a selection overlay when a building is selected. Reusing vertices with identical positions, normals, and colors reduced the campus buffers from 51,600 to 27,422 vertices for Central and from 24,216 to 13,770 for North; triangle index counts are unchanged.

On this machine, a 1980x1230 QML scene was panned programmatically after a one-second warm-up. Across 73 `frameSwapped` intervals during movement, median frame time was 47.82 ms and p95 was 56.96 ms. This is about 21 FPS in that capture and does not establish a 60 FPS result; the local renderer/driver and interactive desktop load affect the measurement. The synchronous Angell Hall selection lookup measured over 100 calls had a 1.021 ms median and 2.807 ms p95. These are local measurements, not guarantees for other machines.
