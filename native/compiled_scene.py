"""Load precompiled static campus meshes when their input fingerprints match."""
import hashlib
import json
from pathlib import Path

if __package__:
    from .geometry_provider import geometry_from_asset
else:
    from geometry_provider import geometry_from_asset

INPUTS = ("src/campusBuildings.json", "src/campusBuildingFootprints.json",
          "native/featured_details.json", "native/assets/campus_environment.json",
          "native/campus_data.py", "native/mesh_builder.py", "native/facade_mesh.py",
          "native/environment_mesh.py")


def fingerprints(root):
    return {name: hashlib.sha256((root / name).read_bytes().replace(b"\r\n", b"\n")).hexdigest() for name in INPUTS}


def load_compiled_scene(root):
    folder = root / "native/assets/compiled"
    path = folder / "manifest.json"
    if not path.is_file():
        return None
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("inputs") != fingerprints(root):
        return None
    return {key: [geometry_from_asset(folder / asset) for asset in files]
            for key, files in manifest["meshes"].items()}
