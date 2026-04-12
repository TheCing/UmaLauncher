# Uma Musume Packet Reference

Generated from **7790** packets (3895 requests, 3895 responses) across **13** training runs (Global).

Runs analyzed:
- Mejiro McQueen [End of Sky] - 2026_03_28_10_26_46
- Mihono Bourbon [Code Glaçage] - 2026_03_30_16_53_16
- Mihono Bourbon [Code Glaçage] - 2026_03_30_17_51_28
- Mihono Bourbon [Code Glaçage] - 2026_03_31_03_55_17
- Mihono Bourbon [Code Glaçage] - 2026_03_31_04_19_00
- Narita Brian [Maverick] - 2026_03_31_08_09_18
- Narita Brian [Maverick] - 2026_04_03_03_30_45
- Oguri Cap [Miraculous White Star] - 2026_03_29_03_01_26
- Oguri Cap [Miraculous White Star] - 2026_03_30_06_28_36
- Oguri Cap [Miraculous White Star] - 2026_03_30_08_32_20
- Oguri Cap [Miraculous White Star] - 2026_03_30_09_04_25
- Tamamo Cross [With Lightning Speed] - 2026_03_29_05_40_59
- Tamamo Cross [With Lightning Speed] - 2026_03_29_07_54_07

---

## Top-Level Request Keys

| Key | Type | Occurrences |
|-----|------|-------------|
| `chara_id` | int | 1774/3895 |
| `choice_number` | int | 1774/3895 |
| `command_group_id` | int | 405/3895 |
| `command_id` | int | 405/3895 |
| `command_type` | int | 405/3895 |
| `continue_type` | int | 42/3895 |
| `current_money` | int | 13/3895 |
| `current_succession_rank_point` | int | 13/3895 |
| `current_turn` | int | 3880/3895 |
| `current_vital` | int | 405/3895 |
| `event_id` | int | 1774/3895 |
| `exchange_item_info_array` | array | 245/3895 |
| `gain_skill_info_array` | array | 5/3895 |
| `is_short` | int | 331/3895 |
| `program_id` | int | 289/3895 |
| `select_id` | int | 405/3895 |
| `start_chara` | object | 13/3895 |
| `steam_id` | string | 3895/3895 |
| `steam_session_ticket` | string | 3895/3895 |
| `tp_info` | object | 13/3895 |
| `use_item_info_array` | array | 212/3895 |
| `use_tp` | int | 13/3895 |
| `viewer_id` | int | 3895/3895 |

## Top-Level Response Keys

| Key | Type | Occurrences |
|-----|------|-------------|
| `add_music` | null | 289/3895 |
| `add_trained_chara_array` | array | 13/3895 |
| `add_trophy_info` | array, null, object | 291/3895 |
| `chara_info` | object | 3564/3895 |
| `command_result` | object | 405/3895 |
| `effected_factor_array` | array | 2/3895 |
| `event_effected_factor_array` | array, null | 1774/3895 |
| `free_data_set` | object | 3494/3895 |
| `home_info` | object | 3276/3895 |
| `mission_list` | array | 15/3895 |
| `not_down_parameter_info` | object | 2179/3895 |
| `not_up_parameter_info` | object | 2179/3895 |
| `prev_chara_grade` | null | 2/3895 |
| `race_add_reward_info` | array | 291/3895 |
| `race_condition_array` | array | 2483/3895 |
| `race_history` | array | 291/3895 |
| `race_reward_info` | null, object | 291/3895 |
| `race_scenario` | null, string | 333/3895 |
| `race_start_info` | null, object | 2438/3895 |
| `reserved_race_array` | array | 15/3895 |
| `reward_summary_info` | object | 289/3895 |
| `start_dress_info` | array | 2/3895 |
| `story_event_chara_bonus_list` | array | 15/3895 |
| `story_event_mission_list` | array | 15/3895 |
| `tp_info` | object | 13/3895 |
| `trophy_reward_info` | null, object | 291/3895 |
| `unchecked_event_array` | array | 2813/3895 |
| `user_item` | null, object | 42/3895 |
| `user_item_array` | array | 13/3895 |
| `win_saddle_id_array` | array | 291/3895 |

---

## Nested Key Reference

### `add_trained_chara_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `add_trained_chara_array[].arrive_route_race_id` | int | 10 | 168, 320, 490 |
| `add_trained_chara_array[].card_id` | int | 10 | 101901, 102602, 106001 |
| `add_trained_chara_array[].chara_grade` | int | 10 | 10, 9 |
| `add_trained_chara_array[].chara_seed` | int | 10 | 1064912302, 1224049813, 395298886 |
| `add_trained_chara_array[].create_time` | string | 10 | 2025-12-13 20:26:37, 2026-03-10 01:12:30, 2026-03-21 17:48:37 |
| `add_trained_chara_array[].factor_id_array` | array | 10 |  |
| `add_trained_chara_array[].factor_info_array` | array | 10 |  |
| `add_trained_chara_array[].factor_info_array[].factor_id` | int | 10 | 203, 303 |
| `add_trained_chara_array[].factor_info_array[].level` | int | 10 | 0 |
| `add_trained_chara_array[].fans` | int | 10 | 278077, 419124, 615202 |
| `add_trained_chara_array[].guts` | int | 10 | 327, 393, 444 |
| `add_trained_chara_array[].is_locked` | int | 10 | 1 |
| `add_trained_chara_array[].is_saved` | int | 10 | 0 |
| `add_trained_chara_array[].nickname_id` | int | 10 | 104, 150, 155 |
| `add_trained_chara_array[].nickname_id_array` | array | 10 |  |
| `add_trained_chara_array[].owner_trained_chara_id` | int | 10 | 2364, 2955, 73 |
| `add_trained_chara_array[].owner_viewer_id` | int | 10 | 115894380675, 375735673971, 480608246985 |
| `add_trained_chara_array[].power` | int | 10 | 1135, 786, 899 |
| `add_trained_chara_array[].proper_distance_long` | int | 10 | 1, 7 |
| `add_trained_chara_array[].proper_distance_middle` | int | 10 | 7, 8 |
| `add_trained_chara_array[].proper_distance_mile` | int | 10 | 7 |
| `add_trained_chara_array[].proper_distance_short` | int | 10 | 1, 2, 5 |
| `add_trained_chara_array[].proper_ground_dirt` | int | 10 | 1, 7 |
| `add_trained_chara_array[].proper_ground_turf` | int | 10 | 7 |
| `add_trained_chara_array[].proper_running_style_nige` | int | 10 | 1, 2, 7 |
| `add_trained_chara_array[].proper_running_style_oikomi` | int | 10 | 1, 4, 8 |
| `add_trained_chara_array[].proper_running_style_sashi` | int | 10 | 1, 7 |
| `add_trained_chara_array[].proper_running_style_senko` | int | 10 | 4, 6, 7 |
| `add_trained_chara_array[].race_cloth_id` | int | 10 | 101901, 102613, 106001 |
| `add_trained_chara_array[].race_result_list` | array | 10 |  |
| `add_trained_chara_array[].race_result_list[].ground_condition` | int | 10 | 1, 4 |
| `add_trained_chara_array[].race_result_list[].popularity` | int | 10 | 1 |
| `add_trained_chara_array[].race_result_list[].prize_money` | int | 10 | 0 |
| `add_trained_chara_array[].race_result_list[].program_id` | int | 10 | 1067, 1075, 846 |
| `add_trained_chara_array[].race_result_list[].result_rank` | int | 10 | 1 |
| `add_trained_chara_array[].race_result_list[].result_time` | int | 10 | 1161462, 910112, 932131 |
| `add_trained_chara_array[].race_result_list[].running_style` | int | 10 | 1, 2, 3 |
| `add_trained_chara_array[].race_result_list[].turn` | int | 10 | 12 |
| `add_trained_chara_array[].race_result_list[].weather` | int | 10 | 1, 3 |
| `add_trained_chara_array[].rank` | int | 10 | 14 |
| `add_trained_chara_array[].rank_score` | int | 10 | 12292, 13199, 13207 |
| `add_trained_chara_array[].rarity` | int | 10 | 3, 4 |
| `add_trained_chara_array[].register_time` | string | 10 | 2025-12-13 20:26:37, 2026-03-10 01:12:30, 2026-03-21 17:48:37 |
| `add_trained_chara_array[].route_id` | int | 10 | 15, 27, 40 |
| `add_trained_chara_array[].running_style` | int | 10 | 1, 2, 3 |
| `add_trained_chara_array[].scenario_id` | int | 10 | 1, 2 |
| `add_trained_chara_array[].single_mode_chara_id` | int | 10 | 0 |
| `add_trained_chara_array[].skill_array` | array | 10 |  |
| `add_trained_chara_array[].skill_array[].level` | int | 10 | 3, 4, 5 |
| `add_trained_chara_array[].skill_array[].skill_id` | int | 10 | 100191, 100601, 110261 |
| `add_trained_chara_array[].speed` | int | 10 | 1017, 1058, 1107 |
| `add_trained_chara_array[].stamina` | int | 10 | 664, 740, 796 |
| `add_trained_chara_array[].succession_chara_array` | array | 10 |  |
| `add_trained_chara_array[].succession_chara_array[].card_id` | int | 10 | 100801, 101102, 102701 |
| `add_trained_chara_array[].succession_chara_array[].factor_id_array` | array | 10 |  |
| `add_trained_chara_array[].succession_chara_array[].factor_info_array` | array | 10 |  |
| `add_trained_chara_array[].succession_chara_array[].factor_info_array[].factor_id` | int | 10 | 203, 303 |
| `add_trained_chara_array[].succession_chara_array[].factor_info_array[].level` | int | 10 | 0 |
| `add_trained_chara_array[].succession_chara_array[].owner_viewer_id` | int | 10 | 115894380675, 480608246985, 942104920468 |
| `add_trained_chara_array[].succession_chara_array[].position_id` | int | 10 | 10 |
| `add_trained_chara_array[].succession_chara_array[].rank` | int | 10 | 13 |
| `add_trained_chara_array[].succession_chara_array[].rarity` | int | 10 | 2, 3 |
| `add_trained_chara_array[].succession_chara_array[].talent_level` | int | 10 | 1, 2 |
| `add_trained_chara_array[].succession_chara_array[].win_saddle_id_array` | array | 10 |  |
| `add_trained_chara_array[].succession_history_array` | array | 10 |  |
| `add_trained_chara_array[].succession_num` | int | 10 | 16, 19, 24 |
| `add_trained_chara_array[].succession_trained_chara_id_1` | int | 10 | 0 |
| `add_trained_chara_array[].succession_trained_chara_id_2` | int | 10 | 0 |
| `add_trained_chara_array[].support_card_list` | array | 10 |  |
| `add_trained_chara_array[].support_card_list[].exp` | int | 10 | 118185, 82935 |
| `add_trained_chara_array[].support_card_list[].limit_break_count` | int | 10 | 3, 4 |
| `add_trained_chara_array[].support_card_list[].position` | int | 10 | 1 |
| `add_trained_chara_array[].support_card_list[].support_card_id` | int | 10 | 30028, 30036, 30086 |
| `add_trained_chara_array[].talent_level` | int | 10 | 4, 5 |
| `add_trained_chara_array[].trained_chara_id` | int | 10 | 2553, 2576, 2579, 2583, 2586 |
| `add_trained_chara_array[].use_type` | int | 10 | 1 |
| `add_trained_chara_array[].viewer_id` | int | 10 | 159392583559 |
| `add_trained_chara_array[].win_saddle_id_array` | array | 10 |  |
| `add_trained_chara_array[].wins` | int | 10 | 12, 14, 21 |
| `add_trained_chara_array[].wiz` | int | 10 | 304, 771, 989 |

