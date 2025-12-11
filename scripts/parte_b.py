import pandas as pd
import os
import sys

# Se agrega el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ahora se importan los módulos
from src.downloaders.immex_downloader import download_immex_excel
from src.matchers.company_matcher import merge_immex_with_rfc

def main():
    # Se carga el padrón limpio (resultado de la Parte A)
    padron_path = "outputs/Pad_Imp_limpio.csv"
    padron_df = pd.read_csv(padron_path, dtype=str)  # Se lee todo como texto

    # Se descarga o carga el IMMEX
    immex_path = download_immex_excel()
    
    # Lectura del excel
    # Saltar las primeras 4 filas (0-3) y usar la fila 5 como encabezado
    immex_df = pd.read_excel(immex_path, dtype=str, skiprows=4)
    
    # Verificación
    print("\n=== DATAFRAME IMMEX CORREGIDO ===")
    print(f"Número de filas: {len(immex_df)}")
    print(f"Número de columnas: {len(immex_df.columns)}")
    print("\nNombre de las columnas:")
    for i, col in enumerate(immex_df.columns):
        print(f"  {i}: '{col}'")
    
    print("\nPrimeras 3 filas de datos REALES:")
    print(immex_df.head(3))
    # =======================================
    
    # Se realiza el cruce
    print("\nRealizando cruce aproximado de empresas...")
    result_df = merge_immex_with_rfc(immex_df, padron_df)
    
    # Se guarda el resultado
    output_path = "outputs/immex_con_rfc.csv"
    os.makedirs("outputs", exist_ok=True)
    result_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"IMMEX con RFC guardado en: {output_path}")
    
    # Estadísticas útiles para tus notas
    match_rate = (result_df['RFC'].notna().sum() / len(result_df)) * 100
    print(f"Tasa de coincidencia: {match_rate:.2f}%")
    
    # Mostrar algunos ejemplos de coincidencias
    print("\nEjemplos de primeras coincidencias")
    matched_samples = result_df[result_df['RFC'].notna()].head(5)
    for _, row in matched_samples.iterrows():
        print(f"• {row.get('RAZÓN_SOCIAL', 'Columna no encontrada')} → RFC: {row['RFC']} (Coinncidencia: {row.get('CONFIANZA_CRUCE', 'N/A')}%)")
    
    return result_df

if __name__ == "__main__":
    main()