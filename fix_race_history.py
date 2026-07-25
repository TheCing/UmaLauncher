"""One-shot repair for existing race logs.

Earlier versions of race_logger.py indexed `sim.horse_result` by the horse's
input-array position instead of by `frame_order - 1`, so saved HorseACT JSONs
and the consolidated `race_results.csv` have the wrong finish order, time,
and defeat reason per horse.

This script:
  1. Reads every HorseACT-format JSON in `umalauncher/appdata/race_logs/`
  2. Remaps each horse's finish data by `frame_order - 1`
  3. Rewrites the JSON (winner index, horse_index_by_finish, and the filename
     are also corrected)
  4. Rebuilds `race_results.csv` from scratch using the corrected data

Run once:
    python fix_race_history.py                # dry run, reports changes
    python fix_race_history.py --apply        # actually rewrites files
    python fix_race_history.py --apply --include-raw   # also include raw
                                                       # packet files (old
                                                       # races will all get
                                                       # the current time as
                                                       # their timestamp)
"""
import os
import sys
import json
import glob
import csv

# Allow importing from umalauncher/ for reprocessing raw packet files
os.environ.setdefault('IS_UL_GLOBAL', '1')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher', 'external'))

LOG_DIR = os.path.join(os.path.dirname(__file__), 'umalauncher', 'appdata', 'race_logs')

RUNNING_STYLES = {1: "Nige", 2: "Senko", 3: "Sashi", 4: "Oikomi"}
APT_LABELS = {1: "G", 2: "F", 3: "E", 4: "D", 5: "C", 6: "B", 7: "A", 8: "S"}


def _apt(v):
    return APT_LABELS.get(v, str(v))


# Fields on each horse entry that were derived from horse_result and need remapping
RESULT_FIELDS = [
    "FinishOrder",
    "FinishTimeRaw",
    "FinishTimeScaled",
    "FinishDiffTimeFromPrev",
    "<Defeat>k__BackingField",
]


def remap_horses(horses):
    """Return a new list of horses with finish-result fields remapped by frame_order."""
    n = len(horses)
    # The current buggy value at index i = true result for frame_order (i+1).
    # So the true result for a horse with frame_order F = current value at index F-1.
    fixed = []
    for i, h in enumerate(horses):
        rhd = h.get('_responseHorseData', {}) or {}
        frame_order = rhd.get('frame_order', i + 1)
        src_idx = frame_order - 1
        if not (0 <= src_idx < n):
            src_idx = i
        src = horses[src_idx]
        new_h = dict(h)
        for fld in RESULT_FIELDS:
            if fld in src:
                new_h[fld] = src[fld]
        fixed.append(new_h)
    return fixed


def build_horse_index_by_finish(horses):
    n = len(horses)
    arr = [0] * n
    for i, h in enumerate(horses):
        fo = h.get("FinishOrder", -1)
        if isinstance(fo, int) and 0 <= fo < n:
            arr[fo] = i
    return arr


def find_winner(horses):
    for i, h in enumerate(horses):
        if h.get("FinishOrder") == 0:
            return i, h
    return 0, horses[0] if horses else None


