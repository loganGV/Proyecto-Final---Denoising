import numpy as np

def calcular_fft(senal, fs):
    """
    Calcula la FFT de una señal 1D.

    """
    N = len(senal)
    
    # 1. Calcular la FFT (Transformada Rápida de Fourier)
    # Numpy devuelve el resultado ordenado: [0, 1, ..., N/2-1, -N/2, ..., -1]
    espectro_complejo = np.fft.fft(senal)
    
    # 2. Calcular el eje de frecuencias correspondiente
    # np.fft.fftfreq genera las frecuencias asociadas a cada bin de la FFT
    frecuencias = np.fft.fftfreq(N, d=1/fs)
    
    # 3. Ordenar para visualización (shift)
    # Movemos las frecuencias negativas a la izquierda y positivas a la derecha
    # Esto hace que el 0 Hz quede en el centro, más fácil de entender gráficamente.
    frecuencias_shift = np.fft.fftshift(frecuencias)
    espectro_shift = np.fft.fftshift(espectro_complejo)
    
    return frecuencias_shift, espectro_shift

# ... (Mantén las importaciones y la función calcular_fft que ya tenías)

def aplicar_filtro_pasa_bajas(espectro_shift, frecuencias_shift, frecuencia_corte):
    """
    Aplica una máscara binaria (Filtro Ideal Pasa Bajas).
    Mantiene las frecuencias por debajo del corte y elimina las superiores.

    """
    # Creamos una copia para no modificar el original
    espectro_filtrado = espectro_shift.copy()
    
    # MÁSCARA DEL FILTRO:
    # Si el valor absoluto de la frecuencia es mayor al corte, lo volvemos 0.
    # Usamos abs() porque el espectro tiene parte negativa y positiva simétricas.
    mask = np.abs(frecuencias_shift) > frecuencia_corte
    
    # Aplicamos la máscara (hacemos cero lo que cumpla la condición)
    espectro_filtrado[mask] = 0
    
    return espectro_filtrado

def reconstruir_senal(espectro_shift):
    """
    Recupera la señal en el tiempo usando la IFFT.
    
    """
    # 1. Des-centrar el espectro (inverse shift)
    # Necesario porque la IFFT de numpy espera el orden estándar (0 al inicio),
    # pero nosotros lo teníamos centrado para graficar.
    espectro_ishift = np.fft.ifftshift(espectro_shift)
    
    # 2. Calcular IFFT
    senal_reconstruida = np.fft.ifft(espectro_ishift)
    
    # 3. Tomar solo la parte Real
    # Matemáticamente, si el espectro es simétrico, la parte imaginaria debería ser 0.
    # Por errores numéricos pequeños, tomamos solo la parte real.
    return np.real(senal_reconstruida)

