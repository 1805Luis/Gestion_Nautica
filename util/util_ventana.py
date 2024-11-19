
#Colocarlo al centro de mi ventana al iniciar el programa
def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int((pantalla_ancho/2)-(aplicacion_ancho/2))
    y = int((pantalla_largo/2)-(aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

def limpiar_panel(panel):
    # Función para limpiar el contenido del panel
    for widget in panel.winfo_children():
        widget.destroy()