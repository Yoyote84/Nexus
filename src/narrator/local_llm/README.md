# Moteur local expérimental de Nexus

Ce dossier contient le moteur d'inférence C++ dérivé de therezor/cardputer-ai, sous licence MIT, ainsi qu'un profil de modèle local expérimental.

## Moteur et modèle

- Source du moteur : REZOR, révision 78c5128672b750977619dc0a6c3b8baed91168ed, licence MIT.
- Modèle : MaxLSB/LeCarnet-3M, révision 0bf134cfceb1b00c7c56a0ebbc1560ec634c3502, licence MIT.
- Format : CRDP v3, LLaMA, Q4_0 row-planar ; tokenizer CTK2 GPT-2 byte-level BPE.
- Profil actuel : contexte de 32 tokens ; jusqu'à 9 tokens de texte par réponse, avec un pas supplémentaire réservé au token EOS.

## Statut qualité

**Ce modèle n'est pas approuvé comme narrateur principal de Nexus.** Le dernier réentraînement vérifié le 24 novembre 2026 a fait baisser la perte d'entraînement sans améliorer la validation (meilleure perte : 6,4704). Les phrases générées étaient incohérentes et le contrôle qualité a bloqué l'export. Les assets conservés dans assets/ sont donc expérimentaux : leur conformité structurelle et leurs empreintes SHA-256 ne garantissent pas une narration correcte.

Le narrateur fiable est le moteur français déterministe décrit dans docs/NARRATIVE_ARCHITECTURE.md. Le petit modèle ne pourra être utilisé qu'en complément après validation de la qualité de ses sorties. Une génération vide, incomplète, trop longue ou contraire au lore doit toujours être rejetée.

## Assets et runtime

Les fichiers éventuels du profil local sont :
- assets/model_lecarnet_q4.bin
- assets/tokenizer_lecarnet_ctk2.bin
- assets/model_manifest.json
- assets/SHA256SUMS.txt

model_data.S incorpore les binaires dans l'image applicative et expose les symboles de début/fin. Le runtime valide l'en-tête CRDP, les dimensions, le tokenizer et les limites du prompt avant l'inférence. Le runtime ne doit jamais bloquer l'utilisation du monde lorsque le modèle est absent ou invalide.

## Responsabilités

- Le moteur du jeu reste seul maître des statistiques, de l'inventaire, des missions, des compétences, des choix et des sauvegardes.
- Le narrateur reçoit un instantané en lecture seule.
- L'inférence, lorsqu'elle sera de nouveau qualifiée, sera isolée dans une tâche FreeRTOS dédiée.
- Le mode hors ligne et le moteur narratif déterministe restent disponibles en cas de manque de mémoire, de latence excessive ou d'échec du modèle.

## Frontières des étapes

L'étape 3 construit et vérifie la narration autonome. L'étape 4 reliera les scènes au contrôleur Cardputer et au firmware ROZA. L'étape 5 vérifiera le binaire installable, la mémoire réelle, la vitesse, la stabilité et les résultats sur le Cardputer ADV.
