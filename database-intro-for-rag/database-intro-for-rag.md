# GameUserInsight 数据库介绍⽂档

本⽂档⽤于 RAG 检索测试,介绍 GameUserInsight 游戏⽤户画像系统中涉及的所有数据域、数据表 及核⼼字段含义,适合按模块分块进⾏语义检索。

## ⼀、原始事件数据库(ods\_event)

#### 概述

原始事件数据库是整个系统的数据源头,记录游戏客户端 SDK 实时上报的所有玩家⾏为事件,通过 Kafka 消息队列流式写⼊。每条事件均为⼀个独⽴的 JSON 消息,包含事件标识、玩家标识、时间戳、设备信息和 业务属性。

## 数据表:ods\_event\_log

描述: 游戏⾏为事件总表,按 event\_type 区分事件类型,每种事件类型在 properties 字段中携带不同的业 务属性。

| 字段名         | 类型        | 含义                                                                                                                      |
|-------------|-----------|-------------------------------------------------------------------------------------------------------------------------|
| event_id    | STRING    | 事件唯⼀标识,格式 evt_{⽇期}{序号}{随机串}                                                                                             |
| event_type  | STRING    | 事件类型,枚举值:login(登录)、logout(退出)、battle(战⽃)、purchase<br>(充值)、item_use(道具使⽤)、level_complete(关卡完成)、social_interact<br>(社交互动) |
| user_id     | STRING    | 玩家唯⼀标识,系统内唯⼀,格式 U{8位数字}                                                                                                 |
| game_id     | STRING    | 游戏标识,⼀个系统可接⼊多款游戏                                                                                                        |
| server_id   | STRING    | 游戏服务器标识                                                                                                                 |
| timestamp   | TIMESTAMP | 事件发⽣的 UTC 时间,精确到毫秒                                                                                                      |
| device_id   | STRING    | 设备唯⼀标识,同⼀设备跨账号登录时相同                                                                                                     |
| platform    | STRING    | 客户端平台,枚举值:Android、iOS、PC、H5                                                                                             |
| app_version | STRING    | 游戏客户端版本号                                                                                                                |
| session_id  | STRING    | 会话标识,⽤于关联同⼀次游戏会话内的事件序列                                                                                                  |

| 字段名        | 类型     | 含义                            |
|------------|--------|-------------------------------|
| network    | STRING | ⽹络类型,枚举值:WiFi、4G、5G、其他        |
| properties | JSON   | 事件专属属性,不同 event_type 有不同的字段结构 |

### 登录事件(login)properties 字段:

| 字段名               | 含义                                      |
|-------------------|-----------------------------------------|
| ip                | 玩家登录 IP 地址(已脱敏)                         |
| client_os         | 操作系统版本                                  |
| device_model      | 设备型号,如 Xiaomi 14 Pro                    |
| screen_resolution | 屏幕分辨率                                   |
| login_channel     | 登录渠道,如 wechat(微信)、qq、phone              |
| login_type        | 登录类型,如 token(Token ⾃动登录)、password(密码登录) |

### 战⽃事件(battle)properties 字段:

| 字段名                       | 含义                                                       |
|---------------------------|----------------------------------------------------------|
| battle_type               | 战⽃类型,如 pvp_arena(竞技场)、pve_dungeon(副本)、guild_war(公会<br>战) |
| battle_id                 | 单次战⽃唯⼀标识                                                 |
| map_id                    | 地图标识                                                     |
| result                    | 战⽃结果:win(胜利)、lose(失败)、draw(平局)                           |
| duration_sec              | 战⽃持续时⻓(秒)                                                |
| character_level           | 参战⻆⾊等级                                                   |
| kills/deaths/assists      | 击杀/死亡/助攻数                                                |
| damage_dealt/damage_taken | 造成伤害/承受伤害                                                |
| rating_change             | 竞技积分变化量(正为增加,负为减少)                                       |
| items_used                | 战⽃中使⽤的道具 ID 列表                                           |
| opponent_avg_rating       | 对⼿平均竞技积分                                                 |

### 充值事件(purchase)properties 字段:

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

### 道具使⽤事件(item\_use)properties 字段:

| 字段名                | 含义                                   |
|--------------------|--------------------------------------|
| item_id            | 使⽤的道具 ID                             |
| item_category      | 道具类别,如 consumable(消耗品)、equipment(装备) |
| quantity           | 使⽤数量                                 |
| source             | 道具来源,如 inventory(背包)、shop(商店)        |
| exp_gained         | 使⽤后获得的经验值(仅适⽤于经验道具)                  |
| remaining_quantity | 使⽤后背包剩余数量                            |

#### 关卡完成事件(level\_complete)properties 字段:

| 字段名                      | 含义                                 |  |
|--------------------------|------------------------------------|--|
| chapter_id               | 章节 ID                              |  |
| level_id                 | 关卡 ID                              |  |
| difficulty               | 难度:normal(普通)、hard(困难)、extreme(极难) |  |
| result                   | 完成状态:complete(完成)、fail(失败)         |  |
| stars                    | 星级评价(1-3星)                         |  |
| attempts                 | 本次关卡累计尝试次数                         |  |
| exp_gained / gold_gained | 本关卡获得经验/⾦币奖励                       |  |

| 字段名           | 含义                  |  |
|---------------|---------------------|--|
| drops         | 掉落物品列表,含道具 ID、品质、数量 |  |
| party_members | 组队成员的 user_id 列表    |  |

