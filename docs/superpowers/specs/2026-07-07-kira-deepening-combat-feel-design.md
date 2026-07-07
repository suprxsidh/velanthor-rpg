# Velanthor v2.2 — Kira story deepening + combat feel

Date: 2026-07-07. Approved scope (user delegated execution before leaving): deepen Kira's
storyline end-to-end, improve combat feel/readability, repo housekeeping. No structural
story rework, no new mechanics. Budget ceiling ~400k tokens, Sonnet subagents, one at a time.

## Why

Current Kira prose (139 scenes, 24 endings) is grammatically clean but flat: functional
beat-delivery with no voice, thin sensory detail (median scene 248 chars), and major endings
resolved in 2–3 sentences. Combat is mechanically deep (combos, status effects, multi-enemy
AI) but reads as a stat printout — no tells, no weight, no pacing.

## Workstream 1 — Housekeeping (first, one commit)

- Delete stale orphans: `data/story.json.merged.20260424` (April merge, superseded — current
  story.json has 721 scenes incl. all Asha; orphan has 161, no Asha),
  `data/story_asha_ch1.json` (all 14 scenes exist in story.json in newer form).
- Delete untracked backup litter: `data/story_backup_*.json`, `data/story_fixed_temp.json`,
  `data/story_kira_expansion.json`, `src/*_backup.py`, `test-game.js`, screenshots out of
  repo root (keep `game-screenshot.png` if referenced by README, else delete).
- Untrack (keep on disk → then delete): tracked `*.bak`, `story.json.backup_before_expand`,
  `story.json_fixed`, `story_vex_expansion.json`, `story_vex_converted.json` — .gitignore
  already ignores `*.bak`; extend it for the rest.
- Fix Chinese leftovers in `src/moves.py` combo descriptions (10 strings) — replace with
  English matching the existing description style.
- `.pyc` untracking (BUILD_PLAN step 7 item): already moot, nothing tracked.

## Workstream 2 — Kira story deepening

### Style bible (`docs/story/kira-style-bible.md`, written first, ~1 page)

- **Voice**: second person, present tense (matches existing). Kira is guarded, precise,
  darkly wry — she notices exits, weighs people like threats, and feels the void as a
  physical pull (cold behind the sternum), not an abstraction.
- **Imagery bank**: void = cold/hunger/static; her magic costs warmth; light sources guttering
  around her when she draws power. Recurring: her mother's voice, the silver crescent,
  unhealed frostbite scars on her fingers.
- **Bans**: em-dash chains, "little did she know", "a chill ran down", generic dark-fantasy
  filler ("ancient evil stirs"), AI-tell constructions. Choices must be verbs, not moods.
- **Scene targets**: normal scenes 400–700 chars, chapter climaxes 700–1100, endings 600–1000.
  Every scene: at least one concrete sensory detail + one line that only Kira would think.
- **Consequence audit rule** (folded in): where a scene references a past choice, name it
  specifically; where `effects` grant stats, the prose should show why.

### Beat map (`docs/story/kira-beat-map.md`)

Chapter-by-chapter emotional targets derived from reading the existing arc before rewriting
(CH1 hunted/alone → ... → endings). Written by the first subagent after reading all 139
scenes; approved by main session before rewrites start.

### Execution

- One Sonnet subagent per batch, sequential (RAM rule), ~28 scenes/batch (5 batches).
- Each batch: read style bible + beat map + its scene slice from story.json, rewrite
  `description` fields (and choice `text` where weak), NEVER touch ids/leads_to/effects/
  requires/type/combat fields. Output JSON patch file; main session validates (json parse,
  key-set identical, graph fields untouched) and merges.
- Validation after all batches: existing verification suite (`analyze_story.py`, story graph
  reachability) must still report 24 Kira endings reachable, zero dead ends.

## Workstream 3 — Combat feel (engine.py, moves.py; no mechanics changes)

1. **Paced output**: short beat-delays between combat lines (existing terminal, `time.sleep`
   ~0.3–0.6s, skippable via config flag / env var for tests).
2. **Contextual damage lines**: damage rendered inside a sentence chosen by move + remaining
   HP band ("The cultist's blade opens your shoulder — 12." / kill lines distinct), not
   `Enemy hits you for 12`.
3. **Enemy tells**: turn before a special/cooldown move fires, print its tell ("The Hollow
   Priest begins the same syllable twice…") — data: add `tell` string per special in
   bestiary.py.
4. **Moment weight**: low-HP warnings (once per band, not spam), combo landing gets its
   chain description line, status effect application/expiry in plain words.
5. **Round header cleanup**: compact status line (HP bars as ▓░, active effects as tags).
- Tests: existing combat tests must pass with delays disabled; add snapshot-style test for
  the new renderer functions (pure functions returning strings → easy to test).

## Not doing (YAGNI)

- No shared-final-act / convergence content (future_plans candidate).
- No new combat mechanics (stances, positioning).
- No prose pass on the other 4 characters yet — Kira is the proof of concept; user reviews
  before scaling.

## Order & verification

1. Housekeeping commit → tests green.
2. Combat feel (engine work benefits all playtesting after it) → combat tests + one scripted
   playthrough to eyeball output.
3. Style bible + beat map → committed.
4. Kira batches 1–5, validate + commit per batch.
5. Full verification suite + manual spot-read of 10 random rewritten scenes + endings.
6. Update README (version v2.2), BUILD_PLAN.md, future_plans.md.
