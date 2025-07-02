# ner_extractor.py
import spacy
from typing import List, Dict

class FinanceEntityExtractor:
    def __init__(self, model_name="pt_core_news_sm"):
        self.nlp = spacy.load(model_name)

    def extract(self, text: str) -> List[Dict]:
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        return entities
