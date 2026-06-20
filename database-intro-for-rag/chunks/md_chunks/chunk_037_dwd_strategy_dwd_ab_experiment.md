---
chunk_id: chunk_037
domain: dwd_strategy
domain_name: 策略与A/B实验库
table: dwd_ab_experiment
table_name: AB实验表
section: null
section_type: null
level: table
char_count: 2006
source_file: database-intro-for-rag.md
---

[数据域: 策略与A/B实验库(dwd_strategy)] [表: dwd_ab_experiment AB实验表]

数据表:dwd\_ab\_experiment(AB实验表)

描述: AB 实验的配置和统计结果表。

| 字段名           | 类型     | 含义                               |
|---------------|--------|----------------------------------|
| experiment_id | STRING | 实验唯⼀标识,主键                        |
| name          | STRING | 实验名称                             |
| description   | STRING | 实验⽬的描述                           |
| layer         | STRING | 实验层,⽤于保证多实验互斥性(同⼀⽤户在同⼀层只能进⼊⼀个实验) |

| 字段名                | 类型        | 含义                                         |
|--------------------|-----------|--------------------------------------------|
| status             | STRING    | 实验状态:draft(草稿)、running(进⾏中)、completed(已完成) |
| start_time         | TIMESTAMP | 实验开始时间                                     |
| end_time           | TIMESTAMP | 实验结束时间                                     |
| variant_name       | STRING    | 分组名称:control(对照组)、variant_A/B/C            |
| traffic_ratio      | FLOAT     | 该分组流量⽐例(所有分组之和为 1.0)                       |
| is_control         | BOOLEAN   | 是否为对照组                                     |
| variant_config     | JSON      | 该分组的实验配置                                   |
| metrics            | ARRAY     | 实验关注的核⼼指标列表                                |
| significance_level | FLOAT     | 统计显著性⽔平(通常设为 0.05,即 5%)                    |
| min_sample_size    | INTEGER   | 得出可信结论所需的最⼩样本量                             |
| sample_size        | INTEGER   | 该分组当前样本量                                   |
| day7_retention     | FLOAT     | 该分组 7 ⽇留存率统计值                              |
| arpu_14d           | FLOAT     | 该分组 14 ⽇ ARPU 统计值                          |
| p_value_vs_control | FLOAT     | 与对照组⽐较的 p 值                                |
| is_significant     | BOOLEAN   | 是否达到统计显著性                                  |
| uplift             | FLOAT     | 相对对照组的提升幅度                                 |
| recommendation     | STRING    | 基于统计结果的推荐决策                                |