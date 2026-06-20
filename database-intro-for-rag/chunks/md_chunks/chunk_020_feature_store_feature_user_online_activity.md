---
chunk_id: chunk_020
domain: feature_store
domain_name: 特征数据库
table: feature_user_online
table_name: 用户在线特征表
section: activity
section_type: feature_group
level: sub_table
char_count: 757
source_file: database-intro-for-rag.md
---

[数据域: 特征数据库(feature_store)] [表: feature_user_online 用户在线特征表] [活跃度特征]

活跃度特征(activity):

| 特征名             | 含义               |
|-----------------|------------------|
| login_count_7d  | 近 7 ⽇登录天数(0-7)   |
| login_count_30d | 近 30 ⽇登录天数(0-30) |
| login_streak    | 当前连续登录天数,未登录则清零  |

| 特征名                      | 含义                                  |
|--------------------------|-------------------------------------|
| avg_session_duration_7d  | 近 7 ⽇单次游戏时⻓均值(秒)                    |
| avg_session_duration_30d | 近 30 ⽇单次游戏时⻓均值(秒)                   |
| days_since_last_login    | 距上次登录天数,0 代表今天已登录                   |
| active_hours             | 玩家活跃时段列表(⼩时),如 [19,20,21,22] 表示晚间活跃 |
| weekend_active_ratio     | 周末登录天数占总登录天数的⽐例                     |

###