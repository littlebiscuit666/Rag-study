---
chunk_id: chunk_042
domain: global
domain_name: 全局
table: null
table_name: null
section: 附录·常用分析场景
section_type: null
level: global
char_count: 1487
source_file: database-intro-for-rag.md
---

[全局: 附录·常用分析场景]

## 附录:常⽤分析场景与对应数据表

| 分析场景         | 主要使⽤的数据表                                                                                   |
|--------------|--------------------------------------------------------------------------------------------|
| 流失⽤户分析       | dim_user_info + feature_user_online + model_churn_prediction + ods_event_log               |
| 付费转化分析       | dwd_trade_order + model_payment_prediction + ads_user_profile<br>+<br>dwd_strategy_monitor |
| 玩家⾏为路径分<br>析 | ods_event_log(按 session_id 聚合)                                                             |
| 推荐效果分析       | ads_recommend_log + dwd_ab_experiment + dwd_trade_order                                    |
| ⽤户分群洞察       | model_cluster + ads_user_profile<br>+ feature_user_online                                  |
| 公会社交分析       | dwd_social_relation + dim_guild + dwd_chat_log + ods_event_log(social_interact)            |
| 关卡设计优化       | dim_level + ods_event_log(level_complete + logout)                                         |
| RFM价值分层      | dwd_trade_order + feature_user_online(payment特征) + ads_user_profile                        |
| 新⼿留存优化       | dim_user_info(register_days <= 7) + ods_event_log + ads_daily_metrics                      |

| 分析场景    | 主要使⽤的数据表                                                          |
|---------|-------------------------------------------------------------------|
| 策略ROI评估 | dwd_strategy_config<br>+ ads_strategy_monitor + dwd_ab_experiment |