# UMich Diag map data and attribution

Accessed 2026-10-10. The eight selectable campus targets use building polygons from the City of Ann Arbor's public **Building Footprints** dataset. The overview also includes 260 campus building-footprint outlines from the portal GeoJSON, updated October 4, 2026. The lawn, paths, and street strips remain schematic orientation context and are not survey or navigation data.

## Central Campus overview footprints

- Source: https://data.a2gov.org/@city-of-ann-arbor/building-footprints (GeoJSON resource `AA_Building_Footprints.json`, updated October 4, 2026).
- `src/campusContextFootprints.json` contains the campus-owned features whose average exterior-ring coordinate falls within WGS84 bounds `[-83.751, 42.268, -83.721, 42.288]`, plus records named with a `UM ` prefix. The 11 FacilityIDs used by the eight selectable targets are excluded to avoid drawing duplicate outlines.
- These 260 contextual outlines are flat and non-selectable. The city source's height field is not used for them; detailed 3D models and building facts remain limited to the eight selected targets.
- The bounds are a regional overview extent around the Central Campus academic core and adjacent university areas. They do not imply an official survey boundary. U-M Campus Plan 2050 describes Central Campus as several connected sub-campus areas; its framework page is https://campusplan2050.umich.edu/plans-and-maps/central-campus/.

## City building geometry

- Dataset page: https://data.a2gov.org/@city-of-ann-arbor/building-footprints
- Feature service: https://a2maps.a2gov.org/a2arcgis/rest/services/OSI/BuildingFootprints/FeatureServer/0
- Current records were queried by `FacilityID` with WGS84 output (`outSR=4326`) on 2026-10-02. The August 31, 2026 downloadable GeoJSON snapshot has older names and does not expose all current service fields, so the app's compact geometry file was generated from the live City feature service response.
- City metadata says the outlines were generated semi-automatically from 2009 LiDAR and 2005–2008 orthophotography, quality checked, and later updated from construction plans and checked against newer aerial imagery. The City page lists the dataset as updated August 31, 2026.
- The City layer credits Woolpert and City of Ann Arbor Community Services. The data page does not expose a license label, so this project records attribution without claiming a particular open-data license.
- Geometry is simplified by at most 0.35 local meters for compact rendering and projected into the existing local-meter scene around `MAP_CENTER` using the WGS84 latitude/longitude values returned by the service. Source `FacilityID`, current `Bldg_Name`, `ABG_BLD_HG`, and `STORIES` values are preserved in `src/campusBuildingFootprints.json`.
- `ABG_BLD_HG` is described by the City as average structure height. Its unit is not separately declared in the layer schema. The project interprets the values as international feet for extrusion: the layer's coordinate system uses international feet, and Burton Tower's value of 120 matches the University's published 120-foot bell-chamber floor height. This is a documented interpretation, not a City-declared field unit. Burton Tower's displayed model height instead uses the University's 192-foot overall-height figure; the City average field remains preserved.
- The City `STORIES` values are retained per footprint component. They are not blindly promoted to one building-wide fact. Where University materials disagree, the detail panel names both values and the model does not add guessed floor bands.

## Matched City records

| Map building | City `FacilityID` | Current City name | City average height field | City stories |
| --- | --- | --- | ---: | ---: |
| Angell Hall | `BLD-034824` | UM Angell Hall | 70 ft | 4 |
| Angell Hall auditoriums | `BLD-034821` | UM Angell Hall | 25 ft | 1 |
| Burton Memorial Tower | `BLD-000825` | UM Burton Memorial Tower | 120 ft | 13 |
| Hatcher North | `BLD-034813` | UM Hatcher Graduate Library | 55 ft | 4 |
| Hatcher South | `BLD-034814` | UM Hatcher Graduate Library | 85 ft | 8 |
| Hatcher connector | `BLD-034815` | UM Hatcher Graduate Library | 12 ft | 1 |
| Shapiro Library | `BLD-034816` | UM Shapiro Library | 59.526 ft | 4 |
| Rackham | `BLD-021687` | UM HW Rackham Building | 82.118 ft | 3 |
| Michigan League | `BLD-000026` | UM Michigan League / Mendelssohn | 54.860 ft | 3 |
| Hill Auditorium | `BLD-008864` | UM Hill Auditorium | 60 ft | 3 |
| Lorch Hall | `BLD-008871` | UM Lorch Hall | 54.938 ft | 4 |

The current City service names Angell's attached auditorium polygon as Angell Hall. Three Hatcher polygons, including a narrow connector, are kept together as one library selection. The separate Mason Hall polygons were excluded.

## University materials used for visible facts and floor-plan links

- Angell Hall: https://sites.lsa.umich.edu/greekcampus/centralcampus/angell-hall/ and https://bentley.umich.edu/wp-content/uploads/2014/09/University_of_Michigan_History_Subject_Guide.pdf. The sources describe the eight-column classical facade and four-story building.
- Burton Memorial Tower: https://bentley.umich.edu/discover/bentley-materials/campus-tour/building-index/burton-tower/ and https://milproj.dc.umich.edu/mort/central/north%20of%20north%20u/Burton%20Tower/index.html. Bentley gives 192 feet overall; the historical survey describes ten floors plus a basement, while the City `STORIES` record says 13.
- Hatcher Library: https://www.lib.umich.edu/locations-and-hours/hatcher-library/navigating-building/. The page describes North full floors 1–4 plus basement and A floors, South floors 1–8, their level-2 connection, and links to official floor plans.
- Shapiro Library: https://www.lib.umich.edu/locations-and-hours/shapiro-library/. The official page links to published floor plans.
- Rackham: https://umaec.umich.edu/projects/completed-projects/horace-h-rackham-school-of-graduate-studies-building/ and https://rackham.umich.edu/about/rackham-building/history-of-the-rackham-building/. U-M describes a five-story limestone building with copper roof and terraces at levels 2 and 4; the City record says 3 stories.
- Michigan League: https://milproj.dc.umich.edu/mort/central/north%20of%20north%20u/Michigan%20League/index.html. The U-M history describes five floors, red brick with white trim, dormer and casement windows, alcoves, and balconies; the City record says 3 stories.
- Hill Auditorium: https://news.umich.edu/history-of-hill-auditorium/ and https://umaec.umich.edu/projects/completed-projects/hill-auditorium-renovation/design/. U-M describes a four-story brick building, its entrance columns and facade bands, and publishes design/elevation materials; the City record says 3 stories.
- Lorch Hall: https://milproj.dc.umich.edu/mort/central/south%20of%20south%20U/Lorch%20Hall/index.html and https://umaec.umich.edu/projects/major-projects/lorch-hall-renovation-and-addition/project-details/. Historical materials describe four-story wings, brick, slate roofs, and arched upper windows. U-M lists a renovation/addition with construction beginning in spring 2026 and estimated completion in winter 2030, so this snapshot may not represent the final project design.

Only directly supported facts and source links appear in building details. Shapiro has no exterior-architecture claim because the linked library page provides floor plans but no such description. The U-M Angell Hall page confirms eight Doric columns and a classical entablature and provides facade photographs. The scene represents those columns and the visible window bays behind them on the east edge of the matching City footprint; this maps the photographed entrance onto the campus footprint, and is not a surveyed facade coordinate. Hill's four columns and floor-band descriptions come from the U-M News source; the model places this feature on the south frontage. Both facade studies use schematic dimensions based on the City footprint and average-height extrusion, not measured construction dimensions. The other cited exterior features remain descriptive text because available sources do not provide sufficiently precise placement and size for this map. No internal rooms are synthesized. The current selection provides official floor-plan links where the University's public pages make plans available.
