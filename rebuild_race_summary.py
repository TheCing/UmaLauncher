"""Rebuild race_summary.json from every race JSON under appdata/race_logs/.

Run after adding the summary feature to seed the dashboard with historical
data, or whenever the schema changes and you want a clean slate.

    uv run python rebuild_race_summary.py          # dry run
    uv run python rebuild_race_summary.py --apply  # actually rewrite
"""
import os
import sys
import json
import glob
import argparse
import base64

os.environ.setdefault('IS_UL_GLOBAL', '1')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher', 'external'))

import race_data_parser
import race_logger
import util

REGION = util.get_region_label()
LOG_DIR = os.path.join(os.path.dirname(__file__), 'umalauncher', 'appdata', REGION, 'race_logs')


class FakeFinish:
    """Shim so _apply_race_to_summary can read .finish_order off horse data."""
    def __init__(self, finish_order):
        self.finish_order = finish_order


def _horse_data_for_summary(horse_entry):
    """Flatten the HorseACT-format horse back into the packet-style dict the summary expects."""
    rhd = horse_entry.get('_responseHorseData') or {}
    return {
        'frame_order': horse_entry.get('postNumber', 0),
        'viewer_id': rhd.get('viewer_id', 0) or rhd.get('owner_viewer_id', 0),
        'owner_viewer_id': rhd.get('owner_viewer_id', 0),
        'trained_chara_id': rhd.get('trained_chara_id', 0),
        'card_id': rhd.get('card_id', 0),
        'chara_id': horse_entry.get('charaId', 0),
        'speed': rhd.get('speed', 0),
        'stamina': rhd.get('stamina', 0),
        'pow': rhd.get('pow', 0),
        'guts': rhd.get('guts', 0),
        'wiz': rhd.get('wiz', 0),
        'running_style': rhd.get('running_style', 0),
        'rank_score': horse_entry.get('<TrainedCharaData>k__BackingField', {}).get('<rankScore>k__BackingField', 0),
        'trainer_name': horse_entry.get('<TrainerName>k__BackingField', ''),
    }


def rebuild(apply: bool):
    summary = {
        'schema_version': race_logger.RACE_SUMMARY_SCHEMA_VERSION,
        'umas': {},
    }
    chara_names = util.get_character_name_dict()

    paths = sorted(glob.glob(os.path.join(LOG_DIR, '**', '*.json'), recursive=True))
    # Skip summary file itself
    paths = [p for p in paths if os.path.basename(p) != race_logger.RACE_SUMMARY_FILENAME]
    print(f'Scanning {len(paths)} race JSON file(s)...')

    processed = 0
    skipped = 0
    for path in paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f'  [skip, unreadable] {os.path.relpath(path, LOG_DIR)}: {e}')
            skipped += 1
            continue

        horses_json = data.get('<RaceHorse>k__BackingField', [])
        if not horses_json:
            skipped += 1
            continue

        # Build packet-style horse dicts + finish_data from the saved JSON
        horses = []
        finish_data = {}
        activated_by_post = {}
        for h_entry in horses_json:
            h = _horse_data_for_summary(h_entry)
            horses.append(h)
            finish_order = h_entry.get('FinishOrder', -1)
            if finish_order >= 0:
                finish_data[h['frame_order'] - 1] = FakeFinish(finish_order)
            # Reuse stored ActivatedSkills if present (already backfilled)
            for s in h_entry.get('ActivatedSkills', []) or []:
                activated_by_post.setdefault(h['frame_order'] - 1, []).append(s)

        # If a file is still broken (no finish data), skip it — the summary
        # would show zero wins/races which isn't useful.
        if not finish_data:
            skipped += 1
            continue

        race_type = data.get('<RaceType>k__BackingField', 'Unknown')
        race_instance_id = (data.get('_raceResult') or {}).get('race_instance_id', 0)
        race_id = os.path.relpath(path, LOG_DIR).replace('\\', '/')

        # Determine owner viewer id from the player team
        owner_viewer_id = 0
        player_array = data.get('<PlayerTeamMemberArray>k__BackingField') or []
        if player_array:
            idx = player_array[0].get('horseIndex') if isinstance(player_array[0], dict) else None
            if isinstance(idx, int) and 0 <= idx < len(horses):
                owner_viewer_id = horses[idx].get('viewer_id', 0) or 0

        race_logger._apply_race_to_summary(
            summary, race_id, race_type, race_instance_id,
            horses, finish_data, activated_by_post,
            owner_viewer_id, chara_names,
        )
        processed += 1

    print(f'Processed {processed}, skipped {skipped}')
    print(f'Umas tracked: {len(summary["umas"])}')

    summary_path = os.path.join(LOG_DIR, race_logger.RACE_SUMMARY_FILENAME)
    if apply:
        race_logger._save_race_summary(summary_path, summary)
        print(f'Wrote {summary_path}')
    else:
        print(f'Would write {summary_path}')
        print('Re-run with --apply to actually write the summary.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='actually write race_summary.json')
    args = parser.parse_args()
    rebuild(args.apply)


if __name__ == '__main__':
    main()
