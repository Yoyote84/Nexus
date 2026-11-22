#pragma once
#include "nexus_world.h"
#include <stdint.h>
namespace nexus {
enum class RuntimeStatus:uint8_t{Empty,Ready,WaitingForClock,ClockBeforeWorld,SaveError,CorruptSave,StorageError};
void nexusRuntimeInit();
bool nexusRuntimeUpdate();
bool nexusRuntimeSaveNow();
// Progression narrative locale : une journée de jeu par secteur inédit.
bool nexusRuntimeAdvanceDays(uint32_t days);
const WorldState* nexusRuntimeWorld();
RuntimeStatus nexusRuntimeStatus();
const char* nexusRuntimeStatusText();
}
