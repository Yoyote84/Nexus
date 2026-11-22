#!/usr/bin/env python3
"""Deterministic original-world migration for Nexus stage 3."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path.cwd()

SEEDS = [
("nexus-seed-001", "Le relais 07 vient d'émettre trois impulsions. Que réponds-tu ?", "Je note leur rythme avant de répondre. LIA, Lecteur d'Indices Acoustiques, confirme que le motif ne correspond à aucune balise connue."),
("nexus-seed-002", "Pourquoi appelle-t-on ce phénomène la Rémanence ?", "Parce que certains lieux conservent des fragments de sons et de mesures. Ils reviennent sans prévenir, comme une archive qui se serait réveillée."),
("nexus-seed-003", "Une cassette porte la date du lendemain. Que fais-tu ?", "Je vérifie l'étiquette et la bande. La Rémanence peut décaler l'ordre des enregistrements, mais cela ne prouve pas que le temps a changé."),
("nexus-seed-004", "La carte de Valbrume montre une zone blanche. Comment l'étudies-tu ?", "Je consigne seulement le secteur où je me trouve. Les blancs de la carte sont des relevés incomplets, pas une invitation à chercher un lieu dangereux."),
("nexus-seed-005", "LIA répète une phrase entendue quelques secondes plus tôt. Que lui demandes-tu ?", "Je lui demande de comparer les deux enregistrements. Une répétition peut révéler un écho, une erreur de bande ou une rémanence."),
("nexus-seed-006", "Tu retrouves une note signée Alma Veyre. Que lis-tu ?", "Alma a écrit que les impulsions reviennent par groupes de trois. Elle conseille de conserver les heures et les écarts, sans tirer de conclusion trop vite."),
("nexus-seed-007", "Un signal semble venir d'un bâtiment fermé. Que fais-tu ?", "Je reste dans un espace autorisé et accessible. Je peux enregistrer le signal à distance sans entrer dans une propriété ni prendre de risque."),
("nexus-seed-008", "Le Cercle des Relais demande ton relevé. Que transmets-tu ?", "Je partage la fréquence, l'heure et la forme du signal, sans coordonnées personnelles. Un relevé précis vaut mieux qu'une rumeur."),
("nexus-seed-009", "Le Bureau des Mesures veut récupérer ta cassette. Comment réagis-tu ?", "Je demande une copie et un reçu d'archive. Les données doivent rester vérifiables et ne pas disparaître dans un dossier fermé."),
("nexus-seed-010", "Un Collecteur prétend avoir trouvé une carte complète. Que lui demandes-tu ?", "Je lui demande la date, la méthode et les relevés qui soutiennent sa découverte. Une carte sans provenance n'est qu'une hypothèse."),
("nexus-seed-011", "Une lumière pulse au rythme d'un ancien enregistrement. Que notes-tu ?", "Je relève trois éléments : durée, intervalle et intensité. Je ne confonds pas une anomalie visuelle avec une présence vivante."),
("nexus-seed-012", "Une empreinte sonore apparaît dans une zone déjà explorée. Que fais-tu ?", "Je compare le nouvel échantillon à l'archive locale. Une rémanence peut changer d'intensité sans créer un nouveau secteur."),
("nexus-seed-013", "Le réseau électrique chute pendant quelques secondes. Comment réagis-tu ?", "Je sécurise mon matériel et j'attends le retour du courant. LIA conserve la dernière mesure pour éviter toute perte de données."),
("nexus-seed-014", "Deux groupes revendiquent le même relevé. Quelle est ta réponse ?", "Je garde l'original daté et je fournis une copie identique aux deux groupes. Les faits doivent rester séparés des intérêts de chacun."),
("nexus-seed-015", "Un appel de détresse se mêle au bruit radio. Que fais-tu ?", "Je vérifie s'il s'agit d'un message réel et je contacte les secours par les moyens habituels si nécessaire. Le jeu ne remplace jamais une aide réelle."),
("nexus-seed-016", "La Rémanence semble plus forte après la pluie. Quelle hypothèse proposes-tu ?", "L'humidité pourrait modifier la propagation des signaux. Je note cette corrélation sans la présenter comme une certitude."),
("nexus-seed-017", "LIA ne reconnaît pas un fragment de voix. Que lui dis-tu ?", "Je lui demande de conserver le fragment comme inconnu. Il vaut mieux garder une incertitude que fabriquer une identité."),
("nexus-seed-018", "Tu trouves un carnet rempli de schémas de fréquences. Que fais-tu ?", "Je photographie les pages et je recopie les mesures lisibles. Je laisse les annotations originales intactes pour les prochains enquêteurs."),
("nexus-seed-019", "Un écho semble répondre à ta propre voix. Comment l'interprètes-tu ?", "Je reproduis le test à faible volume et j'enregistre le délai. Une réponse acoustique n'est pas forcément une conversation."),
("nexus-seed-020", "Ilyes Marot te propose de suivre un bruit hors du sentier. Que réponds-tu ?", "Je refuse de quitter un passage sûr. Nous pouvons relever le phénomène depuis un endroit public et reprendre l'étude plus tard."),
("nexus-seed-021", "La station Veyrac transmet un motif que personne n'a catalogué. Que fais-tu ?", "Je crée une entrée provisoire dans l'archive. Le motif reçoit un identifiant, une date et une description neutre."),
("nexus-seed-022", "Une vieille horloge s'arrête pendant une impulsion. Que conclus-tu ?", "Rien pour l'instant. Je vérifie son alimentation et je compare l'heure avec un appareil indépendant."),
("nexus-seed-023", "Le niveau de rémanence augmente dans plusieurs secteurs. Comment aides-tu le groupe ?", "Je rassemble les mesures comparables et je signale les écarts. Nous avançons par observations, sans supposer qu'une cause unique explique tout."),
("nexus-seed-024", "Une archive contient deux versions du même message. Laquelle gardes-tu ?", "Les deux. Je conserve les sources séparées et j'ajoute une note indiquant ce qui diffère entre les enregistrements."),
("nexus-seed-025", "Quelqu'un veut effacer une mesure qu'il juge impossible. Que proposes-tu ?", "Je recommande de la placer en quarantaine documentaire plutôt que de la supprimer. Une mesure étrange doit pouvoir être réexaminée."),
("nexus-seed-026", "La radio se tait soudainement. Que fais-tu ?", "Je vérifie la batterie, l'antenne et la fréquence. Si tout fonctionne, je marque simplement une période sans réception."),
("nexus-seed-027", "Une carte papier porte la mention Nuit des Retours. Que signifie-t-elle ?", "C'est le nom donné à l'incident du 14 octobre 1986, lorsque plusieurs enregistrements sont revenus avant leur émission prévue."),
("nexus-seed-028", "LIA te demande si la Rémanence est dangereuse. Que réponds-tu ?", "Nous ne le savons pas encore. Restons prudents, évitons les zones interdites et ne transformons pas une hypothèse en certitude."),
("nexus-seed-029", "Tu dois choisir entre conserver une cassette ou poursuivre un relevé. Que décides-tu ?", "Je sécurise d'abord l'archive. Une donnée perdue ne pourra plus aider à comprendre les prochains signaux."),
("nexus-seed-030", "Un secteur connu produit une nouvelle anomalie. Que notes-tu ?", "Je distingue le lieu déjà cartographié du nouvel événement. La progression du monde et les découvertes restent deux choses différentes."),
("nexus-seed-031", "Une voix demande le nom de l'arpenteur. Que réponds-tu ?", "Je donne mon nom de terrain, puis je demande l'identifiant de l'émetteur. Un échange fiable commence par des informations vérifiables."),
("nexus-seed-032", "Le Cercle des Relais t'envoie une fréquence de secours. Que fais-tu ?", "Je la note dans le carnet et je vérifie qu'elle ne remplace pas une fréquence officielle de sécurité. Les communications d'urgence restent prioritaires."),
("nexus-seed-033", "Une série de marques apparaît sur une ancienne carte. Que suggèrent-elles ?", "Elles pourraient représenter des points de mesure successifs. Je les compare aux dates avant de dessiner un itinéraire."),
("nexus-seed-034", "La Rémanence reproduit un bruit de pas dans une pièce vide. Que dis-tu ?", "Je décris le son sans affirmer qu'une personne s'y trouve. Une archive acoustique peut conserver un bruit sans conserver sa source."),
("nexus-seed-035", "Un membre du groupe est inquiet après une observation. Comment l'aides-tu ?", "Je l'écoute et je lui propose de faire une pause dans un endroit sûr. Personne n'a besoin de s'isoler pour prouver quoi que ce soit."),
("nexus-seed-036", "LIA retrouve une note incomplète d'Alma. Comment la complètes-tu ?", "Je n'invente pas les mots manquants. Je marque les passages illisibles et je cherche une seconde copie dans les archives."),
("nexus-seed-037", "Une onde de résonance traverse plusieurs mesures. Que fais-tu ?", "Je compare les horodatages et les intensités. Une onde peut relier des observations sans ouvrir de passage vers un autre monde."),
("nexus-seed-038", "Un nouvel arpenteur te demande comment explorer. Que lui conseilles-tu ?", "Avance à ton rythme, reste dans les lieux accessibles et consigne tes observations. Aucun point précis ne mérite de prendre un risque."),
("nexus-seed-039", "Le signal de la station Veyrac revient après des semaines de silence. Que réponds-tu ?", "Je confirme la réception et j'archive l'heure. Le retour du signal est une nouvelle donnée, pas la preuve que son émetteur est présent."),
("nexus-seed-040", "LIA te demande ce qu'est Nexus. Que lui réponds-tu ?", "Nexus est le réseau de secteurs et d'archives qui relie nos observations. Chaque point ajoute une pièce à l'Atlas des Rémanences.")
]

UNIVERSE = """# Nexus — L'Atlas des Rémanences

