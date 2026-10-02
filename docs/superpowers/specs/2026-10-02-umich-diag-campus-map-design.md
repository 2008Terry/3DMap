# UMich Diag Campus Explorer Design

## Goal

Replace the fictional single-building demo as the app's primary view with a Chinese-language, interactive 3D map of the University of Michigan's Central Campus around the Diag. The map should help a visitor recognize the Diag and nearby landmark buildings, inspect the area from different angles, and select a building to see concise information.

## Agreed scope

- Center the scene on the Diag and cover an approximately 700–800 meter-wide core area, using the vicinity of Huron Street, State Street, Hill Street, and Fletcher Street as orientation bounds.
- Include about eight nearby, recognizable buildings. The initial candidates are Angell Hall, Burton Memorial Tower, Hatcher Graduate Library, Shapiro Library, Rackham Graduate School, Michigan League, Hill Auditorium, and Lorch Hall. Keep the final set limited to buildings that fit the selected view and have usable footprint data.
- Show the Diag lawn, main paths, and adjacent streets as simple context geometry.
- Use actual building footprints where available. Extrude them to approximate heights; add only a small amount of silhouette detail where it materially improves recognition.
- Reuse the existing Vite, React, and Three.js stack and the current Chinese interface style.
- Make the initial scene and building data local to the repository. Do not require a map API key or a live map service at runtime.

## Data and attribution

- Source building footprints from OpenStreetMap where coverage is usable, and use University of Michigan public campus/building information to verify names and basic descriptions.
- Store the resulting, scoped geometry as local project data so the map loads without external requests.
- Prefer published building height or floor-count metadata. Where it is absent, use a documented visual estimate and keep it distinguishable from sourced values in the data.
- Record source URLs, access date, and the source field used for each building in the project data or an accompanying attribution note. Display OpenStreetMap attribution in the interface and include the required ODbL attribution wording.
- Treat the map as an orientation prototype, not a survey-grade or official navigation map.

## Experience and interactions

- The opening view frames the Diag and its selected nearby buildings from an elevated, angled camera.
- Users can orbit by dragging, zoom with the wheel or pinch, and pan the view. A clearly labeled reset control returns to the overview camera.
- Clicking a building or its accessible label highlights it and opens a detail card with its name, building type or campus role, and sourced or estimated floor count when available.
- An accessible list of the mapped buildings provides a keyboard-operable way to select the same targets. Selecting a building from either the scene or list keeps the selection synchronized.
- Clicking empty ground clears the current selection. The detail panel then returns to a short prompt.
- Labels should remain legible without covering the Diag or one another excessively. The selected building's label and details take priority when the view is crowded.
- On narrow screens, keep the 3D scene above a scrollable building list/detail area; retain reachable camera controls and avoid horizontal overflow.
- Use the established Chinese visual language, with English building names as the authoritative labels and concise Chinese descriptions where appropriate.

## Technical design

- Replace the current app content/data with a Diag-area campus explorer. Keep Three.js scene setup in a dedicated component and keep selection and detail state in React.
- Store each mapped building as an ID, official/display name, category or short description, footprint polygon, height or floor estimate, estimate/source status, and provenance.
- Convert source latitude/longitude coordinates to a local meter-based coordinate system centered near the Diag before creating Three.js geometry. This avoids rendering campus coordinates at their raw geographic scale.
- Build footprints as extruded meshes and give the Diag, paths, streets, and ground separate, restrained materials. Use raycasting for 3D selection and keep accessible DOM controls outside the canvas.
- Use shared selection callbacks so scene clicks and the accessible list update the same React state. Keep reset camera behavior independent of selection.
- Preserve responsive layout and reduced-motion support. Avoid continuous floor animation and avoid introducing indoor-floor or room behavior into this campus-area view.

## Out of scope

- Full-campus coverage beyond the Diag-area view.
- Interior building geometry, rooms, floor selection, or floor explosion.
- Routing, live room/service information, indoor positioning, geolocation, accounts, backend services, or map editing.
- Runtime loading of third-party map tiles or dependence on a commercial map token.
- Detailed photorealistic facade or roof modeling.

## Acceptance criteria

- The default page presents the Diag-centered Central Campus area rather than the fictional North Quay building.
- The scene contains a recognizable lawn/path/street layout and a small set of actual nearby building footprints.
- The camera can orbit, pan, zoom, and reset.
- A user can select every mapped building using either the 3D scene or accessible list, see its information, and clear the selection by clicking empty ground.
- The layout remains usable on desktop and narrow mobile widths, with visible keyboard focus and reduced-motion support.
- Map geometry and details load from local project data, and visible source attribution is present.
