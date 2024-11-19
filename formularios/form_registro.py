import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from modelos.Cliente import *
from modelos.SmartCard import *
import util.metodos_comunes as comun


class Registro(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Formulario de Registro de Socio")
        self.geometry("400x350")  # Tamaño de la ventana ajustado
        self.panel_datos()

    def panel_datos(self):
        # Crear un marco para agrupar los campos del formulario
        groupBox = tk.LabelFrame(self, text="Datos del Socio", padx=10, pady=10)
        groupBox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Campo para el nombre
        labelNombre = tk.Label(groupBox, text="Nombre: ", width=15, font=("arial", 10))
        labelNombre.grid(row=0, column=0)
        self.textBoxNombre = tk.Entry(groupBox, width=32)
        self.textBoxNombre.grid(row=0, column=1)

        # Campo para el primer apellido
        labelApellido1 = tk.Label(groupBox, text="Apellido 1: ", width=15, font=("arial", 10))
        labelApellido1.grid(row=1, column=0)
        self.textBoxApellido1 = tk.Entry(groupBox, width=32)
        self.textBoxApellido1.grid(row=1, column=1)

        # Campo para el segundo apellido
        labelApellido2 = tk.Label(groupBox, text="Apellido 2: ", width=15, font=("arial", 10))
        labelApellido2.grid(row=2, column=0)
        self.textBoxApellido2 = tk.Entry(groupBox, width=32)
        self.textBoxApellido2.grid(row=2, column=1)

        # Campo para la titulación (con un combo box)
        labelTitulo = tk.Label(groupBox, text="Titulación: ", width=15, font=("arial", 10))
        labelTitulo.grid(row=3, column=0)
        seleccionTitulo = tk.StringVar()
        self.combo = ttk.Combobox(groupBox, values=["LN", "PNB", "PER", "PY", "CY"], textvariable=seleccionTitulo, width=32,state="readonly")
        self.combo.grid(row=3, column=1)
        seleccionTitulo.set("LN")

        # Campo para el teléfono
        labelTelefono = tk.Label(groupBox, text="Teléfono: ", width=15, font=("arial", 10))
        labelTelefono.grid(row=4, column=0)
        self.textBoxTelefono = tk.Entry(groupBox, width=32)
        self.textBoxTelefono.grid(row=4, column=1)

        # Botón de registro
        btnRegistrar = tk.Button(groupBox, text="Registrar", width=15, bg="#4CAF50", fg="white", command=self.registrar)
        btnRegistrar.grid(row=5, column=1, pady=10)

    def registrar(self):
        # Obtener los datos del formulario
        nombre = self.textBoxNombre.get()
        apellido1 = self.textBoxApellido1.get()
        apellido2 = self.textBoxApellido2.get()
        titulacion = self.combo.get()

        # Verificar que los campos no estén vacíos
        if not nombre or not apellido1 or not apellido2 or not titulacion:
            messagebox.showinfo("Información", "Por favor, complete todos los campos.")
            return

        try:
            # Registrar al cliente (esto podría implicar la creación en una base de datos)
            numero_socio = CClientes.ingresarClientes(nombre, apellido1, apellido2, titulacion, self.textBoxTelefono.get())

            # Asignar el número de socio al master
            self.master.nSocio = numero_socio

            # Escribir la información en la tarjeta (o hacer las operaciones necesarias)
            nombre_hex = comun.ascii_a_hexadecimal(nombre[:9])  # Solo los primeros 9 caracteres
            CSmartCard().write_card(0x27, 0x09, [0x2A] * 9)
            CSmartCard().write_card(0x27, len(nombre_hex), nombre_hex)

            apellido1_hex = comun.ascii_a_hexadecimal(apellido1[:16])  # Solo los primeros 16 caracteres
            CSmartCard().write_card(0x40, 0x10, [0x2A] * 16)
            CSmartCard().write_card(0x40, len(apellido1_hex), apellido1_hex)

            apellido2_hex = comun.ascii_a_hexadecimal(apellido2[:16])  # Solo los primeros 16 caracteres
            CSmartCard().write_card(0x60, 0x10, [0x2A] * 16)
            CSmartCard().write_card(0x60, len(apellido2_hex), apellido2_hex)

            numero_socio_hex = comun.ascii_a_hexadecimal(str(numero_socio)[:13])  # Limitar a 13 caracteres
            CSmartCard().write_card(0x73, 0x0D, [0x2A] * 13)
            CSmartCard().write_card(0x73, len(numero_socio_hex), numero_socio_hex)

            # Cerrar la ventana de registro
            self.destroy()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Socio registrado exitosamente.")
        
        except Exception as e:
            print(f"Error al registrar el cliente: {e}")
            messagebox.showerror("Error", f"Hubo un error al registrar al socio: {e}")

