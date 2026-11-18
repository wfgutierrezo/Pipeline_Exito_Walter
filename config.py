import os
import yaml
from dotenv import load_dotenv

# 1. Rutas absolutas dinámicas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_ORIGEN = BASE_DIR  # <--- ¡Agrega esta línea!
RUTA_YAML = os.path.join(BASE_DIR, "pipeline_config.yaml")

# 2. Cargar Secretos del .env
load_dotenv()
SP_SITE_URL = os.getenv("SP_SITE_URL")
SP_CLIENT_ID = os.getenv("SP_CLIENT_ID")
SP_CLIENT_SECRET = os.getenv("SP_CLIENT_SECRET")
# En producción real, aquí también iría DB_USER y DB_PASSWORD

# 3. Cargar Configuración Estructural del YAML
try:
    with open(RUTA_YAML, 'r', encoding='utf-8') as file:
        app_config = yaml.safe_load(file)
except FileNotFoundError:
    raise FileNotFoundError(f"Falta el archivo de configuración: {RUTA_YAML}")

# 4. Extraer variables del YAML para usarlas en el proyecto
DB_SERVER = app_config['database']['server']
DB_NAME = app_config['database']['db_name']
DRIVER = app_config['database']['driver']

TABLA_STG = app_config['tables']['staging']
TABLA_DWH = app_config['tables']['dwh']
COLUMNAS_ESPERADAS = app_config['schema']['columnas_origen']

# 5. Armar la Cadena de Conexión (Autenticación de Windows)
CADENA_CONEXION_SQL = f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}?driver={DRIVER.replace(' ', '+')}&Trusted_Connection=yes"
