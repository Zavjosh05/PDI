import customtkinter as ctk

class VentanaEmergente(ctk.CTkToplevel):
    def __init__(self, master, title, mainText, firstButton, secondButton, command1, command2):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text=mainText)
        self.label.pack(pady=20)

        # Envolvemos los comandos con lambdas para agregar el self.destroy()
        self.boton1 = ctk.CTkButton(self, text=firstButton, command=lambda: self.ejecutar_y_cerrar(command1))
        self.boton1.pack(pady=5)

        self.boton2 = ctk.CTkButton(self, text=secondButton, command=lambda: self.ejecutar_y_cerrar(command2))
        self.boton2.pack(pady=5)

    def ejecutar_y_cerrar(self, funcion):
        if funcion:
            funcion()
        self.destroy()
