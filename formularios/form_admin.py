import tkinter as tk
from tkinter import ttk
from modelos.Cliente import *
from formularios.form_admin_flota import FormularioFlota
from formularios.form_admin_socios import FormularioSocios




class PanelAdmin:

    def __init__(self, panel_principal):

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
        self.tab_flota = ttk.Frame(self.notebook)
        self.tab_usuario = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_flota, text="\U00002693 Administrar Flota")
        self.notebook.add(self.tab_usuario, text="\U0001F465 Administrar Usuarios")

        # Configurar las pestañas
        self.crear_tab_flota()
        self.crear_tab_usuarios()


    def crear_tab_flota(self):
        FormularioFlota(self.tab_flota)

    def crear_tab_usuarios(self):
        FormularioSocios(self.tab_usuario)

