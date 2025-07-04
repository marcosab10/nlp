# build_all_themes.py
import os
import sys

# Adiciona o diretório 'backend' ao path para que possamos importar o RAGIndexer
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from rag.index import RAGIndexer

def build_themes():
    """Encontra todos os temas no diretório 'themes' e constrói o índice para cada um."""
    # O caminho para a pasta de temas é relativo à localização deste script
    themes_dir = os.path.join(os.path.dirname(__file__), 'themes')
    
    if not os.path.isdir(themes_dir):
        print(f"[❌] Diretório de temas não encontrado em '{themes_dir}'.")
        return

    # Lista todos os subdiretórios na pasta 'themes'
    theme_names = [d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d))]

    if not theme_names:
        print(f"[⚠️] Nenhum tema encontrado no diretório '{themes_dir}'.")
        return

    print(f"Encontrados {len(theme_names)} temas: {', '.join(theme_names)}\n")

    for theme_name in theme_names:
        theme_path = os.path.join(themes_dir, theme_name)
        
        # Cria uma instância do indexador para o tema específico
        indexer = RAGIndexer(theme_path=theme_path)
        
        # Constrói o índice a partir da base de conhecimento do tema
        indexer.build_from_knowledge_base()
        print("---")

    print("\n[✅] Processo de construção de todos os temas concluído.")

if __name__ == "__main__":
    build_themes()
