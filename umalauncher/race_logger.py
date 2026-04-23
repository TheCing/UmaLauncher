"""Logs standalone race results (Room Match, Champions Meet, etc.) to CSV and HorseACT-compatible JSON."""
import os
import csv
import json
import time
import gzip
import math

from loguru import logger
import util
import mdb

RACE_LOG_DIR_NAME = "race_logs"

RUNNING_STYLES = {
    1: "Nige",
    2: "Senko",
    3: "Sashi",
    4: "Oikomi",
}

APTITUDE_LABELS = {
    1: "G", 2: "F", 3: "E", 4: "D", 5: "C", 6: "B", 7: "A", 8: "S",
}

WEATHER_LABELS = {1: "Sunny", 2: "Cloudy", 3: "Rainy", 4: "Snowy"}
GROUND_CONDITION_LABELS = {1: "Good", 2: "SlightlyHeavy", 3: "Heavy", 4: "Bad"}
SEASON_LABELS = {1: "Spring", 2: "Summer", 3: "Autumn", 4: "Winter"}
MOTIVATION_LABELS = {1: "VeryBad", 2: "Bad", 3: "Normal", 4: "Good", 5: "Max"}
MOTIVATION_COEFS = {1: 0.88, 2: 0.94, 3: 1.0, 4: 1.02, 5: 1.04}
RARITY_LABELS = {1: "Rare1", 2: "Rare2", 3: "Rare3"}
DEFEAT_LABELS = {0: "None", 1: "Speed", 2: "Stamina", 3: "Power", 4: "Guts", 5: "Wiz"}

TURN_LABELS = {1: "Right", 2: "Left", 4: "Straight"}
GROUND_TYPE_LABELS = {1: "Turf", 2: "Dirt"}
INITIAL_LANE_TYPE_LABELS = {1: "ExtraSpaceAfter9", 2: "Normal"}
TURF_VISION_TYPE_LABELS = {1: "URA", 2: "Normal"}
DISTANCE_TYPE_RANGES = [(1400, "Short"), (1800, "Mile"), (2400, "Mid"), (999999, "Long")]

# Area values from MDB: 1=Sapporo, 2=Hakodate, 3=Niigata/Kyoto, etc.
# GroundTypeAvailable depends on track having both turf and dirt courses
GROUND_TYPE_AVAILABLE = {1: "TurfOnly", 2: "DirtOnly"}  # Default fallback


def _distance_type(distance):
    for threshold, label in DISTANCE_TYPE_RANGES:
        if distance <= threshold:
            return label
    return "Long"


def _guess_race_type(race_result):
    """Detect race type from race_result packet signals.

    Room Match: has room_id / saved_room_id / host_viewer_id / room_name
    Champions: no room signals, but has a race_instance_id set
    Unknown: no useful signals to distinguish
    """
    if race_result.get('room_id') or race_result.get('saved_room_id') \
            or race_result.get('host_viewer_id') or race_result.get('room_name'):
        return "RoomMatch"
    if race_result.get('race_instance_id'):
        return "Champions"
    return "Unknown"


# Maps HorseACT-style RaceType values to subfolder names (same as HorseACT plugin).
RACE_TYPE_FOLDERS = {
    "RoomMatch": "Room match",
    "Champions": "Champions meeting",
    "Single": "Career",
    "Practice": "Practice room",
}


def _apt(val):
    return APTITUDE_LABELS.get(val, str(val))


def get_log_dir(race_type=None):
    """Return the race logs directory, optionally under a race-type subfolder.

    `race_type` is the HorseACT-style label (RoomMatch/Champions/Single/Practice).
    Unknown or missing types fall through to the top-level race_logs folder.
    """
    base = util.get_appdata(RACE_LOG_DIR_NAME)
    subfolder = RACE_TYPE_FOLDERS.get(race_type) if race_type else None
    d = os.path.join(base, subfolder) if subfolder else base
    if not os.path.exists(d):
        os.makedirs(d)
    return d


def parse_race_scenario(race_scenario_str):
    """Parse the binary race_scenario into horse results."""
    import sys
    sys.path.insert(0, util.get_asset('external'))
    import race_data_parser
    return race_data_parser.parse(race_scenario_str)


