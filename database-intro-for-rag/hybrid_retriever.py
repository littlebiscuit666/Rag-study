#!/usr/bin/env python3
"""
混合检索模块：BM25 + 向量召回，RRF / 加权融合。

用法：
    from hybrid_retriever import HybridRetriever
    retriever = HybridRetriever()
    results = retriever.search("战斗事件有哪些字段？", top_k=5)

融合策略：
    - rrf: Reciprocal Rank Fusion（默认，推荐）
    - weighted: 加权分数融合
"""

import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent

# 延迟导入，避免 import 慢
_bm25_retriever = None
_vector_retriever = None


def _get_bm25():
    global _bm25_retriever
    if _bm25_retriever is None:
        from bm25_retriever import BM25Retriever
        _bm25_retriever = BM25Retriever()
        _bm25_retriever.build_from_jsonl()
    return _bm25_retriever


def _get_vector():
    global _vector_retriever
    if _vector_retriever is None:
        from vector_retriever import VectorRetriever
        _vector_retriever = VectorRetriever()
        if not _vector_retriever.load():
            _vector_retriever.build_from_jsonl()
    return _vector_retriever


class HybridRetriever:
    """BM25 + 向量混合检索器。"""

    def __init__(self, method: str = "rrf", rrf_k: int = 60,
                 bm25_weight: float = 0.5, vector_weight: float = 0.5):
        """
        Args:
            method: 融合方式，'rrf' 或 'weighted'
            rrf_k: RRF 的 k 参数（默认 60）
            bm25_weight: 加权融合时 BM25 的权重（仅 weighted 模式）
            vector_weight: 加权融合时向量的权重（仅 weighted 模式）
        """
        self.method = method
        self.rrf_k = rrf_k
        self.bm25_weight = bm25_weight
        self.vector_weight = vector_weight

        # 延迟加载
        self._bm25 = None
        self._vector = None

    def _ensure_loaded(self):
        if self._bm25 is None:
            self._bm25 = _get_bm25()
        if self._vector is None:
            self._vector = _get_vector()

    # ------------------------------------------------------------------ #
    #  检索
    # ------------------------------------------------------------------ #
    def search(self, query: str, top_k: int = 5,
               candidate_k: int = 20, filter: dict = None) -> list[dict]:
        """
        混合检索。

        Args:
            query: 查询文本
            top_k: 返回结果数
            candidate_k: 每个召回器返回的候选数（默认 20，给融合留足够空间）
            filter: metadata 过滤条件（如 {"domain": "ods_event"}）
        """
        self._ensure_loaded()

        # 1. BM25 召回
        bm25_results = self._bm25.search(query, top_k=candidate_k)
        if filter:
            bm25_results = [r for r in bm25_results
                            if all(r.get(k) == v for k, v in filter.items())]

        # 2. 向量召回
        vec_results = self._vector.search(query, top_k=candidate_k, filter=filter)

        # 3. 融合
        if self.method == "rrf":
            merged = self._rrf_fusion(bm25_results, vec_results)
        elif self.method == "weighted":
            merged = self._weighted_fusion(bm25_results, vec_results)
        else:
            raise ValueError(f"未知融合方式: {self.method}")

        # 4. 取 top_k，补充 content_preview
        merged = merged[:top_k]
        self._fill_preview(merged)

        # 加上 rank
        for i, r in enumerate(merged, 1):
            r["rank"] = i

        return merged

    # ------------------------------------------------------------------ #
    #  融合算法
    # ------------------------------------------------------------------ #
    def _rrf_fusion(self, bm25_results: list[dict], vec_results: list[dict]) -> list[dict]:
        """Reciprocal Rank Fusion"""
        scores = {}  # chunk_id -> {info, score}

        for i, r in enumerate(bm25_results):
            cid = r["chunk_id"]
            if cid not in scores:
                scores[cid] = self._copy_info(r)
                scores[cid]["bm25_rank"] = i + 1
                scores[cid]["bm25_score"] = r["score"]
                scores[cid]["rrf_score"] = 0.0
            scores[cid]["rrf_score"] += 1.0 / (self.rrf_k + i + 1)

        for i, r in enumerate(vec_results):
            cid = r["chunk_id"]
            if cid not in scores:
                scores[cid] = self._copy_info(r)
                scores[cid]["vec_rank"] = i + 1
                scores[cid]["vec_score"] = r["score"]
                scores[cid]["rrf_score"] = 0.0
            else:
                scores[cid]["vec_rank"] = i + 1
                scores[cid]["vec_score"] = r["score"]
            scores[cid]["rrf_score"] += 1.0 / (self.rrf_k + i + 1)

        # 按 rrf_score 降序
        merged = sorted(scores.values(), key=lambda x: x["rrf_score"], reverse=True)

        # 把最终分数放到 score 字段
        for r in merged:
            r["score"] = round(r["rrf_score"], 6)
            r["fusion_method"] = "rrf"

        return merged

    def _weighted_fusion(self, bm25_results: list[dict], vec_results: list[dict]) -> list[dict]:
        """加权分数融合（需要先归一化）"""
        scores = {}

        # BM25 归一化（min-max 到 0~1）
        if bm25_results:
            bm25_max = max(r["score"] for r in bm25_results)
            bm25_min = min(r["score"] for r in bm25_results)
            bm25_range = bm25_max - bm25_min if bm25_max != bm25_min else 1.0

        for i, r in enumerate(bm25_results):
            cid = r["chunk_id"]
            norm = (r["score"] - bm25_min) / bm25_range
            if cid not in scores:
                scores[cid] = self._copy_info(r)
                scores[cid]["bm25_rank"] = i + 1
                scores[cid]["bm25_score"] = r["score"]
                scores[cid]["weighted_score"] = 0.0
            scores[cid]["weighted_score"] += self.bm25_weight * norm

        # 向量分数本身就在 0~1（余弦相似度）
        for i, r in enumerate(vec_results):
            cid = r["chunk_id"]
            if cid not in scores:
                scores[cid] = self._copy_info(r)
                scores[cid]["vec_rank"] = i + 1
                scores[cid]["vec_score"] = r["score"]
                scores[cid]["weighted_score"] = 0.0
            else:
                scores[cid]["vec_rank"] = i + 1
                scores[cid]["vec_score"] = r["score"]
            scores[cid]["weighted_score"] += self.vector_weight * r["score"]

        merged = sorted(scores.values(), key=lambda x: x["weighted_score"], reverse=True)

        for r in merged:
            r["score"] = round(r["weighted_score"], 6)
            r["fusion_method"] = "weighted"

        return merged

    # ------------------------------------------------------------------ #
    #  工具
    # ------------------------------------------------------------------ #
    @staticmethod
    def _copy_info(result: dict) -> dict:
        """复制 chunk 的基本信息到新 dict。"""
        return {
            "chunk_id": result["chunk_id"],
            "domain": result["domain"],
            "table": result.get("table"),
            "section": result.get("section"),
            "level": result.get("level"),
        }

    def _fill_preview(self, results: list[dict]):
        """从 BM25 的 chunks 里取完整 content 做 preview。"""
        bm25 = self._bm25
        if not hasattr(bm25, "chunks"):
            for r in results:
                r["content_preview"] = ""
            return
        by_id = {c["chunk_id"]: c for c in bm25.chunks}
        for r in results:
            cid = r["chunk_id"]
            if cid in by_id:
                content = by_id[cid]["content"]
                r["content_preview"] = content[:200] + ("..." if len(content) > 200 else "")
            else:
                r["content_preview"] = ""

    # ------------------------------------------------------------------ #
    #  对比模式：并排展示 BM25 / 向量 / 混合 结果
    # ------------------------------------------------------------------ #
    def compare(self, query: str, top_k: int = 3) -> dict:
        """返回三种方式的结果对比。"""
        self._ensure_loaded()
        bm25_results = self._bm25.search(query, top_k=top_k)
        vec_results = self._vector.search(query, top_k=top_k)
        hybrid_results = self.search(query, top_k=top_k)
        return {
            "bm25": bm25_results,
            "vector": vec_results,
            "hybrid": hybrid_results,
        }


