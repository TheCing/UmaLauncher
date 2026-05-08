"""End-of-career skill buy optimizer.

Given a `chara_info` dict from the current training packet, computes the subset of
purchasable skills that maximizes rating under the current skill-point budget.

Model
-----
Multiple-choice knapsack with a group_id mutex constraint (so the solver never
suggests buying both a white and its gold upgrade — only one skill per group_id
contributes to the rating slot). Solved via DP in O(G * B).

Hint discount
-------------
Uses the same canonical table as daftuyda/UmaTools' optimizer:

    Lv0: 0%   Lv1: 10%   Lv2: 20%   Lv3: 30%   Lv4: 35%   Lv5: 40%

The effective cost is `floor(base_cost * (1 - discount - fast_learner))`. Note
that Lv4→Lv5 is only +5%, not +10% — and the cap is 40%, not 50%.

Aptitude multiplier
-------------------
Rating is `grade_value * aptitude_multiplier`, where the multiplier depends on
the horse's aptitude for the skill's affinity_role (turf/dirt, sprint/mile/
medium/long, front/pace/late/end). Buckets (matching UmaTools' rating-shared.js):

    good=1.10 (S/A), average=0.90 (B/C), bad=0.80 (D/E/F), terrible=0.70 (G/none)

Multi-role skills like "Mile/Late" are split by '/', grouped into
surface / distance / style, the max multiplier is taken per group, and the
group multipliers are composed multiplicatively — e.g. Mile@A × Late@A =
1.10 × 1.10 = 1.21.

Affinity roles are sourced from UmaTools' `uma_skills.csv` (bundled at
`_assets/uma_skills.csv`), matched to MDB skills by name. Skills without a
CSV role match fall back to `base = 1.0` — the raw grade value.
"""
import csv
import os
from loguru import logger

import mdb
import util


# Matches daftuyda/UmaTools HINT_DISCOUNTS (js/optimizer.js).
HINT_DISCOUNTS = {0: 0.0, 1: 0.10, 2: 0.20, 3: 0.30, 4: 0.35, 5: 0.40}
MAX_HINT_LEVEL = 5
FAST_LEARNER_DISCOUNT = 0.0  # Optional trainee skill — toggle to 0.10 if present.

# Matches UmaTools' BUCKET_MULTIPLIER in rating-shared.js.
BUCKET_MULTIPLIER = {'good': 1.10, 'average': 0.90, 'bad': 0.80, 'terrible': 0.70, 'base': 1.0}

# Rarity values that identify the character's OWN unique skill (vs. an
# inherited/skill-of-a-parent unique). The character's unique is scored
# via unique_bonus (level × per-star-multiplier), NOT as a regular skill.
#   rarity=4 — evolved unique (only ~17 characters have these)
#   rarity=5 — base unique (every character has one)
#   rarity=3 — INHERITED unique passed from a parent in succession; this
#              is just a regular skill on the runner, no unique_bonus.
UNIQUE_OWN_RARITIES = {4, 5}


# Aptitude value (1-8) → bucket. 1=G, 2=F, 3=E, 4=D, 5=C, 6=B, 7=A, 8=S.
APTITUDE_BUCKETS = {
    8: 'good', 7: 'good',           # S, A
    6: 'average', 5: 'average',     # B, C
    4: 'bad', 3: 'bad', 2: 'bad',   # D, E, F
    1: 'terrible',                  # G
}

# Affinity role key → chara_info aptitude field name.
ROLE_TO_FIELD = {
    'turf':   'proper_ground_turf',
    'dirt':   'proper_ground_dirt',
    'sprint': 'proper_distance_short',
    'mile':   'proper_distance_mile',
    'medium': 'proper_distance_middle',
    'long':   'proper_distance_long',
    'front':  'proper_running_style_nige',
    'pace':   'proper_running_style_senko',
    'late':   'proper_running_style_sashi',
    'end':    'proper_running_style_oikomi',
}

# Affinity role → logical group. Multi-role skills take the max per group, then
# compose the groups multiplicatively (matches UmaTools' ROLE_GROUP).
ROLE_GROUP = {
    'turf': 'surface', 'dirt': 'surface',
    'sprint': 'distance', 'mile': 'distance', 'medium': 'distance', 'long': 'distance',
    'front': 'style', 'pace': 'style', 'late': 'style', 'end': 'style',
}


