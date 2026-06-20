---
chunk_id: chunk_022
domain: feature_store
domain_name: 特征数据库
table: feature_user_online
table_name: 用户在线特征表
section: payment
section_type: feature_group
level: sub_table
char_count: 1019
source_file: database-intro-for-rag.md
---

[数据域: 特征数据库(feature_store)] [表: feature_user_online 用户在线特征表] [付费特征]

付费特征(payment):

| 特征名                        | 含义                                      |  |
|----------------------------|-----------------------------------------|--|
| arpu_30d                   | 近 30 ⽇平均付费⾦额(元)                         |  |
| payment_count_30d          | 近 30 ⽇充值次数                              |  |
| payment_count_7d           | 近 7 ⽇充值次数                               |  |
| last_purchase_days         | 距上次充值天数,0 代表今天已充值                       |  |
| avg_purchase_amount        | 历史每次充值的平均⾦额(元)                          |  |
| price_sensitivity          | 价格敏感度评分(0-1),值越低代表越不敏感                  |  |
| preferred_product_category | 偏好商品类别,如 subscription(订阅)、equipment(装备) |  |

| 特征名                    | 含义                  |
|------------------------|---------------------|
| is_monthly_card_active | 是否持有有效⽉卡:true/false |
| is_battle_pass_active  | 是否持有有效战令:true/false |
| ltv_estimate           | 预估⽣命周期价值(元)         |

###