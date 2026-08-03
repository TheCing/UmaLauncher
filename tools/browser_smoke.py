"""Launch the helper browser exactly the way UmaLauncher does, without UmaLauncher.

Imports the real horsium module and calls the real per-browser setup functions
with the settings from appdata/umasettings.json, so what this script does is
what the app does - same profile dirs, same prefs, same flags, same driver
logs. The one intentional difference: the launcher relaunches itself elevated
(util.elevate), this script runs at whatever elevation you started it with.
The elevation status is printed so that difference is never invisible.

Usage (from the repo root):
    uv run python tools/browser_smoke.py                  # browser from settings
    uv run python tools/browser_smoke.py --browser Chrome # override
    uv run python tools/browser_smoke.py --hold 15        # keep window open 15s

To test the launcher's real elevation context, run the same command from an
Administrator terminal.
"""
import argparse
import ctypes
import json
import os
import sys
import time
import traceback

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PKG = os.path.join(REPO, "umalauncher")

# util resolves appdata from the CWD at import time (script mode), so this must
# happen before any app import to hit the real umalauncher/appdata.
os.chdir(PKG)
sys.path.insert(0, PKG)

import horsium  # noqa: E402

HELPER_URL = "https://gametora.com/umamusume/training-event-helper"

# Keys the setup functions read, with safe fallbacks for older settings files.
SETTINGS_DEFAULTS = {
    "enable_browser_override": False,
    "browser_custom_binary": "",
    "browser_custom_driver": "",
    "browser_version": None,
    "adblock_enabled": True,
    "selected_browser": {"Auto": True, "Chrome": False, "Firefox": False, "Edge": False},
}

DRIVER_LOGS = {
    "Firefox": "geckodriver.log",
    "Chrome": "chromedriver.log",
    "Edge": "edgedriver.log",
}


def load_settings():
    path = os.path.join(PKG, "appdata", "umasettings.json")
    settings = dict(SETTINGS_DEFAULTS)
    try:
        with open(path, encoding="utf-8") as f:
            settings.update(json.load(f))
        print(f"settings: {path}")
    except OSError:
        print(f"settings: {path} not found, using defaults")
    return settings


def selected_browser_name(settings):
    return next((name for name, on in settings["selected_browser"].items() if on), "Auto")


def tail_driver_log(browser_name, since_mtime):
    log_path = os.path.join(PKG, "appdata", DRIVER_LOGS[browser_name])
    if not os.path.exists(log_path) or os.path.getmtime(log_path) < since_mtime:
        print(f"  (no fresh {DRIVER_LOGS[browser_name]})")
        return
    lines = [l.rstrip() for l in open(log_path, encoding="utf-8", errors="replace")]
    interesting = [l for l in lines if any(
        k in l.lower() for k in ("launching", "command:", "error", "fail", "crash",
                                 "exited", "denied", "cannot", "sandbox"))]
    print(f"  --- {DRIVER_LOGS[browser_name]} (filtered, last 15) ---")
    for l in interesting[-15:]:
        print("   ", l[:200])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", choices=["Firefox", "Chrome", "Edge"],
                        help="Override the browser from settings")
    parser.add_argument("--hold", type=int, default=0,
                        help="Seconds to keep the window open before quitting")
    parser.add_argument("--window", action="store_true",
                        help="Go through the real BrowserWindow layer (applies the saved "
                             "browser_position rect) instead of the bare setup function. "
                             "Gametora page setup (dark mode, overlay) still needs the launcher.")
    args = parser.parse_args()

    elevated = bool(ctypes.windll.shell32.IsUserAnAdmin())
    print(f"elevated: {elevated}   (the launcher itself ALWAYS runs elevated)")

    settings = load_settings()
    browser_name = args.browser or selected_browser_name(settings)
    if browser_name == "Auto":
        browser_name = "Firefox"

    if args.browser:
        # BrowserWindow picks the browser from settings; honor the override.
        settings["selected_browser"] = {n: (n == browser_name)
                                        for n in ("Auto", "Chrome", "Firefox", "Edge")}
        settings["enable_browser_override"] = False

    if args.window:
        return run_window_mode(settings, browser_name, args.hold)

    setup = horsium.BROWSER_LIST[browser_name]
    print(f"browser:  {browser_name}  ->  {setup.__name__}")
    print(f"url:      {HELPER_URL}\n")

    start = time.time()
    try:
        driver = setup(HELPER_URL, settings)
    except Exception:
        print(f"LAUNCH FAILED after {time.time() - start:.1f}s:\n")
        print(traceback.format_exc())
        tail_driver_log(browser_name, start)
        return 1

    try:
        print(f"LAUNCH OK in {time.time() - start:.1f}s")
        print(f"  handles: {driver.window_handles}")
        print(f"  url:     {driver.current_url[:80]}")
        if args.hold:
            print(f"  holding window open {args.hold}s...")
            time.sleep(args.hold)
    finally:
        driver.quit()
    return 0


class _FakeThreader:
    """Just enough threader for BrowserWindow: it only reads .settings."""
    def __init__(self, settings):
        self.settings = settings


def run_window_mode(settings, browser_name, hold):
    rect = settings.get("browser_position") or [100, 100, 600, 900]
    print(f"browser:  {browser_name} (via BrowserWindow)")
    print(f"rect:     {rect}  (from browser_position setting)")
    print(f"url:      {HELPER_URL}\n")

    start = time.time()
    bw = horsium.BrowserWindow(HELPER_URL, _FakeThreader(settings), rect=rect)
    try:
        if not bw.alive():
            print(f"WINDOW FAILED after {time.time() - start:.1f}s "
                  f"(latest error: {bw.latest_error.strip() or 'none recorded'})")
            tail_driver_log(bw.browser_name, start)
            return 1
        applied = bw.get_window_rect()
        print(f"WINDOW OK in {time.time() - start:.1f}s  (browser: {bw.browser_name})")
        print(f"  requested rect: x={rect[0]} y={rect[1]} w={rect[2]} h={rect[3]}")
        print(f"  applied rect:   x={applied['x']} y={applied['y']} "
              f"w={applied['width']} h={applied['height']}")
        matches = (abs(applied['x'] - rect[0]) <= 16 and abs(applied['y'] - rect[1]) <= 16
                   and abs(applied['width'] - rect[2]) <= 16 and abs(applied['height'] - rect[3]) <= 16)
        print(f"  rect applied:   {'YES' if matches else 'NO (off by more than 16px)'}")
        if hold:
            print(f"  holding window open {hold}s...")
            time.sleep(hold)
        return 0 if matches else 1
    finally:
        bw.quit()
        horsium.quit_all_drivers()


if __name__ == "__main__":
    sys.exit(main())
