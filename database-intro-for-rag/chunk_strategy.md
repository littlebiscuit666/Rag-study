# Chunk 分块策略说明

本文档说明 `database-intro-for-rag.md` 的 chunk 分块策略，用于 BM25 + 向量混合召回的 RAG 系统。

## 一、分块原则

1. **语义完整性优先**：每个 chunk 对应一个完整的语义单元（一张表 / 一组子结构），不把同一概念拆到两个 chunk 里。
2. **粒度适中**：避免 chunk 过大（语义稀释）或过小（上下文丢失）。目标单 chunk 字数在 200~1500 字之间。
3. **表级为主、子表级补充**：数据表是 RAG 查询的基本单位，以此为核心分块；结构复杂的大表再按子结构细分。
4. **保留层级上下文**：每个 chunk 的开头附上所属数据域、表名等路径信息，帮助 embedding 模型理解上下文。
5. **便于 BM25 召回**：chunk 内保留完整的字段名、表名等关键词，不做摘要压缩，确保关键词匹配精度。

## 二、文档结构与分块映射

源文档共 12 个数据域 + 关系总览 + 附录，分块后共 **30 个 chunk**。

### 2.1 表级 chunk（核心）

每张数据表（含字段定义表）作为一个独立 chunk。共 20+ 个表级 chunk。

| 数据域 | 表名 | chunk 粒度 |
|--------|------|-----------|
| 一、ods_event | ods_event_log（主表字段） | 表级 |
| 一、ods_event | ods_event_log（login 事件 properties） | 子表级 |
| 一、ods_event | ods_event_log（battle 事件 properties） | 子表级 |
| 一、ods_event | ods_event_log（purchase 事件 properties） | 子表级 |
| 一、ods_event | ods_event_log（item_use 事件 properties） | 子表级 |
| 一、ods_event | ods_event_log（level_complete 事件 properties） | 子表级 |
| 一、ods_event | ods_event_log（logout 事件 properties） | 子表级 |
| 一、ods_event | ods_event_log（social_interact 事件 properties） | 子表级 |
| 二、dim_user | dim_user_info | 表级 |
| 三、dim_content | dim_item | 表级 |
| 三、dim_content | dim_activity | 表级 |
| 三、dim_content | dim_level | 表级 |
| 四、dwd_trade | dwd_trade_order | 表级 |
| 四、dwd_trade | dwd_trade_consume | 表级 |
| 五、dwd_social | dwd_social_relation | 表级 |
| 五、dwd_social | dim_guild | 表级 |
| 五、dwd_social | dwd_chat_log | 表级 |
| 六、feature_store | feature_user_online（basic 特征） | 子表级 |
| 六、feature_store | feature_user_online（activity 特征） | 子表级 |
| 六、feature_store | feature_user_online（behavior 特征） | 子表级 |
| 六、feature_store | feature_user_online（payment 特征） | 子表级 |
| 六、feature_store | feature_user_online（social 特征） | 子表级 |
| 六、feature_store | feature_user_online（engagement 特征） | 子表级 |
| 七、model_output | model_churn_prediction | 表级 |
| 七、model_output | model_payment_prediction | 表级 |
| 七、model_output | model_cluster | 表级 |
| 七、model_output | model_recommend_vector | 表级 |
| 八、ads_user_profile | ads_user_profile（basic 标签） | 子表级 |
| 八、ads_user_profile | ads_user_profile（behavior 标签） | 子表级 |
| 八、ads_user_profile | ads_user_profile（payment 标签） | 子表级 |
| 八、ads_user_profile | ads_user_profile（prediction 标签） | 子表级 |
| 八、ads_user_profile | ads_user_profile（value 标签 + summary） | 子表级 |
| 九、ads_recommend | ads_recommend_log | 表级 |
| 十、dwd_strategy | dwd_strategy_config | 表级 |
| 十、dwd_strategy | dwd_ab_experiment | 表级 |
| 十一、ads_monitor | ads_daily_metrics | 表级 |
| 十一、ads_monitor | ads_strategy_monitor | 表级 |
| 十二、dwd_agent_session | dwd_agent_session + 工具清单 | 表级 |

### 2.2 全局 chunk

| 名称 | 说明 |
|------|------|
| 数据域关系总览 | 整体数据流向图，回答"架构"、"数据流转"类问题 |
| 附录·常用分析场景 | 分析场景 → 数据表映射，回答"做 XX 分析用哪些表" |

## 三、Chunk 元数据规范

每个 chunk 附带以下 metadata 字段，用于 BM25 和向量召回时的 metadata 过滤：

```json
{
  "chunk_id": "chunk_001",
  "domain": "ods_event",          // 所属数据域（英文标识）
  "domain_name": "原始事件数据库",   // 所属数据域（中文名称）
  "table": "ods_event_log",       // 所属表名（无子表时为 null）
  "table_name": "游戏行为事件总表",  // 表中文名
  "section": "login",             // 子结构名（事件类型/特征组/标签组，无子结构时为 null）
  "section_type": "event_properties", // 子结构类型: event_properties / feature_group / tag_group / null
  "level": "sub_table",           // chunk 粒度: domain / table / sub_table / global
  "char_count": 520,              // 字符数
  "source_file": "database-intro-for-rag.md"
}
```

### section_type 枚举

- `event_properties` — 事件属性组（ods_event 下的 7 种事件）
- `feature_group` — 特征组（feature_store 下的 6 组特征）
- `tag_group` — 标签组（user_profile 下的标签组）
- `null` — 整张表，无子结构拆分

### level 枚举

- `domain` — 数据域级概述
- `table` — 整张表
- `sub_table` — 表的子结构
- `global` — 全局内容（关系图、附录）

## 四、Chunk 内容格式

每个 chunk 的文本内容格式如下（供 embedding 和 BM25 使用）：

```
[数据域: 原始事件数据库(ods_event)] [表: ods_event_log 游戏行为事件总表] [事件: login 登录]

### 登录事件(login)properties 字段:

| 字段名               | 含义                                      |
|-------------------|-----------------------------------------|
| ip                | 玩家登录 IP 地址(已脱敏)                         |
| client_os         | 操作系统版本                                  |
...
```

**说明：**
- 开头的 `[数据域: ...] [表: ...] [xxx: ...]` 是结构化上下文前缀，帮助 embedding 模型定位 chunk 所属层级。
- 正文保留原始 Markdown 格式（表格、标题），BM25 可直接命中字段名和表名。
- 不做 chunk 之间的 overlap，因为每个 chunk 语义独立完整。

## 五、输出文件

分块结果输出为 JSONL 文件，每行一个 chunk 对象：

```
Rag-study/database-intro-for-rag/chunks/database_chunks.jsonl
```

同时输出一个 chunks/ 目录下的单个 .md 文件，便于人工检视。
