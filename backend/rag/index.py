# rag/index.py
import os
import faiss
import pickle
import glob
from sentence_transformers import SentenceTransformer
from typing import List
from pypdf import PdfReader

class RAGIndexer:
    def __init__(self, theme_path: str, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        """Inicializa o indexador para um tema específico."""
        self.model = SentenceTransformer(model_name)
        self.theme_path = theme_path
        
        # Garante que o diretório do tema exista
        os.makedirs(self.theme_path, exist_ok=True)

        # Os caminhos do índice e das passagens agora são relativos à pasta do tema
        self.index_path = os.path.join(self.theme_path, 'faiss_index')
        self.passages_path = os.path.join(self.theme_path, 'passages.pkl')
        
        self.passages = []
        self.index = None

    def load_pdf_base(self, file_path: str, chunk_size: int = 500) -> List[str]:
        """Lê o texto de um único arquivo PDF e o divide em chunks."""
        try:
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                full_text += (page.extract_text() or "") + "\n"
            
            full_text = " ".join(full_text.strip().split())
            chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
            return chunks
        except Exception as e:
            print(f"[❌] Erro ao ler o arquivo PDF '{os.path.basename(file_path)}': {e}")
            return []

    def load_txt_base(self, file_path: str, chunk_size: int = 500) -> List[str]:
        """Lê o texto de um único arquivo TXT e o divide em chunks."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            return chunks
        except Exception as e:
            print(f"[❌] Erro ao ler o arquivo TXT '{os.path.basename(file_path)}': {e}")
            return []

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

    def build_from_knowledge_base(self, chunk_size: int = 500):
        """Lê todos os arquivos (.pdf, .txt) do subdiretório 'knowledge' de um tema."""
        knowledge_path = os.path.join(self.theme_path, "knowledge")
        if not os.path.isdir(knowledge_path):
            print(f"[⚠️] Diretório de conhecimento não encontrado para o tema: {self.theme_path}")
            return

        all_files = glob.glob(os.path.join(knowledge_path, "*.*"))
        pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
        txt_files = [f for f in all_files if f.lower().endswith('.txt')]

        if not pdf_files and not txt_files:
            print(f"[❌] Nenhum arquivo .pdf ou .txt encontrado em '{knowledge_path}'.")
            return

        print(f"[ℹ️] Indexando para o tema: '{os.path.basename(self.theme_path)}'")
        
        all_passages = []
        for file_path in pdf_files:
            print(f"  -> Lendo PDF: '{os.path.basename(file_path)}'...")
            passages = self.load_pdf_base(file_path, chunk_size)
            all_passages.extend(passages)

        for file_path in txt_files:
            print(f"  -> Lendo TXT: '{os.path.basename(file_path)}'...")
            passages = self.load_txt_base(file_path, chunk_size)
            all_passages.extend(passages)
        
        if not all_passages:
            print("[❌] Nenhum texto pôde ser extraído dos arquivos.")
            return

        self.passages = all_passages
        self.create_index()
