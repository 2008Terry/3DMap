# Interactive Building Prototype Design

## Goal

Create a Chinese-language web prototype that makes one fictional campus building easy to understand as a 3D space. The prototype is for exploring spatial interaction: users should be able to inspect floors, rotate the building, and select rooms to learn their identifiers and uses.

## Scope

- Show one procedurally built, fictional four-floor academic building.
- Give each floor a corridor, several rooms, and a small set of shared spaces such as a lounge or service room.
- Label rooms with floor-based identifiers (for example, 101 and 204) and provide a detail view with room name, floor, and use.
- Let users rotate, pan, and zoom the 3D view; choose a floor; spread/collapse the floors; select a room; and reset the camera.
- Keep the interface usable on desktop and narrow mobile screens, with visible keyboard focus and reduced-motion support.

## Experience

The building model is the main focus. A compact floor control sits beside it on wide screens and above it on narrow screens. A room detail panel stays available beside the model or below it on narrow screens. Unselected rooms use restrained floor-specific colors; the selected room gets a clear high-contrast highlight and its room number remains visible in the detail panel. Controls use plain Chinese labels and describe the action they perform.

The memorable interaction is the exploded building: floors separate vertically while retaining their alignment, making room locations and floor relationships visible. Users can move between the overview and a single-floor view without losing their place in the building.

## Technical approach

The repository currently contains project-context documents but no application code or package configuration. Start a small Vite + React app and use Three.js for a real, selectable 3D scene with an orbit camera. Build the building from simple room and corridor meshes in code; do not require external 3D assets, campus data, accounts, or a backend. Keep room metadata in a small local data structure that also drives labels and the detail panel.

## Interaction behavior

- Drag the model to rotate it, use familiar camera controls to pan and zoom, and provide labeled buttons for reset and floor separation.
- Selecting a floor focuses that floor while preserving its vertical context in the building.
- The explode control spreads all floors evenly and toggles back to the assembled view.
- Clicking a room highlights it and updates its detail panel. Clicking empty space clears selection.
- Room numbers follow the floor number, with ground/shared rooms labeled consistently.
- Respect reduced-motion preferences for floor transitions and camera changes.

## Out of scope

Campus-wide maps, routing, indoor positioning, real building plans, live room availability, editing tools, authentication, and hand tracking are not part of this prototype.

## Success criteria

- The page opens to a legible 3D building with four distinguishable floors and visible room numbering.
- Users can rotate and zoom the model, switch the focused floor, assemble or explode the floors, select a room, and reset the view.
- Selecting different rooms updates the displayed room number and use.
- Core controls remain available and readable at desktop and mobile widths.
