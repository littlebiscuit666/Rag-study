---
chunk_id: chunk_011
domain: dim_content
domain_name: 物料/内容数据库
table: dim_activity
table_name: 活动表
section: null
section_type: null
level: table
char_count: 1476
source_file: database-intro-for-rag.md
---

[数据域: 物料/内容数据库(dim_content)] [表: dim_activity 活动表]

数据表:dim\_activity(活动表)

描述: 游戏内运营活动配置,记录活动条件、奖励和⽬标⽤户群体。

| 字段名             | 类型        | 含义                                                                              |
|-----------------|-----------|---------------------------------------------------------------------------------|
| activity_id     | STRING    | 活动唯⼀标识,主键                                                                       |
| activity_name   | STRING    | 活动名称                                                                            |
| activity_type   | STRING    | 活动类型:festival(节⽇活动)、daily_quest(⽇常任务)、limited_sale<br>(限时促销)、login_reward(登录奖励) |
| start_time      | TIMESTAMP | 活动开始时间                                                                          |
| end_time        | TIMESTAMP | 活动结束时间                                                                          |
| status          | STRING    | 活动状态:active(进⾏中)、ended(已结束)、upcoming(未开始)                                       |
| target_segments | ARRAY     | ⽬标⽤户群体,如 all(全体)、vip_6_plus(VIP6及以上)、new_user_7d<br>(注册7天内新⽤户)                  |
| rewards         | ARRAY     | 奖励配置列表,每项包含触发条件(condition)和奖励物品(items)                                          |
| min_level       | INTEGER   | 参与所需最低等级                                                                        |
| push_enabled    | BOOLEAN   | 是否推送通知                                                                          |