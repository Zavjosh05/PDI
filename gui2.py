#importacion de librerias
import numpy as np
import cv2

#importacion de librerias visuales
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, ttk
import os

#importacion de clases
from OperacionesLogicas2 import * 
from Ruido import * 
from Filtros import *
from FiltrosSegmentacion import * 
from ProcesadorImagen import * 


class InterfazProcesadorImagenes(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Procesador de Imágenes")
        self.geometry("1200x800")
        
        self.procesador = ProcesadorImagen()
        self.operaciones_logicas = OperacionesLogicas2()
     
        self.ruido = Ruido()
        self.filtro = Filtros()
        self.filtros_segmentacion = FiltrosSegmentacion()
        
        self.imagen_actual = None
        self.ruta_imagen_actual = None
        self.ruta_imagen1_logica = None
        self.ruta_imagen2_logica = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Panel principal con mejor distribución
        panel_principal = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        panel_principal.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo para botones - ancho ajustado para mejor visualización
        panel_izquierdo = ttk.Frame(panel_principal, width=250)
        panel_principal.add(panel_izquierdo, weight=1)  # Peso 1 para panel izquierdo
        
        # Panel derecho para mostrar imágenes - con más espacio
        panel_derecho = ttk.Frame(panel_principal)
        panel_principal.add(panel_derecho, weight=3)  # Peso 3 para panel derecho (más grande)
        
        # Notebook para pestañas con estilo mejorado
        style = ttk.Style()
        style.configure("TNotebook", tabposition='n')  # Pestañas en la parte superior
        self.notebook = ttk.Notebook(panel_derecho)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear pestañas con más espacio interno
        tab_basico = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_basico, text="Procesamiento Básico")
        
        tab_logicas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_logicas, text="Operaciones Lógicas")
        
        tab_ruido = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_ruido, text="Ruido y Filtros")

        tab_segmentacion = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_segmentacion, text="Segmentación")
        
        tab_histogramas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab_histogramas, text="Histogramas")
        
        # Configurar panel de visualización para cada pestaña con scrollbars
        # Panel básico con scroll
        frame_scroll_basico = ttk.Frame(tab_basico)
        frame_scroll_basico.pack(fill=tk.BOTH, expand=True)
        
        canvas_basico = tk.Canvas(frame_scroll_basico)
        scrollbar_basico = ttk.Scrollbar(frame_scroll_basico, orient="vertical", command=canvas_basico.yview)
        self.panel_basico = ttk.Frame(canvas_basico)
        
        self.panel_basico.bind("<Configure>", lambda e: canvas_basico.configure(scrollregion=canvas_basico.bbox("all")))
        canvas_basico.create_window((0, 0), window=self.panel_basico, anchor="nw")
        canvas_basico.configure(yscrollcommand=scrollbar_basico.set)
        
        canvas_basico.pack(side="left", fill="both", expand=True)
        scrollbar_basico.pack(side="right", fill="y")
        
        # Configuración similar para los otros paneles
        # Panel lógicas con scroll
        frame_scroll_logicas = ttk.Frame(tab_logicas)
        frame_scroll_logicas.pack(fill=tk.BOTH, expand=True)
        
        canvas_logicas = tk.Canvas(frame_scroll_logicas)
        scrollbar_logicas = ttk.Scrollbar(frame_scroll_logicas, orient="vertical", command=canvas_logicas.yview)
        self.panel_logicas = ttk.Frame(canvas_logicas)
        
        self.panel_logicas.bind("<Configure>", lambda e: canvas_logicas.configure(scrollregion=canvas_logicas.bbox("all")))
        canvas_logicas.create_window((0, 0), window=self.panel_logicas, anchor="nw")
        canvas_logicas.configure(yscrollcommand=scrollbar_logicas.set)
        
        canvas_logicas.pack(side="left", fill="both", expand=True)
        scrollbar_logicas.pack(side="right", fill="y")
        
        # Panel ruido con scroll
        frame_scroll_ruido = ttk.Frame(tab_ruido)
        frame_scroll_ruido.pack(fill=tk.BOTH, expand=True)
        
        canvas_ruido = tk.Canvas(frame_scroll_ruido)
        scrollbar_ruido = ttk.Scrollbar(frame_scroll_ruido, orient="vertical", command=canvas_ruido.yview)
        self.panel_ruido = ttk.Frame(canvas_ruido)
        
        self.panel_ruido.bind("<Configure>", lambda e: canvas_ruido.configure(scrollregion=canvas_ruido.bbox("all")))
        canvas_ruido.create_window((0, 0), window=self.panel_ruido, anchor="nw")
        canvas_ruido.configure(yscrollcommand=scrollbar_ruido.set)
        
        canvas_ruido.pack(side="left", fill="both", expand=True)
        scrollbar_ruido.pack(side="right", fill="y")
        
        # Panel histogramas con scroll
        frame_scroll_histogramas = ttk.Frame(tab_histogramas)
        frame_scroll_histogramas.pack(fill=tk.BOTH, expand=True)
        
        canvas_histogramas = tk.Canvas(frame_scroll_histogramas)
        scrollbar_histogramas = ttk.Scrollbar(frame_scroll_histogramas, orient="vertical", command=canvas_histogramas.yview)
        self.panel_histogramas = ttk.Frame(canvas_histogramas)
        
        self.panel_histogramas.bind("<Configure>", lambda e: canvas_histogramas.configure(scrollregion=canvas_histogramas.bbox("all")))
        canvas_histogramas.create_window((0, 0), window=self.panel_histogramas, anchor="nw")
        canvas_histogramas.configure(yscrollcommand=scrollbar_histogramas.set)
        
        canvas_histogramas.pack(side="left", fill="both", expand=True)
        scrollbar_histogramas.pack(side="right", fill="y")
        
        # Crear marco con scrollbar para panel de botones
        canvas_izquierdo = tk.Canvas(panel_izquierdo)
        scrollbar_izquierdo = ttk.Scrollbar(panel_izquierdo, orient="vertical", command=canvas_izquierdo.yview)
        panel_botones = ttk.Frame(canvas_izquierdo)
        
        panel_botones.bind("<Configure>", lambda e: canvas_izquierdo.configure(scrollregion=canvas_izquierdo.bbox("all")))
        canvas_izquierdo.create_window((0, 0), window=panel_botones, anchor="nw")
        canvas_izquierdo.configure(yscrollcommand=scrollbar_izquierdo.set)
        
        canvas_izquierdo.pack(side="left", fill="both", expand=True)
        scrollbar_izquierdo.pack(side="right", fill="y")
        
        # Configurar botones en panel izquierdo con mejor espaciado
        # Sección de carga de imágenes
        ttk.Label(panel_botones, text="Cargar Imágenes", font=("Arial", 12, "bold")).pack(pady=(20, 10), padx=5)
        ttk.Button(panel_botones, text="Cargar Imagen Principal", command=self.cargar_imagen_principal).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Cargar Imagen 1 (Op. Lógicas)", command=self.cargar_imagen1_logica).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Cargar Imagen 2 (Op. Lógicas)", command=self.cargar_imagen2_logica).pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Separator(panel_botones, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        # Sección de procesamiento básico
        ttk.Label(panel_botones, text="Procesamiento Básico", font=("Arial", 12, "bold")).pack(pady=(10, 5), padx=5)
        ttk.Button(panel_botones, text="Convertir a Escala de Grises", command=self.convertir_a_grises).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Aplicar Umbral", command=self.aplicar_umbral).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Ecualización Hipercúbica", command=self.ecualizacion_hipercubica).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Operaciones Aritméticas", command=self.aplicar_operaciones_aritmeticas).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Calcular Histogramas", command=self.calcular_histogramas).pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Separator(panel_botones, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        # Sección de operaciones lógicas
        ttk.Label(panel_botones, text="Operaciones Lógicas", font=("Arial", 12, "bold")).pack(pady=(10, 5), padx=5)
        ttk.Button(panel_botones, text="Aplicar Operaciones Lógicas", command=self.aplicar_operaciones_logicas).pack(fill=tk.X, padx=15, pady=5)
        ttk.Separator(panel_botones, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
         
        # Sección de ruido y filtros
        ttk.Label(panel_botones, text="Ruido y Filtros", font=("Arial", 12, "bold")).pack(pady=(10, 5), padx=5)
        ttk.Button(panel_botones, text="Agregar Ruido Sal y Pimienta", command=self.agregar_ruido_sal_pimienta).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Agregar Ruido Gaussiano", command=self.agregar_ruido_gaussiano).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Aplicar Filtro promediador", command=self.aplicar_filtro_promediador).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Aplicar Filtro Pesado", command=self.aplicar_filtro_pesado).pack(fill=tk.X, padx=15, pady=5)
        ttk.Button(panel_botones, text="Aplicar Filtro de Robert", command=self.aplicar_filtro_Robert).pack(fill=tk.X, padx=15, pady=10)


        ttk.Separator(panel_botones, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)
        
        # Sección de segmentación
        ttk.Label(panel_botones, text="Segmentación", font=("Arial", 12, "bold")).pack(pady=(10, 5), padx=5)
        ttk.Button(panel_botones, text="Segmentación por método de otsu", command=self.aplicar_filtro_otsu).pack(fill=tk.X, padx=15, pady=5)
        ttk.Separator(panel_botones, orient='horizontal').pack(fill=tk.X, padx=10, pady=15)

        # Botón para guardar la imagen actual con más destaque
        ttk.Label(panel_botones, text="Guardar Resultado", font=("Arial", 12, "bold")).pack(pady=(10, 5), padx=5)
        ttk.Button(panel_botones, text="Guardar Imagen Actual", 
                command=self.guardar_imagen_actual, 
                style="Accent.TButton").pack(fill=tk.X, padx=15, pady=10)
        
        # Definir estilo de botón especial para guardar
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))
    
    def cargar_imagen_principal(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        if ruta:
            self.ruta_imagen_actual = ruta
            imagen = self.procesador.cargar_imagen(ruta)
            self.ruido.cargar_imagen(ruta)
            if imagen is not None:
                self.imagen_actual = imagen
                self.mostrar_imagen(self.panel_basico, imagen, "Imagen Original")
                self.notebook.select(0)  # Cambiar a la pestaña de procesamiento básico
    
    def cargar_imagen1_logica(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        if ruta:
            self.ruta_imagen1_logica = ruta
            if self.ruta_imagen2_logica:
                self.operaciones_logicas.cargar_imagenes(self.ruta_imagen1_logica, self.ruta_imagen2_logica)
                self.mostrar_imagenes_logicas()
    
    def cargar_imagen2_logica(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        if ruta:
            self.ruta_imagen2_logica = ruta
            if self.ruta_imagen1_logica:
                self.operaciones_logicas.cargar_imagenes(self.ruta_imagen1_logica, self.ruta_imagen2_logica)
                self.mostrar_imagenes_logicas()

    def verificar_imagen_cargada(self):
        if self.procesador.imagen_original is None:
            self.mostrar_mensaje("Por favor cargue una imagen primero")
            return False
        return True

    def convertir_a_grises(self):
        if not self.verificar_imagen_cargada():
            return
        imagen_grises = self.procesador.convertir_a_grises()
        if imagen_grises is not None:
            self.imagen_actual = imagen_grises
            self.mostrar_imagen(self.panel_basico, imagen_grises, "Imagen en Escala de Grises")
            self.notebook.select(0)  # Cambiar a la pestaña de procesamiento básico
    
    def aplicar_umbral(self):
        if not self.verificar_imagen_cargada():
            return
        imagen_umbral = self.procesador.aplicar_umbral()
        if imagen_umbral is not None:
            self.imagen_actual = imagen_umbral
            self.mostrar_imagen(self.panel_basico, imagen_umbral, "Imagen Umbralizada")
            self.notebook.select(0)  # Cambiar a la pestaña de procesamiento básico
    
    def ecualizacion_hipercubica(self):
        if not self.verificar_imagen_cargada():
            return
        imagen_ecualizada = self.procesador.ecualizacion_hipercubica()
        if imagen_ecualizada is not None:
            self.imagen_actual = imagen_ecualizada
            self.mostrar_imagen(self.panel_basico, imagen_ecualizada, "Ecualización Hipercúbica")
            self.notebook.select(0)  # Cambiar a la pestaña de procesamiento básico
    
    def aplicar_operaciones_aritmeticas(self):
        if not self.verificar_imagen_cargada():
            return
        
        suma, resta, multiplicacion = self.procesador.aplicar_operaciones_aritmeticas()
        
        # Limpiar panel
        for widget in self.panel_basico.winfo_children():
            widget.destroy()
        
        # Crear un marco para contener las tres imágenes en fila
        frame = ttk.Frame(self.panel_basico)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Mostrar las tres imágenes
        if suma is not None:
            self.mostrar_imagen_frame(frame, suma, "Suma", 0, 0)
        if resta is not None:
            self.mostrar_imagen_frame(frame, resta, "Resta", 0, 1)
        if multiplicacion is not None:
            self.mostrar_imagen_frame(frame, multiplicacion, "Multiplicación", 0, 2)
        
        self.notebook.select(0)  # Cambiar a la pestaña de procesamiento básico
    
    def calcular_histogramas(self):
        if not self.verificar_imagen_cargada():
            return
        
        fig_gray, fig_color = self.procesador.calcular_histogramas()
        
        # Limpiar panel de histogramas
        for widget in self.panel_histogramas.winfo_children():
            widget.destroy()
        
        # Mostrar histogramas en la pestaña correspondiente
        if fig_gray is not None and fig_color is not None:
            frame_histogramas = ttk.Frame(self.panel_histogramas)
            frame_histogramas.pack(fill=tk.BOTH, expand=True)
            
            # Mostrar histograma en escala de grises
            canvas_gray = FigureCanvasTkAgg(fig_gray, master=frame_histogramas)
            canvas_gray.draw()
            canvas_gray.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
            
            # Mostrar histograma de color
            canvas_color = FigureCanvasTkAgg(fig_color, master=frame_histogramas)
            canvas_color.draw()
            canvas_color.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
            
            self.notebook.select(4)  # Cambiar a la pestaña de histogramas
    
    def aplicar_operaciones_logicas2(self):
        if self.ruta_imagen1_logica is None or self.ruta_imagen2_logica is None:
            self.mostrar_mensaje("Por favor cargue ambas imágenes para operaciones lógicas")
            return
        
        and_img, or_img, xor_img = self.operaciones_logicas.aplicar_operaciones_logicas()
        
        if and_img is not None and or_img is not None and xor_img is not None:
            # Limpiar panel
            for widget in self.panel_logicas.winfo_children():
                widget.destroy()
            
            # Crear un marco para contener las imágenes y resultados
            frame_logicas = ttk.Frame(self.panel_logicas)
            frame_logicas.pack(fill=tk.BOTH, expand=True)
            
            # Mostrar imágenes originales
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen1, "Imagen 1", 0, 0)
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen2, "Imagen 2", 0, 1)
            
            # Mostrar resultados de operaciones lógicas
            self.mostrar_imagen_frame(frame_logicas, and_img, "AND", 1, 0)
            self.mostrar_imagen_frame(frame_logicas, or_img, "OR", 1, 1)
            self.mostrar_imagen_frame(frame_logicas, xor_img, "XOR", 1, 2)
            
            self.notebook.select(1)  # Cambiar 
        return
    
    def aplicar_operaciones_logicas(self):
        if self.ruta_imagen1_logica is None or self.ruta_imagen2_logica is None:
            self.mostrar_mensaje("Por favor cargue ambas imágenes para operaciones lógicas")
            return
        
        and_img, or_img, xor_img = self.operaciones_logicas.aplicar_operaciones_logicas()
        
        if and_img is not None and or_img is not None and xor_img is not None:
            # Limpiar panel
            for widget in self.panel_logicas.winfo_children():
                widget.destroy()
            
            # Crear un marco para contener las imágenes y resultados
            frame_logicas = ttk.Frame(self.panel_logicas)
            frame_logicas.pack(fill=tk.BOTH, expand=True)
            
            # Mostrar imágenes originales
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen1, "Imagen 1", 0, 0)
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen2, "Imagen 2", 0, 1)
            
            # Mostrar resultados de operaciones lógicas
            self.mostrar_imagen_frame(frame_logicas, and_img, "AND", 1, 0)
            self.mostrar_imagen_frame(frame_logicas, or_img, "OR", 1, 1)
            self.mostrar_imagen_frame(frame_logicas, xor_img, "XOR", 1, 2)
            
            self.notebook.select(1)  # Cambiar a la pestaña de operaciones lógicas
    
    def agregar_ruido_sal_pimienta(self):
        if not self.verificar_imagen_cargada():
            return
        
        imagen_ruido = self.ruido.agregar_ruido_sal_pimienta()
        if imagen_ruido is not None:
            self.imagen_actual = imagen_ruido
            self.mostrar_imagen(self.panel_ruido, imagen_ruido, "Imagen con Ruido Sal y Pimienta")
            self.filtro.imagen_original = imagen_ruido  # Preparar para aplicar filtro
            self.notebook.select(2)  # Cambiar a la pestaña de ruido y filtros
    
    def agregar_ruido_gaussiano(self):
        if not self.verificar_imagen_cargada():
            return
        
        imagen_ruido = self.ruido.agregar_ruido_gaussiano()
        if imagen_ruido is not None:
            self.imagen_actual = imagen_ruido
            self.mostrar_imagen(self.panel_ruido, imagen_ruido, "Imagen con Ruido Gaussiano")
            self.filtro.imagen_original = imagen_ruido  # Preparar para aplicar filtro
            self.notebook.select(2)  # Cambiar a la pestaña de ruido y filtros

    def aplicar_filtro_promediador(self):
        print("shouldnt have called ")
        return
    

    def aplicar_filtro_pesado(self):
        if not self.verificar_imagen_cargada():
            return
        
        imagen_filtrada = self.filtro.filtro_pesado()
        if imagen_filtrada is not None:
            self.imagen_actual = imagen_filtrada
            
            # Mostrar imagen original con ruido y su versión filtrada
            for widget in self.panel_ruido.winfo_children():
                widget.destroy()
            
            frame_ruido = ttk.Frame(self.panel_ruido)
            frame_ruido.pack(fill=tk.BOTH, expand=True)
            
            self.mostrar_imagen_frame(frame_ruido, self.filtro.imagen_original, "Imagen con Ruido", 0, 0)
            self.mostrar_imagen_frame(frame_ruido, imagen_filtrada, "Imagen Filtrada", 0, 1)
            
            self.notebook.select(2)  # Cambiar a la pestaña de ruido y filtros
    
    #metodo que utiliza el boton 
    def aplicar_filtro_Robert(self):
        #banderilla
        
        self.filtros_segmentacion.imagen_original = self.imagen_actual 
        imagen_filtrada = self.filtros_segmentacion.filtro_Robert()
        if imagen_filtrada is not None:
            self.imagen_actual = imagen_filtrada
            
            # Mostrar imagen original con ruido y su versión filtrada
            for widget in self.panel_ruido.winfo_children():
                widget.destroy()
            
            frame_ruido = ttk.Frame(self.panel_ruido)
            frame_ruido.pack(fill=tk.BOTH, expand=True)
            
            self.mostrar_imagen_frame(frame_ruido, self.filtros_segmentacion.imagen_original, "Imagen convertida A gris ", 0, 0)
            self.mostrar_imagen_frame(frame_ruido, imagen_filtrada, "Imagen Filtro robert (Bordes)", 0, 1)
            
            self.notebook.select(2)  # Cambiar a la pestaña de segmentaciones

    def aplicar_filtro_otsu(self):
        self.filtros_segmentacion.imagen_original = self.imagen_actual 
        imagen_filtrada = self.filtros_segmentacion.filtro_otsu()
        if imagen_filtrada is not None:
            self.imagen_actual = imagen_filtrada
            
            # Mostrar imagen original y su versión filtrada
            for widget in self.panel_ruido.winfo_children():
                widget.destroy()
            
            frame_ruido = ttk.Frame(self.panel_ruido)
            frame_ruido.pack(fill=tk.BOTH, expand=True)
            
            self.mostrar_imagen_frame(frame_ruido, self.filtros_segmentacion.imagen_original, "Imagen convertida A gris ", 0, 0)
            self.mostrar_imagen_frame(frame_ruido, imagen_filtrada, "Segmentos obtenidos con otsu (umbralización)", 0, 1)
            
            self.notebook.select(3)  # Cambiar a la pestaña de segmentación
    
    def mostrar_imagenes_logicas(self):
        # Mostrar las imágenes seleccionadas para operaciones lógicas
        for widget in self.panel_logicas.winfo_children():
            widget.destroy()
        
        frame_logicas = ttk.Frame(self.panel_logicas)
        frame_logicas.pack(fill=tk.BOTH, expand=True)
        
        if self.operaciones_logicas.imagen1 is not None:
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen1, "Imagen 1", 0, 0)
        
        if self.operaciones_logicas.imagen2 is not None:
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen2, "Imagen 2", 0, 1)
        
        self.notebook.select(1)  # Cambiar a la pestaña de operaciones lógicas
    
    def guardar_imagen_actual(self):
        if self.imagen_actual is None:
            self.mostrar_mensaje("No hay imagen para guardar")
            return
        
        ruta = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[
            ("JPEG", "*.jpg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("Todos los archivos", "*.*")
        ])
        
        if ruta:
            cv2.imwrite(ruta, self.imagen_actual)
            self.mostrar_mensaje(f"Imagen guardada en {ruta}")
    
    def mostrar_imagen(self, panel, imagen, titulo):
        # Limpiar panel
        for widget in panel.winfo_children():
            widget.destroy()
        
        # Convertir imagen de OpenCV a formato RGB para Tkinter
        if len(imagen.shape) == 3:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        else:
            # Convertir imagen en escala de grises a RGB
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
        
        # Frame contenedor con borde para mejor visualización
        frame_contenedor = ttk.Frame(panel, borderwidth=2, relief="groove")
        frame_contenedor.pack(padx=20, pady=20, expand=True)
        
        # Crear una etiqueta para mostrar el título
        ttk.Label(frame_contenedor, text=titulo, font=("Arial", 12, "bold")).pack(pady=(10, 8))
        
        # Mostrar información de dimensiones
        altura, anchura = imagen_rgb.shape[:2]
        info_text = f"Dimensiones: {anchura}x{altura}"
        ttk.Label(frame_contenedor, text=info_text, font=("Arial", 10)).pack(pady=(0, 8))
        
        # Para imágenes grandes, redimensionar para ajustar a la ventana manteniendo la proporción
        max_width = 800  # Tamaño máximo para mostrar
        max_height = 600
        
        factor_width = max_width / anchura if anchura > max_width else 1
        factor_height = max_height / altura if altura > max_height else 1
        factor = min(factor_width, factor_height)
        
        if factor < 1:  # Solo redimensionar si es necesario
            nueva_anchura = int(anchura * factor)
            nueva_altura = int(altura * factor)
            imagen_redimensionada = cv2.resize(imagen_rgb, (nueva_anchura, nueva_altura))
        else:
            imagen_redimensionada = imagen_rgb
        
        # Mostrar la imagen en un lienzo
        from PIL import Image, ImageTk
        img = Image.fromarray(imagen_redimensionada)
        img_tk = ImageTk.PhotoImage(image=img)
        
        # Etiqueta para mostrar la imagen
        label_img = ttk.Label(frame_contenedor, image=img_tk)
        label_img.image = img_tk  # Mantener una referencia
        label_img.pack(padx=15, pady=15)
    
    def mostrar_imagen_frame(self, frame, imagen, titulo, fila, columna):
        # Convertir imagen de OpenCV a formato RGB para Tkinter
        if len(imagen.shape) == 3:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        else:
            # Convertir imagen en escala de grises a RGB
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
        
        # Crear subframe para cada imagen con borde para mejor visualización
        subframe = ttk.Frame(frame, borderwidth=2, relief="groove")
        subframe.grid(row=fila, column=columna, padx=15, pady=15, sticky="nsew")
        
        # Configurar expansión de la cuadrícula
        frame.grid_columnconfigure(columna, weight=1)
        frame.grid_rowconfigure(fila, weight=1)
        
        # Crear una etiqueta para mostrar el título con mejor estilo
        ttk.Label(subframe, text=titulo, font=("Arial", 11, "bold")).pack(pady=(8, 5))
        
        # Redimensionar imagen para mostrar miniaturas pero con mayor tamaño
        altura, anchura = imagen_rgb.shape[:2]
        factor = min(250 / anchura, 250 / altura)  # Tamaño aumentado de 200 a 250
        nueva_anchura = int(anchura * factor)
        nueva_altura = int(altura * factor)
        imagen_redimensionada = cv2.resize(imagen_rgb, (nueva_anchura, nueva_altura))
        
        # Mostrar la imagen en un lienzo
        from PIL import Image, ImageTk
        img = Image.fromarray(imagen_redimensionada)
        img_tk = ImageTk.PhotoImage(image=img)
        
        # Etiqueta para mostrar la imagen con padding
        label_img = ttk.Label(subframe, image=img_tk)
        label_img.image = img_tk  # Mantener una referencia
        label_img.pack(padx=10, pady=10)
        
        # Agregar información de dimensiones
        info_text = f"Dimensiones: {anchura}x{altura}"
        ttk.Label(subframe, text=info_text, font=("Arial", 9)).pack(pady=(0, 8))
    
    def mostrar_mensaje(self, mensaje):
        from tkinter import messagebox
        messagebox.showinfo("Información", mensaje)


if __name__ == "__main__":
    app = InterfazProcesadorImagenes()
    app.mainloop()