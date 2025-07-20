# sentiment_emotion.py
import os
import openai
from transformers import pipeline
from dotenv import load_dotenv

# Carregar variáveis de ambiente (caso não tenha sido carregado no main.py)
load_dotenv()

class EmotionAnalyzer:
    def __init__(self):
        self.sentiment_pipe = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
        self.emotion_pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=3)
        # Configuração do cliente OpenAI
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def translate_to_english(self, text: str) -> str:
        """Traduz texto de pt-BR para en-US usando OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a translator. Translate the user's input from Portuguese (Brazil) to English (US). Do not add any comments or explanations. Only provide the translation."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[❌] Erro ao traduzir texto: {e}")
            return text  # Em caso de erro, retorna o texto original

    def analyze(self, text: str):
        # Primeiro traduzir o texto para inglês
        english_text = self.translate_to_english(text)
        
        # Analisar o texto traduzido
        sentiment_result = self.sentiment_pipe(english_text)[0]
        emotion_result = self.emotion_pipe(english_text)[0]
        
        return {
            "sentiment": sentiment_result["label"],
            "sentiment_score": round(sentiment_result["score"], 3),
            "emotions": [
                {"label": e["label"], "score": round(e["score"], 3)}
                for e in emotion_result
            ]
        }
