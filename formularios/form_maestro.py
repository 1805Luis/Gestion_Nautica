import tkinter as tk
from tkinter import font  #tipo de letra
from config import *
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from formularios.form_info import FormularioInfoDesign
from formularios.form_reservar import FormularioReservar
from formularios.form_perfil import PerfilUsuario
from formularios.form_registro import *
from formularios.form_info_tarjeta import MiReserva
from formularios.form_admin import *
from modelos.SmartCard import *
from modelos.Cliente import *
from util.demon import ComprobaciónTarjeta  # Importa la función desde el archivo demon.py
import time
import threading


class FormularioMaestroDesign(tk.Tk):

    def __init__(self): #self -> es una convención que se utiliza como nombre para el primer parámetro de un método en una clase.
        super().__init__()
        self.title(TITULO_APP)
        self.iconbitmap("./imagenes/logo.ico")

        # Espera hasta que el lector esté disponible
        while True:
            resultado = CSmartCard.HayLector()
            if resultado == 1:
                break  # Sale del bucle si se detecta el lector
            else:
                # Muestra un mensaje de advertencia y verifica si se cierra
                if not messagebox.askretrycancel("Advertencia", "No se detecta ningún lector de tarjetas. Conéctelo y espere."):
                    self.destroy()  # Cierra la aplicación si el usuario cierra el diálogo
                    return  # Sale del constructor y detiene la ejecución
                self.update()   # Permite que la GUI se actualice
                time.sleep(10)  # Espera antes de verificar nuevamente
        
        # Espera hasta que el lector lea una tarjeta
        while True:
            resultado = CSmartCard.HayTarjeta()
            if resultado == True:
                break  # Sale del bucle si se detecta el lector
            else:
                # Muestra un mensaje de advertencia y verifica si se cierra
                if not messagebox.askretrycancel("Advertencia", "No se detecta ninguna tarjeta. Introduzca una y espere."):
                    self.destroy()  # Cierra la aplicación si el usuario cierra el diálogo
                    return  # Sale del constructor y detiene la ejecución
                
                self.update()   # Permite que la GUI se actualice
                time.sleep(10)  # Espera antes de verificar nuevamente


        # Iniciamos el hilo demonio
        demonio = threading.Thread(target=ComprobaciónTarjeta, args=(self,), daemon=True)
        demonio.start()
        
        
        # Abre la ventana de registro primero
        self.nSocio = self.NumeroSocio()
        
        if self.nSocio != 0:  # Si el número de socio es válido, cargar la aplicación completa
            if CClientes.existeSocio(self.nSocio):
                if CClientes.estadoCuenta(self.nSocio):
                    self.inicializar_interfaz()
                else:
                    return
            else:
                self.abrir_ventana_registro()
                #Espera hasta que se complete el registro para cargar la interfaz completa
                self.wait_window(self.ventana_registro)
                self.inicializar_interfaz()       
      
        else:
            self.abrir_ventana_registro()
            #Espera hasta que se complete el registro para cargar la interfaz completa
            self.wait_window(self.ventana_registro)
            self.inicializar_interfaz()       
    

    def abrir_ventana_registro(self):
        CSmartCard().PrepararTarjeta()

        self.ventana_registro = Registro(self)
        self.ventana_registro.grab_set()# Evita interacción con la ventana principal
        

    def inicializar_interfaz(self): #Configuracion general de la ventana inicial

        self.nSocio = self.NumeroSocio()
        
        w,h = 1024,600
        util_ventana.centrar_ventana(self,w,h)

        self.rol = CClientes.rolSocio(self.nSocio)

        self.perfil = self.definirFotoPerfil()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()

    def paneles(self): #Crear panales: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')      

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False) 
        
        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self): #Configuracion del toolbar
        # Configuración de la barra superior
        font_awesome = font.Font(family='Font Awesome', size=12)  # Cambiado el nombre de la fuente

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Más opciones")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral con ícono de tres barras
        self.buttonMenuLateral = tk.Button(
            self.barra_superior,
            text='\u2630',  # Carácter Unicode para las barras en Font Awesome
            font=font_awesome,
            command=self.toggle_panel,
            bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white"
        )
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Crear el botón de cerrar sesión con la imagen
        self.buttonCerrarSesion = tk.Button(
            self.barra_superior,
            text="\u274C Cerrar Sesion",  
            font=("Roboto", 10),
            command=self.cerrar_sesion,  # Aquí colocas la función que se llama al presionar el botón
            bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white"
        )
        self.buttonCerrarSesion.pack(side=tk.RIGHT)

        # Etiqueta de información
        nombre_completo =  CSmartCard().read_card(0x27,0x08)
        indice = nombre_completo.find('*')
        if indice != -1:  # Asegúrate de que hay un asterisco en la cadena
            nombre = nombre_completo[:indice]
        else:
            nombre = nombre_completo 
        saludo = "Bienvenid@, "+nombre
        self.labelInfo = tk.Label(self.barra_superior, text= saludo)

        self.labelInfo.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelInfo.pack(side=tk.RIGHT)

        

    def cerrar_sesion(self):
        self.destroy()  # Cierra la aplicación
    
    def toggle_panel(self): # Alterar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')
    
    def controles_menu_lateral(self): # Configuracion menu lateral
        # Config menu lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='Font Awesome', size=11)

        #Etiqueta de perfil
        self.labelPerfil = tk.Label(
           self.menu_lateral,image=self.perfil,bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side = tk.TOP, pady = 10)

        #Botones del menu lateral
        self.buttonDashBoard = tk.Button(self.menu_lateral)
        self.buttonProfile = tk.Button(self.menu_lateral)
        self.buttonReserva = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)
        self.buttonReservaActual = tk.Button(self.menu_lateral)
        

        

        if(self.rol == "ADMIN"):
            self.buttonAdministrarBarcos = tk.Button(self.menu_lateral)
            self.buttonAdministrarSocios = tk.Button(self.menu_lateral)

            buttons_info = [
            ("Perfil", "\U0001F464", self.buttonProfile,self.abrir_panel_perfil),
            ("Reservar", "\U0001F4C5", self.buttonReserva,self.abrir_panel_reservas),
            ("Reserva Actual", "\U0001F4BE", self.buttonReservaActual,self.abrir_panel_tarjeta),
            ("Administrar", "\u2699", self.buttonAdministrarBarcos,self.abrir_panel_admin),
            ("Info", "\U00002139", self.buttonInfo,self.abrir_panel_info),
            ]
            
        else:
            buttons_info = [
            ("Perfil", "\U0001F464", self.buttonProfile,self.abrir_panel_perfil),
            ("Reservar", "\U0001F4C5", self.buttonReserva,self.abrir_panel_reservas),
            ("Reserva Actual", "\U0001F4BE", self.buttonReservaActual,self.abrir_panel_tarjeta),
            ("Info", "\U00002139", self.buttonInfo,self.abrir_panel_info),
            ]

        

        for text, icon,button,accion in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome,ancho_menu, alto_menu,accion)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu,accion):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu,
                      command = accion)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)
    
    def bind_hover_events(self, button): # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))
    
    def on_enter(self, event, button): # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button): # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')
    
    def controles_cuerpo(self): # Configurar el cuerpo principal
        FormularioReservar(self.cuerpo_principal,self.nSocio)
    
    def abrir_panel_info(self):
        FormularioInfoDesign()
    
    def abrir_panel_reservas(self):
        util_ventana.limpiar_panel(self.cuerpo_principal)
        FormularioReservar(self.cuerpo_principal,self.nSocio)

    def abrir_panel_perfil(self):
        util_ventana.limpiar_panel(self.cuerpo_principal)
        PerfilUsuario(self.cuerpo_principal,self.nSocio,self.perfil)

    def abrir_panel_tarjeta(self):
        util_ventana.limpiar_panel(self.cuerpo_principal)
        MiReserva(self.cuerpo_principal)

    
    def abrir_panel_admin(self):
        util_ventana.limpiar_panel(self.cuerpo_principal)
        PanelAdmin(self.cuerpo_principal)

        


        
   
    def definirFotoPerfil(self): 
        campo = CClientes.mostrarTitulacionSocio(self.nSocio)
        titulacion = campo[0][0].upper()  # Accede al primer elemento de la lista y luego al primer elemento de la tupla

        if titulacion == "LN":
            return util_img.leer_imagen("./imagenes/titulacion/LN.png",(150,150))
        elif titulacion == "PNB":
            return util_img.leer_imagen("./imagenes/titulacion/PNB.png",(150,150))
        elif titulacion == "PER":
            return util_img.leer_imagen("./imagenes/titulacion/PER.png",(100,150))
        elif titulacion == "PY":
            return util_img.leer_imagen("./imagenes/titulacion/PY.png",(200,150))
        elif titulacion == "CY":
            return util_img.leer_imagen("./imagenes/titulacion/CY.png",(150,150))
        
    def NumeroSocio(self):
        nSocio =  CSmartCard().read_card(0x73,0x0A)
        indice = nSocio.find('*')
        if indice != -1:  # Si hay un asterisco en la cadena
            Socio = nSocio[:indice]
        else:
            Socio = nSocio
        
        if Socio != "": 
            Socio = Socio
        else:
            Socio = 0
        
        return Socio



