#include "nexus_lore_guard.h"
namespace nexus {
namespace {
char lowerAscii(char c) { return c >= 'A' && c <= 'Z' ? static_cast<char>(c + 32) : c; }
bool has(const char* text, const char* phrase) {
  if (!text || !phrase || !*phrase) return false;
  for (const char* p = text; *p; ++p) {
    const char* a = p;
    const char* b = phrase;
    while (*a && *b && lowerAscii(*a) == lowerAscii(*b)) { ++a; ++b; }
    if (!*b) return true;
  }
  return false;
}
}
bool containsLegacyFictionReference(const char* text) {
  static const char* const terms[] = {
    "hawkins", "stranger things", "upside down", "demogorgon",
    "mind flayer", "vecna", "brenner", "starcourt", "hellfire club",
    "demodog", "demobat", "will byers", "dustin", "mike wheeler",
    "lucas sinclair", "jim hopper", "joyce byers", "steve harrington",
    "robin buckley", "nancy wheeler", "max mayfield", "eleven"
  };
  for (const char* term : terms) if (has(text, term)) return true;
  return false;
}
}
