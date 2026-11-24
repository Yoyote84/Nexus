#!/usr/bin/env python3
"""Reject empty, truncated, repetitive or clearly off-purpose Nexus narrator samples."""

from __future__ import annotations
import argparse
import json
import re
import unicodedata
from pathlib import Path

INCOMPLETE_ENDINGS = {
    "a", "au", "aux", "avec", "ce", "ces", "chez", "comme", "dans", "de",
    "des", "du", "elle", "en", "et", "eux", "il", "ils", "je", "la", "le",
    "les", "leur", "lui", "mais", "mes", "mon", "notre", "ou", "par", "pas",
    "pour", "que", "qui", "sa", "sans", "se", "ses", "son", "sous", "sur",
    "ta", "te", "tes", "ton", "un", "une", "vers", "vos", "votre",
}
LORE_ANCHORS = {
    "lia", "remanence", "valbrume", "veyrac", "relais",
    "impulsion", "cassette", "signal", "archive", "empreinte", "resonance",
}
REFUSAL = re.compile(
    r"\b(?:je ne peux pas|je ne suis pas en mesure|je suis desole|desole)\b",
    re.IGNORECASE,
)


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def inspect(path: Path, minimum_samples: int, minimum_lore_samples: int) -> list[str]:
    rows = []
    errors = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"ligne {line_no}: JSON invalide ({exc})")
            continue
        prompt = str(row.get("prompt") or "").strip()
        generated = str(row.get("generated") or "").strip()
        if not prompt or not generated:
            errors.append(f"ligne {line_no}: prompt ou génération vide")
            continue
        normalized = normalize(generated)
        words = re.findall(r"[a-z0-9]+(?:['’][a-z0-9]+)?", normalized)
        if len(words) < 4:
            errors.append(f"ligne {line_no}: génération trop courte ({len(words)} mots)")
        if len(generated) > 140:
            errors.append(f"ligne {line_no}: génération trop longue pour le profil Cardputer")
        if REFUSAL.search(normalized):
            errors.append(f"ligne {line_no}: réponse de refus générique")
        # The deployed narrator has nine text-token slots: a trailing connector
        # or apostrophe signals a sentence clipped by the generation budget.
        terminal = generated.rstrip('”»)]} ').rstrip()
        if not terminal or terminal[-1] not in ".!?…":
            errors.append(f"ligne {line_no}: phrase inachevée (ponctuation finale absente)")
        if re.search(r"(?:['’]|\b(?:l|d|j|c|n|m|s|t|qu))$", normalized):
            errors.append(f"ligne {line_no}: mot coupé en fin de génération")
        if words and words[-1] in INCOMPLETE_ENDINGS:
            errors.append(f"ligne {line_no}: réponse terminée par un mot de liaison")
        for size in (4, 5):
            seen = set()
            for index in range(0, len(words) - size + 1):
                gram = tuple(words[index:index + size])
                if gram in seen:
                    errors.append(f"ligne {line_no}: répétition d'une séquence de {size} mots")
                    break
                seen.add(gram)
        if any(anchor in normalized for anchor in LORE_ANCHORS):
            row["_has_lore_anchor"] = True
        rows.append(row)

    if len(rows) < minimum_samples:
        errors.append(f"seulement {len(rows)} échantillon(s), {minimum_samples} requis")
    lore_count = sum(bool(row.get("_has_lore_anchor")) for row in rows)
    if lore_count < minimum_lore_samples:
        errors.append(
            f"seulement {lore_count} échantillon(s) ancrés dans l'univers Nexus, "
            f"{minimum_lore_samples} requis"
        )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--minimum-samples", type=int, default=4)
    parser.add_argument("--minimum-lore-samples", type=int, default=2)
    args = parser.parse_args()
    path = Path(args.input)
    if not path.is_file():
        raise SystemExit(f"Fichier absent : {path}")
    errors = inspect(path, args.minimum_samples, args.minimum_lore_samples)
    if errors:
        for error in errors:
            print(f"ÉCHEC: {error}")
        raise SystemExit(1)
    print(f"Contrôle narratif réussi : {path}.")


if __name__ == "__main__":
    main()