### `add_trophy_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `add_trophy_info.chara_id_array` | array | 27 |  |
| `add_trophy_info.trophy_id` | int | 27 | 2020, 2028, 3019, 3023, 3036 |

### `chara_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `chara_info.card_id` | int | 3564 | 100602, 101302, 101601, 102101, 102602 |
| `chara_info.chara_effect_id_array` | array | 3564 |  |
| `chara_info.chara_grade` | int | 3564 | 1, 3, 4, 5, 6 |
| `chara_info.default_max_guts` | int | 3564 | 1200 |
| `chara_info.default_max_power` | int | 3564 | 1200 |
| `chara_info.default_max_speed` | int | 3564 | 1200 |
| `chara_info.default_max_stamina` | int | 3564 | 1200 |
| `chara_info.default_max_wiz` | int | 3564 | 1200 |
| `chara_info.disable_skill_id_array` | array | 3564 |  |
| `chara_info.evaluation_info_array` | array | 3564 |  |
| `chara_info.evaluation_info_array[].evaluation` | int | 3564 | 35, 42, 47, 52, 59 |
| `chara_info.evaluation_info_array[].group_outing_info_array` | array | 3564 |  |
| `chara_info.evaluation_info_array[].is_appear` | int | 3564 | 1 |
| `chara_info.evaluation_info_array[].is_outing` | int | 3564 | 0 |
| `chara_info.evaluation_info_array[].story_step` | int | 3564 | 0 |
| `chara_info.evaluation_info_array[].target_id` | int | 3564 | 1 |
| `chara_info.evaluation_info_array[].training_partner_id` | int | 3564 | 1 |
| `chara_info.fans` | int | 3564 | 1, 13844, 1393, 1447, 7679 |
| `chara_info.guest_outing_info_array` | array | 3564 |  |
| `chara_info.guts` | int | 3564 | 150, 159, 170, 182, 188 |
| `chara_info.is_short_race` | int | 3564 | 0, 1 |
| `chara_info.max_guts` | int | 3564 | 1200 |
| `chara_info.max_power` | int | 3564 | 1200 |
| `chara_info.max_speed` | int | 3564 | 1200 |
| `chara_info.max_stamina` | int | 3564 | 1200 |
| `chara_info.max_vital` | int | 3564 | 100, 104, 108, 112, 116 |
| `chara_info.max_wiz` | int | 3564 | 1200 |
| `chara_info.motivation` | int | 3564 | 1, 2, 3, 4, 5 |
| `chara_info.nickname_id_array` | array | 3564 |  |
| `chara_info.playing_state` | int | 3564 | 1, 2, 4, 5 |
| `chara_info.power` | int | 3564 | 110, 115, 117, 125, 130 |
| `chara_info.proper_distance_long` | int | 3564 | 7, 8 |
| `chara_info.proper_distance_middle` | int | 3564 | 7, 8 |
| `chara_info.proper_distance_mile` | int | 3564 | 2, 4, 7, 8 |
| `chara_info.proper_distance_short` | int | 3564 | 1, 2, 3, 5 |
| `chara_info.proper_ground_dirt` | int | 3564 | 1, 2, 3, 6 |
| `chara_info.proper_ground_turf` | int | 3564 | 7 |
| `chara_info.proper_running_style_nige` | int | 3564 | 1, 2, 3, 6, 7 |
| `chara_info.proper_running_style_oikomi` | int | 3564 | 1, 3, 4, 7 |
| `chara_info.proper_running_style_sashi` | int | 3564 | 1, 4, 7 |
| `chara_info.proper_running_style_senko` | int | 3564 | 3, 7 |
| `chara_info.race_program_id` | int | 3564 | 0, 1069, 1075, 629, 630 |
| `chara_info.race_running_style` | int | 3564 | 1, 2, 3, 4 |
| `chara_info.rarity` | int | 3564 | 4, 5 |
| `chara_info.reserve_race_program_id` | int | 3564 | 0 |
| `chara_info.route_id` | int | 3564 | 10004, 5 |
| `chara_info.route_race_id_array` | array | 3564 |  |
| `chara_info.scenario_id` | int | 3564 | 1, 4 |
| `chara_info.short_cut_state` | int | 3564 | 1 |
| `chara_info.single_mode_chara_id` | int | 3564 | 753, 760, 761, 762, 763 |
| `chara_info.skill_array` | array | 3564 |  |
| `chara_info.skill_array[].level` | int | 3564 | 2, 3, 4, 5, 6 |
| `chara_info.skill_array[].skill_id` | int | 3564 | 100161, 100211, 110061, 110131, 110261 |
| `chara_info.skill_point` | int | 3564 | 0, 120, 122, 124, 134 |
| `chara_info.skill_tips_array` | array | 3564 |  |
| `chara_info.skill_tips_array[].group_id` | int | 3564 | 20001, 20033, 20054, 20156, 90007 |
| `chara_info.skill_tips_array[].level` | int | 3564 | 1, 2, 3, 4 |
| `chara_info.skill_tips_array[].rarity` | int | 3564 | 1, 2 |
| `chara_info.speed` | int | 3564 | 129, 133, 139, 141, 146 |
| `chara_info.stamina` | int | 3564 | 245, 250, 260, 266, 275 |
| `chara_info.start_time` | string | 3564 | 2026-03-28 10:26:46, 2026-03-30 16:53:16, 2026-03-30 17:51:28, 2026-03-31 03:... |
| `chara_info.state` | int | 3564 | 0, 2, 3 |
| `chara_info.succession_trained_chara_id_1` | int | 3564 | 1389, 1431, 2516, 2536, 2559 |
| `chara_info.succession_trained_chara_id_2` | int | 3564 | 2521, 2578, 2581, 2585, 2588 |
| `chara_info.support_card_array` | array | 3564 |  |
| `chara_info.support_card_array[].exp` | int | 3564 | 118185 |
| `chara_info.support_card_array[].limit_break_count` | int | 3564 | 4 |
| `chara_info.support_card_array[].owner_viewer_id` | int | 3564 | 0 |
| `chara_info.support_card_array[].position` | int | 3564 | 1 |
| `chara_info.support_card_array[].support_card_id` | int | 3564 | 30028, 30078, 30086 |
| `chara_info.talent_level` | int | 3564 | 3, 5 |
| `chara_info.training_level_info_array` | array | 3564 |  |
| `chara_info.training_level_info_array[].command_id` | int | 3564 | 101 |
| `chara_info.training_level_info_array[].level` | int | 3564 | 1, 2, 3, 4 |
| `chara_info.turn` | int | 3564 | 1, 2, 3, 4, 5 |
| `chara_info.vital` | int | 3564 | 100, 61, 81, 91, 96 |
| `chara_info.wiz` | int | 3564 | 166, 179, 197, 202, 204 |

### `command_result`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `command_result.command_id` | int | 405 | 101, 102, 103, 105, 106 |
| `command_result.result_state` | int | 405 | 1, 2 |
| `command_result.sub_id` | int | 405 | 1, 1001, 1002, 1013, 1016 |

### `effected_factor_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `effected_factor_array[].factor_id_array` | array | 2 |  |
| `effected_factor_array[].factor_info_array` | array | 2 |  |
| `effected_factor_array[].factor_info_array[].factor_id` | int | 2 | 202, 301 |
| `effected_factor_array[].factor_info_array[].level` | int | 2 | 0 |
| `effected_factor_array[].position` | int | 2 | 10 |

### `event_effected_factor_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `event_effected_factor_array[].factor_id_array` | array | 17 |  |
| `event_effected_factor_array[].factor_info_array` | array | 17 |  |
| `event_effected_factor_array[].factor_info_array[].factor_id` | int | 17 | 202, 203, 301, 302 |
| `event_effected_factor_array[].factor_info_array[].level` | int | 17 | 0 |
| `event_effected_factor_array[].position` | int | 17 | 10 |

### `exchange_item_info_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `exchange_item_info_array[].current_num` | int | 245 | 0, 1, 2, 3, 4 |
| `exchange_item_info_array[].shop_item_id` | int | 245 | 10, 13, 23, 5, 8 |

