# 3D internal-structure visibility research

Research date: 2026-10-15. This collection studies how a 2D display can reveal and communicate 3D internal structure across domains. It does not filter methods by the current application stack.

The main finding is that transparency correctness, target visibility, structural legibility, and truthful acquisition of unknown interiors are different problems. The closest candidates to the user's higher-dimensional viewing analogy combine selective disclosure, spatial rearrangement, multiperspective projection, and linked geometric/topological views. No universal all-structures-readable guarantee was established.

## Contents

- Four source-record files: 83 distinct primary-source URLs, with 38 full-text records, 28 abstract/restricted-index records, and 17 official documents. Nineteen research papers/surveys date from 2023–2026.
- `method-families.json`: 16 method families, mechanisms, geometry effects, tradeoffs, and evidence boundaries.
- `obsidian/3D结构透视研究/`: 108 Markdown notes and one native Bases database, including a dashboard, synthesis, comparison matrix, five candidate combinations, evaluation tasks, search log, and source cards.
- `research-protocol.md`: scope, extraction rules, and verification requirements.
- `manifest.json` and `validation.json`: collection counts and structural/publication checks.

The collection was copied into the active Terry's Vault under a new `3D结构透视研究` directory. All 109 published files matched their repository copies by SHA-256; 871 internal links resolved, every note was reachable from the dashboard, and YAML/table-alias checks passed. This does not establish Obsidian rendering or Dropbox synchronization.

## Rebuild and validate

Run `python docs/research/3d-visibility/build_obsidian.py`, then `python docs/research/3d-visibility/validate_collection.py`. The builder writes only the repository staging directory. The validator optionally accepts the published collection directory to compare file hashes. Python 3 and PyYAML are required.

This phase made no application changes, GPU claims, or prototype-validation claims. Search/access gaps and differences between preference, confidence, accuracy, rendering quality, and performance remain explicit in the notes.
