"""Pull CM presets + skill conditions + course specs from the local
TheCing/uma-tools clone and bundle slim JSONs into _assets/.

Run after pulling new data into uma-tools (e.g. when a new CM preset gets
added) to refresh the bundled lookup tables. Idempotent — safe to re-run.

Usage:
    uv run python tools/refresh_race_filter_data.py
"""
import os
import re
import sys
import json

UMA_TOOLS = os.path.expandvars(r"C:\Users\jptyn\Dev\uma-tools")
ASSETS = os.path.join(os.path.dirname(__file__), "..", "umalauncher", "_assets")


def _emit(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    print(f"  wrote {os.path.relpath(path)} ({os.path.getsize(path):,} bytes)")


# ----- Course conditions ----------------------------------------------------

def extract_courses():
    src = os.path.join(UMA_TOOLS, "uma-skill-tools", "data", "course_data.json")
    with open(src, "r", encoding="utf-8") as f:
        courses = json.load(f)
    # Slim: course_id -> { track_id, distance, distance_type, surface, turn }
    out = {}
    for cid, c in courses.items():
        out[cid] = {
            "track_id": c["raceTrackId"],
            "distance": c["distance"],
            "distance_type": c["distanceType"],
            "surface": c["surface"],
            "turn": c["turn"],
        }
    _emit(os.path.join(ASSETS, "course_specs.json"), out)


# ----- Skill conditions ------------------------------------------------------

# Condition keys that meaningfully constrain race conditions. Anything else
# (running_style, phase, order_rate, etc.) is in-race tactical and irrelevant
# to "is this skill applicable to my race?".
RACE_CONDITION_KEYS = {
    "track_id",
    "ground_type",      # 1=turf, 2=dirt
    "ground_condition", # 1=firm, 2=yielding, 3=soft, 4=heavy
    "distance_type",    # 1=sprint, 2=mile, 3=medium, 4=long
    "course_distance",  # specific distance (==/>=/<=)
    "rotation",         # 1=right-handed, 2=left-handed, 4=straight
    "weather",          # 1=sunny, 2=cloudy, 3=rainy, 4=snowy
    "season",           # 1=spring, 2=summer, 3=autumn, 4=winter, 5=sakura
}


def parse_skill_constraints(condition_str: str):
    """Pull the set of allowed values per RACE_CONDITION_KEYS from a single
    condition expression. Lossy on cross-field OR (e.g. `track_id==X|weather==Y`
    would be parsed as both "must be track X" AND "must be weather Y" instead
    of the actual OR — but those are rare enough to accept the false-rejection
    in practice)."""
    out = {}
    if not condition_str:
        return out
    # First split on `|` to get OR alternatives, then `&` for AND clauses.
    # We pool ==/!= equalities per-field across all alternatives, treating
    # them as the union (OR) for that field.
    for alternative in condition_str.split("|"):
        for clause in alternative.split("&"):
            m = re.match(r"^\s*([a-z_]+)\s*(==|!=|<=|>=|<|>)\s*(\d+)\s*$", clause)
            if not m:
                continue
            key, op, val = m.group(1), m.group(2), int(m.group(3))
            if key not in RACE_CONDITION_KEYS:
                continue
            bucket = out.setdefault(key, {"eq": set(), "neq": set(), "lt": None, "le": None, "gt": None, "ge": None})
            if op == "==":
                bucket["eq"].add(val)
            elif op == "!=":
                bucket["neq"].add(val)
            elif op == "<":
                bucket["lt"] = val if bucket["lt"] is None else min(bucket["lt"], val)
            elif op == "<=":
                bucket["le"] = val if bucket["le"] is None else min(bucket["le"], val)
            elif op == ">":
                bucket["gt"] = val if bucket["gt"] is None else max(bucket["gt"], val)
            elif op == ">=":
                bucket["ge"] = val if bucket["ge"] is None else max(bucket["ge"], val)
    # Convert sets to sorted lists for JSON.
    return {
        k: {kk: (sorted(vv) if isinstance(vv, set) else vv) for kk, vv in v.items() if (vv if not isinstance(vv, set) else len(vv) > 0)}
        for k, v in out.items()
    }


def extract_skills():
    src = os.path.join(UMA_TOOLS, "uma-skill-tools", "data", "skill_data.json")
    with open(src, "r", encoding="utf-8") as f:
        skills = json.load(f)
    out = {}
    for sid, s in skills.items():
        merged = {}
        for alt in s.get("alternatives", []):
            cond_pool = (alt.get("condition", "") or "") + "&" + (alt.get("precondition", "") or "")
            cs = parse_skill_constraints(cond_pool)
            # Merge across alternatives (OR'd at skill level — if any alternative
            # passes, the skill is applicable).
            for k, v in cs.items():
                bucket = merged.setdefault(k, {})
                for kk, vv in v.items():
                    if isinstance(vv, list):
                        bucket[kk] = sorted(set(bucket.get(kk, [])) | set(vv))
                    elif kk in ("lt", "le"):
                        bucket[kk] = vv if kk not in bucket else min(bucket[kk], vv)
                    elif kk in ("gt", "ge"):
                        bucket[kk] = vv if kk not in bucket else max(bucket[kk], vv)
        if merged:
            out[sid] = merged
    _emit(os.path.join(ASSETS, "skill_race_constraints.json"), out)


# ----- CM presets ------------------------------------------------------------

# A simple TS literal parser scoped to the presets array — uses regex extraction
# rather than a real parser, brittle but adequate for the limited shape used.

def extract_cm_presets():
    src = os.path.join(UMA_TOOLS, "umalator", "app.tsx")
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()

    # Locate the `const presets = (CC_GLOBAL ? [` block and capture until the
    # matching closing `]`.
    start = text.find("const presets = (CC_GLOBAL ? [")
    if start < 0:
        print("  WARN: couldn't find presets block in app.tsx")
        return
    # Find the closing of the global array (first `]` after that — the JP block
    # follows in the ternary's else branch).
    array_start = text.index("[", start)
    depth = 0
    array_end = -1
    for i in range(array_start, len(text)):
        c = text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                array_end = i
                break
    block = text[array_start + 1:array_end]

    # Each entry is a {} literal — extract each top-level pair.
    entry_pattern = re.compile(r"\{[^{}]*\}")
    enums = {
        "EventType.CM": "CM",
        "EventType.LOH": "LOH",
        "Season.Spring": 1, "Season.Summer": 2, "Season.Autumn": 3, "Season.Winter": 4, "Season.Sakura": 5,
        "GroundCondition.Good": 1, "GroundCondition.Yielding": 2, "GroundCondition.Soft": 3, "GroundCondition.Heavy": 4,
        "Weather.Sunny": 1, "Weather.Cloudy": 2, "Weather.Rainy": 3, "Weather.Snowy": 4,
        "Time.NoTime": 0, "Time.Morning": 1, "Time.Midday": 2, "Time.Evening": 3, "Time.Night": 4,
    }
    presets = []
    for m in entry_pattern.finditer(block):
        e = m.group(0)
        # Replace enum references with their JSON-friendly values
        for k, v in enums.items():
            e = e.replace(k, json.dumps(v))
        # Quote unquoted keys: foo:  → "foo":
        e_json = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', e)
        # Convert TS single-quoted strings to JSON double-quoted (no embedded
        # apostrophes in our presets so a global replace is safe enough).
        e_json = e_json.replace("'", '"')
        try:
            presets.append(json.loads(e_json))
        except Exception as exc:
            print(f"  skip preset (parse fail): {exc}: {e[:100]}")
    _emit(os.path.join(ASSETS, "cm_presets.json"), presets)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    print("Refreshing race filter data from uma-tools…")
    extract_courses()
    extract_skills()
    extract_cm_presets()
    print("Done.")


if __name__ == "__main__":
    main()