## Identité

**Nexus** est un jeu de rôle d'exploration hors ligne. Son sous-titre narratif est **L'Atlas des Rémanences**. L'ambiance associe mystère scientifique, radios analogiques, carnets de terrain et exploration libre. Le jeu ne reprend ni personnages, ni lieux, ni créatures, ni institutions d'une franchise existante.

## Cadre

L'histoire-cadre se déroule en **1987**, autour de **Valbrume**, une commune fictive organisée autour d'un ancien réseau de mesures et de relais radio. La **station Veyrac** servait à synchroniser des observations acoustiques, météorologiques et géophysiques.

Le 14 octobre 1986, pendant la **Nuit des Retours**, plusieurs stations ont enregistré des fragments sonores quelques secondes avant leur émission prévue. Les horloges n'ont pas voyagé dans le temps et aucun monde parallèle n'a été découvert : les appareils ont conservé des séquences impossibles à replacer dans leur ordre habituel.

## Phénomène central : la Rémanence

La **Rémanence** désigne le retour irrégulier de fragments d'informations dans certains enregistrements : impulsions radio, sons, variations électriques, motifs lumineux et mesures contradictoires. Elle peut se manifester dans des secteurs éloignés et évoluer au fil du temps.

Les **empreintes rémanentes** sont des traces mesurables laissées par le phénomène. Elles ne sont pas des monstres ou des espèces humanoïdes. Une observation doit rester décrite avec prudence : le jeu distingue toujours une mesure, une hypothèse et une interprétation.

