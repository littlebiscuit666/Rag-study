#!/usr/bin/env python3
"""
将 database-intro-for-rag.md 按语义分块，生成 JSONL 和单独的 md 文件。

分块策略详见 chunk_strategy.md。
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent
SRC_FILE = BASE_DIR / "database-intro-for-rag.md"
OUTPUT_DIR = BASE_DIR / "chunks"
JSONL_FILE = OUTPUT_DIR / "database_chunks.jsonl"

# 12 个数据域的 (英文标识, 中文名称)
DOMAIN_LIST = [
    ("ods_event", "原始事件数据库"),
    ("dim_user", "用户基础信息库"),
    ("dim_content", "物料/内容数据库"),
    ("dwd_trade", "交易数据库"),
    ("dwd_social", "社交数据库"),
    ("feature_store", "特征数据库"),
    ("model_output", "模型预测结果库"),
    ("ads_user_profile", "用户画像标签库"),
    ("ads_recommend", "推荐结果库"),
    ("dwd_strategy", "策略与A/B实验库"),
    ("ads_monitor", "监控指标库"),
    ("dwd_agent_session", "Agent对话历史库"),
]

# 数据表 → 中文名 映射
TABLE_NAME_MAP = {
    "ods_event_log": "游戏行为事件总表",
    "dim_user_info": "用户基础维度表",
    "dim_item": "道具表",
    "dim_activity": "活动表",
    "dim_level": "关卡表",
    "dwd_trade_order": "充值订单表",
    "dwd_trade_consume": "游戏内消费表",
    "dwd_social_relation": "好友关系表",
    "dim_guild": "公会信息表",
    "dwd_chat_log": "聊天记录表",
    "feature_user_online": "用户在线特征表",
    "model_churn_prediction": "流失预测表",
    "model_payment_prediction": "付费预测表",
    "model_cluster": "用户聚类分群表",
    "model_recommend_vector": "推荐向量表",
    "ads_user_profile": "用户画像宽表",
    "ads_recommend_log": "推荐日志表",
    "dwd_strategy_config": "策略配置表",
    "dwd_ab_experiment": "AB实验表",
    "ads_daily_metrics": "业务大盘日报表",
    "ads_strategy_monitor": "策略效果监控表",
    "dwd_agent_session": "Agent会话表",
}

# 需要按子结构拆分的表及子结构识别规则
# 格式: table_name -> {"section_type": xxx, "sections": [(key, cn_name, start_marker), ...]}
SUB_TABLE_RULES = {
    "ods_event_log": {
        "section_type": "event_properties",
        "sections": [
            ("login", "登录事件", "登录事件(login)properties"),
            ("battle", "战斗事件", "战⽃事件(battle)properties"),
            ("purchase", "充值事件", "充值事件(purchase)properties"),
            ("item_use", "道具使用事件", "道具使⽤事件(item_use)properties"),
            ("level_complete", "关卡完成事件", "关卡完成事件(level_complete)properties"),
            ("logout", "退出事件", "退出事件(logout)properties"),
            ("social_interact", "社交互动事件", "社交互动事件(social_interact)properties"),
        ],
    },
    "feature_user_online": {
        "section_type": "feature_group",
        "sections": [
            ("basic", "基础属性特征", "基础属性特征(basic)"),
            ("activity", "活跃度特征", "活跃度特征(activity)"),
            ("behavior", "行为偏好特征", "⾏为偏好特征(behavior)"),
            ("payment", "付费特征", "付费特征(payment)"),
            ("social", "社交特征", "社交特征(social)"),
            ("engagement", "参与度特征", "参与度特征(engagement)"),
        ],
    },
    "ads_user_profile": {
        "section_type": "tag_group",
        "sections": [
            ("basic", "基础属性标签", "基础属性标签(tags.basic)"),
            ("behavior", "行为偏好标签", "⾏为偏好标签(tags.behavior)"),
            ("payment", "付费标签", "付费标签(tags.payment)"),
            ("prediction", "预测模型标签", "预测模型标签(tags.prediction)"),
            ("value", "价值分层标签+画像摘要", "价值分层标签(tags.value)"),
        ],
    },
}


def read_source():
    with open(SRC_FILE, "r", encoding="utf-8") as f:
        return f.read()


def find_domain_boundaries(text):
    """
    通过匹配每个数据域的英文名（括号内的标识）找到各数据域的起止位置。
    返回: list of (domain_en, domain_cn, start_idx, end_idx)
    以及 global_sections: list of (name, start_idx, end_idx)
    """
    # 找到每个数据域标题的起始位置
    # 标题格式：#{1,2} 一二...、中文名(英文标识)
    # 注意：md 源文件中括号内的下划线可能被转义为 \_
    domain_positions = []
    for domain_en, domain_cn in DOMAIN_LIST:
        # 将 domain_en 中的 _ 替换为 [_\\]+ 以同时匹配 _ 和 \_
        fuzzy_en = domain_en.replace("_", r"\\?_")
        pattern = re.compile(
            r"^#{1,2}\s*.+?\(" + fuzzy_en + r"\).*$",
            re.MULTILINE,
        )
        m = pattern.search(text)
        if m:
            domain_positions.append((domain_en, domain_cn, m.start()))

    # 按在文档中出现的顺序排序
    domain_positions.sort(key=lambda x: x[2])

    domains = []
    for i, (domain_en, domain_cn, start) in enumerate(domain_positions):
        end = domain_positions[i + 1][2] if i + 1 < len(domain_positions) else len(text)
        domains.append((domain_en, domain_cn, start, end))

    # 全局 section：数据域关系总览、附录
    # 它们是 ## 级标题，可能出现在最后一个数据域的范围内
    # 在全文中查找，然后截断最后一个数据域的结束位置
    global_sections = []

    # 数据域关系总览
    rel_m = re.search(r"^##\s*数据域关系总览", text, re.MULTILINE)
    if rel_m:
        g_start = rel_m.start()
        after = text[rel_m.end():]
        next_m = re.search(r"^##\s", after, re.MULTILINE)
        g_end = rel_m.end() + (next_m.start() if next_m else len(after))
        global_sections.append(("数据域关系总览", g_start, g_end))

    # 附录
    app_m = re.search(r"^##\s*附录", text, re.MULTILINE)
    if app_m:
        g_start = app_m.start()
        g_end = len(text)
        global_sections.append(("附录·常用分析场景", g_start, g_end))

    # 如果全局 section 在最后一个数据域内部，则截断最后一个数据域
    if domains and global_sections:
        first_global_start = min(g[1] for g in global_sections)
        last_domain_end = domains[-1][3]
        if last_domain_end > first_global_start:
            d_en, d_cn, d_s, _ = domains[-1]
            domains[-1] = (d_en, d_cn, d_s, first_global_start)

    return domains, global_sections


def find_tables_in_domain(domain_text):
    """
    在一个数据域内，找到所有数据表的标题和位置。
    匹配 "数据表: table_name" 或 "数据表: table_name(中文名)" 格式。
    注意：md 源文件中下划线可能被转义为 \\_。
    返回: list of (table_name, start_offset, end_offset)
    offset 是相对于 domain_text 的。
    """
    pattern = re.compile(
        r'^(?:#{1,2}\s*)?数据表\s*[:：]\s*([a-zA-Z][a-zA-Z0-9\\_]*).*$',
        re.MULTILINE,
    )
    matches = list(pattern.finditer(domain_text))

    tables = []
    for i, m in enumerate(matches):
        # 去掉转义符 \_ → _
        table_name = m.group(1).strip().replace("\\_", "_").replace("\\", "")
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(domain_text)
        tables.append((table_name, start, end))

    return tables


def split_sub_sections(table_text, section_rules):
    """
    将一张有子结构的表拆分为：主表 chunk + 各子结构 chunk。
    section_rules: [(key, cn_name, start_marker), ...]
    返回: [(section_key, section_cn, content), ...]
    第一个为主表（section_key = "main"）。
    """
    # 找每个子结构的起始位置
    # md 源文件中下划线可能被转义为 \_，所以 marker 中的 _ 需要同时匹配 _ 和 \_
    section_positions = []
    for key, cn_name, marker in section_rules:
        # 用 _ 作为分割点，各段 re.escape 后用 \\?_ 连接
        parts = marker.split("_")
        escaped_parts = [re.escape(p) for p in parts]
        fuzzy_marker = r"\\?_".join(escaped_parts)
        m = re.search(fuzzy_marker, table_text)
        if m:
            section_positions.append((key, cn_name, m.start()))

    # 按起始位置排序
    section_positions.sort(key=lambda x: x[2])

    chunks = []

    # 主表部分：表标题 → 第一个子结构之前
    if section_positions:
        first_sub_start = section_positions[0][2]
        main_content = table_text[:first_sub_start].strip()
    else:
        main_content = table_text.strip()

    chunks.append(("main", "主表字段", main_content))

    # 各子结构
    for i, (key, cn_name, pos) in enumerate(section_positions):
        end_pos = section_positions[i + 1][2] if i + 1 < len(section_positions) else len(table_text)
        sub_content = table_text[pos:end_pos].strip()
        chunks.append((key, cn_name, sub_content))

    return chunks


def build_chunk_content(domain_en, domain_cn, table_name, table_cn, section, section_cn, raw_content):
    """
    构建 chunk 的文本内容，加上结构化前缀。
    """
    prefix_parts = [f"[数据域: {domain_cn}({domain_en})]"]
    if table_name:
        prefix_parts.append(f"[表: {table_name} {table_cn}]")
    if section and section != "main":
        prefix_parts.append(f"[{section_cn}]")

    prefix = " ".join(prefix_parts)
    return f"{prefix}\n\n{raw_content.strip()}"


def main():
    text = read_source()
    domains, global_sections = find_domain_boundaries(text)

    print(f"识别到 {len(domains)} 个数据域:")
    for d in domains:
        print(f"  - {d[0]} ({d[1]})")
    print(f"全局 section: {[g[0] for g in global_sections]}")
    print()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chunks = []
    chunk_id = 0

    # ---- 处理每个数据域 ----
    for domain_en, domain_cn, d_start, d_end in domains:
        domain_text = text[d_start:d_end]
        tables = find_tables_in_domain(domain_text)

        if not tables:
            # 没有数据表 → 整个域作为一个 chunk
            chunk_id += 1
            content = f"[数据域: {domain_cn}({domain_en})]\n\n{domain_text.strip()}"
            chunks.append({
                "chunk_id": f"chunk_{chunk_id:03d}",
                "domain": domain_en,
                "domain_name": domain_cn,
                "table": None,
                "table_name": None,
                "section": None,
                "section_type": None,
                "level": "domain",
                "char_count": len(content),
                "source_file": SRC_FILE.name,
                "content": content,
            })
            continue

        for table_name, t_start, t_end in tables:
            table_cn = TABLE_NAME_MAP.get(table_name, table_name)
            table_text = domain_text[t_start:t_end]

            # 判断是否需要子表拆分
            if table_name in SUB_TABLE_RULES:
                rules = SUB_TABLE_RULES[table_name]
                section_type = rules["section_type"]
                sub_chunks = split_sub_sections(table_text, rules["sections"])

                for sec_key, sec_cn, sec_content in sub_chunks:
                    if not sec_content or len(sec_content) < 10:
                        continue
                    chunk_id += 1
                    if sec_key == "main":
                        content = build_chunk_content(
                            domain_en, domain_cn, table_name, table_cn,
                            None, None, sec_content
                        )
                        chunks.append({
                            "chunk_id": f"chunk_{chunk_id:03d}",
                            "domain": domain_en,
                            "domain_name": domain_cn,
                            "table": table_name,
                            "table_name": table_cn,
                            "section": None,
                            "section_type": None,
                            "level": "table",
                            "char_count": len(content),
                            "source_file": SRC_FILE.name,
                            "content": content,
                        })
                    else:
                        content = build_chunk_content(
                            domain_en, domain_cn, table_name, table_cn,
                            sec_key, sec_cn, sec_content
                        )
                        chunks.append({
                            "chunk_id": f"chunk_{chunk_id:03d}",
                            "domain": domain_en,
                            "domain_name": domain_cn,
                            "table": table_name,
                            "table_name": table_cn,
                            "section": sec_key,
                            "section_type": section_type,
                            "level": "sub_table",
                            "char_count": len(content),
                            "source_file": SRC_FILE.name,
                            "content": content,
                        })
            else:
                # 整表作为一个 chunk
                if not table_text.strip() or len(table_text.strip()) < 10:
                    continue
                chunk_id += 1
                content = build_chunk_content(
                    domain_en, domain_cn, table_name, table_cn,
                    None, None, table_text
                )
                chunks.append({
                    "chunk_id": f"chunk_{chunk_id:03d}",
                    "domain": domain_en,
                    "domain_name": domain_cn,
                    "table": table_name,
                    "table_name": table_cn,
                    "section": None,
                    "section_type": None,
                    "level": "table",
                    "char_count": len(content),
                    "source_file": SRC_FILE.name,
                    "content": content,
                })

    # ---- 处理全局 section ----
    for name, g_start, g_end in global_sections:
        global_content = text[g_start:g_end].strip()
        if not global_content:
            continue
        chunk_id += 1
        content = f"[全局: {name}]\n\n{global_content}"
        chunks.append({
            "chunk_id": f"chunk_{chunk_id:03d}",
            "domain": "global",
            "domain_name": "全局",
            "table": None,
            "table_name": None,
            "section": name,
            "section_type": None,
            "level": "global",
            "char_count": len(content),
            "source_file": SRC_FILE.name,
            "content": content,
        })

    # ---- 写出 JSONL ----
    with open(JSONL_FILE, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    # ---- 写出单独的 md 文件（便于检视） ----
    md_dir = OUTPUT_DIR / "md_chunks"
    md_dir.mkdir(parents=True, exist_ok=True)

    for chunk in chunks:
        filename = f"{chunk['chunk_id']}_{chunk['domain']}"
        if chunk["table"]:
            filename += f"_{chunk['table']}"
        if chunk["section"]:
            safe_sec = re.sub(r'[^\w\-.]', '_', chunk["section"])
            filename += f"_{safe_sec}"
        filename += ".md"

        with open(md_dir / filename, "w", encoding="utf-8") as f:
            f.write("---\n")
            for key in ["chunk_id", "domain", "domain_name", "table", "table_name",
                        "section", "section_type", "level", "char_count", "source_file"]:
                val = chunk[key]
                if val is None:
                    f.write(f"{key}: null\n")
                else:
                    f.write(f"{key}: {val}\n")
            f.write("---\n\n")
            f.write(chunk["content"])

    # ---- 统计输出 ----
    total_chars = sum(c["char_count"] for c in chunks)
    level_counts = {}
    domain_counts = {}
    for c in chunks:
        level_counts[c["level"]] = level_counts.get(c["level"], 0) + 1
        domain_counts[c["domain"]] = domain_counts.get(c["domain"], 0) + 1

    print(f"完成！共生成 {len(chunks)} 个 chunk，总字符数 {total_chars}")
    print(f"按粒度统计: {level_counts}")
    print(f"按数据域统计: {domain_counts}")
    print(f"输出文件: {JSONL_FILE}")
    print(f"单独 md 文件目录: {md_dir}")
    print()
    print(f"{'chunk_id':<12} {'level':<10} {'domain':<22} {'table':<26} {'section':<18} {'chars':>6}")
    print("-" * 100)
    for c in chunks:
        print(f"{c['chunk_id']:<12} {c['level']:<10} {c['domain']:<22} "
              f"{str(c['table'] or ''):<26} {str(c['section'] or ''):<18} {c['char_count']:>6}")


if __name__ == "__main__":
    main()
