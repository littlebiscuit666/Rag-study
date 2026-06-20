---
chunk_id: chunk_013
domain: dwd_trade
domain_name: 交易数据库
table: dwd_trade_order
table_name: 充值订单表
section: null
section_type: null
level: table
char_count: 1861
source_file: database-intro-for-rag.md
---

[数据域: 交易数据库(dwd_trade)] [表: dwd_trade_order 充值订单表]

数据表:dwd\_trade\_order(充值订单表)

描述: 玩家现⾦充值的完整订单记录,每笔充值对应⼀条记录。

| 字段名        | 类型     | 含义          |
|------------|--------|-------------|
| order_id   | STRING | 充值订单唯⼀标识,主键 |
| user_id    | STRING | 充值玩家 ID     |
| game_id    | STRING | 游戏标识        |
| product_id | STRING | 充值商品 ID     |

| 字段名               | 类型        | 含义                                                         |
|-------------------|-----------|------------------------------------------------------------|
| product_name      | STRING    | 充值商品名称,如⽉卡、钻⽯礼包、战令                                         |
| amount            | DECIMAL   | 充值⾦额(元)                                                    |
| currency          | STRING    | 货币类型,默认 CNY                                                |
| payment_channel   | STRING    | ⽀付渠道:wechat_pay(微信⽀付)、alipay(⽀付宝)、apple_pay、<br>google_pay |
| payment_status    | STRING    | ⽀付状态:success(成功)、failed(失败)、refund(退款)                     |
| payment_time      | TIMESTAMP | ⽀付完成时间                                                     |
| create_time       | TIMESTAMP | 订单创建时间                                                     |
| complete_time     | TIMESTAMP | 订单完成时间                                                     |
| is_first_purchase | BOOLEAN   | 是否玩家⾸笔充值                                                   |
| is_refund         | BOOLEAN   | 是否发⽣退款                                                     |
| platform          | STRING    | 充值平台                                                       |
| promotion_id      | STRING    | 使⽤的促销活动 ID                                                 |
| discount_amount   | DECIMAL   | 优惠折扣⾦额                                                     |
| actual_paid       | DECIMAL   | 实际⽀付⾦额(扣除折扣后)                                              |