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
# Importamos las nuevas funciones de database_utils
from Modules.database_utils import (
    fetch_data_from_database,
    fetch_data_operadores,
    fetch_operators_list
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import numpy as np
from PyQt6 import QtCore
from matplotlib.patches import FancyBboxPatch

from Modules.graficos import generar_graficos #importa los graficos desde  Modules

def get_resource_path(file_name, folder='Source'):
    """
    Obtiene la ruta de los archivos (íconos, imágenes) en el directorio de recursos.
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
        
        # Layout para los controles (parte superior)
        top_layout = QHBoxLayout()

        # 1) ComboBox principal para seleccionar tipo de informe
        self.informe_selector = QComboBox(self)
        self.informe_selector.addItems([
            "Informe de Altas", 
            "Informe por Categoria", 
            "Novedades de Beneficios",
            "Informe de Operadores"  # <-- NUEVO
        ])
        self.informe_selector.setStyleSheet("font-size: 12px; font-weight: bold; padding: 2px; color:#0A2A35;")
        self.informe_selector.currentIndexChanged.connect(self.update_grafico_options)
        top_layout.addWidget(self.informe_selector)
        
        # 2) Fecha de Inicio
        self.fecha_inicio_label = QLabel("Fecha Inicial:")
        self.fecha_inicio_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.fecha_inicio_label)
        
        self.fecha_inicio_input = QDateEdit(self)
        self.fecha_inicio_input.setCalendarPopup(True)
        self.fecha_inicio_input.setDate(QDate.currentDate())
        self.fecha_inicio_input.setStyleSheet("font-size: 12px; padding: 2px; margin: 0px;")
        top_layout.addWidget(self.fecha_inicio_input)
        
        # 3) Fecha de Fin
        self.fecha_fin_label = QLabel("Fecha Final:")
        self.fecha_fin_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.fecha_fin_label)
        
        self.fecha_fin_input = QDateEdit(self)
        self.fecha_fin_input.setCalendarPopup(True)
        self.fecha_fin_input.setDate(QDate.currentDate())
        self.fecha_fin_input.setStyleSheet("font-size: 12px; padding: 2px; margin: 0px;")
        top_layout.addWidget(self.fecha_fin_input)

        # 4) NUEVO: Label y ComboBox para Operador
        self.operator_label = QLabel("Operador:")
        self.operator_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.operator_label)

        self.operator_combo = QComboBox(self)
        self.operator_combo.setStyleSheet("font-size: 12px; padding: 2px; margin: 0px;")
        top_layout.addWidget(self.operator_combo)

        # 5) NUEVO: Label y ComboBox para Letra
        self.letra_label = QLabel("Letra:")
        self.letra_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.letra_label)

        self.letra_combo = QComboBox(self)
        self.letra_combo.setStyleSheet("font-size: 12px; padding: 2px; margin: 0px;")
        # Agregamos las opciones para filtrar letra. 'T' = todas
        self.letra_combo.addItem("Todas", "T")
        self.letra_combo.addItem("E", "E")
        self.letra_combo.addItem("K", "K")
        self.letra_combo.addItem("V", "V")
        top_layout.addWidget(self.letra_combo)

        # Por defecto, ocultamos estos controles hasta que se seleccione “Informe de Operadores”
        self.operator_label.hide()
        self.operator_combo.hide()
        self.letra_label.hide()
        self.letra_combo.hide()
        
        # 6) Botón Generar Informe
        self.btn_generar = QPushButton(self)
        self.btn_generar.setIcon(QIcon(get_resource_path('generar.png')))
        self.btn_generar.setIconSize(QtCore.QSize(50, 50))
        self.btn_generar.setToolTip('Generar Informe')
        self.btn_generar.clicked.connect(self.generar_informe)
        top_layout.addWidget(self.btn_generar)

        # 7) Botón Guardar en Excel
        self.btn_guardar = QPushButton(self)
        self.btn_guardar.setIcon(QIcon(get_resource_path('toexcel2.png')))
        self.btn_guardar.setIconSize(QtCore.QSize(50, 50))
        self.btn_guardar.setToolTip('Guardar en Excel')
        self.btn_guardar.clicked.connect(self.guardar_en_excel)
        top_layout.addWidget(self.btn_guardar)

        # 8) Botón Mostrar Gráficos
        self.btn_graficos = QPushButton(self)
        self.btn_graficos.setIcon(QIcon(get_resource_path('graphics.png')))
        self.btn_graficos.setIconSize(QtCore.QSize(50, 50))
        self.btn_graficos.setToolTip('Generar Gráficos')
        self.btn_graficos.clicked.connect(self.mostrar_graficos)
        top_layout.addWidget(self.btn_graficos)

        # 9) Botón Exportar Gráfico
        self.btn_exportar_grafico = QPushButton(self)
        self.btn_exportar_grafico.setIcon(QIcon(get_resource_path('save.png')))
        self.btn_exportar_grafico.setIconSize(QtCore.QSize(50, 50))
        self.btn_exportar_grafico.setToolTip('Exportar Gráfico')
        self.btn_exportar_grafico.clicked.connect(self.exportar_grafico)
        top_layout.addWidget(self.btn_exportar_grafico)

        # Añadir el layout de la parte superior al layout principal
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
        self.timer.timeout.connect(self.actualizar_informacion)

        # Por último, cargamos la lista de operadores (aunque estén ocultos inicialmente)
        self.load_operators_list()

    def load_operators_list(self):
        """
        Carga la lista de operadores desde la vista v_personal_jub
        y la asigna al combo de operadores.
        """
        df_ops = fetch_operators_list()
        if df_ops.empty:
            print("No se pudo cargar la lista de operadores o está vacía.")
            return
        
        self.operator_combo.clear()
        for index, row in df_ops.iterrows():
            codigo = row['Codigo']
            descripcion = row['descripcion']
            # El segundo parámetro es 'userData', para obtenerlo con currentData().
            self.operator_combo.addItem(descripcion, codigo)

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
            # Definimos la lógica para cada tipo de informe
            if informe_tipo == "Informe de Altas":
                procedure_name = "Will_ObtenerDatosParaInforme2024V3"
                self.df = fetch_data_from_database(fecha_inicio, fecha_fin, procedure_name)

            elif informe_tipo == "Informe por Categoria":
                procedure_name = "Will_ObtenerDatosParaInforme2024V4"
                self.df = fetch_data_from_database(fecha_inicio, fecha_fin, procedure_name)

            elif informe_tipo == "Novedades de Beneficios":
                procedure_name = "Will_novedades_altasv1"
                self.df = fetch_data_from_database(fecha_inicio, fecha_fin, procedure_name)

            elif informe_tipo == "Informe de Operadores":
                # Tomamos el código y la letra seleccionada
                codigo_operador = self.operator_combo.currentData()
                letra = self.letra_combo.currentData()
                # Llamamos al procedimiento para Informe de Operadores
                self.df = fetch_data_operadores(fecha_inicio, fecha_fin, codigo_operador, letra)

            QApplication.restoreOverrideCursor()

            if self.df is None or self.df.empty:
                self.show_message_box("Información", "No se encontraron datos para las fechas seleccionadas.")
                self.total_registros_label.setText("Total de registros: 0")
                return
            
            # Limpiar tabla y recargar
            self.informe_table.setRowCount(0)
            self.informe_table.setColumnCount(0)

            self.informe_table.setSortingEnabled(False)
            self.informe_table.clearContents()
            self.informe_table.setRowCount(len(self.df))
            self.informe_table.setColumnCount(len(self.df.columns))
            self.informe_table.setHorizontalHeaderLabels(self.df.columns)
            
            for i, row in self.df.iterrows():
                for j, cell in enumerate(row):
                    self.informe_table.setItem(i, j, QTableWidgetItem(str(cell)))

            self.informe_table.setSortingEnabled(True)

            # Actualizar el total de registros
            self.total_registros_label.setText(f"Total de registros: {len(self.df)}")

        except Exception as e:
            QApplication.restoreOverrideCursor()
            self.show_message_box("Error", f"Error al generar el informe: {str(e)}")
 # :::::::::::::: GUARDA EN EXCEL EL INFORME REALIZADO :::::::::::::::::::::::::   
    def guardar_en_excel(self):
        """
        Guarda el informe actual en un archivo Excel,
        usando un nombre sugerido basado en el tipo de informe y rango de fechas.
        """
        if not hasattr(self, 'df') or self.df.empty:
            self.show_message_box("Error", "Primero debe generar un informe.")
            return

        # Obtener el tipo de informe y formatear las fechas
        informe_tipo = self.informe_selector.currentText().replace(' ', '_')  # opcional: reemplaza espacios
        fecha_inicio_str = self.fecha_inicio_input.date().toString("yyyyMMdd")
        fecha_fin_str = self.fecha_fin_input.date().toString("yyyyMMdd")

        # Construir un nombre sugerido
        proposed_filename = f"{informe_tipo}_{fecha_inicio_str}_al_{fecha_fin_str}.xlsx"

        # Desplegar el cuadro de diálogo con el nombre sugerido
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Informe en Excel",
            proposed_filename,   # Nombre sugerido
            "Excel Files (*.xlsx);;All Files (*)"
        )
        if not file_path:  # El usuario canceló el diálogo
            return

        # Guardar en Excel
        try:
            self.df.to_excel(file_path, index=False)  # Requiere openpyxl instalado
            self.show_message_box("Éxito", f"Informe guardado en: {file_path}")
        except Exception as e:
            self.show_message_box("Error", f"Error al guardar el informe: {str(e)}")

# ::::::::::::::::::::::: FUNCIÓN DEL MODULO QUE CREA LOS GRAFICOS Y LOS DIBUJA EN LA INTERZAR PRINCIPAL :::::::::::::::::::::
    def mostrar_graficos(self):
        """
        Muestra gráficos según el tipo de informe y gráfico seleccionados,
        usando la función generar_graficos(...) del módulo 'graficos.py'.
        """
        if not hasattr(self, 'df') or self.df.empty:
            self.show_message_box("Error", "Primero debe generar un informe para mostrar gráficos.")
            return
        
        # Tomamos el informe y el tipo de gráfico elegido
        informe_tipo = self.informe_selector.currentText()
        tipo_grafico = self.combo_tipo_grafico.currentText()

        try:
            # Llamamos la función que hace todo el trabajo de dibujar
            generar_graficos(
                df=self.df,
                informe_tipo=informe_tipo,
                tipo_grafico=tipo_grafico,
                canvas=self.canvas
            )
        except KeyError as e:
            self.show_message_box("Error", f"Error al generar el gráfico: {str(e)}")
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
        Actualiza la lista de gráficos disponibles y 
        muestra/oculta los combos de operador y letra 
        dependiendo del tipo de informe seleccionado.
        """
        informe_tipo = self.informe_selector.currentText()
        self.combo_tipo_grafico.clear()

        # Si es "Informe de Operadores", mostramos combos y agregamos una opción de gráfico (si quisieras)
        if informe_tipo == "Informe de Operadores":
            self.operator_label.show()
            self.operator_combo.show()
            self.letra_label.show()
            self.letra_combo.show()
            # Podrías añadir un gráfico para este informe, si lo deseas
            # self.combo_tipo_grafico.addItem("Gráfico Operadores - Ejemplo")
        else:
            # En cualquier otro informe, ocultamos los combos
            self.operator_label.hide()
            self.operator_combo.hide()
            self.letra_label.hide()
            self.letra_combo.hide()

            # Y cargamos las opciones de gráfico habituales
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
                background-color: #3F9F86;
                color: #34433F;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #add8e6;
                color: #333333;
                border: none;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #87cefa;
            }
        """)
        msg_box.exec()

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path('wolf.png')))
    ex = InformeApp()
    ex.show()
    sys.exit(app.exec())


#pyinstaller --onefile --windowed --icon=wolf.ico --add-data "Source/wolf.png;Source" --add-data "Source/generar.png;Source" --add-data "Source/toexcel2.png;Source" --add-data "Source/graphics.png;Source" --add-data "Source/save.png;Source" --add-data "Modules/styles.py;Modules" --add-data "Modules/database_utils.py;Modules" --distpath "C:/My Software Folder" informesv4.py  

#pyinstaller --onefile --windowed --icon=wolf.ico --add-data "Source/wolf.png;Source" --add-data "Source/generar.png;Source" --add-data "Source/toexcel2.png;Source" --add-data "Source/graphics.png;Source" --add-data "Source/save.png;Source" --add-data "Modules/styles.py;Modules" --add-data "Modules/database_utils.py;Modules" --add-data "Modules/graficos.py;Modules" --distpath "C:/My Software Folder" informes_v4.py
"""
pyinstaller --clean --onefile --windowed --icon=wolf.ico `
--add-data "Source/wolf.png;Source" `
--add-data "Source/generar.png;Source" `
--add-data "Source/toexcel2.png;Source" `
--add-data "Source/graphics.png;Source" `
--add-data "Source/save.png;Source" `
--add-data "Modules/styles.py;Modules" `
--add-data "Modules/database_utils.py;Modules" `
--add-data "Modules/graficos.py;Modules" `
--hidden-import pandas `
--hidden-import pandas._libs `
--collect-submodules pandas `
--collect-data pandas `
--exclude pandas.tests `
--distpath "C:/My Software Folder" informes_v4.py


"""