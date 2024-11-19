import tkinter as tk
from tkinter import *
from tkinter import ttk
from config import COLOR_CUERPO_PRINCIPAL
from tkcalendar import DateEntry
from tkinter import messagebox
from modelos.Barco import *  
from modelos.SmartCard import *
from modelos.Cliente import *
import util.metodos_comunes as comun

class FormularioReservar:

    def __init__(self, panel_principal, nSocio):
        self.Socio = nSocio
        titulacion = CClientes.mostrarTitulacionSocio(self.Socio)
        self.Titulo=titulacion[0][0].upper()
        self.barra_superior = tk.Frame(panel_principal)
        self.barra_superior.pack(side=tk.TOP, fill=tk.X, expand=False)
        self.panel_datos()

        self.barra_inferior = tk.Frame(panel_principal)
        self.barra_inferior.pack(side=tk.TOP, fill='both', expand=True)
        self.panel_barcos()

    def panel_datos(self):
        groupBox = tk.LabelFrame(self.barra_superior, text="Datos de la reserva", padx=5, pady=5)
        groupBox.grid(row=0, column=0, padx=10, pady=10)

        labelIdSocio = Label(groupBox, text="Nº Socio: ", width=10, font=("arial", 10))
        labelIdSocio.grid(row=0, column=0)
        self.textBoxIdSocio = Entry(groupBox, width=32)
        self.textBoxIdSocio.insert(0, self.Socio)  # Insertar texto
        self.textBoxIdSocio.config(state='readonly')  # Solo lectura
        self.textBoxIdSocio.grid(row=0, column=1)

        labelMMSI = Label(groupBox, text="MMSI: ", width=10, font=("arial", 10))
        labelMMSI.grid(row=1, column=0)
        self.textBoxMMSI = Entry(groupBox, width=32)
        self.textBoxMMSI.config(state='readonly')  # Solo lectura
        self.textBoxMMSI.grid(row=1, column=1)

        labelZONA = Label(groupBox, text="ZONA: ", width=10, font=("arial", 10))
        labelZONA.grid(row=2, column=0)
        self.textBoxZona = Entry(groupBox, width=32)
        self.textBoxZona.config(state='readonly')  # Solo lectura
        self.textBoxZona.grid(row=2, column=1)

        labelTitulo = Label(groupBox, text="TITULACION: ", width=10, font=("arial", 10))
        labelTitulo.grid(row=2, column=3)
        self.textBoxTitulo = Entry(groupBox, width=32)
        self.textBoxTitulo.config(state='readonly')  # Solo lectura
        self.textBoxTitulo.grid(row=2, column=4)

        # Sub-GroupBox para las fechas
        fechasGroupBox = tk.LabelFrame(groupBox, text="Fechas de la Reserva", padx=5, pady=5)
        fechasGroupBox.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

        labelInicio = Label(fechasGroupBox, text="Inicio: ", width=10, font=("arial", 10))
        labelInicio.grid(row=0, column=0)
        self.textBoxInicio = DateEntry(fechasGroupBox, width=32, date_pattern='dd/mm/yyyy')
        self.textBoxInicio.grid(row=0, column=1)

        labelFin = Label(fechasGroupBox, text="Fin: ", width=10, font=("arial", 10))
        labelFin.grid(row=0, column=2)
        self.textBoxFin = DateEntry(fechasGroupBox, width=32, date_pattern='dd/mm/yyyy')
        self.textBoxFin.grid(row=0, column=3)

        Button(groupBox, text="Reservar", width=10, bg="#4CAF50", fg="white", command=self.Reservar).grid(row=4, column=2)

    def panel_barcos(self):
        groupBox = LabelFrame(self.barra_inferior, text=f"Lista de barcos permitidos para patrones con licencia {self.Titulo}", padx=5, pady=5)
        groupBox.grid(row=0, column=1, padx=5, pady=5)

        self.tree = ttk.Treeview(groupBox, columns=("MMSI", "Tipo Barco", "Título Requerido", "Zona Navegación", "Eslora", "Tripulación", "Pantalán", "Amarre"), show='headings', height=5)

        # Configurar columnas y ajustar su ancho
        column_widths = [70, 100, 100, 120, 70, 100, 55, 55]  # Anchos para cada columna
        for i, column in enumerate(self.tree["columns"], start=1):
            self.tree.column(f"#{i}", anchor=tk.CENTER, width=column_widths[i - 1])  # Ajustar ancho
            self.tree.heading(f"#{i}", text=column)

        # Lógica para mostrar barcos en el formulario
        for row in CBarcos.mostrarBarcos("disponible",self.Titulo):
            self.tree.insert("", "end", values=row)

        # Ejecutar al hacer click y mostrar resultado
        self.tree.bind("<<TreeviewSelect>>", self.seleccionarRegistro)

        # Empaquetar el Treeview
        self.tree.pack()

    def seleccionarRegistro(self, event):
        # Obtener la selección del Treeview
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')

            # Asignar los valores a los campos de texto
            self.textBoxMMSI.config(state='normal')  # Hacer editable solo para este momento
            self.textBoxMMSI.delete(0, tk.END)
            self.textBoxMMSI.insert(0, item_values[0])  # Suponiendo que el MMSI es el primer valor

            self.textBoxZona.config(state='normal')  # Hacer editable solo para este momento
            self.textBoxZona.delete(0, tk.END)
            self.textBoxZona.insert(0, item_values[3])  # Suponiendo que la Zona es el cuarto valor

            self.textBoxTitulo.config(state='normal')  # Hacer editable solo para este momento
            self.textBoxTitulo.delete(0, tk.END)
            self.textBoxTitulo.insert(0, item_values[2])  # Suponiendo que el Título es el tercer valor

            # Volver a ponerlos en modo solo lectura después de la inserción
            self.textBoxMMSI.config(state='readonly')
            self.textBoxZona.config(state='readonly')
            self.textBoxTitulo.config(state='readonly')

    def Reservar(self):
        MMSI = self.textBoxMMSI.get()
        Zona = self.textBoxZona.get()
        TitulacionMinima = self.textBoxTitulo.get()
        fecha_inicio = self.textBoxInicio.get_date()
        fecha_fin = self.textBoxFin.get_date()

        if not fecha_fin or not fecha_inicio or not MMSI or not Zona or not TitulacionMinima:
            messagebox.showinfo("Informacion", "Los datos están vacíos")
            return
        
        if  fecha_fin < fecha_inicio:
            messagebox.showinfo("Informacion", "La fecha de fin no puede ser más pequeña que la de inicio")
            return
        

        filas = CBarcos.estaAlquilado(MMSI,fecha_inicio,fecha_fin,0)

        if filas != 0:
            messagebox.showinfo("Informacion", "El barco seleccionado está reservado para esas fechas")
            return

            
        if filas == 0:
            MMSI_H = comun.ascii_a_hexadecimal(MMSI)
            CSmartCard().write_card(0x95,0x0B,[0x2A]*11)
            CSmartCard().write_card(0x95,len(MMSI_H),MMSI_H)

            TitulacionMinima_H = comun.ascii_a_hexadecimal(TitulacionMinima)
            CSmartCard().write_card(0xAB,0x05,[0x2A]*5)
            CSmartCard().write_card(0xAB,len(TitulacionMinima_H),TitulacionMinima_H)

            fecha_formateada = fecha_inicio.strftime("%d/%m/%y")
            Inicio_H = comun.ascii_a_hexadecimal(fecha_formateada)
            CSmartCard().write_card(0xE7,0x08,[0x2A]*8)
            CSmartCard().write_card(0xE7,0x08,Inicio_H)

            fecha_formateada = fecha_fin.strftime("%d/%m/%y")
            Fin_H = comun.ascii_a_hexadecimal(fecha_formateada)
            CSmartCard().write_card(0xF4,0x08,[0x2A]*8)
            CSmartCard().write_card(0xF4,0x08,Fin_H)

            Id_Reserva = CBarcos.CrearAlquiler(MMSI, self.Socio, fecha_inicio, fecha_fin)
            Id_Reserva = str(Id_Reserva)
            
            Id_Reserva_H = comun.ascii_a_hexadecimal(Id_Reserva)
            CSmartCard().write_card(0xBB,0x05,[0x2A]*5)
            CSmartCard().write_card(0xBB,len(Id_Reserva_H),Id_Reserva_H)
            
            messagebox.showinfo("Informacion", "Reserva hecha con exito")             
            





       

