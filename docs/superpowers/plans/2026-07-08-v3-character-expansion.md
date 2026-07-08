# Velanthor v3 — Full-Cast Deepening + Level-Up Plan

> **For agentic workers:** Execute with superpowers:executing-plans (inline engine/script work)
> + one Sonnet subagent at a time for prose batches (NEVER parallel — RAM rule). This plan was
> written at the end of the v2.2 session that built the pipeline it reuses; trust the measured
> numbers. Report to the user between phases.

**Goal:** Bring Theron, Vex, Elara, and Asha to Kira's v2.2 prose standard, repair the broken
ending reachability, and ship cross-cutting gameplay level-ups.

**State when written (v2.2, 2026-07-08):** Kira done end-to-end (style bible + beat map +
5 validated batches, median scene 248→682 chars, 24/24 endings reachable). Combat presentation
overhauled (telegraphed specials, contextual damage, HP bars). Pipeline proven:
`scripts/validate_rewrite.py` guards structure; `docs/story/kira-*.md` are the template docs.

**Measured costs from the Kira run (budget accordingly, get user approval per phase):**
- Beat map subagent: ~120k tokens. Prose batch subagent (28 scenes): ~150k tokens.
- One character ≈ style bible (inline, cheap) + beat map + 5-6 batches ≈ **900k-1M tokens**.
- All four characters ≈ 3.5-4M tokens total. DO NOT run in one session. One character per
  session is the right unit; ask the user before starting each.

## The per-character numbers (from data/story.json, v2.2)

| Character | Scenes | Median desc | Reachable endings (qa) | Priority driver |
|---|---|---|---|---|
| Vex | 151 | 118 chars | 3/11 ⚠ | Thinnest prose + most broken endings |
| Asha | 157 | 121 chars | 17/17 | Thinnest prose, newest content |
| Elara | 115 | 189 chars | 16/17 | Smallest, quick win |
| Theron | 152 | 392 chars | 6/17 ⚠ | Best prose already, worst reachability |

## Phase 0 — Ending reachability repair (do FIRST, before any prose)

Theron 11/17 and Vex 8/11 endings unreachable per `qa/verify_endings.py`. Diagnosis done in
v2.2 session: every `*_ENDING*` scene IS referenced by at least one choice/leads_to edge, so
the breakage is upstream — either `requires` gates that can never be satisfied on any path,
or the referencing scenes are themselves unreachable.

1. Write `scripts/trace_reachability.py`: BFS from each character's start scene that tracks
   accumulated stats/items/flags along paths (model `effects` as grants, `requires` as gates).
   For each unreachable ending, print the LAST reachable scene on its path and the exact gate
   that fails. (Existing `qa/verify_endings.py` ignores requires — that's why it undercounts;
   confirm its numbers first.)
2. Fix minimally: adjust `requires` thresholds or add a missing `effects` grant on an earlier
   choice — never delete scenes, never add scenes in this phase. Every fix re-verified with
   the tracer + `scripts/verify_story.py`.
3. Target: Theron 17/17, Vex 11/11, Elara 17/17. Commit per character fixed.

⚠ `qa/verify_endings.py` has a quirk: warns about `KIRA_CH2_KINGS_ROAD` which never existed —
script-side phantom, ignore it.

## Phases 1-4 — Prose deepening, one character per session

**Order: Vex → Asha → Elara → Theron** (worst prose first; Theron last because his 392-char
median means the smallest delta).

Per character, replicate the Kira pipeline exactly:

1. **Style bible** (`docs/story/<name>-style-bible.md`, written inline, ~1 page). Use
   `kira-style-bible.md` as the structural template: Voice / Imagery bank / Bans (copy the
   hard bans verbatim — they're validator-enforced) / Scene targets (same: 400-700 normal,
   700-1100 climax, 600-1000 endings) / Every-scene-must-have / Never-touch.
   Voice starting points (from the existing text — sharpen during CH1 read):
   - **Vex (Shadow, thief):** transactional, fast, streetwise. Counts coin and exits. Sister
     Nyra is her one non-negotiable. Underworld texture: rope tar, dock rot, coin grease.
     Humor sharper than Kira's, guilt buried deeper.
   - **Asha (Warden, druid):** patient, rooted, seasonal. Thinks in weather and growth cycles.
     The border is a body she tends. Nature magic costs should be somatic (sap-slow blood,
     bark-stiff joints) to mirror Kira's frost.
   - **Elara (Merchant heiress):** ledger-minded vengeance. Prices everything, including
     people, including herself. Silk-and-steel register; grief expressed as audit.
   - **Theron (Fallen knight):** liturgical cadence, shame-forward. Armor as penance.
     The void he carries should echo Kira's (shared mythology) but he experiences it as
     weight/rust, not cold/hunger.
