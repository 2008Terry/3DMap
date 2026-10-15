"""Verify research records and links; optionally compare the published vault copy."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import sys
import yaml

root = Path(__file__).resolve().parent
folder = "3D结构透视研究"
collection = root / "obsidian" / folder
notes = list(collection.rglob("*.md"))
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
sources = [s for p in root.glob("*sources.json") for s in json.loads(p.read_text(encoding="utf-8"))["sources"]]
families = json.loads((root / "method-families.json").read_text(encoding="utf-8"))
ids = {s["id"] for s in sources}
assert len(ids) == len(sources) == manifest["sources"]
assert len({s["url"].rstrip("/") for s in sources}) == len(sources)
assert ids == {i for f in families for i in f["source_ids"]}
assert len(notes) == manifest["markdown_notes"]
allowed = {"full-primary", "abstract-primary", "official-doc"}
graph = {}
link_count = 0
source_ids = []
for p in notes:
    text = p.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    assert match, f"missing frontmatter: {p}"
    meta = yaml.safe_load(match[1])
    assert isinstance(meta, dict)
    if meta.get("type") == "research-source":
        assert meta["evidence"] in allowed
        assert meta["source_url"].startswith("https://")
        source_ids.append(meta["id"])
    assert text.count("[[") == text.count("]]"), f"unbalanced links: {p}"
    relative = p.relative_to(collection).as_posix()
    graph[relative] = []
    for raw in re.findall(r"\[\[([^\]]+)\]\]", text):
        target = raw.replace(r"\|", "|").split("|", 1)[0].split("#", 1)[0]
        assert target.startswith(folder + "/"), f"external or ambiguous target: {p}: {target}"
        target = target[len(folder) + 1:]
        if not target.endswith((".md", ".base")):
            target += ".md"
        resolved = collection / target
        assert resolved.is_file(), f"missing link target: {p}: {target}"
        graph[relative].append(target)
        link_count += 1
    for line in text.splitlines():
        if line.startswith("|"):
            assert not re.search(r"\[\[[^\]]*(?<!\\)\|", line), f"table alias pipe: {p}"
assert set(source_ids) == ids and len(source_ids) == len(ids)
base = yaml.safe_load((collection / "来源数据库.base").read_text(encoding="utf-8"))
assert len(base["views"]) == 4
visited = set()
queue = ["00 3D结构透视研究 Dashboard.md"]
while queue:
    name = queue.pop()
    if name in visited:
        continue
    visited.add(name)
    queue.extend(graph.get(name, []))
assert set(graph) <= visited, "unreachable notes"
assert Counter(s["evidence_status"] for s in sources) == manifest["evidence_counts"]
report = {"sources": len(sources), "method_families": len(families), "notes": len(notes),
          "links_resolved": link_count, "unreachable_notes": 0, "yaml_errors": 0,
          "duplicate_source_urls": 0, "table_alias_errors": 0}
if len(sys.argv) > 1:
    published = Path(sys.argv[1])
    assert published.name == folder
    staging_files = {p.relative_to(collection).as_posix(): p for p in collection.rglob("*") if p.is_file()}
    published_files = {p.relative_to(published).as_posix(): p for p in published.rglob("*") if p.is_file()}
    assert set(staging_files) == set(published_files)
    for name, p in staging_files.items():
        assert hashlib.sha256(p.read_bytes()).digest() == hashlib.sha256(published_files[name].read_bytes()).digest(), name
    report["published_files_hash_matched"] = len(staging_files)
    report["published_path"] = str(published)
(root / "validation.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, indent=2))
