---
chunk_id: chunk_015
domain: dwd_social
domain_name: 社交数据库
table: dwd_social_relation
table_name: 好友关系表
section: null
section_type: null
level: table
char_count: 1086
source_file: database-intro-for-rag.md
---

[数据域: 社交数据库(dwd_social)] [表: dwd_social_relation 好友关系表]

数据表:dwd\_social\_relation(好友关系表)

描述: 玩家之间的好友关系及亲密度数据,双向关系单条存储(A-B 和 B-A 各存⼀条)。

| 字段名                  | 类型        | 含义                                |
|----------------------|-----------|-----------------------------------|
| relationship_id      | STRING    | 关系唯⼀标识,主键                         |
| user_id              | STRING    | 发起⽅玩家 ID                          |
| friend_user_id       | STRING    | 接收⽅玩家 ID                          |
| game_id              | STRING    | 游戏标识                              |
| relationship_type    | STRING    | 关系类型:friend(好友)、blacklist(⿊名单)    |
| establish_time       | TIMESTAMP | 建⽴好友关系的时间                         |
| intimacy_score       | INTEGER   | 亲密度分数(0-1000),由互动⾏为频率计算           |
| chat_count_7d        | INTEGER   | 近 7 ⽇聊天消息数                        |
| team_battle_count_7d | INTEGER   | 近 7 ⽇⼀同组队战⽃次数                     |
| gift_count_7d        | INTEGER   | 近 7 ⽇互送礼物次数                       |
| status               | STRING    | 关系状态:active(活跃互动)、inactive(⻓期不互动) |