## Le réseau Nexus

Nexus est le nom donné à l'Atlas des Rémanences : un ensemble de secteurs, de relevés et d'archives qui se répondent. La grille d'exploration est calculée localement à partir des déplacements du joueur. Elle ne dirige jamais le joueur vers un point dangereux, une propriété privée ou un lieu interdit. Les découvertes sont abstraites par secteur et ne nécessitent aucun paquet cartographique à télécharger.

## Personnage et voix d'assistance

Le joueur incarne un **arpenteur**, libre de choisir son nom et sa spécialité. Il observe, enregistre, compare et décide de ce qu'il partage.

**LIA** signifie **Lecteur d'Indices Acoustiques**. C'est un logiciel d'archive embarqué dans le matériel de terrain, pas une personne disparue. LIA trie les fragments, rappelle les relevés antérieurs et propose des pistes. Le moteur de jeu conserve seul l'autorité sur les missions, les objets, les statistiques, les sauvegardes et les conséquences des choix.

**Alma Veyre**, cartographe et responsable de plusieurs relevés de la station Veyrac, a laissé un carnet incomplet après la Nuit des Retours. Ses notes constituent l'un des fils d'enquête.

## Groupes

- **Le Cercle des Relais** : opérateurs bénévoles qui entretiennent les fréquences et échangent des relevés.
- **Le Bureau des Mesures** : service technique chargé de vérifier les appareils et de préserver les données officielles.
- **Les Collecteurs** : indépendants qui recherchent des archives oubliées et des pièces de mesure.

Aucun groupe n'est automatiquement bon ou mauvais. Leurs motivations peuvent diverger selon les découvertes du joueur.

## Vocabulaire du monde

| Terme | Sens dans Nexus |
|---|---|
| Rémanence | Retour irrégulier d'un fragment d'information |
| Empreinte | Trace mesurable d'une Rémanence |
| Impulsion | Signal bref utilisé pour identifier un motif |
| Secteur | Cellule abstraite de progression géographique |
| Onde de résonance | Variation intense du phénomène, sans portail ni passage |
| Archive | Donnée horodatée conservée par LIA ou l'arpenteur |
| Nuit des Retours | Incident initial du 14 octobre 1986 |

## Boucle de jeu

1. Le monde évolue localement avec le temps ou avec les jours de jeu.
2. Les déplacements révèlent des secteurs et peuvent produire des événements.
3. Le joueur compare les empreintes, accomplit des missions et développe son personnage.
4. LIA raconte les conséquences à partir des données validées.
5. Les sauvegardes restent locales et la partie fonctionne sans téléphone, réseau ou Wi-Fi.

## Règles narratives non négociables

- Ne jamais présenter la Rémanence comme une dimension inversée ou un monde parallèle.
- Ne pas introduire de créatures ou de personnages empruntés à une œuvre existante.
- Ne pas envoyer le joueur vers des coordonnées précises, des bâtiments privés ou des lieux dangereux.
- Ne jamais demander de grimper, pénétrer, traverser une route dangereuse ou contourner une interdiction.
- Ne jamais inventer un objet, une mission, une récompense ou une action déjà accomplie.
- Le narrateur ne modifie jamais directement l'état du jeu.
- Les événements inconnus doivent rester des hypothèses, pas des certitudes.
"""

STYLE = """# Guide narratif et éditorial Nexus

## Ton
Mystère calme, enquête de terrain, inquiétude progressive, curiosité scientifique. Le récit privilégie les détails concrets : souffle radio, bandes magnétiques, variations de fréquence, carnets de terrain, cartes annotées, météo et bruits ordinaires devenus ambigus.

## Langue
Français naturel, phrases courtes adaptées à un écran de Cardputer. Éviter les longues descriptions, les termes techniques non expliqués et les anglicismes inutiles.

## LIA
LIA est un outil d'archive. Elle parle avec précision, calme et modestie. Elle distingue ce qu'elle sait, ce qu'elle déduit et ce qu'elle ignore. Elle ne prétend jamais être humaine et ne décide pas à la place du joueur.

## Structure des scènes
Une scène courte contient une observation vérifiable, une incertitude, puis une question ou un choix. Les choix sont équilibrés et ne supposent jamais que le joueur doit se mettre en danger.

