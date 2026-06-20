---
chunk_id: chunk_007
domain: ods_event
domain_name: 原始事件数据库
table: ods_event_log
table_name: 游戏行为事件总表
section: logout
section_type: event_properties
level: sub_table
char_count: 545
source_file: database-intro-for-rag.md
---

[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表] [退出事件]

退出事件(logout)properties 字段:

| 字段名                  | 含义                                           |  |
|----------------------|----------------------------------------------|--|
| session_duration_sec | 本次会话时⻓(秒)                                    |  |
| logout_reason        | 退出原因,如 user_exit(主动退出)、crash(崩溃)、timeout(超时) |  |
| last_scene           | 退出前所在场景,如 main_city(主城)、dungeon(副本)          |  |
| last_action          | 退出前最后⼀次操作                                    |  |

####