---
chunk_id: chunk_041
domain: global
domain_name: 全局
table: null
table_name: null
section: 数据域关系总览
section_type: null
level: global
char_count: 402
source_file: database-intro-for-rag.md
---

[全局: 数据域关系总览]

## 数据域关系总览

```
原始事件 (ods_event_log)
 ↓ 实时计算 (Flink)
计算特征 (feature_store) ← ⽤户基础信息 (dim_user_info)
 ↓ 物料内容 (dim_item / dim_activity)
 ↓ 社交数据 (dwd_social_relation)
 ↓ 交易数据 (dwd_trade_order)
模型预测 (model_output)
 ↓
⽤户画像 (ads_user_profile)
 ↓ ↘
推荐结果 (ads_recommend) 策略匹配 (dwd_strategy_config)
 ↓ ↓
 AB实验 (dwd_ab_experiment)
 ↓
 效果监控 (ads_strategy_monitor)
 ↓
 Agent对话 (dwd_agent_session)
```