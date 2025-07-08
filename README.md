# 🤖 Assistente Inteligente Multitemático

Uma solução de assistente conversacional que integra Processamento de Linguagem Natural (NLP), Retrieval-Augmented Generation (RAG) e Grandes Modelos de Linguagem (LLMs). A plataforma se destaca por seu suporte a múltiplos domínios (temas de agente) e múltiplos temas visuais para o frontend. O sistema carrega dinamicamente a base de conhecimento, intenções e a personalidade do agente, permitindo que o usuário personalize tanto a especialidade do assistente quanto a aparência da interface de chat.

## 🚀 Funcionalidades

- **Interface Web Interativa:** Frontend completo construído com HTML, CSS e JavaScript puro.
- **Seleção Dinâmica de Agente:** Permite ao usuário escolher com qual "personalidade" de agente deseja interagir (ex: Especialista em IA, Consultor Financeiro, Crítico Literário, etc.).
- **Seleção de Tema Visual:** Personalize a aparência do chat com temas como Padrão, Matrix, Cyberpunk e Exterminador do Futuro.
- **Arquitetura Multitemática:** Configure múltiplos assistentes, cada um com sua própria base de conhecimento (`knowledge`), conjunto de intenções (`intents.json`) e persona (`prompt.txt`).
- **Pipeline de NLP:**
    - Compreensão de linguagem natural com detecção de intenções (específica por tema).
    - Análise de sentimentos e emoções.
    - Extração de Entidades Nomeadas (NER).
- **Busca Semântica (RAG):** Utiliza FAISS e SentenceTransformers para buscar informações relevantes na base de conhecimento do tema selecionado.
- **Geração de Respostas com LLM:** Integra-se com a API da OpenAI para gerar respostas contextuais e personalizadas.
- **Memória Conversacional:** Mantém o histórico da conversa por sessão.
- **Escalonamento para Atendimento Humano:** Lógica de decisão para escalonamento, com integração via webhook para plataformas como N8N.
- **Containerização:** Suporte completo para execução com Docker e Docker Compose.

## 🧱 Arquitetura

- **Backend:** FastAPI (Python)
- **Frontend:** HTML, CSS, JavaScript (sem frameworks)
- **LLM:** OpenAI (gpt-3.5-turbo, gpt-4, etc.)
- **Busca Semântica (RAG):** FAISS + SentenceTransformers
- **NLP:** spaCy, Transformers, SentenceTransformers
- **Orquestração/Workflow:** N8N (via Webhook)
- **Serviços Adicionais (via Docker):** Redis, PostgreSQL

## 📁 Estrutura do Projeto

A estrutura foi organizada para separar claramente o backend, o frontend, os temas dos agentes e a configuração de containerização.

```txt
nlp/
├── backend/
│   ├── main.py
│   ├── agent/
│   ├── nlp/
│   ├── rag/
│   └── utils/
├── frontend/
│   ├── index.html
│   └── css/
│       ├── default.css
│       ├── matrix.css
│       ├── cyberpunk.css
│       └── terminator.css
├── n8n-fluxos/
│   └── ChatBot.json
├── themes/
│   ├── ai_specialist/
│   ├── banking/
│   ├── fuzzy_logic_expert/
│   └── literature/
│       ├── knowledge/
│       │   └── *.txt, *.pdf
│       ├── intents.json
│       └── prompt.txt
├── build_all_themes.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## ⚙️ Como Funciona

1.  **Frontend:** O usuário seleciona um tema de agente (ex: "Banking") e um tema visual (ex: "Cyberpunk") e envia uma mensagem.
2.  **Backend (FastAPI):** A `main.py` recebe a requisição.
3.  **Carregamento Dinâmico:** O sistema carrega os componentes do agente selecionado (buscador RAG, detector de intenção, prompt do sistema) com base no tema escolhido.
4.  **Pipeline NLP:** A mensagem do usuário é processada para extrair a intenção, entidades, sentimento e emoções.
5.  **Decisão de Escalonamento:** O `agent/decision.py` avalia se a conversa deve ser escalada para um atendente humano.
6.  **Busca RAG:** Se não for escalonado, o `rag/search.py` busca na base de conhecimento vetorial (índice FAISS) por informações relevantes para a consulta.
7.  **Geração com LLM:** O prompt do sistema, o histórico da conversa, a pergunta do usuário e o contexto recuperado pelo RAG são enviados para a API da OpenAI.
8.  **Resposta:** A resposta gerada pelo LLM é enviada de volta para o frontend e exibida ao usuário.

## 📦 Instalação e Execução

Existem duas maneiras de executar o projeto: localmente com um ambiente Python ou usando Docker.

### Opção 1: Execução Local

**1. Clone o repositório e instale as dependências:**

```bash
# git clone https://github.com/seu-usuario/assistente-bancario.git
cd assistente-bancario
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/macOS
# source venv/bin/activate
pip install -r requirements.txt
```

**2. Baixe o modelo de linguagem para spaCy:**

```bash
python -m spacy download pt_core_news_sm
```

**3. Configure sua chave da API da OpenAI:**

Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave:

```
OPENAI_API_KEY="sk-..."
```

**4. Construa os Índices de Conhecimento:**

Antes de rodar a aplicação, gere os índices de busca para cada tema de agente. Este script irá processar os arquivos em `themes/*/knowledge/` e criar um índice FAISS (`faiss_index`) e um arquivo de passagens (`passages.pkl`) em cada diretório de tema.

```bash
python build_all_themes.py
```

**5. Inicie o Servidor Backend:**

Execute o servidor a partir da raiz do projeto. O Uvicorn irá servir tanto a API quanto o frontend.

```bash
cd backend

uvicorn main:app --reload
```

**6. Acesse a Aplicação:**

Abra seu navegador e acesse `http://127.0.0.1:8000`.

### Opção 2: Execução com Docker (Recomendado)

O `docker-compose` orquestra todos os serviços necessários, incluindo o backend, Redis e Postgres.

**1. Pré-requisitos:**
   - Docker instalado e em execução.
   - Docker Compose instalado.

**2. Configure a Chave da API:**
   - Crie o arquivo `.env` na raiz do projeto, como descrito na execução local.

**3. Construa e Inicie os Containers:**

Execute o seguinte comando na raiz do projeto:

```bash
docker-compose up --build
```

Este comando irá:
- Construir a imagem do Python com todas as dependências.
- Baixar o modelo do spaCy.
- Iniciar os serviços de Redis e Postgres.
- Iniciar a aplicação Python, que por sua vez irá construir os índices dos temas e iniciar o servidor.

**4. Acesse a Aplicação:**

Abra seu navegador e acesse `http://localhost:8000`.

## 🎨 Temas (Agentes)

Para adicionar um novo agente, basta criar uma nova pasta dentro do diretório `themes/`. Por exemplo, para um agente "historiador":

1.  Crie a pasta `themes/historian/`.
2.  Adicione uma pasta `knowledge/` dentro de `historian/` com seus arquivos `.txt` ou `.pdf`.
3.  Crie um arquivo `intents.json` com as intenções e exemplos específicos para história.
4.  Crie um arquivo `prompt.txt` definindo a persona e as regras do agente historiador.

Depois de adicionar o novo tema, execute novamente o script `build_all_themes.py` (se estiver rodando localmente) ou reinicie os containers do Docker para que o novo índice seja criado. O novo agente aparecerá automaticamente no seletor do frontend.
