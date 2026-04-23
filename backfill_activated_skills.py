"""Backfill ActivatedSkills into existing race JSON files.

Older race logs (saved before activated-skills extraction was added) have
full finish data but no per-horse ActivatedSkills arrays. This script
re-parses the embedded SimDataBase64 and adds ActivatedSkills to each
horse entry, leaving everything else untouched.

Run:
    uv run python backfill_activated_skills.py          # dry run
    uv run python backfill_activated_skills.py --apply  # actually rewrite
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


def backfill_one(data):
    """Add ActivatedSkills to each horse. Returns True if something changed."""
    sim_b64 = data.get('<SimDataBase64>k__BackingField', '')
    horses = data.get('<RaceHorse>k__BackingField', [])
    if not sim_b64 or not horses:
        return False

    # Skip if every horse already has ActivatedSkills populated
    if all('ActivatedSkills' in h for h in horses):
        return False

    try:
        sim = race_data_parser.parse(sim_b64)
    except Exception:
        return False

    activated_by_post = {}
    for wrapper in sim.event:
        ev = wrapper.event
        if ev.type != 3 or len(ev.param) < 2:
            continue
        activated_by_post.setdefault(ev.param[0], []).append({
            "skillId": ev.param[1],
            "frameTime": ev.frame_time,
        })

    changed = False
    for h in horses:
        if 'ActivatedSkills' in h:
            continue
        post = h.get('postNumber', 0)
        skills = activated_by_post.get(post - 1)
        if skills:
            h['ActivatedSkills'] = skills
            changed = True
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='actually rewrite files (default: dry run)')
    args = parser.parse_args()

    # Recurse into subfolders (Room match/, Champions meeting/, etc.)
    candidates = sorted(glob.glob(os.path.join(LOG_DIR, '**', '*.json'), recursive=True))
    print(f"Found {len(candidates)} race JSON file(s) under {LOG_DIR}")

    updated = 0
    skipped = 0
    failed = 0
    for path in candidates:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  [read failed] {os.path.relpath(path, LOG_DIR)}: {e}")
            failed += 1
            continue

        try:
            changed = backfill_one(data)
        except Exception as e:
            print(f"  [parse failed] {os.path.relpath(path, LOG_DIR)}: {e}")
            failed += 1
            continue

        if not changed:
            skipped += 1
            continue

        if args.apply:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  [updated] {os.path.relpath(path, LOG_DIR)}")
        else:
            print(f"  [would update] {os.path.relpath(path, LOG_DIR)}")
        updated += 1

    print(f"\n{'Updated' if args.apply else 'Would update'}: {updated}, already had skills: {skipped}, failed: {failed}")
    if not args.apply:
        print("Re-run with --apply to actually rewrite files.")


if __name__ == '__main__':
    main()