### 退出事件(logout)properties 字段:

| 字段名                  | 含义                                           |  |
|----------------------|----------------------------------------------|--|
| session_duration_sec | 本次会话时⻓(秒)                                    |  |
| logout_reason        | 退出原因,如 user_exit(主动退出)、crash(崩溃)、timeout(超时) |  |
| last_scene           | 退出前所在场景,如 main_city(主城)、dungeon(副本)          |  |
| last_action          | 退出前最后⼀次操作                                    |  |

#### 社交互动事件(social\_interact)properties 字段:

| 字段名             | 含义                                                                      |  |
|-----------------|-------------------------------------------------------------------------|--|
| social_type     | 社交类型:guild_donate(公会捐献)、friend_add(添加好友)、chat(聊天)、team_battle<br>(组队战⽃) |  |
| guild_id        | 公会 ID(公会相关社交⾏为时存在)                                                      |  |
| target_user_id  | 互动对象⽤户 ID(私聊、好友申请等场景)                                                   |  |
| donation_amount | 捐献数量(仅公会捐献时存在)                                                          |  |

## ⼆、⽤户基础信息库(dim\_user)

#### 概述

⽤户基础信息库是玩家的静态维度表,记录玩家的注册信息、设备信息、账号属性和游戏内⻆⾊的基础状 态。该库中的数据为快照数据,每⽇更新,部分字段(如 game\_info)会随游戏进程变化⽽更新。

数据表:dim\_user\_info

描述: ⽤户基础维度表,⼀个玩家在⼀款游戏中对应⼀条记录。

| 字段名     | 类型     | 含义        |
|---------|--------|-----------|
| user_id | STRING | 玩家唯⼀标识,主键 |

| 字段名                   | 类型        | 含义                                                               |
|-----------------------|-----------|------------------------------------------------------------------|
| game_id               | STRING    | 游戏标识                                                             |
| server_id             | STRING    | 所在服务器                                                            |
| register_time         | TIMESTAMP | 注册时间                                                             |
| register_channel      | STRING    | 注册渠道,如 wechat_mini_program、app_store、google_play                 |
| device_id             | STRING    | 注册时使⽤的设备 ID                                                      |
| device_model          | STRING    | 设备型号                                                             |
| os                    | STRING    | 操作系统版本                                                           |
| screen_resolution     | STRING    | 屏幕分辨率                                                            |
| account_type          | STRING    | 账号类型,如 wechat、qq、phone                                           |
| is_realname_verified  | BOOLEAN   | 是否完成实名认证                                                         |
| age_group             | STRING    | 年龄段,如 18-24、25-30、31-40                                          |
| gender                | STRING    | 性别:male(男)、female(⼥)、unknown(未知)                                 |
| region                | STRING    | 所在地区(省市级)                                                        |
| game_level            | INTEGER   | 游戏等级                                                             |
| character_class       | STRING    | 职业,如 swordsman(剑⼠)、mage(法师)、archer(⼸⼿)                           |
| combat_power          | BIGINT    | 战⼒值                                                              |
| rank                  | STRING    | 竞技段位,如 bronze(⻘铜)、silver(⽩银)、gold(⻩⾦)、<br>diamond(钻⽯)、master(⼤师) |
| rank_score            | INTEGER   | 竞技积分                                                             |
| vip_level             | INTEGER   | VIP 等级(0-15),由累计充值⾦额决定                                           |
| guild_id              | STRING    | 所在公会 ID,未加⼊公会时为空                                                 |
| guild_role            | STRING    | 公会职位:leader(会⻓)、vice_leader(副会⻓)、elite(精英)、<br>member(普通成员)      |
| total_recharge        | DECIMAL   | 累计充值⾦额(元)                                                        |
| total_consume_gold    | BIGINT    | 累计消耗⾦币总量                                                         |
| total_consume_diamond | BIGINT    | 累计消耗钻⽯总量                                                         |
| first_recharge_time   | TIMESTAMP | ⾸次充值时间                                                           |

| 字段名                   | 类型        | 含义       |
|-----------------------|-----------|----------|
| first_recharge_amount | DECIMAL   | ⾸次充值⾦额   |
| last_recharge_time    | TIMESTAMP | 最近⼀次充值时间 |
| monthly_card_expire   | DATE      | ⽉卡到期⽇期   |
| battle_pass_expire    | DATE      | 战令到期⽇期   |

## 三、物料/内容数据库(dim\_content)

#### 概述

内容数据库记录游戏内所有可交互的物料数据,包括道具、活动和关卡配置,是推荐系统的物品侧数据来 源。

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

数据表:dim\_activity(活动表)

描述: 游戏内运营活动配置,记录活动条件、奖励和⽬标⽤户群体。

| 字段名             | 类型        | 含义                                                                              |
|-----------------|-----------|---------------------------------------------------------------------------------|
| activity_id     | STRING    | 活动唯⼀标识,主键                                                                       |
| activity_name   | STRING    | 活动名称                                                                            |
| activity_type   | STRING    | 活动类型:festival(节⽇活动)、daily_quest(⽇常任务)、limited_sale<br>(限时促销)、login_reward(登录奖励) |
| start_time      | TIMESTAMP | 活动开始时间                                                                          |
| end_time        | TIMESTAMP | 活动结束时间                                                                          |
| status          | STRING    | 活动状态:active(进⾏中)、ended(已结束)、upcoming(未开始)                                       |
| target_segments | ARRAY     | ⽬标⽤户群体,如 all(全体)、vip_6_plus(VIP6及以上)、new_user_7d<br>(注册7天内新⽤户)                  |
| rewards         | ARRAY     | 奖励配置列表,每项包含触发条件(condition)和奖励物品(items)                                          |
| min_level       | INTEGER   | 参与所需最低等级                                                                        |
| push_enabled    | BOOLEAN   | 是否推送通知                                                                          |

