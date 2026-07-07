"""Validate a rewrite patch: same keys, protected fields untouched, prose rules."""
import json
import sys

PROTECTED = ("id", "leads_to", "effects", "requires", "type", "combat")


def main(orig_path, patch_path):
    orig = json.load(open(orig_path))
    oscenes = orig.get("scenes", orig)
    patch = json.load(open(patch_path))
    errs = []
    for k, new in patch.items():
        if k not in oscenes:
            errs.append(f"{k}: not in original")
            continue
        old = oscenes[k]
        for f in PROTECTED:
            if old.get(f) != new.get(f):
                errs.append(f"{k}: protected field '{f}' changed")
        oc = old.get("choices") or []
        nc = new.get("choices") or []
        if len(oc) != len(nc):
            errs.append(f"{k}: choice count changed")
        else:
            for o, n in zip(oc, nc):
                for f in ("letter", "leads_to", "effects", "requires"):
                    if o.get(f) != n.get(f):
                        errs.append(f"{k}: choice {o.get('letter')} field '{f}' changed")
        d = new.get("description", "")
        if "— " in d and d.count("—") > d.count(". ") + d.count("! ") + d.count("? ") + 1:
            errs.append(f"{k}: em-dash overuse ({d.count('—')} in scene)")
        for cliche in ("little did", "chill ran down", "ancient evil",
                       "time seemed to slow", "breath she didn't know"):
            if cliche in d.lower():
                errs.append(f"{k}: banned phrase '{cliche}'")
    print("\n".join(errs) if errs else "OK")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