def _query_race_data(race_instance_id):
    """Look up all race-related MDB data for a given race_instance_id.

    Returns a dict with keys: course_set, fence_set, race_track, race_master,
    race_instance_master, race_bib_master.  Any key may be None if the lookup fails.
    """
    result = {
        "course_set": None,
        "fence_set": None,
        "race_track": None,
        "race_master": None,
        "race_instance_master": None,
        "race_bib_master": None,
    }
    try:
        with mdb.Connection() as (conn, cursor):
            # Course set
            cursor.execute(
                """SELECT rcs.id, rcs.race_track_id, rcs.distance, rcs.ground, rcs.inout,
                          rcs.turn, rcs.fence_set, rcs.float_lane_max, rcs.course_set_status_id,
                          rcs.finish_time_min, rcs.finish_time_min_random_range,
                          rcs.finish_time_max, rcs.finish_time_max_random_range
                   FROM race_instance ri
                   JOIN race r ON ri.race_id = r.id
                   JOIN race_course_set rcs ON r.course_set = rcs.id
                   WHERE ri.id = ?""",
                (race_instance_id,)
            )
            row = cursor.fetchone()
            if not row:
                return result
            result["course_set"] = {
                "Id": row[0], "RaceTrackId": row[1], "Distance": row[2],
                "Ground": row[3], "Inout": row[4], "Turn": row[5],
                "FenceSet": row[6], "FloatLaneMax": row[7],
                "CourseSetStatusId": row[8], "FinishTimeMin": row[9],
                "FinishTimeMinRandomRange": row[10], "FinishTimeMax": row[11],
                "FinishTimeMaxRandomRange": row[12],
            }

            # Fence set
            fence_set_id = row[6]
            cursor.execute("SELECT * FROM race_fence_set WHERE id = ?", (fence_set_id,))
            frow = cursor.fetchone()
            if frow:
                result["fence_set"] = {
                    "Id": frow[0],
                    "Fence1": frow[1], "Fence2": frow[2], "Fence3": frow[3], "Fence4": frow[4],
                    "Fence5": frow[5], "Fence6": frow[6], "Fence7": frow[7], "Fence8": frow[8],
                }

            # Race track
            race_track_id = row[1]
            cursor.execute("SELECT * FROM race_track WHERE id = ?", (race_track_id,))
            trow = cursor.fetchone()
            if trow:
                result["race_track"] = {
                    "Id": trow[0], "InitialLaneType": trow[1], "EnableHalfGate": trow[2],
                    "HorseNumGateVariation": trow[3], "TurfVisionType": trow[4],
                    "FootsmokeColorType": trow[5], "Area": trow[6], "FlagType": trow[7],
                    "GatePanelType": trow[8], "GateLampType": trow[9],
                }

            # Race master
            cursor.execute(
                """SELECT r.id, r."group", r.grade, r.course_set, r.thumbnail_id,
                          r.ff_cue_name, r.ff_cuesheet_name, r.ff_anim, r.ff_camera,
                          r.ff_camera_sub, r.ff_sub, r.goal_gate, r.goal_flower,
                          r.audience, r.entry_num
                   FROM race_instance ri JOIN race r ON ri.race_id = r.id
                   WHERE ri.id = ?""",
                (race_instance_id,)
            )
            rrow = cursor.fetchone()
            if rrow:
                result["race_master"] = {
                    "Id": rrow[0], "Group": rrow[1], "Grade": rrow[2], "CourseSet": rrow[3],
                    "ThumbnailId": rrow[4], "FfCueName": rrow[5], "FfCuesheetName": rrow[6],
                    "FfAnim": rrow[7], "FfCamera": rrow[8], "FfCameraSub": rrow[9],
                    "FfSub": rrow[10], "GoalGate": rrow[11], "GoalFlower": rrow[12],
                    "Audience": rrow[13], "EntryNum": rrow[14],
                }

            # Race instance master
            cursor.execute(
                """SELECT id, race_id, npc_group_id, date, time, clock_time, race_number
                   FROM race_instance WHERE id = ?""",
                (race_instance_id,)
            )
            irow = cursor.fetchone()
            if irow:
                result["race_instance_master"] = {
                    "Id": irow[0], "RaceId": irow[1], "NpcGroupId": irow[2],
                    "Date": irow[3], "Time": irow[4], "ClockTime": irow[5],
                    "RaceNumber": irow[6],
                }

            # Race bib color (try race_id first, then grade-only fallback)
            grade = rrow[2] if rrow else 0
            race_id = rrow[0] if rrow else 0
            cursor.execute(
                "SELECT grade, race_id, bib_color, font_color FROM race_bib_color WHERE race_id = ?",
                (race_id,)
            )
            brow = cursor.fetchone()
            if not brow:
                cursor.execute(
                    "SELECT grade, race_id, bib_color, font_color FROM race_bib_color WHERE grade = ? AND race_id = 0",
                    (grade,)
                )
                brow = cursor.fetchone()
            if brow:
                result["race_bib_master"] = {
                    "Grade": brow[0], "RaceId": brow[1],
                    "BibColor": brow[2], "FontColor": brow[3],
                }

            return result
    except Exception as e:
        logger.debug(f"Could not query race data for race_instance_id {race_instance_id}: {e}")
    return result


