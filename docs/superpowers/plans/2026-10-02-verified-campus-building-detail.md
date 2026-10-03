# Verified Campus Building Detail Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Replace estimated building rectangles and heights with sourced Ann Arbor building geometry, show verified exterior detail where evidence supports it, and make buildings visually dominant over campus context.

**Architecture:** Filter the City of Ann Arbor open building-footprint dataset to the eight existing campus targets and store compact local-meter polygons plus only supported height/level metadata in `campusData.js`. Keep Three.js rendering driven by that dataset, add only per-building façade details supported by cited official drawings or clear photos, and mute context surfaces in the existing scene.

**Tech Stack:** Vite, React, Three.js, City of Ann Arbor GeoJSON, OpenStreetMap coordinates, official University of Michigan project materials.

**Spec:** `docs/superpowers/specs/2026-10-02-umich-building-architecture-detail-design.md`

## Global Constraints

- Keep all eight current buildings in the campus overview.
- Use traceable building polygons and record source attribution.
- Add windows, floor divisions, roof forms, columns, entrances, or floor counts only when verified by a source for that building.
- Do not derive geometry or textures from Google Maps or Google Earth imagery.
- Do not invent interior rooms or layouts; present a published plan only when one is available.
- Keep roads and background visually secondary.
- Run the existing build and inspect the map and existing interactions in a browser.

## Review Focus

- A target building must not accidentally match a neighboring polygon; verify candidate identity with name/point proximity and inspect the resulting map footprint.
- City average-height fields must not be misrepresented as floor counts or roof elevations.
- Concave source polygons and multipolygons must remain valid after local-coordinate projection and Three.js extrusion.
- Missing façade evidence must not turn into procedural decorative windows or invented floor divisions.
- Stronger building contrast must preserve labels, selection highlight, and readability of the Diag.

## Execution Ruling

- The checkout contains uncommitted gesture-recognition work that changed the root app entry. Keep that work intact and expose the campus map through a separate `/campus.html` Vite entrypoint.
- Use the City of Ann Arbor's live Building Footprints FeatureServer query for WGS84 polygons and per-record fields; it contains current names and a `STORIES` field that differ from the August downloadable snapshot.
- Render the photographed Angell Hall portico columns and visible window bays, plus Hill Auditorium's documented south-portico columns and stringcourses, with schematic dimensions. Keep other buildings' supported exterior facts in the detail panel until sources establish precise locations and dimensions; do not infer window grids.

---

### Task 1: Curate verified building geometry and sources

**Files:**
- Modify: `src/campusData.js`
- Create: `src/campusBuildingFootprints.json`
- Modify: `docs/umich-diag-map-sources.md`

**Interfaces:**
- Keep exports `MAP_CENTER`, `CAMPUS_CONTEXT`, and `BUILDINGS`.
- Each building keeps `id`, `name`, `category`, `description`, `center`, `footprint`, `levels`, `heightMeters`, and `sources`; use `null` for unsupported levels or height and remove estimate flags when the value is source-backed.

- [x] Retrieve the City of Ann Arbor Building Footprints FeatureServer records and inspect geometry, `ABG_BLD_HG`, `STORIES`, update date, and attribution.
- [x] Match each target to the official record by `FacilityID` and current `Bldg_Name`; retain related city features for composite buildings such as Angell and Hatcher.
- [x] Project verified polygon rings to the existing local-meter coordinate system; preserve source-supported multipolygon components and simplify only enough to keep the local data compact without changing building outlines visibly.
- [x] Preserve source height and story fields separately; display stories only where official evidence agrees, and never convert height into a floor count.
- [x] Update the source notes with dataset URL, access date, attribute meanings, per-building match evidence, and attribution.
- [x] Inspect all eight records for closed rings, coordinate range, height meaning, and complete provenance.
- [x] Commit with `feat: add verified campus building footprints`.

### Task 2: Render source-supported architecture and de-emphasize roads

**Files:**
- Modify: `src/CampusScene.jsx`
- Create: `src/CampusExplorer.jsx`
- Create: `src/campus-main.jsx`
- Create: `src/campus-overrides.css`
- Create: `campus.html`
- Create: `vite.config.js`
- Modify: `docs/umich-diag-map-sources.md`

**Interfaces:**
- `CampusScene` continues to consume `BUILDINGS` and `CAMPUS_CONTEXT`; any façade-detail data is stored per building with its source reference.
- Building selection, label IDs, and reset-camera behavior remain unchanged.

- [x] Review official University materials and clear, attributable building photographs for the eight targets; record which visible façade features each source verifies.
- [x] Add Angell Hall's source-confirmed eight-column portico and photo-visible window bays, plus Hill Auditorium's four south-facade columns and documented stringcourses, to their building records and render them with explicitly schematic dimensions. Do not add generic window grids or unsupported floor counts.
- [x] Keep buildings with no verified façade imagery as simple sourced footprint extrusions, with no unsupported decorative detail.
- [x] Reduce the contrast and visual weight of street strips and paths through map-specific styles; retain enough Diag context for orientation.
- [x] Add a dedicated map page that preserves the current root app, updates the map detail panel and caveat to distinguish sourced height from unknown floor counts, focuses selected buildings, and is included in the production Vite build.
- [x] Run `npm run build`; open the local map and inspect all eight shapes, labels, selection, camera reset, and visual hierarchy.
- [x] Commit with `feat: render verified campus building details`.
