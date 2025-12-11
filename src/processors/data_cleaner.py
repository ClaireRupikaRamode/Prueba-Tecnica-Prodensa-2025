import pandas as pd
import unicodedata
import re
from thefuzz import fuzz  # Para fuzzy matching

def normalize_text(text):
    """Esta función limpia y normaliza un texto para comparación."""
    if not isinstance(text, str):
        return ""
    # Se eliminan acentos (si los hay)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

    # Se eliminan signos de puntuación y espacios extra
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Se eliminan términos corporativos comunes:
    corporate_terms = {'sa', 'de', 'cv', 'rl', 'sapi', 'sc', 'inc', 'llc'}
    words = text.split()
    filtered_words = [w for w in words if w not in corporate_terms]
    text = ' '.join(filtered_words)
    return text

def find_best_match(query, choices, threshold=80):
    """Esta función encuentra la mejor coincidencia aproximada para un nombre entre una lista."""
    best_score = 0
    best_match = None
    for choice in choices:
        # Se usa un ratio de similitud (de 0 a 100)
        score = fuzz.token_sort_ratio(query, choice)
        if score > best_score and score >= threshold:
            best_score = score
            best_match = choice
    return best_match, best_score