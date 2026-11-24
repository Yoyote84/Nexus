#include "nexus_narrative_engine.h"
#include "nexus_lore_guard.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

using namespace nexus;

static NexusNarrativeContext sampleContext() {
  NexusNarrativeContext context{};
  context.worldSeed = 0x12345678U;
  context.eventSequence = 17U;
  context.simulatedDay = 9U;
  context.sectorKey = 0xA51C27U;
  context.intensity = 42U;
  context.evidenceCount = 1U;
  context.liaTrust = 60U;
  return context;
}

static void testEverySceneProducesCompleteFrenchText() {
  NexusNarrativeContext context = sampleContext();
  for (uint8_t index = 0U;
       index < static_cast<uint8_t>(NarrativeScene::Count); ++index) {
    context.scene = static_cast<NarrativeScene>(index);
    char text[kNexusNarrativeTextCapacity + 1U] = {};
    assert(buildNexusNarrative(context, text, sizeof(text)));
    assert(isNexusNarrativeComplete(text));
    assert(strlen(text) <= kNexusNarrativeTextCapacity);
    assert(strstr(text, ". ") != nullptr);
    assert(!containsLegacyFictionReference(text));
  }
}

static void testDeterminismAndVariation() {
  NexusNarrativeContext context = sampleContext();
  context.scene = NarrativeScene::StrangeSignal;
  char first[kNexusNarrativeTextCapacity + 1U] = {};
  char second[kNexusNarrativeTextCapacity + 1U] = {};
  assert(buildNexusNarrative(context, first, sizeof(first)));
  assert(buildNexusNarrative(context, second, sizeof(second)));
  assert(strcmp(first, second) == 0);

  char variants[24][kNexusNarrativeTextCapacity + 1U] = {};
  size_t unique = 0U;
  for (uint32_t sequence = 0U; sequence < 24U; ++sequence) {
    context.eventSequence = sequence;
    char candidate[kNexusNarrativeTextCapacity + 1U] = {};
    assert(buildNexusNarrative(context, candidate, sizeof(candidate)));
    bool found = false;
    for (size_t i = 0U; i < unique; ++i) {
      if (strcmp(variants[i], candidate) == 0) found = true;
    }
    if (!found) {
      assert(unique < 24U);
      strcpy(variants[unique++], candidate);
    }
  }
  assert(unique >= 4U);
}

static void testNarrativeReactsToEvidenceAndTrust() {
  NexusNarrativeContext context = sampleContext();
  context.scene = NarrativeScene::ResidualTrace;
  context.evidenceCount = 0U;
  context.liaTrust = 20U;
  char cautious[kNexusNarrativeTextCapacity + 1U] = {};
  assert(buildNexusNarrative(context, cautious, sizeof(cautious)));
  assert(strstr(cautious, "hypothèse") != nullptr);

  context.evidenceCount = 9U;
  context.liaTrust = 90U;
  char corroborated[kNexusNarrativeTextCapacity + 1U] = {};
  assert(buildNexusNarrative(context, corroborated, sizeof(corroborated)));
  assert(strstr(corroborated, "concordent") != nullptr);
  assert(strcmp(cautious, corroborated) != 0);
}

