"""Build the Archive universe lookup table from master.mdb and inject it
into training_viewer.html between sentinel markers.

The lookup is what makes the Archive tab in training_viewer.html able to
say "unlocked X / Y" — without a universe of all possible IDs it could
only show what the account JSON already lists.

Run this whenever Global master data changes:
    uv run python tools/build_archive_lookups.py
"""
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MDB = os.path.join(ROOT, "master.mdb")
VIEWER = os.path.join(ROOT, "training_viewer.html")

START = "// __ARCHIVE_UNIVERSE_START__"
END = "// __ARCHIVE_UNIVERSE_END__"


def _names(c, category):
    """index -> EN name from text_data."""
    return {row[0]: row[1] for row in c.execute(
        'SELECT "index", text FROM text_data WHERE category=?', (category,))}


def build(c):
    universe = {}

    # Honors: text_data category 65 is title, 66 is condition. honor_data.id
    # matches text_data.index for category 65/66.
    honor_titles = _names(c, 65)
    honor_conds = _names(c, 66)
    universe["honors"] = [
        {"id": hid, "name": honor_titles.get(hid, f"Honor {hid}"),
         "condition": honor_conds.get(hid, "")}
        for (hid,) in c.execute("SELECT id FROM honor_data ORDER BY id")
    ]

    # Missions: text_data category 67. mission_data.id -> text_data.index.
    mission_names = _names(c, 67)
    universe["missions"] = [
        {"id": mid, "name": mission_names.get(mid, f"Mission {mid}"),
         "mission_type": mt}
        for (mid, mt) in c.execute("SELECT id, mission_type FROM mission_data ORDER BY id")
    ]

    # Main stories: category 94. main_story_data.id -> index.
    main_story_names = _names(c, 94)
    universe["main_stories"] = [
        {"id": sid, "name": main_story_names.get(sid, f"Main Story {sid}")}
        for (sid,) in c.execute("SELECT id FROM main_story_data ORDER BY id")
    ]

    # Character stories: category 92. chara_story_data.story_id -> index.
    chara_story_names = _names(c, 92)
    universe["character_stories"] = [
        {"id": story_id, "chara_id": chara_id,
         "name": chara_story_names.get(story_id, f"Chara Story {story_id}")}
        for (story_id, chara_id) in c.execute(
            "SELECT story_id, chara_id FROM chara_story_data ORDER BY chara_id, story_id")
    ]

    # Extra stories.
    universe["extra_stories"] = [
        {"id": sid, "extra_id": eid}
        for (sid, eid) in c.execute(
            "SELECT id, story_extra_id FROM story_extra_story_data ORDER BY id")
    ]

    # Short episodes.
    universe["short_episodes"] = [
        {"id": sid} for (sid,) in c.execute("SELECT id FROM short_episode ORDER BY id")
    ]

    # Home posters: category 196.
    poster_names = _names(c, 196)
    universe["home_posters"] = [
        {"id": pid, "name": poster_names.get(pid, f"Poster {pid}")}
        for (pid,) in c.execute("SELECT id FROM home_poster_data ORDER BY id")
    ]

    # Tutorials: packets reference the tutorial's group_id (10001-style), not
    # the row id. Dedup by group_id so the universe matches the unlocked set.
    universe["tutorial_guides"] = [
        {"id": gid} for (gid,) in c.execute(
            "SELECT DISTINCT group_id FROM tutorial_guide_data ORDER BY group_id")
    ]

    # Music tracks.
    universe["music_tracks"] = [
        {"id": mid} for (mid,) in c.execute(
            "SELECT music_id FROM jukebox_music_data ORDER BY music_id")
    ]

    # Career Events (in-game "Event Gallery") — single_mode_story_data rows
    # flagged for gallery display. Keyed by story_id, which matches the
    # `id` field in released_episode_data_array.
    universe["career_events"] = [
        {"id": sid} for (sid,) in c.execute(
            "SELECT DISTINCT story_id FROM single_mode_story_data "
            "WHERE story_id > 0 AND gallery_flag = 1 ORDER BY story_id")
    ]

    # Conversation Gallery — home_story_trigger entries. Matches the
    # `home_story_trigger_id` field in talk_gallery_list.
    universe["conversation_gallery"] = [
        {"id": tid} for (tid,) in c.execute(
            "SELECT id FROM home_story_trigger ORDER BY id")
    ]

    return universe


def inject(universe):
    with open(VIEWER, "r", encoding="utf-8") as f:
        html = f.read()
    if START not in html or END not in html:
        # First-time install — inject the block right before </script> of the
        # last script tag. Caller can move it later if they want it elsewhere.
        anchor = html.rfind("</script>")
        if anchor < 0:
            raise SystemExit("Could not find </script> anchor in training_viewer.html")
        block = (
            f"\n{START}\n"
            f"const ARCHIVE_UNIVERSE = {json.dumps(universe, ensure_ascii=False, separators=(',', ':'))};\n"
            f"{END}\n"
        )
        html = html[:anchor] + block + html[anchor:]
    else:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
        block = (
            f"{START}\n"
            f"const ARCHIVE_UNIVERSE = {json.dumps(universe, ensure_ascii=False, separators=(',', ':'))};\n"
            f"{END}"
        )
        html = pattern.sub(block, html)
    with open(VIEWER, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


def main():
    if not os.path.exists(MDB):
        print(f"master.mdb not found at {MDB}", file=sys.stderr)
        sys.exit(1)
    c = sqlite3.connect(MDB)
    universe = build(c)
    for k, v in universe.items():
        print(f"  {k:20s} {len(v):5d}")
    inject(universe)
    size = os.path.getsize(VIEWER)
    print(f"Injected into training_viewer.html ({size:,} bytes total)")


if __name__ == "__main__":
    main()
