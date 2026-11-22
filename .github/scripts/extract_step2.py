#!/usr/bin/env python3
"""One-time, deterministic extraction of the game files from the pinned ROZA commit."""
from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path

SOURCE_ROOT = Path(os.environ["NEXUS_SOURCE_ROOT"]).resolve()
SOURCE_COMMIT = os.environ["NEXUS_SOURCE_COMMIT"]
DEST_ROOT = Path.cwd().resolve()

def destination(path: str) -> str | None:
    if path == "firmware/LICENSE":
        return "LICENSE"
    if path.startswith("firmware/src/hawkins_llm/"):
        return "src/narrator/hawkins_llm/" + path.removeprefix("firmware/src/hawkins_llm/")
    if path.startswith("firmware/src/hawkins_app."):
        return "src/platform/cardputer/legacy/" + path.removeprefix("firmware/src/")
    if path.startswith("firmware/src/hawkins_exploration."):
        return "src/exploration/" + path.removeprefix("firmware/src/")
    if path.startswith(("firmware/src/hawkins_ai_protocol.",
                        "firmware/src/hawkins_narrative_memory.",
                        "firmware/src/hawkins_narrative_memory_codec.",
                        "firmware/src/hawkins_narrative_store.")):
        return "src/narrator/" + path.removeprefix("firmware/src/")
    if path.startswith(("firmware/src/hawkins_adventure_store.",
                        "firmware/src/hawkins_save_codec.",
                        "firmware/src/hawkins_sd_backup.",
                        "firmware/src/hawkins_nvs.")):
        return "src/storage/" + path.removeprefix("firmware/src/")
    if path.startswith("firmware/src/hawkins_") and path.endswith((".cpp", ".h")):
        return "src/core/" + path.removeprefix("firmware/src/")
    if path.startswith("firmware/tools/hawkinstest/"):
        return "tests/hawkinstest/" + path.removeprefix("firmware/tools/hawkinstest/")
    if path.startswith("firmware/tools/hawkinsllmtest/"):
        return "tests/hawkinsllmtest/" + path.removeprefix("firmware/tools/hawkinsllmtest/")
    if path.startswith("firmware/tools/hawkinsaitest/"):
        return "tests/hawkinsaitest/" + path.removeprefix("firmware/tools/hawkinsaitest/")
    if path.startswith("firmware/tools/hawkinsllm/"):
        return "tools/model/" + path.removeprefix("firmware/tools/hawkinsllm/")
    if path.startswith("firmware/docs/hawkins"):
        return "docs/source-notes/firmware/" + path.removeprefix("firmware/docs/")
    if path.startswith("docs/HAWKINS"):
        return "docs/source-notes/project/" + path.removeprefix("docs/")
    if path.startswith("docs/NEXUS_MIGRATION_STEP"):
        return "docs/migration/" + path.removeprefix("docs/")
    return None

copied: list[str] = []
for source in sorted(SOURCE_ROOT.rglob("*")):
    if not source.is_file():
        continue
    rel = source.relative_to(SOURCE_ROOT).as_posix()
    target_rel = destination(rel)
    if target_rel is None:
        continue
    target = DEST_ROOT / target_rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    copied.append(target_rel)

# Keep the assembler include paths valid after moving the model directory.
model_asm = DEST_ROOT / "src/narrator/hawkins_llm/model_data.S"
text = model_asm.read_text(encoding="utf-8")
text = text.replace('"src/hawkins_llm/assets/', '"src/narrator/hawkins_llm/assets/')
model_asm.write_text(text, encoding="utf-8")

# Repoint the native harnesses to the new source layout.
test_script = DEST_ROOT / "tests/hawkinstest/build.sh"
text = test_script.read_text(encoding="utf-8")
text = text.replace("-I ../../src ", "-I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator ")
for old, new in {
    "../../src/hawkins_world.cpp": "../../src/core/hawkins_world.cpp",
    "../../src/hawkins_save_codec.cpp": "../../src/storage/hawkins_save_codec.cpp",
    "../../src/hawkins_exploration.cpp": "../../src/exploration/hawkins_exploration.cpp",
    "../../src/hawkins_character.cpp": "../../src/core/hawkins_character.cpp",
    "../../src/hawkins_missions.cpp": "../../src/core/hawkins_missions.cpp",
    "../../src/hawkins_adventure.cpp": "../../src/core/hawkins_adventure.cpp",
    "../../src/hawkins_narrative_memory.cpp": "../../src/narrator/hawkins_narrative_memory.cpp",
    "../../src/hawkins_narrative_memory_codec.cpp": "../../src/narrator/hawkins_narrative_memory_codec.cpp",
}.items():
    text = text.replace(old, new)
test_script.write_text(text, encoding="utf-8")

llm_script = DEST_ROOT / "tests/hawkinsllmtest/build.sh"
text = llm_script.read_text(encoding="utf-8")
text = text.replace("../../src/hawkins_llm", "../../src/narrator/hawkins_llm")
llm_script.write_text(text, encoding="utf-8")

