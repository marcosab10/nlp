# sentiment_emotion.py
from transformers import pipeline

class EmotionAnalyzer:
    def __init__(self):
        self.sentiment_pipe = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
        self.emotion_pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=3)

    def analyze(self, text: str):
        sentiment_result = self.sentiment_pipe(text)[0]
        emotion_result = self.emotion_pipe(text)[0]
        return {
            "sentiment": sentiment_result["label"],
            "sentiment_score": round(sentiment_result["score"], 3),
            "emotions": [
                {"label": e["label"], "score": round(e["score"], 3)}
                for e in emotion_result
            ]
        }
