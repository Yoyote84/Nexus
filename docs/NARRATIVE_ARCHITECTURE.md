# Architecture de narration — Nexus : L'Odyssée Arcane

## Objectif

Le système doit faire vivre une campagne JDR persistante, jouable hors ligne sur Cardputer ADV. Il soutient le Maître du Jeu, l'interprétation de Manée et Woodsam, les PNJ et la continuité entre les trois dimensions. Le joueur reste seul maître des décisions de Craissant.

## Structure narrative

Les systèmes de narration interactive tels que Yarn Spinner et ink démontrent l'intérêt de séparer les scènes, les lignes de dialogue, les choix, les conditions et les variables persistantes. Yarn Spinner documente les choix conditionnels, les variables, les détours et les storylets ; ink documente la présentation des choix ainsi que l'enregistrement et le rechargement de l'état narratif.

Nexus reprend ces principes dans un moteur C++ adapté au Cardputer : scènes thématiques indépendantes, choix proposés par le MJ, faits de campagne validés par le moteur de règles, variables persistantes, journaux indépendants et sauvegardes locales.

Références de conception :
- Yarn Spinner : https://www.yarnspinner.dev/docs/
- Yarn Spinner — choix, variables et storylets : https://www.yarnspinner.dev/features/
- ink — choix et sauvegarde d'état : https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md

## Canon en cours

Le récit commence à Marcheprime en 1984 et relie trois dimensions : la Terre, Avelune — royaume enchanté conquis — et le Revers, dimension d'origine de Varkhël. Les Seuils sont les passages entre ces mondes et le Nexus est leur point de convergence.

Manée et Woodsam sont joués par le MJ. Craissant est joué par l'utilisateur. Le MJ contrôle les PNJ mais ne prend jamais les décisions du joueur.

## Moteur narratif C++

Le fichier src/narrator/nexus_narrative_engine.cpp propose des scènes originales et déterministes, sans allocation dynamique. Les scènes couvrent les choix initiaux, les événements, les Seuils, le passage de créatures, la découverte d'Avelune, l'influence du Revers et les interventions de Manée et Woodsam.

La formulation est sélectionnée selon la graine du monde, la séquence d'événement, le jour, le secteur, l'intensité, les indices et les jalons d'intrigue. Un même état produit la même sortie ; une progression de campagne peut produire une autre variante.

Le moteur refuse une scène invalide, une valeur de contexte hors limites, une sortie trop longue, vide, inachevée ou contenant des références lexicales héritées. Il ne reçoit aucun pointeur vers les structures mutables du joueur ou de l'inventaire.

## Rôle du petit modèle local

Le modèle LeCarnet-3M n'est pas approuvé comme MJ autonome. Le dernier entraînement vérifié le 24 novembre 2026 a produit des sorties françaises incohérentes et a échoué au contrôle qualité avant export. Les assets structurellement valides ne prouvent pas la qualité narrative.

Le modèle génératif reste optionnel et expérimental. Il ne pourra que proposer une formulation si elle passe les contrôles de français, de pertinence, de continuité, d'originalité et de sécurité. Le moteur déterministe et les données sauvegardées restent les autorités. Une réponse du modèle ne peut jamais modifier les PV, l'inventaire, les compétences, les jets, les relations ou les événements sans validation par le moteur de règles.

## Personnages et journaux

Les trois journaux sont une mémoire durable : Craissant conserve les notes du joueur ; Manée ses mythes, intuitions, découvertes personnelles et hypothèses ; Woodsam ses plans, ressources, risques et observations tactiques.

Les faits confirmés, les hypothèses et les questions restent séparés. Un compagnon ne peut écrire comme souvenir personnel un événement qu'il n'a pas vu ou appris. Les entrées importantes sont associées au jour, au monde et à l'événement quand ces données existent. La persistance sur microSD et les déclencheurs automatiques relèvent de l'étape 4.

## Règles et jets

Les règles proposées sont décrites dans docs/ROLEPLAY_RULES.md : d20 ajouté à une caractéristique, seuils annoncés avant le lancer, conflits, blessures et état critique où la mort est possible. Leur présence dans la documentation ne signifie pas qu'elles sont déjà toutes intégrées au firmware : cette intégration sera vérifiée à l'étape 4, puis testée physiquement à l'étape 5.

## Frontières des cinq étapes

- Étapes 1 et 2 : audit et extraction, terminés.
- Étape 3 : univers original, règles décrites et moteur narratif autonome ; validation de contenu en cours.
- Étape 4 : intégration Cardputer/ROZA, états des trois mondes, jets, fiches, journaux et affichage.
- Étape 5 : firmware installable, mesures mémoire/vitesse et essais physiques par l'utilisateur.
