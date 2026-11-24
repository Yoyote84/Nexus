# Nexus — L'Atlas des Rémanences

Nexus est un jeu de rôle d'exploration hors ligne, destiné au M5Stack Cardputer ADV. Le joueur arpente librement des secteurs, recueille des empreintes de la Rémanence et reconstitue un atlas d'événements inhabituels.

## Univers

L'histoire-cadre prend place en 1987 autour de Valbrume, commune fictive marquée par la Nuit des Retours du 14 octobre 1986. Des fragments de sons et de mesures réapparaissent dans des archives et des signaux. Le joueur est un arpenteur assisté par LIA, le Lecteur d'Indices Acoustiques.

Lire `docs/UNIVERSE.md`, `docs/NARRATIVE_STYLE.md` et `docs/ORIGINALITY_AND_PROVENANCE.md`.

## Cible

- M5Stack Cardputer ADV.
- Module Cap LoRa-1262/GNSS en option pour les données locales de position.
- microSD pour les sauvegardes et les ressources.
- Aucun téléphone, réseau ou Wi-Fi nécessaire pendant une partie.

## Organisation

- `src/core/` — monde, personnage, missions et règles déterministes.
- `src/exploration/` — secteurs et événements de déplacement.
- `src/narrator/` — protocole, mémoire et modèle local.
- `src/storage/` — codecs et adaptateurs de persistance.
- `src/platform/cardputer/` — contrôleur historique à découpler à l'étape 4.
- `tests/` — tests natifs.
- `tools/model/` — corpus, entraînement et export du narrateur.

## Migration en cinq étapes

- [x] 1/5 — audit.
- [x] 2/5 — extraction dans ce dépôt.
- [~] 3/5 — univers et corpus de 120 dialogues originaux terminés ; reconstruction et validation qualité du narrateur en cours.
- [ ] 4/5 — adaptation et intégration dans le firmware ROZA.
- [ ] 5/5 — firmware installable et essais Cardputer.

Le premier export du narrateur a passé les contrôles de structure, mais ses échantillons révélaient des phrases inachevées. Le pipeline a été corrigé : l'étape 3 restera ouverte jusqu'à ce que le nouvel entraînement, les contrôles de qualité, les sommes SHA-256 et les tests natifs réussissent.

Les clés de sauvegarde historiques restent compatibles ; voir `docs/migration/LEGACY_SOURCE_NOTES.md`.
