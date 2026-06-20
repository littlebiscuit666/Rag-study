---
chunk_id: chunk_009
domain: dim_user
domain_name: 用户基础信息库
table: dim_user_info
table_name: 用户基础维度表
section: null
section_type: null
level: table
char_count: 3334
source_file: database-intro-for-rag.md
---

[数据域: 用户基础信息库(dim_user)] [表: dim_user_info 用户基础维度表]

数据表:dim\_user\_info

描述: ⽤户基础维度表,⼀个玩家在⼀款游戏中对应⼀条记录。

| 字段名     | 类型     | 含义        |
|---------|--------|-----------|
| user_id | STRING | 玩家唯⼀标识,主键 |

| 字段名                   | 类型        | 含义                                                               |
|-----------------------|-----------|------------------------------------------------------------------|
| game_id               | STRING    | 游戏标识                                                             |
| server_id             | STRING    | 所在服务器                                                            |
| register_time         | TIMESTAMP | 注册时间                                                             |
| register_channel      | STRING    | 注册渠道,如 wechat_mini_program、app_store、google_play                 |
| device_id             | STRING    | 注册时使⽤的设备 ID                                                      |
| device_model          | STRING    | 设备型号                                                             |
| os                    | STRING    | 操作系统版本                                                           |
| screen_resolution     | STRING    | 屏幕分辨率                                                            |
| account_type          | STRING    | 账号类型,如 wechat、qq、phone                                           |
| is_realname_verified  | BOOLEAN   | 是否完成实名认证                                                         |
| age_group             | STRING    | 年龄段,如 18-24、25-30、31-40                                          |
| gender                | STRING    | 性别:male(男)、female(⼥)、unknown(未知)                                 |
| region                | STRING    | 所在地区(省市级)                                                        |
| game_level            | INTEGER   | 游戏等级                                                             |
| character_class       | STRING    | 职业,如 swordsman(剑⼠)、mage(法师)、archer(⼸⼿)                           |
| combat_power          | BIGINT    | 战⼒值                                                              |
| rank                  | STRING    | 竞技段位,如 bronze(⻘铜)、silver(⽩银)、gold(⻩⾦)、<br>diamond(钻⽯)、master(⼤师) |
| rank_score            | INTEGER   | 竞技积分                                                             |
| vip_level             | INTEGER   | VIP 等级(0-15),由累计充值⾦额决定                                           |
| guild_id              | STRING    | 所在公会 ID,未加⼊公会时为空                                                 |
| guild_role            | STRING    | 公会职位:leader(会⻓)、vice_leader(副会⻓)、elite(精英)、<br>member(普通成员)      |
| total_recharge        | DECIMAL   | 累计充值⾦额(元)                                                        |
| total_consume_gold    | BIGINT    | 累计消耗⾦币总量                                                         |
| total_consume_diamond | BIGINT    | 累计消耗钻⽯总量                                                         |
| first_recharge_time   | TIMESTAMP | ⾸次充值时间                                                           |

| 字段名                   | 类型        | 含义       |
|-----------------------|-----------|----------|
| first_recharge_amount | DECIMAL   | ⾸次充值⾦额   |
| last_recharge_time    | TIMESTAMP | 最近⼀次充值时间 |
| monthly_card_expire   | DATE      | ⽉卡到期⽇期   |
| battle_pass_expire    | DATE      | 战令到期⽇期   |