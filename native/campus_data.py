"""Load the existing campus footprint sources for the native map."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from shapely.geometry import Point, Polygon
from shapely.strtree import STRtree

FEET_TO_METERS = 0.3048
FEATURED_BURTON_HEIGHT_FEET = 192.0
_ACTIVE_INDEX: "_FootprintIndex | None" = None


@dataclass
class Building:
    id: str
    facility_id: str
    name: str
    campus: str
    parts: list[dict[str, Any]]
    height_m: float
    featured: bool = False
    facts: list[str] = field(default_factory=list)
    sources: list[dict[str, str]] = field(default_factory=list)
    category: str = ""
    description: str = ""
    floors: str = ""
    color: str = "#bdb9ab"
    facade_details: dict[str, Any] | None = None
    floor_plan_url: str | None = None

    def to_qml(self) -> dict[str, Any]:
        record = asdict(self)
        record["facadeDetails"] = record.pop("facade_details")
        record["floorPlanUrl"] = record.pop("floor_plan_url")
        record["heightMeters"] = record.pop("height_m")
        return record


@dataclass(frozen=True)
class CampusExtent:
    center_x: float
    center_z: float
    width: float
    depth: float


class _FootprintIndex:
    def __init__(self, buildings: list[Building]):
        self._records: list[tuple[Building, dict[str, Any], Polygon]] = []
        for building in buildings:
            for part in building.parts:
                polygon = Polygon(part["footprint"])
                if polygon.is_valid and not polygon.is_empty:
                    self._records.append((building, part, polygon))
        self._tree = STRtree([record[2] for record in self._records])

    def pick(self, hit_position: tuple[float, float, float]) -> Building | None:
        x, y, z = hit_position
        point = Point(x, z)
        matches: list[Building] = []
        for result in self._tree.query(point):
            building, part, polygon = self._records[int(result)]
            if polygon.covers(point) and -0.05 <= y <= part["height_m"] + 0.05:
                matches.append(building)
        return max(matches, key=lambda item: item.height_m, default=None)


def pick_building(hit_position: tuple[float, float, float]) -> Building | None:
    if _ACTIVE_INDEX is None:
        return None
    return _ACTIVE_INDEX.pick(hit_position)


def _read_json(path: Path) -> Any:
    try:
        with path.open("r", encoding="utf-8") as source:
            return json.load(source)
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to read local campus data at {path}: {error}") from error


def _closed_ring(raw_ring: list[list[float]]) -> list[tuple[float, float]]:
    ring = [(float(point[0]), float(point[1])) for point in raw_ring]
    if ring and ring[0] != ring[-1]:
        ring.append(ring[0])
    return ring


def _source_part(part: dict[str, Any], *, featured: bool = False) -> dict[str, Any]:
    height_feet = float(part.get("heightFeet", part.get("averageHeightFeet", 12.0)))
    return {
        "object_id": str(part.get("objectId", part.get("facilityId", ""))),
        "facility_id": str(part.get("facilityId", "")),
        "footprint": _closed_ring(part["footprint"]),
        "height_m": height_feet * FEET_TO_METERS,
        "height_source": "City average structural height (feet; units inferred)",
        "city_stories": part.get("cityStories"),
        "featured": featured,
    }


def load_buildings(repo_root: Path) -> tuple[list[Building], CampusExtent]:
    global _ACTIVE_INDEX
    repo_root = Path(repo_root)
    city_data = _read_json(repo_root / "src" / "campusBuildings.json")
    featured_footprints = _read_json(repo_root / "src" / "campusBuildingFootprints.json")
    featured_details = _read_json(repo_root / "native" / "featured_details.json")

    buildings_by_id: dict[str, Building] = {}
    for source in city_data["buildings"]:
        parts = [_source_part(part) for part in source["parts"]]
        height_m = max((part["height_m"] for part in parts), default=0.0)
        building = Building(
            id=source["id"],
            facility_id=source.get("facilityId", ""),
            name=source["name"],
            campus=source["campus"],
            parts=parts,
            height_m=height_m,
            category=source["campus"],
            description="建筑轮廓与平均结构高度来自安娜堡市建筑数据。",
            floors="此公开数据快照没有提供楼层数。",
            color="#aebdb9" if source["campus"] == "North Campus" else "#bdb9ab",
            sources=[{
                "label": "City of Ann Arbor Building Footprints",
                "url": featured_footprints["sourceUrl"],
                "datasetUrl": featured_footprints.get("downloadUrl", ""),
                "accessed": featured_footprints.get("accessed", ""),
            }],
        )
        existing = buildings_by_id.get(building.id)
        if existing is None:
            buildings_by_id[building.id] = building
        else:
            existing.parts.extend(building.parts)
            existing.height_m = max(existing.height_m, building.height_m)

    city_source = {
        "label": "City of Ann Arbor Building Footprints",
        "url": featured_footprints["sourceUrl"],
        "datasetUrl": featured_footprints.get("downloadUrl", ""),
        "accessed": featured_footprints.get("accessed", ""),
    }
    for featured_id, details in featured_details.items():
        source_parts = featured_footprints["buildings"].get(featured_id, [])
        parts = [_source_part(part, featured=True) for part in source_parts]
        if not parts:
            raise ValueError(f"Featured building {featured_id!r} has no local footprint data")
        height_m = max(part["height_m"] for part in parts)
        if featured_id == "burton-memorial-tower":
            height_m = FEATURED_BURTON_HEIGHT_FEET * FEET_TO_METERS
            parts[0]["height_m"] = height_m
            parts[0]["height_source"] = "Bentley documented tower height (192 feet)"
        buildings_by_id[featured_id] = Building(
            id=featured_id,
            facility_id=parts[0]["facility_id"],
            name=details["name"],
            campus="Central Campus",
            parts=parts,
            height_m=height_m,
            featured=True,
            facts=details.get("facts", []),
            sources=[city_source, *details.get("sources", [])],
            category=details.get("category", ""),
            description=details.get("description", ""),
            floors=details.get("floors", ""),
            color=details.get("color", "#bdb9ab"),
            facade_details=details.get("facadeDetails"),
            floor_plan_url=details.get("floorPlanUrl"),
        )

    buildings = sorted(buildings_by_id.values(), key=lambda building: (building.campus, building.name.casefold(), building.id))
    points = [point for building in buildings for part in building.parts for point in part["footprint"]]
    if not points:
        raise ValueError("Local campus data contains no building footprint points")
    min_x = min(point[0] for point in points)
    max_x = max(point[0] for point in points)
    min_z = min(point[1] for point in points)
    max_z = max(point[1] for point in points)
    extent = CampusExtent(
        center_x=(min_x + max_x) / 2,
        center_z=(min_z + max_z) / 2,
        width=max_x - min_x,
        depth=max_z - min_z,
    )
    _ACTIVE_INDEX = _FootprintIndex(buildings)
    return buildings, extent
