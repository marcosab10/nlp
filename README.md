# 🤖 Assistente Inteligente Multitemático

<<<<<<< HEAD
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
=======
Solução de assistente conversacional com NLP + RAG + LLM, agora com suporte a múltiplos domínios (temas). O sistema carrega dinamicamente a base de conhecimento, intenções e personalidade do agente, permitindo atuar como um assistente bancário, um analista literário, ou qualquer outro tema configurado.

## 🚀 Funcionalidades

- **Interface Web Interativa:** Frontend com seletor de temas para uma experiência de usuário mais amigável.
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
>>>>>>> 155fc216364856ba81d90ad6ea97a2b4d4c1c383

```txt
assistente-bancario/
├── backend/
│   ├── main.py
│   ├── agent/
│   ├── nlp/
│   ├── rag/
│   └── utils/
<<<<<<< HEAD
├── frontend/
│   ├── index.html
│   └── css/
│       ├── default.css
│       ├── matrix.css
│       └── terminator.css
=======
>>>>>>> 155fc216364856ba81d90ad6ea97a2b4d4c1c383
├── themes/
│   ├── banking/
│   │   ├── knowledge/
│   │   │   └── *.txt, *.pdf
│   │   ├── intents.json
│   │   └── prompt.txt
<<<<<<< HEAD
│   └── ... (outros temas de agente)
=======
│   └── literature/
│       ├── knowledge/
│       │   └── *.txt, *.pdf
│       ├── intents.json
│       └── prompt.txt
>>>>>>> 155fc216364856ba81d90ad6ea97a2b4d4c1c383
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

<<<<<<< HEAD
=======
Este modelo é usado para tarefas de NLP como a extração de entidades.

>>>>>>> 155fc216364856ba81d90ad6ea97a2b4d4c1c383
```bash
python -m spacy download pt_core_news_sm
```

**3. Configure sua chave da API da OpenAI:**

Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave:

```
OPENAI_API_KEY="sk-..."
```

**4. Construa os Índices de Conhecimento:**

<<<<<<< HEAD
Antes de rodar a aplicação, gere os índices de busca para cada tema de agente.
=======
Antes de rodar a aplicação, você precisa gerar os índices de busca para cada tema. O script `build_all_themes.py` automatiza isso.
>>>>>>> 155fc216364856ba81d90ad6ea97a2b4d4c1c383

```bash
python build_all_themes.py
```

Este comando irá ler os arquivos em `themes/*/knowledge/` e criar um índice FAISS (`faiss_index.pkl`) e um arquivo de passagens (`passages.pkl`) dentro de cada diretório de tema.

<<<<<<< HEAD
**5. Inicie o Servidor Backend:**

=======
**5. Inicie o Servidor:**

Navegue até o diretório do backend e inicie o servidor Uvicorn.

>>>>>>> 155fc216364856ba81d90ad6ea97a2b4d4c1c383
```bash
cd backend
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`.

**6. Use a Interface Web:**

<<<<<<< HEAD
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
=======
Após iniciar o servidor, abra o arquivo `frontend/index.html` diretamente no seu navegador.

A interface carregará os temas disponíveis em um menu suspenso, permitindo que você converse com o assistente de sua escolha.

## ⚙️ Testando a API (Opcional)

A forma principal de interagir com o assistente é através da interface web. No entanto, você pode testar o endpoint `/chat` diretamente usando ferramentas como `curl`.

O endpoint `/chat` aceita um campo `theme` para selecionar o assistente desejado.

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
4.  **Pronto!** Reinicie o servidor e abra o `frontend/index.html`. O novo tema aparecerá automaticamente no seletor.
>>>>>>> 155fc216364856ba81d90ad6ea97a2b4d4c1c383