### `free_data_set`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `free_data_set.coin_num` | int | 3494 | 0, 100, 145, 20, 45 |
| `free_data_set.command_info_array` | array | 3494 |  |
| `free_data_set.command_info_array[].command_id` | int | 3494 | 101, 601 |
| `free_data_set.command_info_array[].command_type` | int | 3494 | 1 |
| `free_data_set.command_info_array[].params_inc_dec_info_array` | array | 3494 |  |
| `free_data_set.command_info_array[].params_inc_dec_info_array[].target_type` | int | 593 | 1, 3 |
| `free_data_set.command_info_array[].params_inc_dec_info_array[].value` | int | 593 | 11, 13, 17, 4, 9 |
| `free_data_set.gained_coin_num` | int | 3494 | 0, 100, 60 |
| `free_data_set.item_effect_array` | array, null (null: 2580x) | 3494 |  |
| `free_data_set.item_effect_array[].begin_turn` | int | 914 | 23, 31, 33, 37, 39 |
| `free_data_set.item_effect_array[].effect_type` | int | 914 | 11, 13, 14 |
| `free_data_set.item_effect_array[].effect_value_1` | int | 914 | 0, 101, 105, 40, 6 |
| `free_data_set.item_effect_array[].effect_value_2` | int | 914 | 20, 35, 40, 50, 60 |
| `free_data_set.item_effect_array[].effect_value_3` | int | 914 | 0 |
| `free_data_set.item_effect_array[].effect_value_4` | int | 914 | 0 |
| `free_data_set.item_effect_array[].end_turn` | int | 914 | 23, 31, 33, 38, 39 |
| `free_data_set.item_effect_array[].item_id` | int | 914 | 11001, 11002, 8002, 8003, 9002 |
| `free_data_set.item_effect_array[].use_id` | int | 914 | 1, 2, 3, 4, 5 |
| `free_data_set.pick_up_item_info_array` | array, null (null: 453x) | 3494 |  |
| `free_data_set.pick_up_item_info_array[].coin_num` | int | 3041 | 30, 40, 49, 55, 70 |
| `free_data_set.pick_up_item_info_array[].item_buy_num` | int | 3041 | 0, 1 |
| `free_data_set.pick_up_item_info_array[].item_id` | int | 3041 | 10001, 1202, 2301, 8002, 8003 |
| `free_data_set.pick_up_item_info_array[].limit_buy_count` | int | 3041 | 1 |
| `free_data_set.pick_up_item_info_array[].limit_turn` | int | 3041 | 0, 19, 20, 25, 26 |
| `free_data_set.pick_up_item_info_array[].original_coin_num` | int | 3041 | 150, 30, 40, 55, 70 |
| `free_data_set.pick_up_item_info_array[].shop_item_id` | int | 3041 | 1, 11, 14, 26, 7 |
| `free_data_set.prev_win_points` | int | 3494 | 0, 1040, 1240, 486, 510 |
| `free_data_set.rival_race_info_array` | array | 3494 |  |
| `free_data_set.rival_race_info_array[].chara_id` | int | 2350 | 1004, 1018, 1051, 1054, 1059 |
| `free_data_set.rival_race_info_array[].program_id` | int | 2350 | 627, 628, 629, 630, 632 |
| `free_data_set.sale_value` | int | 3494 | 0, 10, 20 |
| `free_data_set.shop_id` | int | 3494 | 0, 1, 2, 3, 4 |
| `free_data_set.twinkle_race_npc_info_array` | array | 3494 |  |
| `free_data_set.twinkle_race_npc_info_array[].chara_id` | int | 165 | 1001, 1005, 1006 |
| `free_data_set.twinkle_race_npc_info_array[].dress_id` | int | 165 | 100101, 100501, 100601 |
| `free_data_set.twinkle_race_npc_info_array[].guts` | int | 165 | 394, 398, 449, 457, 486 |
| `free_data_set.twinkle_race_npc_info_array[].npc_id` | int | 165 | 1001900, 1005900, 1006900 |
| `free_data_set.twinkle_race_npc_info_array[].power` | int | 165 | 461, 462, 528, 532, 563 |
| `free_data_set.twinkle_race_npc_info_array[].proper_distance_long` | int | 165 | 3, 6, 7 |
| `free_data_set.twinkle_race_npc_info_array[].proper_distance_middle` | int | 165 | 7 |
| `free_data_set.twinkle_race_npc_info_array[].proper_distance_mile` | int | 165 | 6, 7 |
| `free_data_set.twinkle_race_npc_info_array[].proper_distance_short` | int | 165 | 6, 7 |
| `free_data_set.twinkle_race_npc_info_array[].proper_ground_dirt` | int | 165 | 2, 6 |
| `free_data_set.twinkle_race_npc_info_array[].proper_ground_turf` | int | 165 | 7 |
| `free_data_set.twinkle_race_npc_info_array[].proper_running_style_nige` | int | 165 | 1, 2, 5 |
| `free_data_set.twinkle_race_npc_info_array[].proper_running_style_oikomi` | int | 165 | 1, 4, 5 |
| `free_data_set.twinkle_race_npc_info_array[].proper_running_style_sashi` | int | 165 | 5, 7 |
| `free_data_set.twinkle_race_npc_info_array[].proper_running_style_senko` | int | 165 | 7 |
| `free_data_set.twinkle_race_npc_info_array[].skill_array` | array | 165 |  |
| `free_data_set.twinkle_race_npc_info_array[].skill_array[].level` | int | 165 | 1 |
| `free_data_set.twinkle_race_npc_info_array[].skill_array[].skill_id` | int | 165 | 200032, 200222, 200511, 200602, 201071 |
| `free_data_set.twinkle_race_npc_info_array[].speed` | int | 165 | 469, 474, 537, 573, 574 |
| `free_data_set.twinkle_race_npc_info_array[].stamina` | int | 165 | 495, 497, 566, 574, 607 |
| `free_data_set.twinkle_race_npc_info_array[].talent_level` | int | 165 | 1 |
| `free_data_set.twinkle_race_npc_info_array[].win_points` | int | 165 | 0, 2, 3, 4, 5 |
| `free_data_set.twinkle_race_npc_info_array[].wiz` | int | 165 | 428, 431, 482, 490, 524 |
| `free_data_set.twinkle_race_npc_result_array` | array | 3494 |  |
| `free_data_set.twinkle_race_npc_result_array[].program_id` | int | 124 | 2308, 2310, 2314, 2316, 2318 |
| `free_data_set.twinkle_race_npc_result_array[].race_result_array` | array | 124 |  |
| `free_data_set.twinkle_race_npc_result_array[].race_result_array[].npc_id` | int | 124 | 1001900, 1005900, 1006900 |
| `free_data_set.twinkle_race_npc_result_array[].race_result_array[].result_rank` | int | 124 | 15, 16, 17, 2, 6 |
| `free_data_set.twinkle_race_npc_result_array[].turn` | int | 124 | 74 |
| `free_data_set.twinkle_race_ranking` | int | 3494 | 0, 1 |
| `free_data_set.unchecked_event_achievement_id` | int, null (null: 3398x) | 3494 | 22, 28, 31, 34, 35 |
| `free_data_set.user_item_info_array` | array, null (null: 553x) | 3494 |  |
| `free_data_set.user_item_info_array[].item_id` | int | 2941 | 11001, 2001, 2002, 2101, 8002 |
| `free_data_set.user_item_info_array[].num` | int | 2941 | 1, 2, 3, 4 |
| `free_data_set.win_points` | int | 3494 | 0, 10, 130, 190, 70 |

### `gain_skill_info_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `gain_skill_info_array[].level` | int | 5 | 1 |
| `gain_skill_info_array[].skill_id` | int | 5 | 900451, 900681, 910111 |

### `home_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `home_info.available_continue_num` | int | 3276 | 1, 2, 3, 4, 5 |
| `home_info.available_free_continue_num` | int | 3276 | 0, 1 |
| `home_info.command_info_array` | array | 3276 |  |
| `home_info.command_info_array[].command_id` | int | 3276 | 101, 601 |
| `home_info.command_info_array[].command_type` | int | 3276 | 1 |
| `home_info.command_info_array[].failure_rate` | int | 3276 | 0, 17, 18, 20, 7 |
| `home_info.command_info_array[].is_enable` | int | 3276 | 0, 1 |
| `home_info.command_info_array[].level` | int | 3276 | 1, 2, 3, 4, 5 |
| `home_info.command_info_array[].params_inc_dec_info_array` | array | 3276 |  |
| `home_info.command_info_array[].params_inc_dec_info_array[].target_type` | int | 3276 | 1, 3 |
| `home_info.command_info_array[].params_inc_dec_info_array[].value` | int | 3276 | 10, 11, 12, 13, 15 |
| `home_info.command_info_array[].tips_event_partner_array` | array | 3276 |  |
| `home_info.command_info_array[].training_partner_array` | array | 3276 |  |
| `home_info.disable_command_id_array` | array | 3276 |  |
| `home_info.free_continue_num` | int | 3276 | 1 |
| `home_info.free_continue_time` | int | 3276 | 1774669385, 1774758440, 1774887447, 1774981671, 1775187432 |
| `home_info.race_entry_restriction` | int | 3276 | 0, 1 |
| `home_info.shortened_race_state` | int | 3276 | 4 |

### `mission_list[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `mission_list[].event_id` | int | 15 | 146, 147 |
| `mission_list[].exec_count` | int | 15 | 0 |
| `mission_list[].mission_id` | int | 15 | 1001125, 1001135 |
| `mission_list[].mission_status` | int | 15 | 0 |
| `mission_list[].mission_type` | int | 15 | 4 |

### `not_down_parameter_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `not_down_parameter_info.evaluation_chara_id_array` | array | 2179 |  |

### `not_up_parameter_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `not_up_parameter_info.chara_effect_id_array` | array | 2179 |  |
| `not_up_parameter_info.command_lv_array` | array | 2179 |  |
| `not_up_parameter_info.evaluation_chara_id_array` | array | 2179 |  |
| `not_up_parameter_info.has_chara_effect_id_array` | array | 2179 |  |
| `not_up_parameter_info.not_gain_chara_effect_array` | array | 2179 |  |
| `not_up_parameter_info.skill_id_array` | array | 2179 |  |
| `not_up_parameter_info.skill_lv_id_array` | array | 2179 |  |
| `not_up_parameter_info.skill_tips_array` | array | 2179 |  |
| `not_up_parameter_info.status_type_array` | array | 2179 |  |
| `not_up_parameter_info.unsupported_evaluation_chara_id_array` | array | 2179 |  |

