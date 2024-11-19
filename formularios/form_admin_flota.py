import tkinter as tk
from tkinter import *
from tkinter import ttk
from config import COLOR_CUERPO_PRINCIPAL
from tkinter import messagebox
from modelos.Barco import *
from modelos.SmartCard import *
from modelos.Cliente import *

class FormularioFlota:

    def __init__(self, panel_principal):
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.panel_datos()

        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.TOP, fill='both', expand=True)
        self.panel_barcos()

    def panel_datos(self):
        groupBox = tk.LabelFrame(self.barra_superior, text="Datos de la embarcacion", padx=5, pady=5, relief="solid", bd=2)
        groupBox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        labelMMSI = Label(groupBox, text="MMSI: ", width=15, font=("arial", 10))
        labelMMSI.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.textBoxMMSI = Entry(groupBox, width=32)
        self.textBoxMMSI.grid(row=1, column=1, padx=5, pady=5)

        labelTipo = Label(groupBox, text="Tipo de Barco: ", width=15, font=("arial", 10))
        labelTipo.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.textBoxTipo = Entry(groupBox, width=32)
        self.textBoxTipo.grid(row=2, column=1, padx=5, pady=5)

        labelTripulacion = Label(groupBox, text="Tripulación: ", width=15, font=("arial", 10))
        labelTripulacion.grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.textBoxTripulacion = Entry(groupBox, width=10, validate="key", validatecommand=(groupBox.register(self.validar_entero), '%P'))
        self.textBoxTripulacion.grid(row=2, column=3, padx=5, pady=5)

        labelZona = Label(groupBox, text="Zona de Navegación: ", width=15, font=("arial", 10))
        labelZona.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.seleccionZona = StringVar()
        self.comboZona = ttk.Combobox(groupBox, values=[1, 2, 3, 4, 5, 6, 7], textvariable=self.seleccionZona, width=30, state="readonly")
        self.comboZona.grid(row=3, column=1, padx=5, pady=5)
        self.comboZona.bind("<<ComboboxSelected>>", self.actualizar_titulo)

        labelEslora = Label(groupBox, text="Eslora (m): ", width=15, font=("arial", 10))
        labelEslora.grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.textBoxEslora = Entry(groupBox, width=32)
        self.textBoxEslora.grid(row=3, column=3, padx=5, pady=5)
        self.textBoxEslora.bind("<KeyRelease>", self.actualizar_titulo)

        labelTitulo = Label(groupBox, text="Título Requerido: ", width=15, font=("arial", 10))
        labelTitulo.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.textBoxTitulo = Entry(groupBox, width=32, state="readonly")
        self.textBoxTitulo.grid(row=5, column=1, padx=5, pady=5)

        labelPantalan = Label(groupBox, text="Pantalán: ", width=15, font=("arial", 10))
        labelPantalan.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.seleccionPantalan = StringVar()
        self.comboPantalan = ttk.Combobox(groupBox, values=[chr(i) for i in range(65, 91) if chr(i) != 'Ñ'], textvariable=self.seleccionPantalan, width=10, state="readonly")
        self.comboPantalan.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        labelAmarre = Label(groupBox, text="Amarre: ", width=15, font=("arial", 10))
        labelAmarre.grid(row=6, column=2, padx=5, pady=5, sticky="e")
        self.textBoxAmarre = Entry(groupBox, width=10, validate="key", validatecommand=(groupBox.register(self.validar_entero), '%P'))
        self.textBoxAmarre.grid(row=6, column=3, padx=5, pady=5)

        labelEstado = Label(groupBox, text="Estado: ", width=15, font=("arial", 10))
        labelEstado.grid(row=7, column=0, padx=5, pady=5, sticky="e")
        self.seleccionEstado = StringVar()
        self.comboEstado = ttk.Combobox(groupBox, values=["Disponible", "En revisión"],textvariable=self.seleccionEstado, width=10, state="readonly")
        self.comboEstado.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        self.botonAñadir = Button(groupBox, text="Añadir", command=self.anadir, width=10, bg="#4CAF50", fg="white", font=("arial", 10))
        self.botonAñadir.grid(row=8, column=1, padx=5, pady=(10, 10))

        self.botonModificar = Button(groupBox, text="Modificar", command=self.modificar, width=10, bg="#FF9800", fg="white", font=("arial", 10))
        self.botonModificar.grid(row=8, column=2, padx=5, pady=(10, 10))

        self.botonEliminar = Button(groupBox, text="Eliminar", command=self.eliminar, width=10, bg="#F44336", fg="white", font=("arial", 10))
        self.botonEliminar.grid(row=8, column=3, padx=5, pady=(10, 10))

    def actualizar_titulo(self, event=None):
        """Actualiza el título requerido en función de la eslora y zona de navegación."""
        try:
            eslora = float(self.textBoxEslora.get())  # Obtener el valor de eslora
            zona = int(self.seleccionZona.get())  # Obtener el valor de zona de navegación
        except ValueError:
            self.textBoxTitulo.delete(0, tk.END)
            return  # Si los valores no son válidos, limpiar el campo y salir

        # Tabla de requisitos de títulos
        if eslora <= 6 and zona in [6, 7]:
            titulo = "LN"
        elif eslora <= 8 and zona in [5, 6, 7]:
            titulo = "PNB"
        elif eslora <= 15 and zona in [4, 5, 6, 7]:
            titulo = "PER"
        elif eslora <= 24 and zona in [2, 3, 4, 5, 6, 7]:
            titulo = "PY"
        elif eslora <= 24:
            titulo = "CY"
        else:
            titulo = "No disponible"

        # Actualizar el campo Título Requerido
        self.textBoxTitulo.config(state="normal")
        self.textBoxTitulo.delete(0, tk.END)
        self.textBoxTitulo.insert(0, titulo)
        self.textBoxTitulo.config(state="readonly")

    def validar_entero(self, valor):
        """Valida que el campo solo contenga números enteros."""
        if valor.isdigit() or valor == "":  # Permite números enteros o vacío
            return True
        return False

    def panel_barcos(self):
        groupBox = LabelFrame(self.barra_inferior, text=f"Lista de la flota", padx=5, pady=5,relief="solid", bd=2)
        groupBox.pack(fill="both", expand=True,padx=10, pady=10)  

        self.tree = ttk.Treeview(groupBox, columns=("MMSI", "Tipo Barco", "Título Requerido", "Zona Navegación", "Eslora", "Tripulación", "Pantalán", "Amarre","Estado"), show='headings', height=5)

        # Configurar columnas y ajustar su ancho
        column_widths = [70, 100, 100, 100, 70, 100, 50, 50, 100]  # Anchos para cada columna
        for i, column in enumerate(self.tree["columns"], start=1):
            self.tree.column(f"#{i}", anchor=tk.CENTER, width=column_widths[i - 1])  # Ajustar ancho
            self.tree.heading(f"#{i}", text=column)

        self.tree.pack(fill="both", expand=True)
        self.actualizarTreeView()

        # Ejecutar al hacer click y mostrar resultado
        self.tree.bind("<<TreeviewSelect>>", self.seleccionarRegistro)

        # Empaquetar el Treeview
        self.tree.pack()

    def seleccionarRegistro(self, event):
        # Obtener la selección del Treeview
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')

            self.textBoxMMSI.delete(0, tk.END)
            self.textBoxMMSI.insert(0, item_values[0])  

            self.textBoxTipo.delete(0, tk.END)
            self.textBoxTipo.insert(0, item_values[1])  

            self.textBoxTitulo.config(state='normal')  
            self.textBoxTitulo.delete(0, tk.END)
            self.textBoxTitulo.insert(0, item_values[2])
            self.textBoxTitulo.config(state='readonly')

            self.comboZona.config(state='normal')  
            self.seleccionZona.set(item_values[3]) 
            self.comboZona.config(state='readonly')

            self.textBoxEslora.delete(0, tk.END)
            self.textBoxEslora.insert(0, item_values[4])  

            self.textBoxTripulacion.delete(0, tk.END)
            self.textBoxTripulacion.insert(0, item_values[5]) 

            self.comboPantalan.config(state='normal')  
            self.seleccionPantalan.set(item_values[6]) 
            self.comboPantalan.config(state='readonly')


            self.textBoxAmarre.delete(0, tk.END)
            self.textBoxAmarre.insert(0, item_values[7]) 

            self.comboEstado.config(state='normal')  
            self.seleccionEstado.set(item_values[8]) 
            self.comboEstado.config(state='readonly')

    def actualizarTreeView(self):

        try:
            self.tree.delete(*self.tree.get_children())
            # Lógica para mostrar barcos en el formulario
            for row in CBarcos.mostrarBarcos("todos", ""):
                estado = row[8] 

                # Insertar la fila en el Treeview
                item = self.tree.insert("", "end", values=row)

                # Cambiar el color según el estado
                if estado == "Disponible":
                    self.tree.item(item, tags=("verde",))
                elif estado == "En revisión":
                    self.tree.item(item, tags=("amarillo",))

            # Añadir etiquetas para colores
            self.tree.tag_configure("verde", background="lightgreen")  # Fondo verde para "Disponible"
            self.tree.tag_configure("amarillo", background="#FFEB3B")  # Fondo amarillo para "En revisión"
        
        except ValueError as error:
         print("Error al actualizar tabla {}".format(error))

    def comprobar_datos(self):
        MMSI = self.textBoxMMSI.get()
        tipo_barco = self.textBoxTipo.get()
        titulo_requerido = self.textBoxTitulo.get()
        zona_navegacion = self.comboZona.get()
        eslora = self.textBoxEslora.get()
        tripulacion = self.textBoxTripulacion.get()
        pantalan = self.comboPantalan.get()
        amarre = self.textBoxAmarre.get()
        estado = self.comboEstado.get()

            
        if not all([MMSI, tipo_barco, titulo_requerido, zona_navegacion, eslora, tripulacion, pantalan, amarre, estado]):
            messagebox.showinfo("Error", "No puede haber datos vacíos")
            return 0  # O puedes devolver un mensaje de error o lanzar una excepción
        
        # Devolver los valores en un array
        return [MMSI, tipo_barco, titulo_requerido, zona_navegacion, eslora, tripulacion, pantalan, amarre, estado]


    def anadir(self):
        datos = self.comprobar_datos()

        if datos == 0:
            return

        CBarcos.CrearBarco(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7], datos[8])
        self.limpiarDatos()
        self.actualizarTreeView()

    def modificar(self):
        datos = self.comprobar_datos()

        if datos == 0:
            return

        CBarcos.ModificarBarco(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7], datos[8])
        self.limpiarDatos()
        self.actualizarTreeView()

    def eliminar(self):
        CBarcos.EliminarBarco(self.textBoxMMSI.get())
        self.limpiarDatos()
        self.actualizarTreeView()
    
    def limpiarDatos(self):
           
        self.textBoxMMSI.delete(0, tk.END)
        self.textBoxTipo.delete(0, tk.END)
        self.textBoxTitulo.delete(0, tk.END)
        self.textBoxEslora.delete(0, tk.END)
        self.textBoxTripulacion.delete(0, tk.END)
        self.textBoxAmarre.delete(0, tk.END)
        self.comboZona.set("")
        self.comboPantalan.set("")
        self.comboEstado.set("")
