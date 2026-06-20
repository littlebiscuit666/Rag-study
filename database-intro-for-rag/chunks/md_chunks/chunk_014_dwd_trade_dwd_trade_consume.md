---
chunk_id: chunk_014
domain: dwd_trade
domain_name: 交易数据库
table: dwd_trade_consume
table_name: 游戏内消费表
section: null
section_type: null
level: table
char_count: 1383
source_file: database-intro-for-rag.md
---

[数据域: 交易数据库(dwd_trade)] [表: dwd_trade_consume 游戏内消费表]

数据表:dwd\_trade\_consume(游戏内消费表)

描述: 玩家使⽤游戏内货币(⾦币、钻⽯)购买商品的流⽔记录。

| 字段名           | 类型     | 含义                                                                        |
|---------------|--------|---------------------------------------------------------------------------|
| consume_id    | STRING | 消费流⽔唯⼀标识,主键                                                               |
| user_id       | STRING | 消费玩家 ID                                                                   |
| game_id       | STRING | 游戏标识                                                                      |
| consume_type  | STRING | 消费类型:shop_purchase(商店购买)、upgrade(升级强化)、<br>craft(合成制作)、guild_donate(公会捐献) |
| currency_type | STRING | 消耗的货币类型:diamond(钻⽯)、gold(⾦币)                                              |
| amount        | BIGINT | 消耗数量                                                                      |
| item_id       | STRING | 购买/消耗对应的道具 ID                                                             |

| 字段名                   | 类型        | 含义      |
|-----------------------|-----------|---------|
| item_quantity         | INTEGER   | 购买道具数量  |
| shop_id               | STRING    | 所在商店 ID |
| timestamp             | TIMESTAMP | 消费发⽣时间  |
| balance_after_diamond | BIGINT    | 消费后钻⽯余额 |
| balance_after_gold    | BIGINT    | 消费后⾦币余额 |