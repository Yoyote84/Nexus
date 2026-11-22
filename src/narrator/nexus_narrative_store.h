#pragma once
#include "nexus_narrative_memory.h"
#include <stdint.h>

namespace nexus {
enum class NarrativeSaveLoadStatus : uint8_t {
  Loaded, Empty, Corrupt, StorageError
};
NarrativeSaveLoadStatus narrativeSaveLoad(NarrativeMemory& memory,
                                          uint32_t* sequence = nullptr);
bool narrativeSaveCommit(const NarrativeMemory& memory,
                         uint32_t* sequence = nullptr);
}
