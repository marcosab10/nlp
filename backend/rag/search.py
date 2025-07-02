# rag/search.py
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class RAGSearcher:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2',
                 index_path='rag/faiss_index',
                 passages_path='rag/passages.pkl'):
        self.model = SentenceTransformer(model_name)
        self.index = faiss.read_index(index_path)
        with open(passages_path, 'rb') as f:
            self.passages = pickle.load(f)

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        query_vec = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_vec, top_k)
        results = []
        for idx, score in zip(I[0], D[0]):
            if idx < len(self.passages):
                results.append({
                    "text": self.passages[idx],
                    "score": round(float(score), 4)
                })
        return results
