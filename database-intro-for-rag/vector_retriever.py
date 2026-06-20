#!/usr/bin/env python3
"""
向量检索模块：基于 Chroma + bge-small-zh-v1.5 的语义检索。

用法：
    from vector_retriever import VectorRetriever
    retriever = VectorRetriever()
    retriever.build_from_jsonl("chunks/database_chunks.jsonl")
    results = retriever.search("战斗事件有哪些字段？", top_k=5)

命令行：
    python3 vector_retriever.py        # 交互模式
    python3 vector_retriever.py test   # 批量测试
"""

import json
import re
import sys
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).parent
DEFAULT_JSONL = BASE_DIR / "chunks" / "database_chunks.jsonl"
DEFAULT_PERSIST_DIR = BASE_DIR / "chunks" / "chroma_db"

COLLECTION_NAME = "database_chunks"
MODEL_NAME = "BAAI/bge-small-zh-v1.5"

# bge 系列模型官方推荐的 query 前缀，用于提升检索效果
BGE_QUERY_PREFIX = "为这个句子生成表示以用于检索相关文章："


class _SentenceTransformerEmbeddingFunction(embedding_functions.EmbeddingFunction):
    """自定义 EmbeddingFunction，包装 sentence-transformers，支持 bge query 前缀。"""

    def __init__(self, model_name: str, device: str = None):
        self.model = SentenceTransformer(model_name, device=device)

    def __call__(self, input: list[str]) -> list[list[float]]:
        # 注意：这里只处理文档 embedding，query embedding 我们手动加前缀
        embeddings = self.model.encode(input, normalize_embeddings=True, show_progress_bar=False)
        return embeddings.tolist()

    def encode_query(self, query: str) -> list[float]:
        """对查询加 bge 前缀后编码。"""
        text = BGE_QUERY_PREFIX + query
        vec = self.model.encode(text, normalize_embeddings=True, show_progress_bar=False)
        return vec.tolist()


