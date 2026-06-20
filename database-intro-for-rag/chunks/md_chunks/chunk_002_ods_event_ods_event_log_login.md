---
chunk_id: chunk_002
domain: ods_event
domain_name: 原始事件数据库
table: ods_event_log
table_name: 游戏行为事件总表
section: login
section_type: event_properties
level: sub_table
char_count: 605
source_file: database-intro-for-rag.md
---

[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表] [登录事件]

登录事件(login)properties 字段:

| 字段名               | 含义                                      |
|-------------------|-----------------------------------------|
| ip                | 玩家登录 IP 地址(已脱敏)                         |
| client_os         | 操作系统版本                                  |
| device_model      | 设备型号,如 Xiaomi 14 Pro                    |
| screen_resolution | 屏幕分辨率                                   |
| login_channel     | 登录渠道,如 wechat(微信)、qq、phone              |
| login_type        | 登录类型,如 token(Token ⾃动登录)、password(密码登录) |

###