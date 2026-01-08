import os
import numpy as np
from scipy.io import wavfile

def cargar_audio(ruta_relativa):
    """
    Carga un archivo .wav, convierte a mono y normaliza a rango [-1, 1].
    """
    # Verificamos si existe el archivo
    if not os.path.exists(ruta_relativa):
        return None, None, f"Error: El archivo '{ruta_relativa}' no existe."

    try:
        # Leemos el archivo usando scipy
        fs, data = wavfile.read(ruta_relativa)
        
        # 1. Conversión a Mono: Si tiene 2 canales, promediamos
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
            
        # 2. Normalización: Convertir a float y dividir por el máximo absoluto
        # Esto es vital para procesar la señal sin saturación
        data = data.astype(np.float32)
        max_val = np.max(np.abs(data))
        
        if max_val > 0:
            data = data / max_val
            
        return fs, data, None

    except Exception as e:
        return None, None, f"Excepción al leer audio: {str(e)}"

def guardar_audio(ruta_destino, fs, data):
    """
    Guarda la señal procesada en un archivo .wav (formato PCM 16-bit).
    """
    try:
        # Asegurar que los datos no excedan [-1, 1] antes de guardar
        data = np.clip(data, -1.0, 1.0)
        
        # Convertir float32 a int16 para formato WAV estándar
        data_int16 = np.int16(data * 32767)
        
        wavfile.write(ruta_destino, fs, data_int16)
        print(f"-> Archivo guardado exitosamente en: {ruta_destino}")
        return True
    except Exception as e:
        print(f"Error al guardar audio: {e}")
        return False