import customtkinter as ctk

# Inicializar la ventana
ctk.set_appearance_mode("dark")  # Opciones: "System" (por defecto), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Puedes elegir otros temas como "green", "dark-blue", etc.

ventana = ctk.CTk()  # Crea la ventana principal
ventana.geometry("400x300")
ventana.title("Ejemplo de Botón")

# Función a ejecutar cuando se presiona el botón
def accion_boton():
    print("¡Botón presionado!")

# Crear un botón
boton = ctk.CTkButton(
    master=ventana,
    text="Presióname",
    command=accion_boton,
    width=200,
    height=40,
    corner_radius=10,
    fg_color="blue",        # Color de fondo
    hover_color="darkblue", # Color al pasar el mouse
    text_color="white"      # Color del texto
)

# Posicionar el botón
boton.pack(pady=20)

# Iniciar el bucle de la interfaz
ventana.mainloop()
