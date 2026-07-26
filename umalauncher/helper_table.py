import copy
import json
import os

from loguru import logger
import mdb
import util
import constants
from helper_table_defaults import RowTypes

# After-race events (Victory! / Solid Showing / Defeat). For these the first
# choice is always the safe/no-risk pick and select_index 1|2 is the good roll.
AFTER_RACE_EVENT_IDS = (7005, 7006, 7007)

# Learned mapping: story_id -> choice_number -> "select_index:gain_select_id_index"
# -> [condition effect ids]. Lets us predict a choice's outcome from the
# pre-rolled packet (see tools/build_event_outcomes.py). Cached on first use.
_EVENT_OUTCOMES = None


def _get_event_outcomes():
    global _EVENT_OUTCOMES
    if _EVENT_OUTCOMES is None:
        try:
            with open(util.get_asset("_assets/event_outcomes.json"), encoding="utf-8") as f:
                _EVENT_OUTCOMES = json.load(f)
        except Exception:
            logger.warning("event_outcomes.json not found — event predictions disabled.")
            _EVENT_OUTCOMES = {}
    return _EVENT_OUTCOMES


# MANT (scenario 4) races that restock the shop when run (see
# tools/build_shop_restock_races.py). Program ids, cached on first use.
_SHOP_RESTOCK_RACES = None


def _get_shop_restock_races():
    global _SHOP_RESTOCK_RACES
    if _SHOP_RESTOCK_RACES is None:
        try:
            with open(util.get_asset("_assets/shop_restock_races.json"), encoding="utf-8") as f:
                _SHOP_RESTOCK_RACES = set(json.load(f).get("restock_program_ids", []))
        except Exception:
            _SHOP_RESTOCK_RACES = set()
    return _SHOP_RESTOCK_RACES


