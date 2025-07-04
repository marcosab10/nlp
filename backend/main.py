# main.py
import os
import openai
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache

from utils.preprocessing import normalize_text
from nlp.intent_detector import IntentDetector
from nlp.sentiment_emotion import EmotionAnalyzer
from nlp.ner_extractor import FinanceEntityExtractor
from rag.search import RAGSearcher
from agent.memory import ConversationMemory
from agent.decision import EscalationDecider

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# 🔧 Configuração da chave OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ⚙️ Inicialização
app = FastAPI()

# Cache para os componentes do tema
theme_components_cache: Dict[str, Dict[str, Any]] = {}

# Caminho base para os temas
THEMES_BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'themes'))

@lru_cache(maxsize=None)
def get_theme_components(theme: str):
    """
    Carrega e armazena em cache os componentes de um tema (IntentDetector, RAGSearcher, prompt).
    Usa lru_cache para evitar recarregar os mesmos componentes.
    """
    theme_path = os.path.join(THEMES_BASE_PATH, theme)
    if not os.path.isdir(theme_path):
        raise ValueError(f"Theme '{theme}' not found at {theme_path}")

    # Caminhos para os arquivos do tema
    intents_path = os.path.join(theme_path, 'intents.json')
    prompt_path = os.path.join(theme_path, 'prompt.txt')
    
    # Carregar componentes
    intent_detector = IntentDetector(intents_path=intents_path)
    searcher = RAGSearcher(theme_path=theme_path)
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
        
    return {
        "intent_detector": intent_detector,
        "searcher": searcher,
        "prompt_template": prompt_template
    }


@app.get("/")
async def read_index():
    """Serve o arquivo de frontend index.html."""
    # Constrói o caminho absoluto para o arquivo index.html
    # partindo do diretório do main.py e subindo um nível para a raiz do projeto.
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html'))
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"error": "index.html not found"}

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

@app.get("/themes")
async def get_themes():
    """Lista os temas disponíveis na pasta themes."""
    themes = [d for d in os.listdir(THEMES_BASE_PATH) if os.path.isdir(os.path.join(THEMES_BASE_PATH, d))]
    return {"themes": themes}

# Componentes não dependentes de tema
emotion_analyzer = EmotionAnalyzer()
ner_extractor = FinanceEntityExtractor() # Pode ser específico do tema no futuro
memory = ConversationMemory()
decider = EscalationDecider()

# 📥 Modelo da requisição
class ChatInput(BaseModel):
    session_id: str
    message: str
    theme: str = "banking" # Tema padrão

@app.post("/chat")
async def chat_handler(input: ChatInput):
    session_id = input.session_id
    user_message = input.message
    theme = input.theme

    try:
        # 1. Carregar componentes do tema dinamicamente
        components = get_theme_components(theme)
        intent_detector = components["intent_detector"]
        searcher = components["searcher"]
        prompt_template = components["prompt_template"]
    except ValueError as e:
        return {"error": str(e)}

    # 2. Armazenar mensagem do usuário
    memory.add_message(session_id, "user", user_message)

    # 3. Pré-processamento
    clean_text = normalize_text(user_message)

    # 4. NLP: intenção, emoção, entidades
    intent = intent_detector.predict_intent(clean_text)
    emotion = emotion_analyzer.analyze(clean_text)
    entities = ner_extractor.extract(user_message) # Manter NER financeiro por enquanto

    # 5. Busca semântica (RAG)
    docs = searcher.search(clean_text, top_k=3)
    context = "\n\n".join([d["text"] for d in docs])

    # 6. Memória + contexto
    history = memory.get_history(session_id)
    history_text = "\n".join([f"{m['role']}: {m['message']}" for m in history[-5:]])

    # 7. Monta prompt para o LLM usando o template do tema
    prompt = prompt_template.format(
        history_text=history_text,
        context=context,
        intent=intent['intent'],
        intent_confidence=intent['confidence'],
        emotion_sentiment=emotion['sentiment'],
        emotion_label=emotion['emotions'][0]['label'],
        entities=entities,
        user_message=user_message # Adicionado para referência no prompt
    )
    
    # 8. Decisão de escalonamento
    if decider.should_escalate(session_id, intent, emotion):
        response_text = "Sinto muito, não consigo resolver seu problema. Vou te transferir para um atendente humano."
    else:
        # 9. Geração de resposta com LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
        )
        response_text = response.choices[0].message.content

    # 10. Armazenar resposta do assistente
    memory.add_message(session_id, "assistant", response_text)

    return {
        "response": response_text,
        "intent": intent,
        "emotion": emotion,
        "entities": entities,
        "context": docs
    }
