---
chunk_id: chunk_001
domain: ods_event
domain_name: 原始事件数据库
table: ods_event_log
table_name: 游戏行为事件总表
section: null
section_type: null
level: table
char_count: 2177
source_file: database-intro-for-rag.md
---

[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表]

## 数据表:ods\_event\_log

描述: 游戏⾏为事件总表,按 event\_type 区分事件类型,每种事件类型在 properties 字段中携带不同的业 务属性。

| 字段名         | 类型        | 含义                                                                                                                      |
|-------------|-----------|-------------------------------------------------------------------------------------------------------------------------|
| event_id    | STRING    | 事件唯⼀标识,格式 evt_{⽇期}{序号}{随机串}                                                                                             |
| event_type  | STRING    | 事件类型,枚举值:login(登录)、logout(退出)、battle(战⽃)、purchase<br>(充值)、item_use(道具使⽤)、level_complete(关卡完成)、social_interact<br>(社交互动) |
| user_id     | STRING    | 玩家唯⼀标识,系统内唯⼀,格式 U{8位数字}                                                                                                 |
| game_id     | STRING    | 游戏标识,⼀个系统可接⼊多款游戏                                                                                                        |
| server_id   | STRING    | 游戏服务器标识                                                                                                                 |
| timestamp   | TIMESTAMP | 事件发⽣的 UTC 时间,精确到毫秒                                                                                                      |
| device_id   | STRING    | 设备唯⼀标识,同⼀设备跨账号登录时相同                                                                                                     |
| platform    | STRING    | 客户端平台,枚举值:Android、iOS、PC、H5                                                                                             |
| app_version | STRING    | 游戏客户端版本号                                                                                                                |
| session_id  | STRING    | 会话标识,⽤于关联同⼀次游戏会话内的事件序列                                                                                                  |

| 字段名        | 类型     | 含义                            |
|------------|--------|-------------------------------|
| network    | STRING | ⽹络类型,枚举值:WiFi、4G、5G、其他        |
| properties | JSON   | 事件专属属性,不同 event_type 有不同的字段结构 |

###