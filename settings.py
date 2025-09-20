# spanfbl1902@2025
"""
Módulo para definir CORS
"""

# función para definir el tipo de variables
from decouple import config
# función para acceder a las variables del sistema
from dotenv import load_dotenv

# cargar variables
load_dotenv()

# definir debug config
DEBUG = config("DEBUG", cast=bool)

# definir origenes
ORIGENES = [
    # localhost for testing
    "http://localhost:8000"
]

ORIGENES_CORS = ORIGENES

# configuración de la base de datos
BASE_DATOS = config("NOMBRE", cast=str)
USUARIO_BD = config("USUARIO", cast=str)
CLAVE_BD = config("CLAVE", cast=str)
HOST_BD = config("HOST", cast=str)
PUERTO_BD = config("PUERTO", cast=str)

# declarar base de datos
BASE_DATOS_URL = (
    f"postgresql+asyncpg://{USUARIO_BD}:{CLAVE_BD}@{HOST_BD}:{PUERTO_BD}/{BASE_DATOS}"
)