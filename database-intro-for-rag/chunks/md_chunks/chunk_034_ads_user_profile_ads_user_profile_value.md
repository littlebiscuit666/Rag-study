---
chunk_id: chunk_034
domain: ads_user_profile
domain_name: 用户画像标签库
table: ads_user_profile
table_name: 用户画像宽表
section: value
section_type: tag_group
level: sub_table
char_count: 1363
source_file: database-intro-for-rag.md
---

[数据域: 用户画像标签库(ads_user_profile)] [表: ads_user_profile 用户画像宽表] [价值分层标签+画像摘要]

价值分层标签(tags.value):

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