数据表:dim\_level(关卡表)

描述: 游戏内所有 PVE 关卡的配置信息,包含难度、奖励和历史通关统计。

| 字段名        | 类型     | 含义        |
|------------|--------|-----------|
| level_id   | STRING | 关卡唯⼀标识,主键 |
| chapter_id | STRING | 所属章节 ID   |
| level_name | STRING | 关卡名称      |

| 字段名                | 类型      | 含义                                               |
|--------------------|---------|--------------------------------------------------|
| difficulty         | STRING  | 难度等级:normal、hard、extreme                         |
| level_type         | STRING  | 关卡类型:pve_dungeon(副本)、story(剧情)、boss_raid(团队Boss) |
| recommended_power  | BIGINT  | 建议通关战⼒                                           |
| min_level          | INTEGER | 进⼊所需最低等级                                         |
| time_limit_sec     | INTEGER | 关卡时间限制(秒)                                        |
| entry_cost_stamina | INTEGER | 进⼊消耗的体⼒值                                         |
| exp_base           | INTEGER | 基础经验奖励                                           |
| gold_base          | INTEGER | 基础⾦币奖励                                           |
| drop_table         | ARRAY   | 掉落物品配置,每项包含道具 ID、掉落概率、品质和数量范围                    |
| avg_complete_rate  | FLOAT   | 历史平均通关率                                          |
| avg_duration_sec   | FLOAT   | 历史平均通关时⻓(秒)                                      |
| avg_attempts       | FLOAT   | 历史平均挑战次数                                         |
| churn_rate_after   | FLOAT   | 失败后的玩家流失率(⽤于难度设计优化)                              |

## 四、交易数据库(dwd\_trade)

#### 概述

交易数据库记录游戏内所有与货币相关的流⽔数据,包括现⾦充值订单和游戏内货币消费记录,是营收分析 和⽤户付费⾏为研究的核⼼数据源。

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

## 五、社交数据库(dwd\_social)

#### 概述

社交数据库记录玩家之间的关系⽹络和互动⾏为数据,包括好友关系、公会成员关系和聊天记录,⽤于社交 ⽹络分析和社交影响⼒建模。

数据表:dwd\_social\_relation(好友关系表)

描述: 玩家之间的好友关系及亲密度数据,双向关系单条存储(A-B 和 B-A 各存⼀条)。

| 字段名                  | 类型        | 含义                                |
|----------------------|-----------|-----------------------------------|
| relationship_id      | STRING    | 关系唯⼀标识,主键                         |
| user_id              | STRING    | 发起⽅玩家 ID                          |
| friend_user_id       | STRING    | 接收⽅玩家 ID                          |
| game_id              | STRING    | 游戏标识                              |
| relationship_type    | STRING    | 关系类型:friend(好友)、blacklist(⿊名单)    |
| establish_time       | TIMESTAMP | 建⽴好友关系的时间                         |
| intimacy_score       | INTEGER   | 亲密度分数(0-1000),由互动⾏为频率计算           |
| chat_count_7d        | INTEGER   | 近 7 ⽇聊天消息数                        |
| team_battle_count_7d | INTEGER   | 近 7 ⽇⼀同组队战⽃次数                     |
| gift_count_7d        | INTEGER   | 近 7 ⽇互送礼物次数                       |
| status               | STRING    | 关系状态:active(活跃互动)、inactive(⻓期不互动) |

数据表:dim\_guild(公会信息表)

描述: 游戏内公会的基础信息及活跃度指标。

| 字段名                    | 类型        | 含义            |
|------------------------|-----------|---------------|
| guild_id               | STRING    | 公会唯⼀标识,主键     |
| guild_name             | STRING    | 公会名称          |
| game_id                | STRING    | 游戏标识          |
| server_id              | STRING    | 所在服务器         |
| leader_id              | STRING    | 会⻓玩家 ID       |
| create_time            | TIMESTAMP | 公会创建时间        |
| level                  | INTEGER   | 公会等级(1-20)    |
| member_count           | INTEGER   | 当前成员⼈数        |
| max_members            | INTEGER   | 公会成员上限        |
| total_power            | BIGINT    | 全体成员战⼒总和      |
| guild_fund             | BIGINT    | 公会基⾦(⾦币)      |
| guild_battle_count_7d  | INTEGER   | 近 7 ⽇参与公会战次数  |
| group_dungeon_count_7d | INTEGER   | 近 7 ⽇参与组队副本次数 |
| donation_total_gold_7d | BIGINT    | 近 7 ⽇全员捐献⾦币总量 |

数据表:dwd\_chat\_log(聊天记录表)

描述: 玩家聊天记录,已做内容脱敏,保留⽤于社交⾏为分析。

| 字段名          | 类型     | 含义                                              |
|--------------|--------|-------------------------------------------------|
| message_id   | STRING | 消息唯⼀标识,主键                                       |
| user_id      | STRING | 发送者玩家 ID                                        |
| game_id      | STRING | 游戏标识                                            |
| channel_type | STRING | 聊天频道类型:guild(公会)、world(世界)、private(私聊)、team(组队) |
| channel_id   | STRING | 频道 ID,如公会 ID 或私聊双⽅ ID                           |
| message_type | STRING | 消息类型:text(⽂字)、emoji(表情)、image(图⽚)               |

