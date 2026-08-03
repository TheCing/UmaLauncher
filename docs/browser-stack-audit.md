# Browser stack audit (horsium.py + Selenium usage)

*2026-08-03. Grounded against installed selenium 4.38.0 source, selenium.dev docs,
geckodriver docs, Chrome DevTools blog, and Bugzilla. Line refs are to the code
as of commit `14adccd`.*

## Verdict

**Modernize in place; do not replace Selenium.** Playwright was evaluated and
rejected for this app (see §Alternatives): it cannot drive the user's installed
(branded) Firefox at all, offers no OS window-handle API (so all the win32
positioning code stays anyway), and bundling its Chromium adds ~150 MB to the
exe. Everything actually wrong with the current stack is fixable within
Selenium.

## Fact-checks that reframe the code

1. **`FirefoxProfile` is NOT deprecated** (common lore says otherwise; that
   deprecation was reverted after 4.0-beta). Only sub-APIs
   (`add_extension`, `port`, cert flags) are deprecated.
2. **`options.profile` clones the profile twice** — Python `copytree` to a temp
   dir, then base64-ZIP upload which geckodriver extracts to *another* temp
   dir. Nothing the browser writes ever reaches the real directory. The only
   in-place mechanism is the geckodriver CLI arg:
   `options.add_argument("-profile"); options.add_argument(path)`.
   The old caveat about `-profile` breaking Marionette's port was fixed in
   geckodriver 0.31.0.
3. **Chrome ≥136 ignores `--remote-debugging-port` on the default
   user-data-dir** (March 2025 security change). Non-default dir required.
4. `Service(creation_flags=...)` as a constructor kwarg is silently swallowed
   in 4.x — only the attribute assignment (what we do) or
   `popen_kw={"creation_flags": ...}` works.
5. `SE_GECKODRIVER`/`SE_CHROMEDRIVER` env vars silently override an explicit
   `executable_path` (service.py:77) — relevant to the browser-override
   feature.

## Findings

### P0 — architecture

**A1. Firefox profile persistence is fake.** `firefox_setup` builds a
"persistent" profile in appdata but passes it through `FirefoxProfile` →
`options.profile`, so Firefox runs against a throwaway copy (see fact-check 2).
Consequences: cookies/localStorage/gametora settings reset every session; the
mod4 user.js workaround was needed at all; the profile is zipped and uploaded
on every launch (startup cost grows with profile size).
*Fix:* use in-place `-profile` via `options.add_argument`. Complication: helper
and skills windows are two concurrent Firefox instances and cannot share one
profile in place (profile lock). Use per-window profile dirs
(`ff_profile_helper`, `ff_profile_skills`) seeded from the same base, or keep
the clone path for the rarely-used skills window only. Prefs then belong in
`user.js`/`set_preference` as today.

**A2. Dead remote-debugging machinery in `chromium_setup`** (horsium.py:124-159).
Port scan 9222-9229, `--remote-debugging-port`, per-port profile clones
(`chr_profile_p9222` accumulates in appdata). **No code in the repo connects to
the debug port.** It also has a TOCTOU race (port free at scan time, taken at
launch) and now intersects Chrome 136's restrictions. *Fix:* delete the port
scan and flag; keep a single per-browser profile dir. (Verify no external tool
depends on the port first.)

**A3. Dependency drift and duplicate venvs.** `requirements.txt` declares
`selenium~=4.45.0`; the running venv has **4.38.0**. Both `venv/` and `.venv/`
exist; the PyInstaller spec pulls `../.venv/...` while some tooling uses
`venv/`. *Fix:* one venv, `uv pip sync` against a lock, upgrade selenium to the
declared 4.45 line (changelog contains only additive BiDi work between 4.38 and
4.45 that touches nothing we use — retest the profile behavior after upgrade
anyway).

**A4. `--disable-web-security` (Chromium) / `security.fileuri.strict_origin_policy=false`
(Firefox) are broad CORS kill-switches** on profiles that browse the open web
(gametora + whatever links a user clicks). If the helper page genuinely needs
cross-origin access, scope it (serve the helper from the local Flask server and
use proper CORS headers there) rather than disabling web security globally.

### P1 — robustness

