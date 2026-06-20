#!/usr/bin/env python3
"""
BM25 检索模块：基于 chunk 数据构建 BM25 索引，支持中文查询。

用法：
    from bm25_retriever import BM25Retriever
    retriever = BM25Retriever()
    retriever.build_from_jsonl("chunks/database_chunks.jsonl")
    results = retriever.search("战斗事件有哪些字段？", top_k=5)
"""

import json
import re
import jieba
from pathlib import Path
from rank_bm25 import BM25Okapi

BASE_DIR = Path(__file__).parent
DEFAULT_JSONL = BASE_DIR / "chunks" / "database_chunks.jsonl"


class BM25Retriever:
    """BM25 检索器，基于 jieba 中文分词 + rank_bm25"""

    def __init__(self):
        self.chunks = []          # 原始 chunk 列表（含 metadata）
        self.bm25 = None          # BM25 索引
        self.tokenized_corpus = []  # 分词后的文档列表

    # ------------------------------------------------------------------ #
    #  构建索引
    # ------------------------------------------------------------------ #
    def build_from_jsonl(self, jsonl_path: str | Path = DEFAULT_JSONL) -> int:
        """从 JSONL 文件加载 chunk 并构建 BM25 索引。返回 chunk 数量。"""
        chunks = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    chunks.append(json.loads(line))

        self.chunks = chunks
        self._build_index()
        return len(chunks)

    def _build_index(self):
        """对所有 chunk 分词，构建 BM25 索引。"""
        self.tokenized_corpus = [
            self._tokenize(chunk["content"]) for chunk in self.chunks
        ]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    # ------------------------------------------------------------------ #
    #  分词
    # ------------------------------------------------------------------ #
    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """中文分词：去除标点/空白后用 jieba 分词。"""
        # 去掉 markdown 格式符号，保留中文、英文、数字、下划线
        text = re.sub(r"[|#`*_\-\\/]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        tokens = [t for t in jieba.lcut(text) if t.strip()]
        return tokens

    # ------------------------------------------------------------------ #
    #  检索
    # ------------------------------------------------------------------ #
    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        检索与 query 最相关的 top_k 个 chunk。

        返回: list of dict，每个 dict 包含：
            - chunk_id, domain, table, section, level
            - content（截断前 200 字预览）
            - score: BM25 分数
            - rank: 排名（从 1 开始）
        """
        if self.bm25 is None:
            raise RuntimeError("索引未构建，请先调用 build_from_jsonl()")

        query_tokens = self._tokenize(query)
        scores = self.bm25.get_scores(query_tokens)

        # 按分数降序，取 top_k
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for rank, idx in enumerate(top_indices, 1):
            chunk = self.chunks[idx]
            results.append({
                "rank": rank,
                "score": round(scores[idx], 4),
                "chunk_id": chunk["chunk_id"],
                "domain": chunk["domain"],
                "table": chunk.get("table"),
                "section": chunk.get("section"),
                "level": chunk["level"],
                "content_preview": chunk["content"][:200] + ("..." if len(chunk["content"]) > 200 else ""),
            })
        return results

    def search_full(self, query: str, top_k: int = 5) -> list[dict]:
        """返回完整 content 的检索结果。"""
        results = self.search(query, top_k)
        # 把 preview 换成完整 content
        by_id = {c["chunk_id"]: c for c in self.chunks}
        for r in results:
            r["content"] = by_id[r["chunk_id"]]["content"]
            r.pop("content_preview", None)
        return results


# ------------------------------------------------------------------ #
#  命令行测试
# ------------------------------------------------------------------ #
def run_batch_test():
    """批量测试：跑几个预设查询看看效果。"""
    retriever = BM25Retriever()
    n = retriever.build_from_jsonl()
    print(f"已加载 {n} 个 chunk，BM25 索引构建完成\n")

    test_queries = [
        "战斗事件有哪些字段？",
        "用户画像包含哪些标签？",
        "充值订单表有哪些字段？",
        "流失预测模型输出什么？",
        "做流失分析要用哪些表？",
        "公会相关的数据在哪里？",
    ]

    for q in test_queries:
        print("=" * 70)
        print(f"Query: {q}")
        print("-" * 70)
        results = retriever.search(q, top_k=3)
        for r in results:
            table_str = r["table"] or "-"
            section_str = r["section"] or "-"
            print(f"  #{r['rank']}  score={r['score']:<8.4f} "
                  f"[{r['domain']}/{table_str}/{section_str}] "
                  f"({r['chunk_id']})")
        print()


def run_interactive():
    """交互式测试：在终端输入问题，实时返回结果。输入 quit 退出。"""
    retriever = BM25Retriever()
    n = retriever.build_from_jsonl()
    print(f"已加载 {n} 个 chunk，BM25 索引构建完成")
    print("输入你的问题进行检索，输入 quit/q 退出\n")

    while True:
        try:
            query = input("🔍 请输入问题: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if query.lower() in ("quit", "q", "exit"):
            print("再见！")
            break
        if not query:
            continue

        # 支持 "问题 -k 5" 这种格式指定 top_k
        top_k = 5
        m = __import__("re").search(r"-k\s*(\d+)", query)
        if m:
            top_k = int(m.group(1))
            query = query[:m.start()].strip()

        results = retriever.search(query, top_k=top_k)
        print(f"  找到 {len(results)} 个结果：\n")
        for r in results:
            table_str = r["table"] or "-"
            section_str = r["section"] or "-"
            print(f"  #{r['rank']}  score={r['score']:.4f}  "
                  f"[{r['level']}] {r['domain']} / {table_str} / {section_str}  "
                  f"({r['chunk_id']})")
            print(f"      {r['content_preview'][:80]}...")
            print()


def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_batch_test()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
