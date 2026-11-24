# Modèle local expérimental — Nexus

Le modèle LeCarnet-3M et son moteur C++ restent disponibles pour les expérimentations, mais ils ne sont pas la source principale de narration de Nexus tant qu'ils ne réussissent pas les contrôles de qualité.

## Statut qualité

Le dernier essai vérifié le 24 novembre 2026 a entraîné 3 742 144 paramètres pendant huit époques. La meilleure perte de validation est restée à 6,4704 et les phrases générées étaient incohérentes. Le contrôle qualité a échoué avant export et avant le test d'inférence du nouvel export.

Le petit LLM n'est donc pas approuvé comme MJ autonome. La campagne doit rester cohérente même lorsqu'aucun modèle génératif n'est chargé.

## Canon narratif

Le canon actuel est Nexus : L'Odyssée Arcane : Terre à Marcheprime en 1984, royaume d'Avelune conquis, dimension du Revers d'où vient Varkhël, Seuils reliant les trois dimensions et personnages Manée, Woodsam et Craissant.

Le corpus seed_fr.jsonl provient d'un ancien prototype narratif de Valbrume/LIA. Il n'est plus canonique et ne doit pas servir à une nouvelle publication de modèle sans être réécrit et revérifié sur le nouvel univers.

Le narrateur principal testé est le moteur de scènes C++ déterministe. Un modèle génératif ne pourra être utilisé qu'en complément, après validation linguistique, narrative, de sécurité et de mémoire réelle. Une génération vide, incomplète, contradictoire, trop longue ou contraire au canon doit être rejetée.

Voir docs/NARRATIVE_ARCHITECTURE.md, docs/UNIVERSE.md, docs/ROLEPLAY_RULES.md et docs/CHARACTERS_AND_LOGBOOKS.md.
