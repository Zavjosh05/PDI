import numpy as np
import cv2
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, ttk
import os
from PIL import Image, ImageTk
import sys

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
        self.canvas = None
        
        self.configurar_estilos()
        self.crear_interfaz()
    
    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("Header.TFrame", background="#2c3e50")
        self.style.configure("Header.TLabel", background="#2c3e50", foreground="white", font=("Arial", 14, "bold"))
        self.style.configure("Tab.TFrame", background="white")
        self.style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
        self.style.configure("TNotebook.Tab", padding=[10, 5], font=("Arial", 10))
        self.style.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "white")])
        
        self.style.configure("ToolButton.TButton", font=("Arial", 10), padding=5)
        self.style.configure("SectionHeader.TLabel", font=("Arial", 12, "bold"), padding=5)
        self.style.configure("NavButton.TButton", font=("Arial", 10), background="#3498db", foreground="white")
    
    def crear_interfaz(self):
        self.configure(background="#f0f0f0")
        
        header_frame = ttk.Frame(self, style="Header.TFrame")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        
        header_label = ttk.Label(header_frame, text="Procesador de Imágenes", style="Header.TLabel")
        header_label.pack(pady=10)
        
        main_frame = ttk.Frame(self)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        left_panel = ttk.Frame(main_frame, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        left_panel.pack_propagate(False)
        
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.crear_menu_lateral(left_panel)
        self.crear_area_trabajo(right_panel)
    
    def crear_menu_lateral(self, parent):
      # Importar el módulo sys para detectar la plataforma
    
    # Crear un frame contenedor
    container = ttk.Frame(parent)
    container.pack(fill=tk.BOTH, expand=True)
    
    # Crear un canvas con scrollbar para el menú lateral
    canvas = tk.Canvas(container, bg="#f0f0f0", highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    
    # Frame que contendrá todos los elementos del menú
    menu_frame = ttk.Frame(canvas)
    
    # Configurar el canvas para que use el scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Empaquetar scrollbar y canvas
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Crear una ventana en el canvas que contendrá el frame del menú
    canvas_window = canvas.create_window((0, 0), window=menu_frame, anchor="nw")
    
    # Función para actualizar la región de desplazamiento
    def update_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    # Función para ajustar el ancho del frame interno al ancho del canvas
    def on_canvas_configure(event):
        # Actualizar el ancho de la ventana interna al ancho del canvas
        canvas.itemconfig(canvas_window, width=event.width)
    
    # Vinculamos los eventos de configuración
    menu_frame.bind("<Configure>", update_scrollregion)
    canvas.bind("<Configure>", on_canvas_configure)
    
    # Función para manejar el desplazamiento con la rueda del ratón
    def on_mousewheel(event):
        # Para Windows y macOS
        if event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
    
    # Vinculamos el evento de la rueda del ratón solo al canvas
    if sys.platform.startswith('win'):
        # Windows
        canvas.bind("<MouseWheel>", on_mousewheel)
    else:
        # Linux y macOS
        canvas.bind("<Button-4>", on_mousewheel)
        canvas.bind("<Button-5>", on_mousewheel)
    
    # Guardamos referencia para poder destruir los bindings más tarde si es necesario
    self.sidebar_canvas = canvas
    
    sections = [
        ("Cargar Imágenes", [
            ("Cargar Imagen Principal", self.cargar_imagen_principal),
            ("Cargar Imagen 1 (Op. Lógicas)", self.cargar_imagen1_logica),
            ("Cargar Imagen 2 (Op. Lógicas)", self.cargar_imagen2_logica)
        ]),
        ("Procesamiento Básico", [
            ("Convertir a Escala de Grises", self.convertir_a_grises),
            ("Aplicar Umbral", self.aplicar_umbral),
            ("Ecualización Hipercúbica", self.ecualizacion_hipercubica)
        ]),
        ("Operaciones Lógicas", [
            ("Aplicar Operaciones Lógicas", self.aplicar_operaciones_logicas)
        ]),
        ("Ruido y Filtros", [
            ("Agregar Ruido Sal y Pimienta", self.agregar_ruido_sal_pimienta),
            ("Agregar Ruido Gaussiano", self.agregar_ruido_gaussiano),
            ("Aplicar Filtro Pesado", self.aplicar_filtro_pesado),
            ("Aplicar Filtro de Robert", self.aplicar_filtro_Robert)
        ]),
        ("Segmentación", [
            ("Segmentación por método de otsu", self.aplicar_filtro_otsu)
        ]),
        ("Histogramas", [
            ("Calcular Histogramas", self.calcular_histogramas)
        ])
    ]
    
    # Frames para las secciones
    for i, (section_name, buttons) in enumerate(sections):
        section_frame = ttk.Frame(menu_frame, padding=(5, 10))
        section_frame.pack(fill=tk.X, padx=5, pady=(5 if i > 0 else 0))
        
        # Título de sección
        title_bg = "#3498db"  # Color azul para encabezados
        title_frame = tk.Frame(section_frame, bg=title_bg)
        title_frame.pack(fill=tk.X)
        
        label = tk.Label(title_frame, text=section_name, bg=title_bg, fg="white", font=("Arial", 11, "bold"))
        label.pack(fill=tk.X, padx=5, pady=5)
        
        # Botones de sección
        buttons_frame = ttk.Frame(section_frame)
        buttons_frame.pack(fill=tk.X)
        
        for btn_text, btn_command in buttons:
            btn = tk.Button(buttons_frame, text=btn_text, command=btn_command, 
                           bg="#f0f0f0", fg="#333333", 
                           activebackground="#d9d9d9", 
                           relief=tk.GROOVE, borderwidth=1,
                           font=("Arial", 9), pady=3)
            btn.pack(fill=tk.X, padx=5, pady=2)
    
    # Botón para guardar imagen
    save_frame = ttk.Frame(menu_frame, padding=(5, 10))
    save_frame.pack(fill=tk.X, padx=5, pady=5)
    
    save_button = tk.Button(save_frame, text="Guardar Imagen Actual", 
                           command=self.guardar_imagen_actual,
                           bg="#27ae60", fg="white", 
                           activebackground="#219653",
                           font=("Arial", 10, "bold"),
                           relief=tk.RAISED, borderwidth=2, pady=5)
    save_button.pack(fill=tk.X, padx=5, pady=5)
    
    def crear_area_trabajo(self, parent):
        notebook_style = ttk.Style()
        notebook_style.configure("TNotebook", tabposition='n')
        
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Crear pestañas
        self.tabs = {}
        tab_names = ["Procesamiento Básico", "Operaciones Lógicas", "Ruido y Filtros", "Segmentación", "Histogramas"]
        
        for tab_name in tab_names:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=tab_name)
            self.tabs[tab_name] = tab
            
            # Área de visualización para cada pestaña
            display_frame = ttk.Frame(tab)
            display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Configurar un canvas para scroll
            canvas = tk.Canvas(display_frame, bg="white")
            scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=canvas.yview)
            content_frame = ttk.Frame(canvas)
            
            content_frame.bind("<Configure>", lambda e, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
            window_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")
            
            # Asegurar que el contenido se expande con el canvas
            def on_canvas_configure(event, canvas=canvas, window_id=window_id):
                canvas.itemconfig(window_id, width=event.width)
            
            canvas.bind("<Configure>", on_canvas_configure)
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Guardar referencia a los frames donde se mostrarán las imágenes
            setattr(self, f"panel_{tab_name.lower().replace(' ', '_')}", content_frame)
    
    def cargar_imagen_principal(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        if ruta:
            self.ruta_imagen_actual = ruta
            imagen = self.procesador.cargar_imagen(ruta)
            self.ruido.cargar_imagen(ruta)
            if imagen is not None:
                self.imagen_actual = imagen
                self.mostrar_imagen(self.panel_procesamiento_básico, imagen, "Imagen Original")
                self.notebook.select(0)
    
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
            self.mostrar_imagen(self.panel_procesamiento_básico, imagen_grises, "Imagen en Escala de Grises")
            self.notebook.select(0)
    
    def aplicar_umbral(self):
        if not self.verificar_imagen_cargada():
            return
        imagen_umbral = self.procesador.aplicar_umbral()
        if imagen_umbral is not None:
            self.imagen_actual = imagen_umbral
            self.mostrar_imagen(self.panel_procesamiento_básico, imagen_umbral, "Imagen Umbralizada")
            self.notebook.select(0)
    
    def ecualizacion_hipercubica(self):
        if not self.verificar_imagen_cargada():
            return
        imagen_ecualizada = self.procesador.ecualizacion_hipercubica()
        if imagen_ecualizada is not None:
            self.imagen_actual = imagen_ecualizada
            self.mostrar_imagen(self.panel_procesamiento_básico, imagen_ecualizada, "Ecualización Hipercúbica")
            self.notebook.select(0)
    
    def aplicar_operaciones_aritmeticas(self):
        if not self.verificar_imagen_cargada():
            return
        
        suma, resta, multiplicacion = self.procesador.aplicar_operaciones_aritmeticas()
        
        for widget in self.panel_procesamiento_básico.winfo_children():
            widget.destroy()
        
        frame = ttk.Frame(self.panel_procesamiento_básico)
        frame.pack(fill=tk.BOTH, expand=True)
        
        if suma is not None:
            self.mostrar_imagen_frame(frame, suma, "Suma", 0, 0)
        if resta is not None:
            self.mostrar_imagen_frame(frame, resta, "Resta", 0, 1)
        if multiplicacion is not None:
            self.mostrar_imagen_frame(frame, multiplicacion, "Multiplicación", 0, 2)
        
        self.notebook.select(0)
    
    def calcular_histogramas(self):
        if not self.verificar_imagen_cargada():
            return
        
        fig_gray, fig_color = self.procesador.calcular_histogramas()
        
        for widget in self.panel_histogramas.winfo_children():
            widget.destroy()
        
        if fig_gray is not None and fig_color is not None:
            frame_histogramas = ttk.Frame(self.panel_histogramas)
            frame_histogramas.pack(fill=tk.BOTH, expand=True)
            
            canvas_gray = FigureCanvasTkAgg(fig_gray, master=frame_histogramas)
            canvas_gray.draw()
            canvas_gray.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)
            
            canvas_color = FigureCanvasTkAgg(fig_color, master=frame_histogramas)
            canvas_color.draw()
            canvas_color.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)
            
            self.notebook.select(4)
    
    def aplicar_operaciones_logicas(self):
        if self.ruta_imagen1_logica is None or self.ruta_imagen2_logica is None:
            self.mostrar_mensaje("Por favor cargue ambas imágenes para operaciones lógicas")
            return
        
        and_img, or_img, xor_img = self.operaciones_logicas.aplicar_operaciones_logicas()
        
        if and_img is not None and or_img is not None and xor_img is not None:
            for widget in self.panel_operaciones_lógicas.winfo_children():
                widget.destroy()
            
            frame_logicas = ttk.Frame(self.panel_operaciones_lógicas)
            frame_logicas.pack(fill=tk.BOTH, expand=True)
            
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen1, "Imagen 1", 0, 0)
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen2, "Imagen 2", 0, 1)
            
            self.mostrar_imagen_frame(frame_logicas, and_img, "AND", 1, 0)
            self.mostrar_imagen_frame(frame_logicas, or_img, "OR", 1, 1)
            self.mostrar_imagen_frame(frame_logicas, xor_img, "XOR", 1, 2)
            
            self.notebook.select(1)
    
    def agregar_ruido_sal_pimienta(self):
        if not self.verificar_imagen_cargada():
            return
        
        imagen_ruido = self.ruido.agregar_ruido_sal_pimienta()
        if imagen_ruido is not None:
            self.imagen_actual = imagen_ruido
            self.mostrar_imagen(self.panel_ruido_y_filtros, imagen_ruido, "Imagen con Ruido Sal y Pimienta")
            self.filtro.imagen_original = imagen_ruido
            self.notebook.select(2)
    
    def agregar_ruido_gaussiano(self):
        if not self.verificar_imagen_cargada():
            return
        
        imagen_ruido = self.ruido.agregar_ruido_gaussiano()
        if imagen_ruido is not None:
            self.imagen_actual = imagen_ruido