| 字段名        | 类型        | 含义             |
|------------|-----------|----------------|
| content    | STRING    | 消息内容(已脱敏)      |
| timestamp  | TIMESTAMP | 消息发送时间         |
| is_flagged | BOOLEAN   | 是否被⻛控系统标记为违规内容 |

## 六、特征数据库(feature\_store)

#### 概述

特征数据库由 Flink 实时计算引擎和 Spark 离线计算框架共同产出,将原始事件数据聚合为适合机器学习模 型使⽤的特征向量。在线特征存储于 Redis,供实时推理使⽤;离线特征存储于 Hive,供模型训练使⽤。

## 数据表:feature\_user\_online(⽤户在线特征表)

描述: Redis 中的⽤户实时特征快照,Key 为 user\_id,Value 为 JSON 格式的特征向量,每 5 分钟更新⼀ 次。

### 基础属性特征(basic):

| 特征名              | 含义                      |
|------------------|-------------------------|
| user_age_days    | ⽤户注册天数,计算⽅式:当前⽇期 - 注册⽇期 |
| total_recharge   | 累计充值⾦额(元)               |
| vip_level        | 当前 VIP 等级(0-15)         |
| game_level       | 当前游戏等级                  |
| combat_power     | 当前战⼒值                   |
| register_channel | 注册渠道编码                  |

#### 活跃度特征(activity):

| 特征名             | 含义               |
|-----------------|------------------|
| login_count_7d  | 近 7 ⽇登录天数(0-7)   |
| login_count_30d | 近 30 ⽇登录天数(0-30) |
| login_streak    | 当前连续登录天数,未登录则清零  |

| 特征名                      | 含义                                  |
|--------------------------|-------------------------------------|
| avg_session_duration_7d  | 近 7 ⽇单次游戏时⻓均值(秒)                    |
| avg_session_duration_30d | 近 30 ⽇单次游戏时⻓均值(秒)                   |
| days_since_last_login    | 距上次登录天数,0 代表今天已登录                   |
| active_hours             | 玩家活跃时段列表(⼩时),如 [19,20,21,22] 表示晚间活跃 |
| weekend_active_ratio     | 周末登录天数占总登录天数的⽐例                     |

### ⾏为偏好特征(behavior):

| 特征名                    | 含义                      |
|------------------------|-------------------------|
| play_mode_diversity    | 玩法多样性指数(⾹农熵),值越⼤代表玩法越均衡 |
| pvp_ratio_7d           | 近 7 ⽇ PVP 战⽃场次占总战⽃场次的⽐例 |
| pve_ratio_7d           | 近 7 ⽇ PVE 副本场次占总战⽃场次的⽐例 |
| level_complete_rate_7d | 近 7 ⽇关卡通关率(通关次数/尝试次数)   |
| battle_count_7d        | 近 7 ⽇参与战⽃总场次            |
| battle_win_rate_7d     | 近 7 ⽇战⽃胜率               |
| avg_battle_duration_7d | 近 7 ⽇平均单场战⽃时⻓(秒)        |
| item_use_count_7d      | 近 7 ⽇使⽤道具总次数            |
| preferred_character    | 玩家最常使⽤的⻆⾊/职业 ID         |

### 付费特征(payment):

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

### 社交特征(social):

| 特征名                    | 含义                              |  |
|------------------------|---------------------------------|--|
| social_activity_score  | 社交活跃度综合评分(0-5),由聊天、组队、互动频率加权计算  |  |
| friend_count           | 好友数量                            |  |
| guild_participation_7d | 近 7 ⽇参与公会活动次数                   |  |
| chat_message_count_7d  | 近 7 ⽇发送聊天消息总数                   |  |
| team_battle_count_7d   | 近 7 ⽇参与组队战⽃次数                   |  |
| social_influence_score | 社交影响⼒评分(0-1),基于好友互动频率和被发起互动次数计算 |  |

### 参与度特征(engagement):

| 特征名                          | 含义                       |
|------------------------------|--------------------------|
| tutorial_complete            | 是否完成新⼿教程:true/false      |
| tutorial_complete_days       | 完成新⼿教程所⽤天数,值越⼩代表上⼿越快     |
| achievement_count            | 累计解锁成就数量                 |
| daily_quest_complete_rate_7d | 近 7 ⽇每⽇任务完成率             |
| event_participation_rate_30d | 近 30 ⽇活动参与率(参与活动次数/活动总数) |

## 七、模型预测结果库(model\_output)

#### 概述

模型预测结果库存储各机器学习模型对每位⽤户的预测输出,包括流失概率、付费倾向预测、⽤户聚类分群 和推荐向量。这些预测结果会被写⼊⽤户画像标签体系,同时供策略引擎实时调⽤。

数据表:model\_churn\_prediction(流失预测表)

描述: 基于 XGBoost 模型产出的⽤户流失⻛险预测,每⽇全量更新。

