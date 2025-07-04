# 🤖 Assistente Inteligente Multitemático

Solução de assistente conversacional com NLP + RAG + LLM, agora com suporte a múltiplos domínios (temas de agente) e múltiplos temas visuais para o frontend. O sistema carrega dinamicamente a base de conhecimento, intenções e personalidade do agente, e permite que o usuário personalize a aparência da interface de chat.

## 🚀 Funcionalidades

- **Interface Web Interativa:** Frontend completo com HTML, CSS e JavaScript.
- **Seleção de Agente:** Escolha com qual "personalidade" de agente você quer conversar (ex: Bancário, Especialista em IA, etc.).
- **Seleção de Tema Visual:** Personalize a aparência do chat com temas como Padrão, Matrix ou Exterminador do Futuro.
- **Suporte Dinâmico a Múltiplos Temas de Agente:** Configure diferentes assistentes, cada um com sua própria base de conhecimento, intenções e prompt de sistema.
- Compreensão de linguagem natural com detecção de intenções (específica por tema).
- Análise de sentimentos e emoções.
- Extração de entidades.
- Busca semântica com RAG (FAISS + SBERT) na base de conhecimento do tema.
- Geração de respostas personalizadas com OpenAI.
- Escalonamento para atendimento humano (via N8N).

## 🧱 Arquitetura

- **Backend:** FastAPI + Python
- **Frontend:** HTML, CSS, JavaScript (sem frameworks)
- **LLM:** OpenAI (gpt-3.5-turbo, gpt-4, etc.)
- **Busca Semântica:** FAISS + SentenceTransformers
- **Orquestração:** N8N (via HTTP Webhook)

## 📁 Estrutura do Projeto

A estrutura foi atualizada para separar claramente o backend, o frontend e os temas de agente.

```txt
assistente-bancario/
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
│       └── terminator.css
├── themes/
│   ├── banking/
│   │   ├── knowledge/
│   │   │   └── *.txt, *.pdf
│   │   ├── intents.json
│   │   └── prompt.txt
│   └── ... (outros temas de agente)
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

```bash
python -m spacy download pt_core_news_sm
```

**3. Configure sua chave da API da OpenAI:**

Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave:

```
OPENAI_API_KEY="sk-..."
```

**4. Construa os Índices de Conhecimento:**

Antes de rodar a aplicação, gere os índices de busca para cada tema de agente.

```bash
python build_all_themes.py
```

Este comando irá ler os arquivos em `themes/*/knowledge/` e criar um índice FAISS (`faiss_index.pkl`) e um arquivo de passagens (`passages.pkl`) dentro de cada diretório de tema.

**5. Inicie o Servidor Backend:**

```bash
cd backend
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.

**6. Use a Interface Web:**

Após iniciar o servidor, **abra o arquivo `frontend/index.html` diretamente no seu navegador**.

A interface permitirá que você escolha:
- **Agente:** O especialista com quem você quer conversar.
- **Visual:** A aparência da janela de chat.

## ✨ Como Adicionar Novos Temas

### Adicionando um Novo Agente

1.  **Crie a Estrutura:** Adicione uma nova pasta dentro de `themes/`. Por exemplo, `themes/legal_expert/`.
2.  **Adicione os Arquivos:** Dentro da nova pasta, crie:
    *   Uma pasta `knowledge/` com os arquivos de base de conhecimento (`.txt`, `.pdf`).
    *   Um arquivo `intents.json` com as intenções e exemplos para o novo domínio.
    *   Um arquivo `prompt.txt` com o prompt de sistema que define a personalidade do novo agente.
3.  **Construa o Índice:** Execute novamente o script para indexar o novo tema.
    ```bash
    python build_all_themes.py
    ```
4.  **Pronto!** Reinicie o servidor e atualize o `frontend/index.html`. O novo agente aparecerá automaticamente no seletor "Agente".

### Adicionando um Novo Tema Visual

1.  **Crie o CSS:** Adicione um novo arquivo CSS na pasta `frontend/css/`, por exemplo, `cyberpunk.css`.
2.  **Estilize os Elementos:** Use os arquivos `default.css` ou `matrix.css` como base para garantir que todos os seletores CSS necessários (`#chat-container`, `.message`, etc.) sejam estilizados.
3.  **Atualize o HTML:**
    *   Adicione um link para seu novo CSS no `<head>` do `index.html`:
        ```html
        <link id="theme-cyberpunk" rel="stylesheet" href="css/cyberpunk.css" disabled>
        ```
    *   Adicione a nova opção ao seletor de tema visual:
        ```html
        <select id="ui-theme-selector">
            <option value="default">Padrão</option>
            <option value="matrix">Matrix</option>
            <option value="terminator">Exterminador</option>
            <option value="cyberpunk">Cyberpunk</option> <!-- Nova opção -->
        </select>
        ```
    *   Adicione o novo tema ao objeto JavaScript `themeStylesheets` no `index.html`:
        ```javascript
        const themeStylesheets = {
            'default': document.getElementById('theme-default'),
            'matrix': document.getElementById('theme-matrix'),
            'terminator': document.getElementById('theme-terminator'),
            'cyberpunk': document.getElementById('theme-cyberpunk') // Novo tema
        };
        ```
4.  **Pronto!** Abra o `index.html` no navegador e seu novo tema visual estará disponível para seleção.