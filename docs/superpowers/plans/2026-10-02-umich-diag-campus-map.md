# UMich Diag Campus Explorer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Replace the fictional single-building screen with a local-data, interactive 3D map of the Diag and a small set of nearby UMich Central Campus landmarks.

**Architecture:** Store a compact, source-documented map dataset in the repository. Render its Diag context and extruded building footprints in a Three.js component, while React owns the selected building, details, and reset-camera state. Keep an accessible DOM list synchronized with scene selection.

**Tech Stack:** Existing Vite, React, Three.js, CSS, OpenStreetMap footprints, and public University of Michigan building information.

**Spec:** `docs/superpowers/specs/2026-10-02-umich-diag-campus-map-design.md`

## Global Constraints

- Center the scene on the Diag and cover an approximately 700–800 meter-wide core area.
- Include about eight nearby, recognizable buildings; only include targets with usable footprint data.
- Make building geometry and details local to the repository; do not require a map API key or live map service at runtime.
- Record source URLs, access date, and source fields; display OpenStreetMap and ODbL attribution.
- Keep the view an orientation prototype; do not add full-campus coverage, indoor geometry, routing, positioning, accounts, backend services, or editing.
- Retain the existing Vite, React, Three.js stack, Chinese interface style, responsive layout, visible keyboard focus, and reduced-motion support.

## Review Focus

- Footprint rings can contain concave polygons and must extrude without invalid geometry.
- Missing or estimated height/level information must remain identifiable as estimated.
- CSS labels and accessible list items must select the same building IDs as 3D raycasting.
- A drag/rotate gesture must not select a building on pointer-up; empty-ground clicks clear selection.
- The map and controls must remain reachable without horizontal overflow on narrow screens.

---

### Task 1: Source and store Diag-area map data

**Files:**
- Create: `src/campusData.js`
- Create: `docs/umich-diag-map-sources.md`

**Interfaces:**
- `src/campusData.js` exports `MAP_CENTER`, `CAMPUS_CONTEXT`, and `BUILDINGS`.
- `MAP_CENTER` is the latitude/longitude origin used when deriving local coordinates.
- `CAMPUS_CONTEXT` contains local-meter polygon rings for the Diag lawn, primary paths, and nearby street/context surfaces.
- Every `BUILDINGS` entry has `{ id, name, category, description, footprint, levels, heightMeters, heightIsEstimate, sources }`; `footprint` is a closed ring of `[x, z]` local-meter pairs and `sources` contains source URLs and accessed fields.

- [ ] Retrieve Diag-area building footprints from OpenStreetMap and verify candidate building names and roles against University of Michigan public pages or campus maps.
- [ ] Keep approximately eight targets from the agreed candidate list where data fits the view; normalize each footprint to local meters relative to `MAP_CENTER` and store it in `src/campusData.js`.
- [ ] Add source URL, retrieval date, source fields, and attribution wording to `docs/umich-diag-map-sources.md`; identify estimated heights/levels in the data.
- [ ] Check coordinate conversion, ring closure, and building coverage by inspecting the resulting data and source notes.
- [ ] Commit with `feat: add Diag campus map data`.

### Task 2: Render and interact with the Diag 3D scene

**Files:**
- Create: `src/CampusScene.jsx`
- Modify: `src/styles.css`

**Interfaces:**
- `CampusScene({ buildings, context, selectedBuildingId, resetCameraKey, onBuildingSelect, onClearSelection })` owns Three.js resources and renders the map.
- Scene selection calls `onBuildingSelect(buildingId)`; empty-ground click calls `onClearSelection()`.
- The scene exports no mutable Three.js objects to React.

- [ ] Build ground, lawn, path, street, and footprint-extrusion meshes from `CAMPUS_CONTEXT` and `BUILDINGS`; use restrained palette and visually distinguish the Diag.
- [ ] Add orbit controls for rotate, pan, zoom, initial Diag framing, and a reset operation keyed by `resetCameraKey`.
- [ ] Add building labels and raycast selection; prevent orbit drags from becoming clicks, highlight `selectedBuildingId`, and clear selection on ground clicks.
- [ ] Dispose geometries, materials, listeners, animation frames, and renderers when the scene unmounts.
- [ ] Commit with `feat: render interactive Diag campus scene`.

### Task 3: Replace the single-building interface with the campus explorer

**Files:**
- Modify: `src/App.jsx`
- Modify: `src/styles.css`
- Modify: `index.html`

**Interfaces:**
- `App` owns `selectedBuildingId` and `resetCameraKey`, resolves the selected object from `BUILDINGS`, and passes stable selection callbacks to `CampusScene`.
- The building list and scene both select by `BUILDINGS[].id`.

- [ ] Replace fictional North Quay copy and floor controls with a Diag/Central Campus heading, overview/reset controls, mapped-building list, selected-building details, and visible OSM attribution.
- [ ] Show the building name, category/role, and floor count in its detail panel; distinguish estimated values from sourced values and show the empty-selection prompt when nothing is selected.
- [ ] Connect list selection, scene selection, and clear-selection behavior to the same React state; keep reset independent from selection.
- [ ] Update page title and description for the UMich Diag campus explorer.
- [ ] Adapt desktop and narrow-screen layout while preserving focus indicators and reduced-motion behavior.
- [ ] Run `npm run build` and fix any build errors.
- [ ] Commit with `feat: build UMich Diag campus explorer interface`.
