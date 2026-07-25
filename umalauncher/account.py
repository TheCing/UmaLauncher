"""Account data capture and export from home screen packets."""

import json
import os
from datetime import datetime

from loguru import logger
import mdb
import util


# Singleton account data, populated on home screen load
_account_data = None


def capture_home_packet(data):
    """Capture account-level data from a home screen packet.

    Called from carrotjuicer.handle_response when a home screen packet is detected
    (has both 'common_define' and 'user_info').
    """
    global _account_data
    _account_data = {
        'captured_at': datetime.now().isoformat(),
        'user_info': data.get('user_info'),
        'support_card_list': data.get('support_card_list', []),
        'card_list': data.get('card_list', []),
        'chara_list': data.get('chara_list', []),
        'cloth_list': data.get('cloth_list', []),
        'piece_list': data.get('piece_list', []),
        'item_list': data.get('item_list', []),
        'coin_info': data.get('coin_info'),
        'trained_chara': data.get('trained_chara', []),
        'support_card_deck_array': data.get('support_card_deck_array', []),
        'team_data_array': data.get('team_data_array', []),
        'trained_chara_favorite_array': data.get('trained_chara_favorite_array', []),
        'music_list': data.get('music_list', []),
        'champions_info': data.get('champions_info'),
        'honor_info': data.get('honor_info'),
        # Archive sections
        'mission_list': data.get('mission_list', []),
        'main_story_data_list': data.get('main_story_data_list', []),
        'character_story_data_list': data.get('character_story_data_list', []),
        'extra_story_data_list': data.get('extra_story_data_list', []),
        'home_story_data_array': data.get('home_story_data_array', []),
        'released_episode_data_array': data.get('released_episode_data_array', []),
        'short_episode_data_array': data.get('short_episode_data_array', []),
        'talk_gallery_list': data.get('talk_gallery_list', []),
        'home_poster_data_array': data.get('home_poster_data_array', []),
        'tutorial_guide_data_array': data.get('tutorial_guide_data_array', []),
    }
    logger.info(f"Account data captured: {len(_account_data['support_card_list'])} support cards, "
                f"{len(_account_data['card_list'])} character cards, "
                f"{len(_account_data['chara_list'])} characters, "
                f"{len(_account_data['trained_chara'])} raised characters")


def get_account_data():
    """Return the raw captured account data, or None if not yet captured."""
    return _account_data


# Archive fields that appear in screen-specific packets (Missions screen,
# Story Archive, Music menu, etc.) rather than the home packet. We greedily
# update each whenever a non-empty value shows up so the export reflects
# the latest visited state.
_ARCHIVE_OPPORTUNISTIC_FIELDS = (
    'mission_list',
    'main_story_data_list',
    'character_story_data_list',
    'extra_story_data_list',
    'home_story_data_array',
    'released_episode_data_array',
    'short_episode_data_array',
    'talk_gallery_list',
    'home_poster_data_array',
    'tutorial_guide_data_array',
    'music_list',
    'cloth_list',
    'honor_info',
)


def merge_archive_fields(data):
    """Update any archive fields present in `data` into the cached account.

    Safe no-op if capture_home_packet hasn't initialised _account_data yet.
    Only overwrites with non-empty values so a later mission-screen packet
    doesn't get clobbered by an unrelated packet that happens to carry an
    empty key.
    """
    if _account_data is None:
        return
    for key in _ARCHIVE_OPPORTUNISTIC_FIELDS:
        if key not in data:
            continue
        val = data[key]
        if val is None:
            continue
        # Skip empty lists/dicts so we don't downgrade a populated cache.
        if isinstance(val, (list, dict)) and len(val) == 0:
            continue
        _account_data[key] = val


def _resolve_support_card(card):
    """Add human-readable name to a support card entry."""
    support_id = card.get('support_card_id')
    try:
        name = mdb.get_support_card_string(support_id)
    except Exception:
        name = f"Unknown ({support_id})"
    return {
        'support_card_id': support_id,
        'name': name,
        'exp': card.get('exp', 0),
        'limit_break_count': card.get('limit_break_count', 0),
        'favorite': bool(card.get('favorite_flag', 0)),
        'stock': card.get('stock', 0),
    }


def _resolve_character_card(card):
    """Add human-readable name to a character card entry."""
    card_id = card.get('card_id')
    chara_id = card_id // 100 if card_id else 0
    chara_names = mdb.get_chara_name_dict()
    outfit_names = mdb.get_outfit_name_dict()
    return {
        'card_id': card_id,
        'character': chara_names.get(chara_id, f"Unknown ({chara_id})"),
        'outfit': outfit_names.get(card_id, f"Unknown ({card_id})"),
        'rarity': card.get('rarity', 0),
        'talent_level': card.get('talent_level', 0),
    }


def _resolve_character(chara):
    """Add human-readable name to a base character entry."""
    chara_id = chara.get('chara_id')
    chara_names = mdb.get_chara_name_dict()
    return {
        'chara_id': chara_id,
        'name': chara_names.get(chara_id, f"Unknown ({chara_id})"),
        'training_num': chara.get('training_num', 0),
        'fan': chara.get('fan', 0),
        'max_grade': chara.get('max_grade', 0),
        'love_point': chara.get('love_point', 0),
    }


APTITUDE_LABELS = {1: 'G', 2: 'F', 3: 'E', 4: 'D', 5: 'C', 6: 'B', 7: 'A', 8: 'S', 9: 'SS'}
RUNNING_STYLE_LABELS = {1: 'Runner', 2: 'Leader', 3: 'Betweener', 4: 'Chaser'}


