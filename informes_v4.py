import sys, os, pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QDateEdit, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QFileDialog, QComboBox, QCheckBox
)
from PyQt6.QtGui import QIcon, QCursor, QColor
from PyQt6.QtCore import QDate, Qt, QTimer
from PyQt6 import QtCore
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from Modules.styles import apply_styles
from Modules.database_utils import (
    fetch_data_from_database,
    fetch_data_operadores,
    fetch_operators_list,
    fetch_data_no_params,          # ← nuevo helper
)

from Modules.graficos import generar_graficos


# ---------------------------------------------------------------------------
# Utilidad para recursos (PyInstaller)
# ---------------------------------------------------------------------------

def get_resource_path(file_name, folder="Source"):
    if hasattr(sys, "_MEIPASS"):  # type: ignore[attr-defined]
        return os.path.join(sys._MEIPASS, folder, file_name)  # type: ignore[attr-defined]
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), folder, file_name)


# ---------------------------------------------------------------------------
# App principal
# ---------------------------------------------------------------------------

class InformeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # ------------------------------ UI ------------------------------------
    def initUI(self):
        self.setWindowTitle("Generador de Informes")
        self.setGeometry(100, 100, 1200, 700)
        self.setObjectName("mainContainer")
        apply_styles(self)

        main_layout = QVBoxLayout(self)

        # ---------- barra superior ----------
        top_layout = QHBoxLayout()

        self.informe_selector = QComboBox(self)
        self.informe_selector.addItems([
            "Informe de Altas",
            "Informe por Categoria",
            "Novedades de Beneficios",
            "Inf. de actuaciones gestionadas por Operador",
            "Listado de trámites con Anticipo",          # ← NUEVO
        ])
        self.informe_selector.setStyleSheet(
            "font-size: 12px; font-weight: bold; padding: 2px; color:#0A2A35;"
        )
        self.informe_selector.currentIndexChanged.connect(self.update_grafico_options)
        top_layout.addWidget(self.informe_selector)

        # --- Fechas ---
        self.fecha_inicio_label = QLabel("Fecha Inicial:")
        self.fecha_inicio_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.fecha_inicio_label)

        self.fecha_inicio_input = QDateEdit(self)
        self.fecha_inicio_input.setCalendarPopup(True)
        self.fecha_inicio_input.setDate(QDate.currentDate())
        self.fecha_inicio_input.setStyleSheet("font-size: 12px; padding: 2px;")
        top_layout.addWidget(self.fecha_inicio_input)

        self.fecha_fin_label = QLabel("Fecha Final:")
        self.fecha_fin_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.fecha_fin_label)

        self.fecha_fin_input = QDateEdit(self)
        self.fecha_fin_input.setCalendarPopup(True)
        self.fecha_fin_input.setDate(QDate.currentDate())
        self.fecha_fin_input.setStyleSheet("font-size: 12px; padding: 2px;")
        top_layout.addWidget(self.fecha_fin_input)

        # --- Filtros de operador/letra (se ocultan por defecto) ---
        self.operator_label = QLabel("Operador:")
        self.operator_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.operator_label)

        self.operator_combo = QComboBox(self)
        self.operator_combo.setStyleSheet("font-size: 12px; padding: 2px;")
        top_layout.addWidget(self.operator_combo)

        self.letra_label = QLabel("Letra:")
        self.letra_label.setStyleSheet("font-size: 12px; color: #ffff;")
        top_layout.addWidget(self.letra_label)

        self.letra_combo = QComboBox(self)
        self.letra_combo.setStyleSheet("font-size: 12px; padding: 2px;")
        for cod in ("T", "E", "K", "V"):
            self.letra_combo.addItem(cod if cod != "T" else "Todas", cod)
        top_layout.addWidget(self.letra_combo)

        # Ocultamos por defecto
        self.operator_label.hide()
        self.operator_combo.hide()
        self.letra_label.hide()
        self.letra_combo.hide()

        # --- Botones ---
        self.btn_generar = QPushButton(self)
        self.btn_generar.setIcon(QIcon(get_resource_path("generar.png")))
        self.btn_generar.setIconSize(QtCore.QSize(50, 50))
        self.btn_generar.setToolTip("Generar Informe")
        self.btn_generar.clicked.connect(self.generar_informe)
        top_layout.addWidget(self.btn_generar)

        self.btn_guardar = QPushButton(self)
        self.btn_guardar.setIcon(QIcon(get_resource_path("toexcel2.png")))
        self.btn_guardar.setIconSize(QtCore.QSize(50, 50))
        self.btn_guardar.setToolTip("Guardar en Excel")
        self.btn_guardar.clicked.connect(self.guardar_en_excel)
        top_layout.addWidget(self.btn_guardar)

        self.btn_graficos = QPushButton(self)
        self.btn_graficos.setIcon(QIcon(get_resource_path("graphics.png")))
        self.btn_graficos.setIconSize(QtCore.QSize(50, 50))
        self.btn_graficos.setToolTip("Generar Gráficos")
        self.btn_graficos.clicked.connect(self.mostrar_graficos)
        top_layout.addWidget(self.btn_graficos)

        self.btn_exportar_grafico = QPushButton(self)
        self.btn_exportar_grafico.setIcon(QIcon(get_resource_path("save.png")))
        self.btn_exportar_grafico.setIconSize(QtCore.QSize(50, 50))
        self.btn_exportar_grafico.setToolTip("Exportar Gráfico")
        self.btn_exportar_grafico.clicked.connect(self.exportar_grafico)
        top_layout.addWidget(self.btn_exportar_grafico)

        main_layout.addLayout(top_layout)

        # ---------- Pestañas ----------
        self.tabs = QTabWidget()
        self.tab_informes = QWidget()
        self.tab_graficos = QWidget()
        self.tabs.addTab(self.tab_informes, "Informe")
        self.tabs.addTab(self.tab_graficos, "Gráficos")

        # --- Tab informe ---
        self.informe_layout = QVBoxLayout(self.tab_informes)
        self.informe_table = QTableWidget(self)
        self.informe_layout.addWidget(self.informe_table)
        self.total_registros_label = QLabel("Total de registros: 0")
        self.total_registros_label.setStyleSheet("font-size: 12px; color: #333;")
        self.informe_layout.addWidget(self.total_registros_label)

        # --- Tab gráficos ---
        self.graficos_layout = QVBoxLayout(self.tab_graficos)
        self.filter_layout = QHBoxLayout()
        self.combo_tipo_grafico = QComboBox()
        self.combo_tipo_grafico.setStyleSheet("font-size: 12px; color: #333;")
        self.filter_layout.addWidget(self.combo_tipo_grafico)

        self.checkbox_actualizar = QCheckBox("Actualización en Tiempo Real")
        self.checkbox_actualizar.setStyleSheet("font-size: 12px; color: #333;")
        self.checkbox_actualizar.stateChanged.connect(self.toggle_actualizacion_tiempo_real)
        self.filter_layout.addWidget(self.checkbox_actualizar)
        self.graficos_layout.addLayout(self.filter_layout)

        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.graficos_layout.addWidget(self.canvas)

        main_layout.addWidget(self.tabs)

        # ---------- temporizador ----------
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_informacion)

        # lista de operadores
        self.load_operators_list()


    # ------------------------------ Datos ----------------------------------
    def load_operators_list(self):
        df_ops = fetch_operators_list()
        self.operator_combo.clear()
        for _, row in df_ops.iterrows():
            self.operator_combo.addItem(row["descripcion"], row["Codigo"])

    def generar_informe(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.WaitCursor))
        informe_tipo = self.informe_selector.currentText()

        fecha_inicio = self.fecha_inicio_input.date().toString("yyyy-MM-dd")
        fecha_fin = self.fecha_fin_input.date().toString("yyyy-MM-dd")

        try:
            if informe_tipo == "Informe de Altas":
                self.df = fetch_data_from_database(
                    fecha_inicio, fecha_fin, "Will_ObtenerDatosParaInforme2024V3"
                )

            elif informe_tipo == "Informe por Categoria":
                self.df = fetch_data_from_database(
                    fecha_inicio, fecha_fin, "Will_ObtenerDatosParaInforme2024V4"
                )

            elif informe_tipo == "Novedades de Beneficios":
                self.df = fetch_data_from_database(
                    fecha_inicio, fecha_fin, "Will_novedades_altasv1"
                )

            elif informe_tipo == "Inf. de actuaciones gestionadas por Operador":
                self.df = fetch_data_operadores(
                    fecha_inicio, fecha_fin,
                    self.operator_combo.currentData(),
                    self.letra_combo.currentData()
                )

            elif informe_tipo == "Listado de trámites con Anticipo":
                # SP sin parámetros, base Aportes
                self.df = fetch_data_no_params(
                    procedure_name="Will_anticipo_contador",
                    database="Aportes"
                )

            else:
                self.df = pd.DataFrame()

        except Exception as e:
            self.show_message_box("Error", f"Error al generar el informe: {e}")
            self.df = pd.DataFrame()

        finally:
            QApplication.restoreOverrideCursor()

        # ---- rellenar tabla ----
        if self.df.empty:
            self.show_message_box("Información", "No se encontraron datos.")
            self.total_registros_label.setText("Total de registros: 0")
            self.informe_table.setRowCount(0)
            return

        self.informe_table.setSortingEnabled(False)
        self.informe_table.clearContents()
        self.informe_table.setRowCount(len(self.df))
        self.informe_table.setColumnCount(len(self.df.columns))
        self.informe_table.setHorizontalHeaderLabels(self.df.columns)

        # for row_idx, (_, row) in enumerate(self.df.iterrows()):
        #     for col_idx, value in enumerate(row):
        #         self.informe_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
    
        # ------------------------------------------------------------------
        # Rellenar tabla + colorear filas según MesesAnticipo
        # ------------------------------------------------------------------
        for row_idx, (_, row) in enumerate(self.df.iterrows()):
            # Intentamos leer la columna MesesAnticipo de forma segura
            meses_val_raw = row.get("MesesAnticipo", None)
            try:
                meses_val = int(meses_val_raw) if pd.notna(meses_val_raw) else 0
            except (ValueError, TypeError):
                meses_val = 0

            # Elegir color de fondo
            bg_color = None
            if meses_val == 5:
                bg_color = QColor("#FFF59D")   # amarillo suave
            elif meses_val in (6, 7):
                bg_color = QColor("#FFCC80")   # naranja suave

            # Crear items y aplicarlos a la fila
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                if bg_color is not None:
                    item.setBackground(bg_color)
                self.informe_table.setItem(row_idx, col_idx, item)

        self.informe_table.setSortingEnabled(True)
        self.total_registros_label.setText(f"Total de registros: {len(self.df)}")


    # ------------------------------ Excel ----------------------------------
    def guardar_en_excel(self):
        if not hasattr(self, "df") or self.df.empty:
            self.show_message_box("Error", "Primero genere un informe.")
            return

        informe_tipo = self.informe_selector.currentText().replace(" ", "_")
        today_str = QDate.currentDate().toString("yyyyMMdd")
        fecha_inicio_str = self.fecha_inicio_input.date().toString("yyyyMMdd")
        fecha_fin_str = self.fecha_fin_input.date().toString("yyyyMMdd")

        if informe_tipo == "Listado_de_trámites_con_Anticipo":
            proposed_filename = f"Anticipos_{today_str}.xlsx"
        else:
            proposed_filename = f"{informe_tipo}_{fecha_inicio_str}_al_{fecha_fin_str}.xlsx"

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Informe en Excel",
            proposed_filename, "Excel Files (*.xlsx);;All Files (*)"
        )
        if not file_path:
            return

        try:
            self.df.to_excel(file_path, index=False)
            self.show_message_box("Éxito", f"Informe guardado en:\n{file_path}")
        except Exception as e:
            self.show_message_box("Error", f"No se pudo guardar el archivo:\n{e}")

    # ------------------------------ Gráficos --------------------------------
    def mostrar_graficos(self):
        if not hasattr(self, "df") or self.df.empty:
            self.show_message_box("Error", "Primero genere un informe.")
            return

        generar_graficos(
            df=self.df,
            informe_tipo=self.informe_selector.currentText(),
            tipo_grafico=self.combo_tipo_grafico.currentText(),
            canvas=self.canvas
        )

    def exportar_grafico(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Gráfico", "", "PNG Files (*.png);;All Files (*)"
        )
        if file_path:
            try:
                self.canvas.figure.savefig(file_path)
                self.show_message_box("Éxito", f"Gráfico exportado en:\n{file_path}")
            except Exception as e:
                self.show_message_box("Error", f"No se pudo exportar:\n{e}")

    # ------------------------------ Actualización ---------------------------
    def toggle_actualizacion_tiempo_real(self, state):
        if state == Qt.CheckState.Checked:
            self.timer.start(60_000)
        else:
            self.timer.stop()

    def actualizar_informacion(self):
        self.generar_informe()
        self.mostrar_graficos()

    # ------------------------------ UX dinámica -----------------------------
    def update_grafico_options(self):
        informe_tipo = self.informe_selector.currentText()
        self.combo_tipo_grafico.clear()

        # ---- Informe Anticipos: desactivar fechas y gráficos ----
        if informe_tipo == "Listado de trámites con Anticipo":
            # Deshabilitar controles de fechas
            for widget in (
                self.fecha_inicio_input, self.fecha_fin_input,
                self.fecha_inicio_label, self.fecha_fin_label
            ):
                widget.setEnabled(False)

            # Ocultar filtros, desactivar pestaña y botón de gráficos
            for widget in (self.operator_label, self.operator_combo,
                           self.letra_label, self.letra_combo):
                widget.hide()

            self.btn_graficos.setEnabled(False)
            self.tabs.setTabEnabled(1, False)   # 1 = pestaña Gráficos
            return
        else:
            # Rehabilitar todo para otros informes
            for widget in (
                self.fecha_inicio_input, self.fecha_fin_input,
                self.fecha_inicio_label, self.fecha_fin_label
            ):
                widget.setEnabled(True)

            self.btn_graficos.setEnabled(True)
            self.tabs.setTabEnabled(1, True)

        # ---- Informe Operadores: mostrar combos ----
        if informe_tipo == "Inf. de actuaciones gestionadas por Operador":
            self.operator_label.show()
            self.operator_combo.show()
            self.letra_label.show()
            self.letra_combo.show()
        else:
            self.operator_label.hide()
            self.operator_combo.hide()
            self.letra_label.hide()
            self.letra_combo.hide()

        # ---- Opciones de gráficos por informe ----
        if informe_tipo == "Informe de Altas":
            self.combo_tipo_grafico.addItems([
                "Gráfico de Expedientes",
                "Gráfico de Operadores",
                "Gráfico de Actividad",
                "Gráfico Actividad por Área",
                "Mostrar Todos",
            ])
        elif informe_tipo == "Informe por Categoria":
            self.combo_tipo_grafico.addItems([
                "Gráfico de Barras por Categoría",
                "Gráfico Circular por Tipo",
                "Mostrar Todos",
            ])
        elif informe_tipo == "Novedades de Beneficios":
            self.combo_tipo_grafico.addItem("Gráfico de Altas por Mes")

    # ------------------------------ Mensajes --------------------------------
    def show_message_box(self, title, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {background-color: #3F9F86; color: #34433F;
                         font-size: 12px; font-weight: bold;}
            QPushButton {background-color: #add8e6; color: #333;
                         border: none; padding: 5px; border-radius: 5px;
                         font-weight: bold;}
            QPushButton:hover {background-color: #87cefa;}
        """)
        msg_box.exec()


# ---------------------------------------------------------------------------
# Lanzador
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(get_resource_path("wolf.png")))
    ex = InformeApp()
    ex.show()
    sys.exit(app.exec())
