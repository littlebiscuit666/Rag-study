---
chunk_id: chunk_027
domain: model_output
domain_name: 模型预测结果库
table: model_cluster
table_name: 用户聚类分群表
section: null
section_type: null
level: table
char_count: 1131
source_file: database-intro-for-rag.md
---

[数据域: 模型预测结果库(model_output)] [表: model_cluster 用户聚类分群表]

数据表:model\_cluster(⽤户聚类分群表)

描述: 基于 K-Means 聚类模型产出的⽤户分群结果,每周全量更新。

| 字段名                     | 类型        | 含义                            |
|-------------------------|-----------|-------------------------------|
| user_id                 | STRING    | 玩家 ID,主键                      |
| model_name              | STRING    | 模型标识,如 user_clustering_kmeans |
| model_version           | STRING    | 模型版本                          |
| predict_time            | TIMESTAMP | 预测执⾏时间                        |
| cluster_id              | INTEGER   | 聚类簇 ID(0 开始编号)                |
| cluster_name            | STRING    | 聚类簇业务名称,如"竞技型中氪玩家"、"休闲型免费玩家"  |
| cluster_description     | STRING    | 该簇⽤户群体的⾏为特征描述                 |
| avg_login_days_per_week | FLOAT     | 该簇玩家平均每周登录天数                  |
| avg_pvp_ratio           | FLOAT     | 该簇玩家 PVP 参与⽐例均值               |
| avg_monthly_spend       | DECIMAL   | 该簇玩家⽉均消费⾦额均值                  |
| cluster_size            | INTEGER   | 该簇当前玩家总⼈数                     |
| cluster_percentage      | FLOAT     | 该簇占全体玩家的⽐例                    |