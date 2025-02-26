import pyodbc
import pandas as pd

def fetch_data_from_database(fecha_inicio, fecha_fin, procedure_name):
    """
    Conecta a la base de datos y ejecuta un procedimiento almacenado con las fechas proporcionadas.
    Retorna un DataFrame con los resultados o un DataFrame vacío en caso de error.
    """
    drivers = [
        'ODBC Driver 17 for SQL Server',  # Preferido y más reciente
        'SQL Server Native Client 11.0',  # Native Client version 11
        'SQL Server Native Client 10.0',  # Native Client version 10
        'SQL Server',  # Generic ODBC driver name (legacy)
    ]

    for driver in drivers:
        try:
            print(f"Intentando conectar usando el controlador: {driver}")
            conn = pyodbc.connect(f'DRIVER={{{driver}}};SERVER=sql01;DATABASE=Gestion;Trusted_Connection=yes;')
            cursor = conn.cursor()
            
            print(f"Conexión establecida con {driver}. Ejecutando procedimiento: {procedure_name} con fechas: {fecha_inicio} y {fecha_fin}")
            
            # Ejecutar el procedimiento almacenado y obtener resultados
            cursor.execute(f"EXEC {procedure_name} @FechaInicio = ?, @FechaFin = ?", (fecha_inicio, fecha_fin))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            df = pd.DataFrame.from_records(rows, columns=columns)
            
            cursor.close()
            conn.close()
            
            return df
        except Exception as e:
            print(f"Error al conectar o ejecutar consulta usando el controlador {driver}: {e}")
            continue

    # Si no se pudo conectar o hubo un error, devolver un DataFrame vacío y registrar el error
    print("Error: No se pudo conectar a la base de datos o ejecutar el procedimiento almacenado.")
    return pd.DataFrame()