<<<<<<< Updated upstream
            self.mostrar_imagen(self.panel_ruido, imagen_ruido, "Imagen con Ruido Gaussiano")
            self.filtro.imagen_original = imagen_ruido  # Preparar para aplicar filtro
            self.notebook.select(2)  # Cambiar a la pestaña de ruido y filtros

    def aplicar_filtro_promediador(self):
       
        if self.filtro.imagen_original is None:
            self.mostrar_mensaje("Por favor agregue ruido a una imagen primero")
            return
        
        imagen_filtrada  = self.filtro.filtro_promediador()   
        if imagen_filtrada is not None:
            self.imagen_actual = imagen_filtrada
            
            # Mostrar imagen original con ruido y su versión filtrada
            for widget in self.panel_ruido.winfo_children():
                widget.destroy()
            
            frame_ruido = ttk.Frame(self.panel_ruido)
            frame_ruido.pack(fill=tk.BOTH, expand=True)
            
            self.mostrar_imagen_frame(frame_ruido, self.filtro.imagen_original, "Imagen con Ruido", 0, 0)
            self.mostrar_imagen_frame(frame_ruido, imagen_filtrada, "Imagen Filtrada Promediador", 0, 1)
            
            self.notebook.select(2)  # Cambiar a la pestaña de ruido y filtros
        

