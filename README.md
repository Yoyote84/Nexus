# Nexus : L'Odyssée Arcane

Nexus est un jeu de rôle hors ligne sur M5Stack Cardputer ADV. L'histoire commence à Marcheprime en 1984 et relie trois dimensions : la Terre, Avelune et le Revers. Le joueur incarne Craissant, accompagné de Manée et Woodsam, interprétés par le Maître du Jeu.

Le royaume d'Avelune est tombé sous le pouvoir de Varkhël, souverain venu du Revers, qui détourne les Seuils pour envoyer ses créatures sur Terre. Le joueur contrôle Craissant ; le MJ contrôle Manée, Woodsam et tous les PNJ.

Lire docs/UNIVERSE.md, docs/NARRATIVE_STYLE.md, docs/ROLEPLAY_RULES.md et docs/CHARACTERS_AND_LOGBOOKS.md.

## Cible

- M5Stack Cardputer ADV.
- Cap LoRa-1262/GNSS pour l'exploration réelle, sans obligation d'utiliser le GPS.
- microSD pour les sauvegardes, les fiches, les journaux et les ressources.
- Aucun téléphone, réseau ou Wi-Fi nécessaire pendant une partie.

## Organisation

- src/core/ — monde, personnage, missions et règles déterministes.
- src/exploration/ — secteurs et événements de déplacement.
- src/narrator/ — scènes, mémoire des personnages et modèle local expérimental.
- src/storage/ — codecs et adaptateurs de persistance.
- src/platform/cardputer/ — contrôleur historique à découpler à l'étape 4.
- tests/ — tests natifs.
- tools/model/ — corpus, entraînement et export expérimental du narrateur.

## Migration en cinq étapes

- [x] 1/5 — audit.
- [x] 2/5 — extraction dans ce dépôt.
- [~] 3/5 — univers original, scènes et continuité narrative en cours de validation.
- [ ] 4/5 — intégration des trois mondes, des jets, des fiches et des journaux dans le firmware ROZA.
- [ ] 5/5 — firmware installable final et essais physiques sur le Cardputer ADV.

Le moteur narratif hors ligne est validé par les tests natifs. Les prochaines tâches consistent à relier les scènes au monde à trois dimensions, aux jets de dés, aux fiches et aux trois journaux persistants. Le petit modèle génératif reste expérimental et n'est pas approuvé comme MJ autonome.

Les sauvegardes et les journaux doivent rester locaux sur microSD. Les détails techniques et les limites de compatibilité figurent dans docs/MIGRATION_STATUS.md.
