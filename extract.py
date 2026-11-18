import pandas as pd
import os
from datetime import datetime, timedelta
import config  # Importamos nuestro propio archivo config.py

def extraer_datos_diarios():
    """
    Busca y extrae el archivo CSV de ventas correspondiente al cierre del día anterior.
    """
    print("[1/4] Iniciando fase de EXTRACCIÓN...")
    
    # Calculamos dinámicamente la fecha de ayer
    fecha_ayer = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    nombre_archivo = f'ventas_{fecha_ayer}.csv'
    ruta_completa = os.path.join(config.RUTA_ORIGEN, nombre_archivo)
    
    try:
        # En producción, aquí iría el código de SharePoint con io.BytesIO
        # Por ahora, leemos el CSV local que generamos en el Sprint 1
        df_bruto = pd.read_csv(ruta_completa, sep=',')
        
        print(f"      -> Éxito: Se leyeron {len(df_bruto)} registros del archivo '{nombre_archivo}'.")
        return df_bruto
        
    except FileNotFoundError:
        # Si el archivo no está, detenemos el pipeline y alertamos
        raise FileNotFoundError(f"ERROR CRÍTICO: No se encontró el archivo {nombre_archivo}. ¿Las tiendas lo subieron?")
    except Exception as e:
        raise RuntimeError(f"Error inesperado durante la extracción: {e}")

# Bloque de prueba local (Solo se ejecuta si corres este archivo directamente)
if __name__ == "__main__":
    df_prueba = extraer_datos_diarios()
    print(df_prueba.head())
