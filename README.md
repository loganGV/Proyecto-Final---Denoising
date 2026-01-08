# Denoising de Audio con FFT y Validación de Parseval

Este proyecto es una herramienta computacional desarrollada para la materia de **Matemáticas Avanzadas para la Ingeniería**. Su objetivo principal es aplicar conceptos de análisis de Fourier para limpiar señales de audio y validar matemáticamente el proceso.

## 📋 Descripción del Proyecto

La aplicación permite cargar archivos de audio, analizar su espectro de frecuencias mediante la Transformada Rápida de Fourier (FFT), aplicar filtros diseñados en el dominio de la frecuencia y reconstruir la señal limpia. Además, se verifica la conservación de la energía utilizando el **Teorema de Parseval**.

### Objetivos
* Aplicar explícitamente la **Serie/Transformada de Fourier** (DFT/FFT).
* Implementar filtrado en frecuencia (pasa-bajas, pasa-altas, pasa-banda, notch).
* Validar resultados numéricamente (MSE/SNR) y teóricamente (Parseval).

## 🗂 Estructura del Repositorio

El proyecto sigue una arquitectura modular para facilitar la escalabilidad y la revisión:

```
Denoising
├── assets/                  # Archivos de entrada (Audios .wav originales)
├── results/                 # Resultados generados (Audios limpios y Gráficas)
├── src/                     # Código fuente modular
│   ├── file_io.py           # Gestión de carga y guardado de archivos
│   ├── dsp.py               # Procesamiento Digital (FFT, Filtros, Parseval)
│   └── visualization.py     # Generación de gráficas comparativas
├── docs/                    # Documentación y Reporte Técnico
├── main.py                  # Script principal de ejecución
└── requirements.txt         # Dependencias del proyecto
```
## ⚙️ Requisitos Previos
El código está desarrollado en Python. Para asegurar que el proyecto se ejecute correctamente en cualquier entorno, se utilizan librerías estándar de cálculo y visualización.

Python 3.8 o superior

Librerías listadas en requirements.txt (NumPy, SciPy, Matplotlib)

## 🚀 Instalación y Ejecución
Sigue estos pasos para ejecutar el proyecto en tu máquina local:

1. Clonar el repositorio:
	git clone [https://github.com/TU_USUARIO/Denoising.git](https://github.com/TU_USUARIO/Denoising.git)
	cd Denoising

2. Instalar dependencias: Es recomendable usar un entorno virtual.
	pip install -r requirements.txt
	
3. Ejecutar la herramienta: Asegúrate de tener un archivo .wav en la carpeta assets/. Por defecto el script buscará assets/prueba.wav.
	python main.py
	
4. Verificar Resultados:
	* Los audios procesados se guardarán en results/cleaned_audio/.
	* Las gráficas comparativas (Tiempo/Frecuencia) se generarán en results/plots/.

🧪 Metodología Matemática

El núcleo del procesamiento se basa en:

1. Preprocesamiento: Normalización de la señal a rango [-1, 1] y conversión a mono.

2. Transformada (FFT): Conversión de la señal del dominio del tiempo al dominio de la frecuencia.

3. Filtrado: Aplicación de máscara binaria o función de transferencia H(f) sobre el espectro.

4. Reconstrucción (IFFT): Transformada inversa para recuperar la señal de audio.

5. Validación:

	* Teorema de Parseval: La energía total en el tiempo es igual a la energía total en la frecuencia.

📄 Licencia y Datos

Código: De uso libre para fines académicos.

Datos: Los archivos de audio utilizados en assets/ son [Indicar aquí si son grabaciones propias o citar fuente/licencia].

## Proyecto desarrollado por :
	* Logan Gómez Valencia
	* Cesar Ulises Mendoza Gonzalez
	* Ari Ivan Leal Salguero
	* Carlos Fabian Paredes Diaz