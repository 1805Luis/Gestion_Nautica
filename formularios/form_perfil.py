import tkinter as tk
from tkinter import ttk
from tkinter import *
from modelos.Cliente import *
from modelos.SmartCard import *
from modelos.Alquiler import *
from formularios.form_historico_reservas import FormularioGraficasDesign
import util.metodos_comunes as comun
import os
import sys

class PerfilUsuario:

    def __init__(self, panel_principal, nSocio, perfil):
        self.Socio = nSocio
        self.datos_usuario = CClientes.mostrarUsuario(self.Socio)
        self.labelPerfil = perfil

        # Crear el contenedor principal en el Frame existente
        self.panel_principal = panel_principal

        # Establecer el estilo para el Notebook
        self.style = ttk.Style()
        self.style.configure("TNotebook.Tab", background="#555555", foreground="green", padding=[10, 5])  # Pestañas
        self.style.map("TNotebook.Tab", background=[("selected", "#007BFF")], foreground=[("selected", "red")])  # Pestaña seleccionada

        # Crear barra de navegación con pestañas
        self.notebook = ttk.Notebook(self.panel_principal, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Crear las pestañas
        self.tab_informacion = ttk.Frame(self.notebook)
        self.tab_historial = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_informacion, text="Información del Usuario")
        self.notebook.add(self.tab_historial, text="Historial de Reservas")

        # Configurar las pestañas
        self.crear_tab_informacion()
        self.crear_tab_historial()

    def crear_tab_informacion(self):
        """Panel de Información del Usuario"""
        groupBox = tk.LabelFrame(self.tab_informacion, text="Datos Personales", font=("Arial", 12))
        groupBox.pack(fill=tk.BOTH, padx=20, pady=20)

        # Campos de texto para información personal
        labelIdSocio = Label(groupBox, text="Nº Socio: ", width=10, font=("arial", 10))
        labelIdSocio.grid(row=0, column=0, padx=5, pady=5)
        self.textBoxIdSocio = Entry(groupBox, width=32)
        self.textBoxIdSocio.insert(0, self.Socio)  
        self.textBoxIdSocio.config(state='readonly')  
        self.textBoxIdSocio.grid(row=0, column=1, padx=5, pady=5)

        labelNombre = Label(groupBox, text="Nombre: ", width=10, font=("arial", 10))
        labelNombre.grid(row=1, column=0, padx=5, pady=5)
        self.textBoxNombre = Entry(groupBox, width=32)
        self.textBoxNombre.grid(row=1, column=1, padx=5, pady=5)

        labelApellido1 = Label(groupBox, text="Apellido 1: ", width=10, font=("arial", 10))
        labelApellido1.grid(row=2, column=0, padx=5, pady=5)
        self.textBoxApellido1 = Entry(groupBox, width=32)
        self.textBoxApellido1.grid(row=2, column=1, padx=5, pady=5)

        labelApellido2 = Label(groupBox, text="Apellido 2: ", width=10, font=("arial", 10))
        labelApellido2.grid(row=2, column=2, padx=5, pady=5)
        self.textBoxApellido2 = Entry(groupBox, width=32)
        self.textBoxApellido2.grid(row=2, column=3, padx=5, pady=5)

        labelTitulo = Label(groupBox, text="TITULACION: ", width=10, font=("arial", 10))
        labelTitulo.grid(row=3, column=0, padx=5, pady=5)
        self.seleccionTitulo = tk.StringVar()
        self.comboTitulo = ttk.Combobox(groupBox, values=["LN", "PNB", "PER", "PY", "CY"], textvariable=self.seleccionTitulo, width=32, state="readonly")
        self.comboTitulo.grid(row=3, column=1, padx=5, pady=5)

        labelTelf = Label(groupBox, text="Telefono: ", width=10, font=("arial", 10))
        labelTelf.grid(row=4, column=0, padx=5, pady=5)
        self.textBoxTelf = Entry(groupBox, width=32)
        self.textBoxTelf.grid(row=4, column=1, padx=5, pady=5)

        # Botón para actualizar información
        self.botonModificar = Button(groupBox, text="Modificar", command=self.actualizarCliente, width=10, bg="#FF9800", fg="white", font=("arial", 10))
        self.botonModificar.grid(row=5, column=1, padx=5, pady=(10, 10))

        self.botonEliminar = Button(groupBox, text="Eliminar", command=self.eliminarUsuario, width=10, bg="#F44336", fg="white", font=("arial", 10))
        self.botonEliminar.grid(row=5, column=2, padx=5, pady=(10, 10))

        self.obtenerDatos()

    def crear_tab_historial(self):
        """Panel de Historial de Reservas"""
        
        # Variable para controlar qué opción se selecciona
        self.opcion_seleccionada = tk.StringVar(value="grafico")  # Valor por defecto es "grafico"
        
        # Crear los Radiobuttons
        self.radio_grafico = tk.Radiobutton(self.tab_historial, text="Ver Gráfico", variable=self.opcion_seleccionada, value="grafico", command=self.mostrar_contenido)
        self.radio_tabla = tk.Radiobutton(self.tab_historial, text="Ver Tabla", variable=self.opcion_seleccionada, value="tabla", command=self.mostrar_contenido)
        
        self.radio_grafico.grid(row=0, column=0, padx=10,sticky="w") 
        self.radio_tabla.grid(row=0, column=1, padx=10, sticky="w")
        
        # Crear un contenedor para el contenido (Gráfico o Tabla)
        self.contenedor = tk.Frame(self.tab_historial)
        self.contenedor.grid(row=1, column=0, columnspan=2) 
        
        # Inicializar mostrando el gráfico (por defecto)
        self.mostrar_contenido()

    def mostrar_contenido(self):
        """Mostrar el contenido según la opción seleccionada (gráfico o tabla)"""
        # Limpiar el contenedor
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        if self.opcion_seleccionada.get() == "grafico":
            # Mostrar el gráfico
            FormularioGraficasDesign(self.contenedor, self.Socio)
        elif self.opcion_seleccionada.get() == "tabla":
            # Crear y mostrar la tabla de reservas
            self.panel_reservas()

    def eliminarUsuario(self):
        """Eliminar el usuario y escribir en la tarjeta"""
        CSmartCard().write_card(0x73, 0x0D, [0x2A] * 13)
        CClientes.eliminarUsuario(self.Socio)
        os._exit(0)

    def actualizarCliente(self):
        """Actualizar la información del cliente y escribir en la tarjeta"""
        nombre = self.textBoxNombre.get()
        ap1 = self.textBoxApellido1.get()
        ap2 = self.textBoxApellido2.get()
        titulo = self.textBoxTelf.get()
        CClientes.editarUsuario(nombre, ap1, ap2, self.comboTitulo.get(), titulo, self.Socio)

        # Código para escribir en la tarjeta
        nombre = nombre[:9]
        Nombre_H = comun.ascii_a_hexadecimal(nombre)
        CSmartCard().write_card(0x27, 0x09, [0x2A] * 9)
        CSmartCard().write_card(0x27, len(Nombre_H), Nombre_H)

        ap1 = ap1[:16]
        Apellido1_H = comun.ascii_a_hexadecimal(ap1)
        CSmartCard().write_card(0x40, 0x10, [0x2A] * 16)
        CSmartCard().write_card(0x40, len(Apellido1_H), Apellido1_H)

        ap2 = ap2[:16]
        Apellido2_H = comun.ascii_a_hexadecimal(ap2)
        CSmartCard().write_card(0x60, 0x10, [0x2A] * 16)
        CSmartCard().write_card(0x60, len(Apellido2_H), Apellido2_H)

        os.execl(sys.executable, sys.executable, *sys.argv)  # Vuelve a abrir el script desde el inicio

    def obtenerDatos(self):
        datosUsuario = CClientes.mostrarUsuario(self.Socio)
        datosUsuario = datosUsuario[0]

        self.textBoxNombre.delete(0, tk.END)
        self.textBoxNombre.insert(0, datosUsuario[1])  

        self.textBoxApellido1.delete(0, tk.END)
        self.textBoxApellido1.insert(0, datosUsuario[2])  

        self.textBoxApellido2.delete(0, tk.END)
        self.textBoxApellido2.insert(0, datosUsuario[3])  


        self.comboTitulo.config(state='normal')  
        self.seleccionTitulo.set(datosUsuario[4]) 
        self.comboTitulo.config(state='readonly')


        self.textBoxTelf.delete(0, tk.END)
        self.textBoxTelf.insert(0, datosUsuario[5])  

    def panel_reservas(self):
        # Asegúrate de que el contenedor sea self.contenedor
        groupBox = LabelFrame(self.contenedor, text=f"Mis reservas", padx=5, pady=5, relief="solid", bd=2)
        groupBox.pack(fill="both", expand=True, padx=10, pady=10)  # Usar el contenedor correcto y expandir

        
        # Crear el Treeview para mostrar las reservas
        self.tree = ttk.Treeview(groupBox, columns=("MMSI", "Tipo Barco", "Fecha Inicio", "Fecha Fin"), show='headings')

        # Configurar columnas y ajustar su ancho
        self.tree.column("#1", anchor=tk.CENTER, width=100, stretch=tk.YES)  # La columna de "MMSI" se ajusta
        self.tree.column("#2", anchor=tk.CENTER, width=150, stretch=tk.YES)  # La columna de "Tipo Barco" se ajusta
        self.tree.column("#3", anchor=tk.CENTER, width=150, stretch=tk.YES)  # La columna de "Fecha Inicio" se ajusta
        self.tree.column("#4", anchor=tk.CENTER, width=150, stretch=tk.YES)  # La columna de "Fecha Fin" se ajusta

        # Configurar encabezados de las columnas
        self.tree.heading("#1", text="MMSI")
        self.tree.heading("#2", text="Tipo Barco")
        self.tree.heading("#3", text="Fecha Inicio")
        self.tree.heading("#4", text="Fecha Fin")

        self.tree.tag_configure('even', background='#f0f0f0')  
        self.tree.tag_configure('odd', background='#ffffff')

        self.tree.pack(fill="both", expand=True)  


        # Actualizar el Treeview con los datos de las reservas
        self.actualizarTreeView()




    def actualizarTreeView(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, row in enumerate(CAlquiler.mostrarTodos(self.Socio)):
            tag = 'even' if index % 2 == 0 else 'odd' 
            self.tree.insert("", "end", values=row, tags=(tag,))