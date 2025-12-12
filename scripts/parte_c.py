import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.webapp.app import app

def main():
    """Esta función ejecuta la aplicación web para la Parte C"""

    print("=" * 60)
    print("Iniciando aplicación web...")
    print("=" * 60)
    print("\nEsta aplicación permite:")
    print("   1. Ejecutar Parte A (PDF SAT → CSV)")
    print("   2. Ejecutar Parte B (IMMEX + RFC)")
    print("   3. Ver progreso en tiempo real")
    print("   4. Descargar archivos generados")
    print("\nPor favor, abra el navegador y acceda a la siguiente IP:")
    print("   → http://127.0.0.1:5000")
    print("\nLa aplicación se está iniciando...")
    print("   (Presione Ctrl+C para detener)\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == "__main__":
    main()