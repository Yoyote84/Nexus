#!/usr/bin/env python3
"""Verify that the published Nexus model files match their manifest and SHA-256 sums."""

from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

EXPECTED = {"model_lecarnet_q4.bin", "tokenizer_lecarnet_ctk2.bin"}


def fail(message: str) -> None:
    raise SystemExit(f"Validation des assets Nexus échouée : {message}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-dir", default="src/narrator/local_llm/assets")
    parser.add_argument("--seed-corpus", default="tools/model/seed_fr.jsonl")
    args = parser.parse_args()
    root = Path(args.assets_dir)
    manifest_path = root / "model_manifest.json"
    sums_path = root / "SHA256SUMS.txt"
    if not manifest_path.is_file() or not sums_path.is_file():
        fail("manifeste ou fichier SHA256SUMS absent")

    checksums = {}
    for line_no, line in enumerate(sums_path.read_text(encoding="utf-8").splitlines(), 1):
        parts = line.strip().split()
        if len(parts) != 2 or len(parts[0]) != 64 or parts[1] in checksums:
            fail(f"ligne SHA256SUMS invalide ({line_no})")
        try:
            int(parts[0], 16)
        except ValueError:
            fail(f"empreinte non hexadécimale ({line_no})")
        checksums[parts[1]] = parts[0].lower()
    if set(checksums) != EXPECTED:
        fail("SHA256SUMS doit référencer exactement le modèle et le tokenizer")

    for filename, expected_hash in checksums.items():
        path = root / filename
        if not path.is_file():
            fail(f"fichier absent : {filename}")
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            fail(f"SHA-256 incorrect : {filename}")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"manifeste JSON invalide : {exc}")

    if manifest.get("status") != "valid_model_and_tokenizer":
        fail("le statut du manifeste n'est pas valid_model_and_tokenizer")
    if manifest.get("stage") != "3/5":
        fail("le modèle n'est pas marqué étape 3/5")
    if manifest.get("lore_training_status") != "nexus-original-corpus":
        fail("le corpus original Nexus n'est pas déclaré")
    if manifest.get("base_model") != "MaxLSB/LeCarnet-3M":
        fail("modèle de base inattendu")
    if manifest.get("base_model_license") != "MIT":
        fail("licence du modèle de base manquante ou inattendue")

    model = manifest.get("model") or {}
    tokenizer = manifest.get("tokenizer") or {}
    model_path = root / "model_lecarnet_q4.bin"
    tokenizer_path = root / "tokenizer_lecarnet_ctk2.bin"
    if model.get("bytes") != model_path.stat().st_size:
        fail("taille du modèle différente du manifeste")
    if tokenizer.get("bytes") != tokenizer_path.stat().st_size:
        fail("taille du tokenizer différente du manifeste")
    if model.get("version") != 3 or model.get("architecture") != "llama":
        fail("format CRDP ou architecture inattendus")
    if model.get("quantization") != "Q4_0 row-planar":
        fail("quantification inattendue")
    if model.get("context", 0) < 32 or model.get("vocabulary") != tokenizer.get("vocabulary"):
        fail("contexte ou vocabulaire incompatibles")
    if tokenizer.get("format") != "CTK2 byte-level BPE":
        fail("format tokenizer CTK2 attendu")
    heap_bytes = manifest.get("estimated_llm_dynamic_heap_bytes")
    if not isinstance(heap_bytes, int) or not 0 < heap_bytes < 512 * 1024:
        fail("estimation mémoire interne absente ou hors limite SRAM")

    corpus_path = Path(args.seed_corpus)
    seed_rows = [line for line in corpus_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(seed_rows) < 20:
        fail("moins de 20 dialogues originaux dans le corpus")
    training_corpus = manifest.get("training_corpus") or {}
    if training_corpus.get("nexus_seed_count") != len(seed_rows):
        fail("le nombre de dialogues du manifeste ne correspond pas au corpus source")
    if training_corpus.get("nexus_seed_repeat", 0) < 16:
        fail("pondération du corpus original trop faible")

    metrics = manifest.get("training_metrics") or {}
    history = metrics.get("history") or []
    if metrics.get("epochs", 0) < 8 or len(history) < 8:
        fail("nombre d'époques insuffisant pour cette étape de reconstruction")
    validation_losses = [row.get("validation_token_loss") for row in history]
    if not all(isinstance(value, (int, float)) and math.isfinite(value) for value in validation_losses):
        fail("pertes de validation absentes ou non finies")
    best = metrics.get("best_validation_token_loss")
    if not isinstance(best, (int, float)) or not math.isfinite(best):
        fail("meilleure perte de validation absente")
    if abs(min(validation_losses) - best) > 1e-5:
        fail("la meilleure perte ne correspond pas à l'historique")
    if metrics.get("train_examples", 0) < 500 or metrics.get("validation_examples", 0) < 12:
        fail("corpus d'entraînement ou de validation insuffisant")

    print("Assets Nexus validés : SHA-256, tailles, CRDP v3, CTK2, provenance et métriques.")
    print(f"Modèle : {model_path.stat().st_size:,} octets ; tokenizer : {tokenizer_path.stat().st_size:,} octets.")
    print(f"Dialogues Nexus : {len(seed_rows)} ; répétition : {training_corpus['nexus_seed_repeat']} ; époques : {metrics['epochs']}.")


if __name__ == "__main__":
    main()
