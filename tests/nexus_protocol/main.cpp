#include "nexus_ai_protocol.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

using nexus::NexusAiMessage;
using nexus::NexusAiMessageKind;

static void testRequestBuildsBoundedEnvelope() {
  char line[1024];
  assert(nexus::buildNexusAiRequestLine(
      42U, "{\"player\":{\"name\":\"ELEVEN\"},\"day\":3}", line, sizeof(line)));
  assert(strncmp(line, "NEX/1 ", 6U) == 0);
  assert(strstr(line, "\"type\":\"narrate\"") != nullptr);
  assert(strstr(line, "\"id\":42") != nullptr);
  assert(strstr(line, "\"player\":{\"name\":\"ELEVEN\"}") != nullptr);
  assert(line[strlen(line) - 1U] == '\n');
}

static void testRequestRejectsInvalidInputAndOverflow() {
  char small[24];
  assert(!nexus::buildNexusAiRequestLine(0U, "{}", small, sizeof(small)));
  assert(!nexus::buildNexusAiRequestLine(1U, "[]", small, sizeof(small)));
  assert(!nexus::buildNexusAiRequestLine(1U, "{", small, sizeof(small)));
  char large[256];
  assert(!nexus::buildNexusAiRequestLine(
      1U, "{\"very_long\":\"abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz\"}",
      large, 24U));
}

static void testHelloHeartbeat() {
  const char line[] = "NEX/1 {\"type\":\"hello\",\"version\":1}";
  NexusAiMessage message{};
  assert(nexus::parseNexusAiMessage(line, sizeof(line) - 1U, message));
  assert(message.kind == NexusAiMessageKind::Hello);
  assert(message.requestId == 0U && message.text[0] == '\0');
}

static void testNarration() {
  const char line[] =
      "NEX/1 {\"type\":\"narration\",\"id\":7,\"text\":\"La lumiere vacille.\",\"choices\":[\"Repondre\",\"Se cacher\"]}";
  NexusAiMessage message{};
  assert(nexus::parseNexusAiMessage(line, sizeof(line) - 1U, message));
  assert(message.kind == NexusAiMessageKind::Narration);
  assert(message.requestId == 7U);
  assert(message.choiceCount == 2U);
  assert(strcmp(message.choices[0], "Repondre") == 0);
  assert(strcmp(message.choices[1], "Se cacher") == 0);
  assert(strcmp(message.text, "La lumiere vacille.") == 0);
}

static void testNarrationAcceptsFrenchUtf8() {
  const char line[] =
      "NEX/1 {\"type\":\"narration\",\"id\":1,\"text\":\"La lumiere vacille dans le couloir. Quelqu\u0027un frappe a la porte.\",\"choices\":[\"Repondre a la radio\",\"Se cacher\",\"Aller voir\"]}";
  NexusAiMessage message{};
  assert(nexus::parseNexusAiMessage(line, sizeof(line) - 1U, message));
  assert(message.kind == NexusAiMessageKind::Narration);
  assert(message.requestId == 1U);
  assert(message.choiceCount == 3U);
  assert(strcmp(message.text, "La lumiere vacille dans le couloir. Quelqu'un frappe a la porte.") == 0);
}

static void testParserHandlesNonNullTerminatedCdcBuffer() {
  const char json[] =
      "NEX/1 {\"type\":\"narration\",\"id\":11,\"text\":\"Il dit \\\"bonjour\\\".\\\\\",\"choices\":[\"Ecouter\",\"Partir\"]}";
  const size_t exactLength = sizeof(json) - 1U;
  char cdcBuffer[sizeof(json) + 8U];
  memset(cdcBuffer, 0x5A, sizeof(cdcBuffer));
  memcpy(cdcBuffer, json, exactLength);
  NexusAiMessage message{};
  const char* errorCode = nullptr;
  assert(nexus::parseNexusAiMessage(cdcBuffer, exactLength, message, &errorCode));
  assert(strcmp(errorCode, "ok") == 0);
  assert(message.requestId == 11U);
  assert(strcmp(message.text, "Il dit \"bonjour\".\\") == 0);
  assert(message.choiceCount == 2U);
}

