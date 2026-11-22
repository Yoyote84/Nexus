# Extraction provenance

- Source repository: https://github.com/Yoyote84/Roza
- Pinned source commit: `7d344a7956b7c8ffa633e83201e7a2457bb1becb`
- Extraction method: deterministic file copy with explicit destination mapping; ROZA source files remain untouched.
- The model weights and tokenizer in the extracted snapshot were copied byte-for-byte and checked against their original SHA-256 values.
- The Android companion bridge, generic ROZA drivers, credentials, user saves, superseded narrative notes and unrelated firmware applications are excluded.

## Third-party attribution to review

The source project records the Cardputer AI engine and LeCarnet-3M model as MIT-licensed. Training notes identify public datasets with separate terms, including ODC-BY and Apache-2.0. The relevant engine license and upstream model manifest are retained under `src/narrator/local_llm/`; corpus provenance is recorded by the model-build workflow and `tools/model/README.md`.

The model binary currently in the repository is a provisional legacy export and is not approved as a Nexus release asset. The `nexus-model-rebuild.yml` workflow must complete, publish the original Nexus narrator assets and record their new checksums before the model is treated as ready.

The source repository `Roza` retains the historical migration material. Nexus contains only its current universe documentation and concise migration/provenance records.