# ------------------------------------------------------------------ #
#  命令行入口
# ------------------------------------------------------------------ #
def run_batch_test():
    """批量测试，对比三种检索方式。"""
    retriever = HybridRetriever()

    test_queries = [
        "战斗事件有哪些字段？",
        "用户画像包含哪些标签？",
        "充值订单表有哪些字段？",
        "流失预测模型输出什么？",
        "做流失分析要用哪些表？",
        "公会相关的数据在哪里？",
    ]

    for q in test_queries:
        print("=" * 90)
        print(f"Query: {q}")
        print("-" * 90)

        comp = retriever.compare(q, top_k=3)

        # 三列并排展示
        bm25 = comp["bm25"]
        vec = comp["vector"]
        hybrid = comp["hybrid"]

        print(f"  {'BM25':<28}  {'向量':<28}  {'混合(RRF)':<28}")
        print(f"  {'-'*28}  {'-'*28}  {'-'*28}")

        for i in range(3):
            b = bm25[i] if i < len(bm25) else None
            v = vec[i] if i < len(vec) else None
            h = hybrid[i] if i < len(hybrid) else None

            def fmt(r):
                if r is None:
                    return " " * 28
                table = r.get("table") or "-"
                sec = r.get("section") or ""
                label = f"{table}"
                if sec:
                    label += f"/{sec}"
                return f"#{r['rank']} {r['score']:.4f} {label[:22]:<22}"

            print(f"  {fmt(b)}  {fmt(v)}  {fmt(h)}")
        print()


