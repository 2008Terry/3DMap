"""Refresh the bundled campus environment from public City GIS and U-M GTFS.

This is an authoring tool. The desktop application never calls these services.
Raw responses are cached outside the repository so an interrupted download can resume.
"""
from __future__ import annotations

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from io import StringIO
import json
from math import cos, radians
from pathlib import Path
import re
import tempfile
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zipfile import ZipFile

from shapely import make_valid
from shapely.geometry import LineString, Point, Polygon, box, mapping, shape
from shapely.ops import transform, unary_union

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = (42.2772, -83.7385)
LAT_SCALE = 111195.0
LON_SCALE = LAT_SCALE * cos(radians(ORIGIN[0]))
ENVELOPE = "-83.755,42.263,-83.684,42.305"
BASE = "https://a2maps.a2gov.org/a2arcgis/rest/services/"
GTFS = "https://webapps.fo.umich.edu/transit_uploads/google_transit.zip"
LAYERS = {
    "roads": ("RoadOwnership/MapServer/0", "OBJECTID,FULLNAME,Lanes,ROADCLASS,Owner,Material", "1=1"),
    "trees": ("TreeInventory/MapServer/0", "OBJECTID,FACILITYID,COMMONNAME,HEIGHT,DBH,Status", "Status = 'Tree Standing'"),
    "parks": ("ParkBoundary/MapServer/0", "OBJECTID,NAME,ParkType", "1=1"),
    "woodlands": ("NaturalFeatures/MapServer/1", "OBJECTID", "1=1"),
    "buildings": ("OSI/BuildingFootprints/FeatureServer/0", "OBJECTID,FacilityID,Bldg_Name,ABG_BLD_HG", "1=1"),
}


def download(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "MichiganCampusMap/1.0 (offline educational visualization)"})
    with urlopen(request, timeout=150) as response:
        return response.read()


def fetch_layer(name: str, cache: Path) -> list[dict]:
    path = cache / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))["features"]
    service, fields, where = LAYERS[name]
    features = []
    offset = 0
    while True:
        params = {
            "f": "geojson", "where": where, "geometry": ENVELOPE,
            "geometryType": "esriGeometryEnvelope", "inSR": "4326", "outSR": "4326",
            "spatialRel": "esriSpatialRelIntersects", "outFields": fields,
            "returnGeometry": "true", "resultOffset": offset, "resultRecordCount": 1000,
            "orderByFields": "OBJECTID", "geometryPrecision": 7,
        }
        result = json.loads(download(BASE + service + "/query?" + urlencode(params)))
        if "error" in result:
            raise RuntimeError(f"{service}: {result['error']}")
        page = result["features"]
        features.extend(page)
        if len(page) < 1000:
            break
        offset += len(page)
    path.write_text(json.dumps({"type": "FeatureCollection", "features": features}), encoding="utf-8")
    print(f"Downloaded {name}: {len(features)}", flush=True)
    return features


def local_point(lon: float, lat: float) -> tuple[float, float]:
    return ((lon - ORIGIN[1]) * LON_SCALE, (ORIGIN[0] - lat) * LAT_SCALE)


def local_geometry(geometry):
    return transform(local_point, make_valid(shape(geometry)))


def members(geometry, types):
    if geometry.is_empty:
        return
    if geometry.geom_type in types:
        yield geometry
    elif hasattr(geometry, "geoms"):
        for part in geometry.geoms:
            yield from members(part, types)


def points(coordinates):
    return [[round(x, 2), round(z, 2)] for x, z, *_ in coordinates]


def rings(polygon):
    return [points(polygon.exterior.coords), *[points(ring.coords) for ring in polygon.interiors]]


def get_osm(cache: Path) -> dict:
    path = cache / "osm.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    query = ('[out:json][timeout:100];('
             'way[highway~"^(footway|path|pedestrian|steps|cycleway)$"](42.263,-83.755,42.305,-83.684);'
             'way[landuse~"^(grass|forest|recreation_ground)$"](42.263,-83.755,42.305,-83.684);'
             'way[natural~"^(wood|water)$"](42.263,-83.755,42.305,-83.684);'
             ');out geom;')
    errors = []
    for endpoint in ("https://overpass.kumi.systems/api/interpreter", "https://overpass-api.de/api/interpreter"):
        try:
            payload = download(endpoint + "?" + urlencode({"data": query}))
            result = json.loads(payload)
            if "remark" in result:
                raise RuntimeError(result["remark"])
            path.write_bytes(payload)
            print(f"Downloaded OSM: {len(result['elements'])}", flush=True)
            return result
        except Exception as error:
            errors.append(str(error))
    raise RuntimeError("Unable to fetch OSM footpaths: " + "; ".join(errors))


