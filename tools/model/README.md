# Narrateur local français de Nexus

Le pipeline entraîne et exporte le petit modèle de narration destiné au Cardputer ADV.

- Modèle de base : `MaxLSB/LeCarnet-3M`, révision épinglée dans le workflow.
- Corpus de spécialisation : `seed_fr.jsonl`, 120 dialogues originaux de Valbrume, LIA et la Rémanence.
- Données publiques complémentaires : OpenAssistant/OASST1 et Alpaca GPT-4 French, sous réserve de leurs licences et filtres.
- Export firmware : CRDP v3 LLaMA Q4_0 row-planar + tokenizer CTK2 byte-level BPE.
- Fenêtre d'inférence du Cardputer : 32 tokens ; neuf tokens de texte maximum par génération.

Le workflow `nexus-model-rebuild.yml` reconstruit les poids, le tokenizer, les sommes SHA-256 et le manifeste. Il contrôle les références narratives distinctives de l'ancien univers dans les données et les échantillons générés. Le contrôle qualité rejette les réponses vides, génériques, répétitives ou inachevées. Les fichiers publiés sont revérifiés avec `verify_published_assets.py`.

Le premier modèle exporté avait passé la validation structurelle, mais ses échantillons révélaient des coupures en plein mot et des répétitions. L'entraînement a donc été corrigé : frontière de phrase/mot pour les réponses, corpus Nexus plus fortement pondéré (16 répétitions), plafond de neuf tokens et comptage explicite des lignes impossibles à encoder.

Après réussite de la reconstruction, `nexus-inference-verify.yml` compile le vrai moteur C++ avec les stubs hôte, charge les fichiers CRDP v3/CTK2 publiés, encode un prompt français court et exécute plusieurs pas d'inférence déterministe. L'étape 3 n'est achevée qu'après réussite de l'entraînement, de la qualité des échantillons, des empreintes SHA-256, des tests natifs et de cette inférence hôte.

Le narrateur propose uniquement du texte et des pistes. Le moteur déterministe conserve l'autorité sur les statistiques, l'inventaire, les missions, les choix et les sauvegardes.
