# Denoising de Audio con FFT y Validación de Parseval

Este proyecto es una herramienta computacional desarrollada para la materia de **Matemáticas Avanzadas para la Ingeniería**.

## 📋 Descripción del Proyecto

Su objetivo principal es aplicar conceptos de análisis de Fourier para limpiar señales de audio y validar matemáticamente el proceso. La aplicación permite cargar archivos de audio, analizar su espectro de frecuencias mediante la Transformada Rápida de Fourier (FFT), aplicar filtros diseñados en el dominio de la frecuencia y reconstruir la señal limpia. Además, se verifica la conservación de la energía utilizando el **Teorema de Parseval**.

### Objetivos
* Aplicar explícitamente la **Serie/Transformada de Fourier** (DFT/FFT).
* Implementar filtrado en frecuencia (pasa-bajas, pasa-altas, pasa-banda, notch).
* Validar resultados numéricamente (MSE/SNR) y teóricamente (Parseval).
* Proveer una interfaz gráfica que facilite la visualización comparativa de señales en tiempo y frecuencia.

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
El código está desarrollado en Python. Para asegurar que el proyecto se ejecute correctamente en cualquier entorno, se requieren las siguientes librerías:

* NumPy
* SciPy
* Matplotlib
* Pygame

Python 3.8 o superior

## 🚀 Instalación y Ejecución
1. Obtención del código
Primero, asegúrese de tener Git instalado en su sistema verificando con `git --version`. Si no lo tiene, descárguelo desde git-scm.com.

Una vez listo, clone el repositorio:

git clone https://github.com/loganGV/Proyecto_Final_Denoising.git
cd Proyecto_Final_Denoising

2. Preparación del entorno
Se recomienda utilizar un entorno virtual. Instale las dependencias ejecutando el comando correspondiente a su sistema:

En Windows:
pip install -r requirements.txt

En macOS (Terminal):
pip3 install -r requirements.txt

Nota: Si por alguna razón el comando anterior falla al instalar Pygame, puede instalar dicha librería manualmente ejecutando `pip install pygame` (o `pip3 install pygame` en macOS). Si continúa dando un error use el siguiente comando: pip install pygame-ce (o  `pip3 install pygame-ce` en macOS).

3. Ejecución
Para iniciar la aplicación, ejecute el script principal:

En Windows:
python main.py

En macOS:
python3 main.py

Nota: La interfaz incluye controles de reproducción de audio. Asegúrese de contar con salida de audio activa en su equipo.

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

Datos: Los archivos de audio utilizados en assets/ son de uso libre.

## Proyecto desarrollado por :
	* Logan Gómez Valencia
	* Cesar Ulises Mendoza Gonzalez
	* Ari Ivan Leal Salguero
	* Carlos Fabian Paredes Diaz