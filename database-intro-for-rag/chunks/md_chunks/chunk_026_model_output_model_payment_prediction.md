---
chunk_id: chunk_026
domain: model_output
domain_name: 模型预测结果库
table: model_payment_prediction
table_name: 付费预测表
section: null
section_type: null
level: table
char_count: 1430
source_file: database-intro-for-rag.md
---

[数据域: 模型预测结果库(model_output)] [表: model_payment_prediction 付费预测表]

数据表:model\_payment\_prediction(付费预测表)

描述: 基于 DeepFM 模型产出的⽤户付费倾向预测,每⽇全量更新。

| 字段名           | 类型        | 含义                               |
|---------------|-----------|----------------------------------|
| user_id       | STRING    | 玩家 ID,主键                         |
| model_name    | STRING    | 模型标识,如 payment_prediction_deepfm |
| model_version | STRING    | 模型版本                             |
| predict_time  | TIMESTAMP | 预测执⾏时间                           |
| pay_prob_7d   | FLOAT     | 7 ⽇内付费概率(0-1)                    |
| pay_prob_14d  | FLOAT     | 14 ⽇内付费概率(0-1)                   |

| 字段名                     | 类型      | 含义                                                      |
|-------------------------|---------|---------------------------------------------------------|
| estimated_amount_30d    | DECIMAL | 预估 30 ⽇内充值⾦额(元)                                         |
| ltv_90d_estimate        | DECIMAL | 预估 90 ⽇⽣命周期价值(元)                                        |
| ltv_180d_estimate       | DECIMAL | 预估 180 ⽇⽣命周期价值(元)                                       |
| pay_tendency            | STRING  | 付费倾向:none(不付费)、low(低)、medium(中)、high(⾼)                 |
| price_sensitivity_level | STRING  | 价格敏感度等级:low(低敏感,愿意⾼额付费)、medium(中等)、<br>high(⾼敏感,需促销才付费) |
| top_factors             | ARRAY   | 影响付费预测的 Top5 特征及重要性分数                                   |