def _walk_dicts(node):
    """Recursively yield every dict nested anywhere inside node."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk_dicts(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk_dicts(item)


def _extract_events(data):
    """Find the first unchecked_event_array (at any nesting depth) whose entries
    carry a >=2-option choice, and return those entries.

    The array can appear top-level (training events) or nested inside after-race,
    shop-refresh, and scenario-specific packets — hence the recursive walk.
    """
    if not isinstance(data, dict):
        return []
    for obj in _walk_dicts(data):
        unchecked = obj.get('unchecked_event_array')
        if isinstance(unchecked, list) and unchecked:
            filtered = []
            for e in unchecked:
                if not isinstance(e, dict):
                    continue
                contents = e.get('event_contents_info')
                if not isinstance(contents, dict):
                    continue
                choices = contents.get('choice_array')
                if isinstance(choices, list) and len(choices) >= 2:
                    filtered.append(e)
            if filtered:
                return filtered
    return []


def build_event_choices(data):
    """Parse pending career-event choices (found at any nesting depth) into a
    readable list for the helper overlay. Each entry: {title, character,
    choices:[{index, label, kind, select_index}]}. Empty when none pending.

    Classification (ported from the older UmaLauncher event dump):
      - After-race event: choice 0 = Safe; the good/bad select_index split is
        scenario-specific (empirically verified against vital deltas):
          MANT (4):      choice 2 rolls sel 1-4; 1/2 = good (-10), 3/4 = bad (-25)
          Unity Cup (2): choice 2 rolls sel 1-2; 1 = good (-5), 2 = bad (-20)
          URA (1):       sel is fixed (1,2) every play — outcome is NOT
                         pre-rolled, so no prediction is possible.
      - Other events: odd select_index = likely-good gamble; even = likely-bad.
    """
    events = _extract_events(data)
    if not events:
        return []

    # card_id (for special-event title resolution) — find it anywhere in packet.
    # scenario_id decides which after-race select_index encoding applies.
    card_id = 0
    scenario_id = 0
    for obj in _walk_dicts(data):
        ci = obj.get('chara_info')
        if isinstance(ci, dict) and ci.get('card_id'):
            card_id = ci['card_id']
            scenario_id = ci.get('scenario_id', 0)
            break

    chara_names = mdb.get_chara_name_dict()
    status_names = mdb.get_status_name_dict()
    polarity = mdb.get_chara_effect_polarity_dict()
    outcomes_tbl = _get_event_outcomes()

    out = []
    for event in events:
        contents = event['event_contents_info']
        choices = contents['choice_array']
        story_id = event.get('story_id')
        event_id = event.get('event_id')
        chara_id = event.get('chara_id')
        try:
            title = mdb.get_event_titles(story_id, card_id)[0]
        except Exception:
            title = f"Event {story_id}"
        character = chara_names.get(chara_id) if chara_id else None

        story_tbl = outcomes_tbl.get(str(story_id), {})
        is_race = event_id in AFTER_RACE_EVENT_IDS
        event_has_condition = False
        rows = []
        for i, ch in enumerate(choices):
            if not isinstance(ch, dict):
                continue
            si = ch.get('select_index')
            gi = ch.get('gain_select_id_index')
            predicted = False

            if is_race:
                # After-race events (Victory!/Solid Showing/Defeat) reward
                # mood/energy, not conditions, so the condition table doesn't
                # apply — choice 0 is the safe pick, and the pre-rolled
                # select_index tells good/bad. The sel encoding differs per
                # scenario (verified empirically against vital deltas).
                if i == 0:
                    label, kind = "Safe", "safe"
                elif scenario_id == 1:
                    # URA: select_index is fixed every play (no pre-roll) —
                    # the outcome genuinely can't be predicted.
                    label, kind = "Gamble (not pre-rolled)", "unknown"
                elif scenario_id == 2:
                    # Unity Cup/Aoharu: sel 1 = good roll, 2 = bad roll.
                    if si == 1:
                        label, kind = "Good", "good"
                    else:
                        label, kind = "Bad", "bad"
                elif si in (1, 2):
                    # MANT and default: sel 1/2 = good roll, 3/4 = bad roll.
                    label, kind = "Good", "good"
                else:
                    label, kind = "Bad", "bad"
            else:
                # Prediction from the learned outcome table, keyed by this
                # choice's own pre-rolled entry. `can_grant` = this choice yields
                # a condition on at least one roll (a real gamble); `this_roll` is
                # what THIS packet rolled (None = unseen, [] = seen, no condition).
                choice_tbl = story_tbl.get(str(i + 1), {})
                entry_key = f"{si}:{gi}"
                can_grant = any(choice_tbl.get(k) for k in choice_tbl)
                if can_grant:
                    event_has_condition = True
                this_roll = choice_tbl.get(entry_key)

                if this_roll:
                    # This roll grants a condition — the real, specific outcome.
                    names = [status_names.get(e, f"#{e}") for e in this_roll]
                    kind = "bad" if any(polarity.get(e) == "bad" for e in this_roll) else "good"
                    label = " + ".join(names)
                    predicted = True
                elif this_roll == [] and can_grant:
                    # Table-confirmed: this choice can grant a condition, but this
                    # roll misses it (you'd lose the gamble).
                    label, kind, predicted = "No condition (miss)", "miss", True
                else:
                    # No specific condition prediction — fall back to the
                    # select_index hit/miss heuristic (odd = the good roll, even =
                    # the bad roll), same as the original build.
                    if si is not None and si % 2 == 1:
                        label, kind = "Likely Good", "good"
                    else:
                        label, kind = "Likely Bad", "bad"

            rows.append({'index': i, 'label': label, 'kind': kind,
                         'select_index': si, 'predicted': predicted})

        # Surface every choice event. Predictable ones show the condition /
        # Safe-Good-Bad; the rest show "Outcome unknown" rather than being hidden
        # (we don't have condition data for every event, and hiding them is worse
        # than an honest "unknown"). `event_has_condition` is retained only for
        # potential future use.
        if rows:
            out.append({'title': title, 'character': character,
                        'story_id': story_id, 'event_id': event_id, 'choices': rows})
    return out


class TrainingPartner():
    def __init__(self, partner_id, starting_bond, chara_info):
        self.partner_id = partner_id
        self.starting_bond = starting_bond
        self.chara_info = chara_info
        self.chara_id = None

        if partner_id < 100:
            support_id = chara_info['support_card_array'][partner_id - 1]['support_card_id']
            support_card_dict = mdb.get_support_card_dict()
            found_support = False
            if support_id not in support_card_dict:
                logger.warning(f"Could not find support_id {support_id}, attempting to force an update")
                support_card_dict = mdb.get_support_card_dict(force=True)
                if support_id not in support_card_dict:
                    logger.error(f"Could not find support_id {support_id} after forced update")
                    self.img = "https://umapyoi.net/missing_chara.png"
                else:
                    logger.info(f"Successfully found support_id {support_id}")
                    found_support = True
            else:
                found_support = True
            if found_support:
                support_data = support_card_dict[support_id]
                chara_id = support_data[3]
                self.chara_id = chara_id
                self.img = f"https://gametora.com/images/umamusume/characters/icons/chr_icon_{chara_id}.png"
        elif partner_id > 1000:
            self.chara_id = partner_id
            self.img = f"https://gametora.com/images/umamusume/characters/icons/chr_icon_{partner_id}.png"
        else:
            try:
                chara_id = mdb.get_single_mode_unique_chara_dict()[chara_info['scenario_id']][partner_id]
                self.chara_id = chara_id
                self.img = f"https://gametora.com/images/umamusume/characters/icons/chr_icon_{chara_id}.png"
            except KeyError:
                self.img = "https://umapyoi.net/missing_chara.png"
                logger.error(f"Could not find unique chara_id for partner_id {partner_id} in scenario {chara_info['scenario_id']}")
        
        # Precalc-bonds
        bond, useful_bond, hint_bond, hint_useful_bond = self.calc_bonds()
        self.bond = bond
        self.useful_bond = useful_bond
        self.hint_bond = hint_bond
        self.hint_useful_bond = hint_useful_bond
    
    def add_effect_bonus_bond(self, bond):
        # Add 2 extra bond when charming is active and the partner is not Akikawa
        if self.partner_id <= 6 and 8 in self.chara_info.get('chara_effect_id_array', []):
            bond += 2

        # Add 2 extra bond when rising star is active and the partner is Akikawa
        elif self.partner_id == 102 and 9 in self.chara_info.get('chara_effect_id_array', []):
            bond += 2
        
        return bond
    
    def calc_bonds(self):
        bond = 0
        max_possible = min(100, 100 - self.starting_bond)
        # Akikawa is 102
        if self.partner_id < 1000:
            add = 7
            if self.partner_id <= 6:
                support_card_id = self.chara_info['support_card_array'][self.partner_id - 1]['support_card_id']
                support_card_data = mdb.get_support_card_dict()[support_card_id]
                support_card_type = constants.SUPPORT_CARD_TYPE_DICT[(support_card_data[1], support_card_data[2])]
                if support_card_type in ("group", "friend"):
                    add = 4
            
            bond += add

            bond = self.add_effect_bonus_bond(bond)

        bond = min(bond, max_possible)
        
        hint_bond = bond

        if self.partner_id <= 6:
            hint_bond += 5

        hint_bond = self.add_effect_bonus_bond(hint_bond)

        hint_bond = min(hint_bond, max_possible)

        hint_bond -= bond

        return max(bond, 0), max(self.calc_useful_bond(bond, self.starting_bond), 0), max(hint_bond, 0), max(self.calc_useful_bond(hint_bond, self.starting_bond + bond), 0)


    def calc_useful_bond(self, amount, starting_bond):
        usefulness_cutoff = 80
        
        # Ignore group and friend type cards except Satake Mei in Project L'Arc
        if self.partner_id <= 6:
            support_card_id = self.chara_info['support_card_array'][self.partner_id - 1]['support_card_id']

            if support_card_id in (10094, 30160) and self.chara_info['scenario_id'] in (6,):  # Only count Mei in Project L'Arc
                usefulness_cutoff = 60
            elif support_card_id in (10104, 30188) and self.chara_info['scenario_id'] in (7,):  # Only count Ryoka in UAF
                usefulness_cutoff = 60
            else:
                support_card_data = mdb.get_support_card_dict()[support_card_id]
                support_card_type = constants.SUPPORT_CARD_TYPE_DICT[(support_card_data[1], support_card_data[2])]
                if support_card_type in ("group", "friend"):
                    return 0

        cur_bond = amount + starting_bond
        effective_bond = 0

        if 6 < self.partner_id <= 1000:
            if self.partner_id in (102,) and not self.chara_info['scenario_id'] in (1, 6, 4):  # Disable Akikawa usefulness in certain scenarios
                usefulness_cutoff = 60
            else:
                # Skip all non-Umas except Akikawa
                return 0

        new_bond = min(cur_bond, usefulness_cutoff)
        effective_bond = new_bond - starting_bond
        return max(effective_bond, 0)

class HelperTable():
    carrotjuicer = None
    selected_preset = None
    preset_dict = None

    def __init__(self, carrotjuicer):
        self.carrotjuicer = carrotjuicer
        self.preset_dict = {}
        self.selected_preset = None
        self.preset_dict, self.selected_preset = self.carrotjuicer.threader.settings.get_helper_table_data()
        # race_history / race_result_list only appear in post-race packets,
        # so cache the running tally and reuse it on home/training packets.
        self.last_races_run = 0

    def _update_races_run(self, data):
        # Pull from whichever list the current packet happens to carry; fall
        # back to cache when neither is present (most non-race packets).
        for key in ('race_history', 'race_result_list'):
            if data.get(key):
                self.last_races_run = len(data[key])
                return self.last_races_run
        chara_info = data.get('chara_info') or {}
        if chara_info.get('race_result_list'):
            self.last_races_run = len(chara_info['race_result_list'])
        return self.last_races_run

    def update_presets(self, preset_dict, selected_preset):
        self.preset_dict = preset_dict
        self.selected_preset = selected_preset
        if self.carrotjuicer.last_helper_data and self.carrotjuicer.browser and self.carrotjuicer.browser.alive():
            self.carrotjuicer.update_helper_table(self.carrotjuicer.last_helper_data)


    def create_helper_elements(self, data, last_data) -> str:
        """Creates the helper elements for the given response packet.
        """
        # Transfer data from last data if it does not exist in the current data
        if last_data:
            if 'reserved_race_array' not in data and 'reserved_race_array' in last_data:
                data['reserved_race_array'] = last_data['reserved_race_array']
            if 'race_condition_array' not in data and 'race_condition_array' in last_data:
                data['race_condition_array'] = last_data['race_condition_array']
            # Surely this won't cause any issues, right?
            if 'home_info' not in data and 'home_info' in last_data:
                data['home_info'] = last_data['home_info']

        if not 'home_info' in data:
            return None
        
        card_id = data['chara_info']['card_id']
        chara_id = int(str(card_id)[:4])
        
        turn = data['chara_info']['turn']
        scenario_id = data['chara_info']['scenario_id']
        energy = data['chara_info']['vital']
        exclude_director = self.carrotjuicer.threader.settings['bond_exclude_director']
        max_energy = data['chara_info']['max_vital']
        fans = data['chara_info']['fans']
        skillpt = data['chara_info']['skill_point']

        arc_aptitude_points = 0
        arc_expectation_gauge = 0
        arc_supporter_points = 0

        hint_partners = []

        command_info = {}

        all_commands = {}

        def get_commands(scenario_name):
            if 'command_info_array' in data[scenario_name] and data[scenario_name]['command_info_array'] is not None:
                return data[scenario_name]['command_info_array']
            return []

        # Default commands
        for command in get_commands('home_info'):
            all_commands[command['command_id']] = copy.deepcopy(command)
        
        # Scenario specific commands
        # Obsolete, but works as reference for devs
        scenario_keys = [
            'venus_data_set',  # Grand Masters
            'live_data_set',  # Grand Live
            'free_data_set', # MANT
            'team_data_set',  # Aoharu
            'ura_data_set',  # URA
            'arc_data_set',  # Project L'Arc
            'sport_data_set',  # UAF Ready GO!,
            'cook_data_set',  # Great Food Festival
            'mecha_data_set',  # Run! Mecha Umamusume
        ]

        for key in data:
            if key.endswith("_data_set") and 'command_info_array' in data[key]:
                for command in get_commands(key):
                    if 'params_inc_dec_info_array' in command and command['params_inc_dec_info_array'] is not None:
                        # FIXME: make a proper fix for this. Maybe deepcopy the command if it's missing?
                        if command['command_id'] not in all_commands \
                                or 'params_inc_dec_info_array' not in all_commands[command['command_id']] \
                                or all_commands[command['command_id']]['params_inc_dec_info_array'] is None:
                            continue
                        all_commands[command['command_id']]['params_inc_dec_info_array'] += command['params_inc_dec_info_array']


        # Venus specific
        if 'venus_data_set' in data and data['venus_data_set']['venus_chara_command_info_array'] is not None:
            for spirit_data in data['venus_data_set']['venus_chara_command_info_array']:
                if spirit_data['command_id'] in all_commands:
                    all_commands[spirit_data['command_id']]['spirit_data'] = spirit_data


        # Grand Live specific
        if 'live_data_set' in data:
            for command in get_commands('live_data_set'):
                all_commands[command['command_id']]['performance_inc_dec_info_array'] = command['performance_inc_dec_info_array']
        

        # Project L'Arc
        arc_charas = {}
        arc_beginning_or_overseas = False
        if 'arc_data_set' in data:
            for arc_chara in data['arc_data_set'].get('arc_rival_array', []):
                arc_charas[arc_chara['chara_id']] = arc_chara

            for command in data['arc_data_set'].get('command_info_array', []):
                if command['command_id'] in all_commands:
                    all_commands[command['command_id']]['add_global_exp'] = command['add_global_exp']

            arc_beginning_or_overseas = True
            # Make new command for Matches
            if 3 <= turn < 37 or 44 <= turn < 61:
                arc_beginning_or_overseas = False
                all_commands["ss_match"] = {
                    'command_id': "ss_match",
                    'params_inc_dec_info_array': data['arc_data_set'].get('selection_info', []).get('params_inc_dec_info_array', []) + \
                                                 data['arc_data_set'].get('selection_info', []).get('bonus_params_inc_dec_info_array', [])
                }

            for row in self.selected_preset:
                if isinstance(row, RowTypes.LARC_STAR_GAUGE_GAIN.value):
                    row.disabled = arc_beginning_or_overseas
                    break

        # Onsen
        if 'onsen_data_set' in data:
            for command in get_commands('onsen_data_set'):
                all_commands[command['command_id']]['dig_info_array'] = command['dig_info_array']

        # Beyond Dreams (Breeder's Cup)
        if 'breeders_data_set' in data:
            for command in get_commands('breeders_data_set'):
                all_commands[command['command_id']]['team_member_info_array'] = command['team_member_info_array']
                all_commands[command['command_id']]['turn'] = data['chara_info']['turn']
                for idx, member in enumerate(all_commands[command['command_id']]['team_member_info_array']):
                    team_member = [x for x in data['breeders_data_set']['team_member_info_array'] if x['chara_id'] == member['chara_id']]
                    all_commands[command['command_id']]['team_member_info_array'][idx]['rank'] = team_member[0]['rank']
                    all_commands[command['command_id']]['team_member_info_array'][idx]['exp'] = team_member[0]['exp']

        # Ramen
        feeling_turn_info_array = []
        special_feeling_num = 0
        if 'ramen_data_set' in data and 'feeling_reduce_turn_info_array' in data['ramen_data_set']:
            feeling_turn_info_array = data['ramen_data_set']['feeling_turn_info_array']
            special_feeling_num = data['ramen_data_set']['special_feeling_num']

            for command in get_commands('ramen_data_set'):
                all_commands[command['command_id']]['feeling_turn_array'] = next((x['feeling_turn_array'] for x in data['ramen_data_set']['feeling_reduce_turn_info_array'] if x['command_id'] == command['command_id'] ), [])

        #TODO add row for ramen stuff
        selected_region_id_array = []
        if 'ramen_data_set_load' in data and 'selected_region_id_array' in data['ramen_data_set_load']:
            selected_region_id_array = data['ramen_data_set_load']['selected_region_id_array']

        # Aoharu
        if 'team_data_set' in data:
            for command in get_commands('team_data_set'):
                all_commands[command['command_id']]['guide_event_partner_array'] = command['guide_event_partner_array']
                all_commands[command['command_id']]['soul_event_partner_array'] = command['soul_event_partner_array']


        # Support Dict
        eval_dict = {}
        for eval_data in data['chara_info']['evaluation_info_array']:
            try:
                eval_dict[eval_data['training_partner_id']] = TrainingPartner(eval_data['training_partner_id'], eval_data['evaluation'],data['chara_info'])
            except Exception as e:
                logger.error(f"Error while creating TrainingPartner: {e}")
                continue

        onsen_points_gain = {}
        # Onsen
        if 'onsen_data_set' in data:
            onsen_data = data['onsen_data_set']
            for command_data in get_commands('onsen_data_set'):
                command_id = command_data['command_id']
                command_key = constants.COMMAND_ID_TO_KEY.get(command_id, None)
                if command_key and command_key in command_info and 'dig_info_array' in command_data:
                    dig_info_array = copy.deepcopy(command_data['dig_info_array'])
                    command_info[constants.COMMAND_ID_TO_KEY[command_id]]['dig_info_array'] = dig_info_array

            # Make new command for PR Activities
            if 'assistant_command_info' in onsen_data and 'is_enable' in onsen_data['assistant_command_info'] and onsen_data['assistant_command_info']['is_enable'] == 1:
                all_commands["pr_activities"] = {
                    'command_id': "pr_activities",
                    'params_inc_dec_info_array': onsen_data['assistant_command_info'].get(
                        'params_inc_dec_info_array', []) + \
                                                 onsen_data['assistant_command_info'].get(
                                                     'bonus_params_inc_dec_info_array', []),
                    "dig_info_array": onsen_data['assistant_command_info'].get(
                                                     'dig_info_array', [])
                }



        # I'm lazy and don't want to refactor any of this, so I'm just defining these here
        uaf_sport_rank = {}
        uaf_sport_rank_total = {}
        uaf_current_required_rank = {}
        uaf_current_active_effects = {}
        uaf_current_active_bonus = {}
        uaf_sport_competition = {}
        uaf_consultations_left = {}

        for command in all_commands.values():
            if command['command_id'] not in constants.COMMAND_ID_TO_KEY:
                continue
            level = command.get('level', 0)
            failure_rate = command.get('failure_rate', 0)
            gained_stats = {stat_type: 0 for stat_type in set(constants.COMMAND_ID_TO_KEY.values())}
            gained_skillpt = 0
            total_bond = 0
            useful_bond = 0
            gained_energy = 0
            rainbow_count = 0
            arc_aptitude_gain = 0
            onsen_points_gain = 0
            team_member_info_array = {}

            if 'params_inc_dec_info_array' in command and command['params_inc_dec_info_array'] is not None:
                for param in command.get('params_inc_dec_info_array', []):
                    if param['target_type'] < 6:
                        gained_stats[constants.TARGET_TYPE_TO_KEY[param['target_type']]] += param['value']
                    elif param['target_type'] == 30:
                        gained_skillpt += param['value']
                    elif param['target_type'] == 10:
                        gained_energy += param['value']


            # Set up "training partners" for SS Match
            if command['command_id'] == 'ss_match':
                command['training_partner_array'] = []
                arc_eval_dict = {partner_data['chara_id']: partner_data['target_id'] for partner_data in data['arc_data_set']['evaluation_info_array']}
                
                for chara in data['arc_data_set']['selection_info']['selection_rival_info_array']:
                    partner_id = arc_eval_dict[chara['chara_id']]
                    command['training_partner_array'].append(partner_id)


            # For bond, first check if blue venus effect is active.
            spirit_id = 0
            spirit_boost = 0
            venus_blue_active = False
            if 'venus_data_set' in data:
                if 'spirit_data' in command:
                    spirit_id = command['spirit_data']['spirit_id']
                    spirit_boost = command['spirit_data']['is_boost']
                if len(data['venus_data_set']['venus_spirit_active_effect_info_array']) > 0 and data['venus_data_set']['venus_spirit_active_effect_info_array'][0]['chara_id'] == 9041:
                    venus_blue_active = True


            tip_gains_total = [0]
            tip_gains_useful = [0]
            bond_gains_total = [0]
            bond_gains_useful = [0]
            partner_count = 0
            useful_partner_count = 0
            riko_count = 0
            # True only when SSR Light Hello (30052) from the support deck is on this facility.
            has_ssr_light_hello = False
            num_hints = len(command.get('tips_event_partner_array', []))
            if num_hints:
                hint_partners += command.get('tips_event_partner_array')
            for training_partner_id in command.get('training_partner_array', []):
                partner_count += 1

                # Detect if training_partner is rainbowing
                training_partner = eval_dict[training_partner_id]
                if training_partner_id <= 6:
                    # Partner is a support card
                    support_id = data['chara_info']['support_card_array'][training_partner_id - 1]['support_card_id']
                    support_data = mdb.get_support_card_dict()[support_id]
                    support_card_type = mdb.get_support_card_type(support_data)

                    # Don't count friend cards as useful except Mei Satake in Project L'Arc and Light Hello in Grand Live and Ryoka for UAF.
                    # This should probably be moved to a setting rather then beeing predefined for the user to customize
                    if support_card_type != 'friend' or support_id == 30160 and scenario_id in (6,) or support_id == 30052 and scenario_id in (3,) or support_id == 30188 and support_id in (7,):
                        useful_partner_count += 1

                    if support_card_type not in ("group", "friend") and training_partner.starting_bond >= 80 and command['command_id'] in constants.SUPPORT_TYPE_TO_COMMAND_IDS[support_card_type]:
                        rainbow_count += 1
                    elif support_card_type == "group" and util.get_group_support_id_to_passion_zone_effect_id_dict()[support_id] in data['chara_info']['chara_effect_id_array']:
                        rainbow_count += 1
                    elif support_card_type != 'friend' and 'venus_data_set' in data and \
                            len(data['venus_data_set']['venus_spirit_active_effect_info_array']) > 0 and \
                                data['venus_data_set']['venus_spirit_active_effect_info_array'][0]['chara_id'] == 9042:
                        rainbow_count += 1

                    # Checking if Support card is Riko Kashimoto
                    if support_id == 30036 or support_id == 10060:
                        riko_count = 1

                    # SSR Light Hello (Grand Live)
                    if support_id == 30052:
                        has_ssr_light_hello = True

                elif training_partner_id > 1000:  # TODO: Maybe 1000 < training_partner_id < 9000
                    useful_partner_count += 1


                if training_partner_id in command.get('tips_event_partner_array', []):
                    tip_gains_total.append(training_partner.hint_bond)
                    tip_gains_useful.append(training_partner.hint_useful_bond)

                # Optionally leave Director Akikawa (partner 102) out of both bond
                # counts. Her useful bond is only non-zero in Grand Live (see
                # calc_useful_bond); elsewhere dropping it is a no-op. She still
                # counts as a partner on the facility.
                if not (exclude_director and training_partner_id == 102):
                    bond_gains_total.append(training_partner.bond)
                    bond_gains_useful.append(training_partner.useful_bond)

            unity_partner_count = 0
            useful_unity_partner_count = 0
            spirit_burst_partner_count = 0
            unity_near_explode_partner_count = 0
            if 'team_data_set' in data:
                for partner_id  in command.get('guide_event_partner_array', []):
                    # find partner in the evaluation_info_array
                    entry = next((d for d in data['team_data_set'].get('evaluation_info_array') if d["target_id"] == partner_id ), None)

                    # "Useful" is count of partners not yet exploded
                    if entry.get("soul_event_state") == 0:
                        useful_unity_partner_count += 1
                    # One step away from being full
                    if entry.get('soul_threshold_id') == 4:
                        unity_near_explode_partner_count += 1
                    unity_partner_count += 1
                for _ in command.get('soul_event_partner_array', []):
                    # TODO: Should a spirit burst parner be considered a useful partner?
                    unity_partner_count += 1
                    spirit_burst_partner_count += 1

            total_bond = sum(bond_gains_total)
            useful_bond = sum(bond_gains_useful)
            
            if not venus_blue_active:
                total_bond += max(tip_gains_total)
                useful_bond += max(tip_gains_useful)
            else:
                total_bond += sum(tip_gains_total)
                useful_bond += sum(tip_gains_useful)

            current_stats = data['chara_info'].get(constants.COMMAND_ID_TO_KEY[command['command_id']], 0)

            gl_tokens = {token_type: 0 for token_type in constants.GL_TOKEN_LIST}
            # Grand Live tokens
            if 'live_data_set' in data:
                for token_data in command.get('performance_inc_dec_info_array', []):
                    gl_tokens[constants.GL_TOKEN_LIST[token_data['performance_type']-1]] += token_data['value']


            # L'Arc star gauge
            arc_gauge_gain = 0
            if 'arc_data_set' in data:
                # Aptitude points
                if 'add_global_exp' in command:
                    arc_aptitude_gain += command['add_global_exp']


                arc_eval_dict = {partner_data['target_id']: partner_data['chara_id'] for partner_data in data['arc_data_set']['evaluation_info_array']}

                for arc_chara_id in [arc_eval_dict[partner_id] for partner_id in command.get('training_partner_array', [])]:
                    if arc_chara_id in arc_charas:
                        arc_chara = arc_charas[arc_chara_id]
                        arc_gauge_gain += min(1 + rainbow_count, 3 - arc_chara['rival_boost'])  # TODO: Try to avoid doing this right after a match is done?

                # Override row data for SS Match
                if command['command_id'] == "ss_match":
                    # Partners
                    rival_dict = {rival['chara_id']: rival for rival in data['arc_data_set']['arc_rival_array']}
                    selection_list = data['arc_data_set']['selection_info']['selection_rival_info_array']
                    partner_count = len(selection_list)
                    useful_partner_count = partner_count

                    for rival in selection_list:
                        rival_data = rival_dict[rival['chara_id']]
                        effect_data = rival_data['selection_peff_array'][0]
                        effect_type = effect_data['effect_group_id']

                        if effect_type == 3:
                            # Energy recovery
                            gained_energy += 20

                        elif effect_type == 4:
                            # Max energy up & Energy recovery
                            gained_energy += 20

                        elif effect_type == 5:
                            # Motivation up & Energy recovery
                            gained_energy += 20

                        elif effect_type == 6:
                            # Star Gauge refill
                            arc_gauge_gain += 3
                        
                        elif effect_type == 7:
                            # Aptitude points
                            arc_aptitude_gain += 50

            gained_energy = min(gained_energy, max_energy - energy)


            # UAF Ready GO!
            uaf_sport_rank = {}
            uaf_sport_gain = {}
            uaf_current_active_effects = {}
            uaf_current_active_bonus = 0
            uaf_sport_competition = {}
            uaf_sport_rank_total = {2100: 0, 2200: 0, 2300: 0}
            uaf_required_rank_for_turn = {}
            uaf_current_required_rank = -1
            uaf_consultations_left = 0
            
            if 'sport_data_set' in data:
                sport_levels = data['sport_data_set'].get('training_array', [])
                uaf_sport_rank = {item['command_id']: item['sport_rank'] for item in sport_levels}
                uaf_sport_compeition_win = data['sport_data_set'].get('competition_result_array', [])
                
                uaf_active_effects = data['sport_data_set'].get('compe_effect_id_array', [])
                uaf_effects = mdb.get_uaf_training_effects()
                
                for effect_id in uaf_active_effects:
                    key = str(effect_id)[0]
                    value = uaf_effects.get(effect_id)

                    if value is not None:
                        uaf_current_active_effects[key] = value
                        uaf_current_active_bonus += value
                    
                group_counts = {'1': 0, '2': 0, '3': 0} # Janky hacky
                
                for competition in uaf_sport_compeition_win:
                    if competition.get("result_state") == 1:
                        for win_command_id in competition.get("win_command_id_array", []):
                            group = str(win_command_id)[1]
                            if group in group_counts:
                                group_counts[group] += 1
                
                uaf_sport_competition = f"{group_counts['1']}/{group_counts['2']}/{group_counts['3']}"

                uaf_consultations_left = len(data['sport_data_set'].get('item_id_array', []))
                
                uaf_required_rank_for_turn = mdb.get_uaf_required_rank_for_turn()
                uaf_required_rank_for_turn.sort(key=lambda x: x[0], reverse=1)
                
                for row in uaf_required_rank_for_turn:
                    if turn <= row[0]:
                        uaf_current_required_rank = row[1]
                
                # Calculate totals for each base
                for command_id, rank in uaf_sport_rank.items():
                    base = command_id - (command_id % 100)  # Get the base (2100, 2200, 2300, etc.)
                    uaf_sport_rank_total[base] += rank
                        
                command_info_array = data['sport_data_set']['command_info_array']
                
                # Extract and sort gain information
                gain_info_list = []
                for command_info in command_info_array:
                    for gain_info in command_info['gain_sport_rank_array']:
                        command_id = gain_info['command_id']
                        gain_rank = gain_info['gain_rank']
                        gain_info_list.append((command_id, gain_rank))
                        
                # Sort the list by the last digit of command_id and convert it back to dictionary
                gain_info_list.sort(key=lambda x: x[0] % 10)
                uaf_sport_gain = {command_id: gain_rank for command_id, gain_rank in gain_info_list}

            # Onsen
            if 'onsen_data_set' in data:
                if 'dig_info_array' in command:
                    onsen_points_gain += sum(dig_info['dig_value'] for dig_info in command.get('dig_info_array', []))

            # Beyond Dreams (Breeder's Cup)
            has_ssr_casino_drive = False
            if 'breeders_data_set' in data:
                team_member_info_array = command.get('team_member_info_array', [])
                #rank_up_predict = command['rank_up_predict']
                for card in data['chara_info']['support_card_array']:
                    if card["support_card_id"] == 30290:
                        has_ssr_casino_drive = True
                        break

            # Ramen
            feeling_turn_array = []
            if "ramen_data_set" in data:
                feeling_turn_array = command.get("feeling_turn_array", [])

            command_info[command['command_id']] = {
                'scenario_id': scenario_id,
                'current_stats': current_stats,
                'level': level,
                'partner_count': partner_count,
                'useful_partner_count': useful_partner_count,
                'failure_rate': failure_rate,
                'gained_stats': gained_stats,
                'gained_skillpt': gained_skillpt,
                'num_hints': num_hints,
                'total_bond': total_bond,
                'useful_bond': useful_bond,
                'gained_energy': gained_energy,
                'rainbow_count': rainbow_count,
                'gm_fragment': spirit_id,
                'gm_fragment_double': spirit_boost,
                'gl_tokens': gl_tokens,
                'arc_gauge_gain': arc_gauge_gain,
                'arc_aptitude_gain': arc_aptitude_gain,
                'uaf_sport_gain': uaf_sport_gain,
                'onsen_points_gain': onsen_points_gain,
                'unity_partner_count': unity_partner_count,
                'useful_unity_partner_count': useful_unity_partner_count,
                'spirit_burst_partner_count': spirit_burst_partner_count,
                'team_member_info_array': team_member_info_array,
                'has_ssr_casino_drive': has_ssr_casino_drive,
                'turn': turn,
                'unity_near_explode_partner_count': unity_near_explode_partner_count,
                'riko_count': riko_count,
                'feeling_turn_array': feeling_turn_array,
                'feeling_turn_info_array': feeling_turn_info_array,
                'has_ssr_light_hello': has_ssr_light_hello,
            }

        # Simplify everything down to a dict with only the keys we care about.
        # No distinction between normal and summer training.
        command_info = {
            constants.COMMAND_ID_TO_KEY[command_id]: command_info[command_id]
            for command_id in command_info
            if command_id in constants.COMMAND_ID_TO_KEY
        }


        # Process scheduled races
        scheduled_races = []
        if 'reserved_race_array' in data:
            for race_data in data['reserved_race_array'][0]['race_array']:
                program_data = mdb.get_program_id_data(race_data['program_id'])
                if not program_data:
                    util.show_warning_box(f"Could not get program data for program_id {race_data['program_id']}")
                    continue
                
                if program_data['base_program_id'] != 0:
                    program_data = mdb.get_program_id_data(program_data['base_program_id'])
                
                if not program_data:
                    util.show_warning_box(f"Could not get program data for program_id {race_data['program_id']}")
                    continue

                year = race_data['year'] - 1
                month = program_data['month'] - 1
                half = program_data['half'] - 1
                s_turn = 24 * year
                s_turn += month * 2
                s_turn += half
                s_turn += 1
                thumb_url = f"https://gametora.com/images/umamusume/{'en/' if 'IS_UL_GLOBAL' in os.environ else '' }race_banners/thum_race_rt_000_{str(program_data['race_instance_id'])[:4]}_00.png"

                scheduled_races.append({
                    "turn": s_turn,
                    "fans": program_data['need_fan_count'],
                    "thumb_url": thumb_url
                })
            
            scheduled_races.sort(key=lambda x: x['turn'])

        # Grand Masters Fragments
        gm_fragments = [0] * 8
        if 'venus_data_set' in data:
            fragments = data['venus_data_set']['spirit_info_array']
            for fragment in fragments:
                if fragment['spirit_num'] <= 8:
                    gm_fragments[fragment['spirit_num'] - 1] = fragment['spirit_id']
        
        # Grand Live Stats
        gl_stats = {}
        if 'live_data_set' in data:
            gl_stats = data['live_data_set']['live_performance_info']

        # Project L'Arc Stats
        if 'arc_data_set' in data:
            arc_aptitude_points = data['arc_data_set']['arc_info']['global_exp']
            arc_expectation_gauge = data['arc_data_set']['arc_info']['approval_rate']
            arc_supporter_points = arc_charas[chara_id]['approval_point']
        
        # Great Food Festival
        gff_great_success = 0
        gff_success_point = 0
        gff_cooking_point = 0
        gff_tasting_thres = 0
        gff_tasting_great_thres = 0
        gff_vegetables = {}
        gff_field_point = [0, 0]
        if 'cook_data_set' in data:
            cook_data = data['cook_data_set']
            gff_cooking_point = cook_data['cook_info']['cooking_friends_power']
            gff_great_success = mdb.get_cooking_success_rate(gff_cooking_point)
            gff_success_point = cook_data['cook_info']['cooking_success_point']
            if gff_success_point >= 1500:
                gff_great_success = 100
            gff_tasting_thres, gff_tasting_great_thres = mdb.get_cooking_tasting_success_thresholds(data['chara_info']['turn'])
            gff_field_point[0] = cook_data['cook_info']['care_point']
            gff_field_point[1] = cook_data['care_point_gain_num']

            # Vegetables
            for veg_data in cook_data['material_info_array']:
                veg_dict = {
                    "id": veg_data['material_id'],
                    "count": veg_data['num'],
                    "max": 0,
                    "level": 0,
                    "harvest": 0,
                    "img": constants.GFF_VEG_ID_TO_IMG_ID[veg_data['material_id']],
                    "commands": {}
                }
                gff_vegetables[veg_data['material_id']] = veg_dict
            
            for fac_data in cook_data['facility_info_array']:
                fac_id = fac_data['facility_id']
                veg_dict = gff_vegetables[fac_id]
                veg_dict['level'] = fac_data['facility_level']
                veg_dict['max'] = mdb.get_cooking_vegetable_max_count(veg_dict['id'], veg_dict['level'])
            
            for harvest_data in cook_data['material_harvest_info_array']:
                veg_id = harvest_data['material_id']
                veg_dict = gff_vegetables[veg_id]
                veg_dict['harvest'] = harvest_data['harvest_num']
            
            for command_data in cook_data.get('command_material_care_info_array', []):
                if not command_data['command_type'] == 1:
                    continue
                
                command_id = command_data['command_id']
                cur_harvest_info = copy.deepcopy(command_data['material_harvest_info_array'])
                for harvest_info in cur_harvest_info:
                    veg_id = harvest_info['material_id']
                    veg_dict = gff_vegetables[veg_id]
                    harvest_info['harvest_num'] -= veg_dict['harvest']
                    harvest_info['img'] = veg_dict['img']
                command_info[constants.COMMAND_ID_TO_KEY[command_id]]['material_harvest_info_array'] = cur_harvest_info

        # Run! Mecha Umamusume
        if 'mecha_data_set' in data:
            mecha_data = data['mecha_data_set']
            for command_data in mecha_data.get('command_info_array', []):
                command_id = command_data['command_id']
                command_key = constants.COMMAND_ID_TO_KEY.get(command_id, None)
                if command_key and command_key in command_info and 'point_up_info_array' in command_data:
                    command_info[command_key]['point_up_info_array'] = command_data['point_up_info_array']


        # Design Your Island
        if 'pioneer_data_set' in data:
            dyi_data = data['pioneer_data_set']
            for command_data in dyi_data.get('command_info_array', []):
                command_id = command_data['command_id']
                command_key = constants.COMMAND_ID_TO_KEY.get(command_id, None)
                if command_key and command_key in command_info and 'params_inc_dec_info_array' in command_data and command_data['params_inc_dec_info_array'] is not None:
                    command_info[command_key]['params_inc_dec_info_array'] = command_data['params_inc_dec_info_array']
                    #logger.info(f"Command {command_key} : {command_data['params_inc_dec_info_array']}")
            for point_gain_data in dyi_data.get('pioneer_point_gain_info_array', []):
                command_id = point_gain_data['command_id']
                command_key = constants.COMMAND_ID_TO_KEY.get(command_id, None)
                if command_key is None:
                    continue
                gain_num = point_gain_data['gain_num']
                #logger.info(f'Point gain {command_key} ({command_id}) : {gain_num}')
                command_info[constants.COMMAND_ID_TO_KEY[command_id]]['pioneer_point_gain_info_array'] = gain_num
            #Remove the ticket column if:
            #  the column exists AND
            #    the command does not exist
            #    the command is disabled
            if constants.COMMAND_ID_TO_KEY[3101] in command_info and \
                    (not any(command['command_id'] == 3101 for command in data['home_info']['command_info_array'])  or
                      any(command['command_id'] == 3101 and command['is_enable'] == 0 for command in data['home_info']['command_info_array'])):
            #        not any(data['command_id'] == 3101 for data in dyi_data.get('pioneer_point_gain_info_array', [])) and\
            #        not any(data['command_id'] == 3101 for data in dyi_data.get('command_info_array', [])):
                del command_info[constants.COMMAND_ID_TO_KEY[3101]]


        # MANT
        races = []
        pick_up_item_info_array = []
        user_item_info_array = []
        rival_race_info_array = []
        coin_num = -1
        sale_value = 0
        uma_aptitudes = {}
        if "free_data_set" in data:
            free_data = data['free_data_set']
            if 'coin_num' in free_data:
                coin_num = free_data['coin_num']
            if 'sale_value' in free_data:
                sale_value = free_data['sale_value']
            # Shop (shop_item_id, item_id, coin_num, original_coin_num, item_buy_num (1=sold out), limit_buy_count, limit_turn)
            if 'pick_up_item_info_array' in free_data and free_data['pick_up_item_info_array'] is not None:
                pick_up_item_info_array = free_data['pick_up_item_info_array']
            # Inventory (item_id, num)
            if 'user_item_info_array' in free_data and free_data['user_item_info_array'] is not None:
                user_item_info_array = free_data['user_item_info_array']
            # List of rivals for this turn (program_id, chara_id)
            if 'rival_race_info_array' in free_data:
                rival_race_info_array = free_data['rival_race_info_array']
        if "race_condition_array" in data:
            races = data['race_condition_array']
        if "chara_info" in data:
            chara_info = data['chara_info']
            uma_aptitudes["proper_ground_turf"] = chara_info['proper_ground_turf']
            uma_aptitudes["proper_ground_dirt"] = chara_info['proper_ground_dirt']
            uma_aptitudes["proper_distance_short"] = chara_info['proper_distance_short']
            uma_aptitudes["proper_distance_mile"] = chara_info['proper_distance_mile']
            uma_aptitudes["proper_distance_middle"] = chara_info['proper_distance_middle']
            uma_aptitudes["proper_distance_long"] = chara_info['proper_distance_long']




        main_info = {
            "turn": turn,
            "scenario_id": scenario_id,
            "energy": energy,
            "max_energy": max_energy,
            "fans": fans,
            "skillpt": skillpt,
            "races_run": self._update_races_run(data),
            # Persisted by carrotjuicer._process_packet_events so choices survive
            # re-renders driven by packets that don't themselves carry the event.
            "event_choices": getattr(self.carrotjuicer, 'pending_event_choices', []),
            "event_choices_show_ids": self.carrotjuicer.threader.settings["event_choices_show_ids"],
            "shop_restock_program_ids": _get_shop_restock_races(),
            "scheduled_races": scheduled_races,
            "gm_fragments": gm_fragments,
            "gl_stats": gl_stats,
            "hint_partners": hint_partners,
            "arc_aptitude_points": arc_aptitude_points,
            "arc_expectation_gauge": arc_expectation_gauge,
            "arc_supporter_points": arc_supporter_points,
            "uaf_sport_ranks": uaf_sport_rank,
            "uaf_sport_rank_total": uaf_sport_rank_total,
            "uaf_current_required_rank": uaf_current_required_rank,
            "uaf_current_active_effects": uaf_current_active_effects,
            "uaf_current_active_bonus": uaf_current_active_bonus,
            "uaf_sport_competition": uaf_sport_competition,
            "uaf_consultations_left": uaf_consultations_left,
            "gff_great_success": gff_great_success,
            "gff_success_point": gff_success_point,
            "gff_cooking_point": gff_cooking_point,
            "gff_tasting_thres": gff_tasting_thres,
            "gff_tasting_great_thres": gff_tasting_great_thres,
            "gff_vegetables": gff_vegetables,
            "gff_field_point": gff_field_point,
            "eval_dict": eval_dict,
            "all_commands": all_commands,
            'races': races,
            'uma_aptitudes': uma_aptitudes,
            'pick_up_item_info_array': pick_up_item_info_array,
            'user_item_info_array': user_item_info_array,
            'rival_race_info_array': rival_race_info_array,
            'coin_num': coin_num,
            'sale_value': sale_value,
            'feeling_turn_info_array': feeling_turn_info_array,
            'special_feeling_num': special_feeling_num,
            'selected_region_id_array': selected_region_id_array
        }

        # Update preset if needed.
        if self.carrotjuicer.threader.settings['training_helper_table_scenario_presets_enabled']:
            scenario_preset = self.carrotjuicer.threader.settings['training_helper_table_scenario_presets'].get(str(scenario_id), None)
            if scenario_preset and self.selected_preset.name != scenario_preset:
                self.selected_preset = self.carrotjuicer.threader.settings.get_preset_with_name(scenario_preset)
        else:
            general_preset = self.carrotjuicer.threader.settings['training_helper_table_preset']
            if self.selected_preset.name != general_preset:
                self.selected_preset = self.carrotjuicer.threader.settings.get_preset_with_name(general_preset)

        overlay_html = self.selected_preset.generate_overlay(main_info, command_info)

        return overlay_html
