# Diag map data and attribution

Accessed 2026-10-02. This is an orientation prototype centered on the University of Michigan Diag. Its visible building outlines, lawn, paths, and street strips are **schematic estimates**. They must not be used for survey work or official navigation.

## Building anchors

The eight named center coordinates in `src/campusData.js` come from [UMichFreePark's buildings.json](https://github.com/BereZone/umichfreepark/blob/main/src/engine/data/buildings.json), accessed 2026-10-02. For each record we used `id`, `name`, `lat`, `lon`, `coordSource`, and `coordConfidence`. The upstream file labels these coordinates `coordSource: "osm"`, identifies OpenStreetMap via Overpass as its source, and reports `lastVerified: "2026-08-07"`. It contains **center points only**; it does not contain building footprint polygons. We could not independently retrieve the underlying OSM ways or University of Michigan building pages in this environment: requests to OSM, Overpass, and maps.umich.edu returned proxy CONNECT 403.

| Upstream ID | Upstream building name | Latitude | Longitude |
| --- | --- | ---: | ---: |
| `angell-hall` | Angell Hall | 42.27677 | -83.73975 |
| `burton-memorial-tower` | Burton Memorial Tower | 42.27945 | -83.73871 |
| `hatcher-graduate-library` | Harlan Hatcher Graduate Library | 42.27622 | -83.73819 |
| `shapiro-undergraduate-library` | Shapiro Undergraduate Library | 42.27563 | -83.73718 |
| `rackham-building` | Rackham Graduate School | 42.28062 | -83.73726 |
| `michigan-league` | Michigan League | 42.27932 | -83.73756 |
| `hill-auditorium` | Hill Auditorium | 42.27918 | -83.73908 |
| `lorch-hall` | Lorch Hall | 42.27370 | -83.73760 |

The names and short role descriptions are orientation copy derived from these names and familiar building functions. Direct verification against University of Michigan pages remains pending because those pages could not be reached. Do not interpret the prose as a verified department or use listing.

## Geometry and estimates

`MAP_CENTER` is 42.2772° N, 83.7385° W. Longitude is projected to eastward local meters using `111195 × cos(center latitude)` meters per degree; latitude uses 111195 meters per degree and is negated so north is negative `z`. The mapped core is roughly 800 meters across. This is a small-area approximation.

Each building's `footprint` is a closed, axis-aligned rectangle centered on its OSM-derived point. Width and depth were selected for legible relative massing, without measurement from a footprint source. Every building sets `footprintIsEstimate: true`. Every `levels` and `heightMeters` value is illustrative; every building sets `heightIsEstimate: true`. The Diag lawn, primary paths, and street surfaces were also sketched for context and have no sourced outline claim.

## Source credits and license

**© OpenStreetMap contributors.** The underlying OSM coordinate data is available under the [Open Database License (ODbL)](https://www.openstreetmap.org/copyright). See [OpenStreetMap](https://www.openstreetmap.org/) and [Overpass API](https://overpass-api.de/) for the upstream source named by UMichFreePark. These citations do **not** mean the estimated outline polygons came from OpenStreetMap.

Eight center records were adapted from [UMichFreePark](https://github.com/BereZone/umichfreepark), [MIT LICENSE](https://github.com/BereZone/umichfreepark/blob/main/LICENSE), copyright (c) 2026 UMichFreePark contributors. The source file was accessed 2026-10-02.

MIT License

Copyright (c) 2026 UMichFreePark contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
