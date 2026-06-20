---
chunk_id: chunk_038
domain: ads_monitor
domain_name: 监控指标库
table: ads_daily_metrics
table_name: 业务大盘日报表
section: null
section_type: null
level: table
char_count: 2041
source_file: database-intro-for-rag.md
---

[数据域: 监控指标库(ads_monitor)] [表: ads_daily_metrics 业务大盘日报表]

数据表:ads\_daily\_metrics(业务⼤盘⽇报表)

描述: 游戏核⼼业务指标的每⽇快照,每⽇凌晨 0 点产出前⼀⽇数据。

| 字段名                      | 类型      | 含义                                            |
|--------------------------|---------|-----------------------------------------------|
| game_id                  | STRING  | 游戏标识,主键之⼀                                     |
| date                     | DATE    | 统计⽇期,主键之⼀                                     |
| dau                      | INTEGER | ⽇活跃⽤户数(当⽇有登录⾏为的去重⽤户数)                         |
| dau_wow_change           | FLOAT   | DAU 周同⽐变化率(正为增⻓,负为下降)                         |
| new_users                | INTEGER | 新增注册⽤户数                                       |
| avg_session_duration     | FLOAT   | 全体⽤户当⽇平均单次游戏时⻓(秒)                             |
| avg_sessions_per_user    | FLOAT   | 活跃⽤户当⽇平均游戏次数                                  |
| dau_mau_ratio            | FLOAT   | DAU/MAU ⽐值,反映⽤户粘性                             |
| day1_retention           | FLOAT   | 新⽤户次⽇留存率                                      |
| day7_retention           | FLOAT   | 新⽤户 7 ⽇留存率                                    |
| day30_retention          | FLOAT   | 新⽤户 30 ⽇留存率                                   |
| pay_rate                 | FLOAT   | 当⽇付费⽤户占 DAU 的⽐例                               |
| arpu                     | DECIMAL | 当⽇全⽤户⼈均收⼊(元)                                  |
| arppu                    | DECIMAL | 当⽇付费⽤户⼈均收⼊(元)                                 |
| total_revenue            | DECIMAL | 当⽇总营收(元)                                      |
| revenue_wow_change       | FLOAT   | 营收周同⽐变化率                                      |
| arena_participation_rate | FLOAT   | 竞技场参与率(参与竞技场的 DAU ⽐例)                         |
| guild_activity_rate      | FLOAT   | 公会活跃率(参与公会活动的 DAU ⽐例)                         |
| crash_rate               | FLOAT   | 崩溃率(崩溃次数/会话次数)                                |
| alerts                   | ARRAY   | 指标异常告警列表,每项包含告警 ID、严重程度、指标名、当前值、阈<br>值和建议处理措施 |