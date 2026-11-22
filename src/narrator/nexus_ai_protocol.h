#pragma once

#include <stddef.h>
#include <stdint.h>

namespace nexus {

constexpr size_t kNexusAiMaxLine = 1792U;
constexpr size_t kNexusAiTextCapacity = 210U;
constexpr size_t kNexusAiChoiceCount = 3U;
constexpr size_t kNexusAiChoiceCapacity = 34U;
constexpr size_t kNexusAiErrorCapacity = 160U;

enum class NexusAiMessageKind : uint8_t { Invalid = 0, Hello, Narration, Error };

struct NexusAiMessage {
  NexusAiMessageKind kind;
  uint32_t requestId;
  char text[kNexusAiTextCapacity + 1U];
  uint8_t choiceCount;
  char choices[kNexusAiChoiceCount][kNexusAiChoiceCapacity + 1U];
};

bool buildNexusAiRequestLine(uint32_t requestId, const char* contextJson,
                               char* output, size_t capacity);
bool parseNexusAiMessage(const char* line, size_t length,
                           NexusAiMessage& output,
                           const char** errorCode = nullptr);

}  // namespace nexus
