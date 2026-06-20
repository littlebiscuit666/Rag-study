---
chunk_id: chunk_032
domain: ads_user_profile
domain_name: 用户画像标签库
table: ads_user_profile
table_name: 用户画像宽表
section: payment
section_type: tag_group
level: sub_table
char_count: 1040
source_file: database-intro-for-rag.md
---

[数据域: 用户画像标签库(ads_user_profile)] [表: ads_user_profile 用户画像宽表] [付费标签]

付费标签(tags.payment):

| 标签名                | 含义                                                                                        |  |
|--------------------|-------------------------------------------------------------------------------------------|--|
| payment_segment    | 付费分层:whale(⼤R,⽉均消费 >5000 元)、dolphin(中R,⽉均 500-5000 元)、<br>minnow(⼩R,⽉均 <500 元)、free(免费⽤户) |  |
| arpu_level         | ARPU ⽔平:high、medium_high、medium、low                                                       |  |
| price_sensitivity  | 价格敏感度:high(⾼敏感)、medium、low(低敏感)                                                           |  |
| preferred_product  | 偏好商品类型列表,如 monthly_card、battle_pass、pvp_equipment                                         |  |
| payment_regularity | 付费规律性:regular(规律付费,如每⽉续费⽉卡)、occasional(偶尔付费)、first_time<br>(⾸次付费⽤户)                       |  |
| ltv_segment        | LTV 分层:T1(顶级价值)、T2(⾼价值)、T3(中等价值)、T4(低价值)                                                  |  |

####