# 📊 Generador de Informes con PyQt6

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Graphs-orange.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-blue.svg)

## 📝 Descripción
Este es un software de escritorio desarrollado en **Python** utilizando **PyQt6** para generar informes dinámicos basados en datos extraídos de una base de datos. Incluye visualización gráfica de la información usando **Matplotlib** y exportación de datos a **Excel**.

## 🚀 Características
- Interfaz gráfica amigable con **PyQt6**
- Generación de informes personalizados según fechas
- Gráficos interactivos con **Matplotlib**
- Exportación de datos a **Excel (.xlsx)**
- Actualización en tiempo real
- Soporte para múltiples tipos de gráficos y filtros

## 📸 Capturas de Pantalla
![Interfaz](https://via.placeholder.com/800x400?text=Captura+de+Pantalla)

## 📂 Instalación y Uso
### 🔧 1. Clonar el Repositorio
```bash
git clone https://github.com/WolfWilson/informes_jub.git
cd informes_jub
```
### 🛠 2. Crear un Entorno Virtual e Instalar Dependencias
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### ▶️ 3. Ejecutar la Aplicación
```bash
python informesv4.py
```

## 📊 Generación de Informes
El software permite generar informes en base a tres criterios principales:
1. **Informe de Altas**: Datos sobre nuevas incorporaciones.
2. **Informe por Categoría**: Análisis basado en categorías predefinidas.
3. **Novedades de Beneficios**: Cambios recientes en el sistema de beneficios.

## 📈 Tipos de Gráficos Disponibles
✔️ Gráfico de Expedientes
✔️ Gráfico de Operadores
✔️ Gráfico de Actividad
✔️ Gráfico Actividad por Área
✔️ Gráfico de Barras por Categoría
✔️ Gráfico Circular por Tipo
✔️ Gráfico de Altas por Mes

## 💾 Exportación de Datos
El usuario puede exportar:
- 📜 **Informes en Excel (.xlsx)**
- 📊 **Gráficos en formato PNG**

## 🔧 Construcción del Ejecutable
Si deseas generar un ejecutable independiente:
```bash
pyinstaller --onefile --windowed --icon=wolf.ico --add-data "Source/wolf.png;Source" informesv4.py
```
El ejecutable se generará en la carpeta `dist/`.

## 📜 Licencia
Este proyecto está licenciado bajo la **Licencia MIT**.

## 📧 Contacto
Si tienes preguntas o sugerencias, puedes contactarme en: [Tu Email o GitHub].

🚀 **¡Gracias por usar el Generador de Informes!**
