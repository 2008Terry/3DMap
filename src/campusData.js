import sourceFootprints from './campusBuildingFootprints.json';
import campusContextSource from './campusContextFootprints.json';

// Local orientation origin for the City of Ann Arbor WGS84 building outlines.
export const MAP_CENTER = { lat: 42.2772, lon: -83.7385 };

const METERS_PER_DEGREE_LAT = 111_195;
const METERS_PER_DEGREE_LON = METERS_PER_DEGREE_LAT * Math.cos(MAP_CENTER.lat * Math.PI / 180);

const rectangle = (x, z, width, depth) => {
  const west = Number((x - width / 2).toFixed(1));
  const east = Number((x + width / 2).toFixed(1));
  const north = Number((z - depth / 2).toFixed(1));
  const south = Number((z + depth / 2).toFixed(1));
  return [[west, north], [east, north], [east, south], [west, south], [west, north]];
};

// Context outlines remain schematic; building footprints come from the cited City dataset.
export const CAMPUS_CONTEXT = {
  buildings: campusContextSource.buildings,
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
    { id: 'state-street', name: 'State Street', footprint: rectangle(-207, 0, 18, 2400) },
    { id: 'north-university', name: 'North University Avenue', footprint: rectangle(0, -174, 1800, 17) },
    { id: 'south-university', name: 'South University Avenue', footprint: rectangle(0, 254, 1800, 17) },
    { id: 'east-university', name: 'East University Avenue', footprint: rectangle(232, 0, 17, 810) },
  ],
};

const CITY_SOURCE = {
  label: 'City of Ann Arbor Building Footprints',
  url: sourceFootprints.sourceUrl,
  datasetUrl: sourceFootprints.downloadUrl,
  accessed: sourceFootprints.accessed,
};

const UNIVERSITY_SOURCES = {
  angell: { label: 'Angell Hall architecture', url: 'https://sites.lsa.umich.edu/greekcampus/centralcampus/angell-hall/' },
  angellFloors: { label: 'U-M campus buildings guide', url: 'https://bentley.umich.edu/wp-content/uploads/2014/09/University_of_Michigan_History_Subject_Guide.pdf' },
  burton: { label: 'Burton Tower details', url: 'https://bentley.umich.edu/discover/bentley-materials/campus-tour/building-index/burton-tower/' },
  burtonHistory: { label: 'Burton Tower historical description', url: 'https://milproj.dc.umich.edu/mort/central/north%20of%20north%20u/Burton%20Tower/index.html' },
  hatcher: { label: 'Hatcher floor information and official plans', url: 'https://www.lib.umich.edu/locations-and-hours/hatcher-library/navigating-building/' },
  shapiro: { label: 'Shapiro floor plans', url: 'https://www.lib.umich.edu/locations-and-hours/shapiro-library/' },
  rackham: { label: 'Rackham building facts', url: 'https://umaec.umich.edu/projects/completed-projects/horace-h-rackham-school-of-graduate-studies-building/' },
  rackhamHistory: { label: 'Rackham architectural history', url: 'https://rackham.umich.edu/about/rackham-building/history-of-the-rackham-building/' },
  league: { label: 'Michigan League historical architecture', url: 'https://milproj.dc.umich.edu/mort/central/north%20of%20north%20u/Michigan%20League/index.html' },
  hill: { label: 'Hill Auditorium exterior and floor details', url: 'https://news.umich.edu/history-of-hill-auditorium/' },
  hillDesign: { label: 'Hill Auditorium official elevations and design', url: 'https://umaec.umich.edu/projects/completed-projects/hill-auditorium-renovation/design/' },
  lorch: { label: 'Lorch Hall historical architecture', url: 'https://milproj.dc.umich.edu/mort/central/south%20of%20south%20U/Lorch%20Hall/index.html' },
  lorchProject: { label: 'Lorch Hall renovation and addition', url: 'https://umaec.umich.edu/projects/major-projects/lorch-hall-renovation-and-addition/project-details/' },
};

const cityParts = (id) => sourceFootprints.buildings[id].map((part) => ({
  ...part,
  // The city's height field is stored in feet; this is only an extrusion height, not a roof survey.
  heightMeters: id === 'burton-memorial-tower'
    ? 192 * 0.3048
    : part.averageHeightFeet * 0.3048,
}));

const building = ({ id, name, category, description, floors, facts, sources, floorPlanUrl, facadeDetails, color }) => {
  const parts = cityParts(id);
  const maxHeight = Math.max(...parts.map((part) => part.heightMeters));
  return {
    id,
    name,
    category,
    description,
    parts,
    footprint: parts[0].footprint,
    heightMeters: maxHeight,
    heightLabel: id === 'burton-memorial-tower'
      ? '192 英尺（Bentley 记录的塔楼总高）'
      : `市数据平均结构高度 ${Math.max(...parts.map((part) => part.averageHeightFeet)).toFixed(1)} 英尺`,
    floors,
    facts,
    facadeDetails,
    sources: [CITY_SOURCE, ...sources],
    floorPlanUrl,
    color,
  };
};

