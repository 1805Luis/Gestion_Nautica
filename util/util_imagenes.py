from PIL import ImageTk, Image

#Escalar la imagen a un tamaño fijado por nosotros
def leer_imagen(path, size): 
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))