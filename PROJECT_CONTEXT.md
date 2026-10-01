# 3D Map project context

Imported from the ChatGPT cloud project **3D map project** on 2026-10-01. The cloud project's Instructions field was empty and its Sources tab had no attached sources, so the working context below is distilled from its four project chats. The linked chats remain the canonical full conversations; see [CLOUD_CHAT_ARCHIVE.md](CLOUD_CHAT_ARCHIVE.md).

## Product direction

Build a student-first interactive 3D campus map, closer to a campus spatial interface or digital twin than a conventional map. Help students understand the campus and move through it: campus, buildings, floors, rooms, hallways, entrances, stairs, elevators, outdoor paths, and useful campus services. A 3D model alone is not a differentiator; the product should combine spatial understanding with practical student information such as classrooms, study spaces, dining, transit, events, accessibility, and building details where data is available.

The core design problem is spatial comprehension on a 2D screen. Camera controls solve where the viewer is; the product should also help reveal important structures and relationships hidden by occlusion. Treat visibility, relevance, and abstraction as controllable dimensions of the spatial view.

## Interaction principles and candidates

Prefer actions whose physical meaning matches the result. Avoid a large set of hidden gesture shortcuts. Mouse and touch remain useful for precise selection and familiar navigation; richer inputs should make spatial manipulation easier.

Promising interactions from the chats:

- **Dollhouse overview:** inspect and rotate the whole building, then enter floors or rooms.
- **Depth scrubber / clipping:** move a plane through a building to reveal interiors, like scanning a CT volume.
- **Semantic X-ray:** fade geometry based on the selected room, route, floor, or task; avoid making every surface uniformly transparent.
- **Focus lens:** reveal a local interior region while preserving the normal building view elsewhere.
- **Floor explosion / accordion:** spread floors continuously while keeping their spatial context; optionally pull out one floor or peel a facade.
- **Point and ask:** point at a room or feature and ask what it is or how to reach it.
- **Phone motion as a spatial controller:** use ARKit/ARCore tracking to let the viewer move around a virtual building. Webcam hand tracking and gaze are later experiments, not requirements for the first prototype.

A plausible demo sequence is a dollhouse overview, a depth cut, an exploded floor view, and a selected destination revealed through occluding geometry. Candidate interactions should be tested for discoverability and comfort before being treated as product decisions.

## Indoor positioning direction

Represent a user's position as a building and floor plus local coordinates, heading, and confidence, rather than latitude/longitude alone. The chats proposed a hybrid approach:

- GPS/GNSS for outdoor position and initial building detection.
- Wi-Fi fingerprinting for rough indoor location where mapped fingerprints are available.
- IMU / pedestrian dead reckoning for continuous movement, corrected because drift accumulates.
- Barometer readings for relative vertical change and floor-change estimates; absolute altitude by itself is insufficient to identify a floor reliably.
- BLE beacons as optional checkpoints near entrances, stairs, elevators, or major junctions.
- UWB only for high-precision areas where dedicated anchors can be installed.
- Map matching to keep inferred movement within walkable areas and prevent paths through walls.

The suggested progression was GPS + IMU + barometer + building geometry first; Wi-Fi fingerprints next; a small number of BLE checkpoints after that; UWB only when a use case and infrastructure justify it. Treat this as a prototype hypothesis, not a validated deployment plan.

## Competitive position

The research chat found that 3D campus maps already exist, so “campus maps are 2D” is not a sound differentiation claim. It framed the opportunity as joining strengths that are often split across products: high-quality 3D visualization, useful indoor navigation, continuous indoor/outdoor use, and student-first campus information.

- **Concept3D:** mature institutional interactive maps, 3D overlays, tours, wayfinding, and data integrations; strong reference for visualization and campus deployments.
- **MazeMap / Mappedin:** useful references for indoor search, floors, rooms, routing, and indoor/outdoor transitions.
- **NTU Map:** recommended hands-on benchmark for a 3D campus map with indoor plans and campus layers.
- **MGuide:** the closest UMich adjacent product in the research; strong on buildings, rooms, schedules, routes, bus, dining, and study spaces. The product needs a clear answer to why a student would switch or use both.
- **Imperial's campus app:** reference for putting building, floor, room, and student-service information in one institutional interface.
- **OFA:** potentially relevant as a student campus companion. The follow-up corrected the earlier claim that its website provided a clear demo; treat it as a product-direction reference, not a confirmed current 3D visual benchmark.

Potential gap: a student-first spatial experience that combines a comprehensible 3D campus model, indoor/outdoor wayfinding, and timely campus information. Validate this with students and current product evidence before using it as a pitch claim.

## Open questions

- Which student task and user group should anchor the first prototype?
- Which building or campus area has usable floor-plan and room data?
- Which single interaction can be demonstrated reliably on available devices?
- What campus information can be obtained and kept current?
- How should the product complement MGuide rather than duplicate it?

## Source scope

This file is a synthesized handoff, not a verbatim transcript or independent verification of technical or competitor claims. Chat-level summaries and links are in [CLOUD_CHAT_ARCHIVE.md](CLOUD_CHAT_ARCHIVE.md); consult those originals for exact wording and cited sources.
