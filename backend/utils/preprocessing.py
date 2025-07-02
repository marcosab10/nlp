# utils/preprocessing.py
import re
import unicodedata

def normalize_text(text: str) -> str:
    # Remove acentuação
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    # Remove caracteres especiais
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    # Espaços duplicados
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()