| 字段名              | 类型        | 含义                                                                      |
|------------------|-----------|-------------------------------------------------------------------------|
| user_id          | STRING    | 玩家 ID,主键                                                                |
| model_name       | STRING    | 模型标识,如 churn_prediction_xgb                                             |
| model_version    | STRING    | 模型版本,如 v2.3.1                                                           |
| predict_time     | TIMESTAMP | 预测执⾏时间                                                                  |
| churn_prob_7d    | FLOAT     | 7 ⽇内流失概率(0-1)                                                           |
| churn_prob_14d   | FLOAT     | 14 ⽇内流失概率(0-1)                                                          |
| churn_prob_30d   | FLOAT     | 30 ⽇内流失概率(0-1)                                                          |
| is_high_risk_7d  | BOOLEAN   | 7 ⽇内是否判定为⾼危流失⽤户(概率 > 0.5)                                               |
| is_high_risk_14d | BOOLEAN   | 14 ⽇内是否判定为⾼危流失⽤户(概率 > 0.5)                                              |
| risk_level       | STRING    | 综合流失⻛险等级:low(低)、medium(中)、high(⾼)                                       |
| top_factors      | ARRAY     | Top5 影响因⼦,每项包含特征名、特征值、重要性分数和⽅向(positive<br>代表该特征降低流失⻛险,negative 代表增加⻛险) |
| model_confidence | FLOAT     | 模型预测置信度(0-1)                                                            |

关键说明: 流失定义为玩家连续 N 天未登录游戏。流失预测模型的训练标签基于历史数据中实际发⽣的流失 事件。top\_factors 中 direction 为 negative 的特征(如 days\_since\_last\_login 值⼤)表示该特征值越⾼, 流失⻛险越⼤。

数据表:model\_payment\_prediction(付费预测表)

描述: 基于 DeepFM 模型产出的⽤户付费倾向预测,每⽇全量更新。

| 字段名           | 类型        | 含义                               |
|---------------|-----------|----------------------------------|
| user_id       | STRING    | 玩家 ID,主键                         |
| model_name    | STRING    | 模型标识,如 payment_prediction_deepfm |
| model_version | STRING    | 模型版本                             |
| predict_time  | TIMESTAMP | 预测执⾏时间                           |
| pay_prob_7d   | FLOAT     | 7 ⽇内付费概率(0-1)                    |
| pay_prob_14d  | FLOAT     | 14 ⽇内付费概率(0-1)                   |

| 字段名                     | 类型      | 含义                                                      |
|-------------------------|---------|---------------------------------------------------------|
| estimated_amount_30d    | DECIMAL | 预估 30 ⽇内充值⾦额(元)                                         |
| ltv_90d_estimate        | DECIMAL | 预估 90 ⽇⽣命周期价值(元)                                        |
| ltv_180d_estimate       | DECIMAL | 预估 180 ⽇⽣命周期价值(元)                                       |
| pay_tendency            | STRING  | 付费倾向:none(不付费)、low(低)、medium(中)、high(⾼)                 |
| price_sensitivity_level | STRING  | 价格敏感度等级:low(低敏感,愿意⾼额付费)、medium(中等)、<br>high(⾼敏感,需促销才付费) |
| top_factors             | ARRAY   | 影响付费预测的 Top5 特征及重要性分数                                   |

数据表:model\_cluster(⽤户聚类分群表)

描述: 基于 K-Means 聚类模型产出的⽤户分群结果,每周全量更新。

| 字段名                     | 类型        | 含义                            |
|-------------------------|-----------|-------------------------------|
| user_id                 | STRING    | 玩家 ID,主键                      |
| model_name              | STRING    | 模型标识,如 user_clustering_kmeans |
| model_version           | STRING    | 模型版本                          |
| predict_time            | TIMESTAMP | 预测执⾏时间                        |
| cluster_id              | INTEGER   | 聚类簇 ID(0 开始编号)                |
| cluster_name            | STRING    | 聚类簇业务名称,如"竞技型中氪玩家"、"休闲型免费玩家"  |
| cluster_description     | STRING    | 该簇⽤户群体的⾏为特征描述                 |
| avg_login_days_per_week | FLOAT     | 该簇玩家平均每周登录天数                  |
| avg_pvp_ratio           | FLOAT     | 该簇玩家 PVP 参与⽐例均值               |
| avg_monthly_spend       | DECIMAL   | 该簇玩家⽉均消费⾦额均值                  |
| cluster_size            | INTEGER   | 该簇当前玩家总⼈数                     |
| cluster_percentage      | FLOAT     | 该簇占全体玩家的⽐例                    |

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

## ⼋、⽤户画像标签库(ads\_user\_profile)

### 概述

⽤户画像标签库是整个系统对外服务的核⼼数据,由画像引擎综合⽤户基础信息、计算特征和模型预测结果 后产出。标签体系分三层:基础属性标签(事实性)、⾏为偏好标签(统计性)、预测模型标签(概率性)。

数据表:ads\_user\_profile(⽤户画像宽表)

描述: ⽤户画像标签的主宽表,每位玩家⼀条记录,每⽇全量覆盖更新。

### 基础属性标签(tags.basic):

| 标签名               | 含义                                               |
|-------------------|--------------------------------------------------|
| gender            | 性别标签:male、female、unknown                         |
| age_group         | 年龄段标签,如 25-30                                    |
| region            | 所在地区                                             |
| device_type       | 设备档次标签:Android_high_end(⾼端安卓)、iOS_mid(中端苹果)等     |
| register_days     | 注册天数                                             |
| register_channel  | 注册渠道                                             |
| game_level        | 游戏等级                                             |
| character_class   | 主要职业                                             |
| combat_power_tier | 战⼒段位:T1_top(顶尖)、T1(优秀)、T2_high(良好)、T2(普通)、T3(较低) |

