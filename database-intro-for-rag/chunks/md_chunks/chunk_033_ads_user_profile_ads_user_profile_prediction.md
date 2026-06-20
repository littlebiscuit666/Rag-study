---
chunk_id: chunk_033
domain: ads_user_profile
domain_name: 用户画像标签库
table: ads_user_profile
table_name: 用户画像宽表
section: prediction
section_type: tag_group
level: sub_table
char_count: 723
source_file: database-intro-for-rag.md
---

[数据域: 用户画像标签库(ads_user_profile)] [表: ads_user_profile 用户画像宽表] [预测模型标签]

预测模型标签(tags.prediction):

| 标签名                   | 含义                                 |  |  |
|-----------------------|------------------------------------|--|--|
| churn_risk_7d         | 7 ⽇流失⻛险等级:high、medium、low          |  |  |
| churn_risk_30d        | 30 ⽇流失⻛险等级:high、medium、low         |  |  |
| churn_prob_30d        | 30 ⽇流失概率数值(0-1)                    |  |  |
| pay_tendency_7d       | 7 ⽇内付费倾向:high、medium、low、none      |  |  |
| estimated_ltv_90d     | 预估 90 ⽇ LTV(元)                     |  |  |
| next_likely_action    | 预测下次最可能的游戏⾏为,如 arena_battle(参与竞技场) |  |  |
| content_fatigue_score | 内容疲倦度评分(0-1),值越⾼代表玩家对当前内容的新鲜感越低    |  |  |

###