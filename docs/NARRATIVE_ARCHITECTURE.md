# Architecture de narration — Nexus

## Objectif

LIA doit raconter une enquête suivie, en français, sans réseau et sans téléphone. Sa narration doit rester cohérente avec le monde, les choix réellement effectués et les preuves enregistrées. Elle ne doit jamais inventer l'inventaire, les missions, les récompenses ou les actions du joueur.

## Principes repris des outils narratifs éprouvés

Les outils de narration interactive comme **Yarn Spinner** structurent une histoire en scènes, lignes et choix conditionnels. Ils utilisent des variables persistantes pour adapter les dialogues aux décisions précédentes, ainsi que des *storylets* pour sélectionner le contenu pertinent dans une situation donnée. **Ink** suit une approche text-first : le texte et les embranchements restent lisibles par les auteurs, puis sont exécutés par un moteur de jeu.

Nexus reprend ces idées, sans embarquer un moteur généraliste trop lourd pour le Cardputer :

- une scène correspond à un événement ou à une décision validée par le jeu ;
- les variables persistantes sont lues depuis les sauvegardes existantes ;
- plusieurs formulations originales sont disponibles pour chaque scène ;
- une clé déterministe combine la graine du monde, le jour, le secteur et la séquence d'événement ;
- les preuves et la relation avec LIA ajustent le ton et le degré de certitude ;
- la sélection d'un texte ne modifie jamais les règles du jeu.

Références :
- Yarn Spinner — documentation : https://yarnspinner.dev/docs/
- Yarn Spinner — variables, choix conditionnels et storylets : https://www.yarnspinner.dev/features/
- ink d'inkle — langage narratif pour jeux : https://www.inklestudios.com/ink/

## Moteur actuellement ajouté

Le fichier src/narrator/nexus_narrative_engine.cpp fournit une banque de scènes française sans allocation dynamique. Chaque appel construit une sortie courte, déterministe et limitée à 210 octets, compatible avec la capacité du protocole de narration déjà présent.

Les scènes couvrent :
1. ouverture de l'enquête ;
2. les trois choix du premier contact ;
3. découverte d'un secteur ;
4. signal radio ;
5. anomalie électrique ;
6. empreinte rémanente ;
7. mouvement des groupes de Valbrume ;
8. appel radio ambigu ;
9. onde de résonance ;
10. archive retrouvée ;
11. mission accomplie ;
12. observation calme.

Le moteur propose plusieurs formulations par scène. Il complète ensuite le texte selon les preuves déjà confirmées, l'intensité de l'événement, la confiance accordée à LIA et la chronologie. Un appel ambigu reçoit toujours un rappel de sécurité : le jeu ne remplace pas les secours réels.

La sélection est reproductible : un même état produit le même texte. Un changement de jour, de secteur, de séquence d'événement ou de progression peut produire une autre formulation. Cela évite les répétitions immédiates tout en facilitant les tests et la reprise après redémarrage.

Le moteur refuse une scène invalide, une intensité ou une confiance hors limites, une sortie incomplète, un texte trop long et les références lexicales héritées de l'œuvre source. Il ne reçoit aucun pointeur vers les structures mutables du personnage, de l'inventaire ou des missions.

## Pourquoi le petit LLM n'est pas le narrateur principal

Le modèle LeCarnet-3M reste une expérimentation. Le profil embarqué actuel impose 32 tokens de contexte et au plus neuf tokens de texte généré. Le dernier entraînement vérifié le 24 novembre 2026 a obtenu une perte d'entraînement de 1,9065, mais une meilleure perte de validation de 6,4704, sans amélioration utile au fil des époques. Les quatre exemples générés étaient incohérents et le contrôle qualité a échoué.

Une étude récente sur les modèles de langage et les microcontrôleurs ESP32 distingue clairement les systèmes assistés par un hôte, les systèmes reliés au réseau et les modèles réellement exécutés sur le microcontrôleur. Elle ne relève pas de LLM conversationnel généraliste démontré sur ESP32. Nexus ne doit donc pas présenter le petit modèle actuel comme une IA narrative fiable.

Référence technique : revue systématique 2026, *Language and Transformer Models with ESP32-Class Microcontrollers*, https://jurnal.unpad.ac.id/ijmt/article/view/72405/0.

Le modèle pourra être réévalué ultérieurement, mais uniquement derrière le moteur narratif : une génération ne sera jamais utilisée si elle est vide, incomplète, trop longue, hors sujet ou contraire au lore. Le texte déterministe restera le mode de secours et la source fiable.

## Validation

Le test tests/nexus_core/narrative_engine_test.cpp vérifie les scènes, la variation reproductible, la réaction aux preuves et à la confiance, le routage des événements et des choix, les appels ambigus, les limites de taille et le garde-fou d'originalité. Le workflow nexus-narrative-verify.yml exécute ces tests natifs avec les autres régressions du moteur.

## Limite de l'étape 3

Le moteur narratif autonome et ses tests relèvent de l'étape 3. Le branchement de chaque événement du jeu vers ce moteur, l'affichage Cardputer et la priorité entre texte déterministe et génération locale relèvent de l'étape 4. Les mesures de mémoire, de vitesse et de stabilité sur le véritable Cardputer ADV relèvent de l'étape 5.