| 标签名       | 含义                                                                |
|-----------|-------------------------------------------------------------------|
| rank_tier | 竞技段位:bronze/silver/gold/diamond/master                            |
| vip_level | VIP 等级数值                                                          |
| vip_tier  | VIP 档次:VIP_high(VIP6及以上)、VIP_mid(VIP3-5)、VIP_low(VIP1-2)、free(免费) |

#### ⾏为偏好标签(tags.behavior):

| 标签名                  | 含义                                                                         |
|----------------------|----------------------------------------------------------------------------|
| active_level         | 活跃度标签:high(⾼活跃)、medium(中活跃)、low(低活跃)、at_risk(流失⻛险)                         |
| active_period        | 活跃时段:morning(上午)、afternoon(下午)、evening(晚间)、night(深夜)、<br>all_day(全天)       |
| active_hours         | 主要活跃时段列表(⼩时)                                                               |
| weekend_preference   | 周末偏好:weekend_heavy(偏周末)、weekday_heavy(偏⼯作⽇)、balanced(均衡)                   |
| play_mode_preference | 玩法偏好:pvp_dominant(PVP 为主)、pve_dominant(PVE 为主)、balanced(均<br>衡)、casual(休闲) |
| pvp_preference_score | PVP 偏好分数(0-1)                                                              |
| content_preference   | 偏好内容类型列表,如 arena(竞技场)、guild_war(公会战)、dungeon_hard(困难副<br>本)                |
| skill_level          | 技术⽔平:expert(专家)、above_average(良好)、average(普通)、casual(休闲)                   |
| social_style         | 社交类型:active_socializer(⾼社交)、moderate(中度社交)、loner(独⾏侠)                      |

#### 付费标签(tags.payment):

| 标签名                | 含义                                                                                        |  |
|--------------------|-------------------------------------------------------------------------------------------|--|
| payment_segment    | 付费分层:whale(⼤R,⽉均消费 >5000 元)、dolphin(中R,⽉均 500-5000 元)、<br>minnow(⼩R,⽉均 <500 元)、free(免费⽤户) |  |
| arpu_level         | ARPU ⽔平:high、medium_high、medium、low                                                       |  |
| price_sensitivity  | 价格敏感度:high(⾼敏感)、medium、low(低敏感)                                                           |  |
| preferred_product  | 偏好商品类型列表,如 monthly_card、battle_pass、pvp_equipment                                         |  |
| payment_regularity | 付费规律性:regular(规律付费,如每⽉续费⽉卡)、occasional(偶尔付费)、first_time<br>(⾸次付费⽤户)                       |  |
| ltv_segment        | LTV 分层:T1(顶级价值)、T2(⾼价值)、T3(中等价值)、T4(低价值)                                                  |  |

#### 预测模型标签(tags.prediction):

| 标签名                   | 含义                                 |  |  |
|-----------------------|------------------------------------|--|--|
| churn_risk_7d         | 7 ⽇流失⻛险等级:high、medium、low          |  |  |
| churn_risk_30d        | 30 ⽇流失⻛险等级:high、medium、low         |  |  |
| churn_prob_30d        | 30 ⽇流失概率数值(0-1)                    |  |  |
| pay_tendency_7d       | 7 ⽇内付费倾向:high、medium、low、none      |  |  |
| estimated_ltv_90d     | 预估 90 ⽇ LTV(元)                     |  |  |
| next_likely_action    | 预测下次最可能的游戏⾏为,如 arena_battle(参与竞技场) |  |  |
| content_fatigue_score | 内容疲倦度评分(0-1),值越⾼代表玩家对当前内容的新鲜感越低    |  |  |

### 价值分层标签(tags.value):

| 标签名              | 含义                                                                                           |  |
|------------------|----------------------------------------------------------------------------------------------|--|
| rfm_segment      | RFM 价值分群,如 VIP_Develop(重要发展⽤户)、VIP_Core(重要价值⽤户)、VIP_Retain<br>(重要保持⽤户)、Common_Active(普通活跃⽤户) |  |
| rfm_r_score      | RFM 中 R(最近⼀次付费距今时间)评分(1-5分,5分最好)                                                             |  |
| rfm_f_score      | RFM 中 F(付费频率)评分(1-5分)                                                                        |  |
| rfm_m_score      | RFM 中 M(付费⾦额)评分(1-5分)                                                                        |  |
| lifecycle_stage  | ⽣命周期阶段:new_user(新⽤户)、growing(成⻓期)、mature_active(成熟活跃)、<br>declining(衰退期)、churned(流失)         |  |
| lifecycle_detail | ⽣命周期细分,如 engaged_payer(活跃付费⽤户)                                                               |  |
| user_value_tier  | 综合价值等级:S1(最⾼价值)、S2、A1、A2、B1、B2                                                               |  |

### 画像摘要(summary):

| 字段名     | 含义                                          |
|---------|---------------------------------------------|
| summary | ⽤户画像的⾃然语⾔摘要,描述⽤户的核⼼特征、⾏为偏好和当前状态,适合直接展示给运营⼈员 |

## 九、推荐结果库(ads\_recommend)

推荐结果库记录推荐系统对每位⽤户在不同场景下的推荐输出,包括召回来源、排序分数和推荐理由,是推 荐效果分析的核⼼数据源。

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

## ⼗、策略与A/B实验库(dwd\_strategy)

#### 概述

