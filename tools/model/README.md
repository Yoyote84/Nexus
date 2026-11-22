# Narrateur local français de Nexus

Le pipeline entraîne et exporte le petit modèle de narration destiné au Cardputer ADV.

- Modèle de base : MaxLSB/LeCarnet-3M, révision épinglée dans le workflow.
- Corpus de spécialisation : seed_fr.jsonl, dialogues originaux de Valbrume, LIA et la Rémanence.
- Données publiques complémentaires : OpenAssistant/OASST1 et Alpaca GPT-4 French, sous réserve de leurs licences et filtres.
- Export firmware : CRDP v3 LLaMA Q4_0 row-planar + tokenizer CTK2 byte-level BPE.
- Fenêtre d'inférence du Cardputer : 32 tokens.

Le workflow nexus-model-rebuild.yml reconstruit les poids, le tokenizer, les sommes SHA-256 et le manifeste. Il refuse les références narratives distinctives de l'ancien univers dans les exemples de données. Les réponses générées restent soumises au garde-fou lexical intégré au runtime.

Le modèle binaire présent avant la reconstruction est une version provisoire issue de l'ancien entraînement. Il n'est pas une livraison Nexus tant que le workflow de reconstruction et les contrôles ne sont pas réussis.

Le narrateur propose uniquement du texte et des pistes. Le moteur déterministe conserve l'autorité sur les statistiques, l'inventaire, les missions, les choix et les sauvegardes.
