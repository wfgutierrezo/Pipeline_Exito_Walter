import pandas as pd
import numpy as np
import unicodedata

def estandarizar_texto(texto):
    """
    Quita tildes, convierte las 'ñ' en 'n' y elimina caracteres especiales.
    """
    if pd.isna(texto):
        return texto
    # Normaliza el texto separando los caracteres de sus acentos
    texto_norm = unicodedata.normalize('NFKD', str(texto))
    # Filtra solo los caracteres ASCII (elimina los acentos y convierte ñ en n)
    return "".join([c for c in texto_norm if not unicodedata.combining(c)])

def transformar_datos(df):
    """
    Recibe el DataFrame crudo, aplica las reglas de negocio (Historias de Usuario)
    y retorna un DataFrame limpio listo para cargar en la base de datos.
    """
    print("[2/4] Iniciando fase de TRANSFORMACIÓN...")
    
    try:
        # Buena práctica: Trabajar sobre una copia para aislar los datos originales
        df_clean = df.copy()

        # HU001 - Punto 1: Estandarizar Fechas (YYYY-MM-DD)
        # Maneja dinámicamente los formatos mezclados gracias a pd.to_datetime
        df_clean['Fecha_Venta'] = pd.to_datetime(df_clean['Fecha_Venta'], format='mixed', dayfirst=True).dt.strftime('%Y-%m-%d')

        # HU001 - Punto 2 y 3: Separar Ciudad y Tienda
        df_clean[['Ciudad', 'Tienda']] = df_clean['Ciudad_Tienda'].str.split('_', expand=True)

        # HU002 - Punto 1: Producto capitalizado y máximo 30 caracteres
        df_clean['Producto'] = df_clean['Producto'].str.capitalize().str[:30]

        # --- NUEVA REGLA: Normalizar textos (Quitar tildes y eñes) ---
        columnas_texto = ['Ciudad', 'Tienda', 'Producto']
        for col in columnas_texto:
            df_clean[col] = df_clean[col].apply(estandarizar_texto)        

        # HU002 - Punto 2: Cantidad en entero (arreglando el error humano 'Cero')
        df_clean['Cantidad'] = df_clean['Cantidad'].replace('Cero', 0)
        df_clean['Cantidad'] = pd.to_numeric(df_clean['Cantidad']).fillna(0).astype(int)

        # HU002 - Punto 3: Precio sin decimales (manejando nulos)
        df_clean['Precio_Unitario'] = df_clean['Precio_Unitario'].fillna(0).astype(int)

        # HU003 - Punto 1: Valor Total con IVA del 19%
        df_clean['Valor_Total_IVA'] = (df_clean['Cantidad'] * df_clean['Precio_Unitario'] * 1.19).round(0).astype(int)

        # --- ORGANIZACIÓN FINAL ---
        # Filtramos y ordenamos solo las columnas que le interesan a Negocio
        columnas_finales = [
            'ID_Transaccion', 'Fecha_Venta', 'Ciudad', 'Tienda', 
            'Producto', 'Cantidad', 'Precio_Unitario', 'Valor_Total_IVA'
        ]
        df_final = df_clean[columnas_finales]

        print(f"      -> Éxito: {len(df_final)} registros transformados y validados.")
        return df_final
        
    except Exception as e:
        # Si una regla de negocio falla, el pipeline debe detenerse inmediatamente
        raise RuntimeError(f"Error crítico durante la transformación de datos: {e}")

# Bloque de prueba local
if __name__ == "__main__":
    # Importamos el módulo extract solo para hacer la prueba independiente
    from extract import extraer_datos_diarios
    
    df_crudo = extraer_datos_diarios()
    df_procesado = transformar_datos(df_crudo)
    
    print("\n--- MUESTRA DE DATOS LIMPIOS ---")
    print(df_procesado)  
