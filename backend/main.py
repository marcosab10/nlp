# main.py
import os
import openai
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
async def read_root():
    return FileResponse('../frontend/index.html')

intent_detector = IntentDetector()
emotion_analyzer = EmotionAnalyzer()
ner_extractor = FinanceEntityExtractor()
searcher = RAGSearcher()
memory = ConversationMemory()
decider = EscalationDecider()

# 📥 Modelo da requisição
class ChatInput(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat_handler(input: ChatInput):
    session_id = input.session_id
    user_message = input.message

    # 1. Armazenar mensagem do usuário
    memory.add_message(session_id, "user", user_message)

    # 2. Pré-processamento
    clean_text = normalize_text(user_message)

    # 3. NLP: intenção, emoção, entidades
    intent = intent_detector.predict_intent(clean_text)
    emotion = emotion_analyzer.analyze(clean_text)
    entities = ner_extractor.extract(user_message)

    # 4. Busca semântica (RAG)
    docs = searcher.search(clean_text, top_k=3)
    context = "\n\n".join([d["text"] for d in docs])

    # 5. Memória + contexto
    history = memory.get_history(session_id)
    history_text = "\n".join([f"{m['role']}: {m['message']}" for m in history[-5:]])

    # 6. Monta prompt para o LLM
    prompt = f"""
    Você é um assistente bancário inteligente. Sua tarefa é responder às perguntas do cliente de forma clara, empática e precisa.

    **Contexto da Conversa:**
    {history_text}

    **Informações Relevantes (Base de Conhecimento):**
    {context}

    **Análise da Mensagem do Cliente:**
    - Intenção: {intent['intent']} (Confiança: {intent['confidence']})
    - Emoção: {emotion['sentiment']} ({emotion['emotions'][0]['label']})
    - Entidades: {entities}

    **Instruções:**
    1. Use o histórico e o contexto para dar uma resposta informada.
    2. Se a intenção for "desconhecida" ou a confiança for baixa, peça ao cliente para reformular a pergunta.
    3. Se a emoção for negativa (raiva, nojo), seja especialmente cuidadoso e empático.
    4. Responda diretamente à última mensagem do cliente: "{user_message}"
    """

    # 7. Geração de Resposta com OpenAI
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=250,
            temperature=0.7
        )
        response_text = completion.choices[0].message.content

    except Exception as e:
        response_text = "Desculpe, estou com dificuldades para processar sua solicitação no momento."
        print(f"Erro ao chamar a API da OpenAI: {e}")

    # 8. Armazenar resposta do assistente
    memory.add_message(session_id, "assistant", response_text)

    # 9. Decisão de escalonamento (opcional, pode ser expandido)
    escalate = decider.should_escalate(session_id, emotion, intent['intent'])

    # 10. Formatar e retornar a resposta
    return {
        "session_id": session_id,
        "response": response_text,
        "intent": intent,
        "emotion": emotion,
        "entities": entities,
        "escalate": escalate,
        "rag_context": context
    }