def run_interactive():
    """交互式检索，默认混合模式；输入 --bm25 或 --vector 切单一模式。"""
    retriever = HybridRetriever()

    print("混合检索器已加载（BM25 + 向量，RRF 融合）")
    print("输入问题检索，支持以下命令：")
    print("  --bm25     仅用 BM25")
    print("  --vector   仅用向量")
    print("  --hybrid   混合模式（默认）")
    print("  --compare  三种方式对比")
    print("  -k N       指定返回数量")
    print("  quit/q     退出\n")

    mode = "hybrid"

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

        # 模式切换
        if query == "--bm25":
            mode = "bm25"; print("  → 已切换到 BM25 模式"); continue
        if query == "--vector":
            mode = "vector"; print("  → 已切换到向量模式"); continue
        if query == "--hybrid":
            mode = "hybrid"; print("  → 已切换到混合模式"); continue
        if query == "--compare":
            mode = "compare"; print("  → 已切换到对比模式"); continue

        # 解析 -k
        top_k = 5
        m = re.search(r"-k\s*(\d+)", query)
        if m:
            top_k = int(m.group(1))
            query = query[:m.start()].strip()

        if mode == "bm25":
            results = retriever._bm25.search(query, top_k=top_k)
        elif mode == "vector":
            results = retriever._vector.search(query, top_k=top_k)
        elif mode == "compare":
            comp = retriever.compare(query, top_k=top_k)
            _print_compare(comp)
            continue
        else:
            results = retriever.search(query, top_k=top_k)

        _print_results(results)


def _print_results(results):
    print(f"  找到 {len(results)} 个结果：\n")
    for r in results:
        table_str = r.get("table") or "-"
        section_str = r.get("section") or "-"
        score = r.get("score", 0)
        print(f"  #{r['rank']}  score={score:.4f}  "
              f"[{r.get('level', '?')}] {r['domain']} / {table_str} / {section_str}  "
              f"({r['chunk_id']})")
        preview = r.get("content_preview", "")
        if preview:
            print(f"      {preview[:80]}...")
        # 混合模式额外信息
        if "bm25_rank" in r:
            extra = f"      bm25_rank={r['bm25_rank']}"
            if "vec_rank" in r:
                extra += f"  vec_rank={r['vec_rank']}"
            print(extra)
        print()


def _print_compare(comp):
    bm25, vec, hybrid = comp["bm25"], comp["vector"], comp["hybrid"]
    n = max(len(bm25), len(vec), len(hybrid))
    print(f"  {'BM25':<30}  {'向量':<30}  {'混合(RRF)':<30}")
    print(f"  {'-'*30}  {'-'*30}  {'-'*30}")

    def short(r):
        if r is None:
            return " " * 30
        table = r.get("table") or "-"
        sec = r.get("section") or ""
        label = f"{table}"
        if sec:
            label += f"/{sec}"
        return f"#{r['rank']} {r['score']:.4f} {label[:24]:<24}"

    for i in range(n):
        b = bm25[i] if i < len(bm25) else None
        v = vec[i] if i < len(vec) else None
        h = hybrid[i] if i < len(hybrid) else None
        print(f"  {short(b)}  {short(v)}  {short(h)}")
    print()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_batch_test()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
