# the-legend-of (Velanthor)

Dark-fantasy choice-based terminal RPG, Python 3 stdlib only. 5 characters, 714 scenes,
81 endings, turn-based combat. Run: `python3 main.py`.

## Constraints

- Story data lives in `data/story.json` ONLY — the per-character `story_*.json` files are
  historical inputs, not loaded by the game.
- NEVER hand-edit these scene fields: `id`, `leads_to`, `effects`, `requires`, `type`,
  `combat`, choice `letter`/`leads_to`/`effects`/`requires`. Prose passes go through
  `scripts/validate_rewrite.py` (checks structure + banned phrases) before merging.
- Kira prose is governed by `docs/story/kira-style-bible.md` + `kira-beat-map.md`. Any new
  Kira content must follow them. Other characters don't have style bibles yet (planned).
- `VELANTHOR_FAST=1` disables combat pacing delays — REQUIRED for tests/scripted runs.
- Theron (6/17) and Vex (3/11) have pre-existing unreachable endings per
  `qa/verify_endings.py` — known issue, don't "fix" as a side effect of other work.
  (`KIRA_CH2_KINGS_ROAD` warning from that script is a script quirk, not a data bug.)
- Combat mechanics vs presentation: presentation lives in `src/combat_text.py` (pure
  functions, tested in `tests/`); the loop in `src/engine.py:combat_encounter`. Enemy
  specials telegraph one turn ahead (`tell` strings in `src/bestiary.py`), stun cancels
  the windup, heals only fire below 50% HP.

## Verification (run all before claiming done)

```bash
VELANTHOR_FAST=1 python3 test_combat_system.py | tail -1
VELANTHOR_FAST=1 python3 -m unittest tests.test_combat_text
python3 scripts/verify_story.py | tail -1
python3 qa/verify_endings.py   # KIRA must stay 24/24 reachable
```

## Working notes

- **NEXT SESSION START HERE:** `docs/superpowers/plans/2026-07-08-v3-character-expansion.md`
  — full-cast prose deepening + reachability repair + gameplay level-ups. Phase 0
  (ending reachability tracer/fixes) comes before any prose work. One character per
  session, ask user before each phase (~1M tokens/character, measured).
- v2.2 (2026-07-08): Kira deepened end-to-end, combat presentation overhaul.
  Spec: `docs/superpowers/specs/2026-07-07-kira-deepening-combat-feel-design.md`.
- Root `test_*`/`kira_*`/`find_*` scripts are gitignored dev litter from past sessions.
