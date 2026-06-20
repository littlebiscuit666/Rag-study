---
chunk_id: chunk_017
domain: dwd_social
domain_name: 社交数据库
table: dwd_chat_log
table_name: 聊天记录表
section: null
section_type: null
level: table
char_count: 936
source_file: database-intro-for-rag.md
---

[数据域: 社交数据库(dwd_social)] [表: dwd_chat_log 聊天记录表]

数据表:dwd\_chat\_log(聊天记录表)

描述: 玩家聊天记录,已做内容脱敏,保留⽤于社交⾏为分析。

| 字段名          | 类型     | 含义                                              |
|--------------|--------|-------------------------------------------------|
| message_id   | STRING | 消息唯⼀标识,主键                                       |
| user_id      | STRING | 发送者玩家 ID                                        |
| game_id      | STRING | 游戏标识                                            |
| channel_type | STRING | 聊天频道类型:guild(公会)、world(世界)、private(私聊)、team(组队) |
| channel_id   | STRING | 频道 ID,如公会 ID 或私聊双⽅ ID                           |
| message_type | STRING | 消息类型:text(⽂字)、emoji(表情)、image(图⽚)               |

| 字段名        | 类型        | 含义             |
|------------|-----------|----------------|
| content    | STRING    | 消息内容(已脱敏)      |
| timestamp  | TIMESTAMP | 消息发送时间         |
| is_flagged | BOOLEAN   | 是否被⻛控系统标记为违规内容 |