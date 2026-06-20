---
chunk_id: chunk_036
domain: dwd_strategy
domain_name: 策略与A/B实验库
table: dwd_strategy_config
table_name: 策略配置表
section: null
section_type: null
level: table
char_count: 2432
source_file: database-intro-for-rag.md
---

[数据域: 策略与A/B实验库(dwd_strategy)] [表: dwd_strategy_config 策略配置表]

数据表:dwd\_strategy\_config(策略配置表)

描述: 运营策略的完整配置,由 Agent 或运营⼈员创建。

| 字段名                        | 类型        | 含义                                                                                 |
|----------------------------|-----------|------------------------------------------------------------------------------------|
| strategy_id                | STRING    | 策略唯⼀标识,主键                                                                          |
| name                       | STRING    | 策略名称                                                                               |
| strategy_type              | STRING    | 策略类型:churn_save(流失挽留)、payment_convert(付费<br>转化)、active_boost(活跃提升)、new_guide(新⼿引导) |
| status                     | STRING    | 策略状态:active(⽣效中)、paused(暂停)、ended(已结<br>束)                                         |
| priority                   | INTEGER   | 策略优先级(数值越⼤越优先,当⽤户同时命中多条策略时取最<br>⾼优先级执⾏)                                            |
| daily_quota                | INTEGER   | 每⽇最⼤触达⽤户数                                                                          |
| start_time                 | TIMESTAMP | 策略⽣效开始时间                                                                           |
| end_time                   | TIMESTAMP | 策略失效时间                                                                             |
| target_segment             | JSON      | ⽬标⽤户群体的过滤条件,⽀持组合条件                                                                 |
| conditions                 | JSON      | 策略触发的实时条件(基于特征值)                                                                   |
| actions                    | ARRAY     | 执⾏动作列表,每个动作包含渠道、触发时机、内容和频控规则                                                       |
| action_channel             | STRING    | 触达渠道:game_popup(游戏弹窗)、push_notification(推送<br>通知)、game_mail(游戏邮件)、banner(⾸⻚横幅)     |
| frequency_per_user_per_day | INTEGER   | 每⽤户每⽇最多触达次数(频控)                                                                    |
| frequency_per_user_total   | INTEGER   | 每⽤户累计最多触达次数(频控)                                                                    |
| ab_experiment_id           | STRING    | 关联的 AB 实验 ID                                                                       |
| created_by                 | STRING    | 创建者:agent(Agent ⾃动创建)或具体运营⼈员 ID                                                    |