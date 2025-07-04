# 🤖 Assistente Inteligente Multitemático

Solução de assistente conversacional com NLP + RAG + LLM, agora com suporte a múltiplos domínios (temas). O sistema carrega dinamicamente a base de conhecimento, intenções e personalidade do agente, permitindo atuar como um assistente bancário, um analista literário, ou qualquer outro tema configurado.

## 🚀 Funcionalidades

- **Suporte Dinâmico a Múltiplos Temas:** Configure diferentes "personalidades" para o agente, cada uma com sua própria base de conhecimento, intenções e prompt de sistema.
- Compreensão de linguagem natural com detecção de intenções (específica por tema).
- Análise de sentimentos e emoções do cliente.
- Extração de entidades (atualmente focado em finanças, mas pode ser estendido).
- Busca semântica com RAG (FAISS + SBERT) na base de conhecimento do tema.
- Geração de respostas personalizadas com OpenAI.
- Escalonamento automático para atendimento humano.

## 🧱 Arquitetura

- Backend: FastAPI + Python
- LLM: OpenAI (gpt-3.5-turbo, gpt-4, etc.)
- Busca Semântica: FAISS + SentenceTransformers
- Orquestração: N8N (via HTTP Webhook)

## 📁 Estrutura do Projeto

A nova estrutura é baseada em temas, permitindo a fácil adição de novos domínios.

```txt
assistente-bancario/
├── backend/
│   ├── main.py
│   ├── agent/
│   ├── nlp/
│   ├── rag/
│   └── utils/
├── themes/
│   ├── banking/
│   │   ├── knowledge/
│   │   │   └── *.txt, *.pdf
│   │   ├── intents.json
│   │   └── prompt.txt
│   └── literature/
│       ├── knowledge/
│       │   └── *.txt, *.pdf
│       ├── intents.json
│       └── prompt.txt
├── build_all_themes.py
├── requirements.txt
└── README.md
```

## 📦 Instalação e Execução

**1. Clone o repositório e instale as dependências:**

```bash
git clone https://github.com/seu-usuario/assistente-bancario.git
cd assistente-bancario
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/macOS
# source venv/bin/activate
pip install -r requirements.txt
```

**2. Baixe o modelo de linguagem para spaCy:**

Este modelo é usado para tarefas de NLP como a extração de entidades.

```bash
python -m spacy download pt_core_news_sm
```

**3. Configure sua chave da API da OpenAI:**

Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave:

```
OPENAI_API_KEY="sk-..."
```

**4. Construa os Índices de Conhecimento:**

Antes de rodar a aplicação, você precisa gerar os índices de busca para cada tema. O script `build_all_themes.py` automatiza isso.

```bash
python build_all_themes.py
```

Este comando irá ler os arquivos em `themes/*/knowledge/` e criar um índice FAISS (`faiss_index.pkl`) e um arquivo de passagens (`passages.pkl`) dentro de cada diretório de tema.

**5. Inicie o Servidor:**

```bash
uvicorn backend.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

## ⚙️ Como Usar a API

O endpoint `/chat` agora aceita um campo `theme` para selecionar o assistente desejado.

**Exemplo de requisição para o tema "banking":**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
        "session_id": "cliente001",
        "message": "Quero saber sobre o cartão de crédito",
        "theme": "banking"
      }'
```

**Exemplo de requisição para o tema "literature":**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
        "session_id": "leitor001",
        "message": "Qual o tema principal de Dom Casmurro?",
        "theme": "literature"
      }'
```

> Se o campo `theme` não for enviado, o sistema usará `"banking"` como padrão.

## ✨ Como Adicionar um Novo Tema

1.  **Crie a Estrutura:** Adicione uma nova pasta dentro de `themes/`. Por exemplo, `themes/legal/`.
2.  **Adicione os Arquivos:** Dentro da nova pasta (`legal/`), crie:
    *   Uma pasta `knowledge/` contendo os arquivos de base de conhecimento (`.txt`, `.pdf`).
    *   Um arquivo `intents.json` com as intenções e exemplos para o novo domínio.
    *   Um arquivo `prompt.txt` com o prompt de sistema que define a personalidade e as instruções do novo agente. Use os placeholders como `{context}`, `{history_text}`, etc., conforme necessário.
3.  **Construa o Índice:** Execute novamente o script para criar o índice do novo tema.
    ```bash
    python build_all_themes.py
    ```
4.  **Pronto!** Agora você pode fazer requisições à API usando `"theme": "legal"`.