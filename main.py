import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from scipy.io import wavfile
import pygame

# Importación de módulos del proyecto (DSP, I/O y Gráficas)
from src.file_io import cargar_audio
from src.dsp import aplicar_filtro_fft, validar_parseval, calcular_metricas

class DenoisingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DSP Studio - Proyecto Final Ingeniería")
        self.root.geometry("1280x880")
        
        # Configuración de pesos para responsive design
        root.columnconfigure(1, weight=1); root.rowconfigure(0, weight=1)

        # Inicialización del motor de audio (Pygame Mixer)
        try: 
            # Buffer reducido (2048) para minimizar latencia
            pygame.mixer.pre_init(44100, -16, 1, 2048)
            pygame.mixer.init()
        except Exception as e:
            print(f"Advertencia: No se pudo iniciar el motor de audio. {e}")
        
        # Variables de estado y datos de la señal
        self.ruta, self.fs, self.duracion = "", 0, 0
        self.senal_orig, self.senal_filt = None, None
        
        # Variables de control de reproducción
        self.reproducir = False
        self.offset_t = 0.0       
        self.alpha_val = 0.8      
        self.fuente_var = tk.StringVar(value="original")
        
        # Cache para optimización de renderizado
        self.linea_t, self.linea_f, self.datos_dsp_cache = None, None, None
        
        # Rutas de archivos temporales para el buffer de reproducción
        self.path_tmp_orig = os.path.abspath(".tmp_orig.wav")
        self.path_tmp_filt = os.path.abspath(".tmp_filt.wav")

        # --- DEFINICIÓN DE PANELES (Layout) ---
        p_izq = ttk.Frame(root, padding=15, width=340)
        p_izq.grid(row=0, column=0, sticky="nsew")
        p_izq.pack_propagate(False) 
        
        p_der = ttk.Frame(root, padding=10)
        p_der.grid(row=0, column=1, sticky="nsew")

        # --- CONTROLES DE USUARIO (Panel Izquierdo) ---
        
        # 1. Sección de Carga
        ttk.Label(p_izq, text="1. ARCHIVO DE ENTRADA", font="Arial 10 bold").pack(anchor="w")
        ttk.Button(p_izq, text="📂 Cargar Audio (.wav)", command=self.cargar).pack(fill="x", pady=5)
        self.lbl_file = ttk.Label(p_izq, text="Ningún archivo cargado", foreground="gray")
        self.lbl_file.pack(anchor="w", pady=(0, 15))

        # 2. Parámetros del Filtro
        ttk.Label(p_izq, text="2. DISEÑO DE FILTRO", font="Arial 10 bold").pack(anchor="w")
        
        ttk.Label(p_izq, text="Tipo de Filtro:").pack(anchor="w")
        self.cb_tipo = ttk.Combobox(p_izq, values=["Pasa-Bajas (LowPass)", "Pasa-Altas (HighPass)"], state="readonly")
        self.cb_tipo.current(0)
        self.cb_tipo.pack(fill="x", pady=(0, 5))

        ttk.Label(p_izq, text="Frecuencia de Corte (Hz):").pack(anchor="w")
        self.ent_freq = ttk.Entry(p_izq); self.ent_freq.insert(0, "3000"); self.ent_freq.pack(fill="x")
        self.lbl_nyquist = ttk.Label(p_izq, text="(Rango válido: Cargar audio)", font="Arial 8", foreground="#666")
        self.lbl_nyquist.pack(anchor="w", pady=(0, 5))

        # Ajuste visual (Opacidad)
        ttk.Label(p_izq, text="Opacidad de Gráfica (%):").pack(anchor="w")
        fr_alpha = ttk.Frame(p_izq); fr_alpha.pack(fill="x", pady=(0, 15))
        self.ent_alpha = ttk.Entry(fr_alpha); self.ent_alpha.insert(0, "80")
        self.ent_alpha.pack(side="left", fill="x", expand=True)
        self.ent_alpha.bind('<Return>', lambda e: self.set_alpha())
        ttk.Button(fr_alpha, text="Set", width=5, command=self.set_alpha).pack(side="right", padx=5)

        # 3. Botón de Ejecución DSP
        ttk.Label(p_izq, text="3. PROCESAMIENTO", font="Arial 10 bold").pack(anchor="w")
        ttk.Button(p_izq, text="⚙️ Calcular FFT y Filtrar", command=self.procesar).pack(fill="x", pady=5)

        # 4. Control de Reproducción
        fr_play = ttk.LabelFrame(p_izq, text="4. REPRODUCCIÓN", padding=10); fr_play.pack(fill="x", pady=15)
        
        fr_rad = ttk.Frame(fr_play); fr_rad.pack(fill="x")
        ttk.Radiobutton(fr_rad, text="Original", variable=self.fuente_var, value="original", command=self.cambiar_fuente).pack(side="left")
        self.rad_filt = ttk.Radiobutton(fr_rad, text="Filtrado", variable=self.fuente_var, value="filtrado", command=self.cambiar_fuente, state="disabled")
        self.rad_filt.pack(side="right")

        fr_ctrl = ttk.Frame(fr_play); fr_ctrl.pack(fill="x", pady=5)
        self.btn_play = ttk.Button(fr_ctrl, text="▶️", width=5, command=self.toggle_play, state="disabled")
        self.btn_play.pack(side="left")
        self.lbl_t_act = ttk.Label(fr_ctrl, text="0:00"); self.lbl_t_act.pack(side="left", padx=5)
        self.lbl_t_tot = ttk.Label(fr_ctrl, text="/ 0:00"); self.lbl_t_tot.pack(side="right")

        self.slider_t = ttk.Scale(fr_play, from_=0, to=1, orient="horizontal"); self.slider_t.pack(fill="x", pady=5)
        self.slider_t.bind("<ButtonRelease-1>", self.seek)
        self.slider_t.bind("<ButtonPress-1>", lambda e: setattr(self, 'actualizando_slider', True))

        # 5. Resultados Numéricos
        self.btn_save = ttk.Button(p_izq, text="💾 Exportar Resultados", command=self.guardar, state="disabled")
        self.btn_save.pack(fill="x")
        ttk.Label(p_izq, text="VALIDACIÓN MATEMÁTICA:", font="Arial 10 bold").pack(anchor="w", pady=(15, 2))
        self.txt_res = tk.Text(p_izq, height=9, bg="#f8f8f8", font=("Consolas", 11)); self.txt_res.pack(fill="both", expand=True)

        # --- ÁREA DE GRÁFICAS (Matplotlib) ---
        self.fig = Figure(figsize=(5, 5), dpi=100, constrained_layout=True)
        self.ax1, self.ax2 = self.fig.subplots(2, 1) 
        self.canvas = FigureCanvasTkAgg(self.fig, master=p_der)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        NavigationToolbar2Tk(self.canvas, p_der).pack(side="bottom", fill="x")
        self.reset_plots()

    # =========================================================
    # LÓGICA DEL SISTEMA (BACKEND)
    # =========================================================
    
    def cargar(self):
        """Gestiona la carga del archivo, normalización y preparación de la UI."""
        ruta = filedialog.askopenfilename(filetypes=[("WAV Audio", "*.wav")])
        if not ruta: return
        self.detener_audio()
        
        self.ruta, self.lbl_file["text"] = ruta, os.path.basename(ruta)
        
        # Llamada a módulo I/O
        self.fs, self.senal_orig, err = cargar_audio(ruta)
        if err: return messagebox.showerror("Error de Carga", err)

        # Configuración de límites según Teorema de Muestreo (Nyquist)
        self.duracion = len(self.senal_orig) / self.fs
        nyquist = int(self.fs/2)
        self.lbl_nyquist.config(text=f"(Máx: {nyquist} Hz)") 
        self.lbl_t_tot.config(text=f"/ {self.fmt_t(self.duracion)}")
        self.slider_t.config(to=self.duracion, value=0)
        
        # Guardado temporal para reproducción
        self.guardar_wav(self.senal_orig, self.path_tmp_orig)
        self.senal_filt = None
        self.reset_ui_state()
        self.cambiar_fuente()
        self.plot_full()

    def procesar(self):
        """
        Orquesta el procesamiento digital de señales:
        1. FFT -> 2. Máscara de Filtro -> 3. IFFT -> 4. Validación Parseval
        """
        if self.senal_orig is None: return messagebox.showwarning("Atención", "Debe cargar un audio primero.")
        try:
            corte = float(self.ent_freq.get())
            if not (0 < corte < self.fs/2): raise ValueError
        except: return messagebox.showerror("Error", f"Frecuencia inválida (Debe ser > 0 y < {int(self.fs/2)} Hz).")

        tipo_seleccionado = "lowpass" if "LowPass" in self.cb_tipo.get() else "highpass"

        self.detener_audio()
        
        # --- PASO 1, 2 y 3: FFT, Filtrado e IFFT ---
        self.senal_filt, fft_o, fft_f, f = aplicar_filtro_fft(
            self.senal_orig, self.fs, corte, tipo_filtro=tipo_seleccionado
        )
        self.datos_dsp_cache = (fft_o, fft_f, f)
        
        # --- PASO 4: Validación y Métricas ---
        mse, snr = calcular_metricas(self.senal_orig, self.senal_filt)
        et, ef = validar_parseval(self.senal_orig, fft_o)
        
        # Reporte de resultados
        self.txt_res.delete(1.0, tk.END)
        self.txt_res.insert(tk.END, f"Filtro: {tipo_seleccionado.upper()} @ {int(corte)} Hz\n")
        self.txt_res.insert(tk.END, f"SNR: {snr:.2f} dB | MSE: {mse:.5f}\n")
        self.txt_res.insert(tk.END, f"Teorema de Parseval (Energía):\n Tiempo:     {et:.2f}\n Frecuencia: {ef:.2f}")
        
        # Actualización de UI
        self.plot_full()
        self.guardar_wav(self.senal_filt, self.path_tmp_filt)
        self.rad_filt.config(state="normal"); self.btn_save.config(state="normal")
        self.fuente_var.set("filtrado"); self.cambiar_fuente()

    def set_alpha(self):
        """Actualiza la visualización sin recalcular la FFT."""
        try:
            self.alpha_val = float(self.ent_alpha.get()) / 100.0
            if not (0 <= self.alpha_val <= 1): raise ValueError
            if self.linea_t: self.linea_t.set_alpha(self.alpha_val)
            if self.linea_f: self.linea_f.set_alpha(self.alpha_val)
            self.canvas.draw_idle()
        except: messagebox.showerror("Error", "La opacidad debe estar entre 0 y 100.")

    def plot_full(self):
        """Genera las gráficas de dominio del tiempo y frecuencia."""
        self.ax1.clear(); self.ax2.clear()
        t = np.arange(len(self.senal_orig)) / self.fs
        
        # Dominio del Tiempo
        self.ax1.plot(t, self.senal_orig, color='silver', label='Original')
        if self.senal_filt is not None:
            self.linea_t, = self.ax1.plot(t, self.senal_filt, color='#007acc', alpha=self.alpha_val, label='Filtrada')
        
        # Dominio de la Frecuencia
        if self.datos_dsp_cache:
            fft_o, fft_f, f = self.datos_dsp_cache
            # Visualización optimizada (Zoom a frecuencias relevantes)
            try: lim = max(2000, int(float(self.ent_freq.get())) * 3)
            except: lim = 10000
            m = (f > 0) & (f < lim)
            
            self.ax2.plot(f[m], np.abs(fft_o[m]), color='silver', label='Original')
            self.linea_f, = self.ax2.plot(f[m], np.abs(fft_f[m]), color='#d62728', ls='--', alpha=self.alpha_val, label='Filtrada')
            self.ax2.legend(fontsize=8)

        self.config_ax(self.ax1, "Dominio del Tiempo", "Tiempo (s)", "Amplitud")
        self.config_ax(self.ax2, "Espectro de Frecuencia (Magnitud)", "Frecuencia (Hz)", "Magnitud")
        self.canvas.draw()

    # --- FUNCIONES AUXILIARES Y AUDIO ---
    
    def toggle_play(self):
        """Controlador de estado Play/Pause."""
        if not pygame.mixer.music.get_busy() and not self.reproducir: 
            self.cambiar_fuente()
            
        if self.reproducir: 
            pygame.mixer.music.pause()
            self.btn_play.config(text="▶️")
        else:
            if not pygame.mixer.music.get_busy(): 
                pygame.mixer.music.play(start=self.offset_t)
            else: 
                pygame.mixer.music.unpause()
            self.btn_play.config(text="⏸️")
            self.update_bar() 
        
        self.reproducir = not self.reproducir

    def update_bar(self):
        """Sincronización del slider con la reproducción de audio."""
        if self.reproducir and pygame.mixer.music.get_busy():
            if not getattr(self, 'actualizando_slider', False):
                current_pos_sec = pygame.mixer.music.get_pos() / 1000.0
                t = self.offset_t + current_pos_sec
                
                if t > self.duracion: 
                    self.detener_audio()
                else: 
                    self.slider_t.set(t)
                    self.lbl_t_act.config(text=self.fmt_t(t))
            
            self.root.after(50, self.update_bar)
        elif self.reproducir: 
            self.detener_audio() 

    def seek(self, e):
        """Salto temporal en la reproducción."""
        self.actualizando_slider = False
        self.offset_t = self.slider_t.get()
        self.lbl_t_act.config(text=self.fmt_t(self.offset_t))
        if self.reproducir: 
            pygame.mixer.music.play(start=self.offset_t)

    def guardar(self):
        """Exportación de archivos finales."""
        carpeta_results = os.path.abspath("results")
        if not os.path.exists(carpeta_results): os.makedirs(carpeta_results)
        
        ruta = filedialog.asksaveasfilename(
            initialdir=carpeta_results,
            defaultextension=".wav", 
            filetypes=[("WAV Audio", "*.wav")]
        )
        if ruta:
            self.guardar_wav(self.senal_filt, ruta, norm_out=True) 
            self.fig.savefig(os.path.splitext(ruta)[0] + ".png")
            messagebox.showinfo("Proceso Completado", "Audio y gráficas guardados correctamente.")

    def reset_ui_state(self):
        self.rad_filt.config(state="disabled"); self.fuente_var.set("original")
        self.btn_play.config(state="normal"); self.btn_save.config(state="disabled")
        self.txt_res.delete(1.0, tk.END); self.txt_res.insert(tk.END, "Archivo cargado. Listo para procesar.")

    def detener_audio(self):
        pygame.mixer.music.stop()
        self.reproducir = False
        self.offset_t = 0
        self.btn_play.config(text="▶️")
        self.slider_t.set(0)
        self.lbl_t_act.config(text="0:00")
    
    def cambiar_fuente(self):
        self.detener_audio()
        p = self.path_tmp_orig if self.fuente_var.get() == "original" else self.path_tmp_filt
        if os.path.exists(p): 
            try: pygame.mixer.music.load(p)
            except Exception as e: print(f"Error cargando buffer de audio: {e}")

    def guardar_wav(self, s, p, norm_out=False):
        """Escritura de archivo WAV con control de clipping."""
        mx = np.max(np.abs(s))
        if norm_out: wavfile.write(p, self.fs, (s/mx if mx>0 else s).astype(np.float32))
        else: wavfile.write(p, self.fs, ((s/mx if mx>0 else s)*32767).astype(np.int16))

    def config_ax(self, ax, tit, xl, yl):
        ax.set_title(tit); ax.set_xlabel(xl); ax.set_ylabel(yl); ax.legend(fontsize=8); ax.grid(alpha=0.3)
    
    def reset_plots(self): 
        self.ax1.clear(); self.ax2.clear()
        self.config_ax(self.ax1,"Dominio del Tiempo","","")
        self.config_ax(self.ax2,"Espectro de Frecuencia","","")
        self.canvas.draw()
        
    def fmt_t(self, s): return f"{int(s//60)}:{int(s%60):02d}"
    
    def __del__(self): 
        try: os.remove(self.path_tmp_orig); os.remove(self.path_tmp_filt)
        except: pass

if __name__ == "__main__":
    root = tk.Tk(); app = DenoisingApp(root); root.mainloop()