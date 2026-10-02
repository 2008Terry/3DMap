// Coordinates are a local orientation model, not survey or navigation data.
// Positive x is east; positive z is south. Source details: docs/umich-diag-map-sources.md.
export const MAP_CENTER = { lat: 42.2772, lon: -83.7385 };

const METERS_PER_DEGREE_LAT = 111_195;
const METERS_PER_DEGREE_LON = METERS_PER_DEGREE_LAT * Math.cos(MAP_CENTER.lat * Math.PI / 180);

const localPoint = (lat, lon) => [
  Number(((lon - MAP_CENTER.lon) * METERS_PER_DEGREE_LON).toFixed(1)),
  Number((-(lat - MAP_CENTER.lat) * METERS_PER_DEGREE_LAT).toFixed(1)),
];

const rectangle = (x, z, width, depth) => {
  const west = Number((x - width / 2).toFixed(1));
  const east = Number((x + width / 2).toFixed(1));
  const north = Number((z - depth / 2).toFixed(1));
  const south = Number((z + depth / 2).toFixed(1));
  return [[west, north], [east, north], [east, south], [west, south], [west, north]];
};

const anchoredRectangle = (lat, lon, width, depth) => {
  const [x, z] = localPoint(lat, lon);
  return rectangle(x, z, width, depth);
};

// Lawn, walkways, and road strips are interpretive context surfaces.
// Their outlines are sketched in local meters and are not OSM polygons.
export const CAMPUS_CONTEXT = {
  diagLawn: [
    [-63, -108], [7, -139], [87, -89], [105, -18], [36, 59],
    [-47, 57], [-92, -14], [-63, -108],
  ],
  paths: [
    { id: 'diag-east-west', footprint: [[-110, -23], [120, -23], [120, -13], [-110, -13], [-110, -23]] },
    { id: 'diag-north-south', footprint: [[-4, -145], [7, -145], [7, 75], [-4, 75], [-4, -145]] },
    { id: 'diag-southwest-northeast', footprint: [[-101, 58], [-94, 65], [104, -110], [97, -117], [-101, 58]] },
  ],
  streets: [
    { id: 'state-street', name: 'State Street', footprint: rectangle(-207, 0, 18, 820) },
    { id: 'north-university', name: 'North University Avenue', footprint: rectangle(0, -174, 810, 17) },
    { id: 'south-university', name: 'South University Avenue', footprint: rectangle(0, 254, 810, 17) },
    { id: 'east-university', name: 'East University Avenue', footprint: rectangle(232, 0, 17, 810) },
  ],
};

const CENTER_SOURCE = {
  url: 'https://github.com/BereZone/umichfreepark/blob/main/src/engine/data/buildings.json',
  accessed: '2026-10-02',
  fields: ['id', 'name', 'lat', 'lon', 'coordSource', 'coordConfidence'],
};

const schematicBuilding = ({ id, name, category, description, lat, lon, width, depth, levels, heightMeters }) => ({
  id,
  name,
  category,
  description,
  center: { lat, lon },
  footprint: anchoredRectangle(lat, lon, width, depth),
  footprintIsEstimate: true,
  levels,
  heightMeters,
  heightIsEstimate: true,
  sources: [CENTER_SOURCE],
});

// The centers below are OSM-derived values from the cited upstream dataset.
// Widths, depths, levels, and heights are illustrative estimates.
export const BUILDINGS = [
  schematicBuilding({
    id: 'angell-hall', name: 'Angell Hall', category: 'Academic',
    description: 'Central Campus academic building facing the Diag.',
    lat: 42.27677, lon: -83.73975, width: 112, depth: 42, levels: 4, heightMeters: 19,
  }),
  schematicBuilding({
    id: 'burton-memorial-tower', name: 'Burton Memorial Tower', category: 'Landmark',
    description: 'Bell tower and campus landmark north of the Diag.',
    lat: 42.27945, lon: -83.73871, width: 22, depth: 22, levels: 10, heightMeters: 59,
  }),
  schematicBuilding({
    id: 'hatcher-graduate-library', name: 'Harlan Hatcher Graduate Library', category: 'Library',
    description: 'Graduate research library beside the Diag.',
    lat: 42.27622, lon: -83.73819, width: 81, depth: 57, levels: 5, heightMeters: 24,
  }),
  schematicBuilding({
    id: 'shapiro-undergraduate-library', name: 'Shapiro Undergraduate Library', category: 'Library',
    description: 'Undergraduate library south of the Diag.',
    lat: 42.27563, lon: -83.73718, width: 65, depth: 50, levels: 5, heightMeters: 22,
  }),
  schematicBuilding({
    id: 'rackham-building', name: 'Rackham Graduate School', category: 'Academic',
    description: 'Graduate school landmark north of the Diag.',
    lat: 42.28062, lon: -83.73726, width: 92, depth: 64, levels: 4, heightMeters: 21,
  }),
  schematicBuilding({
    id: 'michigan-league', name: 'Michigan League', category: 'Campus life',
    description: 'Campus gathering and event building east of the Diag.',
    lat: 42.27932, lon: -83.73756, width: 65, depth: 52, levels: 4, heightMeters: 20,
  }),
  schematicBuilding({
    id: 'hill-auditorium', name: 'Hill Auditorium', category: 'Performance',
    description: 'Performance hall on North University Avenue.',
    lat: 42.27918, lon: -83.73908, width: 67, depth: 60, levels: 4, heightMeters: 24,
  }),
  schematicBuilding({
    id: 'lorch-hall', name: 'Lorch Hall', category: 'Academic',
    description: 'Academic building at the southern edge of the core view.',
    lat: 42.2737, lon: -83.7376, width: 67, depth: 45, levels: 3, heightMeters: 17,
  }),
];
