# Native Campus Map Design

Date: 2026-10-11
Branch: codex/local-performance-map

## Goal

Create a Windows desktop campus map that runs locally without a browser or WebView. Reuse the existing Central and North Campus building data and gesture-map behavior while improving rendering cost and keeping runtime assets on disk.

## Architecture

- Add a standalone Python application under native/; keep the existing React/Vite prototype intact.
- Use the locally installed PySide6 6.8.3 and Qt Quick 3D for the desktop window and GPU-rendered scene.
- Load src/campusBuildings.json and src/campusBuildingFootprints.json as local data. Generate static 3D geometry from the footprint polygons and stored heights.
- Use shared campus materials and batch static geometry where it preserves selection. Keep a lightweight per-building picking index so map selection does not require a raycast through every rendered triangle.
- Build the campus overview, search, selected-building detail panel, reset control, and mouse camera controls with Qt Quick Controls.
- Run camera capture and hand-gesture recognition off the UI thread. Use a local MediaPipe Tasks model and local runtime files; do not request CDN or cloud resources at runtime.
- Preserve the current hand actions: open palm pans, thumb gesture zooms, and Victory resets the camera. Keep a visible recognized-gesture status.

## Performance

- Render on scene or camera changes; do not run an unconditional full-rate animation loop while the map is idle.
- Prefer combined static geometry and shared materials to reduce draw calls. Keep selection and picking data separate from the render mesh.
- Avoid global shadow maps for the full campus; use a lightweight selected-building highlight.
- Keep the interaction thread responsive by processing camera frames in a worker and limiting inference to one hand.

## Data and fidelity

- Keep the eight featured buildings and their sourced architectural details.
- Render the remaining campus buildings from the City footprint and average-height data already stored in the repository. Continue to label height units as inferred and avoid claiming unsourced stories or facade details.
- Keep Central and North Campus bounds and the existing search by building name or Facility ID.

## Acceptance criteria

- The application starts from the local project without opening a browser.
- Central and North Campus appear in one 3D overview; search and selecting a building show its details.
- Mouse navigation and the three existing gesture actions work, with a visible gesture label.
- Runtime building data, gesture model, and required model files are available locally; the app makes no network requests during use.
- The scene remains responsive while idle and during map interaction. Compare frame time and click-response time against the current Three.js scene on the same machine before claiming a measured performance improvement.

## Scope limits

- No cloud deployment, hosted map tiles, remote model fetch, native executable packaging, or new building-detail research in this phase.
- The first native version uses the existing footprint and height data; it does not promise surveyed roof heights, floor counts, interiors, or verified facade models for all buildings.