**B1. Driver lifecycle leak.** Replaced drivers go to `OLD_DRIVERS` and are only
`quit()` at app shutdown (`quit_all_drivers`), so failed/replaced sessions leave
`geckodriver.exe`/browser processes alive for the whole run. `ensure_tab_open`
also appends `None` after an inner `quit()`. *Fix:* quit the old driver on a
background thread at replacement time; drop the global list.

**B2. Homegrown navigation/wait.** `ensure_tab_open` navigates by injecting
`window.location = ...` and busy-polls `document.still_the_old_page_haha` /
`readyState` with `time.sleep(0.2)`. `driver.get()` already blocks until load;
`WebDriverWait` + `expected_conditions` covers the rest. Removes the marker
hack, the poll loops, and the "mental state" comment.

**B3. No timeouts anywhere.** No `set_page_load_timeout` / `set_script_timeout`.
A hung page or dead session blocks the packet-processing path (this session's
log shows `InvalidSessionIdException` escaping `update_helper_table` and popping
the "This should not happen" box). *Fix:* set both timeouts at driver creation;
catch `WebDriverException` at the `BrowserWindow` boundary and trigger relaunch
instead of letting it reach the msgpack error handler.

**B4. Thread safety.** `BrowserWindow.execute_script` is called from the
CarrotJuicer thread and tray/threader paths; WebDriver sessions are not
thread-safe. *Fix:* a per-window `threading.Lock` around driver access (or
funnel all browser work onto one executor thread).

**B5. `get_browser_pid` scans the entire process table twice** with cmdline
string matching. The driver already knows its child:
`driver.service.process.pid` → `psutil.Process(...).children()` (browser is the
child of chromedriver/msedgedriver). Firefox already uses `moz:processID`.

**B6. `geckodriver.log` written to CWD** (service default), worked around by
deleting it at startup (carrotjuicer.py:100-105). *Fix:*
`FirefoxService(log_output=...)` into appdata, or `subprocess.DEVNULL`.

### P2 — hygiene

- **C1.** Bare `except:` at horsium.py:269 and :303 swallow
  `KeyboardInterrupt`/everything; narrow to `WebDriverException`.
- **C2.** `raise Exception("Wrong window handle")` as control flow inside
  `ensure_tab_open`; restructure into explicit branches.
- **C3.** Deprecated/no-op Chrome flags: `disable-infobars` (dead since ~Chrome
  57), `useAutomationExtension` (removed). `excludeSwitches:["enable-automation"]`
  still valid.
- **C4.** Edge setup ignores `browser_custom_binary`/`browser_custom_driver`
  that Chrome honors (edge_setup passes neither).
- **C5.** `ensure_focus` is a plain function used as a decorator inside the
  class body — works, but should be a module-level helper or `@staticmethod`
  for clarity/tooling.
- **C6.** `urls_match` compares netloc+path only (query/fragment ignored) —
  fine, but deserves a docstring saying it's intentional.
- **C7.** On failure `ensure_focus` shows a blocking warning box from a worker
  thread after 3 full relaunch attempts; consider tray notification instead.

## Alternatives considered

**Playwright:** `launch_persistent_context` gives true in-place profiles (the
one thing Selenium makes hard), and PyInstaller bundling is supported
(`PLAYWRIGHT_BROWSERS_PATH=0`). But it **cannot drive branded Firefox** (only
its own patched build), so the current "user picks their installed browser"
feature dies for Firefox users; it has no window-handle API, so all win32
positioning code remains; bundled Chromium adds ~150 MB; its sync API is not
thread-safe either. Net: solves one P0 at the cost of a feature and a rewrite.

**WebDriver BiDi** (`options.enable_bidi = True`): W3C-standard events could
eventually replace JS polling, but Selenium docs still mark BiDi "in
development"; not a migration target yet. Revisit at ~4.50.

## Suggested sequencing

1. A3 (env/pins) — everything else should be tested on the real 4.45.
2. A2 (delete dead debug-port code) — pure removal, shrinks surface.
3. A1 (in-place Firefox profile) — the user-visible win (settings persist).
4. B1-B6 as one "robustness" pass.
5. C-items opportunistically with the above.
