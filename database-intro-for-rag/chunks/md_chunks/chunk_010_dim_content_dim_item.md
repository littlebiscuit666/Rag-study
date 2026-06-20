---
chunk_id: chunk_010
domain: dim_content
domain_name: 物料/内容数据库
table: dim_item
table_name: 道具表
section: null
section_type: null
level: table
char_count: 1833
source_file: database-intro-for-rag.md
---

[数据域: 物料/内容数据库(dim_content)] [表: dim_item 道具表]

数据表:dim\_item(道具表)

描述: 游戏内所有道具的配置信息,包含属性、价格、获取⽅式等。

| 字段名            | 类型      | 含义                                                                   |
|----------------|---------|----------------------------------------------------------------------|
| item_id        | STRING  | 道具唯⼀标识,主键                                                            |
| item_name      | STRING  | 道具名称                                                                 |
| item_type      | STRING  | 道具类型:equipment(装备)、consumable(消耗品)、cosmetic(外观)、<br>subscription(订阅) |
| item_category  | STRING  | 道具⼦类别,如 helmet(头盔)、weapon(武器)、potion(药⽔)                             |
| rarity         | STRING  | 道具品质:common(普通)、uncommon(精良)、rare(稀有)、epic(史<br>诗)、legendary(传说)     |
| level_required | INTEGER | 使⽤所需玩家等级                                                             |
| class_required | ARRAY   | 可使⽤的职业列表,空数组表示全职业通⽤                                                  |
| stats          | JSON    | 装备属性,如 defense(防御)、hp_bonus(⾎量加成)、crit_resist(暴击抗性)                  |
| price_gold     | BIGINT  | ⾦币价格(游戏内货币,⽆法直接充值)                                                   |
| price_diamond  | INTEGER | 钻⽯价格(⾼级货币,可充值获得)                                                     |
| price_cash     | DECIMAL | ⼈⺠币价格(限直购商品)                                                         |

| 字段名          | 类型      | 含义                                         |
|--------------|---------|--------------------------------------------|
| tags         | ARRAY   | 道具标签,⽤于推荐分类,如 pvp(竞技)、tank(坦克)、defense(防御) |
| release_date | DATE    | 道具发布⽇期                                     |
| is_limited   | BOOLEAN | 是否限时/限量道具                                  |
| drop_sources | ARRAY   | 可获取该道具的来源列表,如关卡 ID、商店 ID                   |