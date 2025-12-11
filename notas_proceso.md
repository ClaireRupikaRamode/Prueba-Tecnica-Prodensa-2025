1. Primero crear un entorno virtual para el proyecto, para así mantener un control de las dependencias.
Ejecutando en la terminal:
///python -m venv venv
source venv/bin/activate #Ya que me encuentro en Linux
pip install --upgrade pip
pip install requests selenium webdriver-manager pdfplumber pymupdf PyPDF2 pandas numpy openpyxl thefuzz python-Levenshtein flask flask-cors python-dotenv tqdm

Para instalar las dependencias de forma automatizada basta con ejecutar:
///pip install -r requirements.txt

2. Luego crear la estructura del proyecto:
///Primero pensaba utilizar esta estructura básica:
Prueba_Tecnica/
| data/                # archivos de origen
├──  scripts/
|    ├── descargar.py
|    ├── pdf_a_csv.py
|    ├── immex_cruce.py
|    ├── utils.py
|    ├── app.py             # web view
|
├──  outputs/
|    ├── padrón.csv
|    ├── immex_rfc.csv

///Sin embargo, al momento de estar realizando la parte B, he decidido organizarme mejor y distribuirlo de una forma más profesional:
Prueba_Tecnica/
│
├── README.md                    # Instrucciones de ejecución
├── requirements.txt             # Dependencias necesarias
├── notas_proceso.md            # Mi proceso durante la prueba
│
├── src/                        # Código fuente dividido por secciones
│   ├── __init__.py
│   ├── downloaders/           # Descargas de archivos
│   │   ├── __init__.py
│   │   ├── sat_downloader.py
│   │   └── immex_downloader.py
│   │
│   ├── processors/            # Procesamiento y conversiones
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   └── data_cleaner.py
│   │
│   ├── matchers/              # Cruce de datos
│   │   ├── __init__.py
│   │   └── company_matcher.py
│   │
│   └── webapp/                # Vista web
│       ├── __init__.py
│       ├── app.py
│       └── templates/
│           └── index.html
|
├── scripts/                           #Ejecución directa de cada parte solicitada
│   ├── parte_a.py                     # Script Parte A
│   ├── parte_b.py                     # Script Parte B
│   └── parte_c.py                     # Script Parte C
│
├── data/                      # Datos crudos
│   ├── raw/                   # Archivos descargados sin cambios
│   └── inter/                 # Resultados intermedios
│
└──  outputs/                   # Resultados finales

Considero que la organización es una parte bastante importante en los proyectos y la considero indispensable antes, durante y después de la realización de un proyecto.

3. Decidí automatizar el proceso de descarga del archivo desde el portal del SAT con el script 'sat_downloader.py', bastando con ejecutarlo para recibir el PDF directamente en la carpeta 'data/raw', sin embargo, este código es solo una función que debe ser llamada por otro código, en este caso 'parte_a.py'

4. Lo siguiente es extraer todo el texto de las tablas que vienen en el PDF, así que haciendo uso de la libería pdfplumber se puede extraer todo el texto de cada página.

#Nota: Intenté realizarlo primero con la biblioteca 'camelot-py', sin embargo, esta no procesó correctamente los datos, generando al final un CSV con información mezclada.

Intenté muchas veces realizar la extracción de datos, sin embargo, siempre
se quedaba trabada la extracción hasta el 'ID 999', esto debido a que estaba utilizando como patrón de extracción lo siguiente:

///pattern = re.compile(r'^(\d+)\s+([A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3})\s+(.+)$')

Lo que causaba que al pasar de la cifra 999 se dejara de extraer datos, ya que el PDF separaba los ID al pasar de 1000 con una ',' haciendo que el script descartara todo lo que no fuera solamente un número, al final bastó hacer una pequeña modificación al patrón de extracción de la siguiente manera:

///pattern = re.compile(r'^([\d,]+)\s+([A-Z&Ñ0-9]{12,13})\s+(.+)$')

Con unas cuantas modificaciones no solo empezó a detectarse correctamente los ID en su totalidad para su extracción, si no que al cambiar la forma en la que se identifica el RFC y el nombre permite que no se lleguen a mezclar datos al recibir datos más complejos que no entren en las reglas que había colocado anteriormente.

Lo siguiente en esta función es filtrar los datos acorde a lo que no debe interpretarse como datos relevantes:

///if not line or 'Página' in line or 'Padrón' in line or 'Registros Activos' in line

Extraer el 

5. 