## Garde-fous
Pas de noms, dialogues, lieux, monstres, organisations, logos, musiques ou scènes appartenant à une franchise tierce. Pas de reproduction de mise en scène ou de séquences reconnaissables. Le simple genre du mystère et de l'exploration reste libre, mais l'expression narrative doit être originale.
"""

def rename_sources():
    for base in (ROOT / "src", ROOT / "tests"):
        for p in sorted((x for x in base.rglob("*") if x.is_file()), key=lambda x: len(x.parts), reverse=True):
            name = p.name.replace("hawkins", "nexus").replace("Hawkins", "Nexus").replace("HAWKINS", "NEXUS")
            if name != p.name:
                p.rename(p.with_name(name))
    old = ROOT / "src/narrator/hawkins_llm"
    if old.exists():
        old.rename(ROOT / "src/narrator/local_llm")
    for old_name, new_name in (("hawkinstest", "nexus_core"), ("hawkinsllmtest", "nexus_llm"), ("hawkinsaitest", "nexus_protocol")):
        old = ROOT / "tests" / old_name
        if old.exists():
            old.rename(ROOT / "tests" / new_name)

def replace_source_names():
    preserve = {
        '"hawkins"': '__KEEP_NVS_KEY__',
        '"/HAWKINS/SLOT0.HWS"': '__KEEP_SD_SLOT0__',
        '"/HAWKINS/SLOT1.HWS"': '__KEEP_SD_SLOT1__',
        '"/HAWKINS/WRITING.TMP"': '__KEEP_SD_TEMP__',
        '"/HAWKINS"': '__KEEP_SD_DIR__',
    }
    restore = {
        '__KEEP_NVS_KEY__': '"hawkins"',
        '__KEEP_SD_SLOT0__': '"/HAWKINS/SLOT0.HWS"',
        '__KEEP_SD_SLOT1__': '"/HAWKINS/SLOT1.HWS"',
        '__KEEP_SD_TEMP__': '"/HAWKINS/WRITING.TMP"',
        '__KEEP_SD_DIR__': '"/HAWKINS"',
    }
    exts = {".cpp", ".h", ".S", ".sh", ".py", ".md", ".json", ".jsonl", ".txt"}
    for base in (ROOT / "src", ROOT / "tests", ROOT / "tools"):
        for p in base.rglob("*"):
            if not p.is_file() or p.suffix not in exts:
                continue
            if p == ROOT / "tools/migration/originalize_step3.py":
                continue
            try:
                data = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            orig = data
            for old, token in preserve.items():
                data = data.replace(old, token)
            data = data.replace("HAWKINS", "NEXUS").replace("Hawkins", "Nexus").replace("hawkins", "nexus")
            data = data.replace("HKA/1 ", "NEX/1 ")
            data = data.replace("EventType::CreatureTrace", "EventType::ResidualTrace")
            data = data.replace("EventType::PortalFluctuation", "EventType::ResonanceWave")
            data = data.replace("nexus_llm/", "local_llm/")
            for token, old in restore.items():
                data = data.replace(token, old)
            if data != orig:
                p.write_text(data, encoding="utf-8", newline="")

def rewrite_app_scene():
    p = ROOT / "src/platform/cardputer/legacy/nexus_app.cpp"
    data = p.read_text(encoding="utf-8")
    a = data.find("void drawFirstContactPage() {")
    b = data.find("\nvoid drawStoragePage()", a)
    if a < 0 or b < 0:
        raise SystemExit("Écran de premier contact introuvable.")
    block = r'''void drawFirstContactPage() {
  cv.fillScreen(TFT_BLACK);
  const bool resolved = (adventure.storyFlags & 0x01U) != 0U;
  drawPageHeader(resolved ? "NEXUS / LIA" : "NEXUS / RELAIS",
                 resolved ? "ARCHIVE" : "RELAIS 07", ACCENT);
  cv.setFont(&fonts::Font0);
  cv.setTextSize(1);
  cv.setTextDatum(top_left);

  if (!resolved) {
    cv.setTextColor(TFT_WHITE, TFT_BLACK);
    cv.drawString("00:17. LE RELAIS 07 EMET.", 5, 20);
    cv.drawString("LA CARTE PERD UN SECTEUR.", 5, 32);
    cv.drawString("UNE VOIX SYNTHETIQUE :", 5, 44);
    cv.drawString("\"ICI LIA. JE LIS LES ECHOS.\"", 5, 56);

    cv.setTextColor(ACCENT, TFT_BLACK);
    cv.drawString("1 REPONDRE AU RELAIS", 5, 75);
    cv.setTextColor(TFT_WHITE, TFT_BLACK);
    cv.drawString("2 ENREGISTRER LES BIPS", 5, 88);
    cv.drawString("3 COUPER ET MARQUER", 5, 101);
  } else {
    const char* lines[4] = {};
    switch (adventure.firstContactChoice) {
      case 1U:
        lines[0] = "TU AS ACCUSE RECEPTION.";
        lines[1] = "LIA : \"SIGNAL RECU.\"";
        lines[2] = "LE RELAIS GARDE LE MOTIF.";
        lines[3] = "LE CARNET S'OUVRE.";
        break;
      case 2U:
        lines[0] = "TU AS ENREGISTRE LES BIPS.";
        lines[1] = "LIA : \"TROIS TEMPS DISTINCTS.\"";
        lines[2] = "LE MOTIF REVIENT EN BOUCLE.";
        lines[3] = "UNE TRACE EST ARCHIVEE.";
        break;
      case 3U:
        lines[0] = "TU AS COUPE LA RECEPTION.";
        lines[1] = "LIA : \"CHOIX CONSIGNE.\"";
        lines[2] = "LA ZONE RESTE A RELEVER.";
        lines[3] = "LE RELAIS GARDE LE SILENCE.";
        break;
      default:
        // Anciennes sauvegardes v1 : le choix avait ete consomme mais pas stocke.
        lines[0] = "TON ANCIEN CHOIX EST CONSERVE.";
        lines[1] = "LIA : \"JE SUIS TOUJOURS LA.\"";
        lines[2] = "LA SUITE NE MODIFIE PAS TON PROFIL.";
        lines[3] = "TU PEUX REPRENDRE TON HISTOIRE.";
        break;
    }
    for (uint8_t i = 0U; i < 4U; ++i) {
      cv.setTextColor(i == 0U ? ACCENT : TFT_WHITE, TFT_BLACK);
      cv.drawString(lines[i], 5, 25 + static_cast<int>(i) * 15);
    }
  }

  cv.setTextDatum(bottom_left);
  cv.setTextColor(ICON_DIM, TFT_BLACK);
  cv.drawString(resolved ? "A IA  Q RETOUR" : "1-3 CHOIX  A IA  Q RETOUR", 3, SH - 2);
}
'''
    data = data[:a] + block + data[b:]
    # Update internal include paths for the new folder boundaries.
    includes = {
        '"nexus_runtime.h"': '"core/nexus_runtime.h"',
        '"nexus_ai_protocol.h"': '"narrator/nexus_ai_protocol.h"',
        '"nexus_nvs.h"': '"storage/nexus_nvs.h"',
        '"nexus_exploration.h"': '"exploration/nexus_exploration.h"',
        '"nexus_character.h"': '"core/nexus_character.h"',
        '"nexus_missions.h"': '"core/nexus_missions.h"',
        '"nexus_adventure.h"': '"core/nexus_adventure.h"',
        '"nexus_adventure_store.h"': '"storage/nexus_adventure_store.h"',
        '"nexus_narrative_store.h"': '"narrator/nexus_narrative_store.h"',
        '"local_llm/runtime.h"': '"narrator/local_llm/runtime.h"',
        '"nexus_sd_backup.h"': '"storage/nexus_sd_backup.h"',
    }
    for old, new in includes.items():
        data = data.replace(old, new)
    data = data.replace('case nexus::EventType::StrangeSignal: return "signal";', 'case nexus::EventType::StrangeSignal: return "echo";')
    data = data.replace('case nexus::EventType::PowerAnomaly: return "anomalie";', 'case nexus::EventType::PowerAnomaly: return "derive";')
    data = data.replace('case nexus::EventType::ResidualTrace: return "trace";', 'case nexus::EventType::ResidualTrace: return "empreinte";')
    data = data.replace('case nexus::EventType::FactionMovement: return "faction";', 'case nexus::EventType::FactionMovement: return "groupe";')
    data = data.replace('case nexus::EventType::ResonanceWave: return "breche";', 'case nexus::EventType::ResonanceWave: return "onde";')
    data = data.replace('return "sensitif";', 'return "analyste";')
    data = data.replace('return "Lia";', 'return "LIA";')
    data = data.replace('return "REPONDRE A LIA (Q)";', 'return "REPONDRE AU RELAIS (Q)";')
    # Runtime guard for narrative output.
    if '"narrator/nexus_lore_guard.h"' not in data:
        data = data.replace('#include "narrator/nexus_ai_protocol.h"', '#include "narrator/nexus_ai_protocol.h"\n#include "narrator/nexus_lore_guard.h"')
    call = "  const bool ok = nexus::nexusLlmRuntimeGenerate(\n      prompt, generated, sizeof(generated), 10U);"
    if call in data:
        data = data.replace(call,
            "  bool ok = nexus::nexusLlmRuntimeGenerate(\n"
            "      prompt, generated, sizeof(generated), 10U);\n"
            "  if (ok && nexus::containsLegacyFictionReference(generated)) {\n"
            "    generated[0] = '\\0';\n"
            "    ok = false;\n"
            "    Serial.println(\"[nexus-llm] sortie rejetee: reference de fiction externe\");\n"
            "  }", 1)
    else:
        raise SystemExit("Appel de génération du narrateur introuvable.")
    p.write_text(data, encoding="utf-8", newline="")

def add_guard_and_test():
    base = ROOT / "src/narrator"
    (base / "nexus_lore_guard.h").write_text(
        "#pragma once\nnamespace nexus {\nbool containsLegacyFictionReference(const char* text);\n}\n",
        encoding="utf-8", newline="")
    (base / "nexus_lore_guard.cpp").write_text(r'''#include "nexus_lore_guard.h"
namespace nexus {
namespace {
char lowerAscii(char c) { return c >= 'A' && c <= 'Z' ? static_cast<char>(c + 32) : c; }
bool has(const char* text, const char* phrase) {
  if (!text || !phrase || !*phrase) return false;
  for (const char* p = text; *p; ++p) {
    const char* a = p;
    const char* b = phrase;
    while (*a && *b && lowerAscii(*a) == lowerAscii(*b)) { ++a; ++b; }
    if (!*b) return true;
  }
  return false;
}
}
bool containsLegacyFictionReference(const char* text) {
  static const char* const terms[] = {
    "hawkins", "stranger things", "upside down", "demogorgon",
    "mind flayer", "vecna", "brenner", "starcourt", "hellfire club",
    "demodog", "demobat", "will byers", "dustin", "mike wheeler",
    "lucas sinclair", "jim hopper", "joyce byers", "steve harrington",
    "robin buckley", "nancy wheeler", "max mayfield", "eleven"
  };
  for (const char* term : terms) if (has(text, term)) return true;
  return false;
}
}
''', encoding="utf-8", newline="")
    test_dir = ROOT / "tests/nexus_core"
    (test_dir / "lore_guard_test.cpp").write_text(r'''#include "nexus_lore_guard.h"
#include <assert.h>
int main() {
  assert(!nexus::containsLegacyFictionReference("LIA archive un echo a Valbrume."));
  assert(!nexus::containsLegacyFictionReference("La Rémanence produit trois impulsions."));
  assert(nexus::containsLegacyFictionReference("Un signal vient de Hawkins."));
  assert(nexus::containsLegacyFictionReference("The Upside Down appears."));
  assert(nexus::containsLegacyFictionReference("Une trace de Demogorgon."));
  return 0;
}
''', encoding="utf-8", newline="")
    build = test_dir / "build.sh"
    data = build.read_text(encoding="utf-8")
    data += '\n"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS -I ../../src/narrator lore_guard_test.cpp ../../src/narrator/nexus_lore_guard.cpp -o /tmp/nexus-lore-guard-test\n/tmp/nexus-lore-guard-test\n'
    build.write_text(data, encoding="utf-8", newline="")

def update_training():
    path = ROOT / "tools/model/seed_fr.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps({"id": i, "prompt": p, "response": r}, ensure_ascii=False) + "\n" for i, p, r in SEEDS), encoding="utf-8", newline="")
    prep = ROOT / "tools/model/prepare_fr_dataset.py"
    data = prep.read_text(encoding="utf-8")
    if "LEGACY_STORY_TERMS" not in data:
        data = data.replace("import re\n", "import re\nimport unicodedata\n")
        anchor = 'UNSAFE_LABELS = {"pii", "not_appropriate", "hate_speech", "sexual_content", "spam", "lang_mismatch", "fails_task"}\n'
        extra = anchor + '''
LEGACY_STORY_TERMS = (
    "hawkins", "stranger things", "upside down", "demogorgon", "mind flayer",
    "vecna", "brenner", "starcourt", "hellfire club", "demodog", "demobat",
    "will byers", "dustin", "mike wheeler", "lucas sinclair", "jim hopper",
    "joyce byers", "steve harrington", "robin buckley", "nancy wheeler",
    "max mayfield", "eleven",
)
def contains_legacy_story_term(*values: str) -> bool:
    import unicodedata
    text = " ".join(values).casefold()
    text = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return any(term in text for term in LEGACY_STORY_TERMS)
'''
        data = data.replace(anchor, extra)
        data = data.replace('if not (12 <= len(prompt) <= 240 and 12 <= len(response) <= 250):',
                            'if contains_legacy_story_term(prompt, response):\n                continue\n            if not (12 <= len(prompt) <= 240 and 12 <= len(response) <= 250):')
        data = data.replace('if not (12 <= len(prompt) <= 260 and 12 <= len(response) <= 320):',
                            'if contains_legacy_story_term(prompt, response):\n            continue\n        if not (12 <= len(prompt) <= 260 and 12 <= len(response) <= 320):')
        data = data.replace('if len(prompt) < 8 or len(response) < 8:',
                            'if len(prompt) < 8 or len(response) < 8:')
        data = data.replace('rows.append({"id": str(row.get("id") or f"seed-{line_no}"),',
                            'if contains_legacy_story_term(prompt, response):\n            raise SystemExit(f"seed_fr.jsonl:{line_no}: référence narrative héritée interdite")\n        rows.append({"id": str(row.get("id") or f"seed-{line_no}"),')
    data = data.replace("hawkins-original", "nexus-original")
    data = data.replace("Les exemples Nexus originaux sont", "Les exemples originaux Nexus sont")
    data = data.replace('"hawkins_seed_count": len(seeds)', '"nexus_seed_count": len(seeds)')
    data = data.replace('"hawkins_seed_repeat": args.seed_repeat', '"nexus_seed_repeat": args.seed_repeat')
    data = data.replace("project-authored Nexus seeds", "project-authored Nexus seeds")
    data = data.replace('"base_model": "TheREZOR/TinyTalk"', '"base_model": "MaxLSB/LeCarnet-3M"')
    data = data.replace('"base_model_license": "CC-BY-4.0"', '"base_model_license": "MIT"')
    data = data.replace('"corpus_license": "Apache-2.0 for OASST1 and French Alpaca; project-authored Nexus seeds"',
                        '"corpus_license": "Apache-2.0 for OASST1 and French Alpaca; project-authored Nexus seeds"')
    data = data.replace('"context_target_tokens": 80', '"context_target_tokens": 32')
    prep.write_text(data, encoding="utf-8", newline="")

    fine = ROOT / "tools/model/finetune_fr.py"
    data = fine.read_text(encoding="utf-8")
    data = data.replace(
        "Fine-tune TheREZOR/TinyTalk on short French chat pairs for an 80-token MCU window.",
        "Fine-tune the French LeCarnet-3M narrator for the 32-token Nexus Cardputer context."
    )
    data = data.replace("La radio grésille dans le sous-sol. Que remarques-tu ?", "Le relais 07 émet trois impulsions. Que réponds-tu ?")
    data = data.replace("Nous sommes devant une porte froide au laboratoire. Que proposes-tu ?", "Une cassette de Valbrume porte une date incohérente. Que vérifies-tu ?")
    data = data.replace("Une lumière clignote dans la forêt après minuit. Décris la scène.", "La station Veyrac renvoie un écho absent du registre. Que notes-tu ?")
    fine.write_text(data, encoding="utf-8", newline="")

    (ROOT / "tools/model/README.md").write_text("""# Narrateur local français de Nexus

