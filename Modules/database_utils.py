# Modules/database_utils.py

import pyodbc
import pandas as pd

def fetch_data_from_database(fecha_inicio, fecha_fin, procedure_name):
    """
    Conecta a la base de datos y ejecuta un procedimiento almacenado con las fechas proporcionadas.
    Retorna un DataFrame con los resultados o un DataFrame vacío en caso de error.
    """
    drivers = [
        'ODBC Driver 17 for SQL Server',
        'SQL Server Native Client 11.0',
        'SQL Server Native Client 10.0',
        'SQL Server',
    ]

    for driver in drivers:
        try:
            print(f"Intentando conectar usando el controlador: {driver}")
            conn = pyodbc.connect(
                f'DRIVER={{{driver}}};SERVER=sql01;DATABASE=Gestion;Trusted_Connection=yes;'
            )
            cursor = conn.cursor()
            
            print(f"Conexión establecida con {driver}. Ejecutando procedimiento: {procedure_name}")
            # Ejecutar el procedimiento almacenado y obtener resultados
            cursor.execute(
                f"EXEC {procedure_name} @FechaInicio = ?, @FechaFin = ?",
                (fecha_inicio, fecha_fin)
            )
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)
            
            cursor.close()
            conn.close()
            
            return df
        except Exception as e:
            print(f"Error al conectar o ejecutar consulta usando el controlador {driver}: {e}")
            continue

    # Si no se pudo conectar o hubo un error, devolver un DataFrame vacío.
    print("Error: No se pudo conectar a la base de datos o ejecutar el procedimiento almacenado.")
    return pd.DataFrame()


def fetch_operators_list():
    """
    Retorna un DataFrame con (Codigo, descripcion) de la vista v_personal_jub,
    ordenado por la columna 'descripcion'.
    """
    drivers = [
        'ODBC Driver 17 for SQL Server',
        'SQL Server Native Client 11.0',
        'SQL Server Native Client 10.0',
        'SQL Server',
    ]
    
    for driver in drivers:
        try:
            conn = pyodbc.connect(
                f'DRIVER={{{driver}}};SERVER=sql01;DATABASE=Gestion;Trusted_Connection=yes;'
            )
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT Codigo, descripcion FROM v_personal_jub ORDER BY descripcion"
            )
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            
            df = pd.DataFrame.from_records(rows, columns=columns)

            cursor.close()
            conn.close()
            return df
        except Exception as e:
            print(f"Error usando controlador {driver} para fetch_operators_list: {e}")
            continue
    
    print("No fue posible obtener la lista de operadores.")
    return pd.DataFrame()


def fetch_data_operadores(fecha_inicio, fecha_fin, codigo_operador, letra):
    """
    Ejecuta el procedimiento Will_ObtenerMovimientos_por_operador 
    enviando 4 parámetros:
      @FechaInicio, @FechaFin, @CodigoOperador, @Letra
    Devuelve un DataFrame con los resultados.
    """
    drivers = [
        'ODBC Driver 17 for SQL Server',
        'SQL Server Native Client 11.0',
        'SQL Server Native Client 10.0',
        'SQL Server',
    ]
    
    for driver in drivers:
        try:
            conn = pyodbc.connect(
                f'DRIVER={{{driver}}};SERVER=sql01;DATABASE=Gestion;Trusted_Connection=yes;'
            )
            cursor = conn.cursor()
            
            query = """
                EXEC Will_ObtenerMovimientos_por_operador 
                     @FechaInicio = ?, 
                     @FechaFin = ?, 
                     @CodigoOperador = ?, 
                     @Letra = ?
            """
            cursor.execute(query, (fecha_inicio, fecha_fin, codigo_operador, letra))
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            
            df = pd.DataFrame.from_records(rows, columns=columns)
            
            cursor.close()
            conn.close()
            
            return df
        except Exception as e:
            print(f"Error al obtener datos de operadores con {driver}: {e}")
            continue
    
    # Si no se pudo conectar, devolver un DataFrame vacío
    return pd.DataFrame()