def bus_stops(cache: Path, domain) -> list[dict]:
    path = cache / "umich_gtfs.zip"
    if not path.exists():
        path.write_bytes(download(GTFS))
    with ZipFile(path) as archive:
        def table(name):
            return list(csv.DictReader(StringIO(archive.read(name).decode("utf-8-sig"))))
        stops, trips, routes, times = [table(name) for name in ("stops.txt", "trips.txt", "routes.txt", "stop_times.txt")]
        route_names = {route["route_id"]: route.get("route_short_name") or route["route_long_name"] for route in routes}
        trip_routes = {trip["trip_id"]: trip["route_id"] for trip in trips}
        stop_routes: dict[str, set] = {}
        for time in times:
            stop_routes.setdefault(time["stop_id"], set()).add(route_names[trip_routes[time["trip_id"]]])
        result = []
        for stop in stops:
            x, z = local_point(float(stop["stop_lon"]), float(stop["stop_lat"]))
            if domain.covers(Point(x, z)):
                result.append({"id": stop["stop_id"], "name": stop["stop_name"], "position": [round(x, 2), round(z, 2)],
                               "routes": sorted(stop_routes.get(stop["stop_id"], []))})
        return result


def assemble(raw: dict, osm: dict, cache: Path) -> dict:
    campus = json.loads((ROOT / "src" / "campusBuildings.json").read_text(encoding="utf-8"))
    featured = json.loads((ROOT / "src" / "campusBuildingFootprints.json").read_text(encoding="utf-8"))
    campus_parts = [part for building in campus["buildings"] for part in building["parts"]]
    campus_parts.extend(part for parts in featured["buildings"].values() for part in parts)
    facilities = {part.get("facilityId") for part in campus_parts}
    footprints = unary_union([make_valid(Polygon(part["footprint"])) for part in campus_parts])
    region_boxes = []
    for region in campus["regions"]:
        west, south, east, north = region["boundsWgs84"]
        min_x, min_z = local_point(west, north)
        max_x, max_z = local_point(east, south)
        region_boxes.append(box(min_x, min_z, max_x, max_z))
    region = unary_union(region_boxes)
    domain = footprints.buffer(180, quad_segs=3).intersection(region)
    result = {"schemaVersion": 1, "accessed": str(date.today()), "originWgs84": list(ORIGIN),
              "coordinateSystem": "local meters; x east, z south; 111195 meters/degree latitude, longitude scaled by cos(42.2772 degrees)",
              "boundsWgs84": [entry["boundsWgs84"] for entry in campus["regions"]],
              "contextRadiusMeters": 180, "roads": [], "paths": [], "surfaces": [], "trees": [],
              "contextBuildings": [], "busStops": [], "sources": []}
    for name, (service, fields, where) in LAYERS.items():
        result["sources"].append({"id": "city-" + name, "label": "City of Ann Arbor " + name.title(),
                                  "url": BASE + service, "attribution": "City of Ann Arbor",
                                  "query": {"boundsWgs84": ENVELOPE, "outSR": 4326, "fields": fields, "where": where}})
    result["sources"].extend([
        {"id": "osm", "label": "OpenStreetMap campus paths and landcover", "url": "https://www.openstreetmap.org/copyright",
         "attribution": "OpenStreetMap contributors", "license": "Open Database License (ODbL) 1.0",
         "licenseUrl": "https://opendatacommons.org/licenses/odbl/1-0/", "snapshot": osm.get("osm3s", {}).get("timestamp_osm_base", "")},
        {"id": "umich-gtfs", "label": "University of Michigan Transit Services GTFS", "url": GTFS,
         "attribution": "University of Michigan Logistics, Transportation & Parking"},
    ])
    for feature in raw["roads"]:
        props = feature["properties"]
        geometry = local_geometry(feature["geometry"]).intersection(domain).simplify(0.6)
        lane_values = re.findall(r"\d+", str(props.get("Lanes") or ""))
        lanes = min(6, max(1, int(lane_values[0]))) if lane_values else 2
        for segment in members(geometry, {"LineString"}):
            if segment.length > 3:
                result["roads"].append({"id": props["OBJECTID"], "name": props.get("FULLNAME", ""),
                    "points": points(segment.coords), "widthMeters": round(lanes * 3.25 + 1.0, 2), "source": "city-roads"})
    for kind in ("parks", "woodlands"):
        for feature in raw[kind]:
            geometry = local_geometry(feature["geometry"]).intersection(domain).simplify(1.5, preserve_topology=True)
            for polygon in members(geometry, {"Polygon"}):
                if polygon.area > 20:
                    result["surfaces"].append({"id": feature["properties"]["OBJECTID"], "kind": kind,
                        "name": feature["properties"].get("NAME", ""), "rings": rings(polygon), "source": "city-" + kind})
    for feature in raw["trees"]:
        point = local_geometry(feature["geometry"])
        if not domain.covers(point) or footprints.covers(point):
            continue
        props = feature["properties"]
        height_range = str(props.get("HEIGHT") or "")
        values = re.findall(r"\d+", height_range)
        display_height = min(19, max(3.5, sum(map(float, values)) / len(values) * 0.3048)) if values else 8.0
        result["trees"].append({"id": props["OBJECTID"], "species": props.get("COMMONNAME", ""),
            "position": [round(point.x, 2), round(point.y, 2)], "displayHeightMeters": round(display_height, 2),
            "sourceHeightRange": height_range, "source": "city-trees"})
    for feature in raw["buildings"]:
        props = feature["properties"]
        if props.get("FacilityID") in facilities:
            continue
        geometry = local_geometry(feature["geometry"])
        if not domain.intersects(geometry):
            continue
        for polygon in members(geometry.simplify(0.45, preserve_topology=True), {"Polygon"}):
            if polygon.area > 8 and not footprints.intersects(polygon.centroid):
                result["contextBuildings"].append({"id": props["OBJECTID"], "facilityId": props.get("FacilityID", ""),
                    "name": props.get("Bldg_Name") or "Context building", "rings": rings(polygon),
                    "heightMeters": round(max(2.5, float(props.get("ABG_BLD_HG") or 12) * 0.3048), 2), "source": "city-buildings"})
    for element in osm["elements"]:
        coordinates = [local_point(point["lon"], point["lat"]) for point in element.get("geometry", [])]
        if len(coordinates) < 2:
            continue
        tags = element.get("tags", {})
        if "highway" in tags:
            if tags.get("access") in {"private", "no"}:
                continue
            geometry = LineString(coordinates).intersection(domain).simplify(0.35)
            for segment in members(geometry, {"LineString"}):
                if segment.length > 2:
                    result["paths"].append({"id": element["id"], "name": tags.get("name", ""), "kind": tags["highway"],
                        "points": points(segment.coords), "widthMeters": 3.0 if tags["highway"] in {"pedestrian", "cycleway"} else 1.9,
                        "source": "osm"})
        elif len(coordinates) > 3 and coordinates[0] == coordinates[-1]:
            kind = tags.get("natural", tags.get("landuse", "grass"))
            geometry = make_valid(Polygon(coordinates)).intersection(domain).simplify(0.8, preserve_topology=True)
            for polygon in members(geometry, {"Polygon"}):
                if polygon.area > 20:
                    result["surfaces"].append({"id": element["id"], "kind": kind, "name": tags.get("name", ""),
                        "rings": rings(polygon), "source": "osm"})
    result["busStops"] = bus_stops(cache, domain)
    result["stats"] = {key: len(result[key]) for key in ("roads", "paths", "surfaces", "trees", "contextBuildings", "busStops")}
    result["accuracyNotes"] = [
        "Road and footpath centerlines, tree positions, surrounding building footprints, landcover boundaries and bus stops use source coordinates.",
        "Road and path widths are display estimates; tree crowns and height use illustrative shapes (City height ranges interpreted as feet).",
        "Building heights interpret the City's ABG_BLD_HG as feet, consistent with the existing campus model; precise roof forms are not surveyed.",
        "People, benches and shelter shapes are illustrative; they do not describe observed people, seating or shelter inventory.",
        "Bus stop routes are a static GTFS snapshot, not live arrivals or confirmation of current service.",
        "Sources are independent snapshots and may not describe later construction. This visualization is not a navigation or survey product.",
    ]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=Path(tempfile.gettempdir()) / "umich-native-environment")
    parser.add_argument("--output", type=Path, default=ROOT / "native" / "assets" / "campus_environment.json")
    args = parser.parse_args()
    args.cache_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {name: executor.submit(fetch_layer, name, args.cache_dir) for name in LAYERS}
        osm_future = executor.submit(get_osm, args.cache_dir)
        raw = {name: future.result() for name, future in futures.items()}
        osm = osm_future.result()
    data = assemble(raw, osm, args.cache_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(json.dumps(data["stats"], indent=2))
    print(args.output)


if __name__ == "__main__":
    main()
