# Modules/graficos.py

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import MaxNLocator

def generar_graficos(df, informe_tipo, tipo_grafico, canvas):
    """
    Genera los gráficos según el tipo de informe y gráfico seleccionados.
    'df'  es el DataFrame con datos ya consultados.
    'informe_tipo'  es el texto del combo principal (p.e. "Informe de Altas").
    'tipo_grafico'  es la opción seleccionada (p.e. "Gráfico de Expedientes").
    'canvas'  es el FigureCanvas donde dibujaremos.
    """

    # Limpiar el lienzo antes de dibujar
    canvas.figure.clear()

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

            # =================================================================
            # EJEMPLOS DE TUS GRÁFICOS PARA "Informe de Altas"
            # =================================================================
            if tipo_grafico == "Gráfico de Expedientes":
                ax = canvas.figure.add_subplot(111)
                letras_count = df['letra'].value_counts()
                colores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

                wedges, texts, autotexts = ax.pie(
                    letras_count.values,
                    labels=letras_count.index,
                    autopct=lambda pct: func(pct, letras_count.values),
                    startangle=90,
                    colors=colores,
                    wedgeprops={'linewidth':1, 'edgecolor': 'white'},
                    textprops={'color':'black', 'fontsize':10}
                )
                ax.set_title('Distribución por Letra de Expediente',  fontsize=12, fontweight='bold')

                for autotext in autotexts:
                    autotext.set_color('black')
                    autotext.set_fontsize(10)
                    autotext.set_fontweight('bold')

                centro_circulo = plt.Circle((0,0),0.70, fc='white')
                ax.add_artist(centro_circulo)
                ax.axis('equal')
                canvas.figure.tight_layout()

            elif tipo_grafico == "Gráfico de Operadores":
                ax = canvas.figure.add_subplot(111)
                df['Operador'] = df['Operador'].str.strip()
                operadores_count = df['Operador'].value_counts()
                cmap = plt.get_cmap('Pastel2')
                norm = plt.Normalize(operadores_count.min(), operadores_count.max())

                bars = []
                for i, (Operador, valor) in enumerate(operadores_count.items()):
                    color = cmap(0.2 + 0.8 * norm(valor))
                    bar = FancyBboxPatch(
                        (i  - 0.4, 0), 0.8, valor,
                        boxstyle="round, pad=0.3",
                        linewidth=2,
                        edgecolor='white',
                        facecolor=color
                    )
                    ax.add_patch(bar)
                    bars.append(bar)

                ax.set_facecolor('#f0f0f0')
                ax.set_xlim(-0.5, len(operadores_count) -0.5)
                ax.set_ylim(0, operadores_count.max() + 2)
                ax.set_title('Actuaciones por Operador', fontsize=12, fontweight='bold')
                ax.set_xlabel('Operador', fontsize=12)
                ax.set_ylabel('Cantidad de Actuaciones', fontsize=12)

                ax.set_xticks(range(len(operadores_count.index)))
                ax.set_xticklabels(operadores_count.index, rotation=45, ha='right', fontsize=8)

                for i, bar in enumerate(bars):
                    yval = operadores_count.values[i]
                    ax.text(i, yval + 0.3, int(yval), ha='center', fontsize=10)

                canvas.figure.tight_layout()
                canvas.draw()

            elif tipo_grafico == "Gráfico de Actividad":
                ax = canvas.figure.add_subplot(111)
                df['fech_alta'] = pd.to_datetime(df['fech_alta'], format='%d-%m-%Y %H:%M', errors='coerce', dayfirst=True)
                df.dropna(subset=['fech_alta'], inplace=True)
                df['hora_alta'] = df['fech_alta'].dt.hour
                horas_count = df['hora_alta'].value_counts().sort_index()

                ax.plot(horas_count.index, horas_count.values, marker='o', linestyle='--', color='blue', markersize=8, markerfacecolor='red')
                ax.set_title('Actividad por Hora', fontsize=16, color='darkgreen')
                ax.set_xlabel('Hora del Día', fontsize=12, color='darkblue')
                ax.set_ylabel('Cantidad de Actuaciones', fontsize=12, color='darkblue')

                for x, y in zip(horas_count.index, horas_count.values):
                    if y == horas_count.max():
                        ax.text(x, y + 2, str(y), fontsize=10, color='black', ha='center', fontweight='bold')
                    else:
                        ax.text(x, y - 2, str(y), fontsize=10, color='black', ha='center', fontweight='bold')

                ax.set_xlim(horas_count.index.min() - 1, horas_count.index.max() + 1)
                ax.set_ylim(0, horas_count.values.max() + 5)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_color('gray')
                ax.spines['left'].set_color('gray')
                ax.tick_params(axis='x', colors='purple', labelsize=10)
                ax.tick_params(axis='y', colors='purple', labelsize=10)
                canvas.draw()

            elif tipo_grafico == "Gráfico Actividad por Área":
                ax = canvas.figure.add_subplot(111)
                descripcion_count = df['Descripcion'].value_counts()
                cmap = plt.get_cmap('viridis')
                norm = plt.Normalize(descripcion_count.min(), descripcion_count.max())

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

                canvas.figure.tight_layout()
                canvas.draw()

            elif tipo_grafico == "Mostrar Todos":
                # Código original para "Mostrar Todos" ...
                canvas.figure.clear()
                axs = canvas.figure.subplots(2, 2)
                
                # 1) Gráfico de Expedientes
                letras_count = df['letra'].value_counts()
                bars = axs[0, 0].bar(letras_count.index, letras_count.values)
                axs[0, 0].set_title('Distribución por Tipo de Letra')
                for bar in bars:
                    yval = bar.get_height()
                    axs[0, 0].text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)
                
                # 2) Gráfico de Operadores
                operadores_count = df['Operador'].value_counts()
                bars = axs[0, 1].bar(operadores_count.index, operadores_count.values)
                axs[0, 1].set_title('Actuaciones por Operador')
                axs[0, 1].set_xlabel('Operador')
                axs[0, 1].set_ylabel('Cantidad de Actuaciones')
                axs[0, 1].tick_params(axis='x', rotation=45, labelsize=8)
                for bar in bars:
                    yval = bar.get_height()
                    axs[0, 1].text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)
                
                # 3) Gráfico de Actividad por Hora
                df['hora_alta'] = pd.to_datetime(df['fech_alta'], errors='coerce', dayfirst=True).dt.hour
                horas_count = df['hora_alta'].value_counts().sort_index()
                axs[1, 0].plot(horas_count.index, horas_count.values, marker='o')
                axs[1, 0].set_title('Actividad por Hora')
                axs[1, 0].set_xlabel('Hora del Día')
                axs[1, 0].set_ylabel('Cantidad de Actuaciones')
                for x, y in zip(horas_count.index, horas_count.values):
                    axs[1, 0].text(x, y, str(y), fontsize=9, ha='center')
                
                # 4) Gráfico Actividad por Descripción
                descripcion_count = df['Descripcion'].value_counts()
                bars = axs[1, 1].bar(descripcion_count.index, descripcion_count.values)
                axs[1, 1].set_title('Distribución de Actividad por Descripción')
                axs[1, 1].set_xlabel('Descripción')
                axs[1, 1].set_ylabel('Cantidad')
                axs[1, 1].tick_params(axis='x', rotation=45, labelsize=8)
                for bar in bars:
                    yval = bar.get_height()
                    axs[1, 1].text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)
                
                canvas.figure.tight_layout()

        elif informe_tipo == "Informe por Categoria" and tipo_grafico in [
            "Gráfico de Barras por Categoría",
            "Gráfico Circular por Tipo",
            "Mostrar Todos"
        ]:
            # Código original para gráficos de "Informe por Categoria" ...
            if tipo_grafico == "Gráfico de Barras por Categoría":
                ax = canvas.figure.add_subplot(111)
                df['Categoria'] = df['Categoria'].str.strip()
                categoria_count = df.groupby('Categoria')['Conteo'].sum().sort_values(ascending=False)

                cmap = plt.get_cmap('viridis')
                norm = plt.Normalize(categoria_count.min(), categoria_count.max())

                bars = []
                for i, (categoria, valor) in enumerate(categoria_count.items()):
                    color = cmap(0.2 + 0.8 * norm(valor))
                    bar = FancyBboxPatch(
                        (i - 0.4, 0), 0.8, valor,
                        boxstyle="round,pad=0.3", linewidth=1, edgecolor="white", facecolor=color
                    )
                    ax.add_patch(bar)
                    bars.append(bar)

                ax.set_facecolor('#f0f0f0')
                ax.set_xlim(-0.5, len(categoria_count) - 0.5)
                ax.set_ylim(0, categoria_count.max() + 2)
                ax.set_title('Totales por Categoría', fontsize=16, fontweight='bold')
                ax.set_xlabel('Categoría', fontsize=12, labelpad=20)
                ax.set_ylabel('Cantidad total en el periodo', fontsize=12)

                ax.set_xticks(range(len(categoria_count.index)))
                ax.set_xticklabels(categoria_count.index, rotation=60, ha='right', fontsize=8, rotation_mode='anchor')

                for i, bar in enumerate(bars):
                    yval = categoria_count.values[i]
                    ax.text(i, yval + 0.5, int(yval), ha='center', fontsize=9)
                    
                canvas.figure.tight_layout()
                plt.subplots_adjust(bottom=0.2)
                canvas.draw()
                    
            elif tipo_grafico == "Gráfico Circular por Tipo":
                ax = canvas.figure.add_subplot(111)
                tipo_count = df['Tipo'].value_counts()
                ax.pie(tipo_count, labels=tipo_count.index, autopct='%1.1f%%')
                ax.set_title('Distribución por Tipo')

            elif tipo_grafico == "Mostrar Todos":
                canvas.figure.clear()
                axs = canvas.figure.subplots(1, 2)
                
                categoria_count = df.groupby('Categoria')['Conteo'].sum().sort_values(ascending=False)
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

                tipo_count = df['Tipo'].value_counts()
                axs[1].pie(tipo_count, labels=tipo_count.index, autopct='%1.1f%%', startangle=90, labeldistance=1.1)
                axs[1].set_title('Distribución por Tipo')
                
                canvas.figure.tight_layout()

        elif informe_tipo == "Novedades de Beneficios" and tipo_grafico == "Gráfico de Altas por Mes":
            ax = canvas.figure.add_subplot(111)
            altas_por_mes = df.groupby(['Anio', 'Mes']).size().reset_index(name='Cantidad')
            altas_por_mes['Periodo'] = altas_por_mes['Anio'].astype(str) + '-' + altas_por_mes['Mes'].astype(str)
            norm = plt.Normalize(altas_por_mes['Cantidad'].min(), altas_por_mes['Cantidad'].max())
            cmap = plt.cm.plasma

            bars = ax.bar(
                altas_por_mes['Periodo'], 
                altas_por_mes['Cantidad'], 
                color=cmap(norm(altas_por_mes['Cantidad'])), 
                edgecolor='black', 
                linewidth=1.2
            )
            ax.set_title('Cantidad de Altas por Mes', fontsize=16, weight='bold', family='Verdana', color='#333333')
            ax.set_xlabel('Mes', fontsize=12, family='Verdana', color='#333333')
            ax.set_ylabel('Cantidad de Altas', fontsize=12, family='Verdana', color='#333333')

            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 1, int(yval), ha='center', fontsize=9)

            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax)
            cbar.set_label('Cantidad', fontsize=12, family='Verdana')

            canvas.figure.tight_layout()

        # Si quisieras gráficos en "Informe de Operadores", lo harías con elif informe_tipo == "Informe de Operadores": ...
        
        # Finalmente, forzamos el repintado
        canvas.draw()

    except KeyError as e:
        # Lanza de nuevo la excepción para que sea capturada desde el main
        raise KeyError(f"Columna no encontrada: {str(e)}")
    except Exception as e:
        raise Exception(str(e))
