# build_index.py
from rag.index import RAGIndexer

indexer = RAGIndexer()
indexer.build_from_txt("../docs/base_conhecimento.txt")