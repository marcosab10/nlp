# rag/index.py
import os
import faiss
import pickle
import glob # Importa a biblioteca glob para encontrar arquivos
from sentence_transformers import SentenceTransformer
from typing import List
from pypdf import PdfReader # Importa a biblioteca para ler PDF

class RAGIndexer:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2',
                 index_path='rag/faiss_index',
                 passages_path='rag/passages.pkl'):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.passages_path = passages_path
        self.passages = []
        self.index = None

    def load_pdf_base(self, file_path: str, chunk_size: int = 500) -> List[str]:
        """Lê o texto de um arquivo PDF, extrai o conteúdo e o divide em chunks."""
        try:
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                full_text += (page.extract_text() or "") + "\n"
            
            # Normaliza espaços em branco e quebras de linha
            full_text = " ".join(full_text.strip().split())

            chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
            self.passages = chunks
            print(f"[✔] PDF lido com sucesso. {len(chunks)} chunks criados.")
            return chunks
        except Exception as e:
            print(f"[❌] Erro ao ler o arquivo PDF: {e}")
            return []

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

    def build_from_pdf(self, pdf_file: str, chunk_size: int = 500):
        """Orquestra a criação do índice a partir de um arquivo PDF."""
        self.load_pdf_base(pdf_file, chunk_size)
        if self.passages:
            self.create_index()

    def build_from_directory(self, dir_path: str, chunk_size: int = 500):
        """Lê todos os arquivos PDF de um diretório, combina o texto e cria o índice."""
        pdf_files = glob.glob(os.path.join(dir_path, "*.pdf"))
        if not pdf_files:
            print(f"[❌] Nenhum arquivo PDF encontrado em '{dir_path}'.")
            return

        print(f"[ℹ️] Encontrados {len(pdf_files)} arquivos PDF para indexação.")
        
        all_passages = []
        for pdf_file in pdf_files:
            print(f"  -> Lendo '{os.path.basename(pdf_file)}'...")
            passages = self.load_pdf_base(pdf_file, chunk_size)
            if passages:
                all_passages.extend(passages)
        
        if not all_passages:
            print("[❌] Nenhum texto pôde ser extraído dos arquivos PDF.")
            return

        self.passages = all_passages
        self.create_index()

    def build_from_txt(self, txt_file: str):
        self.load_txt_base(txt_file)
        self.create_index()
