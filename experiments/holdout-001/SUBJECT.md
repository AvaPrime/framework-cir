# CIR-HOLDOUT-001 subject

Selected after detector freeze. No detector changes after this point until scoring is recorded.

| | |
|---|---|
| Framework | Hugging Face smolagents |
| Version | 1.26.0 |
| Commit | `12c1bc820eca50ace6f80a21d90426d41d74f845` |
| Tag | `v1.26.0` |
| Source | https://github.com/huggingface/smolagents |
| Analyzed tree | `src/` (package only) |
| Detector freeze | `freeze/m1-detectors` @ `13f614143d05b97be4346a60fc4b7f8e80eb3138` |

## Why this subject

- Python, public, pinned release.
- No CIR rule table and no catalog document.
- Mentioned only as a candidate; never reconstructed in this project.
- Small enough that generic analysis finishes; large enough that persistence, tools, and control flow can exist.

Pydantic AI remains in the pool for a later holdout. It was not used to tune detectors.

## Protocol state

- [x] Freeze detectors
- [x] Select subject
- [x] Pin commit
- [x] Run A
- [x] Freeze output (`run-a.json`)
- [ ] Human reference card
- [ ] Score Run A
- [ ] Run B
