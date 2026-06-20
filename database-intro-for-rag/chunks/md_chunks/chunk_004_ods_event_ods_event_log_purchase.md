---
chunk_id: chunk_004
domain: ods_event
domain_name: 原始事件数据库
table: ods_event_log
table_name: 游戏行为事件总表
section: purchase
section_type: event_properties
level: sub_table
char_count: 886
source_file: database-intro-for-rag.md
---

[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表] [充值事件]

充值事件(purchase)properties 字段:

| 字段名               | 含义                                                     |
|-------------------|--------------------------------------------------------|
| order_id          | 充值订单 ID                                                |
| product_id        | 商品 ID                                                  |
| amount            | 充值⾦额(⼈⺠币元)                                             |
| currency          | 货币类型,默认 CNY                                            |
| payment_channel   | ⽀付渠道,如 wechat_pay、alipay                               |
| item_type         | 商品类型,如 subscription(订阅类)、consumable(消耗品)、equipment(装备) |
| is_first_purchase | 是否⾸次充值                                                 |
| vip_exp_gained    | 本次充值获得的 VIP 经验值                                        |

###