static void testParserTrimsCdcLineEnding() {
  const char json[] =
      "NEX/1 {\"type\":\"narration\",\"id\":12,\"text\":\"La radio grésille.\",\"choices\":[\"Répondre\"]}";
  char line[sizeof(json) + 2U];
  const size_t jsonLength = sizeof(json) - 1U;
  memcpy(line, json, jsonLength);
  line[jsonLength] = '\r';
  line[jsonLength + 1U] = '\n';
  NexusAiMessage message{};
  const char* errorCode = nullptr;
  assert(nexus::parseNexusAiMessage(
      line, jsonLength + 2U, message, &errorCode));
  assert(strcmp(errorCode, "ok") == 0);
  assert(message.requestId == 12U);
  assert(strcmp(message.choices[0], "Répondre") == 0);
}

static void testNarrationNormalizesControlCharacters() {
  const char line[] =
      "NEX/1 {\"type\":\"narration\",\"id\":9,\"text\":\"Ligne 1\\rLigne 2\",\"choices\":[\"A\\u0001B\"]}";
  NexusAiMessage message{};
  const char* errorCode = nullptr;
  assert(nexus::parseNexusAiMessage(
      line, sizeof(line) - 1U, message, &errorCode));
  assert(strcmp(errorCode, "ok") == 0);
  assert(strcmp(message.text, "Ligne 1 Ligne 2") == 0);
  assert(strcmp(message.choices[0], "A B") == 0);
}

static void testNarrationExposesPreciseParseFailure() {
  const char line[] =
      "NEX/1 {\"type\":\"narration\",\"id\":9,\"text\":\"Bonjour\"}";
  NexusAiMessage message{};
  const char* errorCode = nullptr;
  assert(!nexus::parseNexusAiMessage(
      line, sizeof(line) - 1U, message, &errorCode));
  assert(strcmp(errorCode, "choices_missing_or_not_array") == 0);
}

static void testInvalidAndUnknownMessages() {
  NexusAiMessage message{};
  const char noPrefix[] = "{\"type\":\"hello\",\"version\":1}";
  assert(!nexus::parseNexusAiMessage(noPrefix, sizeof(noPrefix) - 1U, message));
  const char wrongVersion[] = "NEX/1 {\"type\":\"hello\",\"version\":2}";
  assert(!nexus::parseNexusAiMessage(wrongVersion, sizeof(wrongVersion) - 1U, message));
  const char noId[] = "NEX/1 {\"type\":\"narration\",\"text\":\"Salut\"}";
  assert(!nexus::parseNexusAiMessage(noId, sizeof(noId) - 1U, message));
  const char unknown[] = "NEX/1 {\"type\":\"inventory_change\",\"id\":1}";
  assert(!nexus::parseNexusAiMessage(unknown, sizeof(unknown) - 1U, message));
  const char malformed[] = "NEX/1 {\"type\":";
  assert(!nexus::parseNexusAiMessage(malformed, sizeof(malformed) - 1U, message));
}

static void testRejectsEmptyAndOversizedNarration() {
  NexusAiMessage message{};
  const char empty[] = "NEX/1 {\"type\":\"narration\",\"id\":3,\"text\":\"\"}";
  assert(!nexus::parseNexusAiMessage(empty, sizeof(empty) - 1U, message));

  char line[700];
  size_t offset = static_cast<size_t>(
      snprintf(line, sizeof(line), "NEX/1 {\"type\":\"narration\",\"id\":3,\"text\":\""));
  for (unsigned i = 0U; i < 500U; ++i) line[offset++] = 'x';
  line[offset++] = '"';
  line[offset++] = '}';
  assert(!nexus::parseNexusAiMessage(line, offset, message));
}

static void testRejectsControlCharacters() {
  const char line[] =
      "NEX/1 {\"type\":\"narration\",\"id\":2,\"text\":\"ok\\u0001no\"}";
  NexusAiMessage message{};
  assert(!nexus::parseNexusAiMessage(line, sizeof(line) - 1U, message));
}

int main() {
  testRequestBuildsBoundedEnvelope();
  testRequestRejectsInvalidInputAndOverflow();
  testHelloHeartbeat();
  testNarration();
  testNarrationAcceptsFrenchUtf8();
  testParserHandlesNonNullTerminatedCdcBuffer();
  testParserTrimsCdcLineEnding();
  testNarrationNormalizesControlCharacters();
  testNarrationExposesPreciseParseFailure();
  testInvalidAndUnknownMessages();
  testRejectsEmptyAndOversizedNarration();
  testRejectsControlCharacters();
  puts("NEXUS AI USB: toutes les validations du protocole ont reussi.");
  return 0;
}
