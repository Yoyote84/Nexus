#pragma once

#include "nexus_adventure.h"
#include "nexus_world.h"

#include <stddef.h>
#include <stdint.h>

namespace nexus {

constexpr size_t kNexusNarrativeTextCapacity = 210U;

enum class NarrativeScene : uint8_t {
  Opening = 0,
  FirstContactHelp,
  FirstContactInvestigate,
  FirstContactRetreat,
  SectorDiscovered,
  StrangeSignal,
  PowerAnomaly,
  ResidualTrace,
  FactionMovement,
  DistressCall,
  ResonanceWave,
  ArchiveRecovered,
  MissionCompleted,
  QuietObservation,
  Count
};

// Ces bits correspondent directement aux huit emplacements persistants de
// NarrativeMemory::plotFlags. Ils donnent au récit des jalons durables.
enum class NarrativePlotFlag : uint8_t {
  FirstSignalResolved = 0,
  SignalDecoded,
  ThreeSectorsMapped,
  AlmaArchiveFound,
  CircleContacted,
  BureauContacted,
  CollectorsContacted,
  ResonancePatternKnown
};

constexpr uint8_t narrativePlotMask(NarrativePlotFlag flag) {
  const uint8_t index = static_cast<uint8_t>(flag);
  return index < 8U ? static_cast<uint8_t>(1U << index) : 0U;
}

// Instantané en lecture seule : le narrateur ne reçoit aucun pointeur vers
// les structures mutables du monde, de l'inventaire ou des sauvegardes.
struct NexusNarrativeContext {
  NarrativeScene scene;
  uint32_t worldSeed;
  uint32_t eventSequence;
  uint32_t simulatedDay;
  uint32_t sectorKey;
  uint8_t intensity;
  uint8_t evidenceCount;
  uint8_t plotFlags;
  uint8_t liaTrust;
};

NarrativeScene narrativeSceneForEvent(EventType event);
bool narrativeSceneForFirstContactChoice(FirstContactChoice choice,
                                         NarrativeScene& scene);

bool buildNexusNarrative(const NexusNarrativeContext& context,
                         char* output, size_t outputCapacity);
bool isNexusNarrativeComplete(const char* text);

}  // namespace nexus
