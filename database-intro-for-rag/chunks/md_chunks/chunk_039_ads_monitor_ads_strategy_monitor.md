---
chunk_id: chunk_039
domain: ads_monitor
domain_name: 监控指标库
table: ads_strategy_monitor
table_name: 策略效果监控表
section: null
section_type: null
level: table
char_count: 1438
source_file: database-intro-for-rag.md
---

[数据域: 监控指标库(ads_monitor)] [表: ads_strategy_monitor 策略效果监控表]

数据表:ads\_strategy\_monitor(策略效果监控表)

描述: 运营策略的触达漏⽃和效果归因数据,每⽇更新。

| 字段名          | 类型     | 含义         |
|--------------|--------|------------|
| strategy_id  | STRING | 策略 ID,主键之⼀ |
| monitor_date | DATE   | 监控⽇期,主键之⼀  |

| 字段名                 | 类型      | 含义                              |
|---------------------|---------|---------------------------------|
| exposed             | INTEGER | 策略触达(曝光)⽤户数                     |
| clicked             | INTEGER | 点击触达内容的⽤户数                      |
| engaged             | INTEGER | 深度参与(进⾏⽬标⾏为)的⽤户数                |
| retained_7d         | INTEGER | 7 ⽇内留存的⽤户数                      |
| paid_7d             | INTEGER | 7 ⽇内产⽣付费的⽤户数                    |
| click_rate          | FLOAT   | 点击率(clicked/exposed)            |
| engage_rate         | FLOAT   | 参与率(engaged/exposed)            |
| retain_rate         | FLOAT   | 留存率(retained_7d/exposed)        |
| pay_rate            | FLOAT   | 付费率(paid_7d/exposed)            |
| retention_uplift    | FLOAT   | 相对对照组的留存提升幅度                    |
| revenue_uplift      | FLOAT   | 相对对照组的收⼊提升幅度(元/⽤户)              |
| is_significant      | BOOLEAN | 效果是否显著                          |
| cost                | DECIMAL | 策略执⾏成本(礼包/奖励物价值,元)              |
| incremental_revenue | DECIMAL | 因策略带来的增量收⼊(元)                   |
| roi_ratio           | FLOAT   | 投资回报率(incremental_revenue/cost) |