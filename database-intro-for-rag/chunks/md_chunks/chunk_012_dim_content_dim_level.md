---
chunk_id: chunk_012
domain: dim_content
domain_name: 物料/内容数据库
table: dim_level
table_name: 关卡表
section: null
section_type: null
level: table
char_count: 1549
source_file: database-intro-for-rag.md
---

[数据域: 物料/内容数据库(dim_content)] [表: dim_level 关卡表]

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