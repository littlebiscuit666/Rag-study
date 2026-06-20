---
chunk_id: chunk_040
domain: dwd_agent_session
domain_name: Agent对话历史库
table: dwd_agent_session
table_name: Agent会话表
section: null
section_type: null
level: table
char_count: 1968
source_file: database-intro-for-rag.md
---

[数据域: Agent对话历史库(dwd_agent_session)] [表: dwd_agent_session Agent会话表]

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