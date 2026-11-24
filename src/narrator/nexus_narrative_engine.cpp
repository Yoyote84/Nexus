#include "nexus_narrative_engine.h"

#include "nexus_lore_guard.h"

#include <stdio.h>
#include <string.h>

namespace nexus {
namespace {

struct SceneBank {
  const char* const* lines;
  size_t count;
};

#define NEXUS_SCENE_BANK(name, ...) \
  static const char* const name[] = {__VA_ARGS__}

NEXUS_SCENE_BANK(kOpening,
    "Valbrume dort encore lorsque la station Veyrac laisse passer une impulsion.",
    "Dans le carnet d'Alma Veyre, une heure a été corrigée deux fois.",
    "La radio grésille, puis retrouve un silence presque parfait.",
    "Ton premier relevé rejoint l'Atlas des Rémanences.",
    "Une page oubliée de la station Veyrac porte une annotation récente.");

NEXUS_SCENE_BANK(kFirstContactHelp,
    "Tu choisis de répondre au signal ; LIA enregistre l'heure et le motif.",
    "Tu privilégies l'aide sans quitter un lieu sûr ; la fréquence est conservée.",
    "Tu réponds avec prudence, sans prendre le signal pour une preuve.",
    "Ta décision est notée dans le carnet de terrain, avec le relevé original.");

NEXUS_SCENE_BANK(kFirstContactInvestigate,
    "Tu choisis d'examiner le signal ; les trois impulsions sont comparées.",
    "Tu privilégies les mesures et gardes l'enregistrement original intact.",
    "Tu demandes une analyse avant toute conclusion sur l'origine du signal.",
    "LIA relève l'écart entre les impulsions, sans identifier leur émetteur.");

NEXUS_SCENE_BANK(kFirstContactRetreat,
    "Tu décides de prendre du recul ; LIA archive le signal sans le poursuivre.",
    "Tu refuses de suivre une piste incertaine ; le relevé reste dans l'Atlas.",
    "Tu mets l'appareil en veille ; la découverte est conservée dans le carnet.",
    "Tu choisis la prudence ; rien ne t'oblige à poursuivre cette piste aujourd'hui.");

NEXUS_SCENE_BANK(kSectorDiscovered,
    "Un nouveau secteur entre dans l'Atlas ; LIA ouvre une fiche locale.",
    "La carte abstraite de Valbrume gagne un secteur encore peu documenté.",
    "Une zone jusque-là inconnue rejoint ton carnet d'exploration.",
    "L'Atlas accueille un nouveau secteur, sans désigner de destination précise.",
    "Une première empreinte apparaît dans un secteur qui n'avait pas été relevé.");

NEXUS_SCENE_BANK(kStrangeSignal,
    "Trois impulsions reviennent sur la bande ; leur intervalle varie légèrement.",
    "Une fréquence s'ouvre quelques secondes, puis retombe dans le silence.",
    "Le même motif apparaît deux fois avec un léger décalage.",
    "Un signal faible traverse le bruit radio ; sa durée est désormais consignée.",
    "La station Veyrac relève un motif absent des balises habituelles.");

NEXUS_SCENE_BANK(kPowerAnomaly,
    "Les mesures électriques chutent, puis reviennent à leur niveau initial.",
    "Une variation brève traverse le relevé ; une panne ordinaire reste possible.",
    "Le réseau perd sa stabilité pendant quelques secondes.",
    "Une tension inhabituelle apparaît sur l'enregistreur de terrain.",
    "L'appareil note un écart électrique, sans établir qu'il représente un danger.");

NEXUS_SCENE_BANK(kResidualTrace,
    "Un fragment sonore réapparaît dans une archive récente.",
    "Une empreinte ancienne semble se répéter avec un léger décalage.",
    "Le bruit de fond contient une forme déjà relevée dans le carnet.",
    "Une mesure revient après plusieurs jours ; sa provenance reste à vérifier.",
    "LIA retrouve une ressemblance entre deux fragments conservés séparément.");

NEXUS_SCENE_BANK(kFactionMovement,
    "Le Cercle des Relais modifie ses horaires d'écoute.",
    "Le Bureau des Mesures réclame une copie du relevé.",
    "Les Collecteurs proposent un échange de documents d'archives.",
    "Les groupes de Valbrume ne tirent pas les mêmes conclusions des indices.",
    "Une nouvelle consigne circule parmi les opérateurs des relais.");

NEXUS_SCENE_BANK(kDistressCall,
    "Une voix semble traverser le bruit radio, sans être clairement identifiable.",
    "Un fragment ressemble à un appel à l'aide, mais son origine reste inconnue.",
    "La bande contient une syllabe répétée que LIA ne peut pas attribuer.",
    "Une tonalité inhabituelle se mêle à l'enregistrement du relais.");

NEXUS_SCENE_BANK(kResonanceWave,
    "Une onde de résonance traverse plusieurs mesures au même instant.",
    "Les enregistreurs relèvent une variation simultanée dans plusieurs secteurs.",
    "Une onde brève se propage dans les archives locales.",
    "Plusieurs empreintes semblent répondre au même rythme.",
    "La chronologie des relevés révèle une nouvelle concordance.");

NEXUS_SCENE_BANK(kArchiveRecovered,
    "Une page signée Alma Veyre apparaît dans le dossier de la station Veyrac.",
    "Le carnet d'Alma décrit trois mesures prises avant la Nuit des Retours.",
    "Une annotation d'Alma Veyre relie deux fréquences encore mal documentées.",
    "Dans les archives de Veyrac, une ligne a été ajoutée après le classement.",
    "Un ancien relevé refait surface ; LIA conserve sa date et sa provenance.");

NEXUS_SCENE_BANK(kMissionCompleted,
    "L'objectif est confirmé : les relevés nécessaires sont réunis.",
    "Cette étape de l'enquête est terminée ; les preuves sont classées.",
    "Le carnet reçoit une nouvelle page consacrée à cette découverte.",
    "Le travail de terrain permet maintenant d'examiner une autre piste.");

NEXUS_SCENE_BANK(kQuietObservation,
    "Rien de nouveau n'apparaît dans les mesures.",
    "La fréquence reste silencieuse ; LIA conserve le dernier état connu.",
    "Aucune empreinte nouvelle n'est détectée dans ce relevé.",
    "Le carnet ne reçoit aucune anomalie aujourd'hui ; le calme est aussi une donnée.");

#undef NEXUS_SCENE_BANK

static const SceneBank kBanks[] = {
    {kOpening, sizeof(kOpening) / sizeof(kOpening[0])},
    {kFirstContactHelp, sizeof(kFirstContactHelp) / sizeof(kFirstContactHelp[0])},
    {kFirstContactInvestigate, sizeof(kFirstContactInvestigate) / sizeof(kFirstContactInvestigate[0])},
    {kFirstContactRetreat, sizeof(kFirstContactRetreat) / sizeof(kFirstContactRetreat[0])},
    {kSectorDiscovered, sizeof(kSectorDiscovered) / sizeof(kSectorDiscovered[0])},
    {kStrangeSignal, sizeof(kStrangeSignal) / sizeof(kStrangeSignal[0])},
    {kPowerAnomaly, sizeof(kPowerAnomaly) / sizeof(kPowerAnomaly[0])},
    {kResidualTrace, sizeof(kResidualTrace) / sizeof(kResidualTrace[0])},
    {kFactionMovement, sizeof(kFactionMovement) / sizeof(kFactionMovement[0])},
    {kDistressCall, sizeof(kDistressCall) / sizeof(kDistressCall[0])},
    {kResonanceWave, sizeof(kResonanceWave) / sizeof(kResonanceWave[0])},
    {kArchiveRecovered, sizeof(kArchiveRecovered) / sizeof(kArchiveRecovered[0])},
    {kMissionCompleted, sizeof(kMissionCompleted) / sizeof(kMissionCompleted[0])},
    {kQuietObservation, sizeof(kQuietObservation) / sizeof(kQuietObservation[0])}
};

uint32_t mix(uint32_t value) {
  value ^= value >> 16U;
  value *= 0x7FEB352DU;
  value ^= value >> 15U;
  value *= 0x846CA68BU;
  value ^= value >> 16U;
  return value;
}

uint32_t selectionKey(const NexusNarrativeContext& context) {
  uint32_t value = context.worldSeed ^ 0x9E3779B9U;
  value ^= context.eventSequence * 0x85EBCA6BU;
  value ^= context.simulatedDay * 0xC2B2AE35U;
  value ^= context.sectorKey + 0x27D4EB2FU;
  value ^= static_cast<uint32_t>(context.intensity) << 24U;
  value ^= static_cast<uint32_t>(context.evidenceCount) << 8U;
  value ^= static_cast<uint32_t>(context.liaTrust) << 16U;
  return mix(value);
}

const char* contextLine(const NexusNarrativeContext& context,
                        NarrativeScene scene) {
  if (scene == NarrativeScene::DistressCall) {
    return "Si le danger est réel, contacte les secours par les moyens habituels.";
  }
  if (context.evidenceCount >= 8U) {
    return "Plusieurs relevés concordent ; leur origine reste à établir.";
  }
  if (context.evidenceCount >= 3U) {
    return "Les comparaisons se précisent, mais les faits restent séparés des hypothèses.";
  }
  if (context.intensity >= 75U) {
    return "L'intensité est élevée, sans établir à elle seule un danger.";
  }
  if (context.liaTrust <= 25U) {
    return "LIA signale ses limites et classe cette lecture comme une hypothèse.";
  }
  if (context.liaTrust >= 80U) {
    return "LIA propose une piste ; tu restes libre de la vérifier ou non.";
  }
  if (context.evidenceCount > 0U) {
    return "LIA conserve la trace pour la comparer aux prochaines empreintes.";
  }
  if ((context.simulatedDay & 1U) == 0U) {
    return "La chronologie est conservée pour les comparaisons futures.";
  }
  return "Cette observation rejoint l'Atlas, sans imposer la suite de l'enquête.";
}

}  // namespace

NarrativeScene narrativeSceneForEvent(EventType event) {
  switch (event) {
    case EventType::StrangeSignal: return NarrativeScene::StrangeSignal;
    case EventType::PowerAnomaly: return NarrativeScene::PowerAnomaly;
    case EventType::ResidualTrace: return NarrativeScene::ResidualTrace;
    case EventType::FactionMovement: return NarrativeScene::FactionMovement;
    case EventType::DistressCall: return NarrativeScene::DistressCall;
    case EventType::ResonanceWave: return NarrativeScene::ResonanceWave;
    case EventType::None:
    default: return NarrativeScene::QuietObservation;
  }
}

bool narrativeSceneForFirstContactChoice(FirstContactChoice choice,
                                         NarrativeScene& scene) {
  switch (choice) {
    case FirstContactChoice::Help:
      scene = NarrativeScene::FirstContactHelp;
      return true;
    case FirstContactChoice::Investigate:
      scene = NarrativeScene::FirstContactInvestigate;
      return true;
    case FirstContactChoice::Retreat:
      scene = NarrativeScene::FirstContactRetreat;
      return true;
    default:
      return false;
  }
}

bool isNexusNarrativeComplete(const char* text) {
  if (!text) return false;
  size_t length = 0U;
  while (length <= kNexusNarrativeTextCapacity && text[length] != '\0') {
    const unsigned char value = static_cast<unsigned char>(text[length]);
    if (value < 0x20U || value == 0x7FU) return false;
    ++length;
  }
  if (length == 0U || length > kNexusNarrativeTextCapacity) return false;

  const char last = text[length - 1U];
  if (last != '.' && last != '!' && last != '?') return false;
  return !containsLegacyFictionReference(text);
}

bool buildNexusNarrative(const NexusNarrativeContext& context,
                         char* output, size_t outputCapacity) {
  if (!output || outputCapacity == 0U) return false;
  output[0] = '\0';

  const uint8_t sceneIndex = static_cast<uint8_t>(context.scene);
  if (sceneIndex >= static_cast<uint8_t>(NarrativeScene::Count) ||
      context.intensity > 100U || context.liaTrust > 100U) return false;

  const SceneBank& bank = kBanks[sceneIndex];
  if (!bank.lines || bank.count == 0U) return false;

  const uint32_t key = selectionKey(context);
  const char* first = bank.lines[key % bank.count];
  const char* second = contextLine(context, context.scene);

  char candidate[kNexusNarrativeTextCapacity + 1U] = {};
  const int written = snprintf(candidate, sizeof(candidate), "%s %s", first, second);
  if (written <= 0 ||
      static_cast<size_t>(written) > kNexusNarrativeTextCapacity ||
      static_cast<size_t>(written) + 1U > outputCapacity) return false;

  memcpy(output, candidate, static_cast<size_t>(written) + 1U);
  if (!isNexusNarrativeComplete(output)) {
    output[0] = '\0';
    return false;
  }
  return true;
}

}  // namespace nexus