export const BUILDINGS = [
  building({
    id: 'angell-hall', name: 'Angell Hall', category: 'Academic',
    description: '密歇根大学中央校区的古典风格建筑。',
    floors: '主楼 4 层；市数据将 Auditorium 部件记为 1 层。',
    facts: ['主立面有 8 根多立克柱和古典檐部；校方照片显示柱廊后方有窗面。'],
    sources: [UNIVERSITY_SOURCES.angell, UNIVERSITY_SOURCES.angellFloors],
    facadeDetails: {
      side: 'east', targetFacilityId: 'BLD-034824', columns: 8, windowBays: 7, source: UNIVERSITY_SOURCES.angell,
    },
    color: '#b8b2a4',
  }),
  building({
    id: 'burton-memorial-tower', name: 'Burton Memorial Tower', category: 'Landmark',
    description: '以钟楼和校园钟琴闻名的地标。',
    floors: '楼层口径不一致：市数据记录 13 stories；密歇根大学历史资料记为地下室加 10 层。',
    facts: ['外墙为石灰岩；钟楼总高按 Bentley 资料显示为 192 英尺。'],
    sources: [UNIVERSITY_SOURCES.burton, UNIVERSITY_SOURCES.burtonHistory],
    color: '#c4c0b6',
  }),
  building({
    id: 'hatcher-graduate-library', name: 'Harlan Hatcher Graduate Library', category: 'Library',
    description: '由相连的 Hatcher North 与 Hatcher South 两部分组成。',
    floors: 'North：地下室、1–4 层及 A 半层；South：1–8 层。',
    facts: ['North 与 South 在第 2 层相连；第 4 层可通往两侧书库。'],
    sources: [UNIVERSITY_SOURCES.hatcher],
    floorPlanUrl: UNIVERSITY_SOURCES.hatcher.url,
    color: '#b9c0bb',
  }),
  building({
    id: 'shapiro-undergraduate-library', name: 'Shapiro Undergraduate Library', category: 'Library',
    description: '位于 Diag 南侧的本科图书馆。',
    floors: '市建筑图层记录 4 stories；校方提供逐层平面图。',
    facts: [],
    sources: [UNIVERSITY_SOURCES.shapiro],
    floorPlanUrl: UNIVERSITY_SOURCES.shapiro.url,
    color: '#aaaead',
  }),
  building({
    id: 'rackham-building', name: 'Rackham Graduate School', category: 'Academic',
    description: '1938 年建成的研究生院建筑。',
    floors: '校方资料称 5 层；市图层该建筑记录 3 stories，数值有差异。',
    facts: ['印第安纳石灰岩外墙、铜屋顶；第 2 与第 4 层设外部露台。'],
    sources: [UNIVERSITY_SOURCES.rackham, UNIVERSITY_SOURCES.rackhamHistory],
    color: '#c3bba8',
  }),
  building({
    id: 'michigan-league', name: 'Michigan League', category: 'Campus life',
    description: '带有多翼体量的校园活动建筑。',
    floors: '校方历史资料称地上 5 层；市图层记录 3 stories，数值有差异。',
    facts: ['红砖与白色石材饰边；资料提到老虎窗、平开窗和阳台。'],
    sources: [UNIVERSITY_SOURCES.league],
    color: '#a87560',
  }),
  building({
    id: 'hill-auditorium', name: 'Hill Auditorium', category: 'Performance',
    description: '以大型演出空间和南立面入口著称。',
    floors: '校方资料称 4 层；市图层记录 3 stories，数值有差异。',
    facts: ['南立面入口有 4 根多立克柱；楼层之间有石质或陶土腰线。'],
    sources: [UNIVERSITY_SOURCES.hill, UNIVERSITY_SOURCES.hillDesign],
    facadeDetails: {
      side: 'south', targetFacilityId: 'BLD-008864', columns: 4, stringcourses: [0.28, 0.76], source: UNIVERSITY_SOURCES.hill,
    },
    color: '#a66d59',
  }),
  building({
    id: 'lorch-hall', name: 'Lorch Hall', category: 'Academic',
    description: '历史建筑轮廓来自安娜堡市建筑数据。',
    floors: '历史资料记载原建筑各翼为 4 层；校园图层记录 4 stories。',
    facts: ['历史资料描述砖墙、石板坡屋顶及拱形大窗。校方正在推进翻修与扩建。'],
    sources: [UNIVERSITY_SOURCES.lorch, UNIVERSITY_SOURCES.lorchProject],
    color: '#a87560',
  }),
];