策略库记录运营策略的配置信息和匹配结果,A/B 实验库记录实验⽅案和统计分析结果,两者共同⽀撑运营 效果的科学评估。

数据表:dwd\_strategy\_config(策略配置表)

描述: 运营策略的完整配置,由 Agent 或运营⼈员创建。

| 字段名                        | 类型        | 含义                                                                                 |
|----------------------------|-----------|------------------------------------------------------------------------------------|
| strategy_id                | STRING    | 策略唯⼀标识,主键                                                                          |
| name                       | STRING    | 策略名称                                                                               |
| strategy_type              | STRING    | 策略类型:churn_save(流失挽留)、payment_convert(付费<br>转化)、active_boost(活跃提升)、new_guide(新⼿引导) |
| status                     | STRING    | 策略状态:active(⽣效中)、paused(暂停)、ended(已结<br>束)                                         |
| priority                   | INTEGER   | 策略优先级(数值越⼤越优先,当⽤户同时命中多条策略时取最<br>⾼优先级执⾏)                                            |
| daily_quota                | INTEGER   | 每⽇最⼤触达⽤户数                                                                          |
| start_time                 | TIMESTAMP | 策略⽣效开始时间                                                                           |
| end_time                   | TIMESTAMP | 策略失效时间                                                                             |
| target_segment             | JSON      | ⽬标⽤户群体的过滤条件,⽀持组合条件                                                                 |
| conditions                 | JSON      | 策略触发的实时条件(基于特征值)                                                                   |
| actions                    | ARRAY     | 执⾏动作列表,每个动作包含渠道、触发时机、内容和频控规则                                                       |
| action_channel             | STRING    | 触达渠道:game_popup(游戏弹窗)、push_notification(推送<br>通知)、game_mail(游戏邮件)、banner(⾸⻚横幅)     |
| frequency_per_user_per_day | INTEGER   | 每⽤户每⽇最多触达次数(频控)                                                                    |
| frequency_per_user_total   | INTEGER   | 每⽤户累计最多触达次数(频控)                                                                    |
| ab_experiment_id           | STRING    | 关联的 AB 实验 ID                                                                       |
| created_by                 | STRING    | 创建者:agent(Agent ⾃动创建)或具体运营⼈员 ID                                                    |

数据表:dwd\_ab\_experiment(AB实验表)

描述: AB 实验的配置和统计结果表。

| 字段名           | 类型     | 含义                               |
|---------------|--------|----------------------------------|
| experiment_id | STRING | 实验唯⼀标识,主键                        |
| name          | STRING | 实验名称                             |
| description   | STRING | 实验⽬的描述                           |
| layer         | STRING | 实验层,⽤于保证多实验互斥性(同⼀⽤户在同⼀层只能进⼊⼀个实验) |

| 字段名                | 类型        | 含义                                         |
|--------------------|-----------|--------------------------------------------|
| status             | STRING    | 实验状态:draft(草稿)、running(进⾏中)、completed(已完成) |
| start_time         | TIMESTAMP | 实验开始时间                                     |
| end_time           | TIMESTAMP | 实验结束时间                                     |
| variant_name       | STRING    | 分组名称:control(对照组)、variant_A/B/C            |
| traffic_ratio      | FLOAT     | 该分组流量⽐例(所有分组之和为 1.0)                       |
| is_control         | BOOLEAN   | 是否为对照组                                     |
| variant_config     | JSON      | 该分组的实验配置                                   |
| metrics            | ARRAY     | 实验关注的核⼼指标列表                                |
| significance_level | FLOAT     | 统计显著性⽔平(通常设为 0.05,即 5%)                    |
| min_sample_size    | INTEGER   | 得出可信结论所需的最⼩样本量                             |
| sample_size        | INTEGER   | 该分组当前样本量                                   |
| day7_retention     | FLOAT     | 该分组 7 ⽇留存率统计值                              |
| arpu_14d           | FLOAT     | 该分组 14 ⽇ ARPU 统计值                          |
| p_value_vs_control | FLOAT     | 与对照组⽐较的 p 值                                |
| is_significant     | BOOLEAN   | 是否达到统计显著性                                  |
| uplift             | FLOAT     | 相对对照组的提升幅度                                 |
| recommendation     | STRING    | 基于统计结果的推荐决策                                |

# ⼗⼀、监控指标库(ads\_monitor)

#### 概述

监控指标库记录游戏业务⼤盘数据和各运营策略的效果监控数据,⽀持实时告警和效果归因分析。

数据表:ads\_daily\_metrics(业务⼤盘⽇报表)

描述: 游戏核⼼业务指标的每⽇快照,每⽇凌晨 0 点产出前⼀⽇数据。

