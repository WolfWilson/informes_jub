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

![Interfaz][![imagen-2025-02-26-112808019.png](https://i.postimg.cc/FK3VbV3m/imagen-2025-02-26-112808019.png)](https://postimg.cc/cK130YF5)

![Interfaz][![imagen-2025-02-26-112858053.png](https://i.postimg.cc/mDS3JZm5/imagen-2025-02-26-112858053.png)](https://postimg.cc/VrdbbwQq)

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
3. **Informes por Operadores**: Egresos de cada operador (actividad completado con actuaciones-expedientes)

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
```
El ejecutable se generará en la carpeta `C:/My Software Folder`.

## 📜 Licencia
Este proyecto está licenciado bajo la **Licencia MIT**.

## 📧 Contacto
Si tienes preguntas o sugerencias, puedes contactarme en: [wolfwilson].

🚀 **¡Gracias por usar el Generador de Informes!**
