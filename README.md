# 🤖 Assistente Inteligente Bancário

Solução de atendimento ao cliente com NLP + RAG + LLM para compreensão de linguagem natural, emoção, contexto e respostas automáticas inteligentes.

## 🚀 Funcionalidades

- Compreensão de linguagem natural com detecção de intenções
- Análise de sentimentos e emoções do cliente
- Extração de entidades financeiras
- Busca semântica com RAG (FAISS + SBERT)
- Geração de respostas personalizadas com OpenAI GPT-4o
- Escalonamento automático para atendimento humano

## 🧱 Arquitetura

- Backend: FastAPI + Python
- LLM: OpenAI GPT-4o
- Busca Semântica: FAISS + SentenceTransformers
- Orquestração: N8N (via HTTP Webhook)

## 📁 Estrutura do Projeto

backend/
├── main.py
├── agent/
│ ├── memory.py
│ └── decision.py
├── nlp/
│ ├── intent_detector.py
│ ├── sentiment_emotion.py
│ ├── ner_extractor.py
├── rag/
│ ├── index.py
│ └── search.py
├── utils/
│ └── preprocessing.py
├── docs/
│ └── base_conhecimento.txt
├── nlp/intents.json
    

## 📦 Instalação

```bash
git clone https://github.com/seu-usuario/assistente-bancario.git
cd assistente-bancario
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt

```

```bash

python -m spacy download pt_core_news_sm

```

Esse comando serve para baixar e instalar um modelo de linguagem pré-treinado para a biblioteca `spaCy`. Vamos quebrar o comando:

*   `python -m spacy`: Executa a interface de linha de comando do `spaCy`.
*   `download`: É o comando para baixar um modelo.
*   `pt_core_news_sm`: É o nome do modelo:
    *   `pt`: Refere-se ao idioma Português.
    *   `core`: É um modelo de propósito geral (vocabulário, sintaxe, entidades, etc.).
    *   `news`: Indica que foi treinado em textos de notícias.
    *   `sm`: Significa "small" (pequeno), indicando o tamanho do modelo.

Em resumo, o comando instala um modelo de português para que o `spaCy` possa realizar tarefas de Processamento de Linguagem Natural (NLP), como a extração de entidades que é feita no arquivo `ner_extractor.py`.



```bash

OPENAI_API_KEY=sk-xxxx


source venv/Scripts/activate
uvicorn main:app --reload

curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "cliente001", "message": "Quero saber meu saldo"}'

# Gerar índice FAISS a partir do conteúdo .txt
python backend/rag/build_index.py

```

### 🎯 Objetivos do Projeto

Desenvolver um **Assistente Inteligente Bancário** capaz de:

1.  **Receber e processar** consultas em linguagem natural dos clientes.
2.  **Analisar o contexto emocional** da interação (frustração, urgência, satisfação).
3.  **Consultar a base de conhecimento** bancária existente (produtos, regulamentações, FAQ).
4.  **Gerar respostas personalizadas** que demonstrem compreensão tanto técnica quanto emocional.
5.  **Escalar automaticamente** para atendimento humano quando necessário.

### 🛠️ Componentes Técnicos Esperados

*   **Pipeline de NLP Clássico:**
    *   Pré-processamento e normalização de texto.
    *   Análise de sentimentos e detecção de intenções.
    *   Extração de entidades financeiras (valores, contas, produtos).
*   **Arquitetura RAG (Retrieval-Augmented Generation):**
    *   Sistema de busca semântica na base de conhecimento.
    *   Ranking e seleção de informações relevantes.
    *   Geração contextualizada de respostas.
*   **Agentificação Inteligente:**
    *   Orquestração de múltiplos modelos especializados.
    *   Sistema de decisão para escalação.
    *   Memória conversacional e contexto de sessão.