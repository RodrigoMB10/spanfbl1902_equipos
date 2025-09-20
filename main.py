# spanfbl1902@2025

"""
Módulo principal para ejectuar la API
"""

# módulos para crear una API
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
# módulo para definir los orígines
from settings import ORIGENES_CORS, DEBUG
# módulo para crear respuestas JSON
from starlette.responses import JSONResponse
# módulo para inicializar el servidor
import uvicorn
# módulo para limitar las solicitudes HTTP
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
# función para crear logs
from utils.logging_config import get_logger
# módulos para acceder a los puntos de acceso
from routers import equipos


# definir el tipo de aplicación
app = FastAPI(
    version="0.1.0",
    debug=DEBUG,
    title="Competiciones",
    description="API dedicada a la gestión de equipos"
)
# definir el límite de solicitudes
limite = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
# añadir el límite a la aplicación
app.state.limiter = limite

# gestión de errores cuando el límite ha sido excedido
@app.exception_handler(RateLimitExceeded)
async def maximo_limite_excedido(
    request: Request, exc: RateLimitExceeded
) -> JSONResponse:
    """
    Función para gestionar el límite máximo permitido
    """
    logger.exception(f"Límite máximo excedido: {exc}")
    return JSONResponse(
        status_code=429,
        content={"detail": "Límite máximo excedido"},
    )

# añadir las restricciones al middleware
app.add_middleware(SlowAPIMiddleware)
# incluir routers permitido
app.include_router(equipos.equipos_router)
# definir logger
logger = get_logger(__name__)

# verificar la salud del servidor
@app.get("/")
async def check():
    """
    Función para verificar que la API
    funciona correctamente
    """
    return {"servidor": "en activo"}

# definir CORS
app.add_middleware(
    CORSMiddleware,
    # permitir sólo orígenes reconocidos
    allow_origins=ORIGENES_CORS,
    # sin credenciales por el moment
    allow_credentials=False,
    # métodos
    allow_methods=["POST", "PUT", "DELETE", "GET"],
    # cabecera
    allow_headers=["*"],
)

# iniciar la aplicación
if __name__ == "__main__":
    """
    Función principal para inicializar la applicación
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=DEBUG)
