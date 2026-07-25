"""Read-only proof-of-concept: does an event's rolled choice_array predict the
actual outcome (condition/stat gains that follow)?

Walks the training logs, and for every career event that pauses for a choice,
pairs the pre-rolled choice_array signature with the effect/stat delta observed
on the next chara_info packet. Then reports, per event, whether a given rolled
signature maps to a consistent outcome.

Usage: uv run python tools/analyze_event_outcomes.py
"""
import gzip
import json
import glob
import os
from collections import defaultdict

LOG_GLOBS = [
    "umalauncher/appdata/GL/training_logs/*.gz",
    "umalauncher/appdata/GL/training_logs/*.json",
    "umalauncher/appdata/JP/training_logs/*.gz",
    "umalauncher/appdata/JP/training_logs/*.json",
]


def load_packets(path):
    try:
        content = gzip.open(path, "rb").read().decode("utf-8") if path.endswith(".gz") \
            else open(path, encoding="utf-8").read()
        return json.loads("[" + content + "]")
    except Exception:
        return []


def choice_sig(choice_array):
    return tuple(
        (c.get("select_index"), c.get("gain_select_id_index"))
        for c in choice_array if isinstance(c, dict)
    )


def main():
    files = []
    for g in LOG_GLOBS:
        files += glob.glob(g)

    # (story_id, choice_number, sig) -> Counter of outcome (added_effects tuple, stat_delta_summary)
    outcomes = defaultdict(lambda: defaultdict(int))
    # story_id -> set of sigs (to measure per-play variance)
    story_sigs = defaultdict(set)

    events_seen = 0
    events_linked = 0

    for path in files:
        packets = load_packets(path)
        last_effects = None
        last_choice_number = None
        pending = None  # {story_id, sig, pre_effects}

        for pkt in packets:
            if not isinstance(pkt, dict):
                continue
            direction = pkt.get("_direction")

            # Request: capture the player's pick.
            if direction == 0:
                if "choice_number" in pkt:
                    last_choice_number = pkt.get("choice_number")
                continue

            # Response.
            ci = pkt.get("chara_info")
            cur_effects = None
            if isinstance(ci, dict):
                cur_effects = tuple(sorted(ci.get("chara_effect_id_array", []) or []))

            # Resolve a pending event using this packet's post-state effects.
            if pending is not None and cur_effects is not None and pending["pre_effects"] is not None:
                added = tuple(e for e in cur_effects if e not in pending["pre_effects"])
                key = (pending["story_id"], last_choice_number, pending["sig"])
                outcomes[key][added] += 1
                events_linked += 1
                pending = None

            if cur_effects is not None:
                last_effects = cur_effects

            # Detect a fresh choice event in this packet.
            for ev in (pkt.get("unchecked_event_array") or []):
                if not isinstance(ev, dict):
                    continue
                cc = (ev.get("event_contents_info") or {}).get("choice_array")
                if isinstance(cc, list) and len(cc) >= 2:
                    sig = choice_sig(cc)
                    story = ev.get("story_id")
                    story_sigs[story].add(sig)
                    events_seen += 1
                    pending = {"story_id": story, "sig": sig, "pre_effects": last_effects}
                    last_choice_number = None
                    break

    # --- Report -------------------------------------------------------------
    print(f"files scanned:        {len(files)}")
    print(f"choice events seen:   {events_seen}")
    print(f"events linked to an outcome: {events_linked}")
    print()

    # How deterministic is sig -> added-effects? For (story, choice, sig) keys
    # that we saw >=2 times, is the outcome always the same?
    multi = {k: v for k, v in outcomes.items() if sum(v.values()) >= 2}
    consistent = sum(1 for v in multi.values() if len(v) == 1)
    print(f"(story,choice,sig) combos seen >=2x: {len(multi)}")
    print(f"  of those, outcome was IDENTICAL every time: {consistent}")
    if multi:
        print(f"  => consistency rate: {consistent/len(multi)*100:.1f}%")
    print()

    # Show events where the SAME (story,choice) produced DIFFERENT outcomes for
    # DIFFERENT sigs — i.e. the rolled sig is what distinguishes win/loss.
    by_story_choice = defaultdict(lambda: defaultdict(set))
    for (story, choice, sig), v in outcomes.items():
        for added in v:
            by_story_choice[(story, choice)][sig].add(added)

    discriminating = []
    for (story, choice), sigmap in by_story_choice.items():
        added_sets = set()
        for s in sigmap.values():
            added_sets |= s
        if len(sigmap) >= 2 and len(added_sets) >= 2:
            discriminating.append((story, choice, sigmap))

    print(f"(story,choice) where different rolled sigs => different outcomes: {len(discriminating)}")
    print("  (these are the gamble events where the packet predicts win/loss)")
    for story, choice, sigmap in discriminating[:15]:
        print(f"  story={story} choice_number={choice}")
        for sig, addeds in sigmap.items():
            print(f"      sig={sig} -> added_effects={sorted(addeds)}")


if __name__ == "__main__":
    main()
