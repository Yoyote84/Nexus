# État de migration Nexus

## Plan en cinq étapes

- [x] 1/5 — audit du périmètre et des dépendances.
- [x] 2/5 — extraction du code, des tests, des outils et des assets dans le dépôt Nexus.
- [~] 3/5 — univers original, règles décrites et moteur narratif autonome ; validation de contenu en cours.
- [ ] 4/5 — interfaces de plateforme, adaptateur Cardputer/ROZA et intégration des trois mondes, des fiches, des jets et des journaux.
- [ ] 5/5 — firmware installable final et essais physiques sur le Cardputer ADV avec l'utilisateur.

## Canon narratif actif

L'univers actif est **Nexus : L'Odyssée Arcane**. La campagne commence à Marcheprime en 1984 et met en scène trois dimensions : la Terre, le royaume enchanté d'Avelune conquis par Varkhël, et le Revers dont il est originaire. Les Seuils relient les trois mondes. Le joueur contrôle Craissant ; le MJ contrôle Manée, Woodsam et tous les PNJ. Les détails sont définis dans docs/UNIVERSE.md.

## Changements de l'étape 3

- Les fichiers de jeu et identifiants ont été renommés vers le préfixe nexus_* et le namespace C++ nexus.
- Le canon narratif a été réaligné sur Marcheprime en 1984, les trois dimensions, le royaume conquis, Varkhël et les Seuils utilisés pour envoyer des créatures sur Terre.
- Les scènes du moteur C++ incluent maintenant la manifestation d'un Seuil, le passage d'une créature, la découverte d'Avelune, l'influence du Revers et les interventions de Manée et Woodsam.
- Le corpus tools/model/seed_fr.jsonl appartient à l'ancien prototype Valbrume/LIA ; il n'est plus canonique et doit être réécrit avant tout nouvel entraînement publié.
- Un garde-fou lexical refuse une sortie contenant les références distinctives de l'œuvre précédente.
- Le moteur narratif déterministe autonome reste hors ligne, sans allocation dynamique, et ne peut modifier les choix de Craissant ou l'état du jeu.
- Les huit bits d'intrigue sont conservés dans le format de sauvegarde. Leur signification sera réalignée sur les trois mondes et les personnages pendant l'étape 4, sans modifier le format binaire.
- Le workflow de narration a réussi le 24 novembre 2026 sur le commit af7592f232705f6ac0810248c252929200a2154b (run 45408391743) : tests du monde, exploration, personnage, missions, aventure, mémoire narrative, scènes des trois dimensions et garde-fous avec ASan/UBSan ; test hôte du moteur LLM également réussi.

## Modèle local

Le petit LeCarnet-3M n'est pas approuvé comme MJ autonome. Le dernier entraînement vérifié le 24 novembre 2026 a obtenu une meilleure perte de validation de 6,4704 et produit des phrases incohérentes ; le contrôle qualité a échoué avant export, vérification du nouvel asset et test d'inférence C++.

Le corpus du modèle appartient à l'ancien prototype Valbrume/LIA et doit être remplacé avant tout nouvel entraînement. Le modèle génératif reste expérimental ; le moteur déterministe et les données sauvegardées sont les autorités.

## Éléments définis pour la campagne

- La répartition des rôles MJ/joueur et les trois fiches de personnages sont documentées dans docs/CHARACTERS_AND_LOGBOOKS.md.
- Les règles proposées de d20, difficultés, conflits, PV et mort sont dans docs/ROLEPLAY_RULES.md ; leur intégration au moteur n'est pas terminée.
- Les journaux de Craissant, Manée et Woodsam, avec séparation faits/hypothèses/questions, sont spécifiés dans docs/CHARACTERS_AND_LOGBOOKS.md.
- Le prologue de Marcheprime en 1984 est documenté dans docs/CAMPAIGN_PROLOGUE.md.
- Les références Yarn Spinner et ink sont consignées dans docs/NARRATIVE_ARCHITECTURE.md.

## Limites restantes

Le contrôleur Cardputer conservé sous src/platform/cardputer/legacy/ référence encore des services ROZA. Le dépôt Nexus n'est pas encore une cible de firmware autonome ; l'étape 4 devra relier les trois dimensions, les personnages, les jets, les journaux et l'affichage Cardputer. L'étape 5 reste réservée au binaire installable et aux essais physiques de l'utilisateur.