2. **Beat map** (ONE Sonnet subagent): same prompt contract as Kira's — arc overview,
   chapter beats with climax scene IDs, ending families with emotional truths, payoff
   threads (3-5, with seed/payoff scene IDs), weak choice text list (≤15). Verify every
   cited scene ID exists before committing (`grep`-check against story.json).
3. **Batches** (ONE Sonnet subagent each, sequential): slice sorted scene keys into ~28-scene
   batches. Prompt contract per batch (copy from the Kira run — it worked):
   read style bible + beat map + slice → rewrite `description` only (+ flagged weak choice
   `text`) → keep ALL plot facts → write patch JSON to scratchpad → self-check with
   `python3 scripts/validate_rewrite.py data/story.json <patch>` until OK → final message:
   count, validator result, one best rewrite for quality inspection.
4. **Per-batch merge** (inline): validator → merge → `scripts/verify_story.py` (ALL CHECKS
   PASSED) → `qa/verify_endings.py` (character stays at full reachability — post-Phase-0
   counts) → commit `feat(story): <Name> prose pass batch N/M`.
5. **After last batch:** spot-read 10 random scenes against the style bible; fix weak ones
   inline. Push.

## Phase 5 — Gameplay level-ups (any session, independent of prose)

1. **Surface elemental weaknesses in combat UI:** weakness/resistance data exists and is
   applied (`apply_elemental_weakness` in src/moves.py) but players can't see it mid-fight.
   Add a hint line to the move menu when a move's element matches a living target's weakness
   (e.g. `[2] Void Burst … ★ exploits weakness`). Pure presentation, goes in
   `src/combat_text.py` + menu print in `engine.py`. TDD like v2.2.
2. **Tells for basic attacks of special-less enemies:** 14 specials have tells; enemies
   without specials never telegraph. Add optional `tell` at the Enemy level in bestiary.py
   used as pre-attack flavor on a low random chance. Copywriting task, ~20 enemies.
3. **Choice-text audit game-wide:** run the beat-map "weak choice text" detection across all
   characters at once (mood-words → verbs). Small dedicated subagent + validator pass.
4. **Consequence audit per character:** fold into each character's batch prompts (the Kira
   run did this via payoff threads — keep doing it).

## Stretch (needs its own spec + user sign-off — do NOT start from this plan)

- **Convergence act:** shared final chapter where all five threads meet at the Temple.
  All five storylines already orbit the same Hollow King/crown mythology and the shared
  bestiary (Vespera, The Hollow King) supports it. Brainstorm → spec → plan cycle required.
- New Game+ cross-character knowledge; persistent world state.

## Hard rules (carry from v2.2 — violating these broke nothing only because they were enforced)

- Protected fields (validator-enforced): `id`, `leads_to`, `effects`, `requires`, `type`,
  `combat`, choice `letter`/`leads_to`/`effects`/`requires`.
- `VELANTHOR_FAST=1` for every test/scripted run.
- Full verification block (see project CLAUDE.md) before any "done" claim; character ending
  reachability must never regress from post-Phase-0 counts.
- One subagent at a time. Commit per batch. Push at end of each phase. Update this file's
  checkboxes + project CLAUDE.md working notes as phases complete.

## Phase checklist

- [ ] Phase 0: reachability tracer + Theron/Vex/Elara ending fixes
- [ ] Phase 1: Vex prose pass (style bible, beat map, ~6 batches)
- [ ] Phase 2: Asha prose pass (~6 batches)
- [ ] Phase 3: Elara prose pass (~5 batches)
- [ ] Phase 4: Theron prose pass (~6 batches)
- [ ] Phase 5.1: weakness hints in combat UI
- [ ] Phase 5.2: basic-attack tells
- [ ] Phase 5.3: game-wide choice-text audit