### `race_condition_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `race_condition_array[].ground_condition` | int | 2165 | 1, 2, 3, 4 |
| `race_condition_array[].program_id` | int | 2165 | 1069, 298, 304, 638, 808 |
| `race_condition_array[].weather` | int | 2165 | 1, 2, 3, 4 |

### `race_history[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `race_history[].frame_order` | int | 291 | 1, 3, 5, 8, 9 |
| `race_history[].ground_condition` | int | 291 | 1, 2, 3, 4 |
| `race_history[].program_id` | int | 291 | 1069, 1070, 1075, 1078 |
| `race_history[].result_rank` | int | 291 | 1 |
| `race_history[].running_style` | int | 291 | 1, 2, 3, 4 |
| `race_history[].turn` | int | 291 | 12 |
| `race_history[].weather` | int | 291 | 1, 2, 3 |

### `race_reward_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `race_reward_info.campaign_id_array` | array | 289 |  |
| `race_reward_info.gained_coin_num` | int | 17 | 0 |
| `race_reward_info.gained_fans` | int | 289 | 1392, 1446, 6165, 6286, 6563 |
| `race_reward_info.race_reward` | array | 289 |  |
| `race_reward_info.race_reward[].item_id` | int | 289 | 59, 73, 75, 89, 92 |
| `race_reward_info.race_reward[].item_num` | int | 289 | 1200, 2, 40, 400, 800 |
| `race_reward_info.race_reward[].item_type` | int | 289 | 11, 30, 91, 93 |
| `race_reward_info.race_reward_bonus` | array | 289 |  |
| `race_reward_info.race_reward_bonus[].item_id` | int | 134 | 110, 43, 59 |
| `race_reward_info.race_reward_bonus[].item_num` | int | 134 | 10, 1200, 40, 80, 800 |
| `race_reward_info.race_reward_bonus[].item_type` | int | 134 | 30, 90, 91 |
| `race_reward_info.race_reward_bonus_win` | array | 289 |  |
| `race_reward_info.race_reward_plus_bonus` | array | 289 |  |
| `race_reward_info.result_rank` | int | 289 | 1, 11, 17, 2, 3 |
| `race_reward_info.result_time` | int | 289 | 1048962, 1162469, 898577, 911124, 913810 |

### `race_start_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `race_start_info.continue_num` | int | 784 | 0, 1, 2, 3 |
| `race_start_info.ground_condition` | int | 784 | 1, 2, 3, 4 |
| `race_start_info.program_id` | int | 784 | 1069, 1075, 629, 630, 632 |
| `race_start_info.race_horse_data` | array | 784 |  |
| `race_start_info.race_horse_data[].card_id` | int | 784 | 100602, 101302, 101601, 102101, 102602 |
| `race_start_info.race_horse_data[].chara_color_type` | int | 784 | 0 |
| `race_start_info.race_horse_data[].chara_id` | int | 784 | 1006, 1013, 1016, 1021, 1026 |
| `race_start_info.race_horse_data[].final_grade` | int | 784 | 5, 6, 7, 8, 9 |
| `race_start_info.race_horse_data[].frame_order` | int | 784 | 1, 10, 3, 5, 8 |
| `race_start_info.race_horse_data[].frame_order_change_flag` | int | 784 | 0 |
| `race_start_info.race_horse_data[].guts` | int | 784 | 193, 208, 226, 231, 238 |
| `race_start_info.race_horse_data[].item_id_array` | array | 784 |  |
| `race_start_info.race_horse_data[].mob_id` | int | 784 | 0 |
| `race_start_info.race_horse_data[].motivation` | int | 784 | 2, 3, 4, 5 |
| `race_start_info.race_horse_data[].motivation_change_flag` | int | 784 | 0 |
| `race_start_info.race_horse_data[].nickname_id` | int | 784 | 0 |
| `race_start_info.race_horse_data[].npc_type` | int | 784 | 11 |
| `race_start_info.race_horse_data[].owner_trainer_name` | string | 784 |  |
| `race_start_info.race_horse_data[].owner_viewer_id` | int | 784 | 0 |
| `race_start_info.race_horse_data[].popularity` | int | 784 | 1 |
| `race_start_info.race_horse_data[].popularity_mark_rank_array` | array | 784 |  |
| `race_start_info.race_horse_data[].pow` | int | 784 | 170, 202, 228, 252, 272 |
| `race_start_info.race_horse_data[].proper_distance_long` | int | 784 | 7, 8 |
| `race_start_info.race_horse_data[].proper_distance_middle` | int | 784 | 7, 8 |
| `race_start_info.race_horse_data[].proper_distance_mile` | int | 784 | 2, 4, 7, 8 |
| `race_start_info.race_horse_data[].proper_distance_short` | int | 784 | 1, 2, 3, 5 |
| `race_start_info.race_horse_data[].proper_ground_dirt` | int | 784 | 1, 2, 3, 6 |
| `race_start_info.race_horse_data[].proper_ground_turf` | int | 784 | 7 |
| `race_start_info.race_horse_data[].proper_running_style_nige` | int | 784 | 1, 2, 3, 6, 7 |
| `race_start_info.race_horse_data[].proper_running_style_oikomi` | int | 784 | 1, 3, 4, 7 |
| `race_start_info.race_horse_data[].proper_running_style_sashi` | int | 784 | 1, 4, 7 |
| `race_start_info.race_horse_data[].proper_running_style_senko` | int | 784 | 3, 7 |
| `race_start_info.race_horse_data[].race_dress_id` | int | 784 | 100646, 101302, 101601, 102101, 102613 |
| `race_start_info.race_horse_data[].race_result_array` | array | 784 |  |
| `race_start_info.race_horse_data[].race_result_array[].auto_continue_num` | int | 754 | 0 |
| `race_start_info.race_horse_data[].race_result_array[].bashin_diff` | int | 754 | 15429, 25731, 31972, 3918, 45611 |
| `race_start_info.race_horse_data[].race_result_array[].bashin_diff_from_top` | int | 754 | 0 |
| `race_start_info.race_horse_data[].race_result_array[].frame_order` | int | 754 | 1, 2, 3, 5, 9 |
| `race_start_info.race_horse_data[].race_result_array[].ground_condition` | int | 754 | 1, 2, 3 |
| `race_start_info.race_horse_data[].race_result_array[].is_excitement` | int | 754 | 0, 1 |
| `race_start_info.race_horse_data[].race_result_array[].is_running_alone` | int | 754 | 0, 1 |
| `race_start_info.race_horse_data[].race_result_array[].last_straight_line_rank` | int | 754 | 1, 2, 3, 4 |
| `race_start_info.race_horse_data[].race_result_array[].motivation` | int | 754 | 2, 3, 4, 5 |
| `race_start_info.race_horse_data[].race_result_array[].popularity` | int | 754 | 1 |
| `race_start_info.race_horse_data[].race_result_array[].program_id` | int | 754 | 1069, 1070, 1075, 1078 |
| `race_start_info.race_horse_data[].race_result_array[].race_num` | int | 754 | 1 |
| `race_start_info.race_horse_data[].race_result_array[].result_rank` | int | 754 | 1 |
| `race_start_info.race_horse_data[].race_result_array[].result_time` | int | 754 | 1048581, 904176, 909601, 911124, 912606 |
| `race_start_info.race_horse_data[].race_result_array[].running_style` | int | 754 | 1, 2, 3, 4 |
| `race_start_info.race_horse_data[].race_result_array[].single_mode_chara_id` | int | 754 | 760, 761, 762, 763, 764 |
| `race_start_info.race_horse_data[].race_result_array[].skill_activate_count` | int | 754 | 0, 1 |
| `race_start_info.race_horse_data[].race_result_array[].start_dash_state` | int | 754 | 0, 2 |
| `race_start_info.race_horse_data[].race_result_array[].state` | int | 754 | 1 |
| `race_start_info.race_horse_data[].race_result_array[].turn` | int | 754 | 12 |
| `race_start_info.race_horse_data[].race_result_array[].viewer_id` | int | 754 | 159392583559 |
| `race_start_info.race_horse_data[].race_result_array[].weather` | int | 754 | 1, 2, 3 |
| `race_start_info.race_horse_data[].rarity` | int | 784 | 4, 5 |
| `race_start_info.race_horse_data[].running_style` | int | 784 | 1, 2, 3, 4 |
| `race_start_info.race_horse_data[].single_mode_chara_id` | int | 784 | 753, 760, 761, 762, 763 |
| `race_start_info.race_horse_data[].single_mode_win_count` | int | 784 | 0, 1, 2, 3, 4 |
| `race_start_info.race_horse_data[].skill_array` | array | 784 |  |
| `race_start_info.race_horse_data[].skill_array[].level` | int | 784 | 2, 3, 4, 5, 6 |
| `race_start_info.race_horse_data[].skill_array[].skill_id` | int | 784 | 100161, 100211, 110061, 110131, 110261 |
| `race_start_info.race_horse_data[].speed` | int | 784 | 172, 212, 245, 252, 255 |
| `race_start_info.race_horse_data[].stamina` | int | 784 | 248, 253, 268, 274, 299 |
| `race_start_info.race_horse_data[].talent_level` | int | 784 | 3, 5 |
| `race_start_info.race_horse_data[].team_id` | int | 784 | 0 |
| `race_start_info.race_horse_data[].team_member_id` | int | 784 | 0 |
| `race_start_info.race_horse_data[].team_rank` | int | 784 | 0 |
| `race_start_info.race_horse_data[].trained_chara_id` | int | 784 | 0 |
| `race_start_info.race_horse_data[].trainer_name` | string | 784 | Cing |
| `race_start_info.race_horse_data[].viewer_id` | int | 784 | 159392583559 |
| `race_start_info.race_horse_data[].win_saddle_id_array` | array | 784 |  |
| `race_start_info.race_horse_data[].wiz` | int | 784 | 231, 243, 263, 270, 284 |
| `race_start_info.random_seed` | int | 784 | 1145325894, 1432231452, 19647544, 2073021925, 402646649 |
| `race_start_info.season` | int | 784 | 1, 2, 3, 4, 5 |
| `race_start_info.weather` | int | 784 | 1, 2, 3, 4 |

