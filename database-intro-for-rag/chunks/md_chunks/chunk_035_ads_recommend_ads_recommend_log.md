---
chunk_id: chunk_035
domain: ads_recommend
domain_name: 推荐结果库
table: ads_recommend_log
table_name: 推荐日志表
section: null
section_type: null
level: table
char_count: 2071
source_file: database-intro-for-rag.md
---

[数据域: 推荐结果库(ads_recommend)] [表: ads_recommend_log 推荐日志表]

数据表:ads\_recommend\_log(推荐⽇志表)

描述: 推荐请求和响应的完整⽇志,每次请求对应⼀条记录。

| 字段名           | 类型        | 含义                                                                                  |  |  |
|---------------|-----------|-------------------------------------------------------------------------------------|--|--|
| request_id    | STRING    | 推荐请求唯⼀标识,主键                                                                         |  |  |
| user_id       | STRING    | 请求推荐的玩家 ID                                                                          |  |  |
| scene         | STRING    | 推荐场景:shop_home(商店⾸⻚)、battle_result(战⽃结算)、level_fail(关<br>卡失败)、daily_recommend(每⽇推荐) |  |  |
| top_k         | INTEGER   | 请求返回的推荐数量                                                                           |  |  |
| exclude_items | ARRAY     | 需排除的道具 ID 列表(如已购买的商品)                                                               |  |  |
| ab_group      | STRING    | 所在的 AB 实验分组                                                                         |  |  |
| timestamp     | TIMESTAMP | 请求时间                                                                                |  |  |
| item_rank     | INTEGER   | 推荐道具的排名(从 1 开始)                                                                     |  |  |
| item_id       | STRING    | 推荐道具 ID                                                                             |  |  |
| item_type     | STRING    | 推荐道具类型                                                                              |  |  |
| score         | FLOAT     | 推荐综合评分(0-1)                                                                         |  |  |
| recall_source | STRING    | 召回来源:vector(向量召回)、cf(协同过滤)、rule(规则召回)                                               |  |  |
| reason        | STRING    | 推荐理由,供前端展示                                                                          |  |  |
| latency_ms    | INTEGER   | 推荐服务响应时延(毫秒)                                                                        |  |  |