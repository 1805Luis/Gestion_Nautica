import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modelos.Alquiler import *
from datetime import datetime

class FormularioGraficasDesign():

    def __init__(self, panel_principal,nSocio):    
        self.N_Socio = nSocio       
        self.espacio_grafica = tk.Frame(panel_principal)
        self.espacio_grafica.pack(side=tk.TOP, fill=tk.X, expand=False)
        # Crear 1 subgráfico usando Matplotlib
        figura = Figure(figsize=(9, 5), dpi=100)
        ax1 = figura.add_subplot(111)             
        
        # Ajustar la distribución para agregar espacio de separación en el eje Y
        figura.subplots_adjust(hspace=0.4)

        # Graficar en los subgráficos
        self.grafico1(ax1)

        # Agregar los gráficos a la ventana de Tkinter
        canvas = FigureCanvasTkAgg(figura, master=panel_principal)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def grafico1(self, ax):
        # Obtén el año actual
        anioActual = datetime.now().year

        # Meses del año
        x = list(range(1, 13))  # 1 a 12 para cada mes
        
        # Llamar al método para obtener los datos de alquileres
        resultado = CAlquiler.mostrarHistorico(self.N_Socio, anioActual)

        # Crear un array con 12 ceros
        y = [0] * 12

        # Rellenar el array con los valores de num_alquileres en los meses correspondientes
        for mes, num_alquileres in resultado:
            y[mes - 1] = num_alquileres

        # Crear el gráfico de barras
        ax.bar(x, y, label=f'Número de reservas en {anioActual}', color='blue', alpha=0.7)

        # Configurar títulos y etiquetas
        ax.set_title(f'Reservas por Mes en el Año {anioActual}')
        ax.set_xlabel('Mes')
        ax.set_ylabel('Número de reservas')
        ax.legend()

        # Añadir etiquetas para cada barra
        for i, v in enumerate(y):
            ax.text(x[i] - 0.2, v + 0.1, str(v), color='black')

        # Establecer las etiquetas de los meses en el eje X
        ax.set_xticks(x)
        ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])

        # Añadir cuadrícula
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Ajustar el límite superior del eje Y con un margen adicional
        max_y = max(y)  # Valor máximo de la lista y
        ax.set_ylim(0, max_y + 0.5 if max_y < 10 else max_y * 1.1)  # Añadir margen superior
