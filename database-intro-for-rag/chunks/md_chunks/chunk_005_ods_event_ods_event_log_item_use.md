---
chunk_id: chunk_005
domain: ods_event
domain_name: 原始事件数据库
table: ods_event_log
table_name: 游戏行为事件总表
section: item_use
section_type: event_properties
level: sub_table
char_count: 598
source_file: database-intro-for-rag.md
---

[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表] [道具使用事件]

道具使⽤事件(item\_use)properties 字段:

| 字段名                | 含义                                   |
|--------------------|--------------------------------------|
| item_id            | 使⽤的道具 ID                             |
| item_category      | 道具类别,如 consumable(消耗品)、equipment(装备) |
| quantity           | 使⽤数量                                 |
| source             | 道具来源,如 inventory(背包)、shop(商店)        |
| exp_gained         | 使⽤后获得的经验值(仅适⽤于经验道具)                  |
| remaining_quantity | 使⽤后背包剩余数量                            |

####