# État de migration Nexus

## Plan en cinq étapes

- [x] 1/5 — audit du périmètre et des dépendances.
- [x] 2/5 — extraction du code, des tests, des outils et des assets dans le dépôt Nexus.
- [x] 3/5 — originalisation de l'univers, des identifiants, des textes et du corpus du narrateur.
- [ ] 4/5 — interfaces de plateforme, adaptateur Cardputer/ROZA, compilation et contrôles d'intégration.
- [ ] 5/5 — firmware installable final et essais physiques sur le Cardputer ADV avec l'utilisateur.

## Canon narratif actif

L'univers actif est Nexus — L'Atlas des Rémanences. L'histoire se déroule autour de Valbrume en 1987. Le mystère central est la Rémanence : le retour irrégulier de fragments d'informations dans des archives et des signaux. LIA signifie Lecteur d'Indices Acoustiques. Le vocabulaire, les groupes, les personnages et les règles sont définis dans docs/UNIVERSE.md.

## Changements de l'étape 3

- Les fichiers et identifiants du jeu ont été renommés du préfixe historique vers nexus_* et le namespace C++ nexus.
- Les événements narratifs de créatures et de brèches ont été remplacés par des empreintes rémanentes et des ondes de résonance, sans changer l'ordre numérique des événements sauvegardés.
- L'écran de premier contact, les objectifs, les missions, les libellés et les exemples du narrateur ont été réécrits.
- Le corpus français de spécialisation contient des dialogues originaux de Valbrume et passe par un filtre qui exclut les références distinctives de l'ancien univers.
- Un garde-fou lexical refuse une sortie du narrateur contenant ces références.
- Les clés NVS historiques hawkins et le dossier SD /HAWKINS restent conservés pour ne pas perdre les anciennes sauvegardes. Ce sont des identifiants techniques de compatibilité, pas des éléments du monde.
- Les documents source historiques restent sous docs/source-notes/ pour provenance et ne font pas partie du canon du jeu.

## Modèle local

Les poids quantifiés actuellement présents dans le dépôt sont provisoires et ont été spécialisés sur l'ancien corpus. Le workflow nexus-model-rebuild.yml doit les remplacer par une exportation réentraînée sur le corpus original. Cette reconstruction est contrôlée séparément : l'étape 3 couvre l'originalisation et le nouveau pipeline ; l'étape 4 ne devra intégrer que l'artefact Nexus vérifié. Le modèle ne change jamais l'état autoritaire du jeu.

## Limites restantes

Le contrôleur Cardputer conservé sous src/platform/cardputer/legacy/ référence encore des services ROZA. Le snapshot n'est pas encore une cible de firmware autonome ; cet adaptateur sera séparé à l'étape 4. L'étape 5 restera réservée au binaire installable et aux essais physiques de l'utilisateur.
