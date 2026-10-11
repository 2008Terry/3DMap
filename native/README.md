# Native Campus Map

This is a local Windows desktop application built with PySide6 and Qt Quick. It loads the Central and North Campus footprints from the repository's existing JSON data.

## Run

From the repository root, run:

```powershell
.\native\run.ps1
```

The first run creates `native/.venv` and installs the pinned Python requirements. To select a Python 3.12 interpreter, set `LOCAL_PYTHON` to its `python.exe` path before running `native/setup.ps1`.

The application reads its data from `src/campusBuildings.json`, `src/campusBuildingFootprints.json`, and `native/featured_details.json`. Gesture recognition uses the bundled `native/assets/gesture_recognizer.task` model and the local MediaPipe Tasks package; the running app makes no network requests. The camera starts only after selecting **Start hand control**. If camera access or model initialization fails, mouse navigation stays available. The app does not start a web server or open a browser.
