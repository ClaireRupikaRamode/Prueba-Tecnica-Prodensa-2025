import requests
import os

def download_immex_excel(output_path="data/raw/directorio_immex.xlsx"):
    """ Esta función descarga el archivo Excel del Directorio IMMEX desde un enlace directo."""
    url = "https://www.snice.gob.mx/~oracle/SNICE_DOCS/IMMEX_OCTUBRE_2025-DIRECTORIO_20251110-20251110.xlsx"
    
    # User-Agent para simular un navegador
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()  # Error si la descarga falla

    # Asegura que exista el directorio
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Iniciando descarga desde: {url}")
    

    # Guarda el archivo
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    #print(f"Excel descargado en: {output_path}")
    print(f"Excel descargado")
    return output_path