class VectorRetriever:
    """基于 Chroma + bge 的向量检索器。"""

    def __init__(
        self,
        model_name: str = MODEL_NAME,
        persist_dir: str | Path = DEFAULT_PERSIST_DIR,
        device: str = None,
    ):
        self.persist_dir = Path(persist_dir)
        self.ef = _SentenceTransformerEmbeddingFunction(model_name, device=device)
        self.client = chromadb.PersistentClient(path=str(self.persist_dir))
        self.collection = None

    # ------------------------------------------------------------------ #
    #  构建索引
    # ------------------------------------------------------------------ #
    def build_from_jsonl(self, jsonl_path: str | Path = DEFAULT_JSONL, force_rebuild: bool = False) -> int:
        """
        从 JSONL 文件加载 chunk，embedding 后存入 Chroma。
        如果集合已存在且 force_rebuild=False，则跳过构建直接加载。
        返回 chunk 数量。
        """
        # 检查是否已存在集合
        existing_names = [c.name for c in self.client.list_collections()]

        if COLLECTION_NAME in existing_names and not force_rebuild:
            self.collection = self.client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=self.ef,
            )
            count = self.collection.count()
            print(f"集合已存在，直接加载（共 {count} 条）")
            return count

        if COLLECTION_NAME in existing_names and force_rebuild:
            self.client.delete_collection(COLLECTION_NAME)
            print("已删除旧集合，重新构建...")

        # 读取 JSONL
        chunks = []
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    chunks.append(json.loads(line))

        # 创建集合
        self.collection = self.client.create_collection(
            name=COLLECTION_NAME,
            embedding_function=self.ef,
            metadata={"hnsw:space": "cosine"},  # 余弦相似度
        )

        # 批量添加
        ids = [c["chunk_id"] for c in chunks]
        documents = [c["content"] for c in chunks]
        metadatas = [
            {
                "domain": c["domain"],
                "domain_name": c.get("domain_name", ""),
                "table": c.get("table") or "",
                "table_name": c.get("table_name") or "",
                "section": c.get("section") or "",
                "section_type": c.get("section_type") or "",
                "level": c["level"],
                "char_count": c["char_count"],
            }
            for c in chunks
        ]

        print(f"正在对 {len(chunks)} 个 chunk 做 embedding ...")
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )
        print(f"构建完成，共 {self.collection.count()} 条")

        # 把原始 chunks 存一份到内存，方便返回时用
        self._chunks_by_id = {c["chunk_id"]: c for c in chunks}

        return len(chunks)

    def load(self) -> bool:
        """加载已存在的集合，成功返回 True，不存在返回 False。"""
        existing_names = [c.name for c in self.client.list_collections()]
        if COLLECTION_NAME not in existing_names:
            return False
        self.collection = self.client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=self.ef,
        )
        # 加载所有 chunk 数据到内存（量少，无所谓）
        data = self.collection.get(include=["documents", "metadatas"])
        self._chunks_by_id = {}
        for cid, doc, meta in zip(data["ids"], data["documents"], data["metadatas"]):
            self._chunks_by_id[cid] = {
                "chunk_id": cid,
                "content": doc,
                **meta,
            }
        return True

    # ------------------------------------------------------------------ #
    #  检索
    # ------------------------------------------------------------------ #
    def search(self, query: str, top_k: int = 5, filter: dict = None) -> list[dict]:
        """
        向量检索，返回 top_k 个最相似的 chunk。

        filter: Chroma where 条件，如 {"domain": "ods_event"}
        """
        if self.collection is None:
            raise RuntimeError("索引未构建/加载，请先调用 build_from_jsonl() 或 load()")

        # 手动编码 query（加 bge 前缀）
        query_embedding = self.ef.encode_query(query)

        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter,
            include=["documents", "metadatas", "distances"],
        )

        results = []
        ids = result["ids"][0]
        distances = result["distances"][0]
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]

        for rank, (cid, dist, doc, meta) in enumerate(zip(ids, distances, documents, metadatas), 1):
            # Chroma 返回的是 distance（越小越相似），转成 similarity score（越大越相似）
            # cosine distance = 1 - cosine_similarity
            score = 1.0 - dist

            results.append({
                "rank": rank,
                "score": round(score, 4),
                "chunk_id": cid,
                "domain": meta.get("domain"),
                "table": meta.get("table") or None,
                "section": meta.get("section") or None,
                "level": meta.get("level"),
                "content_preview": doc[:200] + ("..." if len(doc) > 200 else ""),
            })

        return results

    def search_full(self, query: str, top_k: int = 5, filter: dict = None) -> list[dict]:
        """返回完整 content 的检索结果。"""
        results = self.search(query, top_k=top_k, filter=filter)
        for r in results:
            if hasattr(self, "_chunks_by_id") and r["chunk_id"] in self._chunks_by_id:
                r["content"] = self._chunks_by_id[r["chunk_id"]]["content"]
            r.pop("content_preview", None)
        return results


# ------------------------------------------------------------------ #
#  命令行入口
# ------------------------------------------------------------------ #
def run_batch_test():
    """批量测试预设查询。"""
    retriever = VectorRetriever()
    if not retriever.load():
        retriever.build_from_jsonl()

    print(f"向量索引加载完成，共 {retriever.collection.count()} 个 chunk\n")

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
    """交互式检索。"""
    retriever = VectorRetriever()
    if not retriever.load():
        retriever.build_from_jsonl()

    print(f"向量索引加载完成，共 {retriever.collection.count()} 个 chunk")
    print("输入问题进行检索，输入 quit/q 退出\n")

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

        # 支持 -k 5 指定 top_k
        top_k = 5
        m = re.search(r"-k\s*(\d+)", query)
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
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_batch_test()
    else:
        run_interactive()


if __name__ == "__main__":
    main()
