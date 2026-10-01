# Interactive Building Prototype Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build a Chinese-language web prototype for inspecting one fictional four-floor academic building in 3D.

**Architecture:** Use a small Vite + React app for the interface and local building data. Render room and corridor meshes with Three.js in a dedicated scene component; keep selection, floor focus, explode state, and room details in the React page.

**Tech Stack:** Vite, React, Three.js, CSS.

**Spec:** `docs/superpowers/specs/2026-10-01-interactive-building-design.md`

## Global Constraints

- Show one procedurally built, fictional four-floor academic building.
- Give each floor a corridor, several rooms, and a small set of shared spaces such as a lounge or service room.
- Label rooms with floor-based identifiers (for example, 101 and 204) and provide a detail view with room name, floor, and use.
- Let users rotate, pan, and zoom the 3D view; choose a floor; spread/collapse the floors; select a room; and reset the camera.
- Keep the interface usable on desktop and narrow mobile screens, with visible keyboard focus and reduced-motion support.
- Campus-wide maps, routing, indoor positioning, real building plans, live room availability, editing tools, authentication, and hand tracking are not part of this prototype.

## Review Focus

- A room is selected while another floor is focused; selection and focus must stay coherent.
- Empty-space clicks clear selection without activating a neighboring room.
- Rapidly toggling exploded and assembled views must not leave floors at intermediate offsets.
- Small screens must keep both the model and its controls reachable without horizontal overflow.
- Reduced-motion preferences must skip animated floor and camera transitions.

---

### Task 1: App foundation and fictional building data

**Files:**
- Create: `package.json`
- Create: `index.html`
- Create: `src/main.jsx`
- Create: `src/buildingData.js`
- Create: `src/styles.css`
- Create: `src/App.jsx`

**Interfaces:**
- `src/buildingData.js` exports `FLOORS` and `ROOMS`.
- Each room has `id`, `floor`, `number`, `name`, `use`, `x`, `z`, `width`, and `depth` fields; room IDs are stable strings.
- `App` owns the selected room ID, selected floor, and exploded state, and passes scene controls through explicit props.

- [x] Create a Vite entry point with `dev` and `build` scripts and dependencies on React, React DOM, Three.js, and Vite.
- [x] Define four floors and at least four numbered rooms per floor, including classrooms, a study room, and one shared space; use consistent floor-based numbers such as `101` and `204`.
- [x] Create the Chinese page shell with a building title, floor controls, an empty scene area, an explode/reset control area, and a room detail panel.
- [x] Add the initial responsive layout, type and color tokens, visible keyboard focus, and reduced-motion CSS rules.
- [x] Confirm the app entry renders the page shell and that the four-floor data is available to `App`.

### Task 2: Procedural 3D building scene

**Files:**
- Create: `src/BuildingScene.jsx`
- Modify: `src/App.jsx`
- Modify: `src/styles.css`

**Interfaces:**
- `BuildingScene({ rooms, selectedFloor, selectedRoomId, exploded, onRoomSelect, onClearSelection })` renders the building and forwards room selection by stable room ID.
- `App` consumes `onRoomSelect(roomId)` and `onClearSelection()` to update the selected room detail.

- [x] Build floor slabs, corridors, room meshes, and shared spaces from `ROOMS` and fixed floor dimensions; do not load external models.
- [x] Add an orbit camera with pointer rotation, pan, zoom, and a reset operation exposed to the page controls.
- [x] Add room-number labels that remain readable in the assembled and exploded views.
- [x] Use raycasting to select a room mesh; clicking empty scene space calls `onClearSelection`.
- [x] Apply a clear selected-room highlight and visually de-emphasize rooms outside `selectedFloor` while preserving their vertical context.
- [x] Animate floors between aligned and evenly separated heights, and immediately apply target positions when reduced motion is enabled.
- [x] Ensure a new explode target cancels or replaces an in-progress transition so repeated toggles settle at the latest state.
- [x] Confirm the scene shows four floors, room labels, and the selected floor state.

### Task 3: Complete page interactions and responsive finish

**Files:**
- Modify: `src/App.jsx`
- Modify: `src/styles.css`
- Modify: `src/BuildingScene.jsx`

**Interfaces:**
- Floor controls set `selectedFloor` to a floor ID or `null` for the overview.
- The explode control toggles `exploded`; reset restores the camera without changing the selected room or floor.
- The detail panel resolves the current room from `ROOMS` and shows number, name, floor, and use.

- [x] Connect the floor selector, explode toggle, and camera reset controls to scene props.
- [x] Keep a selected room visible in the detail panel when the focused floor changes; clear it only when the user selects empty scene space.
- [x] Show a useful empty-selection message and room-specific details after selection.
- [x] Confirm clicking empty scene space clears selection and does not select an adjacent room.
- [x] Complete narrow-screen layout so controls and details remain reachable around the 3D scene.
- [x] Confirm the page fits a narrow mobile viewport without horizontal overflow.
- [x] Confirm keyboard focus is visible on all controls and reduced-motion settings bypass scene transitions.

## Implementation note

Do not add or run automated tests for this plan. Keep the implementation focused on the stated prototype scope.
