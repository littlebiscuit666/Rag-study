---
chunk_id: chunk_021
domain: feature_store
domain_name: 特征数据库
table: feature_user_online
table_name: 用户在线特征表
section: behavior
section_type: feature_group
level: sub_table
char_count: 677
source_file: database-intro-for-rag.md
---

[数据域: 特征数据库(feature_store)] [表: feature_user_online 用户在线特征表] [行为偏好特征]

⾏为偏好特征(behavior):

| 特征名                    | 含义                      |
|------------------------|-------------------------|
| play_mode_diversity    | 玩法多样性指数(⾹农熵),值越⼤代表玩法越均衡 |
| pvp_ratio_7d           | 近 7 ⽇ PVP 战⽃场次占总战⽃场次的⽐例 |
| pve_ratio_7d           | 近 7 ⽇ PVE 副本场次占总战⽃场次的⽐例 |
| level_complete_rate_7d | 近 7 ⽇关卡通关率(通关次数/尝试次数)   |
| battle_count_7d        | 近 7 ⽇参与战⽃总场次            |
| battle_win_rate_7d     | 近 7 ⽇战⽃胜率               |
| avg_battle_duration_7d | 近 7 ⽇平均单场战⽃时⻓(秒)        |
| item_use_count_7d      | 近 7 ⽇使⽤道具总次数            |
| preferred_character    | 玩家最常使⽤的⻆⾊/职业 ID         |

###