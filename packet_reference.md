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
