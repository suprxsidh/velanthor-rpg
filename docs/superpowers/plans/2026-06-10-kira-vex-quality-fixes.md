# KIRA & VEX Quality Fixes Implementation Plan

**Goal:** Fix KIRA's placeholder ending descriptions and VEX's illusion-of-choice funnel in Chapter 1. Then replay all 5 characters.

**Architecture:** Two independent workstreams running in parallel, followed by a replay validation pass.

**Tech Stack:** Python, story.json JSON data

---

## Background

### KIRA Issue
14 endings have placeholder descriptions (< 60 chars each) that need proper narrative text. The agents also flagged Chapters 4-5 scene descriptions as thin.

### VEX Issue  
5 Chapter 1 scenes have A/B/C choices but ALL choices lead to VEX_CH1_SISTER. This makes choices meaningless. Fix: create new intermediate scenes so different choices produce different content before converging at the sister.

---

## Task 1: Fix KIRA Placeholder Endings

**Files:** Modify `data/story.json` (14 endings and Ch4-5 scenes)

Approach:
- Read KIRA's full endings and key scenes to match tone/style  
- Write 150-300 word narrative descriptions for each placeholder ending
- KIRA's themes: void magic, burden of power, family legacy, freedom vs. responsibility
- Also check Ch4-5 scenes for thin descriptions and flesh them out

## Task 2: Fix VEX CH1 Funnel  

**Files:** Create new scenes in `data/story.json`, modify existing scenes

Approach:
- For each of the 5 funnel scenes, split 1-2 choices to new intermediate scenes
- New scenes describe the outcome of that specific choice
- Each new scene leads to VEX_CH1_SISTER (rejoin the main path)
- Minimum new content per scene (60-100 words), focus on meaningful consequence

Affected scenes:
1. VEX_CH1_BETRAYAL_SETUP → create VEX_CH1_BETRAYAL_TRAP, VEX_CH1_BETRAYAL_SNOOP
2. VEX_CH1_CORRUPTION → create VEX_CH1_CORRUPT_EXPOSE, VEX_CH1_CORRUPT_LEVERAGE  
3. VEX_CH1_FIRST_JOB → create VEX_CH1_JOB_LOOT, VEX_CH1_JOURNAL  
4. VEX_CH1_MENTOR → create VEX_CH1_TRAINING, VEX_CH1_STREET_SMART
5. VEX_CH1_STREET_RIVALS → create VEX_CH1_CHALLENGE, VEX_CH1_DIRT

## Task 3: Replay All Characters

**Files:** `scripts/test_playability.py`

Run BFS path tracer for all 5 characters, then a deterministic playthrough tracing every reachable scene.

## Execution

Run Task 1 and Task 2 in parallel via subagents, then Task 3 after both complete.
