import matplotlib.pyplot as plt
import numpy as np
import os

def plot_analisis_espectral(t, senal, freqs, espectro, nombre_salida="analisis_inicial.png"):
    """
    Genera una gráfica comparativa: Dominio del Tiempo vs. Frecuencia.
    Guarda la imagen en la carpeta results/plots/.
    """
    plt.figure(figsize=(12, 6))
    
    # --- Gráfica 1: Dominio del Tiempo ---
    plt.subplot(2, 1, 1)
    plt.plot(t, senal, color='blue', alpha=0.7)
    plt.title("Señal en el Dominio del Tiempo")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud Normalizada")
    plt.grid(True, alpha=0.3)
    
    # --- Gráfica 2: Dominio de la Frecuencia (Magnitud) ---
    plt.subplot(2, 1, 2)
    # Calculamos la magnitud: |X[k]|
    magnitud = np.abs(espectro)
    
    plt.plot(freqs, magnitud, color='red', alpha=0.7)
    plt.title("Espectro de Frecuencia (Magnitud FFT)")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud |X(f)|")
    plt.grid(True, alpha=0.3)
    
    # Ajustar límites para ver mejor (zoom en frecuencias audibles)
    # Opcional: limitar el eje X a la mitad positiva si se desea
    # plt.xlim(0, max(freqs)) 

    plt.tight_layout()
    
    # Guardar gráfica
    ruta_guardado = os.path.join('results', 'plots', nombre_salida)
    plt.savefig(ruta_guardado)
    print(f"-> Gráfica guardada en: {ruta_guardado}")
    plt.close() # Cerrar para liberar memoria

# ... (Mantén lo anterior)

def plot_comparacion_tiempo(t, senal_orig, senal_filt, nombre_salida="comparacion_tiempo.png"):
    """
    Grafica la señal original vs la filtrada superpuestas.
    """
    plt.figure(figsize=(12, 6))
    
    plt.plot(t, senal_orig, label='Original (Con Ruido)', color='lightgray', alpha=0.8)
    plt.plot(t, senal_filt, label='Filtrada (Limpia)', color='green', alpha=0.9)
    
    plt.title("Comparación en el Tiempo: Original vs Filtrada")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    ruta = os.path.join('results', 'plots', nombre_salida)
    plt.savefig(ruta)
    print(f"-> Gráfica comparativa guardada en: {ruta}")
    plt.close()
