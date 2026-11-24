# Modèle local expérimental — Nexus

Le modèle LeCarnet-3M et son moteur C++ restent disponibles pour les expérimentations, mais **ils ne sont pas la source principale de narration de Nexus** tant qu'ils ne réussissent pas les contrôles de qualité.

## Limites mesurées

- Modèle de base : MaxLSB/LeCarnet-3M, révision 0bf134cfceb1b00c7c56a0ebbc1560ec634c3502, licence MIT.
- Export : CRDP v3 LLaMA Q4_0 row-planar ; tokenizer CTK2.
- Profil du firmware : contexte de 32 tokens et maximum de 9 tokens de texte par génération.
- Le dernier essai sur GitHub Actions (24 novembre 2026) a entraîné 3 742 144 paramètres pendant 8 époques. La perte d'entraînement est descendue à 1,9065, tandis que la meilleure perte de validation est restée à 6,4704.
- Les sorties de test n'étaient pas exploitables. Le contrôle qualité a échoué avant l'export et avant le test d'inférence du nouveau modèle.

La structure binaire de l'ancien export et ses sommes SHA-256 valides prouvent seulement que les fichiers sont lisibles et conformes au format. Elles ne prouvent pas la qualité linguistique ni la fiabilité narrative.

## Stratégie approuvée

Le narrateur principal est le moteur déterministe src/narrator/nexus_narrative_engine.cpp. Il sélectionne des scènes originales selon les événements, les choix, les preuves, les huit jalons d'intrigue persistants, la chronologie et la relation avec LIA. Il fonctionne entièrement hors ligne, sans allocation dynamique, et n'altère jamais l'état du jeu.

Le modèle LeCarnet ne pourra être réactivé comme source de texte que lorsqu'un entraînement distinct passera :
1. la validation sur des exemples tenus à l'écart de l'entraînement ;
2. les contrôles de français naturel, de phrase complète et de pertinence Nexus ;
3. les garde-fous de sécurité et d'originalité ;
4. le chargement et l'inférence réels dans le moteur C++ ;
5. les mesures de mémoire et de temps sur le matériel cible.

Le workflow nexus-model-rebuild.yml est donc manuel uniquement. Il ne bloque plus les tests du moteur narratif et ne publie pas automatiquement un modèle simplement parce que son export est structurellement valide.

Voir docs/NARRATIVE_ARCHITECTURE.md pour la stratégie complète.