### `reserved_race_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `reserved_race_array[].deck_name` | string | 15 |  |
| `reserved_race_array[].deck_num` | int | 15 | 0 |
| `reserved_race_array[].race_array` | array | 15 |  |
| `reserved_race_array[].race_array[].program_id` | int | 2 | 629, 74 |
| `reserved_race_array[].race_array[].year` | int | 2 | 1, 2 |

### `reward_summary_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `reward_summary_info.add_card_bonus_info` | null (null: 289x) | 289 |  |
| `reward_summary_info.add_card_list` | array | 289 |  |
| `reward_summary_info.add_chara_list` | array | 289 |  |
| `reward_summary_info.add_cloth_list` | array | 289 |  |
| `reward_summary_info.add_fcoin` | int | 289 | 0, 10 |
| `reward_summary_info.add_honor_list` | array | 289 |  |
| `reward_summary_info.add_item_list` | array | 289 |  |
| `reward_summary_info.add_item_list[].item_id` | int | 289 | 59, 73, 75, 89, 92 |
| `reward_summary_info.add_item_list[].number` | int | 289 | 1600, 2, 400, 80, 800 |
| `reward_summary_info.add_music_list` | array | 289 |  |
| `reward_summary_info.add_piece_list` | array | 289 |  |
| `reward_summary_info.add_present_num` | int | 289 | 0 |
| `reward_summary_info.add_story_id_array` | array | 289 |  |
| `reward_summary_info.add_support_card_list` | array | 289 |  |
| `reward_summary_info.add_support_card_num_array` | array | 289 |  |
| `reward_summary_info.add_total_fan` | int | 289 | 0 |
| `reward_summary_info.force_update_honor_id` | int | 289 | 0 |
| `reward_summary_info.new_chara_profile_array` | array | 289 |  |

### `start_chara`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `start_chara.boost_story_event_id` | int | 13 | 0 |
| `start_chara.card_id` | int | 13 | 100602, 101302, 101601, 102101, 102602 |
| `start_chara.friend_support_card_info` | object | 13 |  |
| `start_chara.friend_support_card_info.support_card_id` | int | 13 | 30010, 30017, 30081 |
| `start_chara.friend_support_card_info.viewer_id` | int | 13 | 247284426671, 436142174352, 835437190118, 877126053216, 912385931989 |
| `start_chara.is_play_training_challenge` | bool | 13 | False, True |
| `start_chara.rental_succession_trained_chara` | object | 13 |  |
| `start_chara.rental_succession_trained_chara.is_circle_member` | bool | 13 | False |
| `start_chara.rental_succession_trained_chara.is_event_rental` | bool | 13 | False |
| `start_chara.rental_succession_trained_chara.trained_chara_id` | int | 13 | 0, 108, 3036, 3790 |
| `start_chara.rental_succession_trained_chara.viewer_id` | int | 13 | 0, 115894380675, 375735673971, 480608246985 |
| `start_chara.scenario_id` | int | 13 | 1, 4 |
| `start_chara.select_deck_id` | int | 13 | 10, 3, 5, 7, 8 |
| `start_chara.selected_difficulty_info` | object | 13 |  |
| `start_chara.selected_difficulty_info.difficulty` | int | 13 | 0 |
| `start_chara.selected_difficulty_info.difficulty_id` | int | 13 | 0 |
| `start_chara.selected_difficulty_info.is_boost` | int | 13 | 0 |
| `start_chara.succession_trained_chara_id_1` | int | 13 | 0, 1389, 1431, 2516, 2536 |
| `start_chara.succession_trained_chara_id_2` | int | 13 | 0, 1170, 2521, 2543, 516 |
| `start_chara.support_card_ids` | array | 13 |  |

### `tp_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `tp_info.current_tp` | int | 26 | 100, 83, 85, 90, 98 |
| `tp_info.max_recovery_time` | int | 26 | 1774694591, 1774703591, 1774879116, 1774898596, 1774907596 |
| `tp_info.max_tp` | int | 26 | 100 |

### `trophy_reward_info`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `trophy_reward_info.item_id` | int | 2 | 43 |
| `trophy_reward_info.item_num` | int | 2 | 30 |
| `trophy_reward_info.item_type` | int | 2 | 90 |

### `unchecked_event_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `unchecked_event_array[].chara_id` | int | 1774 | 0, 1006, 1013, 1016, 1026 |
| `unchecked_event_array[].event_contents_info` | object | 1774 |  |
| `unchecked_event_array[].event_contents_info.choice_array` | array | 1774 |  |
| `unchecked_event_array[].event_contents_info.choice_array[].receive_item_id` | int | 1653 | 0 |
| `unchecked_event_array[].event_contents_info.choice_array[].select_index` | int | 1653 | 1, 2, 3, 4 |
| `unchecked_event_array[].event_contents_info.choice_array[].target_race_id` | int | 1653 | 0 |
| `unchecked_event_array[].event_contents_info.show_clear` | int | 1774 | 0, 1, 2, 5 |
| `unchecked_event_array[].event_contents_info.show_clear_sort_id` | int | 1774 | 0, 1, 2, 3, 4 |
| `unchecked_event_array[].event_contents_info.support_card_id` | int | 1774 | 0, 10024, 30010, 30036, 30078 |
| `unchecked_event_array[].event_id` | int | 1774 | 10000, 1001, 1013, 20043, 3000 |
| `unchecked_event_array[].minigame_result` | null (null: 1774x) | 1774 |  |
| `unchecked_event_array[].play_timing` | int | 1774 | 1, 2, 3, 6, 7 |
| `unchecked_event_array[].story_id` | int | 1774 | 400000400, 400001401, 501013400, 501013524, 801056003 |
| `unchecked_event_array[].succession_event_info` | null, object (null: 1757x) | 1774 |  |
| `unchecked_event_array[].succession_event_info.effect_type` | int | 17 | 1, 2 |

### `use_item_info_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `use_item_info_array[].current_num` | int | 212 | 1, 2, 3, 4, 5 |
| `use_item_info_array[].item_id` | int | 212 | 11001, 11002, 2002, 2101, 3101 |
| `use_item_info_array[].use_num` | int | 212 | 1, 2, 3 |

### `user_item`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `user_item.item_id` | int | 38 | 95 |
| `user_item.number` | int | 38 | 817, 818, 819, 820, 821 |

### `user_item_array[]`

| Path | Type | Count | Sample Values |
|------|------|-------|---------------|
| `user_item_array[].item_id` | int | 7 | 59 |
| `user_item_array[].number` | int | 7 | 5329650, 5386630, 5389810, 5393710, 5397170 |

---

## Standalone Race Packets (Room Match / Champions Meet)

These packets are sent when a Room Match or Champions Meet race completes. They are **not** part of a training run and do **not** contain `race_start_info`. They are distinguished by having both `race_horse_data_array` and `race_scenario` at the top level, without an active training session.

Detection condition in `carrotjuicer.py`:
```python
if not self.training_tracker and 'race_horse_data_array' in data and 'race_scenario' in data:
```

Generated from **1** Room Match packet.

### Top-Level Keys

| Key | Type | Description |
|-----|------|-------------|
| `ground_condition` | int | 1=Good, 2=SlightlyHeavy, 3=Heavy, 4=Bad |
| `race_horse_data_array` | array | Per-horse stats, skills, aptitudes (similar to `race_start_info.race_horse_data` in training) |
| `race_result` | object | Room/match metadata (room name, host, race instance, seed, etc.) |
| `race_scenario` | string | Base64-encoded gzip protobuf — frame-by-frame race simulation data |
| `season` | int | 1=Spring, 2=Summer, 3=Autumn, 4=Winter |
| `trained_chara_array` | array | Detailed trained character data (deck, factors, succession, rank score) |
| `weather` | int | 1=Sunny, 2=Cloudy, 3=Rainy, 4=Snowy |

### `race_result`

Room/match metadata. Present in Room Match packets; structure may differ for Champions Meet.

| Path | Type | Sample Values |
|------|------|---------------|
| `race_result.saved_room_id` | int | 68242958 |
| `race_result.room_id` | int | 68242958 |
| `race_result.register_id` | int | 1768116277 |
| `race_result.host_viewer_id` | int | 835120372397 |
| `race_result.room_name` | string | "Let's have fun!" |
| `race_result.message` | string | "May the best Umamusume win!" |
| `race_result.season` | int | 4 |
| `race_result.weather` | int | 1 |
| `race_result.ground_condition` | int | 1 |
| `race_result.motivation` | int | 5 |
| `race_result.entry_num` | int | 9 |
| `race_result.current_entry_num` | int | 9 |
| `race_result.private_entry_type` | int | 0 |
| `race_result.private_entry_num` | int | 0 |
| `race_result.private_current_entry_num` | int | 0 |
| `race_result.is_allow_watching` | int | 1 |
| `race_result.trained_chara_restriction` | int | 0 |
| `race_result.restriction_type` | int | 0 |
| `race_result.start_time` | string | "2026-01-11 07:24:37" |
| `race_result.random_seed` | int | 1258164112 |
| `race_result.race_instance_id` | int | 800023 |
| `race_result.favorite_flag` | int | 0 |
| `race_result.own_join_type` | int | 2 |
| `race_result.simulate_app_version` | string | "1.20.7" |
| `race_result.simulate_resource_version` | string | "10004010" |
| `race_result.expiration_time` | string | "2027-01-11 07:24:37" |
| `race_result.restrict_chara_info_array` | array | [] |

### `race_horse_data_array[]`

Per-horse data. Similar to `race_start_info.race_horse_data` in training packets, but with some additional fields (`viewer_id`, `team_id`, `team_member_id`, `trained_chara_id`, `nickname_id`).

