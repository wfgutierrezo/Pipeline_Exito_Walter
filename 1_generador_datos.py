import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Calculamos la fecha de ayer para el nombre del archivo (Formato YYYYMMDD)
# Si hoy es 17 de noviembre, esto generará '20261116'
fecha_ayer = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

# 2. Simulamos las ventas de UN SOLO DÍA con los mismos errores humanos/de sistema
datos_diarios = {
    'ID_Transaccion': ['T100', 'T101', 'T102', 'T103', 'T104'],
    # Fechas cruzadas simulando el día de ayer
    'Fecha_Venta': ['16/11/2026', '11-16-2026', '16/11/2026', '11-16-2026', '16/11/2026'], 
    'Ciudad_Tienda': ['Bogota_Norte', 'Medellin_Sur', 'Cali_Centro', 'Bogota_Norte', 'Medellin_Sur'],
    'Producto': ['televisor samsung', 'NEVERA LG', 'lavadora Haceb', 'Televisor Samsung 55 pulgadas UHD', 'licuadora'],
    'Cantidad': [2, 1, 'Cero', 3, 1],
    'Precio_Unitario': [1500000, 2000000, 1800000, np.nan, 150000]
}

df_diario = pd.DataFrame(datos_diarios)

# 3. Nombramos el archivo dinámicamente con la fecha
nombre_archivo = f'ventas_{fecha_ayer}.csv'

# 4. Exportamos a CSV
# index=False evita exportar los números de fila, sep=',' es el estándar universal
df_diario.to_csv(nombre_archivo, index=False, sep=',')

print(f"Éxito: Archivo de carga diaria '{nombre_archivo}' generado.")
print("¡El origen de datos ahora es aprueba de balas!")