Le pipeline entraîne et exporte le petit modèle de narration destiné au Cardputer ADV.

- Modèle de base : MaxLSB/LeCarnet-3M, révision épinglée dans le workflow.
- Corpus de spécialisation : seed_fr.jsonl, dialogues originaux de Valbrume, LIA et la Rémanence.
- Données publiques complémentaires : OpenAssistant/OASST1 et Alpaca GPT-4 French, sous réserve de leurs licences et filtres.
- Export firmware : CRDP v3 LLaMA Q4_0 row-planar + tokenizer CTK2 byte-level BPE.
- Fenêtre d'inférence du Cardputer : 32 tokens.

Le workflow nexus-model-rebuild.yml reconstruit les poids, le tokenizer, les sommes SHA-256 et le manifeste. Il refuse les références narratives distinctives de l'ancien univers dans les exemples de données. Les réponses générées restent soumises au garde-fou lexical intégré au runtime.

Le modèle binaire présent avant la reconstruction est une version provisoire issue de l'ancien entraînement. Il n'est pas une livraison Nexus tant que le workflow de reconstruction et les contrôles ne sont pas réussis.

Le narrateur propose uniquement du texte et des pistes. Le moteur déterministe conserve l'autorité sur les statistiques, l'inventaire, les missions, les choix et les sauvegardes.
""", encoding="utf-8", newline="")

def write_docs():
    (ROOT / "docs/UNIVERSE.md").write_text(UNIVERSE, encoding="utf-8", newline="")
    (ROOT / "docs/NARRATIVE_STYLE.md").write_text(STYLE, encoding="utf-8", newline="")
    (ROOT / "docs/ORIGINALITY_AND_PROVENANCE.md").write_text("""# Originalité, provenance et droits

