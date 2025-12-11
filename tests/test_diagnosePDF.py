# Script para diagnosticar la estructura del PDF descargado
import pdfplumber
import re
from pathlib import Path

def analizar_paginas_pdf(pdf_path, paginas_analizar=10):
    """Analiza las primeras páginas para entender la estructura"""
    print(f"Analizando estructura del PDF: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num in range(min(paginas_analizar, len(pdf.pages))):
            page = pdf.pages[page_num]
            text = page.extract_text()
            
            print(f"\n{'='*60}")
            print(f"PÁGINA {page_num + 1}")
            print(f"{'='*60}")
            
            lines = text.split('\n')
            print(f"Total líneas en página: {len(lines)}")
            
            # Mostrar primeras y últimas líneas
            print("\nPrimeras 10 líneas:")
            for i, line in enumerate(lines[:10]):
                print(f"{i+1:3}: {line}")
            
            print("\nÚltimas 10 líneas:")
            for i, line in enumerate(lines[-10:]):
                print(f"{len(lines)-10+i+1:3}: {line}")
            
            # Buscar patrones
            print("\nBuscando patrones de registro...")
            for i, line in enumerate(lines):
                # Patrón simple: número al inicio
                if re.match(r'^\s*\d+', line.strip()):
                    print(f"Línea {i+1} parece registro: {line[:80]}...")
    
if __name__ == "__main__":
    pdf_path = Path("data/raw/Pad_Imp.pdf")
    analizar_paginas_pdf(pdf_path, paginas_analizar=5)