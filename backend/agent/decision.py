# agent/decision.py
from typing import Dict

class EscalationDecider:
    def __init__(self, config: Dict = None):
        # Thresholds default
        self.config = config or {
            "emo_negativa": ["anger", "disgust", "fear"],
            "emo_score_min": 0.65,
            "sentiment_ruim": "NEGATIVE",
            "intencao_desconhecida": "unknown",
            "interacoes_sem_resposta": 3,
        }
        self.session_erro_count = {}

    def should_escalate(self, session_id: str, emotion_analysis: Dict, intent: str):
        emotions = emotion_analysis.get("emotions", [])
        negative_emotions = [
            emo for emo in emotions
            if emo["label"].lower() in self.config["emo_negativa"] and emo["score"] >= self.config["emo_score_min"]
        ]

        sentiment = emotion_analysis.get("sentiment", "").upper()
        is_sentiment_bad = sentiment == self.config["sentiment_ruim"]

        erro_count = self.session_erro_count.get(session_id, 0)

        if intent == self.config["intencao_desconhecida"]:
            erro_count += 1
        else:
            erro_count = 0  # zera contador se conseguiu responder

        self.session_erro_count[session_id] = erro_count

        if negative_emotions or is_sentiment_bad or erro_count >= self.config["interacoes_sem_resposta"]:
            return True

        return False
