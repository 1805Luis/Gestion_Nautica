import tkinter as tk
from tkinter import *
from tkinter import ttk
from config import COLOR_CUERPO_PRINCIPAL
from tkinter import messagebox
from modelos.SmartCard import *
from modelos.Cliente import *
import util.metodos_comunes as comun

class FormularioSocios:

    def __init__(self, panel_principal):
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.LEFT, fill='both', expand=False)
        self.panel_datos()

        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.LEFT, fill='both', expand=False)
        self.panel_usuarios()

    def panel_datos(self):
        groupBox = tk.LabelFrame(self.barra_superior, text="Usuario seleccionado", padx=5, pady=5, relief="solid", bd=2)
        groupBox.pack(fill="both", expand=False,padx=10, pady=10)  

        labelD = Label(groupBox, text="ID: ", width=15, font=("arial", 10))
        labelD.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.textBoxID = Entry(groupBox, width=10,state="readonly")
        self.textBoxID.grid(row=0, column=1, padx=5, pady=5)

        labelPregunta = Label(groupBox, text="¿Qué quieres modificar?", font=("arial", 10))
        labelPregunta.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.checkRol = BooleanVar(value=True)
        self.checkEstado = BooleanVar(value=True)

        checkRol = Checkbutton(groupBox, text="Rol", variable=self.checkRol, command=self.toggle_fields)
        checkRol.grid(row=2, column=0, padx=5, pady=5)

        checkEstado = Checkbutton(groupBox, text="Estado Cuenta", variable=self.checkEstado, command=self.toggle_fields)
        checkEstado.grid(row=2, column=1, padx=5, pady=5)

        self.labelRol = Label(groupBox, text="Rol: ", width=15, font=("arial", 10))
        self.labelRol.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.seleccionRol = StringVar()
        self.comboRol = ttk.Combobox(groupBox, values=["user", "admin"], textvariable=self.seleccionRol, width=10, state="readonly")
        self.comboRol.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Campos de Estado Cuenta
        self.labelEstadoCuenta = Label(groupBox, text="Estado Cuenta: ", width=15, font=("arial", 10))
        self.labelEstadoCuenta.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.seleccionEstadoCuenta = StringVar()
        self.comboEstadoCuenta = ttk.Combobox(groupBox, values=["activa", "suspendida"], textvariable=self.seleccionEstadoCuenta, width=10, state="readonly")
        self.comboEstadoCuenta.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Botones
        self.botonModificar = Button(groupBox, text="Modificar", command=self.modificar, width=10, bg="#FF9800", fg="white", font=("arial", 10))
        self.botonModificar.grid(row=5, column=0, padx=5, pady=(10, 10))

        self.botonEliminar = Button(groupBox, text="Eliminar", command=self.eliminar, width=10, bg="#F44336", fg="white", font=("arial", 10))
        self.botonEliminar.grid(row=5, column=1, padx=5, pady=(10, 10))

    def toggle_fields(self):
        
        if self.checkRol.get():
            self.labelRol.grid(row=3, column=0, padx=5, pady=5, sticky="e")  
            self.comboRol.grid(row=3, column=1, padx=5, pady=5, sticky="w")  
        else:
            self.labelRol.grid_forget()  
            self.comboRol.grid_forget()  

        if self.checkEstado.get():
            self.labelEstadoCuenta.grid(row=4, column=0, padx=5, pady=5, sticky="e")  
            self.comboEstadoCuenta.grid(row=4, column=1, padx=5, pady=5, sticky="w")  
        else:
            self.labelEstadoCuenta.grid_forget() 
            self.comboEstadoCuenta.grid_forget()  

    def panel_usuarios(self):
        groupBox = LabelFrame(self.barra_inferior, text=f"Lista de usuarios", padx=5, pady=5,relief="solid", bd=2)
        groupBox.pack(fill="both", expand=False,padx=10, pady=10)  

        self.tree = ttk.Treeview(groupBox, columns=("Nº Socio", "Rol", "Estado de la cuenta"), show='headings', height=5)

        column_widths = [60, 60, 150]  
        for i, column in enumerate(self.tree["columns"], start=1):
            self.tree.column(f"#{i}", anchor=tk.CENTER, width=column_widths[i - 1])  
            self.tree.heading(f"#{i}", text=column)

        self.tree.pack(fill="both", expand=True)
        self.actualizarTreeView()

        self.tree.bind("<<TreeviewSelect>>", self.seleccionarRegistro)

        self.tree.pack()

    def seleccionarRegistro(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')

            self.textBoxID.config(state='normal')  
            self.textBoxID.delete(0, tk.END)
            self.textBoxID.insert(0, item_values[0])  
            self.textBoxID.config(state='readonly')

            self.comboRol.config(state='normal')  
            self.seleccionRol.set(item_values[1]) 
            self.comboRol.config(state='readonly')

            self.comboEstadoCuenta.config(state='normal')  
            self.seleccionEstadoCuenta.set(item_values[2]) 
            self.comboEstadoCuenta.config(state='readonly')

    def actualizarTreeView(self):

        try:
            self.tree.delete(*self.tree.get_children())
            for row in CClientes.mostrarTodosSocios():
                estado = row[2] 

                item = self.tree.insert("", "end", values=row)

                if estado == "activa":
                    self.tree.item(item, tags=("verde",))
                elif estado == "suspendida":
                    self.tree.item(item, tags=("rojo",))

            self.tree.tag_configure("verde", background="lightgreen") 
            self.tree.tag_configure("rojo", background="red")  
        
        except ValueError as error:
         print("Error al actualizar tabla {}".format(error))


    def modificar(self):
        Id = self.textBoxID.get()
        Rol = self.comboRol.get()
        Cuenta = self.comboEstadoCuenta.get()

            
        if not self.checkRol.get() and not self.checkEstado.get():
            messagebox.showwarning("Advertencia", "Debes seleccionar al menos un campo para modificar.")
            return
        
        CClientes.actualizarRolCuenta(Id,Rol,Cuenta)

        self.actualizarTreeView()

    def eliminar(self):
        CClientes.eliminarUsuario(self.textBoxID.get())
