---
chunk_id: chunk_016
domain: dwd_social
domain_name: 社交数据库
table: dim_guild
table_name: 公会信息表
section: null
section_type: null
level: table
char_count: 972
source_file: database-intro-for-rag.md
---

[数据域: 社交数据库(dwd_social)] [表: dim_guild 公会信息表]

数据表:dim\_guild(公会信息表)

描述: 游戏内公会的基础信息及活跃度指标。

| 字段名                    | 类型        | 含义            |
|------------------------|-----------|---------------|
| guild_id               | STRING    | 公会唯⼀标识,主键     |
| guild_name             | STRING    | 公会名称          |
| game_id                | STRING    | 游戏标识          |
| server_id              | STRING    | 所在服务器         |
| leader_id              | STRING    | 会⻓玩家 ID       |
| create_time            | TIMESTAMP | 公会创建时间        |
| level                  | INTEGER   | 公会等级(1-20)    |
| member_count           | INTEGER   | 当前成员⼈数        |
| max_members            | INTEGER   | 公会成员上限        |
| total_power            | BIGINT    | 全体成员战⼒总和      |
| guild_fund             | BIGINT    | 公会基⾦(⾦币)      |
| guild_battle_count_7d  | INTEGER   | 近 7 ⽇参与公会战次数  |
| group_dungeon_count_7d | INTEGER   | 近 7 ⽇参与组队副本次数 |
| donation_total_gold_7d | BIGINT    | 近 7 ⽇全员捐献⾦币总量 |