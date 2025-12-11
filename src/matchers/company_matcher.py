import pandas as pd
import os
import sys

# Se agrega el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ahora se importan los módulos
from processors.data_cleaner import normalize_text, find_best_match

def merge_immex_with_rfc(immex_df, padron_df):
    """ Esta función cruza el directorio IMMEX con el padrón para asignar RFC."""
    # Se crea una columna de nombre normalizado en ambos DataFrames
    padron_df['NOMBRE_NORM'] = padron_df['NOMBRE'].apply(normalize_text)
    immex_df['RAZON_SOCIAL_NORM'] = immex_df['RAZÓN_SOCIAL'].apply(normalize_text)

    # Se crea un diccionario {nombre_normalizado: rfc} para búsquedas rápidas
    padron_dict = pd.Series(padron_df['RFC'].values, index=padron_df['NOMBRE_NORM']).to_dict()

    # Para cada empresa en IMMEX, se busca la mejor coincidencia en el padrón
    matched_rfcs = []
    confidence_scores = []

    for immex_name_norm in immex_df['RAZON_SOCIAL_NORM']:
        # Primero se intenta buscar una coincidencia exacta en el nombre normalizado
        if immex_name_norm in padron_dict:
            matched_rfcs.append(padron_dict[immex_name_norm])
            confidence_scores.append(100)  # Coincidencia exacta
        else:
            # Si no hay exacta, se realiza un fuzzy matching contra todas las opciones del padrón
            best_match_norm, best_score = find_best_match(
                immex_name_norm,
                list(padron_dict.keys()),
                threshold=85  # Ajuste para el umbral de fuzzy matching
            )
            if best_match_norm:
                matched_rfcs.append(padron_dict[best_match_norm])
                confidence_scores.append(best_score)
            else:
                matched_rfcs.append(None)  # No se encontró coincidencia
                confidence_scores.append(0)

    # Se añaden resultados al DataFrame IMMEX
    immex_df['RFC'] = matched_rfcs
    immex_df['CONFIANZA_CRUCE'] = confidence_scores

    # Se concatenan NÚMERO_IMMEX y AÑO_IMMEX
    if 'NÚMERO_IMMEX' in immex_df.columns and 'AÑO_IMMEX' in immex_df.columns:
        immex_df['IMMEX_COMPLETO'] = immex_df['NÚMERO_IMMEX'].astype(str) + '-' + immex_df['AÑO_IMMEX'].astype(str)

    return immex_df