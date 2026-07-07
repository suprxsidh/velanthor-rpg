# Kira Nightwind — Style Bible (v2.2 prose pass)

Contract for anyone rewriting KIRA_* scenes. Follow mechanically. When a rule here
conflicts with making a scene better, the rule wins — consistency across 139 scenes
beats one clever paragraph.

## Voice

- Second person, present tense (matches the rest of the game). Never past tense.
- Kira is guarded, precise, darkly wry. She was raised being hunted: she counts exits
  before she counts friends, and she weighs every stranger as a threat first and a
  person second. Her humor is dry and arrives at the worst moments.
- She does not gasp, tremble, or feel her heart "hammer". She notices, calculates,
  decides. Fear shows in what she *does* (checking the door twice, palming a knife),
  never in narrated emotion words.
- The void is not an abstraction to her. It is physical: a cold pull behind the
  sternum, a hunger that eats warmth. Drawing on it COSTS — candles gutter, frost
  webs across glass, her fingertips go white. Show at least one cost cue whenever
  she uses void magic in a scene.

## Imagery bank (draw from these; invent within this register)

- void: cold, static, hunger, the space between heartbeats, sound arriving late
- her magic: light bending away from her, breath fogging in warm rooms, the taste of iron
- recurring anchors (seed early, pay off late): her mother's voice half-remembered,
  the silver crescent of the Circle, the frostbite scars on her fingers that never healed
- Crownhaven: wet stone, tallow smoke, bells that ring a beat out of time
- the Cult: too-clean robes, smiles that hold too long, children's chalk drawings where
  children shouldn't be

## Bans (hard)

- No em-dash chains (one "—" per sentence maximum; prefer none — this is game copy,
  hyphens and periods do the work)
- No "little did she know", "a chill ran down", "ancient evil", "time seemed to slow",
  "she let out a breath she didn't know she was holding"
- No AI-tell constructions: "It's not X, it's Y", triadic flourishes ("no X, no Y,
  only Z"), "something in her [verb]ed"
- Choices are verbs, not moods: "Follow the merchant" not "Embrace curiosity"

## Scene length targets (characters, description field)

- Normal scenes: 400–700
- Chapter climaxes (per beat map): 700–1100
- Endings: 600–1000 — an ending earns its weight: consequence, image, and what it
  cost Kira, in that order. Never resolve in two sentences.

## Every scene must have

1. At least one concrete sensory detail (sound, temperature, smell, texture — not sight-only).
2. At least one line only Kira would think (her read of a person, an exit noted, a dry aside).
3. If the scene's choices carry `effects` (stat changes), prose that motivates them —
   a +courage choice should read like it takes nerve.
4. If the scene references a past event, name it specifically (the merchant's crescent,
   the cellar in Millbrook) — never "what happened before".

## Never touch

`id`, `leads_to`, `effects`, `requires`, `type`, `combat` fields, choice `letter`s,
scene count, graph structure. Rewrite `description` and (only where flagged weak)
choice `text`. The validator will reject anything else.
