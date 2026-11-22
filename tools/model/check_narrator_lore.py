#!/usr/bin/env python3
"""Reject distinctive legacy-franchise terms from Nexus narrator corpus and samples."""
from __future__ import annotations
import argparse
import json
import re
import unicodedata
from pathlib import Path

TERMS = (
    "hawkins", "stranger things", "upside down", "demogorgon", "mind flayer",
    "vecna", "brenner", "starcourt", "hellfire club", "demodog", "demobat",
    "will byers", "dustin", "mike wheeler", "lucas sinclair", "jim hopper",
    "joyce byers", "steve harrington", "robin buckley", "nancy wheeler",
    "max mayfield", "eleven",
)
PATTERNS = tuple((term, re.compile(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", re.IGNORECASE)) for term in TERMS)

def normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))

def inspect(path: Path):
    raw = path.read_text(encoding="utf-8")
    failures = []
    if path.suffix == ".jsonl":
        for line_no, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
                text = " ".join(str(value.get(k, "")) for k in ("prompt", "response", "generated"))
            except json.JSONDecodeError:
                text = line
            norm = normalize(text)
            for term, pattern in PATTERNS:
                if pattern.search(norm):
                    failures.append((f"{path}:{line_no}", term))
    else:
        norm = normalize(raw)
        for term, pattern in PATTERNS:
            if pattern.search(norm):
                failures.append((str(path), term))
    return failures

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True)
    args = parser.parse_args()
    failed = []
    for name in args.input:
        path = Path(name)
        if not path.is_file():
            raise SystemExit(f"Fichier absent : {path}")
        failed.extend(inspect(path))
    if failed:
        for location, term in failed[:50]:
            print(f"Référence narrative héritée détectée: {location}: {term}")
        raise SystemExit(1)
    print(f"Contrôle lexical réussi sur {len(args.input)} fichier(s).")

if __name__ == "__main__":
    main()
