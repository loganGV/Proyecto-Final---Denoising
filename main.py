import os
import numpy as np
from src.file_io import cargar_audio, guardar_audio
from src.dsp import calcular_fft, aplicar_filtro_pasa_bajas, reconstruir_senal
from src.visualization import plot_analisis_espectral, plot_comparacion_tiempo

def main():
    print("\n=== PROYECTO: Denoising de Audio con FFT ===")
    print("Materia: Matemáticas Avanzadas para la Ingeniería")
    
    # ---------------------------------------------------------
    # 1. CONFIGURACIÓN Y CARGA
    # ---------------------------------------------------------
    # Definimos la ruta del archivo. Busca 'prueba.wav' en assets/audio_samples/
    archivo_input = os.path.join('assets', 'audio_samples', 'prueba.wav')
    
    print(f"\n[1/5] Cargando archivo: {archivo_input}...")
    fs, senal, error = cargar_audio(archivo_input)
    
    if error:
        print(f"❌ ERROR: {error}")
        print("Tip: Asegúrate de que el archivo 'prueba.wav' esté en la carpeta 'assets/audio_samples/'")
        return

    print(f"   -> Éxito: Fs={fs}Hz, Muestras={len(senal)}")

    # ---------------------------------------------------------
    # 2. ANÁLISIS ESPECTRAL (FFT) - SEÑAL ORIGINAL
    # ---------------------------------------------------------
    print("\n[2/5] Calculando FFT de la señal original...")
    
    # Vector de tiempo para gráficas
    N = len(senal)
    tiempo = np.linspace(0, N/fs, N)
    
    # Cálculo de FFT
    freqs, espectro = calcular_fft(senal, fs)
    
    # Graficar estado original
    print("   -> Generando gráfica: '1_original.png'")
    plot_analisis_espectral(tiempo, senal, freqs, espectro, "1_original.png")

    # ---------------------------------------------------------
    # 3. FILTRADO EN FRECUENCIA
    # ---------------------------------------------------------
    # Frecuencia de Corte: Frecuencias mayores a esto serán eliminadas.
    # AJUSTE: 4000 Hz es estándar para voz. Bájalo a 2000 o 1000 si sigue habiendo ruido agudo.
    FC_CORTE = 4000 
    print(f"\n[3/5] Aplicando Filtro Pasa-Bajas (Corte: {FC_CORTE} Hz)...")
    
    espectro_filt = aplicar_filtro_pasa_bajas(espectro, freqs, FC_CORTE)
    
    # ---------------------------------------------------------
    # 4. RECONSTRUCCIÓN (IFFT)
    # ---------------------------------------------------------
    print("\n[4/5] Reconstruyendo señal en el tiempo (IFFT)...")
    senal_limpia = reconstruir_senal(espectro_filt)
    
    # Graficar espectro filtrado (para ver el corte)
    print("   -> Generando gráfica: '2_filtrado.png'")
    plot_analisis_espectral(tiempo, senal_limpia, freqs, espectro_filt, "2_filtrado.png")
    
    # Graficar comparación visual
    print("   -> Generando gráfica: '3_comparacion_time.png'")
    plot_comparacion_tiempo(tiempo, senal, senal_limpia, "3_comparacion_time.png")

    # ---------------------------------------------------------
    # 5. GUARDADO DE RESULTADOS
    # ---------------------------------------------------------
    ruta_salida = os.path.join('results', 'cleaned_audio', 'resultado_limpio.wav')
    print(f"\n[5/5] Guardando audio procesado en: {ruta_salida}...")
    
    exito = guardar_audio(ruta_salida, fs, senal_limpia)
    
    if exito:
        print("\n✅ ¡PROCESO FINALIZADO CON ÉXITO!")
        print("   - Revisa la carpeta 'results/plots' para ver las gráficas.")
        print("   - Escucha 'results/cleaned_audio/resultado_limpio.wav' para verificar el audio.")
    else:
        print("\n❌ Hubo un error al guardar el archivo.")

if __name__ == "__main__":
    # Crear carpetas necesarias si no existen
    os.makedirs(os.path.join('results', 'cleaned_audio'), exist_ok=True)
    os.makedirs(os.path.join('results', 'plots'), exist_ok=True)
    
    main()