def _resolve_trained_chara(tc):
    """Add human-readable name and aptitude labels to a trained character."""
    card_id = tc.get('card_id')
    chara_id = card_id // 100 if card_id else 0
    chara_names = mdb.get_chara_name_dict()
    outfit_names = mdb.get_outfit_name_dict()
    return {
        'trained_chara_id': tc.get('trained_chara_id'),
        'card_id': card_id,
        'character': chara_names.get(chara_id, f"Unknown ({chara_id})"),
        'outfit': outfit_names.get(card_id, f"Unknown ({card_id})"),
        'rank_score': tc.get('rank_score', 0),
        'rank': tc.get('rank', 0),
        'stats': {
            'speed': tc.get('speed', 0),
            'stamina': tc.get('stamina', 0),
            'power': tc.get('power', 0),
            'guts': tc.get('guts', 0),
            'wisdom': tc.get('wiz', 0),
        },
        'running_style': RUNNING_STYLE_LABELS.get(tc.get('running_style'), tc.get('running_style')),
        'aptitudes': {
            'turf': APTITUDE_LABELS.get(tc.get('proper_ground_turf'), '?'),
            'dirt': APTITUDE_LABELS.get(tc.get('proper_ground_dirt'), '?'),
            'short': APTITUDE_LABELS.get(tc.get('proper_distance_short'), '?'),
            'mile': APTITUDE_LABELS.get(tc.get('proper_distance_mile'), '?'),
            'middle': APTITUDE_LABELS.get(tc.get('proper_distance_middle'), '?'),
            'long': APTITUDE_LABELS.get(tc.get('proper_distance_long'), '?'),
            'runner': APTITUDE_LABELS.get(tc.get('proper_running_style_nige'), '?'),
            'leader': APTITUDE_LABELS.get(tc.get('proper_running_style_senko'), '?'),
            'betweener': APTITUDE_LABELS.get(tc.get('proper_running_style_sashi'), '?'),
            'chaser': APTITUDE_LABELS.get(tc.get('proper_running_style_oikomi'), '?'),
        },
        'fans': tc.get('fans', 0),
        'wins': tc.get('wins', 0),
        'rarity': tc.get('rarity', 0),
        'talent_level': tc.get('talent_level', 0),
        'skill_count': len(tc.get('skill_array', [])),
        'race_count': len(tc.get('race_result_list', [])),
    }


def export_account(output_dir=None):
    """Export resolved account data to a human-readable JSON file.

    Returns the output file path, or None if no data captured yet.
    """
    if not _account_data:
        logger.warning("No account data captured yet. Navigate to the home screen first.")
        return None

    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'account_export')
    os.makedirs(output_dir, exist_ok=True)

    user = _account_data.get('user_info') or {}
    name = user.get('name', 'Unknown')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"account_{name}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    export = {
        'exported_at': datetime.now().isoformat(),
        'captured_at': _account_data['captured_at'],
        'user': {
            'name': user.get('name'),
            'viewer_id': user.get('viewer_id'),
            'rank_score': user.get('rank_score'),
            'total_fans': user.get('fan'),
            'best_team_evaluation': user.get('best_team_evaluation_point'),
            'registered': user.get('register_time'),
        },
        'currencies': _account_data.get('coin_info'),
        'support_cards': [_resolve_support_card(c) for c in _account_data['support_card_list']],
        'character_cards': [_resolve_character_card(c) for c in _account_data['card_list']],
        'characters': [_resolve_character(c) for c in _account_data['chara_list']],
        'raised_characters': [_resolve_trained_chara(tc) for tc in _account_data['trained_chara']],
        'support_decks': _account_data.get('support_card_deck_array', []),
        'items': _account_data.get('item_list', []),
        'pieces': _account_data.get('piece_list', []),
        'archive': {
            'honors': _account_data.get('honor_info') or {},
            'missions': _account_data.get('mission_list', []),
            'music_tracks': _account_data.get('music_list', []),
            'costumes': _account_data.get('cloth_list', []),
            'stories': {
                'main': _account_data.get('main_story_data_list', []),
                'character': _account_data.get('character_story_data_list', []),
                'extra': _account_data.get('extra_story_data_list', []),
                'home': _account_data.get('home_story_data_array', []),
            },
            'episodes': {
                'released': _account_data.get('released_episode_data_array', []),
                'short': _account_data.get('short_episode_data_array', []),
            },
            'talk_gallery': _account_data.get('talk_gallery_list', []),
            'home_posters': _account_data.get('home_poster_data_array', []),
            'tutorial_guides': _account_data.get('tutorial_guide_data_array', []),
        },
        'summary': {
            'support_cards': len(_account_data['support_card_list']),
            'character_cards': len(_account_data['card_list']),
            'characters': len(_account_data['chara_list']),
            'raised_characters': len(_account_data['trained_chara']),
            'costumes': len(_account_data.get('cloth_list', [])),
            'music_tracks': len(_account_data.get('music_list', [])),
            'honors': len((_account_data.get('honor_info') or {}).get('honor_list', [])),
            'missions': len(_account_data.get('mission_list', [])),
            'main_stories_read': len(_account_data.get('main_story_data_list', [])),
            'character_stories_read': len(_account_data.get('character_story_data_list', [])),
            'extra_stories_read': len(_account_data.get('extra_story_data_list', [])),
            'episodes_released': len(_account_data.get('released_episode_data_array', [])),
            'episodes_short': len(_account_data.get('short_episode_data_array', [])),
            'talk_gallery_entries': len(_account_data.get('talk_gallery_list', [])),
        },
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(export, f, indent=2, ensure_ascii=False)

    logger.info(f"Account exported to {filepath}")
    return filepath
