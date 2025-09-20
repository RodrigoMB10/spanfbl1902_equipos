# spanfbl1902@2025

"""
Módulo para recoger las acciones que ocurren
durante la ejecución del programa
"""

# módulo para crear y editar archivos
import os
# módulo para crear logs
import logging
# clase para determinar la fecha y hora en la que se registra una acción
from datetime import datetime
# clase para guardar los logs en un archivo
from logging.handlers import RotatingFileHandler

# instancias de directorio y archivo
RUTA_DIRECTORIO = "logs"
RUTA_ARCHIVO = "Equipos"
# crea la carpeta logs si no existe
os.makedirs(RUTA_DIRECTORIO, exist_ok=True)
# recupera la fecha y hora
nombre_archivo = datetime.now().strftime("%d-%m-%Y.log")
ruta_archivo = os.path.join(RUTA_DIRECTORIO, f"{RUTA_ARCHIVO}_{nombre_archivo}")
# formato de log
FORMATO_LOGS = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# configuración del logger raíz
logging.basicConfig(
    level=logging.INFO,
    format=FORMATO_LOGS,
    handlers=[
        RotatingFileHandler(ruta_archivo, maxBytes=5*1024*1024, backupCount=3),
        logging.StreamHandler()
    ],
)


def get_logger(name: str) -> logging.Logger:
    """
    Función para inicializar los logs
    Devuelve el archivo
    """
    return logging.getLogger(name)