def fix_json_file(path, apply):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if '<RaceHorse>k__BackingField' not in data:
        return None  # not a HorseACT file, skip

    horses = data.get('<RaceHorse>k__BackingField', [])
    if not horses:
        return None

    # Idempotency: skip re-fixing files already remapped
    already_fixed = data.get('_umalauncher_finish_order_remapped', False)
    if already_fixed:
        winner_idx, winner = find_winner(horses)
        winner_name = winner.get('<charaName>k__BackingField', 'Unknown') if winner else 'Unknown'
        return {
            'path': path,
            'new_path': path,
            'changed': False,
            'winner': winner_name,
            'data': data,
        }

    fixed = remap_horses(horses)

    # Detect if anything actually changed
    changed = any(
        any(h.get(f) != fh.get(f) for f in RESULT_FIELDS)
        for h, fh in zip(horses, fixed)
    )
    if not changed:
        # Still mark as fixed so we know it was checked
        data['_umalauncher_finish_order_remapped'] = True
        if apply:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        winner_idx, winner = find_winner(horses)
        winner_name = winner.get('<charaName>k__BackingField', 'Unknown') if winner else 'Unknown'
        return {
            'path': path,
            'new_path': path,
            'changed': False,
            'winner': winner_name,
            'data': data,
        }

    data['<RaceHorse>k__BackingField'] = fixed
    data['_umalauncher_finish_order_remapped'] = True

    # Also update the player team array (it holds a reference list of horses
    # mirrored by horseIndex)
    player_arr = data.get('<PlayerTeamMemberArray>k__BackingField', [])
    if player_arr:
        idx_map = {h.get('horseIndex'): h for h in fixed}
        new_player = []
        for ph in player_arr:
            hi = ph.get('horseIndex')
            if hi in idx_map:
                merged = dict(ph)
                for fld in RESULT_FIELDS:
                    if fld in idx_map[hi]:
                        merged[fld] = idx_map[hi][fld]
                new_player.append(merged)
            else:
                new_player.append(ph)
        data['<PlayerTeamMemberArray>k__BackingField'] = new_player

    # Winner index + horse_index_by_finish
    winner_idx, winner = find_winner(fixed)
    data['<ResultHorseIndex>k__BackingField'] = winner_idx
    data['<HorseIndexByFinishOrder>k__BackingField'] = build_horse_index_by_finish(fixed)

    # Filename: WinnerName-FinishTimeRaw-YYYYMMDD.json
    winner_name = winner.get('<charaName>k__BackingField', 'Unknown') if winner else 'Unknown'
    winner_time = winner.get('FinishTimeRaw', 0.0) if winner else 0.0
    old_filename = os.path.basename(path)
    # Extract date from old filename (last segment before .json)
    stem = old_filename[:-5] if old_filename.endswith('.json') else old_filename
    parts = stem.rsplit('-', 1)
    date_str = parts[1] if len(parts) == 2 else '00000000'
    safe_name = winner_name.replace('/', '_').replace('\\', '_').replace(':', '_')
    new_filename = f"{safe_name}-{winner_time:.4f}s-{date_str}.json"
    new_path = os.path.join(os.path.dirname(path), new_filename)

    if apply:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        if new_filename != old_filename and not os.path.exists(new_path):
            os.rename(path, new_path)

    return {
        'path': path,
        'new_path': new_path,
        'changed': True,
        'winner': winner_name,
        'data': data,
    }


def row_from_horse(h, metadata):
    rhd = h.get('_responseHorseData', {}) or {}
    tc = h.get('<TrainedCharaData>k__BackingField', {}) or {}
    skills = [s.get('name', str(s.get('id', ''))) for s in (h.get('_skills', []) or [])]
    # Skills might be under _responseHorseData.skill_array
    if not skills:
        skill_array = rhd.get('skill_array', [])
        skills = [str(s.get('skill_id', '')) for s in skill_array]

    running_style = h.get('<RunningType>k__BackingField') or RUNNING_STYLES.get(rhd.get('running_style', 0), '')
    if running_style in ('Base', 'None', ''):
        running_style = RUNNING_STYLES.get(rhd.get('running_style', 0), '')

    fo = h.get('FinishOrder', -1)
    finish_order = fo + 1 if isinstance(fo, int) and fo >= 0 else ''
    finish_time = h.get('FinishTimeScaled', 0)
    finish_time_str = f"{finish_time:.2f}" if finish_time else ''

    return {
        'timestamp': metadata.get('timestamp', ''),
        'race_start_time': metadata.get('race_start_time', ''),
        'room_name': metadata.get('room_name', ''),
        'room_id': metadata.get('room_id', ''),
        'race_instance_id': metadata.get('race_instance_id', ''),
        'entry_count': metadata.get('entry_count', ''),
        'weather': metadata.get('weather', ''),
        'ground_condition': metadata.get('ground_condition', ''),
        'season': metadata.get('season', ''),
        'finish_order': finish_order,
        'finish_time': finish_time_str,
        'last_spurt_dist': '',
        'trainer_name': h.get('<TrainerName>k__BackingField', rhd.get('trainer_name', '')),
        'viewer_id': rhd.get('viewer_id') or rhd.get('owner_viewer_id', ''),
        'chara_name': h.get('<charaName>k__BackingField', ''),
        'chara_id': rhd.get('chara_id', h.get('charaId', 0)),
        'card_id': rhd.get('card_id', 0),
        'running_style': running_style,
        'speed': rhd.get('speed', 0),
        'stamina': rhd.get('stamina', 0),
        'power': rhd.get('pow', 0),
        'guts': rhd.get('guts', 0),
        'wisdom': rhd.get('wiz', 0),
        'final_grade': rhd.get('final_grade', ''),
        'rank_score': tc.get('<RankScore>k__BackingField', ''),
        'scenario_id': tc.get('<ScenarioId>k__BackingField', ''),
        'fans': tc.get('<Fans>k__BackingField', ''),
        'wins': tc.get('<WinsCount>k__BackingField', ''),
        'turf': _apt(rhd.get('proper_ground_turf', 0)),
        'dirt': _apt(rhd.get('proper_ground_dirt', 0)),
        'short': _apt(rhd.get('proper_distance_short', 0)),
        'mile': _apt(rhd.get('proper_distance_mile', 0)),
        'mid': _apt(rhd.get('proper_distance_middle', 0)),
        'long': _apt(rhd.get('proper_distance_long', 0)),
        'nige': _apt(rhd.get('proper_running_style_nige', 0)),
        'senko': _apt(rhd.get('proper_running_style_senko', 0)),
        'sashi': _apt(rhd.get('proper_running_style_sashi', 0)),
        'oikomi': _apt(rhd.get('proper_running_style_oikomi', 0)),
        'skills': ' | '.join(str(s) for s in skills if s),
    }


