# rag/index.py
import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from typing import List

class RAGIndexer:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2',
                 index_path='rag/faiss_index',
                 passages_path='rag/passages.pkl'):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.passages_path = passages_path
        self.passages = []
        self.index = None

    def load_txt_base(self, file_path: str, chunk_size: int = 500) -> List[str]:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        self.passages = chunks
        return chunks

    def create_index(self):
        embeddings = self.model.encode(self.passages, convert_to_numpy=True, show_progress_bar=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.save_index()
        print(f"[✔] Index criado com {len(self.passages)} passagens.")

    def save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.passages_path, 'wb') as f:
            pickle.dump(self.passages, f)

    def build_from_txt(self, txt_file: str):
        self.load_txt_base(txt_file)
        self.create_index()
