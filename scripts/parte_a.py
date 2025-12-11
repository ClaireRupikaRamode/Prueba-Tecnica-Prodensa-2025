import sys
import os

# Se agrega el directorio raíz del proyecto al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Ahora se importan los módulos
from src.downloaders.sat_downloader import pdf_downloader
from src.processors.pdf_processor import extract_table_from_pdf, clean_padron_data

def main():
    print("Procesando el archivo")
    # Se descarga el PDF
    pdf_path = pdf_downloader()
    # Se procesa y se limpia
    print("Extrayendo y limpiando datos del PDF, por favor espere...")
    df = extract_table_from_pdf(pdf_path)
    df = clean_padron_data(df)
    # Se guarda el resultado
    output_path = "outputs/Pad_Imp_limpio.csv"
    os.makedirs("outputs", exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig') # Encoding para abrir en Excel
    #print("Padrón limpio guardado en: data/raw/Pad_Imp_limpio.csv")
    print(f"Padrón limpio guardado")
    return df

if __name__ == "__main__":
    main()