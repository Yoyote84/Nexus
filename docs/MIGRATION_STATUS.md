# État de migration Nexus

## Plan en cinq étapes

- [x] 1/5 — audit du périmètre et des dépendances.
- [x] 2/5 — extraction du code, des tests, des outils et des assets dans le dépôt Nexus.
- [~] 3/5 — univers original, nouveaux identifiants, textes et corpus publiés ; reconstruction des poids du narrateur en cours.
- [ ] 4/5 — interfaces de plateforme, adaptateur Cardputer/ROZA, compilation et contrôles d'intégration.
- [ ] 5/5 — firmware installable final et essais physiques sur le Cardputer ADV avec l'utilisateur.

## Canon narratif actif

L'univers actif est **Nexus — L'Atlas des Rémanences**. L'histoire se déroule autour de Valbrume en 1987. Le mystère central est la Rémanence : le retour irrégulier de fragments d'informations dans des archives et des signaux. LIA signifie Lecteur d'Indices Acoustiques. Le vocabulaire, les groupes, les personnages et les règles sont définis dans `docs/UNIVERSE.md`.

## Changements de l'étape 3

- Les fichiers de jeu et identifiants ont été renommés vers le préfixe `nexus_*` et le namespace C++ `nexus`.
- Les événements narratifs de créatures et de brèches ont été remplacés par des empreintes rémanentes et des ondes de résonance, sans changer l'ordre numérique des événements sauvegardés.
- L'écran de premier contact, les objectifs, les missions, les libellés et les exemples du narrateur ont été réécrits.
- Un corpus initial de 40 dialogues français originaux de Valbrume/LIA a été ajouté.
- Le pipeline exclut les références distinctives de l'ancienne fiction dans les données publiques et le corpus original.
- Un garde-fou lexical refuse une sortie du narrateur contenant ces références.
- Les anciennes clés NVS `hawkins` et le dossier SD `/HAWKINS` restent conservés pour les sauvegardes antérieures ; ce sont des identifiants techniques de compatibilité, pas des éléments du monde.
- Les anciens documents narratifs importés ont été retirés de Nexus ; la copie historique d'origine reste dans `Roza`.

## Modèle local

Les poids quantifiés présents au début de l'étape 3 étaient issus de l'ancien corpus ; leur manifeste les marque explicitement comme provisoires et non approuvés pour une publication Nexus. Le workflow `.github/workflows/nexus-model-rebuild.yml` reconstruit le modèle et le tokenizer sur le corpus original. L'étape 3 ne sera déclarée entièrement terminée qu'après validation de ce nouvel export et de ses sommes SHA-256.

Le modèle ne modifie jamais directement l'état autoritaire du jeu : statistiques, inventaire, missions, choix et sauvegardes restent contrôlés par le moteur déterministe.

## Limites restantes

Le contrôleur Cardputer conservé sous `src/platform/cardputer/legacy/` référence encore des services ROZA. Le dépôt Nexus n'est pas encore une cible de firmware autonome ; cet adaptateur sera séparé à l'étape 4. L'étape 5 reste réservée au binaire installable et aux essais physiques de l'utilisateur.
