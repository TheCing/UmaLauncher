"""Re-parse race JSON files whose SimDataBase64 failed to parse (v100000004+).

For each race log that has `_raceResult == {}` or horses with FinishOrder=-1,
re-decompress the embedded SimDataBase64 using the updated parser and fix:
  - Per-horse FinishOrder, FinishTimeRaw, FinishTimeScaled, FinishDiffTimeFromPrev, Defeat
  - Top-level ResultHorseIndex and HorseIndexByFinishOrder
  - File name (replaces "Unknown-0.0000s" / "race_unknown_*" with winner + time)

Run once:
    uv run python repair_unknown_races.py             # dry run
    uv run python repair_unknown_races.py --apply     # actually rewrite
"""
import os
import sys
import json
import glob
import argparse

os.environ.setdefault('IS_UL_GLOBAL', '1')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher', 'external'))

import race_data_parser

LOG_DIR = os.path.join(os.path.dirname(__file__), 'umalauncher', 'appdata', 'race_logs')
DEFEAT_LABELS = {0: "None", 1: "Speed", 2: "Stamina", 3: "Power", 4: "Guts", 5: "Wiz"}


def is_broken(data):
    """A race is 'broken' if the parser previously bailed — all horses have FinishOrder=-1."""
    horses = data.get('<RaceHorse>k__BackingField', [])
    if not horses:
        return False
    return all(h.get('FinishOrder', -1) == -1 for h in horses)


def repair_race(data):
    """Re-parse SimDataBase64 and patch the horse + race-level fields. Returns (winner_name, winner_time_raw) or None."""
    sim_b64 = data.get('<SimDataBase64>k__BackingField', '')
    if not sim_b64:
        return None

    sim = race_data_parser.parse(sim_b64)
    horses = data.get('<RaceHorse>k__BackingField', [])
    if not horses or len(sim.horse_result) != len(horses):
        return None

    # Collect activated skills per post position from SKILL events (type=3).
    activated_by_post = {}
    for wrapper in sim.event:
        ev = wrapper.event
        if ev.type != 3 or len(ev.param) < 2:
            continue
        activated_by_post.setdefault(ev.param[0], []).append({
            "skillId": ev.param[1],
            "frameTime": ev.frame_time,
        })

    # sim.horse_result is indexed by post position (frame_order - 1).
    # Each horse entry has a `postNumber` (= frame_order).
    for h in horses:
        post = h.get('postNumber', 0)
        idx = post - 1
        if idx < 0 or idx >= len(sim.horse_result):
            continue
        hr = sim.horse_result[idx]
        h['FinishOrder'] = hr.finish_order
        h['FinishTimeRaw'] = hr.finish_time_raw
        h['FinishTimeScaled'] = hr.finish_time
        h['FinishDiffTimeFromPrev'] = hr.finish_diff_time
        h['<Defeat>k__BackingField'] = DEFEAT_LABELS.get(hr.defeat, "None")
        skills = activated_by_post.get(idx)
        if skills:
            h['ActivatedSkills'] = skills

    # Winner = horse with FinishOrder == 0 (game uses 0-indexed finish order).
    winner = next((h for h in horses if h.get('FinishOrder') == 0), None)
    if winner is None:
        return None

    winner_idx = horses.index(winner)
    winner_name = winner.get('<charaName>k__BackingField', 'Unknown')
    winner_time_raw = winner.get('FinishTimeRaw', 0.0)

    # Rebuild HorseIndexByFinishOrder: horses sorted by FinishOrder
    sorted_by_finish = sorted(range(len(horses)), key=lambda i: horses[i].get('FinishOrder', 999))
    data['<HorseIndexByFinishOrder>k__BackingField'] = sorted_by_finish
    data['<ResultHorseIndex>k__BackingField'] = winner_idx

    return winner_name, winner_time_raw


def target_filename(old_path, winner_name, winner_time_raw):
    """Compute the correct filename — matches race_logger.save_race_packet."""
    # Strip the 8-digit date suffix from the old filename, preserve if present.
    old_base = os.path.basename(old_path)
    # Try to extract the date from either "Unknown-*-YYYYMMDD.json" or "race_unknown_YYYY_MM_DD_HH_MM_SS.json"
    import re
    m = re.search(r'(\d{8})\.json$', old_base)
    if m:
        date_str = m.group(1)
    else:
        m = re.search(r'(\d{4})_(\d{2})_(\d{2})', old_base)
        date_str = (m.group(1) + m.group(2) + m.group(3)) if m else '00000000'
    safe_name = winner_name.replace("/", "_").replace("\\", "_").replace(":", "_")
    return f"{safe_name}-{winner_time_raw:.4f}s-{date_str}.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='actually rewrite files (default: dry run)')
    args = parser.parse_args()

    candidates = sorted(
        glob.glob(os.path.join(LOG_DIR, 'Unknown-*.json'))
        + glob.glob(os.path.join(LOG_DIR, 'race_unknown_*.json'))
    )
    print(f"Found {len(candidates)} candidate file(s) in {LOG_DIR}")

    repaired = 0
    skipped = 0
    for old_path in candidates:
        with open(old_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not is_broken(data):
            print(f"  [skip, not broken] {os.path.basename(old_path)}")
            skipped += 1
            continue
        try:
            result = repair_race(data)
        except Exception as e:
            print(f"  [parse failed] {os.path.basename(old_path)}: {e}")
            skipped += 1
            continue
        if result is None:
            print(f"  [no result] {os.path.basename(old_path)}")
            skipped += 1
            continue
        winner_name, winner_time_raw = result
        new_name = target_filename(old_path, winner_name, winner_time_raw)
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        if args.apply:
            # Avoid clobbering an existing good file
            if os.path.exists(new_path) and new_path != old_path:
                print(f"  [target exists, skipping] {os.path.basename(old_path)} -> {new_name}")
                skipped += 1
                continue
            with open(old_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            if new_path != old_path:
                os.rename(old_path, new_path)
            print(f"  [repaired] {os.path.basename(old_path)} -> {new_name} (winner: {winner_name} @ {winner_time_raw:.4f}s)")
        else:
            print(f"  [would repair] {os.path.basename(old_path)} -> {new_name} (winner: {winner_name} @ {winner_time_raw:.4f}s)")
        repaired += 1

    print(f"\n{'Repaired' if args.apply else 'Would repair'}: {repaired}, skipped: {skipped}")
    if not args.apply:
        print("Re-run with --apply to actually rewrite files.")


if __name__ == '__main__':
    main()
