---
chunk_id: chunk_006
domain: ods_event
domain_name: 原始事件数据库
table: ods_event_log
table_name: 游戏行为事件总表
section: level_complete
section_type: event_properties
level: sub_table
char_count: 901
source_file: database-intro-for-rag.md
---

[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表] [关卡完成事件]

关卡完成事件(level\_complete)properties 字段:

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

###