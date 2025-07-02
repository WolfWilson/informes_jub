import pyodbc
import pandas as pd


# ---------------------------------------------------------------------------
# Helpers genéricos (con y sin parámetros)
# ---------------------------------------------------------------------------

def _get_connection(drivers, database: str):
    """Intenta conectarse usando la lista de drivers y devuelve conn o None."""
    for driver in drivers:
        try:
            print(f"Intentando conectar con el controlador: {driver}")
            return pyodbc.connect(
                f"DRIVER={{{driver}}};SERVER=sql01;DATABASE={database};Trusted_Connection=yes;"
            )
        except Exception as exc:
            print(f"No se pudo conectar con {driver}: {exc}")
            continue
    return None


def _rows_to_df(rows, cursor) -> pd.DataFrame:
    columns = [col[0] for col in cursor.description]
    return pd.DataFrame.from_records(rows, columns=columns)


# ---------------------------------------------------------------------------
# Procedimientos con rango de fechas
# ---------------------------------------------------------------------------

def fetch_data_from_database(fecha_inicio, fecha_fin, procedure_name):
    """
    Ejecuta un procedimiento con @FechaInicio y @FechaFin.
    """
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "SQL Server Native Client 11.0",
        "SQL Server Native Client 10.0",
        "SQL Server",
    ]

    conn = _get_connection(drivers, "Gestion")
    if not conn:
        print("Error: sin conexión para fetch_data_from_database.")
        return pd.DataFrame()

    cursor = conn.cursor()
    try:
        cursor.execute(
            f"EXEC {procedure_name} @FechaInicio = ?, @FechaFin = ?",
            (fecha_inicio, fecha_fin)
        )
        df = _rows_to_df(cursor.fetchall(), cursor)
    finally:
        cursor.close()
        conn.close()
    return df


# ---------------------------------------------------------------------------
# Procedimiento SIN parámetros (nuevo)
# ---------------------------------------------------------------------------

def fetch_data_no_params(procedure_name: str,
                         database: str = "Gestion") -> pd.DataFrame:
    """
    Ejecuta un procedimiento almacenado que NO recibe parámetros.
    """
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "SQL Server Native Client 11.0",
        "SQL Server Native Client 10.0",
        "SQL Server",
    ]

    conn = _get_connection(drivers, database)
    if not conn:
        print("Error: sin conexión para fetch_data_no_params.")
        return pd.DataFrame()

    cursor = conn.cursor()
    try:
        cursor.execute(f"EXEC {procedure_name}")
        df = _rows_to_df(cursor.fetchall(), cursor)
    finally:
        cursor.close()
        conn.close()
    return df


# ---------------------------------------------------------------------------
# Vista de operadores
# ---------------------------------------------------------------------------

def fetch_operators_list():
    """
    Devuelve (Codigo, descripcion) de v_personal_jub.
    """
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "SQL Server Native Client 11.0",
        "SQL Server Native Client 10.0",
        "SQL Server",
    ]

    conn = _get_connection(drivers, "Gestion")
    if not conn:
        print("No fue posible obtener la lista de operadores.")
        return pd.DataFrame()

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT Codigo, descripcion FROM v_personal_jub ORDER BY descripcion"
        )
        df = _rows_to_df(cursor.fetchall(), cursor)
    finally:
        cursor.close()
        conn.close()
    return df


# ---------------------------------------------------------------------------
# Procedimiento por operador
# ---------------------------------------------------------------------------

def fetch_data_operadores(fecha_inicio, fecha_fin, codigo_operador, letra):
    """
    Ejecuta Will_ObtenerMovimientos_por_operador con 4 parámetros.
    """
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "SQL Server Native Client 11.0",
        "SQL Server Native Client 10.0",
        "SQL Server",
    ]

    conn = _get_connection(drivers, "Gestion")
    if not conn:
        return pd.DataFrame()

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            EXEC Will_ObtenerMovimientos_por_operador
                 @FechaInicio = ?, @FechaFin = ?, @CodigoOperador = ?, @Letra = ?
            """,
            (fecha_inicio, fecha_fin, codigo_operador, letra)
        )
        df = _rows_to_df(cursor.fetchall(), cursor)
    finally:
        cursor.close()
        conn.close()
    return df