_SKILL_ROLE_CACHE = None
_STAT_SCORES_CACHE = None


def _build_stat_scores():
    """Port of UmaTools' STAT_SCORES lookup table (rating-shared.js).

    Returns a 2501-length list where `sc[stat] = rating contribution of that
    single stat`. Total stat rating = sum over speed/stamina/power/guts/wisdom.
    The formula has three piecewise rate regions: 0-1200, 1201-2000, 2001-2500.
    """
    R1 = [5, 8, 10, 13, 16, 18, 21, 24, 26, 28, 29, 30, 31, 33, 34, 35, 39, 41, 42, 43, 52, 55, 66, 68, 68]
    R2 = [79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 92, 93, 94, 96, 97, 98, 100, 101, 102, 103, 105,
          106, 107, 109, 110, 111, 113, 114, 115, 117, 118, 119, 121, 122, 123, 124, 126, 127, 128,
          130, 131, 132, 134, 135, 136, 138, 139, 140, 141, 143, 144, 145, 147, 148, 149, 151, 152,
          153, 155, 156, 157, 159, 160, 161, 162, 164, 165, 166, 168, 169, 170, 172, 173, 174, 176,
          177, 178, 179, 181, 182, 182]
    MAX_STAT_VALUE = 2500
    sc = [0] * (MAX_STAT_VALUE + 1)
    raw = 0
    idx = 0
    for c in range(1, 1201):
        if c <= 49:
            idx = 0
        elif c <= 99:
            idx = 1
        elif c % 50 == 0:
            idx += 1
        raw += R1[idx]
        sc[c] = round(raw / 10)
    raw = 38413
    idx = 0
    for c in range(1201, 2001):
        if c <= 1209:
            idx = 0
        elif c <= 1219:
            idx = 1
        elif c % 10 == 0:
            idx += 1
        raw += R2[idx]
        sc[c] = round(raw / 10)
    raw = 142796
    idx = 0
    rate = 183
    for c in range(2001, MAX_STAT_VALUE + 1):
        if idx >= 25:
            rate += 1
            idx = 0
        raw += rate
        idx += 1
        sc[c] = round(raw / 10)
    return sc


def _get_stat_scores():
    global _STAT_SCORES_CACHE
    if _STAT_SCORES_CACHE is None:
        _STAT_SCORES_CACHE = _build_stat_scores()
    return _STAT_SCORES_CACHE


def _clamp_stat(value):
    try:
        v = int(value)
    except (TypeError, ValueError):
        return 0
    return max(0, min(2500, v))


def _normalize_name(name):
    if not name:
        return ''
    return name.strip().lower()


