# spanfbl1902@2025

"""
Módulo para crear una conexión con la base de datos
"""

# funciones para abrir una comunicación con la base de datos
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase
# módulo para crear una sesión asyncrónica
from typing import AsyncGenerator
# módulo para acceder a la base de datos
from settings import BASE_DATOS_URL

# definir motor
engine = create_async_engine(
        BASE_DATOS_URL,
        echo=True,
        future=True,
        pool_size=5,
        max_overflow=2,
)
# definir sesión asyncrónica
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

class Base(AsyncAttrs, DeclarativeBase):
    """
    Clase para crear la base
    """
    pass


async def comunicar_base_datos() -> AsyncGenerator[AsyncSession, None]:
    """
    Función para crear una conexión
    con la base de datos
    """
    db = async_session()
    try:
        yield db
    finally:
        await db.close()
