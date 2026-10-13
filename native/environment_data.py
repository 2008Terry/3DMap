"""Load the bundled, source-attributed environment without network access."""
from __future__ import annotations

import json
from pathlib import Path


def load_environment(repo_root: Path) -> dict:
    path = Path(repo_root) / "native" / "assets" / "campus_environment.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Unable to read local campus environment at {path}: {error}") from error
    if data.get("schemaVersion") != 1:
        raise ValueError(f"Unsupported campus environment format at {path}")
    for key in ("roads", "paths", "surfaces", "trees", "contextBuildings", "busStops", "sources"):
        if not isinstance(data.get(key), list):
            raise ValueError(f"Missing environment collection {key!r} at {path}")
    return data
