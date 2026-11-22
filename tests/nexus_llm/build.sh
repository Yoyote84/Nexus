#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
CXX_BIN="${CXX:-g++}"
ENGINE_DIR="../../src/narrator/local_llm"
test -f "$ENGINE_DIR/port.h" || { echo "LLM source folder missing: $ENGINE_DIR" >&2; exit 1; }
test -f "$ENGINE_DIR/llm.cpp" || { echo "LLM engine missing: $ENGINE_DIR/llm.cpp" >&2; exit 1; }
"$CXX_BIN" -std=c++17 -O2 -Wall -Wextra -pthread \
  -DLLM_FORCE_SCALAR \
  -I host -I "$ENGINE_DIR" \
  main.cpp "$ENGINE_DIR/llm.cpp" "$ENGINE_DIR/port.cpp" \
  -o /tmp/nexus-local-llm-test
/tmp/nexus-local-llm-test
