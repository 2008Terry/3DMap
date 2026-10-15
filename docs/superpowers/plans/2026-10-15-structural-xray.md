# Structural xray implementation plan

1. Reproduce on Windows: add a reusable Qt capture harness loading the production MapScene and inspector. Save baseline xray, exploded and indoor frames plus GPU identity under ignored `.superpowers/interior-validation/`.
2. Add failing behavior/geometry tests: Burton catalog (B, 1-10), actual expanded view bounds, preserved modes during floor changes, disjoint room/corridor zones and independent structure geometry. Run these before fixing.
3. Fix material alpha compositing and sRGB conversion, introduce independent ceiling/zone/outline meshes, union wall runs. Update InspectionScene for selected-level xray emphasis and accurate picking.
4. Fit the camera to expanded bounds and viewport FOV, refit on spread/mode/resize. Remove gesture-only mode switching. Add source-bounded Burton profile to generated reference data and its generator.
5. Run native tests, native renderer captures, web tests/build, inspect screenshots and shader logs. Record actual evidence and limitations in the research report, review the diff, commit with Conventional Commits, push and compare remote SHA.

Review focus: alpha accumulation on the View3D texture; closed room access/collision; cut/discard picking; basement elevation and tall exploded framing; preserving interior camera and campus exterior behavior.

Execution: inline in the primary checkout. User's autonomous execution instruction overrides optional design/plan approval pauses. No new worktree.

## Execution record

- Reproduced the white xray on D3D11; intermediate material-only capture removes it before structural changes.
- Catalog/geometry tests observed failing before implementation. Original controller fails the new thumb-mode regression; final controller passes.
- Final review identified shared walls sealing MUTO's door. Added a failing real-building connectivity test, then prioritized corridor-facing edges and subtracted door openings after wall union. Reviewer verified all eight interior mesh cases pass.
- 23 structural/controller/data checks pass; full native suite has the same five legacy/environment failures reproduced from HEAD. Web's six tests and build pass. Reference generation is deterministic and diff whitespace checks pass.
- Final production QML captures: 30 mode/building-wing combinations, six narrow frames, and three Shapiro upper-floor frames reached by actual PageUp events. All five xray frames have zero near-white pixels within the inspection viewport.
- Ruling: keep unsupported walls, circulation and dimensions explicitly schematic. Burton basement catalog comes from user review; official evidence establishes its tenth-floor bell chamber only. No unrelated gesture/runtime changes.
