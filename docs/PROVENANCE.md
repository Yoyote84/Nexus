# Extraction provenance

- Source repository: https://github.com/Yoyote84/Roza
- Pinned source commit: `7d344a7956b7c8ffa633e83201e7a2457bb1becb`
- Extraction method: deterministic file copy with explicit destination mapping; ROZA source files remain untouched.
- Model weights and tokenizer are copied byte-for-byte and checked against the SHA-256 values from the source manifest.
- The Android companion bridge, generic ROZA drivers, credentials, user saves and unrelated firmware applications are excluded.

## Third-party attribution to review

The source project records the Cardputer AI engine as MIT and the LeCarnet-3M model as MIT; its training notes also identify ODC-BY and Apache-2.0 source corpora. The original notices and manifests are retained under `src/narrator/hawkins_llm/` and `docs/source-notes/`. Step 3 must verify the exact upstream notices and redistribution terms before release.
