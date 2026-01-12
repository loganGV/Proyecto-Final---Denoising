import numpy as np

def aplicar_filtro_fft(senal, fs, frecuencia_corte=4000, tipo_filtro='lowpass'):
    """
    Calcula FFT, aplica filtro (pasa-bajas o pasa-altas) y reconstruye (IFFT).
    tipo_filtro: 'lowpass' (elimina agudos) o 'highpass' (elimina graves).
    """
    N = len(senal)
    
    # 1. FFT: Transformada de la señal al dominio de la frecuencia
    fft_original = np.fft.fft(senal)
    freqs = np.fft.fftfreq(N, d=1/fs)
    
    # 2. Diseño de la Máscara (Filtro ideal)
    if tipo_filtro == 'lowpass':
        # Pasa-bajas: Mantiene frecuencias menores al corte
        mascara = np.abs(freqs) < frecuencia_corte
    elif tipo_filtro == 'highpass':
        # Pasa-altas: Mantiene frecuencias mayores al corte
        mascara = np.abs(freqs) > frecuencia_corte
    else:
        mascara = np.ones_like(freqs, dtype=bool)
    
    # 3. Filtrado: Multiplicación en frecuencia
    fft_filtrada = fft_original * mascara
    
    # 4. IFFT: Reconstrucción al dominio del tiempo
    senal_reconstruida = np.fft.ifft(fft_filtrada)
    
    # Devolvemos la parte real (la imaginaria es residual numérico)
    return np.real(senal_reconstruida), fft_original, fft_filtrada, freqs

def validar_parseval(senal_tiempo, senal_frecuencia):
    """
    Valida que la energía se conserve entre dominios (Teorema de Parseval).
    """
    N = len(senal_tiempo)
    energia_t = np.sum(np.abs(senal_tiempo)**2)
    energia_f = np.sum(np.abs(senal_frecuencia)**2) / N
    return energia_t, energia_f

def calcular_metricas(original, procesada):
    """
    Calcula MSE (Error Cuadrático Medio) y SNR (Relación Señal-Ruido).
    """
    # Ajuste de longitud por seguridad
    min_len = min(len(original), len(procesada))
    orig = original[:min_len]
    proc = procesada[:min_len]

    mse = np.mean((orig - proc) ** 2)
    
    ruido = orig - proc
    potencia_ruido = np.mean(ruido ** 2)
    potencia_senal = np.mean(orig ** 2)
    
    if potencia_ruido == 0:
        return mse, 100 
        
    snr = 10 * np.log10(potencia_senal / potencia_ruido)
    return mse, snr