"""Author the static offline mesh bundle; run after changing source data or mesh code."""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "native"))
from campus_data import load_buildings
from compiled_scene import fingerprints
from environment_data import load_environment
from environment_mesh import build_environment_meshes
from facade_mesh import build_facade_mesh
from geometry_provider import write_geometry_asset
from mesh_builder import build_campus_mesh, build_featured_mesh

folder = ROOT / "native/assets/compiled"
folder.mkdir(parents=True, exist_ok=True)
buildings, _ = load_buildings(ROOT)
generic = [b for b in buildings if not b.featured]
started = time.perf_counter()
meshes = {
    "central": [build_campus_mesh([b for b in generic if b.campus == "Central Campus"])],
    "north": [build_campus_mesh([b for b in generic if b.campus == "North Campus"])],
    "featured": [build_featured_mesh(b) for b in buildings if b.featured],
    "facades": [build_facade_mesh(buildings)],
    "environment": list(build_environment_meshes(load_environment(ROOT), buildings).values()),
}
files = {}
for group, buffers in meshes.items():
    files[group] = []
    for index, mesh in enumerate(buffers):
        name = f"{group}-{index}.meshbin"
        write_geometry_asset(mesh, folder / name)
        files[group].append(name)
(folder / "manifest.json").write_text(json.dumps({"schemaVersion": 1, "inputs": fingerprints(ROOT), "meshes": files}, indent=2) + "\n")
print(f"Compiled {sum(map(len, files.values()))} meshes in {time.perf_counter()-started:.2f}s; {sum(p.stat().st_size for p in folder.glob('*.meshbin'))/1e6:.2f} MB")
