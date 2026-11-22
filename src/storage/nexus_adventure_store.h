#pragma once
#include "nexus_adventure.h"
#include <stdint.h>

namespace nexus {

enum class AdventureSaveLoadStatus : uint8_t { Loaded, Empty, Corrupt, StorageError };
AdventureSaveLoadStatus adventureSaveLoad(AdventureState& state, uint32_t* sequence = nullptr);
bool adventureSaveCommit(const AdventureState& state, uint32_t* sequence = nullptr);

}  // namespace nexus
