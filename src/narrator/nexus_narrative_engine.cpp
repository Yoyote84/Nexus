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
    "Marcheprime, 1984. La pierre gravée de Craissant réagit à trois impulsions radio.",
    "Manée reconnaît un symbole proche d'une vieille légende, sans en connaître le sens.",
    "La radio portative grésille alors qu'elle n'est pas allumée.",
    "Le premier indice rejoint le carnet de l'expédition Nexus.",
    "Au-delà des pins, l'air se plisse comme si le paysage cachait une couture.");

NEXUS_SCENE_BANK(kFirstContactHelp,
    "Tu choisis de répondre au signal ; Woodsam note l'heure et le motif.",
    "Tu privilégies l'aide sans quitter un lieu sûr ; la fréquence est conservée.",
    "Tu réponds avec prudence, sans prendre le signal pour une preuve.",
    "Ta décision est notée dans le carnet de terrain, avec le relevé original.");

NEXUS_SCENE_BANK(kFirstContactInvestigate,
    "Tu choisis d'examiner le signal ; les trois impulsions sont comparées.",
    "Tu privilégies les mesures et gardes l'enregistrement original intact.",
    "Tu demandes une analyse avant toute conclusion sur l'origine du signal.",
    "Manée compare les trois impulsions, sans prétendre connaître leur origine.");

NEXUS_SCENE_BANK(kFirstContactRetreat,
    "Tu décides de prendre du recul ; LIA archive le signal sans le poursuivre.",
    "Tu refuses de suivre une piste incertaine ; le relevé reste dans l'Atlas.",
    "Tu mets l'appareil en veille ; la découverte est conservée dans le carnet.",
    "Tu choisis la prudence ; rien ne t'oblige à poursuivre cette piste aujourd'hui.");

NEXUS_SCENE_BANK(kSectorDiscovered,
    "Un nouveau secteur de Marcheprime entre dans la carte de l'expédition.",
    "La carte de Marcheprime gagne un secteur encore peu documenté.",
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
    "Les Sentinelles d'Avelune changent leurs signaux pour éviter les patrouilles.",
    "Les réfugiés d'Avelune demandent une preuve que les Seuils peuvent être refermés.",
    "Les fidèles de Varkhël recherchent ceux qui connaissent encore les anciens passages.",
    "Les habitants d'Avelune ne s'accordent pas sur la manière de résister au conquérant.",
    "Une nouvelle consigne circule parmi les opérateurs des relais.");

NEXUS_SCENE_BANK(kDistressCall,
    "Une voix semble traverser le bruit radio, sans être clairement identifiable.",
    "Un fragment ressemble à un appel à l'aide, mais son origine reste inconnue.",
    "La bande contient une syllabe répétée que LIA ne peut pas attribuer.",
    "Une voix inconnue traverse le grésillement ; impossible de dire si elle vient d'Avelune ou du Revers.");

NEXUS_SCENE_BANK(kResonanceWave,
    "Une onde traverse les trois dimensions ; la pierre répond au même rythme.",
    "Les trois mondes semblent vibrer au même instant.",
    "Une onde brève traverse un Seuil encore dormant.",
    "Des signes séparés semblent répondre à un même appel.",
    "La chronologie révèle une concordance entre la Terre, Avelune et le Revers.");

NEXUS_SCENE_BANK(kArchiveRecovered,
    "Une ancienne carte d'Avelune révèle la position d'un Seuil oublié.",
    "Une chronique décrit les gardiens qui protégeaient autrefois les passages.",
    "Une inscription relie le symbole de Craissant à un ancien passage entre les mondes.",
    "Dans les ruines d'Avelune, une ligne semble avoir été gravée après la chute du royaume.",
    "Un ancien relevé refait surface ; le groupe conserve sa date et sa provenance.");

NEXUS_SCENE_BANK(kThresholdManifestation,
    "L'air se plisse et laisse apparaître un Seuil, instable et silencieux.",
    "La pierre gravée chauffe ; une ligne lumineuse dessine un passage dans l'air.",
    "Le paysage se dédouble un instant, révélant une ouverture vers un autre monde.");

NEXUS_SCENE_BANK(kCreatureCrossing,
    "Une forme venue du Revers franchit le Seuil avant qu'il ne se referme.",
    "Une créature inconnue apparaît dans les pins ; elle semble chercher un passage.",
    "Un bruit de griffes résonne derrière la couture lumineuse. Quelque chose a traversé.");

