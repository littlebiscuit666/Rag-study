---
chunk_id: chunk_025
domain: model_output
domain_name: 模型预测结果库
table: model_churn_prediction
table_name: 流失预测表
section: null
section_type: null
level: table
char_count: 1779
source_file: database-intro-for-rag.md
---

[数据域: 模型预测结果库(model_output)] [表: model_churn_prediction 流失预测表]

数据表:model\_churn\_prediction(流失预测表)

描述: 基于 XGBoost 模型产出的⽤户流失⻛险预测,每⽇全量更新。

| 字段名              | 类型        | 含义                                                                      |
|------------------|-----------|-------------------------------------------------------------------------|
| user_id          | STRING    | 玩家 ID,主键                                                                |
| model_name       | STRING    | 模型标识,如 churn_prediction_xgb                                             |
| model_version    | STRING    | 模型版本,如 v2.3.1                                                           |
| predict_time     | TIMESTAMP | 预测执⾏时间                                                                  |
| churn_prob_7d    | FLOAT     | 7 ⽇内流失概率(0-1)                                                           |
| churn_prob_14d   | FLOAT     | 14 ⽇内流失概率(0-1)                                                          |
| churn_prob_30d   | FLOAT     | 30 ⽇内流失概率(0-1)                                                          |
| is_high_risk_7d  | BOOLEAN   | 7 ⽇内是否判定为⾼危流失⽤户(概率 > 0.5)                                               |
| is_high_risk_14d | BOOLEAN   | 14 ⽇内是否判定为⾼危流失⽤户(概率 > 0.5)                                              |
| risk_level       | STRING    | 综合流失⻛险等级:low(低)、medium(中)、high(⾼)                                       |
| top_factors      | ARRAY     | Top5 影响因⼦,每项包含特征名、特征值、重要性分数和⽅向(positive<br>代表该特征降低流失⻛险,negative 代表增加⻛险) |
| model_confidence | FLOAT     | 模型预测置信度(0-1)                                                            |

关键说明: 流失定义为玩家连续 N 天未登录游戏。流失预测模型的训练标签基于历史数据中实际发⽣的流失 事件。top\_factors 中 direction 为 negative 的特征(如 days\_since\_last\_login 值⼤)表示该特征值越⾼, 流失⻛险越⼤。