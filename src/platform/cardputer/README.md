# Cardputer host boundary

`legacy/` contains the extracted ROZA game screen/controller as a migration reference. It still includes ROZA-owned headers and globals (UI, SD and GNSS) and is not an independent build target yet. Step 4 will replace these direct dependencies with explicit Nexus platform interfaces and a thin ROZA adapter. Do not copy the ROZA display, keyboard, SD, GNSS or LoRa drivers into this repository.
