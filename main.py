import time
from extract import extraer_datos_diarios
from transform import transformar_datos
from load_staging import cargar_datos_staging
from load_dwh import cargar_datos_dwh  # <-- NUEVO IMPORT

def ejecutar_pipeline():
    print("="*60)
    print(" INICIANDO PIPELINE DE VENTAS EXITO (ETL) ".center(60, "-"))
    print("="*60)
    
    tiempo_inicio = time.time()
    
    try:
        # Paso 1: EXTRACCIÓN
        df_crudo = extraer_datos_diarios()
        
        # Paso 2: TRANSFORMACIÓN
        df_limpio = transformar_datos(df_crudo)
        
        # Paso 3: CARGA (Staging temporal)
        carga_stg = cargar_datos_staging(df_limpio)
        
        # Paso 4: CARGA (Data Warehouse histórico)
        if carga_stg:
            carga_dwh = cargar_datos_dwh()
        
        # FINALIZACIÓN
        if carga_stg and carga_dwh:
            tiempo_fin = time.time()
            duracion = round(tiempo_fin - tiempo_inicio, 2)
            print("-" * 60)
            print(f"[5/5] PIPELINE FINALIZADO CON ÉXITO.")
            print(f"      -> Tiempo total de ejecución: {duracion} segundos.")
            print("="*60)
            
    except Exception as e:
        print("-" * 60)
        print(f"[X] ALERTA CRÍTICA: El pipeline ha fallado.")
        print(f"      -> Detalle del error: {e}")
        print("="*60)

if __name__ == "__main__":
    ejecutar_pipeline()
