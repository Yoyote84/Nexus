# État de migration Nexus

## Plan en cinq étapes

- [x] 1/5 — audit du périmètre et des dépendances.
- [x] 2/5 — extraction du code, des tests, des outils et des assets dans le dépôt Nexus.
- [~] 3/5 — univers, identifiants, textes et corpus originaux réalisés ; validation finale du nouveau narrateur en cours.
- [ ] 4/5 — interfaces de plateforme, adaptateur Cardputer/ROZA, compilation et contrôles d'intégration.
- [ ] 5/5 — firmware installable final et essais physiques sur le Cardputer ADV avec l'utilisateur.

## Canon narratif actif

L'univers actif est **Nexus — L'Atlas des Rémanences**. L'histoire se déroule autour de Valbrume en 1987. Le mystère central est la Rémanence : le retour irrégulier de fragments d'informations dans des archives et des signaux. LIA signifie Lecteur d'Indices Acoustiques. Le vocabulaire, les groupes, les personnages et les règles sont définis dans `docs/UNIVERSE.md`.

## Changements de l'étape 3

- Les fichiers de jeu et identifiants ont été renommés vers le préfixe `nexus_*` et le namespace C++ `nexus`.
- Les événements narratifs de créatures et de brèches ont été remplacés par des empreintes rémanentes et des ondes de résonance, sans changer l'ordre numérique des événements sauvegardés.
- L'écran de premier contact, les objectifs, les missions, les libellés et les exemples du narrateur ont été réécrits.
- Un corpus initial de 40 dialogues français originaux de Valbrume/LIA est disponible dans `tools/model/seed_fr.jsonl`.
- Le pipeline exclut les références distinctives de l'ancienne fiction dans les données publiques et le corpus original.
- Un garde-fou lexical refuse une sortie du narrateur contenant ces références.
- Les exemples d'entraînement sont désormais tronqués à une frontière de mot/phrase et sont alignés sur la limite de neuf tokens de texte du profil embarqué.
- La pondération des dialogues originaux Nexus a été renforcée ; un contrôle distinct rejette les échantillons vides, génériques, répétitifs ou inachevés.
- Un vérificateur dédié contrôle les empreintes SHA-256, les tailles, le manifeste, le format du modèle et la provenance du corpus.
- Le workflow exécute aussi les tests natifs du moteur de jeu et les tests hôte du moteur LLM.
- Les anciennes clés NVS `hawkins` et le dossier SD `/HAWKINS` restent conservés pour les sauvegardes antérieures ; ce sont des identifiants techniques de compatibilité, pas des éléments du monde.
- Les anciens documents narratifs importés ont été retirés de Nexus ; la copie historique d'origine reste dans `Roza`.

## Modèle local

Le premier export CRDP v3/CTK2 a passé les contrôles structurels et ses sommes SHA-256 ont été publiées. Toutefois, les premiers échantillons générés montraient des phrases coupées et des répétitions : ce modèle n'est donc pas encore approuvé comme narrateur Nexus final.

Le pipeline a été corrigé pour ne plus couper les réponses en plein mot, renforcer l'apprentissage sur les dialogues originaux, vérifier les sorties générées et recontrôler les assets publiés. La reconstruction relancée doit encore terminer avec succès avant de cocher l'étape 3/5.

La taille de mémoire dynamique figurant au manifeste est une estimation arithmétique, pas une mesure sur le matériel. La mémoire libre réelle, les performances et la stabilité seront contrôlées à l'étape 5.

Le modèle ne modifie jamais directement l'état autoritaire du jeu : statistiques, inventaire, missions, choix et sauvegardes restent contrôlés par le moteur déterministe.

## Limites restantes

Le contrôleur Cardputer conservé sous `src/platform/cardputer/legacy/` référence encore des services ROZA. Le dépôt Nexus n'est pas encore une cible de firmware autonome ; cet adaptateur sera séparé à l'étape 4. L'étape 5 reste réservée au binaire installable et aux essais physiques de l'utilisateur.