Note: `viewer_id` identifies the trainer/player who owns the horse. Multiple horses may share the same `viewer_id` (team of 3). `team_id` groups horses by team.

| Path | Type | Sample Values |
|------|------|---------------|
| `race_horse_data_array[].viewer_id` | int | 127402280066, 159392583559, 835120372397 |
| `race_horse_data_array[].trainer_name` | string | "Cing", "thefakeshadow", "yuu" |
| `race_horse_data_array[].owner_viewer_id` | int | 0 |
| `race_horse_data_array[].owner_trainer_name` | string | "" |
| `race_horse_data_array[].chara_id` | int | 1002, 1004, 1006, 1007, 1020 |
| `race_horse_data_array[].card_id` | int | 100201, 100402, 100602, 100701, 102001 |
| `race_horse_data_array[].trained_chara_id` | int | 1497, 1516, 1521, 1574, 1707 |
| `race_horse_data_array[].single_mode_chara_id` | int | 1497, 1516, 1521, 1574, 1707 |
| `race_horse_data_array[].nickname_id` | int | 54, 67, 70, 84, 154 |
| `race_horse_data_array[].rarity` | int | 3, 4, 5 |
| `race_horse_data_array[].talent_level` | int | 3, 5 |
| `race_horse_data_array[].frame_order` | int | 1–9 (post position) |
| `race_horse_data_array[].running_style` | int | 1=Nige, 2=Senko, 3=Sashi, 4=Oikomi |
| `race_horse_data_array[].speed` | int | 697–1200 |
| `race_horse_data_array[].stamina` | int | 594–1043 |
| `race_horse_data_array[].pow` | int | 699–1081 |
| `race_horse_data_array[].guts` | int | 323–459 |
| `race_horse_data_array[].wiz` | int | 1013–1159 |
| `race_horse_data_array[].motivation` | int | 5 (1=VeryBad .. 5=Max) |
| `race_horse_data_array[].final_grade` | int | 14, 15, 16 |
| `race_horse_data_array[].popularity` | int | 1–9 |
| `race_horse_data_array[].popularity_mark_rank_array` | array | [6, 6, 3] |
| `race_horse_data_array[].mob_id` | int | 0 |
| `race_horse_data_array[].npc_type` | int | 11 |
| `race_horse_data_array[].race_dress_id` | int | 100201, 100430, 100646 |
| `race_horse_data_array[].chara_color_type` | int | 0 |
| `race_horse_data_array[].team_id` | int | 1, 2, 3 |
| `race_horse_data_array[].team_member_id` | int | 1, 2, 3 |
| `race_horse_data_array[].team_rank` | int | 0 |
| `race_horse_data_array[].single_mode_win_count` | int | 11, 12, 13 |
| `race_horse_data_array[].proper_ground_turf` | int | 1–8 (G–S) |
| `race_horse_data_array[].proper_ground_dirt` | int | 1–8 |
| `race_horse_data_array[].proper_distance_short` | int | 1–8 |
| `race_horse_data_array[].proper_distance_mile` | int | 1–8 |
| `race_horse_data_array[].proper_distance_middle` | int | 1–8 |
| `race_horse_data_array[].proper_distance_long` | int | 1–8 |
| `race_horse_data_array[].proper_running_style_nige` | int | 1–8 |
| `race_horse_data_array[].proper_running_style_senko` | int | 1–8 |
| `race_horse_data_array[].proper_running_style_sashi` | int | 1–8 |
| `race_horse_data_array[].proper_running_style_oikomi` | int | 1–8 |
| `race_horse_data_array[].skill_array` | array | |
| `race_horse_data_array[].skill_array[].skill_id` | int | 110061, 200171, ... |
| `race_horse_data_array[].skill_array[].level` | int | 1–6 |
| `race_horse_data_array[].race_result_array` | array | Training race history (program_id, result_rank, turn) |
| `race_horse_data_array[].win_saddle_id_array` | array | |
| `race_horse_data_array[].item_id_array` | array | |
| `race_horse_data_array[].motivation_change_flag` | int | 0 |
| `race_horse_data_array[].frame_order_change_flag` | int | 0 |

### `trained_chara_array[]`

Extended character data including support deck, factors, succession (parents), and rank score. Matched to `race_horse_data_array` entries by `viewer_id` + `card_id`.

| Path | Type | Sample Values |
|------|------|---------------|
| `trained_chara_array[].viewer_id` | int | 159392583559 |
| `trained_chara_array[].owner_viewer_id` | int | 0 |
| `trained_chara_array[].owner_trained_chara_id` | int | 0 |
| `trained_chara_array[].trained_chara_id` | int | 1707 |
| `trained_chara_array[].card_id` | int | 100602 |
| `trained_chara_array[].running_style` | int | 2 |
| `trained_chara_array[].speed` | int | 1200 |
| `trained_chara_array[].stamina` | int | 802 |
| `trained_chara_array[].power` | int | 910 |
| `trained_chara_array[].guts` | int | 455 |
| `trained_chara_array[].wiz` | int | 1075 |
| `trained_chara_array[].rank` | int | 15 |
| `trained_chara_array[].rank_score` | int | 15687 |
| `trained_chara_array[].rarity` | int | 4 |
| `trained_chara_array[].talent_level` | int | 5 |
| `trained_chara_array[].chara_grade` | int | 900 |
| `trained_chara_array[].scenario_id` | int | 2 |
| `trained_chara_array[].nickname_id` | int | 54 |
| `trained_chara_array[].fans` | int | 414700 |
| `trained_chara_array[].wins` | int | 13 |
| `trained_chara_array[].succession_num` | int | 0 |
| `trained_chara_array[].race_cloth_id` | int | 100646 |
| `trained_chara_array[].create_time` | string | "2026-01-09 07:02:53" |
| `trained_chara_array[].proper_ground_turf` | int | 1–8 |
| `trained_chara_array[].proper_ground_dirt` | int | 1–8 |
| `trained_chara_array[].proper_distance_short` | int | 1–8 |
| `trained_chara_array[].proper_distance_mile` | int | 1–8 |
| `trained_chara_array[].proper_distance_middle` | int | 1–8 |
| `trained_chara_array[].proper_distance_long` | int | 1–8 |
| `trained_chara_array[].proper_running_style_nige` | int | 1–8 |
| `trained_chara_array[].proper_running_style_senko` | int | 1–8 |
| `trained_chara_array[].proper_running_style_sashi` | int | 1–8 |
| `trained_chara_array[].proper_running_style_oikomi` | int | 1–8 |
| `trained_chara_array[].skill_array` | array | Same format as `race_horse_data_array[].skill_array` |
| `trained_chara_array[].support_card_list` | array | Support deck used in training |
| `trained_chara_array[].support_card_list[].position` | int | 1–6 |
| `trained_chara_array[].support_card_list[].support_card_id` | int | 30028, 30036, 30086 |
| `trained_chara_array[].support_card_list[].limit_break_count` | int | 3, 4 |
| `trained_chara_array[].support_card_list[].exp` | int | 82935, 118185 |
| `trained_chara_array[].factor_id_array` | array | Own factor IDs |
| `trained_chara_array[].factor_info_array` | array | Own factor details |
| `trained_chara_array[].factor_info_array[].factor_id` | int | 203, 401, 3402 |
| `trained_chara_array[].factor_info_array[].level` | int | 0 |
| `trained_chara_array[].succession_chara_array` | array | Parent characters (6 entries: 2 parents x 3 generations) |
| `trained_chara_array[].succession_chara_array[].position_id` | int | 10, 11, 12, 20, 21, 22 |
| `trained_chara_array[].succession_chara_array[].card_id` | int | 100701, 100801, 102701 |
| `trained_chara_array[].succession_chara_array[].rank` | int | 13 |
| `trained_chara_array[].succession_chara_array[].rarity` | int | 2, 3, 5 |
| `trained_chara_array[].succession_chara_array[].talent_level` | int | 1, 2, 3 |
| `trained_chara_array[].succession_chara_array[].owner_viewer_id` | int | 0 |
| `trained_chara_array[].succession_chara_array[].factor_id_array` | array | |
| `trained_chara_array[].succession_chara_array[].factor_info_array` | array | |
| `trained_chara_array[].succession_chara_array[].factor_info_array[].factor_id` | int | 203, 3402 |
| `trained_chara_array[].succession_chara_array[].factor_info_array[].level` | int | 0 |
| `trained_chara_array[].succession_chara_array[].win_saddle_id_array` | array | |
| `trained_chara_array[].succession_history_array` | array | |
| `trained_chara_array[].race_result_list` | array | Career race results |
| `trained_chara_array[].race_result_list[].program_id` | int | 1070 |
| `trained_chara_array[].race_result_list[].result_rank` | int | 1 |
| `trained_chara_array[].race_result_list[].turn` | int | 12 |
| `trained_chara_array[].race_result_list[].running_style` | int | 1, 2, 3 |
| `trained_chara_array[].race_result_list[].result_time` | int | 919306 |
| `trained_chara_array[].race_result_list[].weather` | int | 1, 2, 3 |
| `trained_chara_array[].race_result_list[].ground_condition` | int | 1, 4 |
| `trained_chara_array[].race_result_list[].popularity` | int | 1 |
| `trained_chara_array[].race_result_list[].prize_money` | int | 0 |
| `trained_chara_array[].nickname_id_array` | array | |
| `trained_chara_array[].win_saddle_id_array` | array | |

### `race_scenario`

Base64-encoded gzip protobuf containing the full race simulation. Decoded via `external/race_data_parser.py`.

Contains:
- **Header**: version, max_length
- **Frame data**: per-tick snapshots for each horse (distance, lane_position, speed, hp, temptation_mode)
- **Horse results**: per-horse finish data:
  - `finish_order` (0-indexed: 0 = 1st place)
  - `finish_time` (scaled time in seconds)
  - `finish_time_raw` (raw simulation time)
  - `finish_diff_time` (diff from previous finisher, using scaled time)
  - `start_delay_time`
  - `guts_order`, `wiz_order`
  - `last_spurt_start_distance`
  - `running_style` (may differ from declared style)
  - `defeat` (0=None, 1=Speed, 2=Stamina, 3=Power, 4=Guts, 5=Wiz)