def _build_program_to_instance_map(race_result_arrays):
    """Batch-lookup program_id -> race_instance_id for all horses' race_result_array entries."""
    all_program_ids = set()
    for rra in race_result_arrays:
        for entry in rra:
            all_program_ids.add(entry.get('program_id', 0))
    all_program_ids.discard(0)

    if not all_program_ids:
        return {}

    mapping = {}
    try:
        with mdb.Connection() as (conn, cursor):
            # SQLite limits placeholders; batch in chunks
            pid_list = list(all_program_ids)
            for chunk_start in range(0, len(pid_list), 500):
                chunk = pid_list[chunk_start:chunk_start + 500]
                placeholders = ','.join('?' * len(chunk))
                cursor.execute(
                    f"SELECT id, race_instance_id FROM single_mode_program WHERE id IN ({placeholders})",
                    chunk
                )
                for row in cursor.fetchall():
                    mapping[row[0]] = row[1]
    except Exception as e:
        logger.debug(f"Could not build program->instance mapping: {e}")
    return mapping


def _build_race_record(horse_data, program_to_instance):
    """Build HorseACT-style _raceRecord from race_result_array."""
    rra = horse_data.get('race_result_array', [])

    win_ids = []
    all_ids = []
    is_undefeated = True

    for entry in rra:
        pid = entry.get('program_id', 0)
        rid = program_to_instance.get(pid, 0)
        if rid:
            all_ids.append(rid)
            if entry.get('result_rank', 0) == 1:
                win_ids.append(rid)
            else:
                is_undefeated = False
        else:
            is_undefeated = False

    # Pad to 64 entries like HorseACT's C# List serialization
    pad_size = 64
    win_padded = win_ids + [0] * (pad_size - len(win_ids))
    all_padded = all_ids + [0] * (pad_size - len(all_ids))

    return {
        "<IsUndefeated>k__BackingField": is_undefeated,
        "<WinRaceInstanceIdList>k__BackingField": {
            "_items": win_padded,
            "_size": len(win_ids),
            "_version": 1,
            "_syncRoot": 0,
        },
        "_raceInstanceIdList": {
            "_items": all_padded,
            "_size": len(all_ids),
            "_version": 1,
            "_syncRoot": 0,
        },
    }


def _transform_trained_chara(tc):
    """Transform raw trained_chara_array entry into HorseACT C#-style format
    that hakuraku's race replayer expects."""
    if not tc:
        return None

    out = dict(tc)  # Keep all raw fields as a base

    # Transform support_card_list -> <SupportCardArray>k__BackingField
    support_cards = tc.get('support_card_list', [])
    if support_cards:
        out["<SupportCardArray>k__BackingField"] = [
            {
                "<Position>k__BackingField": sc.get('position', 0),
                "<SupportCardId>k__BackingField": sc.get('support_card_id', 0),
                "<LimitBreakCount>k__BackingField": sc.get('limit_break_count', 0),
                "<Exp>k__BackingField": sc.get('exp', 0),
            }
            for sc in support_cards
        ]

    # Transform succession_chara_array -> <SuccessionCharaList>k__BackingField
    succession = tc.get('succession_chara_array', [])
    if succession:
        items = []
        for parent in succession:
            factors = parent.get('factor_info_array', [])
            items.append({
                "_positionId": parent.get('position_id', 0),
                "<CardId>k__BackingField": parent.get('card_id', 0),
                "_rank": parent.get('rank', 0),
                "<FactorDataArray>k__BackingField": [
                    {"FactorId": f.get('factor_id', 0)}
                    for f in factors
                ],
            })
        out["<SuccessionCharaList>k__BackingField"] = {"_items": items}

    # Transform own factor_info_array -> <FactorDataArray>k__BackingField
    own_factors = tc.get('factor_info_array', [])
    if own_factors:
        out["<FactorDataArray>k__BackingField"] = [
            {"FactorId": f.get('factor_id', 0)}
            for f in own_factors
        ]

    # Map remaining fields to C#-style names for completeness
    out["<ScenarioId>k__BackingField"] = tc.get('scenario_id', 0)
    out["<TalentLevel>k__BackingField"] = tc.get('talent_level', 0)
    out["<CharaGrade>k__BackingField"] = tc.get('chara_grade', 0)
    out["<Rarity>k__BackingField"] = tc.get('rarity', 0)
    out["<CreateTime>k__BackingField"] = tc.get('create_time', '')
    out["<SuccessionCount>k__BackingField"] = tc.get('succession_num', 0)

    return out


