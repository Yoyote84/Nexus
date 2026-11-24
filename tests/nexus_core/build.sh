#!/usr/bin/env bash
# Tests natifs du moteur Nexus, sans matériel ESP32.
set -euo pipefail
cd "$(dirname "$0")"
if ! declare -p CXX >/dev/null 2>&1; then CXX=g++; elif [ -z "$CXX" ]; then CXX=g++; fi
if ! declare -p SAN >/dev/null 2>&1; then SAN=0; fi
SANFLAGS=""
if [ "$SAN" = "1" ]; then
  SANFLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"
fi
"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator \
  main.cpp ../../src/core/nexus_world.cpp ../../src/storage/nexus_save_codec.cpp \
  ../../src/exploration/nexus_exploration.cpp ../../src/core/nexus_character.cpp \
  -o /tmp/roza-nexustest
/tmp/roza-nexustest
"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator missions_test.cpp ../../src/core/nexus_missions.cpp \
  -o /tmp/roza-nexus-missions-test
/tmp/roza-nexus-missions-test
"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator adventure_test.cpp ../../src/core/nexus_adventure.cpp \
  ../../src/core/nexus_character.cpp ../../src/core/nexus_missions.cpp \
  -o /tmp/roza-nexus-adventure-test
/tmp/roza-nexus-adventure-test
"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator narrative_memory_test.cpp \
  ../../src/narrator/nexus_narrative_memory.cpp \
  ../../src/narrator/nexus_narrative_memory_codec.cpp \
  -o /tmp/roza-nexus-narrative-test
/tmp/roza-nexus-narrative-test

"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator \
  narrative_engine_test.cpp ../../src/narrator/nexus_narrative_engine.cpp \
  ../../src/narrator/nexus_lore_guard.cpp -o /tmp/nexus-narrative-engine-test
/tmp/nexus-narrative-engine-test

"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src/narrator lore_guard_test.cpp ../../src/narrator/nexus_lore_guard.cpp \
  -o /tmp/nexus-lore-guard-test
/tmp/nexus-lore-guard-test
