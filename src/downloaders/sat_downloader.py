import requests
import os

def pdf_downloader(output_path="data/raw/Pad_Imp.pdf"):
    """Esta función se encarga de descargar el PDF del padrón de importadores desde la página oficial del SAT."""
    url = "https://www.sat.gob.mx/minisitio/PadronImportadoresExportadores/documentos/Pad_Imp.pdf"
    # User-Agent para simular un navegador
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()  # Error si la descarga falla

    # Asegura que exista el directorio
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Guarda el archivo
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"PDF descargado en: {output_path}")
    return output_path