def _build_race_param(horse_data):
    """Build HorseACT-style _raceParam from raw horse data."""
    motivation = horse_data.get('motivation', 3)
    coef = MOTIVATION_COEFS.get(motivation, 1.0)
    raw_speed = horse_data.get('speed', 0)
    raw_stamina = horse_data.get('stamina', 0)
    raw_pow = horse_data.get('pow', 0)
    raw_guts = horse_data.get('guts', 0)
    raw_wiz = horse_data.get('wiz', 0)
    return {
        "<RawSpeed>k__BackingField": raw_speed,
        "<RawStamina>k__BackingField": raw_stamina,
        "<RawPow>k__BackingField": raw_pow,
        "<RawGuts>k__BackingField": raw_guts,
        "<RawWiz>k__BackingField": raw_wiz,
        "<BaseSpeed>k__BackingField": raw_speed * coef,
        "<BaseStamina>k__BackingField": raw_stamina * coef,
        "<BasePow>k__BackingField": raw_pow * coef,
        "<BaseGuts>k__BackingField": raw_guts * coef,
        "<BaseWiz>k__BackingField": raw_wiz * coef,
        "<Motivation>k__BackingField": MOTIVATION_LABELS.get(motivation, "Normal"),
        "<MotivationCoef>k__BackingField": coef,
    }


def _build_horse_entry(index, horse_data, horse_result, chara_name, trained_chara, race_record):
    """Build a HorseACT-compatible horse object."""
    popularity = horse_data.get('popularity', 0)
    pop_marks = horse_data.get('popularity_mark_rank_array', [0, 0, 0])

    entry = {
        "horseIndex": index,
        "postNumber": horse_data.get('frame_order', index + 1),
        "charaId": horse_data.get('chara_id', 0),
        "<charaName>k__BackingField": chara_name,
        "FinishOrder": horse_result.finish_order if horse_result else -1,
        "FinishTimeRaw": horse_result.finish_time_raw if horse_result else 0.0,
        "FinishTimeScaled": horse_result.finish_time if horse_result else 0.0,
        "FinishDiffTimeFromPrev": horse_result.finish_diff_time if horse_result else 0.0,
        "_raceParam": _build_race_param(horse_data),
        "_responseHorseData": horse_data,
        "<Popularity>k__BackingField": popularity,
        "<PopularityRankLeft>k__BackingField": pop_marks[0] if len(pop_marks) > 0 else 0,
        "<PopularityRankCenter>k__BackingField": pop_marks[1] if len(pop_marks) > 1 else 0,
        "<PopularityRankRight>k__BackingField": pop_marks[2] if len(pop_marks) > 2 else 0,
        "_gateInPopularity": 0,
        "<Rarity>k__BackingField": RARITY_LABELS.get(horse_data.get('rarity', 3), "Rare3"),
        "<TrainerName>k__BackingField": horse_data.get('trainer_name', horse_data.get('owner_trainer_name', '')),
        "IsGhost": False,
        "_isRunningStyleExInitialized": False,
        "_runningStyleEx": "None",
        "<Defeat>k__BackingField": DEFEAT_LABELS.get(horse_result.defeat if horse_result else 0, "None"),
        "<RaceDressId>k__BackingField": horse_data.get('race_dress_id', 0),
        "<RaceDressIdWithOption>k__BackingField": horse_data.get('race_dress_id', 0),
        "<RunningType>k__BackingField": "Base",
        "<ActiveProperDistance>k__BackingField": _apt(horse_data.get('proper_distance_long', 0)),
        "<ActiveProperGroundType>k__BackingField": _apt(horse_data.get('proper_ground_turf', 0)),
        "<MobId>k__BackingField": horse_data.get('mob_id', 0),
        "_raceRecord": race_record,
        "<FinishOrderRawScore>k__BackingField": 0,
    }

    transformed_tc = _transform_trained_chara(trained_chara)
    if transformed_tc:
        entry["<TrainedCharaData>k__BackingField"] = transformed_tc

    return entry


