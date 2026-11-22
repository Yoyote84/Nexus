#!/usr/bin/env bash
# Tests natifs du moteur Hawkins, sans matériel ESP32.
set -euo pipefail
cd "$(dirname "$0")"
if [ -z "${CXX:-}" ]; then CXX=g++; fi
SANFLAGS=""
if [ "${SAN:-0}" = "1" ]; then
  SANFLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer"
fi
"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator \
  main.cpp ../../src/core/hawkins_world.cpp ../../src/storage/hawkins_save_codec.cpp \
  ../../src/exploration/hawkins_exploration.cpp ../../src/core/hawkins_character.cpp \
  -o /tmp/roza-hawkinstest
/tmp/roza-hawkinstest
"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator missions_test.cpp ../../src/core/hawkins_missions.cpp \
  -o /tmp/roza-hawkins-missions-test
/tmp/roza-hawkins-missions-test
"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator adventure_test.cpp ../../src/core/hawkins_adventure.cpp \
  ../../src/core/hawkins_character.cpp ../../src/core/hawkins_missions.cpp \
  -o /tmp/roza-hawkins-adventure-test
/tmp/roza-hawkins-adventure-test
"$CXX" -std=c++17 -Wall -Wextra -Werror $SANFLAGS \
  -I ../../src -I ../../src/core -I ../../src/exploration -I ../../src/storage -I ../../src/narrator narrative_memory_test.cpp \
  ../../src/narrator/hawkins_narrative_memory.cpp \
  ../../src/narrator/hawkins_narrative_memory_codec.cpp \
  -o /tmp/roza-hawkins-narrative-test
/tmp/roza-hawkins-narrative-test