static void testPersistentPlotFlagsChangeNarrative() {
  NexusNarrativeContext context = sampleContext();
  context.scene = NarrativeScene::ResidualTrace;
  context.plotFlags = 0U;
  context.evidenceCount = 1U;
  context.liaTrust = 60U;
  char baseline[kNexusNarrativeTextCapacity + 1U] = {};
  assert(buildNexusNarrative(context, baseline, sizeof(baseline)));

  context.plotFlags = narrativePlotMask(NarrativePlotFlag::AlmaArchiveFound);
  char archive[kNexusNarrativeTextCapacity + 1U] = {};
  assert(buildNexusNarrative(context, archive, sizeof(archive)));
  assert(strstr(archive, "Alma") != nullptr);
  assert(strcmp(baseline, archive) != 0);

  context.plotFlags = narrativePlotMask(NarrativePlotFlag::ResonancePatternKnown);
  char pattern[kNexusNarrativeTextCapacity + 1U] = {};
  assert(buildNexusNarrative(context, pattern, sizeof(pattern)));
  assert(strstr(pattern, "motif") != nullptr);
  assert(strcmp(archive, pattern) != 0);

  context.plotFlags = narrativePlotMask(NarrativePlotFlag::ThreeSectorsMapped);
  char map[kNexusNarrativeTextCapacity + 1U] = {};
  assert(buildNexusNarrative(context, map, sizeof(map)));
  assert(strstr(map, "Trois secteurs") != nullptr);

  assert(narrativePlotMask(NarrativePlotFlag::FirstSignalResolved) == 0x01U);
  assert(narrativePlotMask(NarrativePlotFlag::SignalDecoded) == 0x02U);
  assert(narrativePlotMask(NarrativePlotFlag::ThreeSectorsMapped) == 0x04U);
  assert(narrativePlotMask(NarrativePlotFlag::AlmaArchiveFound) == 0x08U);
  assert(narrativePlotMask(NarrativePlotFlag::CircleContacted) == 0x10U);
  assert(narrativePlotMask(NarrativePlotFlag::BureauContacted) == 0x20U);
  assert(narrativePlotMask(NarrativePlotFlag::CollectorsContacted) == 0x40U);
  assert(narrativePlotMask(NarrativePlotFlag::ResonancePatternKnown) == 0x80U);
}

static void testEventAndChoiceRouting() {
  assert(narrativeSceneForEvent(EventType::StrangeSignal) == NarrativeScene::StrangeSignal);
  assert(narrativeSceneForEvent(EventType::PowerAnomaly) == NarrativeScene::PowerAnomaly);
  assert(narrativeSceneForEvent(EventType::ResidualTrace) == NarrativeScene::ResidualTrace);
  assert(narrativeSceneForEvent(EventType::FactionMovement) == NarrativeScene::FactionMovement);
  assert(narrativeSceneForEvent(EventType::DistressCall) == NarrativeScene::DistressCall);
  assert(narrativeSceneForEvent(EventType::ResonanceWave) == NarrativeScene::ResonanceWave);
  assert(narrativeSceneForEvent(EventType::None) == NarrativeScene::QuietObservation);

  NarrativeScene scene = NarrativeScene::QuietObservation;
  assert(narrativeSceneForFirstContactChoice(FirstContactChoice::Help, scene));
  assert(scene == NarrativeScene::FirstContactHelp);
  assert(narrativeSceneForFirstContactChoice(FirstContactChoice::Investigate, scene));
  assert(scene == NarrativeScene::FirstContactInvestigate);
  assert(narrativeSceneForFirstContactChoice(FirstContactChoice::Retreat, scene));
  assert(scene == NarrativeScene::FirstContactRetreat);
  assert(!narrativeSceneForFirstContactChoice(static_cast<FirstContactChoice>(255U), scene));
}

static void testSafetyAndInvalidInput() {
  NexusNarrativeContext context = sampleContext();
  context.scene = NarrativeScene::DistressCall;
  char text[kNexusNarrativeTextCapacity + 1U] = {};
  assert(buildNexusNarrative(context, text, sizeof(text)));
  assert(strstr(text, "secours") != nullptr);

  char tiny[8] = "x";
  assert(!buildNexusNarrative(context, tiny, sizeof(tiny)));
  assert(tiny[0] == '\0');

  context.intensity = 101U;
  assert(!buildNexusNarrative(context, text, sizeof(text)));
  assert(text[0] == '\0');

  context.intensity = 20U;
  context.scene = static_cast<NarrativeScene>(255U);
  assert(!buildNexusNarrative(context, text, sizeof(text)));
  assert(text[0] == '\0');

  assert(!isNexusNarrativeComplete(nullptr));
  assert(!isNexusNarrativeComplete(""));
  assert(!isNexusNarrativeComplete("Une phrase sans ponctuation"));
  assert(!isNexusNarrativeComplete("Hawkins n'appartient pas à Nexus."));
}

int main() {
  testEverySceneProducesCompleteFrenchText();
  testDeterminismAndVariation();
  testNarrativeReactsToEvidenceAndTrust();
  testPersistentPlotFlagsChangeNarrative();
  testEventAndChoiceRouting();
  testSafetyAndInvalidInput();
  puts("NEXUS: moteur narratif hors ligne, variantes, cohérence et garde-fous valides.");
  return 0;
}
