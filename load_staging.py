import pandas as pd
from sqlalchemy import create_engine
import config

# Aquí definimos que la función recibe una variable llamada df_limpio
def cargar_datos_staging(df_limpio):
    """
    Recibe el DataFrame limpio y lo carga en la tabla STG (Staging) en SQL Server.
    Usa el método 'replace' para hacer un DROP y CREATE automático de la tabla temporal.
    """
    print("[3/4] Iniciando fase de CARGA A STAGING (Load)...")
    
    try:
        # 1. Creamos el motor de conexión con SQLAlchemy
        engine = create_engine(config.CADENA_CONEXION_SQL)
        
        # 2. Inyectamos los datos a SQL Server
        df_limpio.to_sql(
            name=config.TABLA_STG, 
            con=engine, 
            if_exists='replace', 
            index=False
        )
        
        print(f"      -> Éxito: {len(df_limpio)} registros insertados en la tabla [{config.TABLA_STG}] de SQL Server.")
        return True

    except Exception as e:
        raise RuntimeError(f"Error crítico conectando o insertando en SQL Server: {e}")


# Bloque de prueba local
if __name__ == "__main__":
    from extract import extraer_datos_diarios
    from transform import transformar_datos
    
    # Paso A: Extraemos los datos y los guardamos en 'df_crudo'
    df_crudo = extraer_datos_diarios()
    
    # Paso B: Transformamos 'df_crudo' y el resultado lo guardamos EXACTAMENTE como 'df_limpio'
    df_limpio = transformar_datos(df_crudo)
    
    # Paso C: Le enviamos ese 'df_limpio' a nuestra función de carga
    cargar_datos_staging(df_limpio)