- **Events**: skill activations, position changes, etc. with frame timestamps

### Key Differences from Training Race Packets

| | Training Race | Standalone Race |
|---|---|---|
| **Trigger** | During a training run | Room Match / Champions Meet |
| **Detection** | `race_scenario` + `race_start_info` | `race_horse_data_array` + `race_scenario` (no `race_start_info`) |
| **Horse data location** | `race_start_info.race_horse_data` | `race_horse_data_array` (top-level) |
| **Trained chara data** | Not present | `trained_chara_array` (deck, factors, succession) |
| **Room metadata** | Not present | `race_result` (room_name, room_id, host, etc.) |
| **Team info** | `team_id` = 0 | `team_id` = 1, 2, 3 (groups of 3 horses per player) |
| **`viewer_id`** | Same for all (player only) | Different per trainer |
| **`race_scenario` format** | Same protobuf | Same protobuf |

---

## Non-Training Packets (Home Screen, Circle, etc.)

These packets are sent outside of training runs and are currently **not processed** by `carrotjuicer.py` (they fall through the handler). They contain account-level inventory data, social features, and game state that could be useful for tools and analysis.

Captured from a single play session (2026-04-06).

### Home Screen Load

Sent when the game finishes loading and reaches the home screen. Contains the bulk of account-level data — **92 top-level keys**. This is the richest single packet in the game.

Detection: First large packet after login, identifiable by presence of `common_define` + `user_info` + `support_card_list`.

#### `support_card_list[]` — Support Card Inventory (191 cards observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `viewer_id` | int | Owner's viewer ID | 159392583559 |
| `support_card_id` | int | Support card ID (maps to MDB) | 10001, 20020, 30078 |
| `exp` | int | Total accumulated EXP | 24110, 56935, 74990 |
| `limit_break_count` | int | Number of limit breaks (0–4) | 0, 2, 4 |
| `favorite_flag` | int | 1 if favorited, 0 otherwise | 0, 1 |
| `stock` | int | Duplicate stock count | 0 |
| `possess_time` | string | When the card was first obtained | "2025-06-27 00:12:26" |
| `create_time` | string | Creation timestamp | "2025-06-27 00:12:26" |

#### `card_list[]` — Character Card Inventory (72 cards observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `card_id` | int | Character card ID (maps to MDB) | 100101, 100201, 105601 |
| `rarity` | int | Star rarity (3=3★, 4=4★, 5=5★) | 3, 4, 5 |
| `talent_level` | int | Talent level (limit break equivalent) | 1–5 |
| `create_time` | string | When the card was obtained | "2025-07-15 08:18:37" |
| `skill_data_array` | array | Skill data (usually empty at account level) | [] |

#### `chara_list[]` — Base Character Roster (52 characters observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `chara_id` | int | Character ID | 1001, 1002, 1003 |
| `training_num` | int | Number of times trained | 9, 13, 19 |
| `love_point` | int | Affection/love points | 183, 783, 1207 |
| `fan` | int | Total fan count for this character | 3228930, 4808108 |
| `max_grade` | int | Highest grade achieved | 15, 16 |
| `dress_id` | int | Equipped dress ID (0 = default) | 0, 100130, 2 |
| `mini_dress_id` | int | Equipped chibi dress ID | 2, 100301 |

#### `cloth_list[]` — Costume Inventory (78 costumes observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `cloth_id` | int | Costume/outfit ID (maps to MDB) | 5, 101, 102 |

#### `piece_list[]` — Limit Break Pieces (72 entries observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `piece_id` | int | Piece ID (matches card_id) | 100101, 100201 |
| `piece_num` | int | Number of pieces owned | 0, 130, 190 |

#### `item_list[]` — Items Inventory (72 items observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `item_id` | int | Item ID (maps to MDB) | 1, 4, 7 |
| `number` | int | Quantity owned | 648, 2579, 5684 |

#### `coin_info` — Currency Balances

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `fcoin` | int | Free coins (jewels) | 8635 |
| `coin` | int | Paid coins | 4790 |

#### `music_list[]` — Unlocked Music (22 tracks observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `music_id` | int | Music track ID | 1001, 1004, 1005 |
| `acquisition_time` | string | When the track was unlocked | "2025-07-06 02:24:17" |

#### Other Inventory Keys

| Key | Description |
|-----|-------------|
| `card_dress_array` | Card-specific dress/outfit data |
| `directory_card_array` | Card directory / collection entries |
| `release_card_array` | Released/unlocked cards |
| `release_item_flag` | Item release flags |

#### `trained_chara[]` — Raised Characters (232 characters observed)

Full raised character data with stats, skills, factors, and career results.

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `viewer_id` | int | Owner's viewer ID | 159392583559 |
| `trained_chara_id` | int | Unique raised character ID | 156 |
| `owner_viewer_id` | int | Original owner (0 = self) | 0 |
| `owner_trained_chara_id` | int | Original raised chara ID (0 = self) | 0 |
| `single_mode_chara_id` | int | Training mode character ID | 50 |
| `chara_seed` | int | Random seed for the character | 1190714959 |
| `card_id` | int | Character card ID used | 105601 |
| `succession_trained_chara_id_1` | int | Parent 1 trained_chara_id | 140 |
| `succession_trained_chara_id_2` | int | Parent 2 trained_chara_id | 155 |
| `use_type` | int | Usage type | 0 |
| `speed` | int | Speed stat | 867 |
| `stamina` | int | Stamina stat | 899 |
| `power` | int | Power stat | 677 |
| `wiz` | int | Wisdom stat | 360 |
| `guts` | int | Guts stat | 418 |
| `fans` | int | Fan count | 234819 |
| `rank_score` | int | Rank score | 9035 |
| `rank` | int | Grade rank | 12 |
| `scenario_id` | int | Training scenario used | 1 |
| `route_id` | int | Route taken | 9 |
| `arrive_route_race_id` | int | Route arrival race ID | 99 |
| `proper_ground_turf` | int | Turf aptitude (1=G, 3=E, 5=D, 7=B, 8=A, 9=S) | 7 |
| `proper_ground_dirt` | int | Dirt aptitude | 2 |
| `proper_running_style_nige` | int | Runner aptitude | 3 |
| `proper_running_style_senko` | int | Leader aptitude | 7 |
| `proper_running_style_sashi` | int | Betweener aptitude | 7 |
| `proper_running_style_oikomi` | int | Chaser aptitude | 2 |
| `proper_distance_short` | int | Short distance aptitude | 2 |
| `proper_distance_mile` | int | Mile distance aptitude | 5 |
| `proper_distance_middle` | int | Middle distance aptitude | 7 |
| `proper_distance_long` | int | Long distance aptitude | 7 |
| `succession_num` | int | Times used as succession parent | 45 |
| `rarity` | int | Star rarity | 3 |
| `is_saved` | int | 1 if saved | 1 |
| `is_locked` | int | 1 if locked from deletion | 1 |
| `talent_level` | int | Talent level | 2 |
| `race_cloth_id` | int | Race outfit ID | 105601 |
| `chara_grade` | int | Character grade | 8 |
| `running_style` | int | Preferred running style (1=Nige, 2=Senko, 3=Sashi, 4=Oikomi) | 3 |
| `nickname_id` | int | Earned nickname/title ID | 98 |
| `wins` | int | Win count | 0 |
| `register_time` | string | When registered | "2025-07-31 09:16:47" |
| `create_time` | string | When created | "2025-07-31 09:16:47" |
| `skill_array[]` | array | Learned skills | |
| `skill_array[].skill_id` | int | Skill ID | 100561, 200362 |
| `skill_array[].level` | int | Skill level | 1, 3 |
| `support_card_list[]` | array | Support deck used (6 cards) | |
| `support_card_list[].position` | int | Deck slot (1–6) | 1, 2, 3, 4, 5, 6 |
| `support_card_list[].support_card_id` | int | Support card ID | 30028, 20020 |
| `support_card_list[].exp` | int | Card EXP at time of training | 56935, 74990 |
| `support_card_list[].limit_break_count` | int | Card limit breaks (0–4) | 0, 2, 4 |
| `factor_id_array` | array | Factor IDs (own) | [203, 2202, 1001501] |
| `factor_info_array[]` | array | Factor details (own) | |
| `factor_info_array[].factor_id` | int | Factor ID | 203, 2202 |
| `factor_info_array[].level` | int | Factor level | 0 |
| `succession_chara_array[]` | array | Parent characters (6 entries: 2 parents × 3 generations) | |
| `succession_chara_array[].position_id` | int | 10/11/12=parent1 chain, 20/21/22=parent2 chain | 10, 11, 20 |
| `succession_chara_array[].card_id` | int | Parent's card ID | 100601 |
| `succession_chara_array[].rank` | int | Parent's rank | 12 |
| `succession_chara_array[].rarity` | int | Parent's rarity | 3 |
| `succession_chara_array[].talent_level` | int | Parent's talent level | 2 |
| `succession_chara_array[].owner_viewer_id` | int | Parent's owner (0=self) | 0, 375747068419 |
| `succession_chara_array[].factor_id_array` | array | Parent's factor IDs | |
| `succession_chara_array[].factor_info_array[]` | array | Parent's factor details | |
| `succession_chara_array[].win_saddle_id_array` | array | Parent's earned saddle/trophy IDs | |
| `race_result_list[]` | array | Career race results | |
| `race_result_list[].turn` | int | Turn when race occurred | 12, 18, 29 |
| `race_result_list[].program_id` | int | Race program ID | 1069, 646 |
| `race_result_list[].weather` | int | 1=Sunny, 2=Cloudy, 3=Rainy | 1, 2 |
| `race_result_list[].ground_condition` | int | 1=Good, 2=SlightlyHeavy, 3=Heavy, 4=Bad | 1, 2 |
| `race_result_list[].running_style` | int | Style used in race | 3 |
| `race_result_list[].popularity` | int | Popularity (betting rank) | 1, 2 |
| `race_result_list[].result_rank` | int | Finishing position | 1, 2 |
| `race_result_list[].result_time` | int | Finish time (microseconds?) | 1173177 |
| `race_result_list[].prize_money` | int | Prize money earned | 0 |
| `win_saddle_id_array` | array | Earned saddle/trophy IDs | [6, 10, 12, 14] |
| `nickname_id_array` | array | All earned nickname IDs | [2, 7, 24, 26, 42] |