def _synthetic_timestamp(filename, ordinal_within_day):
    """Build a synthetic timestamp for a race file.

    Filenames look like 'WinnerName-96.0775s-20260409.json'. We extract the
    YYYYMMDD date and use the file's ordinal within that date to build a
    unique HH:MM:SS suffix so every race gets a distinct, sortable timestamp.
    (The original timestamps were lost when this fix script rewrote mtimes.)
    """
    import re
    stem = filename[:-5] if filename.endswith('.json') else filename
    m = re.search(r'(\d{8})$', stem)
    if not m:
        return ''
    date_str = m.group(1)
    # Format as YYYY-MM-DD HH:MM:SS with ordinal spread across the day
    # (ordinal_within_day * 60 seconds -> spaced 1 minute apart, scales to
    # ~1440 races per day)
    total_seconds = ordinal_within_day * 60
    hh = (total_seconds // 3600) % 24
    mm = (total_seconds // 60) % 60
    ss = total_seconds % 60
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} {hh:02d}:{mm:02d}:{ss:02d}"


def rebuild_csv(results, apply, append=False):
    """Rebuild race_results.csv from fixed HorseACT data.

    If append=True, open the CSV in append mode and only write the header
    when the file is empty (so rows from raw-packet reprocessing stay).
    """
    # Sort results by filename so ordinals are stable, then assign an
    # ordinal within each YYYYMMDD date
    import re
    from collections import defaultdict
    date_ordinals = defaultdict(int)
    sorted_results = sorted(results, key=lambda r: os.path.basename(r['path']))

    rows = []
    for r in sorted_results:
        data = r['data']
        horses = data.get('<RaceHorse>k__BackingField', [])
        race_result = data.get('_raceResult', {}) or {}
        filename = os.path.basename(r['path'])
        m = re.search(r'(\d{8})', filename)
        date_key = m.group(1) if m else 'unknown'
        ordinal = date_ordinals[date_key]
        date_ordinals[date_key] += 1

        metadata = {
            'timestamp': _synthetic_timestamp(filename, ordinal),
            'race_start_time': race_result.get('start_time', ''),
            'room_name': race_result.get('room_name', ''),
            'room_id': race_result.get('room_id', ''),
            'race_instance_id': race_result.get('race_instance_id', ''),
            'entry_count': race_result.get('entry_num', len(horses)),
            'weather': data.get('_weather', ''),
            'ground_condition': data.get('_groundCondition', ''),
            'season': data.get('_season', ''),
        }

        sorted_horses = sorted(horses, key=lambda h: h.get('FinishOrder', 99))
        for h in sorted_horses:
            rows.append(row_from_horse(h, metadata))

    if not rows:
        print("No rows to write.")
        return

    csv_path = os.path.join(LOG_DIR, 'race_results.csv')
    fieldnames = list(rows[0].keys())
    if apply:
        mode = 'a' if append else 'w'
        file_has_content = append and os.path.exists(csv_path) and os.path.getsize(csv_path) > 0
        with open(csv_path, mode, newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_has_content:
                writer.writeheader()
            writer.writerows(rows)
        print(f"{'Appended' if append else 'Wrote'} {len(rows)} HorseACT-derived rows to {csv_path}")
    else:
        print(f"Would {'append' if append else 'write'} {len(rows)} HorseACT-derived rows to {csv_path}")


def classify_files(json_files):
    """Split files into HorseACT-format, raw-packet, and other."""
    horseact, raw, other = [], [], []
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            other.append(jf)
            continue
        if '<RaceHorse>k__BackingField' in data:
            horseact.append(jf)
        elif 'race_horse_data_array' in data and 'race_scenario' in data:
            raw.append(jf)
        else:
            other.append(jf)
    return horseact, raw, other


def reprocess_raw_packets(files, apply):
    """Run the (now-fixed) log_race() on each raw packet file.

    Monkey-patches race_logger's timestamp generator so each race keeps a
    unique timestamp derived from the file's mtime (otherwise they'd all
    collide on the current time and the viewer would merge them).
    """
    if not files:
        return 0
    if not apply:
        print(f"\nWould reprocess {len(files)} raw packet file(s) via race_logger.log_race")
        return len(files)

    import race_logger  # imported late so dry runs don't need umalauncher deps
    import time as _time
    real_strftime = _time.strftime
    current_ts_holder = {'value': None}

    def patched_strftime(fmt, *args):
        if fmt == '%Y-%m-%d %H:%M:%S' and current_ts_holder['value']:
            return current_ts_holder['value']
        return real_strftime(fmt, *args)

    ok = 0
    for jf in files:
        try:
            mt = os.path.getmtime(jf)
            current_ts_holder['value'] = _time.strftime('%Y-%m-%d %H:%M:%S', _time.localtime(mt))
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Patch time.strftime in race_logger's module namespace
            race_logger.time.strftime = patched_strftime
            try:
                race_logger.log_race(data)
            finally:
                race_logger.time.strftime = real_strftime
            ok += 1
            print(f"  [RAW] {os.path.basename(jf)} reprocessed (ts={current_ts_holder['value']})")
        except Exception as e:
            print(f"  [ERR] {os.path.basename(jf)}: {e}")
    return ok


def main():
    apply = '--apply' in sys.argv
    include_raw = '--include-raw' in sys.argv
    json_files = sorted(glob.glob(os.path.join(LOG_DIR, '*.json')))
    if not json_files:
        print(f"No JSON files found in {LOG_DIR}")
        return

    horseact_files, raw_files, other_files = classify_files(json_files)
    print(f"Found {len(horseact_files)} HorseACT, {len(raw_files)} raw-packet, "
          f"{len(other_files)} other JSON file(s)\n")

    # Step 1: remap HorseACT JSONs in place
    results = []
    changed = 0
    for jf in horseact_files:
        try:
            r = fix_json_file(jf, apply)
            if r is None:
                continue
            if r['changed']:
                changed += 1
                print(f"  [FIX] {os.path.basename(jf)} -> winner: {r['winner']}")
            results.append(r)
        except Exception as e:
            print(f"  [ERR] {os.path.basename(jf)}: {e}")
    print(f"\n{changed} HorseACT file(s) remapped\n")

    # Step 2: delete old CSV so we can rebuild cleanly
    csv_path = os.path.join(LOG_DIR, 'race_results.csv')
    if apply and os.path.exists(csv_path):
        os.remove(csv_path)
        print(f"Removed old {csv_path}\n")

    # Step 3: reprocess raw packet files via the now-fixed log_race
    # (this creates the CSV header row)
    if include_raw:
        reprocess_raw_packets(raw_files, apply)
    elif raw_files:
        print(f"Skipping {len(raw_files)} raw packet file(s). "
              f"Re-run with --include-raw to include them.")

    # Step 4: append fixed HorseACT rows to the CSV
    if results:
        rebuild_csv(results, apply, append=(include_raw and bool(raw_files)))

    if not apply:
        print("\nDry run. Re-run with --apply to actually write files.")


if __name__ == '__main__':
    main()
