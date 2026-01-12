import matplotlib.pyplot as plt
import numpy as np
import os

def plot_analisis_espectral(t, senal, freqs, espectro, nombre_salida="analisis.png"):
    """
    Genera una figura con dos subgráficas:
    1. Señal en el dominio del tiempo.
    2. Magnitud del espectro en el dominio de la frecuencia.
    
    Args:
        t (np.array): Eje de tiempo.
        senal (np.array): Amplitud de la señal.
        freqs (np.array): Eje de frecuencias.
        espectro (np.array): Resultado de la FFT (complejo).
        nombre_salida (str): Nombre del archivo .png a guardar.
    """
    plt.figure(figsize=(10, 8))
    
    # --- Gráfica 1: Dominio del Tiempo ---
    plt.subplot(2, 1, 1)
    plt.plot(t, senal, color='#1f77b4', alpha=0.8) # Azul
    plt.title("Dominio del Tiempo")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.grid(True, alpha=0.3)
    
    # --- Gráfica 2: Dominio de la Frecuencia (Magnitud) ---
    plt.subplot(2, 1, 2)
    # Calculamos la magnitud: |X[k]| = sqrt(Re^2 + Im^2)
    magnitud = np.abs(espectro)
    
    plt.plot(freqs, magnitud, color='#d62728', alpha=0.8) # Rojo
    plt.title("Dominio de la Frecuencia (Espectro de Magnitud)")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud |X(f)|")
    plt.grid(True, alpha=0.3)
    
    # Ajuste visual para evitar superposiciones
    plt.tight_layout()
    
    # Guardar en la carpeta de resultados
    ruta_guardado = os.path.join('results', 'plots', nombre_salida)
    plt.savefig(ruta_guardado)
    print(f"   -> Gráfica guardada: {ruta_guardado}")
    plt.close() # Importante: cerrar para liberar memoria

def plot_comparacion_tiempo(t, senal_orig, senal_filt, nombre_salida="comparacion.png"):
    """
    Grafica la señal original y la filtrada superpuestas para comparar.
    """
    plt.figure(figsize=(12, 5))
    
    # Graficar Original (Fondo gris)
    plt.plot(t, senal_orig, label='Original (Ruido)', color='gray', alpha=0.5)
    
    # Graficar Filtrada (Frente verde)
    plt.plot(t, senal_filt, label='Filtrada (Limpia)', color='green', alpha=0.8, linewidth=1.5)
    
    plt.title("Comparación: Antes vs. Después del Filtrado")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    ruta_guardado = os.path.join('results', 'plots', nombre_salida)
    plt.savefig(ruta_guardado)
    print(f"   -> Comparación guardada: {ruta_guardado}")
    plt.close()