NEXUS_SCENE_BANK(kAveluneDiscovery,
    "Avelune apparaît au-delà du passage : une forêt ancienne couvre les ruines d'un royaume.",
    "Les pierres d'Avelune portent les marques d'une conquête récente.",
    "Une route oubliée traverse les bois d'Avelune, mais ses anciens gardiens ont disparu.");

NEXUS_SCENE_BANK(kReverseInfluence,
    "Le Revers altère les sons ; la voix semble venir de plusieurs directions à la fois.",
    "Une poussière grise traverse le Seuil et fait vaciller les couleurs du paysage.",
    "La lumière se contracte. Le Revers laisse une trace sur la pierre.");

NEXUS_SCENE_BANK(kManeeInterlude,
    "Manée rapproche le symbole d'un récit ancien, mais refuse d'en faire une certitude.",
    "Manée note une ressemblance avec une légende et cherche ce qui ne correspond pas.",
    "Manée suit son intuition : le signe parle d'un passage, pas nécessairement d'une porte.");

NEXUS_SCENE_BANK(kWoodsamInterlude,
    "Woodsam vérifie les issues et compte les ressources avant de proposer un plan.",
    "Woodsam garde le groupe ensemble et repère un abri à proximité.",
    "Woodsam observe la créature sans s'approcher ; il cherche une issue praticable.");

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
    {kThresholdManifestation, sizeof(kThresholdManifestation) / sizeof(kThresholdManifestation[0])},
    {kCreatureCrossing, sizeof(kCreatureCrossing) / sizeof(kCreatureCrossing[0])},
    {kAveluneDiscovery, sizeof(kAveluneDiscovery) / sizeof(kAveluneDiscovery[0])},
    {kReverseInfluence, sizeof(kReverseInfluence) / sizeof(kReverseInfluence[0])},
    {kManeeInterlude, sizeof(kManeeInterlude) / sizeof(kManeeInterlude[0])},
    {kWoodsamInterlude, sizeof(kWoodsamInterlude) / sizeof(kWoodsamInterlude[0])},
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
  value ^= static_cast<uint32_t>(context.companionTrust) << 16U;
  return mix(value);
}

const char* contextLine(const NexusNarrativeContext& context,
                        NarrativeScene scene) {
  if (scene == NarrativeScene::DistressCall) {
    return "Si le danger est réel, contacte les secours par les moyens habituels.";
  }
  if ((context.plotFlags & narrativePlotMask(NarrativePlotFlag::AveluneArchiveFound)) != 0U) {
    return "Les archives d'Avelune offrent une piste supplémentaire à comparer aux indices.";
  }
  if ((context.plotFlags & narrativePlotMask(NarrativePlotFlag::ResonancePatternKnown)) != 0U) {
    return "Le motif est mieux décrit ; son origine reste à établir.";
  }
  if ((context.plotFlags & narrativePlotMask(NarrativePlotFlag::ThreeSectorsMapped)) != 0U) {
    return "Trois secteurs peuvent maintenant être comparés dans l'Atlas.";
  }
  if ((context.plotFlags & (narrativePlotMask(NarrativePlotFlag::CircleContacted) |
                            narrativePlotMask(NarrativePlotFlag::BureauContacted) |
                            narrativePlotMask(NarrativePlotFlag::CollectorsContacted))) != 0U) {
    return "Les témoignages sont conservés séparément des mesures vérifiées.";
  }
  if ((context.plotFlags & narrativePlotMask(NarrativePlotFlag::SignalDecoded)) != 0U) {
    return "Le motif est classé, mais l'identité de son émetteur demeure inconnue.";
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
  if (context.companionTrust <= 25U) {
    return "Manée et Woodsam signalent leurs doutes et gardent cette lecture au rang d'hypothèse.";
  }
  if (context.companionTrust >= 80U) {
    return "Manée propose une piste ; tu restes libre de la vérifier ou non.";
  }
  if (context.evidenceCount > 0U) {
    return "Woodsam conserve la trace pour la comparer aux prochains indices.";
  }
  if ((context.simulatedDay & 1U) == 0U) {
    return "La chronologie est conservée pour les comparaisons futures.";
  }
  return "Cette observation rejoint le journal de l'expédition, sans imposer la suite de l'enquête.";
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
      context.intensity > 100U || context.companionTrust > 100U) return false;

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