def _load_skill_roles():
    """Parse uma_skills.csv once, return {normalized_name: affinity_role}.

    Builds the lookup from all three name columns (`name`, `alias_name`,
    `localized_name`) so we can match MDB entries regardless of whether the
    client is Global (EN) or JP.
    """
    global _SKILL_ROLE_CACHE
    if _SKILL_ROLE_CACHE is not None:
        return _SKILL_ROLE_CACHE

    path = util.get_asset(os.path.join('_assets', 'uma_skills.csv'))
    mapping = {}
    try:
        with open(path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                role = (row.get('affinity_role') or '').strip()
                if not role:
                    continue
                for key in ('name', 'alias_name', 'localized_name'):
                    nm = _normalize_name(row.get(key))
                    if nm:
                        mapping[nm] = role
    except FileNotFoundError:
        logger.warning(f"uma_skills.csv not found at {path} — skill recommender will use raw grades.")
    except Exception:
        logger.exception("Failed to load uma_skills.csv")

    _SKILL_ROLE_CACHE = mapping
    return _SKILL_ROLE_CACHE


def _effective_cost(base_cost, hint_level):
    """Apply hint discount. hint_level=0 means no hint."""
    lvl = max(0, min(MAX_HINT_LEVEL, int(hint_level)))
    discount = HINT_DISCOUNTS.get(lvl, 0.0) + FAST_LEARNER_DISCOUNT
    multiplier = max(0.0, 1.0 - discount)
    # UmaTools uses floor(rawCost + epsilon) to round down consistently.
    return max(0, int(base_cost * multiplier + 1e-9))


def _build_aptitude_buckets(chara_info):
    """Return {role_key: bucket} for all 10 roles from a chara_info dict."""
    out = {}
    for role, field in ROLE_TO_FIELD.items():
        val = chara_info.get(field, 0)
        out[role] = APTITUDE_BUCKETS.get(val, 'terrible')
    return out


def _aptitude_multiplier(role_str, buckets):
    """Compute the aptitude multiplier for a skill's affinity role string.

    Matches UmaTools' `evaluateSkillScore` logic:
      - Empty/unknown role → 1.0 (base)
      - Single role → BUCKET_MULTIPLIER[role_bucket]
      - Multi-role "X/Y" → group each by surface/distance/style, take max
        multiplier per group, then multiply groups together.
    """
    if not role_str:
        return 1.0
    parts = [p.strip().lower() for p in role_str.split('/') if p.strip()]
    if not parts:
        return 1.0

    if len(parts) == 1:
        role = parts[0]
        if role not in buckets:
            return 1.0
        return BUCKET_MULTIPLIER[buckets[role]]

    # Multi-role: per-group max, then compose.
    group_max = {}
    for role in parts:
        if role not in buckets:
            continue
        mult = BUCKET_MULTIPLIER[buckets[role]]
        grp = ROLE_GROUP.get(role, role)
        if grp not in group_max or mult > group_max[grp]:
            group_max[grp] = mult

    if not group_max:
        return 1.0
    factor = 1.0
    for mult in group_max.values():
        factor *= mult
    return factor


def build_candidate_pool(chara_info):
    """Build the list of purchasable end-state options from a chara_info packet.

    Models skill upgrade chains correctly: within a group_id, the variants
    are ordered by `group_rate` (○=1 → ◎=2 → gold=3, with ×=-1 as debuff).
    To END UP with a higher tier you must pay for every lower tier first
    (and only the topmost tier's grade contributes to rating). So instead
    of treating ○/◎/gold as independent alternatives at their raw costs,
    each is offered as an end-state option with its CUMULATIVE chain cost.

    Returns (pool, budget). Pool entries contain:
        skill_id, group_id, rarity, name, base_cost, hint_level, cost
        (cumulative SP for the whole chain to this tier), chain (list of
        skills that get bought along the way), base_grade, multiplier,
        grade (aptitude-adjusted).
    """
    chain_dict = mdb.get_skill_chain_dict()  # group_id -> sorted [(sid, gr, rar, cost, grade), ...]
    name_dict = mdb.get_skill_name_dict()
    role_map = _load_skill_roles()
    buckets = _build_aptitude_buckets(chara_info)

    budget = chara_info.get('skill_point', 0)
    owned_ids = {s['skill_id'] for s in chara_info.get('skill_array', [])}

    # Hints stored by (group_id, rarity) so we can apply the same discount to
    # every tier in that rarity within the group. (A "white hint Lv5" on the
    # Firm group covers both ○ and ◎ since they're both rarity=1.) Presence
    # of an entry also signals that this rarity is OFFERED in the end-of-
    # career shop — without it, gold tiers aren't purchasable even if a
    # lower tier is hinted.
    hint_by_group_rarity = {}
    for tip in chara_info.get('skill_tips_array', []):
        key = (tip['group_id'], tip['rarity'])
        level = tip.get('level', 1)
        if level > hint_by_group_rarity.get(key, 0):
            hint_by_group_rarity[key] = level

    card_id = chara_info.get('card_id', 0)
    talent_level = chara_info.get('talent_level', 99)
    inherent_ids = set(mdb.get_card_inherent_skills(card_id, talent_level))

    def _tier_offered(sid, gid, rar):
        """A specific tier is reachable in the shop if it's either inherent
        to the card or there's a hint at its (group_id, rarity)."""
        return sid in inherent_ids or (gid, rar) in hint_by_group_rarity

    # Reachable groups = anywhere any tier is offered.
    reachable_groups = {gid for gid, _rar in hint_by_group_rarity.keys()}
    for sid in inherent_ids:
        for g, members in chain_dict.items():
            if any(m[0] == sid for m in members):
                reachable_groups.add(g)
                break

    pool = []
    for gid in reachable_groups:
        members = chain_dict.get(gid)
        if not members:
            continue

        # Highest group_rate already owned in this chain (>0 only — debuffs
        # don't satisfy upgrade prerequisites).
        max_owned_gr = max(
            (gr for sid, gr, _rar, _c, _g in members if sid in owned_ids and gr > 0),
            default=0,
        )

        # Walk tiers in ascending group_rate, accumulating cost. Stop the
        # chain at any tier that's not reachable (so a chara without the
        # gold hint can't pretend they can buy a Demon-tier skill).
        cumulative_cost = 0
        cumulative_chain = []
        for sid, gr, rar, base_cost, base_grade in members:
            if gr <= 0:
                continue  # debuff, not part of upgrade chain
            if rar in UNIQUE_OWN_RARITIES:
                continue  # uniques aren't end-of-career-buyable
            if gr <= max_owned_gr:
                continue  # already own this tier or a higher one
            if not _tier_offered(sid, gid, rar):
                # This tier is not in the shop for this chara — chain ends here.
                break
            if base_grade <= 0:
                continue  # zero-grade skill, not worth buying

            hint_lv = hint_by_group_rarity.get((gid, rar), 0)
            tier_cost = _effective_cost(base_cost, hint_lv)
            cumulative_cost += tier_cost
            cumulative_chain.append({
                'skill_id': sid,
                'name': name_dict.get(sid, f"Skill {sid}"),
                'cost': tier_cost,
                'hint_level': hint_lv,
                'rarity': rar,
                'group_rate': gr,
            })

            # Viable end-state — emit it as a candidate.
            name = name_dict.get(sid, f"Skill {sid}")
            role = role_map.get(_normalize_name(name), '')
            multiplier = _aptitude_multiplier(role, buckets)
            grade = int(round(base_grade * multiplier))
            pool.append({
                'skill_id': sid,
                'group_id': gid,
                'rarity': rar,
                'name': name,
                'base_cost': base_cost,
                'hint_level': hint_lv,
                'cost': cumulative_cost,
                'chain': list(cumulative_chain),  # snapshot
                'base_grade': base_grade,
                'role': role,
                'multiplier': multiplier,
                'grade': grade,
            })

    return pool, budget


def _solve_knapsack_with_groups(items, budget):
    """0/1 knapsack with at-most-one-per-group constraint.

    `items` is a list of dicts with keys: cost, grade, group_id.
    Returns (selected_items, total_cost, total_grade).

    Strategy: bucket items by group_id, then DP over (group → pick-one-or-none).
    Classic multiple-choice knapsack — for each group we pre-pick the best among
    (none, item_a, item_b, ...) and build a DP table budget-indexed.
    """
    if budget <= 0 or not items:
        return [], 0, 0

    # Bucket by group_id.
    groups = {}
    for it in items:
        groups.setdefault(it['group_id'], []).append(it)

    group_list = list(groups.values())

    # dp[c] = max grade achievable with cost ≤ c
    # choice[g][c] = which item index within group g was picked (or -1 for none)
    dp = [0] * (budget + 1)
    choice = [[-1] * (budget + 1) for _ in group_list]

    for g_idx, group_items in enumerate(group_list):
        new_dp = dp[:]
        for c in range(budget + 1):
            # Option: skip the group (inherits dp[c])
            best_grade = dp[c]
            best_choice = -1
            for i, it in enumerate(group_items):
                if it['cost'] <= c:
                    prev = dp[c - it['cost']]
                    cand = prev + it['grade']
                    if cand > best_grade:
                        best_grade = cand
                        best_choice = i
            new_dp[c] = best_grade
            choice[g_idx][c] = best_choice
        dp = new_dp

    # Reconstruct selection
    selected = []
    c = budget
    for g_idx in range(len(group_list) - 1, -1, -1):
        pick = choice[g_idx][c]
        if pick >= 0:
            it = group_list[g_idx][pick]
            selected.append(it)
            c -= it['cost']

    selected.reverse()
    total_cost = sum(it['cost'] for it in selected)
    total_grade = sum(it['grade'] for it in selected)
    return selected, total_cost, total_grade


def compute_rating_breakdown(chara_info, extra_skill_score=0):
    """Estimate the horse's total rating using UmaTools' formula.

    Returns {stats, skills, unique, total}. The `extra_skill_score` parameter
    lets the caller add the recommender's buy delta so we can report a
    "post-buys" projection without re-scoring everything.

    Matches `calculateRatingBreakdown` in rating-shared.js:
        total = sum(calcStatScore(stat) for 5 stats)
              + unique_bonus(talent_level, unique_level)
              + sum(grade_value * aptitude_multiplier for owned skills)
    """
    stat_scores = _get_stat_scores()
    stats_total = (
        stat_scores[_clamp_stat(chara_info.get('speed', 0))]
        + stat_scores[_clamp_stat(chara_info.get('stamina', 0))]
        + stat_scores[_clamp_stat(chara_info.get('power', 0))]
        + stat_scores[_clamp_stat(chara_info.get('guts', 0))]
        + stat_scores[_clamp_stat(chara_info.get('wiz', 0))]
    )

    meta = mdb.get_skill_meta_dict()
    name_dict = mdb.get_skill_name_dict()
    role_map = _load_skill_roles()
    buckets = _build_aptitude_buckets(chara_info)

    owned_skill_score = 0
    unique_level = 0
    for s in chara_info.get('skill_array', []):
        sid = s.get('skill_id')
        row = meta.get(sid)
        if not row:
            continue
        base_grade, _group_id, rarity = row
        # Character's own unique skill — scored separately via unique_bonus.
        # See UNIQUE_OWN_RARITIES for which rarities qualify.
        if rarity in UNIQUE_OWN_RARITIES:
            unique_level = max(unique_level, int(s.get('level', 0)))
            continue
        if base_grade <= 0:
            # Skip debuffs (purple rarity 5) — they have negative grade and the
            # game doesn't count them toward rating anyway.
            continue
        name = name_dict.get(sid, '')
        role = role_map.get(_normalize_name(name), '')
        mult = _aptitude_multiplier(role, buckets)
        owned_skill_score += int(round(base_grade * mult))

    # Unique bonus: lvl × (120 if ≤2★ else 170). `talent_level` is the horse's
    # star rating (1-5). Matches UmaTools' calcUniqueBonus.
    star_level = chara_info.get('talent_level', 5) or 5
    mult_per_level = 120 if star_level in (1, 2) else 170
    unique_bonus = unique_level * mult_per_level

    skills_total = owned_skill_score + int(round(extra_skill_score))
    return {
        'stats': stats_total,
        'skills': skills_total,
        'unique': unique_bonus,
        'total': stats_total + skills_total + unique_bonus,
    }


def _skill_matches_filter(role_str, only_distance, only_style):
    """Returns True if the skill should be kept under the user's filter.

    Logic:
      - Skill with empty role: always kept (universal — applies to any horse).
      - only_distance set: skill kept only if it has no distance role component
        OR one of its distance components matches `only_distance`.
      - only_style set: same logic for style components.
      - Multi-role like 'Mile/Late' has both a distance ('mile') and a style
        ('late') component; both filters apply independently.
    """
    if not only_distance and not only_style:
        return True
    if not role_str:
        return True
    parts = [p.strip().lower() for p in role_str.split('/') if p.strip()]
    distances = [p for p in parts if ROLE_GROUP.get(p) == 'distance']
    styles = [p for p in parts if ROLE_GROUP.get(p) == 'style']
    if only_distance and distances and only_distance not in distances:
        return False
    if only_style and styles and only_style not in styles:
        return False
    return True


def recommend(chara_info, only_distance="", only_style=""):
    """Main entry point. Returns a dict with:
        selected: list of picked skill entries
        skipped:  list of unpicked candidates (sorted by grade-per-cost desc)
        budget:   SP available
        spent:    SP that would be spent
        rating:   total aptitude-adjusted rating gained from the recommended buys
        current_breakdown: rating breakdown of the horse as-is
        projected_breakdown: rating breakdown assuming the recommended buys go through

    `only_distance` and `only_style` (lowercase keys like 'mile', 'front')
    optionally constrain the candidate pool to skills that match. Skills
    with no role at all (universal) are always included.
    """
    pool, budget = build_candidate_pool(chara_info)
    if only_distance or only_style:
        pool = [it for it in pool if _skill_matches_filter(it.get('role', ''), only_distance, only_style)]
    current_breakdown = compute_rating_breakdown(chara_info)

    if not pool:
        return {
            'selected': [],
            'skipped': [],
            'budget': budget,
            'spent': 0,
            'rating': 0,
            'current_breakdown': current_breakdown,
            'projected_breakdown': current_breakdown,
        }

    selected, spent, rating = _solve_knapsack_with_groups(pool, budget)
    picked_ids = {it['skill_id'] for it in selected}
    skipped = [it for it in pool if it['skill_id'] not in picked_ids]
    # Sort skipped by value-per-cost descending so the "next best" is obvious.
    skipped.sort(key=lambda it: (it['grade'] / max(it['cost'], 1)), reverse=True)

    projected_breakdown = compute_rating_breakdown(chara_info, extra_skill_score=rating)

    return {
        'selected': selected,
        'skipped': skipped,
        'budget': budget,
        'spent': spent,
        'rating': rating,
        'current_breakdown': current_breakdown,
        'projected_breakdown': projected_breakdown,
    }


def format_html(result):
    """Render a recommendation dict as an HTML string suitable for show_info_box."""
    budget = result['budget']
    spent = result['spent']
    rating = result['rating']
    selected = result['selected']
    skipped = result['skipped']
    current = result.get('current_breakdown') or {}
    projected = result.get('projected_breakdown') or {}

    def total_line():
        if not current or not projected:
            return ""
        cur_total = current.get('total', 0)
        proj_total = projected.get('total', 0)
        delta = proj_total - cur_total
        stats = current.get('stats', 0)
        unique = current.get('unique', 0)
        cur_skills = current.get('skills', 0)
        proj_skills = projected.get('skills', 0)
        return (
            f"<b>Current rating:</b> {cur_total}"
            f" &nbsp;→&nbsp; <b>Post-buys cap:</b> {proj_total}"
            f" &nbsp;(<b>+{delta}</b>)<br>"
            f"<i>stats {stats} + unique {unique} + skills {cur_skills}"
            f" → {proj_skills}</i><br>"
        )

    if not selected and not skipped:
        return (
            total_line()
            + f"SP available: <b>{budget}</b><br>"
            + "No purchasable skills found — nothing to recommend."
        )

    def row(it, buy):
        tag = "[BUY]" if buy else ""
        hint_suffix = f" (hint Lv{it['hint_level']})" if it['hint_level'] > 0 else ""
        role_suffix = f" <i>[{it['role']}]</i>" if it.get('role') else ""
        mult = it.get('multiplier', 1.0)
        mult_tag = f" ×{mult:.2f}" if abs(mult - 1.0) > 1e-6 else ""
        # Surface the chain when buying an upgraded tier requires also paying
        # for prerequisites, e.g. "via ○ (90)" before reaching ◎.
        chain = it.get('chain') or []
        chain_note = ""
        if len(chain) > 1:
            prereqs = [f"{c['name']} ({c['cost']})" for c in chain[:-1]]
            chain_note = f"<br><small style='color:#888'>via {' → '.join(prereqs)}</small>"
        return (f"<tr><td>{tag}</td><td>{it['name']}{hint_suffix}{role_suffix}{chain_note}</td>"
                f"<td align='right'>{it['cost']}</td>"
                f"<td align='right'>+{it['grade']}{mult_tag}</td></tr>")

    lines = [
        total_line(),
        f"<b>SP budget:</b> {budget} &nbsp;|&nbsp; <b>Would spend:</b> {spent} &nbsp;|&nbsp; <b>Remaining:</b> {budget - spent}",
        f"<b>Rating gained:</b> +{rating} (aptitude-adjusted)",
        "<br><table cellpadding='4' cellspacing='0' border='0'>",
        "<tr><th></th><th align='left'>Skill</th><th>SP</th><th>Rating</th></tr>",
    ]
    for it in selected:
        lines.append(row(it, True))
    if skipped:
        lines.append("<tr><td colspan='4'><hr></td></tr>")
        lines.append("<tr><td colspan='4'><i>Not bought (ranked by rating/SP):</i></td></tr>")
        for it in skipped[:10]:
            lines.append(row(it, False))
    lines.append("</table>")
    return "".join(lines)
