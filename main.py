import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
# Importamos la función de nuestro módulo recién creado
from src.file_io import cargar_audio

def main():
    print("=== Denoising de Audio con FFT ===")
    
    # Ruta al archivo de prueba (asegúrate de tener uno aquí)
    archivo_input = os.path.join('assets', 'prueba.wav')
    
    print(f"Intentando cargar: {archivo_input}...")
    
    # Llamamos al módulo file_io
    fs, senal, error = cargar_audio(archivo_input)
    
    if error:
        print(error)
        print("IMPORTANTE: Recuerda poner un archivo 'prueba.wav' en la carpeta assets/")
    else:
        print("\n¡Carga Exitosa!")
        print(f" - Frecuencia de muestreo (fs): {fs} Hz")
        print(f" - Muestras totales: {len(senal)}")
        print(f" - Duración: {len(senal)/fs:.2f} segundos")
        print(" - Preprocesamiento: Mono y Normalizado [OK]")

if __name__ == "__main__":
    # Creamos las carpetas de resultados automáticamente si no existen
    os.makedirs(os.path.join('results', 'cleaned_audio'), exist_ok=True)
    os.makedirs(os.path.join('results', 'plots'), exist_ok=True)
    
    main()