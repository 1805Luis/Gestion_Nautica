import tkinter as tk
from PIL import Image, ImageTk  # Para manejar imágenes
import util.util_ventana as util_ventana
from config import TITULO_APP


class FormularioInfoDesign(tk.Toplevel):  
    def __init__(self) -> None:
        super().__init__()
        self.config_window()
        self.construirWidget()

    def config_window(self):  
        self.title(TITULO_APP)
        self.iconbitmap("./imagenes/logo.ico")
        w, h = 400, 300  
        util_ventana.centrar_ventana(self, w, h)
    
    def construirWidget(self):
        # Configurar el Canvas
        self.canvas = tk.Canvas(self, width=400, height=300)
        self.canvas.pack(fill="both", expand=True)
        
        # Cargar la imagen de fondo
        self.fondo_img = Image.open("./imagenes/barco.png")  
        self.fondo_img = self.fondo_img.resize((400, 300), Image.Resampling.LANCZOS)  
        self.fondo_tk = ImageTk.PhotoImage(self.fondo_img)
        
        # Mostrar la imagen en el Canvas
        self.canvas.create_image(0, 0, image=self.fondo_tk, anchor="nw")
        
        # Frase icónica
        frase_iconica = "¡El viento es el mejor compañero de un marinero!"
        self.labelFrase = tk.Label(self.canvas, text=frase_iconica)
        self.labelFrase.config(fg="#FFFFFF", font=("Roboto", 10), bg="black", wraplength=350, justify="center")

        # Calcular la posición para centrar la frase
        text_width = self.labelFrase.winfo_reqwidth()  # Ancho del texto
        canvas_width = 400  # Ancho del Canvas
        x_position = (canvas_width - text_width) / 2  # Centrar el texto

        # Colocar la frase centrada
        self.labelFrase.place(x=x_position, y=240)
