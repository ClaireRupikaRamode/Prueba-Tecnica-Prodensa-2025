import pdfplumber
import pandas as pd
import re

def extract_table_from_pdf(pdf_path):
    """Esta función extrae y limpia la tabla del PDF del padrón."""
    import pdfplumber
    import pandas as pd
    import re

    all_rows = []
    # Se sigue un patrón para identificar una fila válida: Número/ID, RFC, Nombre 
    # ([\d,]+) = uno o más dígitos, incluyendo comas que separen cifras grandes (ID) 
    # \s+ = uno o más espacios 
    # ([A-Z&Ñ0-9]{12,13}) = RFC 
    # \s+ = más espacios 
    # (.+)$') = todo lo demás es el nombre
    pattern = re.compile(r'^([\d,]+)\s+([A-Z&Ñ0-9]{12,13})\s+(.+)$')

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                # Filtros básicos de líneas 'no-dato'
                if not line or 'Página' in line or 'Padrón' in line or 'Registros Activos' in line:
                    continue

                match = pattern.match(line)
                if match:
                    # Extraemos el ID con comas, RFC y Nombre
                    id_num_with_comma, rfc, nombre = match.groups()
                    # Se eliminan las comas del ID para tener un número limpio en el CSV
                    id_num = id_num_with_comma.replace(',', '')
                    all_rows.append({'ID': id_num, 'RFC': rfc, 'NOMBRE': nombre})
                else:
                    # Se verifica qué lineas no se están capturando
                    if len(all_rows) > 990 and len(all_rows) < 1010:
                        print("Pág {page_num}, Línea no capturada: '{line}'")

    #Se crea el DataFrame
    df = pd.DataFrame(all_rows, columns=['ID', 'RFC', 'NOMBRE'])
    df = df.drop_duplicates()
    return df

def clean_padron_data(df):
    """Limpieza adicional del DataFrame."""
    # Se eliminan espacios extra en los nombres y RFC
    df['NOMBRE'] = df['NOMBRE'].str.strip()
    df['RFC'] = df['RFC'].str.strip()
    # Se convierte el ID a numérico (de ser necesario)
    df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
    # Se ordena por ID
    df = df.sort_values('ID').reset_index(drop=True)
    return df