ai_script = DEST_ROOT / "tests/hawkinsaitest/build.sh"
text = ai_script.read_text(encoding="utf-8")
text = text.replace("-I ../../src -I", "-I ../../src -I ../../src/core -I ../../src/narrator -I")
text = text.replace("../../src/hawkins_ai_protocol.cpp", "../../src/narrator/hawkins_ai_protocol.cpp")
ai_script.write_text(text, encoding="utf-8")

# Validate the two shipped model payloads before recording the extraction.
assets = DEST_ROOT / "src/narrator/hawkins_llm/assets"
expected: dict[str, str] = {}
for line in (assets / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
    if line.strip():
        digest, filename = line.split(maxsplit=1)
        expected[filename.strip()] = digest
for filename, digest in expected.items():
    actual = hashlib.sha256((assets / filename).read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f"SHA-256 mismatch for {filename}: expected {digest}, got {actual}")

# The UI controller is retained as a legacy host adapter; ROZA drivers are deliberately not copied.
platform_readme = DEST_ROOT / "src/platform/cardputer/README.md"
platform_readme.parent.mkdir(parents=True, exist_ok=True)
platform_readme.write_text(
    "# Cardputer host boundary\n\n"
    "`legacy/` contains the extracted ROZA game screen/controller as a migration reference. "
    "It still includes ROZA-owned headers and globals (UI, SD and GNSS) and is not an independent "
    "build target yet. Step 4 will replace these direct dependencies with explicit Nexus platform "
    "interfaces and a thin ROZA adapter. Do not copy the ROZA display, keyboard, SD, GNSS or LoRa "
    "drivers into this repository.\n",
    encoding="utf-8",
)

(DEST_ROOT / "docs/PROVENANCE.md").write_text(
    "# Extraction provenance\n\n"
    f"- Source repository: https://github.com/Yoyote84/Roza\n"
    f"- Pinned source commit: `{SOURCE_COMMIT}`\n"
    "- Extraction method: deterministic file copy with explicit destination mapping; ROZA source files remain untouched.\n"
    "- Model weights and tokenizer are copied byte-for-byte and checked against the SHA-256 values from the source manifest.\n"
    "- The Android companion bridge, generic ROZA drivers, credentials, user saves and unrelated firmware applications are excluded.\n\n"
    "## Third-party attribution to review\n\n"
    "The source project records the Cardputer AI engine as MIT and the LeCarnet-3M model as MIT; "
    "its training notes also identify ODC-BY and Apache-2.0 source corpora. The original notices and "
    "manifests are retained under `src/narrator/hawkins_llm/` and `docs/source-notes/`. "
    "Step 3 must verify the exact upstream notices and redistribution terms before release.\n",
    encoding="utf-8",
)

(DEST_ROOT / "docs/MIGRATION_STATUS.md").write_text(
    "# Nexus migration status\n\n"
    "## Five-stage plan\n\n"
    "- [x] 1/5 — audit scope and dependencies.\n"
    "- [x] 2/5 — extract the game source, tests, tools, documentation and local model assets into this repository.\n"
    "- [ ] 3/5 — replace legacy names and protected narrative elements with an original setting and identity.\n"
    "- [ ] 4/5 — separate platform interfaces, connect the ROZA Cardputer adapter and establish CI/build integration.\n"
    "- [ ] 5/5 — produce the installable firmware and complete physical Cardputer ADV tests with the user.\n\n"
    "## Extraction boundary\n\n"
    "The deterministic game state, missions, character, world, exploration logic, narrative protocol/memory, "
    "save codecs, local narrator engine, model assets, test harnesses and model tools are now in Nexus. "
    "The former app controller is retained under `src/platform/cardputer/legacy/` for refactoring. "
    "ROZA's shared display, keyboard, SD, GNSS, LoRa, Wi-Fi and Bluetooth drivers remain in the ROZA repository.\n\n"
    "This snapshot is not yet a standalone firmware build: the host controller and storage/NVS integration "
    "still reference ROZA/ESP32 services. Those boundaries are the subject of Step 4. No source file was "
    "deleted from ROZA during extraction.\n",
    encoding="utf-8",
)

readme = DEST_ROOT / "README.md"
readme_text = readme.read_text(encoding="utf-8")
readme_text = readme_text.replace("- [ ] Step 2 — extract source into this repository",
                                  "- [x] Step 2 — extract source into this repository")
readme_text = readme_text.replace("See `docs/MIGRATION_STATUS.md` for the current boundary and verification notes.",
                                  "See `docs/MIGRATION_STATUS.md` and `docs/PROVENANCE.md` for the current boundary, source pin and verification notes.")
readme.write_text(readme_text, encoding="utf-8")

print(f"Copied {len(copied)} source files")
print(f"Verified model payloads: {', '.join(sorted(expected))}")
print("Extraction mapping completed successfully")
