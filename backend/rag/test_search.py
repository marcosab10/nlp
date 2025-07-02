# test_search.py
from rag.search import RAGSearcher

searcher = RAGSearcher()
resultados = searcher.search("Como abrir uma conta poupança?", top_k=2)

for r in resultados:
    print(f"\n[Score: {r['score']}]\n{r['text']}")