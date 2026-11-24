# Moteur local de narration Nexus

Ce dossier contient le moteur d'inférence C++ dérivé de [therezor/cardputer-ai](https://github.com/therezor/cardputer-ai), sous licence MIT, et son profil de modèle destiné au narrateur local de Nexus.

## Moteur et modèle

- Source du moteur : REZOR, révision `78c5128672b750977619dc0a6c3b8baed91168ed`, licence MIT.
- Modèle de base : `MaxLSB/LeCarnet-3M`, révision `0bf134cfceb1b00c7c56a0ebbc1560ec634c3502`, licence MIT.
- Format d'export : CRDP v3, LLaMA, Q4_0 row-planar.
- Tokenizer : CTK2 GPT-2 byte-level BPE.
- Profil visé : contexte de 32 tokens ; jusqu'à 9 tokens de texte par réponse, avec un pas supplémentaire réservé au token EOS.

## Assets

Le workflow de l'étape 3 publie les fichiers suivants dans `assets/` :

- `assets/model_lecarnet_q4.bin`
- `assets/tokenizer_lecarnet_ctk2.bin`
- `assets/model_manifest.json`
- `assets/SHA256SUMS.txt`

Les sommes SHA-256 et le manifeste doivent être vérifiés avant d'accepter un export comme version finale de Nexus. Le premier export a passé les contrôles de structure, mais ses premiers échantillons comportaient des phrases coupées et des répétitions ; il reste provisoire tant que le nouvel entraînement et les contrôles qualité du workflow ne sont pas terminés.

Après la publication d'un export par le pipeline, le workflow `nexus-inference-verify.yml` charge ces deux binaires dans le moteur C++ sur hôte, encode un prompt et vérifie l'exécution de plusieurs pas d'inférence. Ce test confirme que le format exporté est réellement consommable par le moteur, sans constituer un essai de performance sur l'ESP32-S3.

`model_data.S` incorpore les deux binaires dans l'image applicative et expose les symboles de début/fin. Le runtime les lit directement depuis la Flash mappée. La microSD n'est pas utilisée pour charger les poids du narrateur.

## Runtime et responsabilités

- `runtime.cpp` valide les limites des binaires, initialise `Transformer`, `Tokenizer` et `Sampler`, contrôle le tokenizer CTK2 et refuse un prompt trop long au lieu d'en supprimer silencieusement le début.
- Le contexte narratif est construit à partir de l'état connu du jeu et de l'action du joueur.
- La génération est isolée dans une tâche FreeRTOS dédiée dans l'adaptateur Cardputer historique.
- L'IA ne modifie jamais directement les statistiques, l'inventaire, les missions, les compétences ou les sauvegardes : le moteur déterministe reste l'autorité.

## Mode de secours

Un chargement invalide, un manque de mémoire ou une génération vide doit désactiver uniquement le narrateur. Le monde Nexus et ses mécaniques déterministes doivent rester utilisables.

## Frontières des étapes

La validation complète du corpus, des sorties, des assets et de l'inférence hôte relève de l'étape 3. Le découplage de l'adaptateur Cardputer et son intégration autonome dans le firmware ROZA relèvent de l'étape 4. Les mesures mémoire réelles, la vitesse, la stabilité et les essais sur le vrai Cardputer ADV relèvent de l'étape 5.
