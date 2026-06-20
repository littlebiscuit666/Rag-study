---
chunk_id: chunk_008
domain: ods_event
domain_name: 原始事件数据库
table: ods_event_log
table_name: 游戏行为事件总表
section: social_interact
section_type: event_properties
level: sub_table
char_count: 685
source_file: database-intro-for-rag.md
---

[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表] [社交互动事件]

社交互动事件(social\_interact)properties 字段:

| 字段名             | 含义                                                                      |  |
|-----------------|-------------------------------------------------------------------------|--|
| social_type     | 社交类型:guild_donate(公会捐献)、friend_add(添加好友)、chat(聊天)、team_battle<br>(组队战⽃) |  |
| guild_id        | 公会 ID(公会相关社交⾏为时存在)                                                      |  |
| target_user_id  | 互动对象⽤户 ID(私聊、好友申请等场景)                                                   |  |
| donation_amount | 捐献数量(仅公会捐献时存在)                                                          |  |