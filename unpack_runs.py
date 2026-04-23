"""Unpack all completed training runs (.gz) into CSVs.

Usage:
    python unpack_runs.py              # unpack all, skip existing CSVs
    python unpack_runs.py --force      # re-generate all CSVs
"""
import os
import sys
import glob

# Set Global env before importing anything from umalauncher
os.environ['IS_UL_GLOBAL'] = '1'

# Add umalauncher and its subdirs to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'umalauncher', 'external'))

from training_tracker import TrainingTracker, TrainingAnalyzer
import util

REGION = util.get_region_label()
LOG_DIR = os.path.join(os.path.dirname(__file__), 'umalauncher', 'appdata', REGION, 'training_logs')


def main():
    force = '--force' in sys.argv

    log_files = sorted(
        glob.glob(os.path.join(LOG_DIR, '*.gz')) + glob.glob(os.path.join(LOG_DIR, '*.json'))
    )
    if not log_files:
        print(f'No training logs found in {LOG_DIR}')
        return

    print(f'Found {len(log_files)} training run(s)\n')

    generated = 0
    skipped = 0
    failed = 0

    for log_path in log_files:
        base = log_path.rsplit('.', 1)[0]
        csv_path = base + '.csv'
        name = os.path.basename(base)

        if os.path.exists(csv_path) and not force:
            print(f'  SKIP  {name} (CSV exists)')
            skipped += 1
            continue

        try:
            tt = TrainingTracker('dummy', full_path=base)
            app = TrainingAnalyzer()
            app.set_training_tracker(tt)
            app.to_csv()
            generated += 1
            print(f'  OK    {name}')
        except Exception as e:
            failed += 1
            print(f'  FAIL  {name}: {e}')

    print(f'\nDone: {generated} generated, {skipped} skipped, {failed} failed')


if __name__ == '__main__':
    main()
