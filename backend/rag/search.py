# rag/search.py
import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class RAGSearcher:
    def __init__(self, theme_path: str, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """Inicializa o buscador para um tema específico."""
        self.model = SentenceTransformer(model_name)
        index_path = os.path.join(theme_path, 'faiss_index')
        passages_path = os.path.join(theme_path, 'passages.pkl')

        if not os.path.exists(index_path) or not os.path.exists(passages_path):
            raise FileNotFoundError(
                f"Índice ou passagens não encontrados para o tema em '{theme_path}'. "
                f"Execute o script de build para este tema primeiro."
            )

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