def _build_phase_calculator(distance):
    """Build phase distance calculator matching HorseACT format."""
    d = float(distance)
    return {
        "<PhaseMiddleStartDistance>k__BackingField": d / 6.0,
        "<PhaseEndStartDistance>k__BackingField": d * 2.0 / 3.0,
        "<PhaseLastStartDistance>k__BackingField": d * 5.0 / 6.0,
        "_courseDistance": d,
        "_isInitialized": True,
    }


def save_race_packet(data):
    """Save race data as a HorseACT-compatible JSON file."""
    race_result = data.get('race_result', {})
    race_type = _guess_race_type(race_result)
    log_dir = get_log_dir(race_type)

    horses = data.get('race_horse_data_array', [])
    trained_charas = data.get('trained_chara_array', [])

    if not horses:
        logger.warning("No horses in race packet, skipping save.")
        return None

    # Parse finish order from race_scenario.
    # sim.horse_result is indexed by post position (frame_order - 1),
    # NOT by input array position. See training_tracker.py which uses the
    # same `horse_result[frame_order-1]` pattern.
    scenario_str = data.get('race_scenario', '')
    finish_data = {}
    if scenario_str and isinstance(scenario_str, str):
        try:
            sim = parse_race_scenario(scenario_str)
            for i, hr in enumerate(sim.horse_result):
                finish_data[i] = hr
        except Exception as e:
            logger.warning(f"Could not parse race_scenario: {e}")

    # Build trained_chara lookup by viewer_id + card_id
    tc_lookup = {}
    for tc in trained_charas:
        key = (tc.get('owner_viewer_id') or tc.get('viewer_id'), tc.get('card_id'))
        tc_lookup[key] = tc

    # Name lookup
    chara_names = util.get_character_name_dict()

    # Build program_id -> race_instance_id mapping for _raceRecord
    all_rra = [h.get('race_result_array', []) for h in horses]
    program_to_instance = _build_program_to_instance_map(all_rra)

    # Build per-horse entries
    all_horses = []
    for i, h in enumerate(horses):
        chara_id = h.get('chara_id', 0)
        chara_name = chara_names.get(chara_id, f"Chara {chara_id}")
        frame_order = h.get('frame_order', i + 1)
        hr = finish_data.get(frame_order - 1)

        viewer_id = h.get('viewer_id') or h.get('owner_viewer_id', '')
        card_id = h.get('card_id', 0)
        tc = tc_lookup.get((viewer_id, card_id))

        race_record = _build_race_record(h, program_to_instance)
        entry = _build_horse_entry(i, h, hr, chara_name, tc, race_record)
        all_horses.append(entry)

    # Determine player teams (group by team_id)
    team_ids = {}
    for i, h in enumerate(horses):
        tid = h.get('team_id', 0)
        if tid not in team_ids:
            team_ids[tid] = []
        team_ids[tid].append(i)

    # Player team = largest team or first team
    player_team_indices = max(team_ids.values(), key=len) if team_ids else []
    player_team = [all_horses[i] for i in player_team_indices]

    # Find best finisher on player team
    player_team_top = None
    for entry in sorted(player_team, key=lambda e: e["FinishOrder"] if e["FinishOrder"] >= 0 else 999):
        player_team_top = entry
        break

    # Find winner (finish_order 0 = 1st place)
    winner_idx = 0
    winner_name = "Unknown"
    winner_time_raw = 0.0
    for i, entry in enumerate(all_horses):
        if entry["FinishOrder"] == 0:
            winner_idx = i
            winner_name = entry["<charaName>k__BackingField"]
            winner_time_raw = entry["FinishTimeRaw"]
            break

    # Build finish order and popularity index arrays
    horse_index_by_finish = [0] * len(all_horses)
    horse_index_by_pop = [0] * len(all_horses)
    for i, entry in enumerate(all_horses):
        fo = entry["FinishOrder"]
        if 0 <= fo < len(all_horses):
            horse_index_by_finish[fo] = i
        pop = entry["<Popularity>k__BackingField"]
        if 0 < pop <= len(all_horses):
            horse_index_by_pop[pop - 1] = i

    # Race metadata
    weather_raw = data.get('weather', race_result.get('weather', 1))
    ground_raw = data.get('ground_condition', race_result.get('ground_condition', 1))
    season_raw = data.get('season', race_result.get('season', 1))
    race_instance_id = race_result.get('race_instance_id', 0)

    # Query all MDB race data
    race_data = _query_race_data(race_instance_id)
    course_set = race_data["course_set"]
    fence_set = race_data["fence_set"]
    race_track = race_data["race_track"]
    race_master = race_data["race_master"]
    race_instance_master = race_data["race_instance_master"]
    race_bib_master = race_data["race_bib_master"]

    distance = course_set["Distance"] if course_set else 0
    turn_val = course_set["Turn"] if course_set else 1
    ground_val = course_set["Ground"] if course_set else 1

    # Derived course fields
    furlong_num = math.ceil(distance / 200) if distance else 0
    section_distance = distance / (furlong_num * 1.5) if furlong_num else 0.0

    # Race track derived fields
    initial_lane_type_val = race_track["InitialLaneType"] if race_track else 1
    half_gate = bool(race_track["EnableHalfGate"]) if race_track else False
    horse_num_var_gate = bool(race_track["HorseNumGateVariation"]) if race_track else False
    turf_vision_val = race_track["TurfVisionType"] if race_track else 1

    # Goal gate/flower from race master
    goal_gate = race_master["GoalGate"] if race_master else 0
    goal_flower = race_master["GoalFlower"] if race_master else 0

    # Build the HorseACT-compatible output
    output = {
        "<RaceType>k__BackingField": race_type,
        "<IsExistPlayerRace>k__BackingField": True,
        "<IsExistGhostRace>k__BackingField": False,
        "<IsExistFollowRace>k__BackingField": False,
        "<IsMultiplePlayerRace>k__BackingField": len(team_ids) > 1,
        "<RandomSeed>k__BackingField": race_result.get('random_seed', 0),
        "<SingleRaceProgramId>k__BackingField": 0,
        "<IsSingleRaceExportRetryEnable>k__BackingField": False,
        "<SingleRaceRetryCount>k__BackingField": 0,
        "<OpponentEvaluate>k__BackingField": 0,
        "<SelfEvaluate>k__BackingField": 0,
        "<SupportCardScoreBonus>k__BackingField": 0,
        "<ScoreCalcTeamId>k__BackingField": 0,
        "<RaceNo>k__BackingField": race_instance_master["RaceNumber"] if race_instance_master else 0,
    }

    if course_set:
        output["<RaceCourseSet>k__BackingField"] = course_set
    if fence_set:
        output["<FenceSet>k__BackingField"] = fence_set
    if race_track:
        output["<RaceTrack>k__BackingField"] = race_track

    output.update({
        "<GoalGate>k__BackingField": goal_gate,
        "<GoalGateFlower>k__BackingField": goal_flower,
        "<InitialLaneType>k__BackingField": INITIAL_LANE_TYPE_LABELS.get(initial_lane_type_val, "Normal"),
        "<RotationCategory>k__BackingField": TURN_LABELS.get(turn_val, "Right"),
        "<GroundTypeAvailable>k__BackingField": "TurfAndDirt",
        "<CourseSectionDistance>k__BackingField": section_distance,
        "<CourseDistanceType>k__BackingField": _distance_type(distance) if distance else "Unknown",
        "<CourseFurlongNum>k__BackingField": furlong_num,
        "<IsHalfGate>k__BackingField": half_gate,
        "<IsHorseNumVariationGate>k__BackingField": horse_num_var_gate,
        "<TurfVisionType>k__BackingField": TURF_VISION_TYPE_LABELS.get(turf_vision_val, "Normal"),
        "<GroundCondition>k__BackingField": GROUND_CONDITION_LABELS.get(ground_raw, "Good"),
        "<Weather>k__BackingField": WEATHER_LABELS.get(weather_raw, "Sunny"),
        "<Season>k__BackingField": SEASON_LABELS.get(season_raw, "Spring"),
        "<Time>k__BackingField": "Daytime",
        "_baseSpeed": -1.0,
        "<BorderTimeScaled>k__BackingField": 0.0,
        "<ChallengeMatchDifficulty>k__BackingField": "Easy",
        "<NumRaceHorses>k__BackingField": len(horses),
        "<PostNumberMax>k__BackingField": len(horses) - 1,
        "_playerHorseIndex": player_team_indices[0] if player_team_indices else 0,
        "<PlayerTeamMemberArray>k__BackingField": player_team,
        "<PlayerTeamTopFinishOrderHorse>k__BackingField": player_team_top,
        "<IsGateInPopularityInitialized>k__BackingField": True,
        "<RaceHorse>k__BackingField": all_horses,
    })

    if race_bib_master:
        output["<RaceBibMaster>k__BackingField"] = race_bib_master
    if race_master:
        output["_raceMaster"] = race_master
    if race_instance_master:
        output["_raceInstanceMaster"] = race_instance_master

    output.update({
        "<SimDataBase64>k__BackingField": scenario_str if isinstance(scenario_str, str) else "",
        "<EpisodeRaceReplayId>k__BackingField": 0,
        "<IsNotSimulateExport>k__BackingField": False,
        "<LaneDistanceMax>k__BackingField": 1.25,
        "<ReplayCheckInfo>k__BackingField": {
            "RewardSetArray": None,
            "RewardPlusBonusSetArray": None,
            "BonusRewardSetArray": None,
            "BonusRewardWinSetArray": None,
            "IsItemNumLimit": False,
        },
        "<ReplayCheckInfoDaily>k__BackingField": None,
        "<ReplayCheckInfoLegend>k__BackingField": None,
        "<IsDailyLegendRace>k__BackingField": False,
        "<ReplayCheckInfoChallengeMatch>k__BackingField": None,
        "RaceRewardSingle": {
            "reward": None,
            "RaceGainedFanCount": 0,
            "RaceAfterPlayer": None,
        },
        "<ResultHorseIndex>k__BackingField": winner_idx,
        "<PrevGradeType>k__BackingField": None,
        "<MainStoryRaceGimmickType>k__BackingField": None,
        "<IsMainStoryRaceMatchGimmick>k__BackingField": False,
    })

    if distance:
        output["_phaseCalculator"] = _build_phase_calculator(distance)

    output.update({
        "<HorseIndexByFinishOrder>k__BackingField": horse_index_by_finish,
        "<HorseIndexByPopularity>k__BackingField": horse_index_by_pop,
        "umalauncher_version": util.VERSION if hasattr(util, 'VERSION') else "unknown",
        "_raceResult": race_result,
    })

    # Filename: CharaName-FinishTimeRaw+s-YYYYMMDD.json
    date_str = time.strftime("%Y%m%d")
    safe_name = winner_name.replace("/", "_").replace("\\", "_").replace(":", "_")
    filename = f"{safe_name}-{winner_time_raw:.4f}s-{date_str}.json"
    filepath = os.path.join(log_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    logger.info(f"Saved HorseACT-compatible race data to {filepath}")
    return filepath


def log_race(data):
    """Parse a standalone race packet and append results to the race log CSV."""
    try:
        _log_race_inner(data)
    except Exception as e:
        logger.error(f"Failed to log race: {e}")
        import traceback
        logger.error(traceback.format_exc())


def _log_race_inner(data):
    race_result = data.get('race_result', {})
    horses = data.get('race_horse_data_array', [])
    trained_charas = data.get('trained_chara_array', [])

    if not horses:
        logger.warning("No horses in race packet, skipping log.")
        return

    # Parse finish order from race_scenario
    scenario_str = data.get('race_scenario', '')
    finish_data = {}
    if scenario_str and isinstance(scenario_str, str):
        try:
            sim = parse_race_scenario(scenario_str)
            for i, hr in enumerate(sim.horse_result):
                finish_data[i] = hr
        except Exception as e:
            logger.warning(f"Could not parse race_scenario: {e}")

    # Build trained_chara lookup by viewer_id + card_id for matching
    tc_lookup = {}
    for tc in trained_charas:
        key = (tc.get('owner_viewer_id') or tc.get('viewer_id'), tc.get('card_id'))
        tc_lookup[key] = tc

    # Name dicts
    chara_names = util.get_character_name_dict()
    skill_names = mdb.get_skill_name_dict()

    # Race metadata
    room_name = race_result.get('room_name', '')
    room_id = race_result.get('room_id', '')
    race_instance_id = race_result.get('race_instance_id', '')
    start_time = race_result.get('start_time', '')
    entry_num = race_result.get('entry_num', len(horses))
    weather = data.get('weather', '')
    ground_condition = data.get('ground_condition', '')
    season = data.get('season', '')
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    # Build rows
    rows = []
    for i, h in enumerate(horses):
        chara_id = h.get('chara_id', 0)
        card_id = h.get('card_id', 0)
        chara_name = chara_names.get(chara_id, f"Chara {chara_id}")

        # sim.horse_result is indexed by post position (frame_order - 1)
        frame_order = h.get('frame_order', i + 1)
        hr = finish_data.get(frame_order - 1)
        finish_order = hr.finish_order + 1 if hr else ''
        finish_time = f"{hr.finish_time:.2f}" if hr else ''
        last_spurt = f"{hr.last_spurt_start_distance:.1f}" if hr else ''

        # Get skill list from race_horse_data_array
        skills = h.get('skill_array', [])
        skill_strs = []
        for s in skills:
            sid = s.get('skill_id', 0)
            sname = skill_names.get(sid, str(sid))
            skill_strs.append(sname)

        # Match to trained_chara for extra info
        viewer_id = h.get('viewer_id') or h.get('owner_viewer_id', '')
        tc = tc_lookup.get((viewer_id, card_id), {})
        rank_score = tc.get('rank_score', '')
        scenario_id = tc.get('scenario_id', '')
        fans = tc.get('fans', '')
        wins = tc.get('wins', '')

        row = {
            'timestamp': timestamp,
            'race_start_time': start_time,
            'room_name': room_name,
            'room_id': room_id,
            'race_instance_id': race_instance_id,
            'entry_count': entry_num,
            'weather': weather,
            'ground_condition': ground_condition,
            'season': season,
            'finish_order': finish_order,
            'finish_time': finish_time,
            'last_spurt_dist': last_spurt,
            'trainer_name': h.get('trainer_name', h.get('owner_trainer_name', '')),
            'viewer_id': viewer_id,
            'chara_name': chara_name,
            'chara_id': chara_id,
            'card_id': card_id,
            'running_style': RUNNING_STYLES.get(h.get('running_style', 0), str(h.get('running_style', ''))),
            'speed': h.get('speed', 0),
            'stamina': h.get('stamina', 0),
            'power': h.get('pow', 0),
            'guts': h.get('guts', 0),
            'wisdom': h.get('wiz', 0),
            'final_grade': h.get('final_grade', ''),
            'rank_score': rank_score,
            'scenario_id': scenario_id,
            'fans': fans,
            'wins': wins,
            'turf': _apt(h.get('proper_ground_turf', 0)),
            'dirt': _apt(h.get('proper_ground_dirt', 0)),
            'short': _apt(h.get('proper_distance_short', 0)),
            'mile': _apt(h.get('proper_distance_mile', 0)),
            'mid': _apt(h.get('proper_distance_middle', 0)),
            'long': _apt(h.get('proper_distance_long', 0)),
            'nige': _apt(h.get('proper_running_style_nige', 0)),
            'senko': _apt(h.get('proper_running_style_senko', 0)),
            'sashi': _apt(h.get('proper_running_style_sashi', 0)),
            'oikomi': _apt(h.get('proper_running_style_oikomi', 0)),
            'skills': ' | '.join(skill_strs),
        }
        rows.append(row)

    # Sort by finish order
    rows.sort(key=lambda r: r['finish_order'] if isinstance(r['finish_order'], int) else 999)

    # Append to CSV
    csv_path = os.path.join(get_log_dir(), "race_results.csv")
    file_exists = os.path.exists(csv_path)

    fieldnames = list(rows[0].keys())
    with open(csv_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(csv_path) == 0:
            writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Logged {len(rows)} horses from race to {csv_path}")


def reprocess_all():
    """Reprocess all saved race packet JSONs into the CSV."""
    import glob

    log_dir = get_log_dir()
    json_files = sorted(glob.glob(os.path.join(log_dir, "*.json")))

    if not json_files:
        print(f"No race JSON files found in {log_dir}")
        return

    # Clear existing CSV
    csv_path = os.path.join(log_dir, "race_results.csv")
    if os.path.exists(csv_path):
        os.remove(csv_path)

    ok = 0
    fail = 0
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                file_data = json.load(f)
            # Only process raw packet files (have race_horse_data_array),
            # skip HorseACT-format files (have <RaceHorse>k__BackingField)
            if 'race_horse_data_array' in file_data:
                log_race(file_data)
                ok += 1
            else:
                logger.debug(f"Skipping {os.path.basename(jf)} (not a raw packet)")
        except Exception as e:
            fail += 1
            logger.error(f"Failed to reprocess {os.path.basename(jf)}: {e}")

    print(f"Reprocessed: {ok} races logged, {fail} failed")
