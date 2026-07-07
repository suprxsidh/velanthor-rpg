# Kira Deepening + Combat Feel (v2.2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deepen Kira's 139-scene storyline with a style-bible-driven prose pass, and make combat read as drama instead of a stat printout — no mechanics changes.

**Architecture:** Combat presentation is extracted into a new pure-function module `src/combat_text.py` (testable strings, no I/O) which `engine.py` calls; story changes are data-only edits to `description`/choice-`text` fields in `data/story.json`, validated by a structural-integrity script before merge.

**Tech Stack:** Python 3 (stdlib only, matches repo), JSON story data, existing verification suite (`scripts/verify_story.py`, `qa/verify_endings.py`, `test_combat_system.py`).

## Global Constraints

- Never modify scene `id`, `leads_to`, `effects`, `requires`, `type`, `combat`, or choice `letter` fields in story.json — prose fields only (`description`, choice `text`).
- Kira must keep exactly 24 reachable endings and 139 scenes; `scripts/verify_story.py` must report 0 broken refs / 0 dead ends after every merge.
- No new combat mechanics — presentation only. All existing tests must pass with `VELANTHOR_FAST=1`.
- Prose rules (from spec + user's standing no-slop rule): no em-dash chains, no "little did she know" / "chill ran down" clichés, scene length targets 400–700 chars (climaxes 700–1100, endings 600–1000), every scene gets ≥1 concrete sensory detail.
- Theron/Vex unreachable endings are PRE-EXISTING (baseline: Theron 6/17, Vex 3/11 reachable) — out of scope, do not "fix".
- Subagents: Sonnet, strictly one at a time.

---

### Task 1: Repo housekeeping

**Files:**
- Modify: `.gitignore`
- Modify: `src/moves.py:40-60` (11 Chinese-remnant strings)
- Delete (untracked): `data/story.json.merged.20260424`, `data/story_asha_ch1.json`, `data/story_backup_*.json` (6 files), `data/story_fixed_temp.json`, `data/story_kira_expansion.json`, `src/bestiary_backup.py`, `src/engine_backup.py`, `src/moves_backup.py`, `test-game.js`
- Untrack + delete (tracked): `data/story.json.backup_before_expand`, `data/story.json_fixed`, `data/story_elara.json.bak`, `data/story_kira.json.bak`, `data/story_theron.json.bak`, `data/story_vex_converted.json.bak`

**Interfaces:**
- Produces: clean repo; `tests/` directory become trackable (gitignore scoped to root).

- [ ] **Step 1: Scope dev-script ignores to repo root so `tests/` can be tracked later**

In `.gitignore` replace the unanchored patterns with root-anchored ones:

```gitignore
__pycache__/
*.pyc
.DS_Store
*.bak
*.current
/test_*
/trace_*
/find_*
/kira_*
/analyze_*_paths.py
/count_scenes.py
/add_kira.py
/test_save
wiki/.DS_Store
data/story_backup_*.json
```

Note: `/test_*` keeps ignoring the root dev scripts but allows `tests/*.py`. `test_combat_system.py` is already tracked — already-tracked files are unaffected by ignore rules.

- [ ] **Step 2: Delete stale untracked files**

```bash
cd ~/opencode-projects/the-legend-of
rm data/story.json.merged.20260424 data/story_asha_ch1.json \
   data/story_backup_20260424.json data/story_backup_20260504.json \
   data/story_backup_phase3.json data/story_backup_v1.5.1.json \
   data/story_backup_v2_20260504.json data/story_backup_vex_expansion.json \
   data/story_fixed_temp.json data/story_kira_expansion.json \
   src/bestiary_backup.py src/engine_backup.py src/moves_backup.py test-game.js \
   game-screenshot.png game-start-screen.png
```

- [ ] **Step 3: Untrack tracked backup litter**

```bash
git rm data/story.json.backup_before_expand data/story.json_fixed \
       data/*.bak
```

- [ ] **Step 4: Replace the 11 Chinese-remnant combo descriptions in `src/moves.py`**

Each keeps its English lead, drops the Chinese tail, gains a proper clause (exact replacements):

| Line | New description |
|---|---|
| 40 | `"Dark evolution — the wound deepens with every heartbeat"` |
| 45 | `"Defensive fury — a measured strike from perfect footing"` |
| 48 | `"Deadly combination — venom seeps into the open cut"` |
| 49 | `"Shadow execution — the mark glows where the knife will land"` |
| 50 | `"Stealth strike — they never saw the second blade"` |
| 53 | `"Psychological warfare — fear does half the work"` |
| 54 | `"Business destruction — their composure shatters like glass"` |
| 55 | `"Social manipulation — they want to help you now"` |
| 58 | `"Nature's trap — roots close like a fist"` |
| 59 | `"Beast fury — claws follow where the call leads"` |
| 60 | `"Nature's blessing — green light knits the flesh"` |

(Use a single `—` per line, not chains; these are game copy, allowed as single separators.)

- [ ] **Step 5: Verify nothing broke**

```bash
python3 scripts/verify_story.py | tail -3   # expect: ✓ ALL CHECKS PASSED
python3 test_combat_system.py | tail -2     # expect: ALL AGENTS APPROVED
python3 -c "import src.moves"               # expect: no output
grep -c '[一-龥]' src/moves.py               # expect: 0
```

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "chore: remove backup litter and stale orphan story files, fix combo copy"
```

---

### Task 2: Combat text renderer module (pure functions, TDD)

**Files:**
- Create: `src/combat_text.py`
- Create: `tests/test_combat_text.py`

**Interfaces:**
- Produces (consumed by Task 3):
  - `hp_bar(current: int, maximum: int, width: int = 20) -> str` — `▓`/`░` bar, no color codes.
  - `damage_line(attacker: str, move_name: str, damage: int, target_hp_after: int, target_max_hp: int, target: str = "you") -> str` — full sentence containing the damage number; wording varies by remaining-HP band (>0.5 / ≤0.5 / ≤0.25 / dead ≤0).
  - `enemy_tell(enemy_name: str, tell: str) -> str` — formatted one-liner.
  - `low_hp_warning(current: int, maximum: int, already_warned: set) -> str | None` — returns a warning string the first time HP crosses 50% and 25% bands, else None; mutates `already_warned` with band keys `"half"`/`"quarter"`.
  - `beat(seconds: float = 0.45) -> None` — `time.sleep` unless env `VELANTHOR_FAST` is set.

- [ ] **Step 1: Write failing tests**

```python
# tests/test_combat_text.py
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.combat_text import hp_bar, damage_line, enemy_tell, low_hp_warning

class TestHpBar(unittest.TestCase):
    def test_full(self):
        self.assertEqual(hp_bar(10, 10, width=10), "▓" * 10)
    def test_half(self):
        self.assertEqual(hp_bar(5, 10, width=10), "▓" * 5 + "░" * 5)
    def test_zero_floor(self):
        self.assertEqual(hp_bar(-3, 10, width=10), "░" * 10)

class TestDamageLine(unittest.TestCase):
    def test_contains_number_and_target(self):
        line = damage_line("Bandit", "Dirty Strike", 12, 60, 100)
        self.assertIn("12", line)
        self.assertIn("Bandit", line)
    def test_kill_band_wording_differs(self):
        healthy = damage_line("Bandit", "Dirty Strike", 12, 80, 100)
        kill = damage_line("Bandit", "Dirty Strike", 12, 0, 100)
        self.assertNotEqual(healthy, kill)

class TestEnemyTell(unittest.TestCase):
    def test_contains_name_and_tell(self):
        line = enemy_tell("Hollow Priest", "begins the same syllable twice")
        self.assertIn("Hollow Priest", line)
        self.assertIn("syllable", line)

class TestLowHpWarning(unittest.TestCase):
    def test_warns_once_per_band(self):
        warned = set()
        self.assertIsNotNone(low_hp_warning(49, 100, warned))
        self.assertIsNone(low_hp_warning(45, 100, warned))
        self.assertIsNotNone(low_hp_warning(20, 100, warned))
        self.assertIsNone(low_hp_warning(10, 100, warned))
    def test_no_warning_above_half(self):
        self.assertIsNone(low_hp_warning(80, 100, set()))

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run to verify failure**

```bash
python3 -m unittest tests.test_combat_text -v 2>&1 | tail -3
# Expected: ModuleNotFoundError / ImportError on src.combat_text
```

- [ ] **Step 3: Implement `src/combat_text.py`**

```python
"""Combat presentation helpers — pure functions, no game state.

All functions return strings (or None); engine.py decides when to print.
Pacing: beat() honors VELANTHOR_FAST so tests and scripted runs skip delays.
"""
import os
import time

def hp_bar(current, maximum, width=20):
    if maximum <= 0:
        return "░" * width
    filled = max(0, min(width, round(width * current / maximum)))
    return "▓" * filled + "░" * (width - filled)

def damage_line(attacker, move_name, damage, target_hp_after, target_max_hp, target="you"):
    frac = target_hp_after / target_max_hp if target_max_hp else 0
    if target_hp_after <= 0:
        if target == "you":
            return f"{attacker}'s {move_name} lands — {damage} — and the world tilts. You are down."
        return f"{attacker} takes {move_name} for {damage} and drops, finished."
    if frac <= 0.25:
        if target == "you":
            return f"{attacker}'s {move_name} tears through your guard — {damage}. You taste copper."
        return f"{move_name} rips into {attacker} for {damage} — it staggers, barely upright."
    if frac <= 0.5:
        if target == "you":
            return f"{attacker}'s {move_name} connects hard — {damage}. Your knees argue."
        return f"{move_name} slams {attacker} for {damage} — it is hurting now."
    if target == "you":
        return f"{attacker}'s {move_name} catches you — {damage}."
    return f"{move_name} strikes {attacker} for {damage}."

def enemy_tell(enemy_name, tell):
    return f"⚠ {enemy_name} {tell}"

def low_hp_warning(current, maximum, already_warned):
    frac = current / maximum if maximum else 0
    if frac <= 0.25 and "quarter" not in already_warned:
        already_warned.update({"half", "quarter"})
        return "Your vision narrows. One more mistake ends this."
    if frac <= 0.5 and "half" not in already_warned:
        already_warned.add("half")
        return "Blood on your grip. This is no longer going your way."
    return None

def beat(seconds=0.45):
    if not os.environ.get("VELANTHOR_FAST"):
        time.sleep(seconds)
```

- [ ] **Step 4: Run tests to verify pass**

```bash
python3 -m unittest tests.test_combat_text -v 2>&1 | tail -3
# Expected: OK (7 tests)
```

- [ ] **Step 5: Commit**

```bash
git add src/combat_text.py tests/test_combat_text.py
git commit -m "feat(combat): pure-function combat text renderer with tests"
```

---

### Task 3: Wire renderer into engine + enemy tells in bestiary

**Files:**
- Modify: `src/engine.py` (combat_encounter, ~lines 627–980: damage prints, enemy turn, round header)
- Modify: `src/bestiary.py` (add `tell` to special moves)
- Test: existing `test_combat_system.py` + `tests/test_combat_text.py`

**Interfaces:**
- Consumes: all Task 2 functions (`from src.combat_text import hp_bar, damage_line, enemy_tell, low_hp_warning, beat`).
- Produces: no new public API; behavior-identical combat with new presentation.

- [ ] **Step 1: Add `tell` strings to bestiary special moves**

In `src/bestiary.py`, for every enemy move dict that has a cooldown/special flag, add a
`"tell"` key with a one-line physical tell written in the game's voice. Every enemy with
specials gets one (examples to follow for the rest):

```python
# e.g. Hollow Priest special
{"name": "Void Sermon", ..., "tell": "begins the same syllable twice, voice doubling"}
# e.g. Bandit heavy
{"name": "Dirty Strike", ..., "tell": "shifts his weight to the back foot, blade low"}
```

- [ ] **Step 2: Engine — announce tells one turn ahead**

In the enemy-turn section of `combat_encounter`, where the AI selects a special move for
*next* use (cooldown ready), print the tell this turn:

```python
from src.combat_text import hp_bar, damage_line, enemy_tell, low_hp_warning, beat
# in enemy turn loop, when a special is off cooldown and will be used next round:
if next_move.get("tell"):
    print(f"  {YELLOW}{enemy_tell(en.name, next_move['tell'])}{RESET}")
```

If the AI currently picks moves same-turn (no lookahead), implement the tell as: when a
special is selected, print the tell, `beat(0.8)`, then resolve it — the pause IS the window.

- [ ] **Step 3: Engine — replace bare damage prints with `damage_line`, add beats**

Replace prints of the form `print(f"{en.name} hits you for {dmg}")` and player-hit
equivalents with `damage_line(...)` calls followed by `beat()`. Keep color wrapping.

- [ ] **Step 4: Engine — compact round header with HP bars + effect tags**

At the top of each round, replace the current status dump:

```python
print(f"\n{BOLD}— Round {combat_round} —{RESET}")
print(f"  You   {hp_bar(self.health, true_max_hp)} {self.health}/{true_max_hp}  MP {self.mana}" + (f"  [{', '.join(e.effect_type for e in self.status_effects)}]" if self.status_effects else ""))
for i in alive_indices:
    print(f"  {enemies[i].name:<12} {hp_bar(enemy_hp_list[i], enemies[i].hp)} {enemy_hp_list[i]}/{enemies[i].hp}")
```

- [ ] **Step 5: Engine — low-HP warnings**

Initialize `hp_warnings = set()` at combat start; after any player damage:

```python
w = low_hp_warning(self.health, true_max_hp, hp_warnings)
if w:
    beat(); print(f"  {RED}{w}{RESET}")
```

- [ ] **Step 6: Verify**

```bash
VELANTHOR_FAST=1 python3 test_combat_system.py | tail -2   # ALL AGENTS APPROVED
VELANTHOR_FAST=1 python3 -m unittest tests.test_combat_text 2>&1 | tail -1  # OK
VELANTHOR_FAST=1 python3 scripts/combat_sandbox.py 2>&1 | head -40  # eyeball new output
```

- [ ] **Step 7: Commit**

```bash
git add src/engine.py src/bestiary.py
git commit -m "feat(combat): enemy tells, contextual damage lines, HP bars, paced output"
```

---

### Task 4: Kira style bible + beat map

**Files:**
- Create: `docs/story/kira-style-bible.md` (main session writes — content already specified in spec §Workstream 2; transcribe verbatim with the imagery bank, bans, scene-length targets, consequence rule)
- Create: `docs/story/kira-beat-map.md` (Sonnet subagent writes)

**Interfaces:**
- Produces: both docs are the prompt-contract for all Task 5 batches.

- [ ] **Step 1: Write style bible from spec §Workstream 2** (verbatim transcription + expansion of the voice/imagery/bans/targets bullets into prose rules a rewriter can follow mechanically)

- [ ] **Step 2: Dispatch ONE Sonnet subagent to write the beat map**

Prompt contract: read all 139 KIRA_* scenes from `data/story.json` (jq/python extraction),
produce `docs/story/kira-beat-map.md`: per chapter — what Kira wants, what it costs,
the emotional note each chapter must end on, which scenes are climaxes (get the 700–1100
char budget), which endings belong to which thematic family (crown/mother/void/walk-away),
and the 3–5 payoff threads that must be seeded early (crescent symbol, mother's voice,
frostbite scars). No rewriting yet.

- [ ] **Step 3: Main session reviews beat map** against the actual ending list (24) and chapter structure; fix drift inline.

- [ ] **Step 4: Commit**

```bash
git add docs/story/
git commit -m "docs(story): Kira style bible and beat map for v2.2 prose pass"
```

---

### Task 5: Kira prose pass — 5 sequential batches

**Files:**
- Create: `scripts/validate_rewrite.py` (once, batch 1)
- Modify: `data/story.json` (KIRA_* `description` + weak choice `text` only)

**Interfaces:**
- Consumes: style bible, beat map, Task 2/3 combat output unaffected.
- Produces per batch: `patch file scratchpad/kira_batch_N.json` → merged into story.json.

- [ ] **Step 1 (once): Write `scripts/validate_rewrite.py`**

```python
"""Validate a rewrite patch: same keys, protected fields untouched, prose rules."""
import json, re, sys

PROTECTED = ("id", "leads_to", "effects", "requires", "type", "combat")

def main(orig_path, patch_path):
    orig = json.load(open(orig_path)); oscenes = orig.get("scenes", orig)
    patch = json.load(open(patch_path))
    errs = []
    for k, new in patch.items():
        if k not in oscenes:
            errs.append(f"{k}: not in original"); continue
        old = oscenes[k]
        for f in PROTECTED:
            if old.get(f) != new.get(f):
                errs.append(f"{k}: protected field '{f}' changed")
        oc = old.get("choices") or []; nc = new.get("choices") or []
        if len(oc) != len(nc):
            errs.append(f"{k}: choice count changed")
        else:
            for o, n in zip(oc, nc):
                for f in ("letter", "leads_to", "effects", "requires"):
                    if o.get(f) != n.get(f):
                        errs.append(f"{k}: choice {o.get('letter')} field '{f}' changed")
        d = new.get("description", "")
        if "—" in d and "——" in d.replace("— ", "—"):
            errs.append(f"{k}: em-dash chain")
        for cliche in ("little did", "chill ran down", "ancient evil"):
            if cliche in d.lower():
                errs.append(f"{k}: banned phrase '{cliche}'")
    print("\n".join(errs) if errs else "OK")
    sys.exit(1 if errs else 0)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
```

- [ ] **Step 2 (per batch N=1..5): dispatch ONE Sonnet subagent**

Batch slices: sort KIRA_* keys; batch = 28 scenes (last batch ~27). Subagent prompt
contract: receives style bible + beat map + its slice extracted as JSON; returns the same
JSON with only `description` and (where flagged weak) choice `text` rewritten to targets;
writes to `scratchpad/kira_batch_N.json`. Explicit instruction block: NEVER change
protected fields; scene-length targets; ≥1 sensory detail; endings get full weight.

- [ ] **Step 3 (per batch): validate → merge → verify → commit**

```bash
python3 scripts/validate_rewrite.py data/story.json scratchpad/kira_batch_N.json  # OK
python3 - <<'EOF'
import json
d = json.load(open('data/story.json')); s = d.get('scenes', d)
p = json.load(open('scratchpad/kira_batch_N.json'))
s.update(p)
json.dump(d, open('data/story.json','w'), indent=2, ensure_ascii=False)
EOF
python3 scripts/verify_story.py | tail -3          # ✓ ALL CHECKS PASSED
python3 qa/verify_endings.py | grep KIRA           # KIRA 24 0
git add data/story.json scripts/validate_rewrite.py
git commit -m "feat(story): Kira prose pass batch N/5"
```

- [ ] **Step 4: After batch 5 — spot-read 10 random rewritten scenes** (main session, direct file read, judge against style bible; fix weak ones inline before final commit).

---

### Task 6: Final verification + docs

**Files:**
- Modify: `README.md` (version → v2.2, mention combat presentation + Kira prose depth)
- Modify: `~/opencode-projects/BUILD_PLAN.md` (step 7 ✅ with summary)
- Create/Modify: `future_plans.md` (add: scale prose pass to Theron/Vex/Elara/Asha; fix pre-existing Theron/Vex unreachable endings; convergence act idea)
- Create: `CLAUDE.md` (project constraints: protected story fields, VELANTHOR_FAST, verification commands, style bible location)

- [ ] **Step 1: Full suite**

```bash
VELANTHOR_FAST=1 python3 test_combat_system.py | tail -2
VELANTHOR_FAST=1 python3 -m unittest tests.test_combat_text 2>&1 | tail -1
python3 scripts/verify_story.py | tail -3
python3 qa/verify_endings.py | tail -8
```

- [ ] **Step 2: Scripted playthrough** — pipe a known choice sequence through `main.py` with `VELANTHOR_FAST=1`, eyeball one combat + three rewritten scenes render correctly in-game.

- [ ] **Step 3: Update docs listed above, commit**

```bash
git add README.md future_plans.md CLAUDE.md
git commit -m "docs: v2.2 — combat feel overhaul + Kira prose deepening"
```

- [ ] **Step 4: Push** (repo already public on suprxsidh)

```bash
git push origin master
```

---

## Self-review notes

- Spec coverage: housekeeping→T1, combat feel 1–5→T2/T3, style bible/beat map→T4, batches+validation→T5, verification/docs→T6. Gap check: spec's "screenshots out of repo root" — resolved: README doesn't reference them; they're untracked; deleted in T1 Step 2? They're not in the rm list — ADD: `rm game-screenshot.png game-start-screen.png` to T1 Step 2.
- Type consistency: `damage_line` signature consistent between T2 tests/impl and T3 usage. `low_hp_warning` set-mutation contract consistent.
- Placeholders: none — all code shown, bestiary tells are per-enemy copywriting done at T3 Step 1 with two exemplars and instruction that EVERY special gets one.
