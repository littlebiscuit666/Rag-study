---
chunk_id: chunk_023
domain: feature_store
domain_name: 特征数据库
table: feature_user_online
table_name: 用户在线特征表
section: social
section_type: feature_group
level: sub_table
char_count: 600
source_file: database-intro-for-rag.md
---

[数据域: 特征数据库(feature_store)] [表: feature_user_online 用户在线特征表] [社交特征]

社交特征(social):

| 特征名                    | 含义                              |  |
|------------------------|---------------------------------|--|
| social_activity_score  | 社交活跃度综合评分(0-5),由聊天、组队、互动频率加权计算  |  |
| friend_count           | 好友数量                            |  |
| guild_participation_7d | 近 7 ⽇参与公会活动次数                   |  |
| chat_message_count_7d  | 近 7 ⽇发送聊天消息总数                   |  |
| team_battle_count_7d   | 近 7 ⽇参与组队战⽃次数                   |  |
| social_influence_score | 社交影响⼒评分(0-1),基于好友互动频率和被发起互动次数计算 |  |

###