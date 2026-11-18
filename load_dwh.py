from sqlalchemy import create_engine, text
import config

def cargar_datos_dwh():
    """
    Mueve los datos de Staging (STG) al Data Warehouse (DWH) usando MERGE (Upsert).
    Si el registro existe (mismo ID), lo actualiza. Si no existe, lo inserta.
    """
    print("[4/5] Iniciando fase de CARGA A DWH (Merge/Upsert)...")
    
    # Bloque de código nativo para SQL Server
    query_merge = f"""
    -- 1. Si la tabla histórica no existe, la creamos copiando la estructura de Staging vacía
    IF OBJECT_ID('{config.TABLA_DWH}', 'U') IS NULL
    BEGIN
        SELECT * INTO {config.TABLA_DWH} FROM {config.TABLA_STG} WHERE 1 = 0;
    END

    -- 2. Ejecutar el Upsert (MERGE)
    MERGE INTO {config.TABLA_DWH} AS target
    USING {config.TABLA_STG} AS source
    ON target.ID_Transaccion = source.ID_Transaccion
    
    WHEN MATCHED THEN
        UPDATE SET 
            target.Fecha_Venta = source.Fecha_Venta,
            target.Ciudad = source.Ciudad,
            target.Tienda = source.Tienda,
            target.Producto = source.Producto,
            target.Cantidad = source.Cantidad,
            target.Precio_Unitario = source.Precio_Unitario,
            target.Valor_Total_IVA = source.Valor_Total_IVA
            
    WHEN NOT MATCHED THEN
        INSERT (ID_Transaccion, Fecha_Venta, Ciudad, Tienda, Producto, Cantidad, Precio_Unitario, Valor_Total_IVA)
        VALUES (source.ID_Transaccion, source.Fecha_Venta, source.Ciudad, source.Tienda, source.Producto, source.Cantidad, source.Precio_Unitario, source.Valor_Total_IVA);
    """
    
    try:
        engine = create_engine(config.CADENA_CONEXION_SQL)
        # Ejecutamos el SQL usando un bloque seguro de SQLAlchemy
        with engine.begin() as conn:
            conn.execute(text(query_merge))
            
        print(f"      -> Éxito: Datos consolidados en la tabla histórica [{config.TABLA_DWH}].")
        return True
        
    except Exception as e:
        raise RuntimeError(f"Error crítico ejecutando MERGE en SQL Server: {e}")
