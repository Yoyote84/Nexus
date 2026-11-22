# Nexus migration status

## Five-stage plan

- [x] 1/5 — audit scope and dependencies.
- [x] 2/5 — extract the game source, tests, tools, documentation and local model assets into this repository.
- [ ] 3/5 — replace legacy names and protected narrative elements with an original setting and identity.
- [ ] 4/5 — separate platform interfaces, connect the ROZA Cardputer adapter and establish CI/build integration.
- [ ] 5/5 — produce the installable firmware and complete physical Cardputer ADV tests with the user.

## Extraction boundary

The deterministic game state, missions, character, world, exploration logic, narrative protocol/memory, save codecs, local narrator engine, model assets, test harnesses and model tools are now in Nexus. The former app controller is retained under `src/platform/cardputer/legacy/` for refactoring. ROZA's shared display, keyboard, SD, GNSS, LoRa, Wi-Fi and Bluetooth drivers remain in the ROZA repository.

This snapshot is not yet a standalone firmware build: the host controller and storage/NVS integration still reference ROZA/ESP32 services. Those boundaries are the subject of Step 4. No source file was deleted from ROZA during extraction.
