# intent_detector.py
from sentence_transformers import SentenceTransformer, util
import json
import torch

class IntentDetector:
    def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.model = SentenceTransformer(model_name)
        with open('nlp/intents.json', 'r', encoding='utf-8') as f:
            self.intents = json.load(f)
        self.intent_embeddings = {
            intent["name"]: self.model.encode(intent["examples"], convert_to_tensor=True)
            for intent in self.intents
        }

    def predict_intent(self, text: str):
        query_embedding = self.model.encode(text, convert_to_tensor=True)
        best_score = 0
        best_intent = "unknown"
        for intent, embeddings in self.intent_embeddings.items():
            cos_scores = util.cos_sim(query_embedding, embeddings)[0]
            score = torch.max(cos_scores).item()
            if score > best_score:
                best_score = score
                best_intent = intent
        return {"intent": best_intent, "confidence": round(best_score, 3)}
