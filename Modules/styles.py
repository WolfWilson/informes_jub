from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QLinearGradient, QBrush, QColor, QPalette
from PyQt6.QtCore import Qt

def apply_styles(widget: QWidget):
    # Crear un gradiente de fondo que simule el degradado de la imagen
    gradient = QLinearGradient(0, 0, 0, widget.height())  # Degradado vertical
    
    # Colores basados en la imagen proporcionada
    gradient.setColorAt(0.0, QColor(0, 150, 140))  # Verde azulado
    gradient.setColorAt(0.5, QColor(80, 190, 170))  # Verde intermedio
    gradient.setColorAt(1.0, QColor(160, 240, 190))  # Verde claro / Lima suave

    # Aplicar el gradiente al widget
    palette = QPalette()
    brush = QBrush(gradient)
    palette.setBrush(QPalette.ColorRole.Window, brush)
    widget.setPalette(palette)
    
    # Aplicar estilos CSS a los widgets
    widget.setStyleSheet("""
        QLabel {
            color: #ffffff;  /* Texto blanco para mejor legibilidad */
            background-color: transparent;  /* Fondo transparente */
            font-size: 14px;
            font-weight: bold;
        }
        
        QPushButton {
            color: #ffffff;  /* Color del texto */
            background-color: #82DCC5;  /* Color verde medio */
            border: 1px solid #388E3C;  /* Borde de un verde más oscuro */
            padding: 5px;
            border-radius: 5px;
        }
        
        QPushButton:hover {
            background-color: #66BB6A;  /* Color verde más claro cuando se pasa el mouse */
        }
        
        QPushButton:pressed {
            background-color: #2E7D32;  /* Color verde más oscuro cuando se presiona */
            border: 1px solid #1B5E20;  /* Borde verde más oscuro */
        }

        QDateEdit {
            border: 1px solid #a0a0a0;
            border-radius: 5px;
            padding: 2px;
        }
        
        /* Estilo del botón desplegable (la flecha) */
        QDateEdit::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #a0a0a0;
        }

        /* Estilo para la flecha del botón desplegable */
        QDateEdit::down-arrow {
            width: 10px;
            height: 10px;
            border: 1px solid black;
            background-color: #82DCC5;  /* Flecha negra */
        }

        /* Cambia el color de la flecha cuando se pasa el mouse por encima */
        QDateEdit::down-arrow:hover {
            background-color: #555555;
        }

        QScrollBar:vertical {
            border: none;
            background: #f0f8ff;  
            width: 12px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #87cefa;
            min-height: 20px;
            border-radius: 6px;
            transition: background-color 0.3s ease;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #00bfff;
        }

        QScrollBar:horizontal {
            border: none;
            background: #f0f8ff;
            height: 12px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #87cefa;
            min-width: 20px;
            border-radius: 6px;
            transition: background-color 0.3s ease;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #00bfff;
        }

        QTabWidget::pane {
            background-color: #ffffff;
            border: 1px solid #a0a0a0;
        }

        QTabBar::tab {
            background-color: #e0f7ff;
            color: #333333;
            padding: 5px;
            border: 1px solid #a0a0a0;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }

        QTabBar::tab:selected {
            background-color: #add8e6;
        }

        QTableWidget {
            gridline-color: #cccccc;
            background-color: #ffffff;
            color: #333333;
        }

        QHeaderView::section {
            background-color: #e0f7ff;
            padding: 5px;
            border: 1px solid #a0a0a0;
            font-weight: bold;
            color: #333333;
        }

        QCalendarWidget QWidget {
            alternate-background-color: #f0f8ff;
            color: #333333;
        }

        QCalendarWidget QAbstractItemView:enabled {
            selection-background-color: #87cefa;
            selection-color: white;
        }
    """)
