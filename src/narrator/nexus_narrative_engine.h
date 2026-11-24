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

// Instantané en lecture seule : le narrateur ne reçoit aucun pointeur vers
// les structures mutables du monde, de l'inventaire ou des sauvegardes.
struct NexusNarrativeContext {
  uint32_t worldSeed;
  uint32_t eventSequence;
  uint32_t simulatedDay;
  uint32_t sectorKey;
  uint8_t intensity;
  uint8_t evidenceCount;
  uint8_t liaTrust;
};

NarrativeScene narrativeSceneForEvent(EventType event);
bool narrativeSceneForFirstContactChoice(FirstContactChoice choice,
                                         NarrativeScene& scene);

bool buildNexusNarrative(const NexusNarrativeContext& context,
                         char* output, size_t outputCapacity);
bool isNexusNarrativeComplete(const char* text);

}  // namespace nexus