| 字段名                      | 类型      | 含义                                            |
|--------------------------|---------|-----------------------------------------------|
| game_id                  | STRING  | 游戏标识,主键之⼀                                     |
| date                     | DATE    | 统计⽇期,主键之⼀                                     |
| dau                      | INTEGER | ⽇活跃⽤户数(当⽇有登录⾏为的去重⽤户数)                         |
| dau_wow_change           | FLOAT   | DAU 周同⽐变化率(正为增⻓,负为下降)                         |
| new_users                | INTEGER | 新增注册⽤户数                                       |
| avg_session_duration     | FLOAT   | 全体⽤户当⽇平均单次游戏时⻓(秒)                             |
| avg_sessions_per_user    | FLOAT   | 活跃⽤户当⽇平均游戏次数                                  |
| dau_mau_ratio            | FLOAT   | DAU/MAU ⽐值,反映⽤户粘性                             |
| day1_retention           | FLOAT   | 新⽤户次⽇留存率                                      |
| day7_retention           | FLOAT   | 新⽤户 7 ⽇留存率                                    |
| day30_retention          | FLOAT   | 新⽤户 30 ⽇留存率                                   |
| pay_rate                 | FLOAT   | 当⽇付费⽤户占 DAU 的⽐例                               |
| arpu                     | DECIMAL | 当⽇全⽤户⼈均收⼊(元)                                  |
| arppu                    | DECIMAL | 当⽇付费⽤户⼈均收⼊(元)                                 |
| total_revenue            | DECIMAL | 当⽇总营收(元)                                      |
| revenue_wow_change       | FLOAT   | 营收周同⽐变化率                                      |
| arena_participation_rate | FLOAT   | 竞技场参与率(参与竞技场的 DAU ⽐例)                         |
| guild_activity_rate      | FLOAT   | 公会活跃率(参与公会活动的 DAU ⽐例)                         |
| crash_rate               | FLOAT   | 崩溃率(崩溃次数/会话次数)                                |
| alerts                   | ARRAY   | 指标异常告警列表,每项包含告警 ID、严重程度、指标名、当前值、阈<br>值和建议处理措施 |

数据表:ads\_strategy\_monitor(策略效果监控表)

描述: 运营策略的触达漏⽃和效果归因数据,每⽇更新。

| 字段名          | 类型     | 含义         |
|--------------|--------|------------|
| strategy_id  | STRING | 策略 ID,主键之⼀ |
| monitor_date | DATE   | 监控⽇期,主键之⼀  |

| 字段名                 | 类型      | 含义                              |
|---------------------|---------|---------------------------------|
| exposed             | INTEGER | 策略触达(曝光)⽤户数                     |
| clicked             | INTEGER | 点击触达内容的⽤户数                      |
| engaged             | INTEGER | 深度参与(进⾏⽬标⾏为)的⽤户数                |
| retained_7d         | INTEGER | 7 ⽇内留存的⽤户数                      |
| paid_7d             | INTEGER | 7 ⽇内产⽣付费的⽤户数                    |
| click_rate          | FLOAT   | 点击率(clicked/exposed)            |
| engage_rate         | FLOAT   | 参与率(engaged/exposed)            |
| retain_rate         | FLOAT   | 留存率(retained_7d/exposed)        |
| pay_rate            | FLOAT   | 付费率(paid_7d/exposed)            |
| retention_uplift    | FLOAT   | 相对对照组的留存提升幅度                    |
| revenue_uplift      | FLOAT   | 相对对照组的收⼊提升幅度(元/⽤户)              |
| is_significant      | BOOLEAN | 效果是否显著                          |
| cost                | DECIMAL | 策略执⾏成本(礼包/奖励物价值,元)              |
| incremental_revenue | DECIMAL | 因策略带来的增量收⼊(元)                   |
| roi_ratio           | FLOAT   | 投资回报率(incremental_revenue/cost) |

# ⼗⼆、Agent 对话历史库(dwd\_agent\_session)

### 概述

Agent 对话历史库记录所有 Agent 与运营⼈员之间的交互会话,包括完整的多轮对话内容、⼯具调⽤记录和 Agent 执⾏结果,⽤于 Agent 能⼒审计和体验优化。

数据表:dwd\_agent\_session(Agent会话表)

描述: Agent 会话的元数据和完整消息记录。

| 字段名        | 类型     | 含义        |
|------------|--------|-----------|
| session_id | STRING | 会话唯⼀标识,主键 |
| user_id    | STRING | 操作⼈员 ID   |

| 字段名               | 类型        | 含义                                                         |
|-------------------|-----------|------------------------------------------------------------|
| user_role         | STRING    | 操作⼈员⻆⾊:game_operator(运营)、data_analyst(数据分析)、<br>admin(管理员) |
| started_at        | TIMESTAMP | 会话开始时间                                                     |
| ended_at          | TIMESTAMP | 会话结束时间                                                     |
| message_role      | STRING    | 消息⻆⾊:user(⽤户发⾔)、assistant(Agent 回复)                        |
| message_content   | STRING    | 消息⽂本内容                                                     |
| message_timestamp | TIMESTAMP | 消息发送时间                                                     |
| tool_name         | STRING    | 调⽤的⼯具名称,如 query_metrics、create_strategy                    |
| tool_input        | JSON      | ⼯具调⽤的输⼊参数                                                  |
| tool_output       | JSON      | ⼯具调⽤的返回结果                                                  |

#### 系统内置 Agent ⼯具清单:

| ⼯具名                   | 功能描述                    |
|-----------------------|-------------------------|
| query_metrics         | 查询业务指标数据,⽀持⾃然语⾔转 SQL    |
| query_user_profile    | 查询单⽤户或⽤户群体的画像标签         |
| query_strategy        | 查询策略配置和效果数据             |
| create_strategy       | 创建新的运营策略                |
| update_strategy       | 修改已有策略的配置               |
| trigger_ab_experiment | 创建并启动 AB 实验             |
| get_ab_results        | 获取实验统计结果和显著性检验          |
| predict_churn         | 对指定⽤户群体执⾏即时流失⻛险预测       |
| recommend_items       | 为指定⽤户获取实时推荐结果           |
| export_report         | 将分析结果导出为 Excel 或 PDF 报告 |

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