Les textes de l'univers Nexus, notamment le cadre de Valbrume, la Rémanence, le réseau Nexus, LIA, Alma Veyre, les groupes et le corpus de dialogues de tools/model/seed_fr.jsonl, sont rédigés pour ce projet.

Les mécaniques générales (exploration par secteurs, missions, inventaire, progression, événements et narration locale) sont conservées et ne sont pas des personnages ou textes d'une franchise.

Le moteur local et le modèle de base restent soumis à leurs licences tierces. Les notices de provenance et les licences correspondantes sont conservées dans src/narrator/local_llm/ et dans les archives de migration. Le nouveau corpus ne remplace pas les obligations d'attribution du modèle de base ni des corpus publics utilisés pour le réentraînement.

Le modèle binaire actuellement présent dans le dépôt provient de l'ancienne étape de narration. Il est provisoire et non approuvé pour une publication Nexus tant qu'il n'a pas été réentraîné sur le corpus original, exporté, puis contrôlé. Le workflow nexus-model-rebuild.yml réalise cette reconstruction. L'intégration et le budget de mémoire/Flash seront vérifiés à l'étape 4 ; les essais physiques à l'étape 5.

Le nom Nexus est le titre retenu par le propriétaire du projet. Ce dépôt ne constitue pas une recherche d'antériorité ou une garantie de disponibilité juridique du nom. Une recherche de marque dans les territoires et classes pertinents reste nécessaire avant une diffusion commerciale.
""", encoding="utf-8", newline="")
    (ROOT / "docs/migration/LEGACY_SOURCE_NOTES.md").write_text("""# Archives de migration

