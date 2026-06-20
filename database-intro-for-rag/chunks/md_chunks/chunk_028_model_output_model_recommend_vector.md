---
chunk_id: chunk_028
domain: model_output
domain_name: 模型预测结果库
table: model_recommend_vector
table_name: 推荐向量表
section: null
section_type: null
level: table
char_count: 767
source_file: database-intro-for-rag.md
---

[数据域: 模型预测结果库(model_output)] [表: model_recommend_vector 推荐向量表]

数据表:model\_recommend\_vector(推荐向量表)

描述: 基于双塔推荐模型产出的⽤户偏好向量,⽤于商品的向量相似度召回。

| 字段名             | 类型        | 含义                                  |
|-----------------|-----------|-------------------------------------|
| user_id         | STRING    | 玩家 ID,主键                            |
| model_name      | STRING    | 模型标识,如 two_tower_recommendation     |
| model_version   | STRING    | 模型版本                                |
| computed_at     | TIMESTAMP | 向量计算时间                              |
| user_vector     | ARRAY     | ⽤户偏好向量(float<br>数组),维度为 64 维        |
| vector_dim      | INTEGER   | 向量维度,默认 64                          |
| top_preferences | ARRAY     | ⽤户偏好品类 Top5,每项包含品类名和偏好分数,由向量余弦相似度计算 |