=======
            self.mostrar_imagen(self.panel_ruido_y_filtros, imagen_ruido, "Imagen con Ruido Gaussiano")
            self.filtro.imagen_original = imagen_ruido
            self.notebook.select(2)
>>>>>>> Stashed changes
    
    def aplicar_filtro_pesado(self):
        if not self.verificar_imagen_cargada():
            return
        
        imagen_filtrada = self.filtro.filtro_pesado()
        if imagen_filtrada is not None:
            self.imagen_actual = imagen_filtrada
            
            for widget in self.panel_ruido_y_filtros.winfo_children():
                widget.destroy()
            
            frame_ruido = ttk.Frame(self.panel_ruido_y_filtros)
            frame_ruido.pack(fill=tk.BOTH, expand=True)
            
            self.mostrar_imagen_frame(frame_ruido, self.filtro.imagen_original, "Imagen con Ruido", 0, 0)
            self.mostrar_imagen_frame(frame_ruido, imagen_filtrada, "Imagen Filtrada", 0, 1)
            
            self.notebook.select(2)
    
    def aplicar_filtro_Robert(self):
        self.filtros_segmentacion.imagen_original = self.imagen_actual 
        imagen_filtrada = self.filtros_segmentacion.filtro_Robert()
        if imagen_filtrada is not None:
            self.imagen_actual = imagen_filtrada
            
            for widget in self.panel_ruido_y_filtros.winfo_children():
                widget.destroy()
            
            frame_ruido = ttk.Frame(self.panel_ruido_y_filtros)
            frame_ruido.pack(fill=tk.BOTH, expand=True)
            
            self.mostrar_imagen_frame(frame_ruido, self.filtros_segmentacion.imagen_original, "Imagen convertida A gris", 0, 0)
            self.mostrar_imagen_frame(frame_ruido, imagen_filtrada, "Imagen Filtro robert (Bordes)", 0, 1)
            
            self.notebook.select(2)

    def aplicar_filtro_otsu(self):
        self.filtros_segmentacion.imagen_original = self.imagen_actual 
        imagen_filtrada = self.filtros_segmentacion.filtro_otsu()
        if imagen_filtrada is not None:
            self.imagen_actual = imagen_filtrada
            
            for widget in self.panel_segmentación.winfo_children():
                widget.destroy()
            
            frame_seg = ttk.Frame(self.panel_segmentación)
            frame_seg.pack(fill=tk.BOTH, expand=True)
            
            self.mostrar_imagen_frame(frame_seg, self.filtros_segmentacion.imagen_original, "Imagen convertida A gris", 0, 0)
            self.mostrar_imagen_frame(frame_seg, imagen_filtrada, "Segmentos obtenidos con otsu", 0, 1)
            
            self.notebook.select(3)
    
    def mostrar_imagenes_logicas(self):
        for widget in self.panel_operaciones_lógicas.winfo_children():
            widget.destroy()
        
        frame_logicas = ttk.Frame(self.panel_operaciones_lógicas)
        frame_logicas.pack(fill=tk.BOTH, expand=True)
        
        if self.operaciones_logicas.imagen1 is not None:
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen1, "Imagen 1", 0, 0)
        
        if self.operaciones_logicas.imagen2 is not None:
            self.mostrar_imagen_frame(frame_logicas, self.operaciones_logicas.imagen2, "Imagen 2", 0, 1)
        
        self.notebook.select(1)
    
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
        for widget in panel.winfo_children():
            widget.destroy()
        
        if len(imagen.shape) == 3:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        else:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
        
        frame_contenedor = tk.Frame(panel, bg="white", bd=1, relief=tk.SOLID)
        frame_contenedor.pack(padx=20, pady=20, expand=True)
        
        titulo_frame = tk.Frame(frame_contenedor, bg="#3498db")
        titulo_frame.pack(fill=tk.X)
        
        titulo_label = tk.Label(titulo_frame, text=titulo, font=("Arial", 12, "bold"), bg="#3498db", fg="white")
        titulo_label.pack(pady=8)
        
        altura, anchura = imagen_rgb.shape[:2]
        info_frame = tk.Frame(frame_contenedor, bg="white")
        info_frame.pack(fill=tk.X)
        
        info_label = tk.Label(info_frame, text=f"Dimensiones: {anchura}x{altura}", font=("Arial", 10), bg="white")
        info_label.pack(pady=5)
        
        max_width = 700
        max_height = 500
        
        factor_width = max_width / anchura if anchura > max_width else 1
        factor_height = max_height / altura if altura > max_height else 1
        factor = min(factor_width, factor_height)
        
        if factor < 1:
            nueva_anchura = int(anchura * factor)
            nueva_altura = int(altura * factor)
            imagen_redimensionada = cv2.resize(imagen_rgb, (nueva_anchura, nueva_altura))
        else:
            imagen_redimensionada = imagen_rgb
        
        img = Image.fromarray(imagen_redimensionada)
        img_tk = ImageTk.PhotoImage(image=img)
        
        imagen_frame = tk.Frame(frame_contenedor, bg="white")
        imagen_frame.pack(padx=10, pady=10)
        
        label_img = tk.Label(imagen_frame, image=img_tk, bd=0)
        label_img.image = img_tk
        label_img.pack()
    
    def mostrar_imagen_frame(self, frame, imagen, titulo, fila, columna):
        if len(imagen.shape) == 3:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        else:
            imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)
        
        subframe = tk.Frame(frame, bg="white", bd=1, relief=tk.SOLID)
        subframe.grid(row=fila, column=columna, padx=10, pady=10, sticky="nsew")
        
        frame.grid_columnconfigure(columna, weight=1)
        frame.grid_rowconfigure(fila, weight=1)
        
        titulo_frame = tk.Frame(subframe, bg="#3498db")
        titulo_frame.pack(fill=tk.X)
        
        titulo_label = tk.Label(titulo_frame, text=titulo, font=("Arial", 11, "bold"), bg="#3498db", fg="white")
        titulo_label.pack(pady=5)
        
        altura, anchura = imagen_rgb.shape[:2]
        factor = min(250 / anchura, 250 / altura)
        nueva_anchura = int(anchura * factor)
        nueva_altura = int(altura * factor)
        imagen_redimensionada = cv2.resize(imagen_rgb, (nueva_anchura, nueva_altura))
        
        img = Image.fromarray(imagen_redimensionada)
        img_tk = ImageTk.PhotoImage(image=img)
        
        imagen_frame = tk.Frame(subframe, bg="white")
        imagen_frame.pack(padx=5, pady=5)
        
        label_img = tk.Label(imagen_frame, image=img_tk, bd=0)
        label_img.image = img_tk
        label_img.pack()
        
        info_frame = tk.Frame(subframe, bg="white")
        info_frame.pack(fill=tk.X)
        
        info_label = tk.Label(info_frame, text=f"Dimensiones: {anchura}x{altura}", font=("Arial", 9), bg="white")
        info_label.pack(pady=5)
    
    def mostrar_mensaje(self, mensaje):
        from tkinter import messagebox
        messagebox.showinfo("Información", mensaje)


if __name__ == "__main__":
    app = InterfazProcesadorImagenes()
    app.mainloop()