Les documents docs/source-notes/ sont des instantanés historiques importés depuis le dépôt ROZA pour assurer la traçabilité technique. Ils décrivent l'ancienne version de travail et ne constituent ni le canon narratif ni le contenu destiné au joueur. L'univers actif est défini par docs/UNIVERSE.md et docs/NARRATIVE_STYLE.md.

Les anciennes clés NVS hawkins et le répertoire SD /HAWKINS sont conservés uniquement pour lire les sauvegardes antérieures.
""", encoding="utf-8", newline="")
    (ROOT / "docs/MIGRATION_STATUS.md").write_text("""# État de migration Nexus

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
""", encoding="utf-8", newline="")
    (ROOT / "README.md").write_text("""# Nexus — L'Atlas des Rémanences

Nexus est un jeu de rôle d'exploration hors ligne, destiné au M5Stack Cardputer ADV. Le joueur arpente librement des secteurs, recueille des empreintes de la Rémanence et reconstitue un atlas d'événements inhabituels.

## Univers

L'histoire-cadre prend place en 1987 autour de Valbrume, commune fictive marquée par la Nuit des Retours du 14 octobre 1986. Des fragments de sons et de mesures réapparaissent dans des archives et des signaux. Le joueur est un arpenteur assisté par LIA, le Lecteur d'Indices Acoustiques.

Lire docs/UNIVERSE.md, docs/NARRATIVE_STYLE.md et docs/ORIGINALITY_AND_PROVENANCE.md.

## Cible

- M5Stack Cardputer ADV.
- Module Cap LoRa-1262/GNSS en option pour les données locales de position.
- microSD pour les sauvegardes et les ressources.
- Aucun téléphone, réseau ou Wi-Fi nécessaire pendant une partie.

## Organisation

- src/core/ — monde, personnage, missions et règles déterministes.
- src/exploration/ — secteurs et événements de déplacement.
- src/narrator/ — protocole, mémoire et modèle local.
- src/storage/ — codecs et adaptateurs de persistance.
- src/platform/cardputer/ — contrôleur historique à découpler à l'étape 4.
- tests/ — tests natifs.
- tools/model/ — corpus, entraînement et export du narrateur.

## Migration en cinq étapes

- [x] 1/5 — audit.
- [x] 2/5 — extraction dans ce dépôt.
- [x] 3/5 — univers, textes et corpus originaux.
- [ ] 4/5 — adaptation et intégration dans le firmware ROZA.
- [ ] 5/5 — firmware installable et essais Cardputer.

