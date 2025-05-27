import customtkinter as ctk

app = ctk.CTk()

# Obtener resolución de la pantalla
ancho = app.winfo_screenwidth()
alto = app.winfo_screenheight()

# Aplicar geometría
app.geometry(f"{ancho}x{alto}+0+0")

app.mainloop()