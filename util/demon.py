import time
from tkinter import Toplevel, Label, Button
from modelos.SmartCard import *

dialogo = None  # Variable global para el diálogo

def ComprobaciónTarjeta(parent):
    global dialogo
    while True:
        print(f"[Hilo demonio] Registro de tiempo: {time.strftime('%H:%M:%S')}")
        resultado = CSmartCard.HayTarjeta()

        if not resultado and dialogo is None:
            # Si no hay tarjeta y no se ha mostrado el diálogo, lo creamos
            dialogo = Toplevel(parent)
            dialogo.title("Advertencia")
            dialogo.geometry("300x150")

            # Calcular posición centrada para el diálogo
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 150
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 75
            dialogo.geometry(f"300x150+{x}+{y}")

            Label(dialogo, text="No se detecta ninguna tarjeta. Vuelva a introducirla.").pack(pady=20)

            # Botón "Reintentar"
            Button(dialogo, text="Reintentar", command=lambda: reintentar(parent)).pack(pady=5)
            # Botón "Cerrar"
            Button(dialogo, text="Cerrar", command=cerrar_aplicacion).pack(pady=10)

            dialogo.transient(parent)  # Mantiene el diálogo en la parte superior
            dialogo.grab_set()  # Bloquea la interacción con la ventana principal
            parent.update()

        elif resultado and dialogo is not None:
            # Si la tarjeta vuelve a insertarse y el diálogo está abierto, lo cerramos
            dialogo.destroy()
            dialogo = None  # Restablecemos la referencia del diálogo a None

        # Espera un breve período para evitar un bucle ocupado
        time.sleep(2)

def cerrar_aplicacion():
    """Cerrar la aplicación."""
    if dialogo:
        dialogo.destroy()  # Cierra el diálogo si está abierto
    # Cierra toda la aplicación
    exit(0)  # Esto cerrará la aplicación completamente

def reintentar(parent):
    """Reiniciar la comprobación de la tarjeta."""
    global dialogo
    if dialogo:
        dialogo.destroy()  # Cierra el diálogo si está abierto
        dialogo = None  # Restablecemos la referencia del diálogo a None

    # No reiniciar el bucle aquí; solo cerramos el diálogo y continuamos
