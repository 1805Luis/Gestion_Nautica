import tkinter as tk
from tkinter import ttk,messagebox
from tkcalendar import DateEntry  # Importar DateEntry
from modelos.SmartCard import *
from datetime import datetime,date
from formularios.form_reservar import FormularioReservar
import util.util_ventana as util_ventana
import util.metodos_comunes as comun
from modelos.Alquiler import *
from modelos.Barco import *  





class MiReserva:
    def __init__(self, panel_principal):
        # Configuración del panel principal
        self.panel_principal = panel_principal


        self.idReserva = CSmartCard().read_card(0xBB,0x05)
        self.idReserva = self.limpiar_Campo(self.idReserva)

        self.nSocio = CSmartCard().read_card(0x73,0x0A)
        self.nSocio = self.limpiar_Campo(self.nSocio)

        self.crear_elementos()


    def crear_elementos(self):
         # Título
        ttk.Label(self.panel_principal, text="Reserva Actual", font=("Arial", 16)).pack(pady=10)       

        # Obtener la información de la reserva desde la función
        self.info_reserva = self.obtener_reserva_actual()

        # Crear y mostrar los detalles de la reserva
        for campo, valor in self.info_reserva.items():
            if "Fecha" in campo:
                self.crear_campo_fecha(campo, valor)
            else:
                self.crear_detalle(campo, valor)
        
        if(self.idReserva == ''):

            # Botón para guardar cambios
            ttk.Button(self.panel_principal, text="Crear Reserva", command= self.abrir_panel_reservas).pack(pady=10)
        
        else:
            ttk.Button(self.panel_principal, text="Guardar Reserva", command= self.guardar_cambios).pack(pady=10)
            ttk.Button(self.panel_principal, text="Eliminar Reserva", command= self.eliminar_alquiler).pack(pady=10)


    def crear_detalle(self, campo, valor):
        """Función auxiliar para crear etiquetas de campo y valor en la interfaz."""
        if "Separador" in campo:  # Detecta cualquier campo que empiece con "Separador"
            frame = ttk.Frame(self.panel_principal, height=10)  # Altura para el espacio en blanco
            frame.pack(pady=5)
            return
        frame = ttk.Frame(self.panel_principal)
        frame.pack(pady=5, padx=10, fill="x")
        ttk.Label(frame, text=f"{campo}", font=("Arial", 10)).pack(side="left", padx=5)
        ttk.Label(frame, text=valor, font=("Arial", 10, "bold")).pack(side="right", padx=5)


    def crear_campo_fecha(self, campo, valor):
        """Función auxiliar para crear un campo de fecha editable con DateEntry en la interfaz."""
        frame = ttk.Frame(self.panel_principal)
        frame.pack(pady=5, padx=10, fill="x")

        ttk.Label(frame, text=f"{campo}:", font=("Arial", 10)).pack(side="left", padx=5)
        
        # Crear DateEntry para seleccionar fechas
        fecha_entry = DateEntry(frame, font=("Arial", 10), date_pattern="yyyy-mm-dd")
        fecha_entry.set_date(valor)  # Establecer la fecha inicial
        fecha_entry.pack(side="right", padx=5)

        # Guardamos la referencia del campo editable
        if campo == "Fecha de Inicio":
            self.fecha_inicio_entry = fecha_entry
        elif campo == "Fecha de Finalización":
            self.fecha_fin_entry = fecha_entry

    def guardar_cambios(self):

        # Obtener las fechas como cadenas desde las entradas
        fecha_inicio_str = self.fecha_inicio_entry.get()
        fecha_fin_str = self.fecha_fin_entry.get()

        # Convertir las cadenas a objetos date
        self.fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        self.fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

        fecha_hoy = date.today()

        if  self.fecha_fin < self.fecha_inicio:
            messagebox.showinfo("Informacion", "La fecha de fin no puede ser más pequeña que la de inicio")
            return
        
        if fecha_hoy > self.fecha_inicio and fecha_hoy > self.fecha_fin:
            messagebox.showinfo("Información", f"La fecha de reserva ha de ser mayor que el día de hoy ({fecha_hoy})")
            return
        
        filas = CBarcos.estaAlquilado(self.MMSI,self.fecha_inicio,self.fecha_fin,self.idReserva)

        if filas != 0:
                messagebox.showinfo("Informacion", "El barco seleccionado está reservado para esas fechas")
                return
        else:

            fecha_inicio_Tarjeta = datetime.strptime(self.Inicio, "%Y-%m-%d").date()
            fecha_fin_Tarjeta = datetime.strptime(self.Fin, "%Y-%m-%d").date()
            
            if(fecha_inicio_Tarjeta >= fecha_hoy and fecha_fin_Tarjeta >= fecha_hoy):
                CAlquiler.actualizarReserva(self.idReserva,self.fecha_inicio, self.fecha_fin)
                self.actualizarFechas()
                self.actualizar_interfaz()
                messagebox.showinfo("Informacion", "Actualizacion con exito")
                return
            else:
                Id_Reserva = CBarcos.CrearAlquiler(self.MMSI, self.nSocio, self.fecha_inicio, self.fecha_fin)
                self.idReserva = Id_Reserva
                Id_Reserva = str(Id_Reserva)

                Id_Reserva_H = comun.ascii_a_hexadecimal(Id_Reserva)
                CSmartCard().write_card(0xBB,0x05,[0x2A]*5)
                CSmartCard().write_card(0xBB,len(Id_Reserva_H),Id_Reserva_H)

                self.actualizarFechas()

                self.actualizar_interfaz()

                messagebox.showinfo("Informacion", "Reserva creada con exito")
                return

    def actualizar_interfaz(self):
        # Limpia la interfaz actual
        for widget in self.panel_principal.winfo_children():
            widget.destroy()
        
        self.crear_elementos()

    def obtener_reserva_actual(self):

        nombre = CSmartCard().read_card(0x27,0x09)
        nombre = self.limpiar_Campo(nombre)

        ap1 = CSmartCard().read_card(0x40,0x10)
        ap1 = self.limpiar_Campo(ap1)

        ap2 = CSmartCard().read_card(0x60,0x10)
        ap2 = self.limpiar_Campo(ap2)

        apellidos = ap1+" "+ap2


        if(self.idReserva == ''):

            return {
                "Numero de Socio:": self.nSocio,
                "Nombre del Socio:": nombre,
                "Apellidos del Socio:": apellidos,
                "Separador1":"",
                "Id reserva:" : "No tiene ninguna reserva"
            }

        else:
        
            MMSI = CSmartCard().read_card(0x95,0x0B)
            self.MMSI = self.limpiar_Campo(MMSI)

            Inicio = CSmartCard().read_card(0xE7,0x09)
            Inicio = self.limpiar_Campo(Inicio)
            self.Inicio = self.modificar_fecha(Inicio)

            Fin = CSmartCard().read_card(0xF4,0x0C)
            Fin = self.limpiar_Campo(Fin)
            self.Fin = self.modificar_fecha(Fin)
            
            
            return {
                "Numero de Socio:": self.nSocio,
                "Nombre del Socio:": nombre,
                "Apellidos del Socio:": apellidos,
                "Separador1":"",
                "Id de la reserva:": self.idReserva,
                "MMSI del barco alquilado:" : self.MMSI,
                "Separador2":"",
                "Fecha de Inicio": self.Inicio,
                "Fecha de Finalización": self.Fin
            }
    
    def limpiar_Campo(self,valor):
        indice = valor.find('*')
        if indice != -1:  # Si hay un asterisco en la cadena
            Campo = valor[:indice]
        else:
            Campo = valor
        
        
        return Campo
    
    def modificar_fecha(self,fecha_original):
        # Convertir a objeto datetime
        fecha_objeto = datetime.strptime(fecha_original, "%d/%m/%y")

        # Formatear al nuevo formato YYYY-MM-DD
        fecha_nueva = fecha_objeto.strftime("%Y-%m-%d")

        return fecha_nueva

    def abrir_panel_reservas(self):
        util_ventana.limpiar_panel(self.panel_principal)
        FormularioReservar(self.panel_principal,self.nSocio)

    def actualizarFechas(self):
        fecha_formateada = self.fecha_inicio.strftime("%d/%m/%y")
        Inicio_H = comun.ascii_a_hexadecimal(fecha_formateada)
        CSmartCard().write_card(0xE7,0x08,[0x2A]*8)
        CSmartCard().write_card(0xE7,0x08,Inicio_H)

        fecha_formateada = self.fecha_fin.strftime("%d/%m/%y")
        Fin_H = comun.ascii_a_hexadecimal(fecha_formateada)
        CSmartCard().write_card(0xF4,0x08,[0x2A]*8)
        CSmartCard().write_card(0xF4,0x08,Fin_H)

    def eliminar_alquiler(self):
        CAlquiler.eliminarAlquiler(self.idReserva)  
        CSmartCard().write_card(0xBB,0x05,[0x2A]*5)
        self.idReserva = ''
        self.actualizar_interfaz()