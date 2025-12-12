from flask import Flask, render_template, jsonify, send_file, session
import subprocess
import threading
import os
import time
import uuid
from datetime import datetime
import sys
import json

app = Flask(__name__)
app.secret_key = 'clave_secreta_prueba_tecnica'

# Obtener el directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUTS_DIR = os.path.join(BASE_DIR, 'outputs')

# Rutas completas a los archivos
FILE_PATHS = {
    'parte_a': os.path.join(OUTPUTS_DIR, 'Pad_Imp_limpio.csv'),
    'parte_b': os.path.join(OUTPUTS_DIR, 'Immex_con_RFC.csv')
}

# Estado global de los procesos
process_status = {
    'parte_a': {'running': False, 'progress': 0, 'message': '', 'file_path': FILE_PATHS['parte_a']},
    'parte_b': {'running': False, 'progress': 0, 'message': '', 'file_path': FILE_PATHS['parte_b']}
}

def run_parte_a():
    """Ejecuta la Parte A en segundo plano"""
    global process_status
    process_id = 'parte_a'
    
    try:
        process_status[process_id]['running'] = True
        process_status[process_id]['message'] = 'Iniciando descarga del PDF...'
        process_status[process_id]['progress'] = 10
        
        # Importar y ejecutar módulo
        from scripts.parte_a import main as parte_a_main
        process_status[process_id]['message'] = 'Procesando PDF...'
        process_status[process_id]['progress'] = 30
        
        # Ejecutar proceso
        df = parte_a_main()  # Tu función existente
        
        process_status[process_id]['message'] = 'Guardando resultados...'
        process_status[process_id]['progress'] = 80
        
        # Verificar que el archivo se creó
        if os.path.exists(FILE_PATHS['parte_a']):
            process_status[process_id]['message'] = 'Proceso completado'
            process_status[process_id]['progress'] = 100
            process_status[process_id]['file_path'] = FILE_PATHS['parte_a']
        else:
            process_status[process_id]['message'] = 'Proceso terminado, pero no se encontró el archivo'
            process_status[process_id]['progress'] = 0
        
    except Exception as e:
        process_status[process_id]['message'] = f'Error: {str(e)}'
        process_status[process_id]['progress'] = 0
    finally:
        time.sleep(1)
        process_status[process_id]['running'] = False

def run_parte_b():
    """Ejecuta la Parte B en segundo plano"""
    global process_status
    process_id = 'parte_b'
    
    try:
        process_status[process_id]['running'] = True
        process_status[process_id]['message'] = 'Descargando IMMEX...'
        process_status[process_id]['progress'] = 20
        
        from scripts.parte_b import main as parte_b_main
        process_status[process_id]['message'] = 'Realizando cruce de datos...'
        process_status[process_id]['progress'] = 50
        
        df = parte_b_main()
        
        process_status[process_id]['message'] = 'Asignando RFCs...'
        process_status[process_id]['progress'] = 80
        
        # Verificar que el archivo se creó
        if os.path.exists(FILE_PATHS['parte_b']):
            process_status[process_id]['message'] = 'Proceso completado'
            process_status[process_id]['progress'] = 100
            process_status[process_id]['file_path'] = FILE_PATHS['parte_b']
        else:
            process_status[process_id]['message'] = 'Proceso terminó pero archivo no encontrado'
            process_status[process_id]['progress'] = 0
        
    except Exception as e:
        process_status[process_id]['message'] = f'Error: {str(e)}'
        process_status[process_id]['progress'] = 0
    finally:
        time.sleep(1)
        process_status[process_id]['running'] = False

#Rutas del backend

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/status/<process_id>')
def get_status(process_id):
    """Obtener estado del proceso"""
    if process_id in process_status:
        return jsonify(process_status[process_id])
    return jsonify({'error': 'Proceso no encontrado'}), 404

@app.route('/api/run/<process_id>', methods=['POST'])
def run_process(process_id):
    """Iniciar un proceso"""
    if process_id not in process_status:
        return jsonify({'error': 'Proceso no válido'}), 400
    
    if process_status[process_id]['running']:
        return jsonify({'error': 'El proceso ya está en ejecución'}), 409
    
    # Reiniciar estado
    process_status[process_id] = {
        'running': True, 
        'progress': 0, 
        'message': 'Iniciando...',
        'file_path': FILE_PATHS[process_id]
    }
    
    # Ejecutar en segundo plano
    if process_id == 'parte_a':
        thread = threading.Thread(target=run_parte_a)
    elif process_id == 'parte_b':
        thread = threading.Thread(target=run_parte_b)
    
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': f'Proceso {process_id} iniciado'})

@app.route('/api/download/<process_id>')
def download_file(process_id):
    """Descargar archivo generado"""
    if process_id not in FILE_PATHS:
        return "Proceso no encontrado", 404
    
    file_path = FILE_PATHS[process_id]
    
    if not os.path.exists(file_path):
        return "Archivo no disponible. Ejecuta el proceso primero.", 404
    
    filename = os.path.basename(file_path)
    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype='text/csv'
    )

@app.route('/api/files/exist')
def check_files():
    """Verificar si los archivos ya existen"""
    files = {
        'parte_a': os.path.exists(FILE_PATHS['parte_a']),
        'parte_b': os.path.exists(FILE_PATHS['parte_b'])
    }
    return jsonify(files)

if __name__ == '__main__':
    app.run(debug=True, port=5000)