Le binaire de modèle déjà présent est temporaire jusqu'à l'exécution réussie du workflow nexus-model-rebuild.yml. Les clés de sauvegarde historiques restent compatibles ; voir docs/migration/LEGACY_SOURCE_NOTES.md.
""", encoding="utf-8", newline="")

def finalize_code():
    world_h = ROOT / "src/core/nexus_world.h"
    data = world_h.read_text(encoding="utf-8")
    data = data.replace("CreatureTrace", "ResidualTrace").replace("PortalFluctuation", "ResonanceWave")
    world_h.write_text(data, encoding="utf-8", newline="")
    world_cpp = ROOT / "src/core/nexus_world.cpp"
    data = world_cpp.read_text(encoding="utf-8")
    data = data.replace('return "Signal étrange";', 'return "Écho radio";')
    data = data.replace('return "Anomalie électrique";', 'return "Dérive électrique";')
    data = data.replace('return "Trace de créature";', 'return "Empreinte rémanente";')
    data = data.replace('return "Mouvement de faction";', 'return "Activité de groupe";')
    data = data.replace('return "Appel de détresse";', 'return "Appel de secours";')
    data = data.replace('return "Fluctuation de brèche";', 'return "Onde de résonance";')
    world_cpp.write_text(data, encoding="utf-8", newline="")
    mission = ROOT / "src/core/nexus_missions.cpp"
    data = mission.read_text(encoding="utf-8")
    data = data.replace('{"LE PREMIER SIGNAL", "Repondre au premier appel radio", 1U},', '{"PREMIER CONTACT", "Accuser reception du relais LIA", 1U},')
    data = data.replace('{"CARTOGRAPHIE", "Explorer trois secteurs distincts", 3U},', '{"CARTOGRAPHIE DES ECHOS", "Explorer trois secteurs distincts", 3U},')
    data = data.replace('{"PISTE DE L\\'ANOMALIE", "Trouver deux signaux", 2U},', '{"ARCHIVE INCOMPLETE", "Retrouver deux empreintes remanentes", 2U},')
    mission.write_text(data, encoding="utf-8", newline="")
    adventure = ROOT / "src/core/nexus_adventure.cpp"
    data = adventure.read_text(encoding="utf-8").replace('case AdventureItem::Evidence: return "PREUVE";', 'case AdventureItem::Evidence: return "FRAGMENT ARCHIVE";')
    adventure.write_text(data, encoding="utf-8", newline="")
    character = ROOT / "src/core/nexus_character.cpp"
    data = character.read_text(encoding="utf-8").replace('{"SENSITIF", "Resiste aux anomalies", "Bonus : Perception / Charisme",', '{"ANALYSTE", "Lit les motifs de remanence", "Bonus : Perception / Charisme",')
    character.write_text(data, encoding="utf-8", newline="")
    exploration = ROOT / "src/exploration/nexus_exploration.cpp"
    data = exploration.read_text(encoding="utf-8").replace('mission "Piste de l\\'anomalie"', 'mission "Archive incomplete"')
    exploration.write_text(data, encoding="utf-8", newline="")
    # Rewrite test fixture name, not player save formats.
    test = ROOT / "tests/nexus_core/adventure_test.cpp"
    data = test.read_text(encoding="utf-8").replace('"ELEVEN"', '"ALIX"')
    test.write_text(data, encoding="utf-8", newline="")
    # Explicit include paths for the new source boundaries.
    test_llm = ROOT / "tests/nexus_llm/build.sh"
    if test_llm.exists():
        data = test_llm.read_text(encoding="utf-8").replace("../../src/local_llm", "../../src/narrator/local_llm")
        test_llm.write_text(data, encoding="utf-8", newline="")
    # Mark model as provisional until the new corpus has been trained and exported.
    manifest = ROOT / "src/narrator/local_llm/assets/model_manifest.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["status"] = "legacy_asset_pending_original_nexus_retrain"
    data["lore_training_status"] = "not_approved_for_nexus_release"
    data["note"] = "Temporary pre-Nexus narrative fine-tune. Replace through nexus-model-rebuild.yml before release."
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="")
    # Document and preserve the legacy storage namespace and folder.
    nvs = ROOT / "src/storage/nexus_nvs.cpp"
    data = nvs.read_text(encoding="utf-8")
    data = data.replace('const char* kNamespace = "hawkins";', '// Legacy save namespace retained to keep old player progress readable.\nconst char* kNamespace = "hawkins";')
    nvs.write_text(data, encoding="utf-8", newline="")
    advstore = ROOT / "src/storage/nexus_adventure_store.cpp"
    data = advstore.read_text(encoding="utf-8")
    data = data.replace('constexpr char kNamespace[] = "hawkins";', '// Legacy save namespace retained for existing adventure slots.\nconstexpr char kNamespace[] = "hawkins";')
    advstore.write_text(data, encoding="utf-8", newline="")
    sd = ROOT / "src/storage/nexus_sd_backup.cpp"
    data = sd.read_text(encoding="utf-8")
    data = data.replace('constexpr char kDirectory[] = "/HAWKINS";', '// Legacy SD archive path retained so old backups remain readable.\nconstexpr char kDirectory[] = "/HAWKINS";')
    sd.write_text(data, encoding="utf-8", newline="")
    # Point the assembler to the moved local narrator binaries.
    asm = ROOT / "src/narrator/local_llm/model_data.S"
    data = asm.read_text(encoding="utf-8")
    data = data.replace('"src/nexus_llm/assets/', '"src/narrator/local_llm/assets/')
    data = data.replace('"src/local_llm/assets/', '"src/narrator/local_llm/assets/')
    asm.write_text(data, encoding="utf-8", newline="")

def main():
    rename_sources()
    replace_source_names()
    rewrite_app_scene()
    add_guard_and_test()
    update_training()
    write_docs()
    finalize_code()
    print(f"Nexus originalization files updated; authored seed examples: {len(SEEDS)}")

if __name__ == "__main__":
    main()
