# État de migration Nexus

## Plan en cinq étapes

- [x] 1/5 — audit du périmètre et des dépendances.
- [x] 2/5 — extraction du code, des tests, des outils et des assets dans le dépôt Nexus.
- [~] 3/5 — univers original et moteur narratif français hors ligne ajoutés ; validation CI en cours. Le LLM génératif reste expérimental.
- [ ] 4/5 — interfaces de plateforme, adaptateur Cardputer/ROZA et intégration du moteur narratif.
- [ ] 5/5 — firmware installable final et essais physiques sur le Cardputer ADV avec l'utilisateur.

## Canon narratif actif

L'univers actif est **Nexus — L'Atlas des Rémanences**. L'histoire se déroule autour de Valbrume en 1987. Le mystère central est la Rémanence : le retour irrégulier de fragments d'informations dans des archives et des signaux. LIA signifie Lecteur d'Indices Acoustiques. Le vocabulaire, les groupes, les personnages et les règles sont définis dans `docs/UNIVERSE.md`.

## Changements de l'étape 3

- Les fichiers de jeu et identifiants ont été renommés vers le préfixe `nexus_*` et le namespace C++ `nexus`.
- Les événements narratifs de créatures et de brèches ont été remplacés par des empreintes rémanentes et des ondes de résonance, sans changer l'ordre numérique des événements sauvegardés.
- L'écran de premier contact, les objectifs, les missions, les libellés et les exemples du narrateur ont été réécrits.
- Un corpus de dialogues français originaux de Valbrume/LIA est conservé dans tools/model/seed_fr.jsonl pour les expérimentations de modèle.
- Le pipeline exclut les références distinctives de l'ancienne fiction dans les données publiques et le corpus original.
- Un garde-fou lexical refuse une sortie contenant ces références.
- Un moteur narratif déterministe autonome fournit des scènes originales pour les choix de premier contact, les événements, les découvertes, les archives, les missions et les périodes calmes.
- La sélection de scènes varie selon la graine, le jour, le secteur, la séquence d'événement, les preuves et la relation avec LIA, sans modifier l'état du jeu.
- Les exemples d'entraînement sont désormais tronqués à une frontière de mot/phrase et alignés sur la limite de neuf tokens de texte du profil embarqué.
- La pondération des dialogues originaux Nexus a été renforcée ; les exemples incompatibles avec cette petite fenêtre sont écartés et comptabilisés plutôt que de faire échouer tout l'entraînement.
- Un contrôle distinct rejette les échantillons vides, génériques, répétitifs ou inachevés.
- Un vérificateur dédié contrôle les empreintes SHA-256, les tailles, le manifeste, le format du modèle et la provenance du corpus.
- Le workflow exécute les tests natifs du moteur de jeu et les tests hôte de sécurité du moteur LLM.
- Après une reconstruction réussie, un second workflow charge le véritable CRDP v3 et CTK2 dans le moteur C++ sur hôte, encode un prompt et exécute plusieurs pas d'inférence déterministe.
- Les anciennes clés NVS `hawkins` et le dossier SD `/HAWKINS` restent conservés pour les sauvegardes antérieures ; ce sont des identifiants techniques de compatibilité, pas des éléments du monde.
- Les anciens documents narratifs importés ont été retirés de Nexus ; la copie historique d'origine reste dans `Roza`.

## Modèle local et stratégie de narration

Le petit LeCarnet-3M n'est pas approuvé comme narrateur principal. La vérification du 24 novembre 2026 a confirmé 3 742 144 paramètres, un contexte de 32 tokens et une génération limitée à neuf tokens de texte. Le dernier entraînement a atteint une perte d'entraînement de 1,9065 mais une meilleure perte de validation de 6,4704 après huit époques. Les quatre échantillons produits étaient incohérents ; le contrôle qualité a échoué avant l'export, la vérification des nouveaux assets et le test d'inférence C++.

Le moteur narratif fiable est src/narrator/nexus_narrative_engine.cpp. Il propose plusieurs formulations originales par scène, choisit de façon reproductible selon le contexte sauvegardé et adapte son degré de certitude aux preuves et à la relation avec LIA. Il reste hors ligne, sans allocation dynamique, et ne peut modifier ni les choix ni l'état du jeu.

Le workflow de reconstruction du LLM est manuel uniquement. Les assets antérieurs restent expérimentaux : un manifeste valide, un format CRDP conforme et des sommes SHA-256 correctes ne suffisent pas à prouver une qualité linguistique.

Voir docs/NARRATIVE_ARCHITECTURE.md pour les choix de conception, les références et les critères de validation.

## Limites restantes

Le contrôleur Cardputer conservé sous `src/platform/cardputer/legacy/` référence encore des services ROZA. Le dépôt Nexus n'est pas encore une cible de firmware autonome ; cet adaptateur sera séparé à l'étape 4. L'étape 5 reste réservée au binaire installable et aux essais physiques de l'utilisateur.
