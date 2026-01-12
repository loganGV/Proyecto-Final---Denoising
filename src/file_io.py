import os
import numpy as np
from scipy.io import wavfile

def cargar_audio(ruta_relativa):
    """
    Carga un archivo .wav, lo convierte a mono y lo normaliza al rango [-1, 1].
    Retorna: fs (frecuencia), data (array numpy float32), error (str o None).
    """
    # Validación básica de existencia
    if not os.path.exists(ruta_relativa):
        return None, None, f"Error: El archivo '{ruta_relativa}' no existe."

    try:
        # Lectura cruda del archivo .wav
        fs, data = wavfile.read(ruta_relativa)
        
        # 1. Conversión a Mono:
        # Si la señal tiene más de 1 dimensión (es estéreo), promediamos los canales
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
            
        # 2. Normalización (Crucial para DSP):
        # Convertimos a float32 para tener precisión decimal en la FFT.
        # Dividimos por el máximo para escalar todo entre -1.0 y 1.0.
        data = data.astype(np.float32)
        max_val = np.max(np.abs(data))
        
        if max_val > 0:
            data = data / max_val
            
        return fs, data, None

    except Exception as e:
        return None, None, f"Excepción al leer audio: {str(e)}"

def guardar_audio(ruta_destino, fs, data):
    """
    Convierte la señal flotante de vuelta a PCM 16-bit y la guarda como .wav.
    """
    try:
        # 1. Clipping (Protección):
        # Aseguramos que ningún valor matemático exceda el rango [-1, 1]
        # para evitar distorsión digital severa (clipping) al convertir.
        data = np.clip(data, -1.0, 1.0)
        
        # 2. Conversión a Enteros (PCM 16-bit):
        # Multiplicamos por 32767 (2^15 - 1) para volver al formato estándar de audio.
        data_int16 = np.int16(data * 32767)
        
        wavfile.write(ruta_destino, fs, data_int16)
        print(f"-> Archivo guardado exitosamente en: {ruta_destino}")
        return True
    except Exception as e:
        print(f"Error al guardar audio: {e}")
        return False