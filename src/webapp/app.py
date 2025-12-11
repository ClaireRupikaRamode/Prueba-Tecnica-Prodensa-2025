from flask import Flask, render_template, send_file, jsonify
import os
import subprocess
import threading

app = Flask(__name__)

# Ruta principal: Muestra la página con botones
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para descargar el Padrón
@app.route('/download/padron')
def download_padron():
    file_path = "outputs/padron_importadores_limpio.csv"
    # Asegúrate de que el archivo exista. Si no, podrías generarlo aquí.
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Archivo no encontrado. Ejecuta primero el procesamiento.", 404

# Ruta para descargar IMMEX con RFC
@app.route('/download/immex')
def download_immex():
    file_path = "outputs/immex_con_rfc.csv"
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "Archivo no encontrado. Ejecuta primero el procesamiento.", 404

# (OPCIONAL) Ruta para ejecutar el procesamiento completo desde la web
@app.route('/run-process')
def run_process():
    def run_script():
        # Ejecuta los scripts de las partes A y B
        subprocess.run(['python', 'scripts/parte_a.py'])
        subprocess.run(['python', 'scripts/parte_b.py'])
    # Ejecuta en un hilo separado para no bloquear la respuesta
    thread = threading.Thread(target=run_script)
    thread.start()
    return jsonify({"status": "Procesamiento iniciado en segundo plano."})

if __name__ == '__main__':
    app.run(debug=True)