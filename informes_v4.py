import sys
import os
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QDateEdit, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QFileDialog, QComboBox, QCheckBox
)
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QDate, Qt, QTimer
from Modules.styles import apply_styles
from Modules.database_utils import fetch_data_from_database  # Utiliza el módulo existente para la conexión a la base de datos
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import numpy as np
from PyQt6 import QtCore
from matplotlib.patches import FancyBboxPatch

#pyinstaller --onefile --windowed --icon=wolf.ico --add-data "Source/wolf.png;Source" --add-data "Source/generar.png;Source" --add-data "Source/toexcel2.png;Source" --add-data "Source/graphics.png;Source" --add-data "Source/save.png;Source" --add-data "Modules/styles.py;Modules" --add-data "Modules/database_utils.py;Modules" --distpath "C:/My Software Folder" informesv4.py

def get_resource_path(file_name, folder='Source'):
    """
    Obtiene la ruta de los archivos (íconos, imágenes) en el directorio de recursos.
    
    :param file_name: El nombre del archivo (ej. 'wolf.png', 'fondo.jpg')
    :param folder: El nombre de la carpeta donde se encuentran los recursos (ej. 'Source')
    :return: Ruta absoluta del archivo de recurso.
    """
    if hasattr(sys, '_MEIPASS'):
        # Cuando está ejecutándose en un ejecutable compilado con PyInstaller
        return os.path.join(sys._MEIPASS, folder, file_name)
    else:
        # Cuando se ejecuta en modo de desarrollo
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), folder, file_name)


class InformeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Configuración de la interfaz
        self.setWindowTitle('Generador de Informes')
        self.setGeometry(100, 100, 1200, 700)
        self.setObjectName("mainContainer")
        
        # Aplicar estilos personalizados
        apply_styles(self)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Layout para los botones e inputs
        top_layout = QHBoxLayout()
        
        # ComboBox para seleccionar tipo de informe
        self.informe_selector = QComboBox(self)
        self.informe_selector.addItems(["Informe de Altas", "Informe por Categoria", "Novedades de Beneficios"])
        self.informe_selector.setStyleSheet("font-size: 12px; font-weight: bold; padding: 2px; color:#0A2A35;")
        self.informe_selector.currentIndexChanged.connect(self.update_grafico_options)  # Actualizar opciones de gráficos según el informe seleccionado
        top_layout.addWidget(self.informe_selector)
        
        # Sección de Fecha de Inicio
        self.fecha_inicio_label = QLabel("Fecha Inicial:")
        self.fecha_inicio_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.fecha_inicio_label)
        
        self.fecha_inicio_input = QDateEdit(self)
        self.fecha_inicio_input.setCalendarPopup(True)
        self.fecha_inicio_input.setDate(QDate.currentDate())
        self.fecha_inicio_input.setStyleSheet("font-size: 12px; padding: 2px; margin: 0px;")
        top_layout.addWidget(self.fecha_inicio_input)
        
        # Sección de Fecha de Fin
        self.fecha_fin_label = QLabel("Fecha Final:")
        self.fecha_fin_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.fecha_fin_label)
        
        self.fecha_fin_input = QDateEdit(self)
        self.fecha_fin_input.setCalendarPopup(True)
        self.fecha_fin_input.setDate(QDate.currentDate())
        self.fecha_fin_input.setStyleSheet("font-size: 12px; padding: 2px; margin: 0px;")
        top_layout.addWidget(self.fecha_fin_input)
        
        
        self.btn_generar = QPushButton(self)
        self.btn_generar.setIcon(QIcon(get_resource_path('generar.png')))  # Cargar el icono desde 'Source/generar.png'
        self.btn_generar.setIconSize(QtCore.QSize(50, 50))  # Ajustar el tamaño del icono (Ancho, Alto)
        self.btn_generar.setToolTip('Generar Informe')  # Mostrar el tooltip al pasar el mouse
        self.btn_generar.clicked.connect(self.generar_informe)
        top_layout.addWidget(self.btn_generar)

        self.btn_guardar = QPushButton(self)
        self.btn_guardar.setIcon(QIcon(get_resource_path('toexcel2.png')))  # Cargar el icono desde 'Source/save.png'
        self.btn_guardar.setIconSize(QtCore.QSize(50, 50))  # Ajustar el tamaño del icono (Ancho, Alto)
        self.btn_guardar.setToolTip('Guardar en Excel')  # Tooltip
        self.btn_guardar.clicked.connect(self.guardar_en_excel)
        top_layout.addWidget(self.btn_guardar)

        self.btn_graficos = QPushButton(self)
        self.btn_graficos.setIcon(QIcon(get_resource_path('graphics.png')))  # Cargar el icono desde 'Source/graphics.png'
        self.btn_graficos.setIconSize(QtCore.QSize(50, 50))  # Ajustar el tamaño del icono (Ancho, Alto)
        self.btn_graficos.setToolTip('Generar Gráficos')  # Tooltip
        self.btn_graficos.clicked.connect(self.mostrar_graficos)
        top_layout.addWidget(self.btn_graficos)

        self.btn_exportar_grafico = QPushButton(self)
        self.btn_exportar_grafico.setIcon(QIcon(get_resource_path('save.png')))  # Cargar el icono desde 'Source/toexcel.png'
        self.btn_exportar_grafico.setIconSize(QtCore.QSize(50, 50))  # Ajustar el tamaño del icono (Ancho, Alto)
        self.btn_exportar_grafico.setToolTip('Exportar Gráfico')  # Tooltip
        self.btn_exportar_grafico.clicked.connect(self.exportar_grafico)
        top_layout.addWidget(self.btn_exportar_grafico)

        # Añadir el layout de botones e inputs al layout principal
        main_layout.addLayout(top_layout)
        
        # Crear las pestañas para la parte inferior
        self.tabs = QTabWidget()
        self.tab_informes = QWidget()
        self.tab_graficos = QWidget()
        
        self.tabs.addTab(self.tab_informes, "Informe")
        self.tabs.addTab(self.tab_graficos, "Gráficos")
        
        # Configuración de layout para la pestaña de informes
        self.informe_layout = QVBoxLayout(self.tab_informes)
        
        # Tabla para mostrar el informe
        self.informe_table = QTableWidget(self)
        self.informe_layout.addWidget(self.informe_table)

        # Añadir el label para mostrar el total de registros
        self.total_registros_label = QLabel("Total de registros: 0")
        self.total_registros_label.setStyleSheet("font-size: 12px; color: #333;")
        self.informe_layout.addWidget(self.total_registros_label)
        
        # Configuración de layout para la pestaña de gráficos
        self.graficos_layout = QVBoxLayout(self.tab_graficos)
        
        # Opciones de filtro y tipo de gráfico
        self.filter_layout = QHBoxLayout()
        self.combo_tipo_grafico = QComboBox()
        self.combo_tipo_grafico.setStyleSheet("font-size: 12px; color: #333;")
        self.filter_layout.addWidget(self.combo_tipo_grafico)
        
        self.checkbox_actualizar = QCheckBox("Actualización en Tiempo Real")
        self.checkbox_actualizar.setStyleSheet("font-size: 12px; color: #333;")
        self.checkbox_actualizar.stateChanged.connect(self.toggle_actualizacion_tiempo_real)
        self.filter_layout.addWidget(self.checkbox_actualizar)
        
        self.graficos_layout.addLayout(self.filter_layout)
        
        # Área de gráficos usando Matplotlib
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.graficos_layout.addWidget(self.canvas)

        # Agregar las pestañas al layout principal
        main_layout.addWidget(self.tabs)
        
        self.setLayout(main_layout)
        
        # Timer para actualización en tiempo real
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_informacion)  # Actualiza datos y gráficos periódicamente

    def actualizar_informacion(self):
        """
        Actualiza los datos de la tabla y el gráfico en tiempo real.
        """
        self.generar_informe()
        self.mostrar_graficos()

    def generar_informe(self):
        """
        Genera el informe según el tipo seleccionado y las fechas ingresadas.
        """
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))

        fecha_inicio = self.fecha_inicio_input.date().toString('yyyy-MM-dd')
        fecha_fin = self.fecha_fin_input.date().toString('yyyy-MM-dd')
        informe_tipo = self.informe_selector.currentText()
        
        try:
            if informe_tipo == "Informe de Altas":
                procedure_name = "Will_ObtenerDatosParaInforme2024V3"
            elif informe_tipo == "Informe por Categoria":
                procedure_name = "Will_ObtenerDatosParaInforme2024V4"
            elif informe_tipo == "Novedades de Beneficios":
                procedure_name = "Will_novedades_altasv1"
            
            # Usar fetch_data_from_database para ejecutar la consulta y obtener los datos
            self.df = fetch_data_from_database(fecha_inicio, fecha_fin, procedure_name)
            QApplication.restoreOverrideCursor()  # Restaurar el cursor
            if self.df is None or self.df.empty:
                self.show_message_box("Información", "No se encontraron datos para las fechas seleccionadas.")
                self.total_registros_label.setText("Total de registros: 0")
                return
            
            # Asegurarse de que la tabla está completamente limpia antes de cargar nuevos datos
            self.informe_table.setRowCount(0)
            self.informe_table.setColumnCount(0)

            self.informe_table.setSortingEnabled(False)  # Deshabilitar la ordenación temporalmente
            self.informe_table.clearContents()  # Limpiar contenido de la tabla antes de actualizar
            self.informe_table.setRowCount(len(self.df))
            self.informe_table.setColumnCount(len(self.df.columns))
            self.informe_table.setHorizontalHeaderLabels(self.df.columns)
            
            for i, row in self.df.iterrows():
                for j, cell in enumerate(row):
                    self.informe_table.setItem(i, j, QTableWidgetItem(str(cell)))

            self.informe_table.setSortingEna
            self.informe_table.setSortingEnabled(True)  # Habilitar ordenación después de cargar los datos
            # Rehabilitar la ordenación después de cargar los datos

            # Actualizar el total de registros en el QLabel
            self.total_registros_label.setText(f"Total de registros: {len(self.df)}")

        except Exception as e:
            QApplication.restoreOverrideCursor()  # Restaurar el cursor en caso de excepción
            self.show_message_box("Error", f"Error al generar el informe: {str(e)}")
    
    def guardar_en_excel(self):
        """
        Guarda el informe actual en un archivo Excel.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Guardar Informe en Excel", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            try:
                if hasattr(self, 'df'):
                    self.df.to_excel(file_path, index=False)
                    self.show_message_box("Éxito", f"Informe guardado en: {file_path}")
                else:
                    self.show_message_box("Error", "Primero debe generar un informe.")
            except Exception as e:
                self.show_message_box("Error", f"Error al guardar el informe: {str(e)}")
    
    def mostrar_graficos(self):
        """
        Muestra gráficos según el tipo de informe y gráfico seleccionados.
        """
        if not hasattr(self, 'df') or self.df.empty:
            self.show_message_box("Error", "Primero debe generar un informe para mostrar gráficos.")
            return
        
        self.canvas.figure.clear()
        
        # Aquí iría el código para generar los gráficos dependiendo del informe
        self.canvas.draw()

        tipo_grafico = self.combo_tipo_grafico.currentText()
        informe_tipo = self.informe_selector.currentText()
        
        try:
            if informe_tipo == "Informe de Altas" and tipo_grafico in [
                "Gráfico de Expedientes", 
                "Gráfico de Operadores", 
                "Gráfico de Actividad", 
                "Gráfico Actividad por Área",
                "Mostrar Todos"
            ]:
                
                def func(pct, allvalues):
                    absolute = int(np.round(pct / 100. * np.sum(allvalues)))
                    return "{:d}\n({:.1f}%)".format(absolute, pct)
        
                # Implementación de gráficos para "Informe de Altas"
                if tipo_grafico == "Gráfico de Expedientes":
                    ax = self.canvas.figure.add_subplot(111)
                      # Obtener los datos de conteo de letras
                    letras_count = self.df['letra'].value_counts()

                      # Colores personalizados para el gráfico
                    colores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

                     # Generar el gráfico de pastel con algunas opciones personalizadas
                    wedges, texts, autotexts = ax.pie(
                        letras_count.values,
                        labels=letras_count.index,
                        autopct=lambda pct: func(pct, letras_count.values), #muestra valores numericos dentro de los circulos
                    #autopct=('%1.1f%%'),  #porcentaje de secciones
                        startangle=90,
                        colors=colores,
                        wedgeprops={'linewidth':1, 'edgecolor': 'white'},
                        textprops={'color':'black', 'fontsize':10}


                    )

                    ax.set_title('Distribución por Letra de Expediente',  fontsize= 12, fontweight='bold')
                    for autotext in autotexts:
                        autotext.set_color('black')
                        autotext.set_fontsize(10)
                        autotext.set_fontweight('bold')

                    centro_circulo = plt.Circle((0,0),0.70, fc='white')
                    ax.add_artist(centro_circulo)

                    ax.axis('equal')

                    self.canvas.figure.tight_layout()

                elif tipo_grafico == "Gráfico de Operadores":
                    ax = self.canvas.figure.add_subplot(111)
                    self.df['Operador'] = self.df['Operador'].str.strip()#para eliminar espacios en blanco
                    operadores_count = self.df['Operador'].value_counts()#datos de conteo
                    cmap = plt.get_cmap('Pastel2')

                    #normalizar los valores de las barras para obtener colors en diferentes intensidades
                    norm = plt.Normalize(operadores_count.min(), operadores_count.max())

                    #crear el gráfico de barras con bordes rounded
                    bars =[]
                    for i, (Operador, valor) in enumerate(operadores_count.items()):
                        #crear barra rectangular con bordes redondeados usando fancyBboxPatch
                        color = cmap(0.2 + 0.8 * norm(valor)) #asignar el color según el valor
                        bar = FancyBboxPatch(
                        (i  - 0.4, 0), 0.8, valor,    
                        boxstyle="round, pad=0.3", #bordes rounded
                        linewidth=2,
                        edgecolor='white',
                        facecolor=color #color basado en el colormap creado
                    )
                        
                        ax.add_patch(bar) #agregar la barra al gráfico
                        bars.append(bar) #color de relleno basado en el colormap

                    #ajustar para que coincidad con las barras
                    ax.set_facecolor('#f0f0f0')

                    ax.set_xlim(-0.5, len(operadores_count) -0.5)
                    ax.set_ylim(0, operadores_count.max() + 2) #margen superior


                    ax.set_title('Actuaciones por Operador', fontsize=12, fontweight='bold')
                    ax.set_xlabel('Operador', fontsize=12)
                    ax.set_ylabel('Cantidad de Actuaciones', fontsize=12)

                                  
                    ax.set_xticks(range(len(operadores_count.index)))
                    ax.set_xticklabels(operadores_count.index, rotation=45, ha='right', fontsize=8)

                    for i, bar in enumerate(bars):
                            yval = operadores_count.values[i]
                            ax.text(i, yval + 0.3, int(yval), ha='center', fontsize=10)


                    self.canvas.figure.tight_layout()
                    self.canvas.draw()   
                    
                
                elif tipo_grafico == "Gráfico de Actividad":
                    ax = self.canvas.figure.add_subplot(111)
                     # Convertir la columna de fechas a datetime
                    self.df['fech_alta'] = pd.to_datetime(self.df['fech_alta'], format='%d-%m-%Y %H:%M', errors='coerce', dayfirst=True)
                    # Eliminar filas con valores nulos
                    self.df = self.df.dropna(subset=['fech_alta'])# Extraer la hora de la columna 'fech_alta'
                    self.df['hora_alta'] = self.df['fech_alta'].dt.hour 
                    horas_count = self.df['hora_alta'].value_counts().sort_index()# Contar la cantidad de ocurrencias por hora y ordenar

                     # Personalización del gráfico de líneas
                    ax.plot(horas_count.index, horas_count.values, marker='o', linestyle='--', color='blue', markersize=8, markerfacecolor='red')

                     # Personalización del título y etiquetas de los ejes
                    ax.set_title('Actividad por Hora', fontsize=16, color='darkgreen')
                    ax.set_xlabel('Hora del Día', fontsize=12, color='darkblue')
                    ax.set_ylabel('Cantidad de Actuaciones', fontsize=12, color='darkblue')

                    for x, y in zip(horas_count.index, horas_count.values):
                            if y == horas_count.max():
                                ax.text(x, y + 2, str(y), fontsize=10, color='black', ha='center', fontweight='bold')  # Desplaza hacia arriba en el máximo
                            else:
                                ax.text(x, y - 2, str(y), fontsize=10, color='black', ha='center', fontweight='bold')  # Desplaza hacia abajo en otros puntos

                      # Personalización de los ejes (límites y colores)
                    ax.set_xlim(horas_count.index.min() - 1, horas_count.index.max() + 1)
                    ax.set_ylim(0, horas_count.values.max() + 5)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['bottom'].set_color('gray')
                    ax.spines['left'].set_color('gray')

                    # Personalización de los ticks (marcas) del eje x e y
                    ax.tick_params(axis='x', colors='purple', labelsize=10)
                    ax.tick_params(axis='y', colors='purple', labelsize=10)
                # Mostrar el gráfico actualizado
                    self.canvas.draw()

                # Gráfico personalizado de "Actividad por Área"
                elif tipo_grafico == "Gráfico Actividad por Área":
                    ax = self.canvas.figure.add_subplot(111)
                    descripcion_count = self.df['Descripcion'].value_counts()

                    cmap = plt.get_cmap('viridis')  # Colormap verde-azul
                    norm = plt.Normalize(descripcion_count.min(), descripcion_count.max())

                    # Dibujar barras con colores del colormap
                    bars = []
                    for i, (descripcion, valor) in enumerate(descripcion_count.items()):
                        color = cmap(0.2 + 0.8 * norm(valor))
                        bar = FancyBboxPatch(
                            (i - 0.4, 0), 0.8, valor,
                            boxstyle="round,pad=0.3", linewidth=1, edgecolor='white', facecolor=color
                        )
                        ax.add_patch(bar)
                        bars.append(bar)

                    ax.set_facecolor('#f0f0f0')
                    ax.set_xlim(-0.5, len(descripcion_count) - 0.5)
                    ax.set_ylim(0, descripcion_count.max() + 2)
                    ax.set_title('Distribución de Actividad por Descripción', fontsize=12, fontweight='bold')
                    ax.set_xlabel('Descripción', fontsize=12)
                    ax.set_ylabel('Cantidad', fontsize=12)

                    ax.set_xticks(range(len(descripcion_count.index)))
                    ax.set_xticklabels(descripcion_count.index, rotation=45, ha='right', fontsize=8)

                    for i, bar in enumerate(bars):
                        yval = descripcion_count.values[i]
                        ax.text(i, yval + 0.3, int(yval), ha='center', fontsize=9)

                    self.canvas.figure.tight_layout()
                    self.canvas.draw()
                
                elif tipo_grafico == "Mostrar Todos":
                    self.canvas.figure.clear()
                    axs = self.canvas.figure.subplots(2, 2)
                    
                    # Gráfico de Expedientes
                    letras_count = self.df['letra'].value_counts()
                    bars = axs[0, 0].bar(letras_count.index, letras_count.values)
                    axs[0, 0].set_title('Distribución por Tipo de Letra')
                    for bar in bars:
                        yval = bar.get_height()
                        axs[0, 0].text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)
                    
                    # Gráfico de Operadores
                    operadores_count = self.df['Operador'].value_counts()
                    bars = axs[0, 1].bar(operadores_count.index, operadores_count.values)
                    axs[0, 1].set_title('Actuaciones por Operador')
                    axs[0, 1].set_xlabel('Operador')
                    axs[0, 1].set_ylabel('Cantidad de Actuaciones')
                    axs[0, 1].tick_params(axis='x', rotation=45, labelsize=8)
                    for bar in bars:
                        yval = bar.get_height()
                        axs[0, 1].text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)
                    
                    # Gráfico de Actividad por Hora
                    self.df['hora_alta'] = pd.to_datetime(self.df['fech_alta'], errors='coerce', dayfirst=True).dt.hour
                    horas_count = self.df['hora_alta'].value_counts().sort_index()
                    axs[1, 0].plot(horas_count.index, horas_count.values, marker='o')
                    axs[1, 0].set_title('Actividad por Hora')
                    axs[1, 0].set_xlabel('Hora del Día')
                    axs[1, 0].set_ylabel('Cantidad de Actuaciones')
                    for x, y in zip(horas_count.index, horas_count.values):
                        axs[1, 0].text(x, y, str(y), fontsize=9, ha='center')
                    
                    # Gráfico Actividad por Descripción en anillo
                    descripcion_count = self.df['Descripcion'].value_counts()
                    bars = axs[1, 1].bar(descripcion_count.index, descripcion_count.values)
                    axs[1, 1].set_title('Distribución de Actividad por Descripción')
                    axs[1, 1].set_xlabel('Descripción')
                    axs[1, 1].set_ylabel('Cantidad')
                    axs[1, 1].tick_params(axis='x', rotation=45, labelsize=8)
                    for bar in bars:
                        yval = bar.get_height()
                        axs[1, 1].text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)
                    
                    self.canvas.figure.tight_layout()
            
            elif informe_tipo == "Informe por Categoria" and tipo_grafico in [
                "Gráfico de Barras por Categoría",
                "Gráfico Circular por Tipo",
                "Mostrar Todos"
            ]:
                # Implementación de gráficos para "Informe por Categoria"
                if tipo_grafico == "Gráfico de Barras por Categoría":
                    ax = self.canvas.figure.add_subplot(111)
                    # Eliminar los espacios en blanco de las etiquetas de categoría
                    self.df['Categoria'] = self.df['Categoria'].str.strip()
                    categoria_count = self.df.groupby('Categoria')['Conteo'].sum().sort_values(ascending=False)

                    # Configuración del colormap
                    cmap = plt.get_cmap('viridis')  # Colormap verde-azul
                    norm = plt.Normalize(categoria_count.min(), categoria_count.max())

                    #crear el grafico de barra usando FancyBboxpatch
                    bars = []
                    for i, (categoria, valor) in enumerate(categoria_count.items()):
                        color = cmap(0.2 + 0.8 * norm(valor))
                        bar = FancyBboxPatch(
                            (i - 0.4, 0), 0.8, valor,
                            boxstyle="round,pad=0.3", linewidth=1, edgecolor="white", facecolor= color
                        )
                        ax.add_patch(bar)
                        bars.append(bar)

                    #configutacion visual del gráfico
                    ax.set_facecolor('#f0f0f0')  # Color de fondo claro
                    ax.set_xlim(-0.5, len(categoria_count) - 0.5)  # Limitar el espacio horizontal
                    ax.set_ylim(0, categoria_count.max() + 2)  # Ajustar el límite del eje y

                    #configuracion de titulos y etiquetas
                    ax.set_title('Totales por Categoría', fontsize=16, fontweight='bold')
                    ax.set_xlabel('Categoría', fontsize=12, labelpad=20)  # Añadir espacio extra debajo del eje x
                    ax.set_ylabel('Cantidad total en el periodo', fontsize=12)

                    #personalizar de los ticks del eje x
                    ax.set_xticks(range(len(categoria_count.index)))
                    ax.set_xticklabels(categoria_count.index, rotation=60, ha='right', fontsize=8, rotation_mode='anchor')

                   
                    #anadir valores encima de cada barra con un desplazamiento
                    for i, bar in enumerate(bars):
                        yval = categoria_count.values[i]
                        ax.text(i, yval + 0.5, int(yval), ha= 'center', fontsize = 9)
                        
                    self.canvas.figure.tight_layout()
                    plt.subplots_adjust(bottom=0.2)  # Aumentar el espacio inferior
                    self.canvas.draw()
                        
                
                elif tipo_grafico == "Gráfico Circular por Tipo":
                    ax = self.canvas.figure.add_subplot(111)
                    tipo_count = self.df['Tipo'].value_counts()
                    ax.pie(tipo_count, labels=tipo_count.index, autopct='%1.1f%%')
                    ax.set_title('Distribución por Tipo')
                
                elif tipo_grafico == "Mostrar Todos":
                    self.canvas.figure.clear()
                    axs = self.canvas.figure.subplots(1, 2)
                    
                    categoria_count = self.df.groupby('Categoria')['Conteo'].sum().sort_values(ascending=False)
                    bars = axs[0].bar(categoria_count.index, categoria_count.values, width=0.6)
                    axs[0].set_title('Totales por Categoría', fontsize=14)
                    axs[0].set_xlabel('Categoría', fontsize=12)
                    axs[0].set_ylabel('Cantidad total en el periodo', fontsize=12)
                    axs[0].set_xticks(range(len(categoria_count.index)))
                    axs[0].set_xticklabels(categoria_count.index, rotation=45, ha='right', fontsize=8)
                    max_conteo = categoria_count.max()
                    axs[0].yaxis.set_major_locator(MaxNLocator(integer=True, nbins=10))
                    axs[0].set_ylim(0, max_conteo + 10)
                    for bar in bars:
                        yval = bar.get_height()
                        axs[0].text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)

                    tipo_count = self.df['Tipo'].value_counts()
                    axs[1].pie(tipo_count, labels=tipo_count.index, autopct='%1.1f%%', startangle=90, labeldistance=1.1)
                    axs[1].set_title('Distribución por Tipo')
                    
                    self.canvas.figure.tight_layout()

                    

            elif informe_tipo == "Novedades de Beneficios" and tipo_grafico =="Gráfico de Altas por Mes":
                ax = self.canvas.figure.add_subplot(111)
                # Agrupar por Año y Mes y contar las ocurrencias (altas por mes)
                altas_por_mes = self.df.groupby(['Anio', 'Mes']).size().reset_index(name='Cantidad')
                # Crear una columna combinada de 'Año-Mes' para el eje X
                altas_por_mes['Periodo'] = altas_por_mes['Anio'].astype(str) + '-' + altas_por_mes['Mes'].astype(str)

                 
                # Crear un colormap basado en los valores de 'Cantidad'
                norm = plt.Normalize(altas_por_mes['Cantidad'].min(), altas_por_mes['Cantidad'].max())
                cmap = plt.cm.plasma  # Puedes cambiarlo a 'viridis', 'coolwarm', 'Blues', etc.

                # Generar el gráfico de barras con los datos agrupados
                bars = ax.bar(
                        altas_por_mes['Periodo'], 
                        altas_por_mes['Cantidad'], 
                        color=cmap(norm(altas_por_mes['Cantidad'])), 
                        edgecolor='black', 
                        linewidth=1.2  # Líneas de borde más visibles
                )

                #configuracion de titulos e etiquetas
                ax.set_title('Cantidad de Altas por Mes', fontsize=16, weight='bold', family='Verdana', color='#333333')
                ax.set_xlabel('Mes', fontsize=12, family='Verdana', color='#333333')
                ax.set_ylabel('Cantidad de Altas', fontsize=12, family='Verdana', color='#333333')


                for bar in bars:
                     yval = bar.get_height()
                     ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)

                 # Añadir un mapa de colores al gráfico como leyenda
                sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
                sm.set_array([])
                cbar = plt.colorbar(sm, ax=ax)
                cbar.set_label('Cantidad', fontsize=12, family='Verdana')

                
                    
                self.canvas.figure.tight_layout()

            self.canvas.draw()
        
        except KeyError as e:
            self.show_message_box("Error", f"Error al generar el gráfico: Columna no encontrada - {str(e)}")
        except Exception as e:
            self.show_message_box("Error", f"Error al generar el gráfico: {str(e)}")
    



    def exportar_grafico(self):
        """
        Exporta el gráfico actual a un archivo PNG.
        """
        file_path, _ = QFileDialog.getSaveFileName(self, "Exportar Gráfico", "", "PNG Files (*.png);;All Files (*)")
        if file_path:
            try:
                self.canvas.figure.savefig(file_path)
                self.show_message_box("Éxito", f"Gráfico exportado en: {file_path}")
            except Exception as e:
                self.show_message_box("Error", f"Error al exportar el gráfico: {str(e)}")
    
    def toggle_actualizacion_tiempo_real(self, state):
        """
        Activa o desactiva la actualización automática de datos y gráficos.
        """
        if state == Qt.CheckState.Checked:
            self.timer.start(60000)  # Actualiza cada 60 segundos (1 minuto)
        else:
            self.timer.stop()
    
    def update_grafico_options(self):
        """
        Actualiza la lista de gráficos disponibles dependiendo del tipo de informe seleccionado.
        """
        informe_tipo = self.informe_selector.currentText()
        self.combo_tipo_grafico.clear()

        if informe_tipo == "Informe de Altas":
            self.combo_tipo_grafico.addItems([
                "Gráfico de Expedientes", 
                "Gráfico de Operadores", 
                "Gráfico de Actividad", 
                "Gráfico Actividad por Área",
                "Mostrar Todos"
            ])
        elif informe_tipo == "Informe por Categoria":
            self.combo_tipo_grafico.addItems([
                "Gráfico de Barras por Categoría",
                "Gráfico Circular por Tipo",
                "Mostrar Todos"
            ])
        elif informe_tipo == "Novedades de Beneficios":
            self.combo_tipo_grafico.addItems([
                "Gráfico de Altas por Mes"
            ])
    
    def show_message_box(self, title, message):
        """
        Muestra una ventana emergente con un mensaje.
        """
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #3F9F86;  /* Fondo blanco para las ventanas emergentes */
                color: #34433F;  /* Texto oscuro */
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #add8e6;  /* Botón celeste claro */
                color: #333333;
                border: none;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #87cefa;  /* Fondo más claro al pasar el ratón por encima */
            }
        """)
        msg_box.exec()

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path('wolf.png')))
    ex = InformeApp()
    ex.show()
    sys.exit(app.exec())
