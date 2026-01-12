import matplotlib.pyplot as plt
import numpy as np

def guardar_graficas(senal, filtrada, fft_orig, fft_filt, freqs, ruta_salida):
    """
    Genera y guarda una imagen PNG comparando las señales en Tiempo y Frecuencia.
    Útil para el reporte final o exportación de resultados.
    """
    # Crear figura con tamaño definido (ancho, alto en pulgadas)
    plt.figure(figsize=(10, 8))
    
    # 1. Subplot Superior: Dominio del Tiempo
    # Comparamos la forma de onda superpuesta para ver la reducción de ruido
    plt.subplot(2, 1, 1)
    plt.plot(senal, label='Original', alpha=0.6)
    plt.plot(filtrada, label='Filtrada', alpha=0.6, color='orange')
    plt.title('Dominio del Tiempo (Amplitud vs Tiempo)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2. Subplot Inferior: Dominio de la Frecuencia (Espectro)
    plt.subplot(2, 1, 2)
    
    # Máscara de visualización para limpiar la gráfica:
    # - freqs > 0: Ignoramos frecuencias negativas (por simetría hermitiana de la FFT de señales reales).
    # - freqs < 8000: Hacemos "zoom" a la banda audible principal (0-8kHz) donde suele estar la voz/música.
    mask = (freqs > 0) & (freqs < 8000)
    
    # Graficamos la Magnitud (np.abs) del espectro
    plt.plot(freqs[mask], np.abs(fft_orig[mask]), label='Espectro Original', alpha=0.6)
    plt.plot(freqs[mask], np.abs(fft_filt[mask]), label='Espectro Filtrado', color='red', linestyle='--')
    
    plt.title('Dominio de la Frecuencia (Magnitud vs Hz)')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Ajuste final y guardado
    plt.tight_layout() # Ajusta automáticamente los márgenes para que no se encimen etiquetas
    plt.savefig(ruta_salida)
    plt.close() # IMPORTANTE: Cierra la figura para liberar memoria RAM