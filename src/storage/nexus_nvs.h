#pragma once

#include "nexus_world.h"
#include "nexus_exploration.h"
#include "nexus_character.h"
#include "nexus_missions.h"
#include <stdint.h>

namespace nexus {

enum class WorldSaveLoadStatus : uint8_t { Loaded, Empty, Corrupt, StorageError };
enum class ExplorationSaveLoadStatus : uint8_t { Loaded, Empty, Corrupt, StorageError };
enum class CharacterSaveLoadStatus : uint8_t { Loaded, Empty, Corrupt, StorageError };
enum class MissionSaveLoadStatus : uint8_t { Loaded, Empty, Corrupt, StorageError };

WorldSaveLoadStatus worldSaveLoad(WorldState& world, uint32_t* sequence = nullptr);
bool worldSaveCommit(const WorldState& world, uint32_t* sequence = nullptr);

ExplorationSaveLoadStatus explorationSaveLoad(ExplorationState& state,
                                               uint32_t* sequence = nullptr);
bool explorationSaveCommit(const ExplorationState& state,
                           uint32_t* sequence = nullptr);

CharacterSaveLoadStatus characterSaveLoad(CharacterState& character,
                                           uint32_t* sequence = nullptr);
bool characterSaveCommit(const CharacterState& character,
                         uint32_t* sequence = nullptr);

MissionSaveLoadStatus missionSaveLoad(MissionState& state,
                                      uint32_t* sequence = nullptr);
bool missionSaveCommit(const MissionState& state,
                       uint32_t* sequence = nullptr);

}  // namespace nexus
