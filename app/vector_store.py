import numpy as np
import faiss
from typing import Any, Dict, List
from app.config import settings

class EntitlementVectorStore:
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.doc_store: List[Dict[str, Any]] = []

    def _get_embedding(self, text: str) -> np.ndarray:
        rng = np.random.default_rng(seed=abs(hash(text)) % (2**32))
        vec = rng.standard_normal(self.dimension).astype(np.float32)
        return vec / (np.linalg.norm(vec) + 1e-12)

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        if not documents: return
        vectors = [self._get_embedding(doc["text"]) for doc in documents]
        self.doc_store.extend(documents)
        self.index.add(np.vstack(vectors).astype(np.float32))

    def similarity_search_with_entitlements(self, query: str, allowed_report_ids: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
        if self.index.ntotal == 0: return []
        query_vec = self._get_embedding(query).reshape(1, -1).astype(np.float32)
        scores, indices = self.index.search(query_vec, min(self.index.ntotal, 20))
        matched = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1: continue
            doc = self.doc_store[idx]
            if doc["report_id"] in allowed_report_ids:
                item = dict(doc)
                item["score"] = float(score)
                matched.append(item)
                if len(matched) >= top_k: break
        return matched

vector_db = EntitlementVectorStore(dimension=settings.EMBEDDING_DIMENSION)
