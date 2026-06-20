---
chunk_id: chunk_003
domain: ods_event
domain_name: 原始事件数据库
table: ods_event_log
table_name: 游戏行为事件总表
section: battle
section_type: event_properties
level: sub_table
char_count: 1251
source_file: database-intro-for-rag.md
---

[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表] [战斗事件]

战⽃事件(battle)properties 字段:

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

###