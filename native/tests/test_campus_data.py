import importlib.util
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "native" / "campus_data.py"


def load_module():
    assert MODULE_PATH.is_file(), "native campus loader has not been implemented"
    spec = importlib.util.spec_from_file_location("campus_data", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_loads_both_campuses_and_featured_building_details():
    module = load_module()

    buildings, extent = module.load_buildings(ROOT)

    assert len(buildings) == 623
    assert {building.campus for building in buildings} == {"Central Campus", "North Campus"}
    angell = next(building for building in buildings if building.id == "angell-hall")
    assert angell.facility_id == "BLD-034824"
    assert angell.featured is True
    assert angell.facts
    assert angell.sources
    assert extent.width > 0 and extent.depth > 0


def test_malformed_building_json_reports_its_path(tmp_path):
    module = load_module()
    source_dir = tmp_path / "src"
    source_dir.mkdir()
    (source_dir / "campusBuildings.json").write_text("{", encoding="utf-8")

    with pytest.raises(ValueError, match="campusBuildings.json"):
        module.load_buildings(tmp_path)


def test_spatial_pick_resolves_a_building_from_the_hit_position():
    module = load_module()
    buildings, _ = module.load_buildings(ROOT)
    building = next(item for item in buildings if not item.featured)
    from shapely.geometry import Polygon

    point = Polygon(building.parts[0]["footprint"]).representative_point()
    picked = module.pick_building((point.x, building.height_m / 2, point.y))

    assert picked is not None
    assert picked.id == building.id
