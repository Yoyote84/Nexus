# Nexus

Nexus is the standalone repository for the offline-first exploration RPG extracted from the ROZA firmware project.

The extraction is being performed in stages. This initial repository keeps the original game implementation intact while separating game logic, exploration, local narration, persistence, tests and documentation from the ROZA hardware drivers.

## Target hardware

- M5Stack Cardputer ADV
- Optional Cap LoRa-1262 GNSS module
- microSD storage for persistent saves and game assets

The game is designed to run offline on the Cardputer. A phone or network connection is not required during gameplay.

## Migration status

- [x] Step 1 — audit and extraction scope
- [ ] Step 2 — extract source into this repository
- [ ] Step 3 — create an original setting, naming and narrative assets
- [ ] Step 4 — integrate and validate the ROZA firmware adapter
- [ ] Step 5 — final firmware package and physical device testing

## Important

This is an extraction snapshot, not yet the final renamed game. Original narrative identifiers and assets are retained only as migration input and will be reviewed in Step 3. The ROZA repository remains the firmware host; its hardware drivers are not duplicated here.

See `docs/MIGRATION_STATUS.md` for the current boundary and verification notes.
