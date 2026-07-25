"""Build the set of MANT (Make a New Track, scenario 4) races that restock the
shop when run, learned from training logs.

In MANT, running certain "designated" races immediately restocks the shop with
new items (and auto-skips the after-race event). This isn't in the race-list
packet (every available race looks identical there) nor cleanly in master.mdb,
so we derive it empirically: for each race run, did the shop gain new items
shortly after? Designated races do this ~always; regular races ~never — a clean
bimodal split, so we keep only high-confidence program_ids.

Output: umalauncher/_assets/shop_restock_races.json
    { "restock_program_ids": [<single_mode program_id>, ...] }

Re-run to widen coverage as you play more MANT runs:
    uv run python tools/build_shop_restock_races.py
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
OUT = os.path.join(ROOT, "umalauncher/_assets/shop_restock_races.json")

MIN_OBSERVATIONS = 3
MIN_RESTOCK_RATE = 0.9
LOOKAHEAD = 16  # packets to scan after a race for the (delayed) restock


def load_packets(path):
    try:
        content = gzip.open(path, "rb").read().decode("utf-8") if path.endswith(".gz") \
            else open(path, encoding="utf-8").read()
        return json.loads("[" + content + "]")
    except Exception:
        return []


def _walk(n):
    if isinstance(n, dict):
        yield n
        for v in n.values():
            yield from _walk(v)
    elif isinstance(n, list):
        for v in n:
            yield from _walk(v)


def shop_item_ids(pkt):
    for d in _walk(pkt):
        if isinstance(d, dict) and d.get("pick_up_item_info_array") is not None:
            return frozenset(it["item_id"] for it in d["pick_up_item_info_array"])
    return None


def main():
    files = []
    for g in LOG_GLOBS:
        files += glob.glob(g)

    # program_id -> [restocked?bool, ...]
    obs = defaultdict(list)
    for path in files:
        packets = load_packets(path)
        last_shop = None
        for i, o in enumerate(packets):
            if not isinstance(o, dict):
                continue
            s = shop_item_ids(o)
            if s is not None:
                last_shop = s
            if o.get("_direction") == 0 and "program_id" in o and "current_turn" in o:
                if last_shop is None:
                    continue
                grew = False
                for j in range(i + 1, min(len(packets), i + 1 + LOOKAHEAD)):
                    s2 = shop_item_ids(packets[j])
                    if s2 is not None and (s2 - last_shop):
                        grew = True
                        break
                obs[o["program_id"]].append(grew)

    restock = sorted(
        pid for pid, v in obs.items()
        if len(v) >= MIN_OBSERVATIONS and sum(v) / len(v) >= MIN_RESTOCK_RATE
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"restock_program_ids": restock}, f, separators=(",", ":"))

    print(f"files scanned:            {len(files)}")
    print(f"programs observed:        {len(obs)}")
    print(f"restock program_ids kept: {len(restock)}  (rate>={MIN_RESTOCK_RATE}, n>={MIN_OBSERVATIONS})")
    print(f"  {restock}")
    print(f"wrote {os.path.relpath(OUT)} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
