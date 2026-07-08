# Future plans

- Scale the v2.2 prose pass to the other 4 characters (Theron → Vex → Elara → Asha), each
  with their own style bible + beat map, same batch/validator pipeline. Kira is the template.
- Fix pre-existing unreachable endings: Theron 11/17 unreachable, Vex 8/11 unreachable
  (per `qa/verify_endings.py`) — likely broken `requires` gates or orphaned branches.
- Convergence act: a shared final chapter where the 5 storylines meet (all of them already
  orbit the Hollow King / crown mythology). Big lift — needs its own spec.
- Combat: elemental weaknesses surfaced in the UI (data exists, players can't see it);
  tells for basic enemies without specials (currently only 14 specials have tells).
- Consequence audit for non-Kira characters: earlier choices visibly paying off later.
