Guía de Ejecución

1. Clonar el repositorio

git clone https://github.com/ClaireRupikaRamode/Prueba-Tecnica-Prodensa-2025.git
cd Prueba-Tecnica-Prodensa-2025


2. Crear entorno virtual (de preferencia)

# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate


3. Instalar dependencias (forma automatizada)

(Automaticamente)
pip install -r requirements.txt

(Manualmente)
pip install --upgrade pip
pip install requests pdfplumber pandas numpy thefuzz flask flask-cors tqdm


4. Ejecutar Parte A por separado (Opcional)

python scripts/parte_a.py


5. Ejecutar Parte B por separado (Opcional)

python scripts/parte_b.py


6. Ejecutar Parte C (Vista Web)

python scripts/parte_c.py

abrir en el navegador: http://127.0.0.1:5000


Vista Web (Parte C)

La aplicación web permite:

    - Ejecutar Parte A y Parte B desde botones

    - Ver progreso en tiempo real con barras animadas

    - Descargar archivos CSV generados
