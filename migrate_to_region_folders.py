"""One-shot migration: move existing race_logs and training_logs under a region subfolder.

Before: appdata/race_logs/<files>  and  appdata/training_logs/<files>
After:  appdata/{GL|JP}/race_logs/<files>  and  appdata/{GL|JP}/training_logs/<files>

Pass --region GL or --region JP to pick the destination. Defaults to the
region the current environment would use (GL if IS_UL_GLOBAL is set).

    uv run python migrate_to_region_folders.py                       # dry run, auto region
    uv run python migrate_to_region_folders.py --apply               # move files
    uv run python migrate_to_region_folders.py --region JP --apply   # move to JP instead
"""
import os
import sys
import argparse
import shutil

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ.setdefault('IS_UL_GLOBAL', '1')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher', 'external'))

import util

APPDATA = os.path.join(os.path.dirname(__file__), 'umalauncher', 'appdata')


def migrate_folder(subfolder, region, apply):
    src = os.path.join(APPDATA, subfolder)
    dst = os.path.join(APPDATA, region, subfolder)
    if not os.path.isdir(src):
        print(f'  [skip] {subfolder}/ does not exist')
        return 0

    moved = 0
    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        # Don't re-migrate the region folder itself if it somehow lives here
        if entry in ('GL', 'JP') and os.path.isdir(src_path):
            continue
        dst_path = os.path.join(dst, entry)
        if os.path.exists(dst_path):
            print(f'  [exists, skipping] {subfolder}/{entry}')
            continue
        if apply:
            os.makedirs(dst, exist_ok=True)
            shutil.move(src_path, dst_path)
            print(f'  [moved] {subfolder}/{entry} -> {region}/{subfolder}/{entry}')
        else:
            print(f'  [would move] {subfolder}/{entry} -> {region}/{subfolder}/{entry}')
        moved += 1
    return moved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', choices=['GL', 'JP'], default=util.get_region_label(),
                        help="Which region bucket to move existing logs into (default: current env's region)")
    parser.add_argument('--apply', action='store_true', help='actually move files')
    args = parser.parse_args()

    print(f'Migrating existing appdata into region: {args.region}')
    total = 0
    for sub in ('race_logs', 'training_logs'):
        total += migrate_folder(sub, args.region, args.apply)
    print(f"\n{'Moved' if args.apply else 'Would move'}: {total} item(s)")
    if not args.apply:
        print('Re-run with --apply to actually move files.')


if __name__ == '__main__':
    main()