#### `support_card_deck_array[]` — Saved Decks (10 decks observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `deck_id` | int | Deck slot number | 1, 2, 3 |
| `name` | string | User-assigned deck name | "TT", "Deck 2" |
| `support_card_id_array` | array[int] | 5 support card IDs in this deck | [30028, 30074, 30041, 30078, 30010] |

#### `team_data_array[]` — Team Formations (15 entries observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `distance_type` | int | 1=Short, 2=Mile, 3=Middle, 4=Long, 5=Dirt | 1 |
| `member_id` | int | Team slot position | 1, 2, 3 |
| `trained_chara_id` | int | Assigned raised character ID | 1778, 1799 |
| `running_style` | int | 1=Nige, 2=Senko, 3=Sashi, 4=Oikomi | 2, 3 |

#### `trained_chara_favorite_array[]` — Favorited Characters (121 entries observed)

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `trained_chara_id` | int | Raised character ID | 179, 222, 556 |
| `icon_type` | int | Favorite icon/category | 0, 1, 4 |
| `memo` | string | User note (usually empty) | "" |

#### `user_info` — Player Profile

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `viewer_id` | int | Player's unique ID | 159392583559 |
| `name` | string | Display name | "Cing" |
| `comment` | string | Profile comment | "：o" |
| `honor_id` | int | Equipped honor/title ID | 403101 |
| `sex` | int | Gender setting | 1 |
| `tutorial_step` | int | Tutorial progress (1000 = complete) | 1000 |
| `leader_chara_id` | int | Home screen leader character | 1040 |
| `leader_chara_dress_id` | int | Leader's outfit ID | 104001 |
| `support_card_id` | int | Displayed support card | 30078 |
| `partner_chara_id` | int | Partner character ID | 2198 |
| `bonus_follow_num` | int | Bonus follow count | 40 |
| `fan` | int | Total fan count | 253589974 |
| `rank_score` | int | Total rank score | 4076052 |
| `best_team_evaluation_point` | int | Best team evaluation | 258265 |
| `register_time` | string | Account creation date | "2025-06-27 00:02:28" |
| `create_time` | string | Creation timestamp | "2025-06-27 00:02:28" |
| `update_time` | string | Last update timestamp | "2026-04-06 20:33:13" |
| `birth_day` | string | Birthday (MMDD) | "0902" |
| `last_ticket_natural_recovery_time` | string | Last TP recovery time | "2026-04-06 15:42:40" |

#### `champions_info` — Champions Meet State

| Field | Type | Description | Sample Values |
|-------|------|-------------|---------------|
| `champions_id` | int | Current champions event ID (0 = none active) | 0 |
| `entry_times` | int | Number of entries | 0 |
| `free_entry_times` | int | Free entries remaining | 0 |
| `round_id` | int | Current round | 0 |
| `next_tier` | int | Next tier threshold | 0 |
| `state` | int | Current state | 0 |
| `entry_trained_chara_id_array` | array | Entered character IDs | [] |
| `league_type` | int | League type | 0 |

#### `honor_info` — Honors / Titles

| Field | Type | Description |
|-------|------|-------------|
| `honor_list[]` | array | All earned honor entries |
| `honor_list[].honor_id` | int | Honor ID (maps to MDB) |
| `honor_list[].create_time` | string | When the honor was earned |
| `last_checked_time` | int | Unix timestamp of last check |

#### Other Inventory Keys

| Key | Description |
|-----|-------------|
| `card_dress_array` | Card-specific dress/outfit data |
| `directory_card_array` | Card directory / collection entries |
| `release_card_array` | Released/unlocked cards |
| `release_item_flag` | Item release flags |

#### Other Account Keys

| Key | Description |
|-----|-------------|
| `last_select_support_card_deck_id` | Last used support card deck ID |
| `scenario_record_array` | Training scenario completion records |
| `single_mode_chara_light` | Training mode character summary data |
| `single_mode_difficulty_info_array` | Training difficulty settings |
| `single_mode_scenario_id_array` | Available training scenario IDs |
| `single_mode_rental_succession_num` | Rental succession count |
| `single_mode_succession_free_rental_time` | Free rental succession timer |

#### Game State & Progress

| Key | Description |
|-----|-------------|
| `common_define` | Game constants and configuration |
| `login_bonus_list` | Login bonus state |
| `login_trophy_info_array` | Login trophy info |
| `ranking` | Player ranking data |
| `rp_info` | RP (ranking points) info |
| `tp_info` | TP (training points) info |
| `add_friend_point` | Friend point balance |
| `support_user_num` | Number of support users |
| `notice_data` | System notices |
| `tutorial_guide_data_array` | Tutorial state |
| `unread_announce_id_array` | Unread announcement IDs |
| `user_last_checked_time_list` | Timestamps for various user checks |
| `user_birth` | User birthday setting |
| `optin_user_birth` | Birthday opt-in flag |
| `country_type` | Country/region type |
| `is_linkage` | Account linkage status |
| `dma_state` | DMA (Digital Markets Act) state |
| `res_version` | Resource version |

#### Race & Competition

| Key | Description |
|-----|-------------|
| `challenge_match_load_info` | Challenge Match state |
| `daily_race_playing_info` | Daily race progress |
| `daily_legend_race_playing_info` | Daily Legend race progress |
| `legend_race_playing_info` | Legend race progress |
| `practice_race_state` | Practice race state |
| `practice_partner_chara_array` | Practice partner characters |
| `practice_partner_owner_info_array` | Practice partner owner info |
| `stadium_race_chara_id_array` | Stadium race character IDs |
| `team_stadium_race_status` | Team Stadium race status |
| `team_stadium_user` | Team Stadium user data |
| `team_building_load_info` | Team Building state |
| `training_challenge_exam_infos` | Training challenge exam info |
| `training_challenge_user_info` | Training challenge user data |

#### Gacha & Shop

| Key | Description |
|-----|-------------|
| `gacha_banner_info` | Current gacha banner info |
| `gacha_campaign_info_array` | Active gacha campaigns |
| `added_gacha_stock_info` | New gacha stock info |
| `limited_shop_info` | Limited shop offerings |
| `border_line` | Gacha/ranking border lines |
| `payment_purchased_times_list` | Payment purchase history counts |
| `season_pack_info` | Season pack offerings |
| `cygames_id_apply_product_flag` | Cygames ID product flag |
| `cygames_id_serial_code_reward_info_array` | Serial code reward info |

#### Story & Events

| Key | Description |
|-----|-------------|
| `main_story_data_list` | Main story progress |
| `character_story_data_list` | Character story progress |
| `extra_story_data_list` | Extra story progress |
| `home_story_data_array` | Home screen story data |
| `event_data_array` | Event data |
| `story_event_id` | Current story event ID |
| `story_event_first_flag` | Story event first-time flag |
| `story_event_mission_list` | Story event missions |
| `story_event_roulette_coin_num` | Story event roulette coins |
| `story_favorite_array` | Favorited stories |
| `released_episode_data_array` | Released episode data |
| `short_episode_data_array` | Short episode data |
| `chara_profile_array` | Character profile data |
| `valentine_campaign_received_array` | Valentine campaign state |
| `fan_raid_id` | Fan raid event ID |
| `fan_raid_first_flag` | Fan raid first-time flag |

#### Home & Social

| Key | Description |
|-----|-------------|
| `home_position_info` | Home screen character positioning |
| `home_poster_data_array` | Home screen poster/banner data |
| `jukebox_info` | Jukebox settings |
| `jukebox_request_history` | Jukebox request history |
| `last_information_update_time` | Last info update timestamp |
| `menu_badge_info` | Menu badge notification counts |
| `parental_consent` | Parental consent flag |
| `recheck_dmm_jewel` | DMM jewel recheck flag |
| `talk_gallery_list` | Talk gallery entries |
| `circle_data` | Circle (guild) summary data |

### Circle / Guild Packets

Sent when entering the Circle screen. Contains social/guild data.

Detection: Presence of `circle_info` + `circle_user_array`.

| Key | Description |
|-----|-------------|
| `circle_info` | Circle details (name, level, etc.) |
| `circle_user_array` | Circle member list |
| `circle_chat_message_array` | Circle chat messages |
| `circle_item_donate_array` | Item donation records |
| `circle_item_request_array` | Item requests |
| `circle_post_partner_array` | Rental partner posts |
| `circle_ranking_this_month` | Current month circle ranking |
| `circle_ranking_last_month` | Last month circle ranking |
| `room_info_array` | Circle room info |
| `room_match_info_array` | Room Match info |
| `room_user_array` | Room users |
| `summary_user_info_array` | Summary user info |
| `change_leader` | Leader change info |
| `chat_polling_interval` | Chat poll interval |
| `daily_donated_count` | Daily donation count |
| `daily_post_partner_count` | Daily partner post count |
| `is_calculate` | Calculation flag |
| `is_scout_able` | Scouting availability |
| `is_show_ranking_result` | Ranking result visibility |

### Other Observed Packets

| Keys | Context |
|------|---------|
| `support_card_data` | Viewing a specific support card's details |
| `trained_chara_array`, `trained_chara_favorite_array`, `room_match_entry_chara_id_array` | Viewing Room Match character selection |
| `release_card_array` | Card release/unlock event |
| `circle_item_donate_array`, `circle_user_array`, `reward_summary_info` | Circle donation reward |
| `circle_item_donate_array`, `current_item_data_array`, `daily_donated_count`, `reward_summary_info` | Circle donation with item update |
| `home_poster_data_array`, `home_story_data_array`, `released_episode_data_array`, `short_episode_data_array`, `talk_gallery_data_array`, `tutorial_guide_data_array` | Home screen story/episode refresh |
