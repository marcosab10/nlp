# build_index.py
from rag.index import RAGIndexer

# Crie uma instância do indexador
indexer = RAGIndexer()

# Especifique o caminho para o diretório que contém os PDFs
docs_directory = "../docs/"

# Chame o novo método para construir o índice a partir do diretório
indexer.build_from_directory(docs_directory)

print("\nÍndice criado com sucesso a partir de todos os PDFs no diretório 'docs'.")