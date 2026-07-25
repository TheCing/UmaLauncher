"""Build the event-outcome lookup that lets the helper predict a choice's
result before you click, from your own training logs.

For every career event that pauses for a choice, we pair the pre-rolled
choice_array signature with the condition(s) that actually followed. Only
(story_id, choice_number, signature) combos with a single, consistent observed
outcome are kept — so the table never asserts a result we haven't seen hold.

A choice's outcome is determined by its OWN rolled entry (the choice_array
element at the picked position), which generalizes across rolls of the other
choices — so we key by that entry rather than the whole signature.

Output: umalauncher/_assets/event_outcomes.json
    { "<story_id>": { "<choice_number>": { "<entry_key>": [effect_id, ...] } } }
  where entry_key is "<select_index>:<gain_select_id_index>".

Re-run after playing more events to widen coverage:
    uv run python tools/build_event_outcomes.py
"""
import gzip
import json
import glob
import os
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_GLOBS = [
    os.path.join(ROOT, "umalauncher/appdata/GL/training_logs/*.gz"),
    os.path.join(ROOT, "umalauncher/appdata/GL/training_logs/*.json"),
    os.path.join(ROOT, "umalauncher/appdata/JP/training_logs/*.gz"),
    os.path.join(ROOT, "umalauncher/appdata/JP/training_logs/*.json"),
]
OUT = os.path.join(ROOT, "umalauncher/_assets/event_outcomes.json")


def load_packets(path):
    try:
        content = gzip.open(path, "rb").read().decode("utf-8") if path.endswith(".gz") \
            else open(path, encoding="utf-8").read()
        return json.loads("[" + content + "]")
    except Exception:
        return []


def entry_list(choice_array):
    """Per-choice rolled entries as 'select_index:gain_select_id_index' strings."""
    return [f"{c.get('select_index')}:{c.get('gain_select_id_index')}"
            for c in choice_array if isinstance(c, dict)]


def main():
    files = []
    for g in LOG_GLOBS:
        files += glob.glob(g)

    # (story, choice_number, entry_key) -> {outcome_tuple: count}
    observed = defaultdict(lambda: defaultdict(int))

    for path in files:
        packets = load_packets(path)
        last_effects = None
        last_choice_number = None
        pending = None
        for pkt in packets:
            if not isinstance(pkt, dict):
                continue
            if pkt.get("_direction") == 0:
                if "choice_number" in pkt:
                    last_choice_number = pkt.get("choice_number")
                continue
            ci = pkt.get("chara_info")
            cur = tuple(sorted(ci.get("chara_effect_id_array", []) or [])) if isinstance(ci, dict) else None
            if pending is not None and cur is not None and pending["pre"] is not None:
                added = tuple(e for e in cur if e not in pending["pre"])
                entries = pending["entries"]
                cn = last_choice_number
                # The picked choice's own rolled entry drives its outcome.
                if isinstance(cn, int) and 1 <= cn <= len(entries):
                    observed[(pending["story"], cn, entries[cn - 1])][added] += 1
                pending = None
            if cur is not None:
                last_effects = cur
            for ev in (pkt.get("unchecked_event_array") or []):
                if not isinstance(ev, dict):
                    continue
                cc = (ev.get("event_contents_info") or {}).get("choice_array")
                if isinstance(cc, list) and len(cc) >= 2:
                    pending = {"story": ev.get("story_id"), "entries": entry_list(cc), "pre": last_effects}
                    last_choice_number = None
                    break

    # Keep only consistent (single-outcome) combos.
    table = defaultdict(lambda: defaultdict(dict))
    kept = dropped = 0
    for (story, choice, entry), outcomes in observed.items():
        if story is None:
            continue
        if len(outcomes) != 1:
            dropped += 1
            continue
        added = next(iter(outcomes))
        table[str(story)][str(choice)][entry] = list(added)
        kept += 1

    # Plain nested dict for JSON.
    out = {s: {c: dict(sigs) for c, sigs in choices.items()} for s, choices in table.items()}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    n_stories = len(out)
    n_entries = sum(len(sigs) for choices in out.values() for sigs in choices.values())
    print(f"files scanned:      {len(files)}")
    print(f"kept combos:        {kept}  (dropped {dropped} inconsistent)")
    print(f"stories covered:    {n_stories}")
    print(f"total sig entries:  {n_entries}")
    print(f"wrote {os.path.relpath(OUT)} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
