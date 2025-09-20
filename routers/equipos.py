# spanfbl1902@2025

"""
Módulo para gestionar equipos
"""

# módulo parar crear el punto de acceso
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, Body
# módulo para comunicar con la base de datos
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
# módulo parar inicializar la base de datos
from base_datos.base_datos import comunicar_base_datos
# módulo parar acceder las tablas
from models.equipo import IndiceEquipos as ORMIndiceEquipos, Equipos as ORMEquipos, Denominaciones as ORMDenominaciones, Logotipos as ORMLogotipos, Direcciones as ORMDirecciones, Estadios as ORMEstadios, DenominacionesEquipo as ORMDenominacionesEquipo, LogotiposEquipo as ORMLogotiposEquipo, DireccionesEquipo as ORMDireccionesEquipo, EstadiosEquipo as ORMEstadiosEquipo, CompeticionesEquipo as ORMCompeticionesEquipo
from schemas.tablas_equipos import IndiceEquipos as PydanticIndiceEquipos, Equipos as PydanticEquipos, Estadios as PydanticEstadios, Direcciones as PydanticDirecciones, Logotipos as PydanticLogotipos, Denominaciones as PydanticDenominaciones, DenominacionesEquipo as PydanticDenominacionesEquipo, LogotiposEquipo as PydanticLogotiposEquipo, DireccionesEquipo as PydanticDireccionesEquipo, EstadiosEquipo as PydanticEstadiosEquipo, CompeticionesEquipo as PydanticCompeticionesEquipo,  EditarDenominaciones, EditarEquipos, EditarDirecciones, EditarEstadios, EditarLogotipos, EditarIndiceEquipos, EditarCompeticionesEquipo, EditarDenominacionesEquipo, EditarLogotiposEquipo, EditarEstadiosEquipo, EditarDireccionesEquipo
# módulo para grabar logs
from utils.logging_config import get_logger

# definir logger
logger = get_logger(__name__)
# definir router
equipos_router = APIRouter(tags=["equipos"])

# router para crear un equipo base
@equipos_router.post("/crear_equipo_base/")
async def crear_equipo_base(
    equipo_base: PydanticIndiceEquipos, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para crear un equipo base
    
    Parámetros:
    - equipo_base {Object}: que define un equipo base
    - db {Object}: conexión a una base de datos

    Retorna:
    - equipo_base {Object}: detalles del equipo base creado o error
    """
    try:
        logger.info(f"Creando nuevo equipo base: {equipo_base}")
        # crea una nueva entidad en la base de datos
        nuevo_equipo_base = ORMIndiceEquipos(**equipo_base.model_dump())
        db.add(nuevo_equipo_base)
        await db.commit()
        await db.refresh(nuevo_equipo_base)
        logger.info(f"Equipo base {nuevo_equipo_base} creado satisfactoriamente")
        # respuesta satisfactoria
        return {
            "indice_equipo_id": nuevo_equipo_base.indice_equipo_id,
            "fundacion": nuevo_equipo_base.fundacion
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear un equipo
@equipos_router.post("/crear_equipo/")
async def crear_equipo(
    equipo: PydanticEquipos, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para crear un equipo
    
    Parámetros:
    - equipo {Object}: que define un equipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - equipo {Object}: detalles del equipo creado o error
    """
    try:
        logger.info(f"Creando nuevo equipo: {equipo}")
        # crea una nueva entidad en la base de datos
        nuevo_equipo = ORMEquipos(**equipo.model_dump())
        db.add(nuevo_equipo)
        await db.commit()
        await db.refresh(nuevo_equipo)
        logger.info(f"Equipo {nuevo_equipo} creado satisfactoriamente")
        # respuesta satisfactoria
        return {
            "equipo_id": nuevo_equipo.equipo_id,
            "equipo_base": nuevo_equipo.equipo_base_id,
            "denominacion_equipo": nuevo_equipo.denominacion_equipo_id,
            "logotipo_equipo": nuevo_equipo.logotipo_equipo_id,
            "estadio": nuevo_equipo.estadio_id,
            "direccion": nuevo_equipo.direccion_id,
            "temporada": nuevo_equipo.temporada_id
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear una denominación
@equipos_router.post("/crear_denominacion/")
async def crear_denominacion(
    denominacion: PydanticDenominaciones, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para crear una denominación
    
    Parámetros:
    - denominación {Object}: que define una denominación
    - db {Object}: conexión a una base de datos

    Retorna:
    - denominación {Object}: detalles de la denominación creada o error
    """
    try:
        logger.info(f"Creando nueva denominación: {denominacion}")
        # crea una nueva entidad en la base de datos
        nueva_denominacion = ORMDenominaciones(**denominacion.model_dump())
        db.add(nueva_denominacion)
        await db.commit()
        await db.refresh(nueva_denominacion)
        logger.info(f"Denominación {nueva_denominacion} creada satisfactoriamente")
        # respuesta satisfactoria
        return {
            "denominacion_id": nueva_denominacion.denominacion_id,
            "denominacion": nueva_denominacion.denominacion
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear un logotipo
@equipos_router.post("/crear_logotipo/")
async def crear_logotipo(
    logotipo: PydanticLogotipos, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para crear un logotipo
    
    Parámetros:
    - logotipo {Object}: que define un logotipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - logotipo {Object}: detalles del logotipo creado o error
    """
    try:
        logger.info(f"Creando nuevo logotipo: {logotipo}")
        # crea una nueva entidad en la base de datos
        nuevo_logotipo = ORMLogotipos(**logotipo.model_dump())
        db.add(nuevo_logotipo)
        await db.commit()
        await db.refresh(nuevo_logotipo)
        logger.info(f"Logotipo {nuevo_logotipo} creado satisfactoriamente")
        # respuesta satisfactoria
        return {
            "logotipo_id": nuevo_logotipo.logotipo_id,
            "logotipo": nuevo_logotipo.logotipo
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear una dirección
@equipos_router.post("/crear_direccion/")
async def crear_direccion(
    direccion: PydanticDirecciones, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para crear una dirección
    
    Parámetros:
    - direccion {Object}: que define una dirección
    - db {Object}: conexión a una base de datos

    Retorna:
    - direccion {Object}: detalles de la dirección creada o error
    """
    try:
        logger.info(f"Creando nueva dirección: {direccion}")
        # crea una nueva entidad en la base de datos
        nueva_direccion = ORMDirecciones(**direccion.model_dump())
        db.add(nueva_direccion)
        await db.commit()
        await db.refresh(nueva_direccion)
        logger.info(f"Dirección {nueva_direccion} creada satisfactoriamente")
        # respuesta satisfactoria
        return {
            "direccion_id": nueva_direccion.direccion_id,
            "direccion": nueva_direccion.direccion,
            "comunidad_autonoma": nueva_direccion.comunidad_autonoma,
            "provincia": nueva_direccion.provincia,
            "localidad": nueva_direccion.localidad
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear un estadio
@equipos_router.post("/crear_estadio/")
async def crear_estadio(
    estadio: PydanticEstadios, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para crear un estadio
    
    Parámetros:
    - estadio {Object}: que define un estadio
    - db {Object}: conexión a una base de datos

    Retorna:
    - estadio {Object}: detalles del estadio creado o error
    """
    try:
        logger.info(f"Creando nuevo estadop: {estadio}")
        # crea una nueva entidad en la base de datos
        nuevo_estadio = ORMEstadios(**estadio.model_dump())
        db.add(nuevo_estadio)
        await db.commit()
        await db.refresh(nuevo_estadio)
        logger.info(f"Estado {nuevo_estadio} creado satisfactoriamente")
        # respuesta satisfactoria
        return {
            "estadio_id": nuevo_estadio.estadio_id,
            "inauguracion": nuevo_estadio.inauguracion,
            "nombre_estadio": nuevo_estadio.nombre_estadio,
            "capacidad": nuevo_estadio.capacidad,
            "comunidad_autonoma": nuevo_estadio.comunidad_autonoma_id,
            "provincia": nuevo_estadio.provincia_id,
            "localidad": nuevo_estadio.localidad
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear una denominación de un equipo
@equipos_router.post("/crear_denominacion_equipo/")
async def crear_denominacion_equipo(
    denominacion_equipo: PydanticDenominacionesEquipo, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para vincular una denominación a un equipo
    
    Parámetros:
    - denominacion_equipo {Object}: que define una denominación de un equipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - denominacion_equipo {Object}: detalles de la denominación creada o error
    """
    try:
        logger.info(f"Creando nueva denominación de equipo: {denominacion_equipo}")
        # crea una nueva entidad en la base de datos
        nueva_denominacion_equipo = ORMDenominacionesEquipo(**denominacion_equipo.model_dump())
        db.add(nueva_denominacion_equipo)
        await db.commit()
        await db.refresh(nueva_denominacion_equipo)
        logger.info(f"Denominación de equipo {nueva_denominacion_equipo} creada satisfactoriamente")
        # respuesta satisfactoria
        return {
            "denominaciones_equipo_id": nueva_denominacion_equipo.denominaciones_equipo_id,
            "equipo": nueva_denominacion_equipo.equipo,
            "denominacion": nueva_denominacion_equipo.denominacion
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear un logotipo de un equipo
@equipos_router.post("/crear_logotipo_equipo/")
async def crear_logotipo_equipo(
    logotipo_equipo: PydanticLogotiposEquipo, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para vincular un logotipo a un equipo
    
    Parámetros:
    - logotipo_equipo {Object}: que define un logotipo de un equipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - logotipo_equipo {Object}: detalles del logotipo creado o error
    """
    try:
        logger.info(f"Creando nuevo logotipo de equipo: {logotipo_equipo}")
        # crea una nueva entidad en la base de datos
        nuevo_logotipo_equipo = ORMLogotiposEquipo(**logotipo_equipo.model_dump())
        db.add(nuevo_logotipo_equipo)
        await db.commit()
        await db.refresh(nuevo_logotipo_equipo)
        logger.info(f"Logotipo de equipo {nuevo_logotipo_equipo} creado satisfactoriamente")
        # respuesta satisfactoria
        return {
            "logotipos_equipo_id": nuevo_logotipo_equipo.logotipos_equipo_id,
            "equipo": nuevo_logotipo_equipo.equipo_id,
            "logotipo": nuevo_logotipo_equipo.logotipo
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear una dirección de un equipo
@equipos_router.post("/crear_direccion_equipo/")
async def crear_direccion_equipo(
    direccion_equipo: PydanticDireccionesEquipo, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para vincular una dirección a un equipo
    
    Parámetros:
    - direccion_equipo {Object}: que define una dirección de un equipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - direccion_equipo {Object}: detalles de la direccion creada o error
    """
    try:
        logger.info(f"Creando nueva dirección de equipo: {direccion_equipo}")
        # crea una nueva entidad en la base de datos
        nueva_direccion_equipo = ORMDireccionesEquipo(**direccion_equipo.model_dump())
        db.add(nueva_direccion_equipo)
        await db.commit()
        await db.refresh(nueva_direccion_equipo)
        logger.info(f"Logotipo de equipo {nueva_direccion_equipo} creado satisfactoriamente")
        # respuesta satisfactoria
        return {
            "direccion_equipo_id": nueva_direccion_equipo.direcciones_equipo_id,
            "equipo": nueva_direccion_equipo.equipo_id,
            "direccion": nueva_direccion_equipo.direccion
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear un estadio de un equipo
@equipos_router.post("/crear_estadio_equipo/")
async def crear_estadion_equipo(
    estadio_equipo: PydanticEstadiosEquipo, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para vincular un logotipo a un equipo
    
    Parámetros:
    - estadio_equipo {Object}: que define un estadio de un equipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - estadio_equipo {Object}: detalles del estadio creado o error
    """
    try:
        logger.info(f"Creando nuevo estadio de equipo: {estadio_equipo}")
        # crea una nueva entidad en la base de datos
        nuevo_estadio_equipo = ORMEstadiosEquipo(**estadio_equipo.model_dump())
        db.add(nuevo_estadio_equipo)
        await db.commit()
        await db.refresh(nuevo_estadio_equipo)
        logger.info(f"Estadio de equipo {nuevo_estadio_equipo} creado satisfactoriamente")
        # respuesta satisfactoria
        return {
            "estadios_equipo_id": nuevo_estadio_equipo.estadios_equipo_id,
            "equipo": nuevo_estadio_equipo.equipo,
            "estadio": nuevo_estadio_equipo.estadio
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para crear una competición de un equipo
@equipos_router.post("/crear_competicion_equipo/")
async def crear_competicion_equipo(
    competicion_equipo: PydanticCompeticionesEquipo, 
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para vincular una competición a un equipo
    
    Parámetros:
    - competicion_equipo {Object}: que define un competición de un equipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - competicion_equipo {Object}: detalles de la competición creada o error
    """
    try:
        logger.info(f"Creando nuevo competición de equipo: {competicion_equipo}")
        # crea una nueva entidad en la base de datos
        nueva_competicion_equipo = ORMCompeticionesEquipo(**competicion_equipo.model_dump())
        db.add(nueva_competicion_equipo)
        await db.commit()
        await db.refresh(nueva_competicion_equipo)
        logger.info(f"Competición de equipo {nueva_competicion_equipo} creada satisfactoriamente")
        # respuesta satisfactoria
        return {
            "competiciones_equipo_id": nueva_competicion_equipo.competiciones_equipo_id,
            "competicion": nueva_competicion_equipo.competicion,
            "temporada": nueva_competicion_equipo.temporada_id,
            "equipo": nueva_competicion_equipo.equipo
        }
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para eliminar un equipo base de la base de datos
@equipos_router.delete("/eliminar_equipo_base/")
async def eliminar_equipo_base(
    equipo_base_id: int = Query(
        description="ID del equipo base"
    ),
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para borrar un equipo base

    Parámetros:
    - equipo_base_id {int}: el id que identifica un equipo base
    - db {Object}: conexión a una base de datos

    Retorna:
    - Mensaje satisfactorio o error
    """
    try:
        logger.info(f"Obteniendo equipo base: {equipo_base_id}")
        # obtener el equipo base para identificarlo
        equipo_base = await db.get(ORMIndiceEquipos, equipo_base_id)
        # borra entidad de la base de datos si existe
        if equipo_base:
            # borrar equipo base
            logger.info(f"Borrando equipo base: {equipo_base.indice_equipo_id}")
            await db.delete(equipo_base)
            await db.commit()
            logger.info(f"Equipo base {equipo_base_id} borrado satisfactoriamente")
            # respuesta satisfactoria
            return {"mensaje": f"Equipo base {equipo_base_id} borrado satisfactoriamente"}
        # respuesta de error si el equipo base no existe
        else:
            logger.warning(f"No se encontró el equipo base con ID: {equipo_base_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Equipo base no existe"
            )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}"
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para eliminar un equipo de la base de datos
@equipos_router.delete("/eliminar_equipo/")
async def eliminar_equipo(
    equipo_id: int = Query(
        description="ID del equipo"
    ),
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para borrar un equipo

    Parámetros:
    - equipo_id {int}: el id que identifica un equipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - Mensaje satisfactorio o error
    """
    try:
        logger.info(f"Obteniendo equipo: {equipo_id}")
        # obtener el equipo para identificarlo
        equipo = await db.get(ORMEquipos, equipo_id)
        # borra entidad de la base de datos si existe
        if equipo:
            # borrar equipo
            logger.info(f"Borrando equipo: {equipo.equipo_id}")
            await db.delete(equipo)
            await db.commit()
            logger.info(f"Equipo {equipo_id} borrado satisfactoriamente")
            # respuesta satisfactoria
            return {"mensaje": f"Equipo {equipo_id} borrado satisfactoriamente"}
        # respuesta de error si el equipo no existe
        else:
            logger.warning(f"No se encontró el equipo con ID: {equipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Equipo no existe"
            )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}"
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para eliminar una denominación de la base de datos
@equipos_router.delete("/eliminar_denominacion/")
async def eliminar_denominacion(
    denominacion_id: int = Query(
        description="ID de la denominación"
    ),
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para borrar una denominación

    Parámetros:
    - denominacion_id {int}: el id que identifica una denominación
    - db {Object}: conexión a una base de datos

    Retorna:
    - Mensaje satisfactorio o error
    """
    try:
        logger.info(f"Obteniendo denominación: {denominacion_id}")
        # obtener la denominación para identificarla
        denominacion = await db.get(ORMDenominaciones, denominacion_id)
        # borra entidad de la base de datos si existe
        if denominacion:
            # borrar denominación
            logger.info(f"Borrando denominación: {denominacion.denominacion_id}")
            await db.delete(denominacion)
            await db.commit()
            logger.info(f"Denominación {denominacion_id} borrada satisfactoriamente")
            # respuesta satisfactoria
            return {"mensaje": f"Denominación {denominacion_id} borrada satisfactoriamente"}
        # respuesta de error si la denominación no existe
        else:
            logger.warning(f"No se encontró la denominación con ID: {denominacion_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Denominación no existe"
            )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}"
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para eliminar un logotipo de la base de datos
@equipos_router.delete("/eliminar_logotipo/")
async def eliminar_logotipo(
    logotipo_id: int = Query(
        description="ID del logotipo"
    ),
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para borrar un logotipo

    Parámetros:
    - logotipo_id {int}: el id que identifica un logotipo
    - db {Object}: conexión a una base de datos

    Retorna:
    - Mensaje satisfactorio o error
    """
    try:
        logger.info(f"Obteniendo logotipo: {logotipo_id}")
        # obtener el logotipo para identificarlo
        logotipo = await db.get(ORMLogotipos, logotipo_id)
        # borra entidad de la base de datos si existe
        if logotipo:
            # borrar logotipo
            logger.info(f"Borrando logotipo: {logotipo.logotipo_id}")
            await db.delete(logotipo)
            await db.commit()
            logger.info(f"Logotipo {logotipo_id} borrado satisfactoriamente")
            # respuesta satisfactoria
            return {"mensaje": f"Logotipo {logotipo_id} borrado satisfactoriamente"}
        # respuesta de error si el logotipo no existe
        else:
            logger.warning(f"No se encontró el logotipo con ID: {logotipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Logotipo no existe"
            )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}"
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para eliminar un estadio de la base de datos
@equipos_router.delete("/eliminar_estadio/")
async def eliminar_estadio(
    estadio_id: int = Query(
        description="ID del estadio"
    ),
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para borrar un estadio

    Parámetros:
    - estadio_id {int}: el id que identifica un estadio
    - db {Object}: conexión a una base de datos

    Retorna:
    - Mensaje satisfactorio o error
    """
    try:
        logger.info(f"Obteniendo estadio: {estadio_id}")
        # obtener el estadio para identificarlo
        estadio = await db.get(ORMEstadios, estadio_id)
        # borra entidad de la base de datos si existe
        if estadio:
            # borrar estadio
            logger.info(f"Borrando estadio: {estadio.estadio_id}")
            await db.delete(estadio)
            await db.commit()
            logger.info(f"Estadio {estadio_id} borrado satisfactoriamente")
            # respuesta satisfactoria
            return {"mensaje": f"Estadio {estadio_id} borrado satisfactoriamente"}
        # respuesta de error si el estadio no existe
        else:
            logger.warning(f"No se encontró el estadio con ID: {estadio_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Estadio no existe"
            )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}"
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para eliminar una dirección de la base de datos
@equipos_router.delete("/eliminar_direccion/")
async def eliminar_direccion(
    direccion_id: int = Query(
        description="ID de la dirección"
    ),
    db: AsyncSession = Depends(comunicar_base_datos)
):
    """
    Función asyncrónica para borrar una dirección

    Parámetros:
    - direccion_id {int}: el id que identifica una dirección
    - db {Object}: conexión a una base de datos

    Retorna:
    - Mensaje satisfactorio o error
    """
    try:
        logger.info(f"Obteniendo dirección: {direccion_id}")
        # obtener la dirección para identificarla
        direccion = await db.get(ORMDirecciones, direccion_id)
        # borra entidad de la base de datos si existe
        if direccion:
            # borrar dirección
            logger.info(f"Borrando dirección: {direccion.direccion_id}")
            await db.delete(direccion)
            await db.commit()
            logger.info(f"Dirección {direccion_id} borrada satisfactoriamente")
            # respuesta satisfactoria
            return {"mensaje": f"Dirección {direccion_id} borrada satisfactoriamente"}
        # respuesta de error si la dirección no existe
        else:
            logger.warning(f"No se encontró la dirección con ID: {direccion_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Dirección no existe"
            )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}"
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para editar un equipo base de la base de datos
@equipos_router.patch("/editar_equipo_base/")
async def editar_equipo_base(
    datos_actualizados: EditarIndiceEquipos = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    equipo_base_id: int = Query(..., description="ID del equipo base"),
):
    """
    Función asíncrona para editar parcialmente un equipo base

    Parámetros:
    - equipo_base_id {int}: ID del equipo base a modificar
    - datos_actualizados {EditarIndiceEquipos}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo equipo base con ID: {equipo_base_id}")
        # obtener el equipo base para identificarlo
        equipo_base = await db.get(ORMIndiceEquipos, equipo_base_id)
        # respuesta de error para equipo base no encontrado
        if not equipo_base:
            logger.warning(f"No se encontró el equipo base con ID: {equipo_base_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Equipo base no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar el equipo base {equipo_base_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(equipo_base, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(equipo_base)
        # respuesta satisfactoria
        return {"mensaje": f"Equipo base {equipo_base_id} actualizado correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar un equipo de la base de datos
@equipos_router.patch("/editar_equipo/")
async def editar_equipo(
    datos_actualizados: EditarEquipos = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    equipo_id: int = Query(..., description="ID del equipo"),
):
    """
    Función asíncrona para editar parcialmente un equipo

    Parámetros:
    - equipo_id {int}: ID del equipo a modificar
    - datos_actualizados {EditarEquipos}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo equipo con ID: {equipo_id}")
        # obtener el equipo para identificarlo
        equipo = await db.get(ORMEquipos, equipo_id)
        # respuesta de error para equipo no encontrado
        if not equipo:
            logger.warning(f"No se encontró el equipo con ID: {equipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Equipo no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar el equipo {equipo_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(equipo, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(equipo)
        # respuesta satisfactoria
        return {"mensaje": f"Equipo {equipo_id} actualizado correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar una denominación de la base de datos
@equipos_router.patch("/editar_denominacion/")
async def editar_denominacion(
    datos_actualizados: EditarDenominaciones = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    denominacion_id: int = Query(..., description="ID de la denominación"),
):
    """
    Función asíncrona para editar parcialmente una denominación

    Parámetros:
    - denominacion_id {int}: ID de la denominación a modificar
    - datos_actualizados {EditarDenominaciones}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo denominación con ID: {denominacion_id}")
        # obtener la denominación para identificarla
        denominacion = await db.get(ORMDenominaciones, denominacion_id)
        # respuesta de error para equipo no encontrado
        if not denominacion:
            logger.warning(f"No se encontró la denominación con ID: {denominacion_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Denominación no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar la denominación {denominacion_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(denominacion, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(denominacion)
        # respuesta satisfactoria
        return {"mensaje": f"Denominación {denominacion_id} actualizada correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar un logotipo de la base de datos
@equipos_router.patch("/editar_logotipos/")
async def editar_logotipos(
    datos_actualizados: EditarLogotipos = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    logotipo_id: int = Query(..., description="ID del logotipo"),
):
    """
    Función asíncrona para editar parcialmente un logotipo

    Parámetros:
    - logotipo_id {int}: ID del logotipo a modificar
    - datos_actualizados {EditarLogotipos}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo logotipo con ID: {logotipo_id}")
        # obtener el logotipo para identificarlo
        logotipo = await db.get(ORMLogotipos, logotipo_id)
        # respuesta de error para logotipo no encontrado
        if not logotipo:
            logger.warning(f"No se encontró el logotipo con ID: {logotipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Logotipo no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar el logotipo {logotipo_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(logotipo, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(logotipo)
        # respuesta satisfactoria
        return {"mensaje": f"Logotipo {logotipo_id} actualizado correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar un estadio de la base de datos
@equipos_router.patch("/editar_estadio/")
async def editar_estadio(
    datos_actualizados: EditarEstadios = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    estadio_id: int = Query(..., description="ID del estadio"),
):
    """
    Función asíncrona para editar parcialmente un estadio

    Parámetros:
    - estadio_id {int}: ID del estadio a modificar
    - datos_actualizados {EditarEstadios}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo estadio con ID: {estadio_id}")
        # obtener el estadio para identificarlo
        estadio = await db.get(ORMEstadios, estadio_id)
        # respuesta de error para estadio no encontrado
        if not estadio:
            logger.warning(f"No se encontró el estadio con ID: {estadio_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Estadio no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar el estadio {estadio_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(estadio, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(estadio)
        # respuesta satisfactoria
        return {"mensaje": f"Estadio {estadio_id} actualizado correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar una dirección de la base de datos
@equipos_router.patch("/editar_direccion/")
async def editar_direccion(
    datos_actualizados: EditarDirecciones = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    direccion_id: int = Query(..., description="ID de la dirección"),
):
    """
    Función asíncrona para editar parcialmente una dirección

    Parámetros:
    - direccion_id {int}: ID de la dirección a modificar
    - datos_actualizados {EditarDirecciones}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo dirección con ID: {direccion_id}")
        # obtener la dirección para identificarla
        direccion = await db.get(ORMDirecciones, direccion_id)
        # respuesta de error para equipo no encontrado
        if not direccion:
            logger.warning(f"No se encontró la dirección con ID: {direccion_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Dirección no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar la dirección {direccion_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(direccion, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(direccion)
        # respuesta satisfactoria
        return {"mensaje": f"Dirección {direccion_id} actualizada correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar una competición de equipo de la base de datos
@equipos_router.patch("/editar_competicion_equipo/")
async def editar_competicion_equipo(
    datos_actualizados: EditarCompeticionesEquipo = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    competicion_equipo_id: int = Query(..., description="ID de la competición de equipo"),
):
    """
    Función asíncrona para editar parcialmente una competición de equipo

    Parámetros:
    - competicion_equipo_id {int}: ID de la competición a modificar
    - datos_actualizados {EditarCompeticionesEquipo}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo competición de equipo con ID: {competicion_equipo_id}")
        # obtener la competición de equipo para identificarla
        competicion_equipo = await db.get(ORMCompeticionesEquipo, competicion_equipo_id)
        # respuesta de error para competición de equipo no encontrada
        if not competicion_equipo:
            logger.warning(f"No se encontró la competición de equipo con ID: {competicion_equipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Competición de equipo no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar la competición de equipo {competicion_equipo_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(competicion_equipo, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(competicion_equipo)
        # respuesta satisfactoria
        return {"mensaje": f"Competición de equipo {competicion_equipo_id} actualizada correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar una denominación de equipo de la base de datos
@equipos_router.patch("/editar_denominacion_equipo/")
async def editar_denominacion_equipo(
    datos_actualizados: EditarDenominacionesEquipo = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    denominacion_equipo_id: int = Query(..., description="ID de la denominación de equipo"),
):
    """
    Función asíncrona para editar parcialmente una denominación de equipo

    Parámetros:
    - denominacion_equipo_id {int}: ID de la denominación a modificar
    - datos_actualizados {EditarDenominacionesEquipo}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo denominación de equipo con ID: {denominacion_equipo_id}")
        # obtener la denominación de equipo para identificarla
        denominacion_equipo = await db.get(ORMDenominacionesEquipo, denominacion_equipo_id)
        # respuesta de error para denominación de equipo no encontrada
        if not denominacion_equipo:
            logger.warning(f"No se encontró la denominación de equipo con ID: {denominacion_equipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Denominación de equipo no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar la denominación de equipo {denominacion_equipo_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(denominacion_equipo, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(denominacion_equipo)
        # respuesta satisfactoria
        return {"mensaje": f"Denominación de equipo {denominacion_equipo_id} actualizada correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar un logotipo de equipo de la base de datos
@equipos_router.patch("/editar_logotipo_equipo/")
async def editar_logotipo_equipo(
    datos_actualizados: EditarLogotiposEquipo = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    logotipo_equipo_id: int = Query(..., description="ID del logotipo de equipo"),
):
    """
    Función asíncrona para editar parcialmente un logotipo de equipo

    Parámetros:
    - logotipo_equipo_id {int}: ID del logotipo a modificar
    - datos_actualizados {EditarLogotiposEquipo}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo logotipo de equipo con ID: {logotipo_equipo_id}")
        # obtener el logotipo de equipo para identificarlo
        logotipo_equipo = await db.get(ORMLogotiposEquipo, logotipo_equipo_id)
        # respuesta de error para logotipo de equipo no encontrada
        if not logotipo_equipo:
            logger.warning(f"No se encontró el logotipo de equipo con ID: {logotipo_equipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Logotipo de equipo no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar el logotipo de equipo {logotipo_equipo_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(logotipo_equipo, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(logotipo_equipo)
        # respuesta satisfactoria
        return {"mensaje": f"Logotipo de equipo {logotipo_equipo_id} actualizado correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar una dirección de equipo de la base de datos
@equipos_router.patch("/editar_direccion_equipo/")
async def editar_direccion_equipo(
    datos_actualizados: EditarDireccionesEquipo = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    direccion_equipo_id: int = Query(..., description="ID de la dirección de equipo"),
):
    """
    Función asíncrona para editar parcialmente una dirección de equipo

    Parámetros:
    - direccion_equipo_id {int}: ID de la dirección a modificar
    - datos_actualizados {EditarDireccionesEquipo}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo dirección de equipo con ID: {direccion_equipo_id}")
        # obtener la dirección de equipo para identificarla
        direccion_equipo = await db.get(ORMDireccionesEquipo, direccion_equipo_id)
        # respuesta de error para dirección de equipo no encontrada
        if not direccion_equipo:
            logger.warning(f"No se encontró la dirección de equipo con ID: {direccion_equipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Dirección de equipo no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar la dirección de equipo {direccion_equipo_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(direccion_equipo, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(direccion_equipo)
        # respuesta satisfactoria
        return {"mensaje": f"Dirección de equipo {direccion_equipo_id} actualizada correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para editar un estadio de equipo de la base de datos
@equipos_router.patch("/editar_estadio_equipo/")
async def editar_estadio_equipo(
    datos_actualizados: EditarEstadiosEquipo = Body(...),
    db: AsyncSession = Depends(comunicar_base_datos),
    estadio_equipo_id: int = Query(..., description="ID del estadio de equipo"),
):
    """
    Función asíncrona para editar parcialmente un estadio de equipo

    Parámetros:
    - estadio_equipo_id {int}: ID del estadio a modificar
    - datos_actualizados {EditarEstadiosEquipo}: campos opcionales a modificar
    - db {AsyncSession}: sesión de conexión a la base de datos

    Retorna:
    - Mensaje con los campos actualizados o error
    """
    try:
        logger.info(f"Obteniendo estadio de equipo con ID: {estadio_equipo_id}")
        # obtener el estadio de equipo para identificarlo
        estadio_equipo = await db.get(ORMEstadiosEquipo, estadio_equipo_id)
        # respuesta de error para estadio de equipo no encontrada
        if not estadio_equipo:
            logger.warning(f"No se encontró el estadio de equipo con ID: {estadio_equipo_id}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content="Estadio de equipo no existe"
            )
        # variable para acceder a los datos proporcionados por los parámetros
        actualizaciones = datos_actualizados.model_dump(exclude_unset=True)
        # respuesta de error para valores vacíos
        if not actualizaciones:
            logger.info(f"No se proporcionaron datos para actualizar el estadio de equipo {estadio_equipo_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        # iterar los campos editados para almacenarlos
        for campo, valor in actualizaciones.items():
            setattr(estadio_equipo, campo, valor)
            logger.info(f"Campo '{campo}' actualizado a '{valor}'")
        # actualizar la base de datos
        await db.commit()
        await db.refresh(estadio_equipo)
        # respuesta satisfactoria
        return {"mensaje": f"Estadio de equipo {estadio_equipo_id} actualizado correctamente", "datos_actualizados": actualizaciones}
    # error si se incumple una restricción en la base de datos
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio inaccesible temporalmente"
        )


# router para obtener un equipo_base o todos los equipos_base
# en la base de datos
@equipos_router.get("/equipos_base/")
async def obtener_equipo_base(
    equipo_base_id: int = Query(
        None, description="ID del equipo base"
    ),
    db: AsyncSession = Depends(comunicar_base_datos),
):
    """
    Función asyncrónica parar obtener un equipo base
    
    Parámetros:
    - equipo_base_id {int}: el id del equipo base a buscar
    - db {Object}: conexión a una base de datos

    Retorna:
    - equipos_base {Array[Object]} listado de equipos base
    - o error
    """
    try:
        # búsqueda por equipo_base_id
        if equipo_base_id is not None:
            logger.info(f"Obteniendo equipo base: {equipo_base_id}")
            equipo_base = await db.get(ORMIndiceEquipos, equipo_base_id)
            # error por equipo base no encontrado
            if equipo_base is None:
                mensaje = f"Equipo base '{equipo_base_id}' no encontrado"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Equipo base con ID: '{equipo_base_id}' encontrado")
            return {"data": equipo_base}
        # búsqueda general si no se han especificado ningún parámetro
        logger.info("Obteniendo todos los equipos base")
        result = await db.execute(select(ORMIndiceEquipos))
        equipos_base = result.scalars().all()
        # mensaje para búsqueda insatisfactoria
        if not equipos_base:
            mensaje = "No hay equipos base creados"
            logger.warning(mensaje)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensaje
            )
        logger.info("Todas los equipos base obtenidos")
        return {"data": equipos_base}
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para obtener un equipo, todos los equipos,
# todos los equipos de un equipo base, todos los equipos
# de una competición, todos los equipos de una temporada
# o todos los equipos de una competición en una
# temporada en la base de datos
@equipos_router.get("/equipos/")
async def obtener_equipo(
    equipo_id: int = Query(
        None, description="ID del equipo"
    ),
    equipo_base_id: int = Query(
        None, description="ID del equipo base"
    ),
    competicion_id: int = Query(
        None, description="ID de la competición"
    ),
    temporada_id: int = Query(
        None, description="ID de la temporada"
    ),
    db: AsyncSession = Depends(comunicar_base_datos),
):
    """
    Función asyncrónica parar obtener un equipo
    
    Parámetros:
    - equipo_id {int}: el id del equipo a buscar
    - equipo_base_id {int}: el id del equipo base a buscar
    - competicion_id {int}: el id de la competición a buscar
    - temporada_id {int}: el id de la temporada a buscar
    - db {Object}: conexión a una base de datos

    Retorna:
    - equipos {Array[Object]} listado de equipos
    - o error
    """
    try:
        # búsqueda por equipo_id
        if equipo_id is not None:
            logger.info(f"Obteniendo equipo: {equipo_id}")
            equipo = await db.get(ORMEquipos, equipo_id)
            # error por equipo no encontrado
            if equipo is None:
                mensaje = f"Equipo '{equipo_id}' no encontrado"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Equipo con ID: '{equipo_id}' encontrado")
            return {"data": equipo}
        # búsqueda por equipo_base_id
        if equipo_base_id is not None:
            logger.info(f"Obteniendo equipos de equipo base: {equipo_base_id}")
            result = await db.execute(select(ORMEquipos).filter(ORMEquipos.equipo_base_id == equipo_base_id))
            equipos = result.scalars().all()
            # error por equipo base no encontrado
            if not equipos:
                mensaje = f"No se encuentran equipos para el equipo base {equipo_base_id}"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            logger.info(f"Equipos del equipo base: '{equipo_base_id}' encontrados")
            return {"data": equipos}
        # búsqueda por competicion_id & temporada_id
        if competicion_id is not None and temporada_id is not None:
            logger.info(f"Obteniendo equipos de competición: {competicion_id}")
            result = await db.execute(select(ORMCompeticionesEquipo).filter(ORMCompeticionesEquipo.competicion_id == competicion_id))
            equipos_competicion = result.scalars().all()
            # lista vacía para incluir los datos de los equipos
            equipos = []
            # iterar en la listado de la base de datos para añadirlos a la respuesta
            for equipo in equipos_competicion:
                result = await db.execute(select(ORMEquipos).filter(ORMEquipos.equipo_id == equipo.equipo, ORMEquipos.temporada_id == temporada_id))
                # añadir equipo al listado
                equipos.append(result)
            # error por equipos no encontrados
            if len(equipos) == 0:
                mensaje = f"No se encuentran equipos para la competición {competicion_id} de la temporada {temporada_id}"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Equipos de la competición: '{competicion_id}' para la temporada '{temporada_id}' encontrados")
            return {"data": equipos}
        # búsqueda por competicion_id
        if competicion_id is not None:
            logger.info(f"Obteniendo equipos de competición: {competicion_id}")
            stmt = (
                select(ORMEquipos)
                .join(ORMEquipos.competiciones)
                .where(ORMCompeticionesEquipo.competicion == competicion_id)
                .options(
                    joinedload(ORMEquipos.competiciones)
                    .joinedload(ORMCompeticionesEquipo.competicion)
                )
            )
            result = await db.execute(stmt)
            equipos = result.scalars().all()
            # error por equipos no encontrados
            if not equipos:
                mensaje = f"No se encuentran equipos para la competición {competicion_id}"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Equipos de la competición: '{competicion_id}' encontrados")
            return {"data": equipos}
        # búsqueda por temporada_id
        if temporada_id is not None:
            logger.info(f"Obteniendo equipos de temporada: {temporada_id}")
            result = await db.execute(select(ORMEquipos).filter(ORMEquipos.temporada_id == temporada_id))
            equipos = result.scalars().all()
            # error por equipos no encontrados
            if not equipos:
                mensaje = f"No se encuentran equipos para la temporada {temporada_id}"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Equipos de la temporada: '{temporada_id}' encontrados")
            return {"data": equipos}
        # búsqueda general si no se han especificado ningún parámetro
        logger.info("Obteniendo todos los equipos")
        result = await db.execute(select(ORMEquipos))
        equipos = result.scalars().all()
        # mensaje para búsqueda insatisfactoria
        if not equipos:
            mensaje = "No hay equipos creados"
            logger.warning(mensaje)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensaje
            )
        logger.info("Todas los equipos obtenidos")
        return {"data": equipos}
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para obtener una denominación, todas las
# denominaciones o todas las denominaciones de 
# un equipo base en la base de datos
@equipos_router.get("/denominaciones/")
async def obtener_denominacion(
    denominacion_id: int = Query(
        None, description="ID de la denominación"
    ),
    equipo_base_id: int = Query(
        None, description="ID del equipo base"
    ),
    db: AsyncSession = Depends(comunicar_base_datos),
):
    """
    Función asyncrónica parar obtener una denominación
    
    Parámetros:
    - denominacion_id {int}: el id de la denominación a buscar
    - equipo_base_id {int}: el id del equipo base a buscar
    - db {Object}: conexión a una base de datos

    Retorna:
    - denominaciones {Array[Object]} listado de denominaciones
    - o error
    """
    try:
        # búsqueda por denominacion_id
        if denominacion_id is not None:
            logger.info(f"Obteniendo denominación: {denominacion_id}")
            denominacion = await db.get(ORMDenominaciones, denominacion_id)
            # error por denominación no encontrada
            if denominacion is None:
                mensaje = f"Denominación '{denominacion_id}' no encontrada"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Denominación con ID: '{denominacion_id}' encontrada")
            return {"data": denominacion}
        # búsqueda por equipo_base_id
        if equipo_base_id is not None:
            logger.info(f"Obteniendo equipos de equipo base: {equipo_base_id}")
            stmt = (
                select(ORMEquipos)
                .join(ORMEquipos.denominaciones)
                .where(ORMDenominacionesEquipo.equipo_id == equipo_base_id)
                .options(
                    joinedload(ORMEquipos.denominaciones)
                    .joinedload(ORMDenominacionesEquipo.denominacion)
                )
            )
            result = await db.execute(stmt)
            denominaciones = result.scalars().all()
            # error por equipo base no encontrado
            if denominaciones is None:
                mensaje = f"Denominaciones pertenecientes a equipo base '{equipo_base_id}' no encontradas"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Denominaciones pertenecientes a equipo base con ID: '{equipo_base_id}' encontradas")
            return {"data": denominaciones}
        # búsqueda general si no se han especificado ningún parámetro
        logger.info("Obteniendo todas las denominaciones")
        result = await db.execute(select(ORMDenominaciones))
        denominaciones = result.scalars().all()
        # mensaje para búsqueda insatisfactoria
        if not denominaciones:
            mensaje = "No hay denominaciones creados"
            logger.warning(mensaje)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensaje
            )
        logger.info("Todas las denominaciones obtenidas")
        return {"data": denominaciones}
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para obtener un logotipo, todos los
# logotipos o todos los logotipos de 
# un equipo base en la base de datos
@equipos_router.get("/logotipos/")
async def obtener_logotipo(
    logotipo_id: int = Query(
        None, description="ID del logotipos"
    ),
    equipo_base_id: int = Query(
        None, description="ID del equipo base"
    ),
    db: AsyncSession = Depends(comunicar_base_datos),
):
    """
    Función asyncrónica parar obtener un logotipo
    
    Parámetros:
    - logotipo_id {int}: el id del logotipo a buscar
    - equipo_base_id {int}: el id del equipo base a buscar
    - db {Object}: conexión a una base de datos

    Retorna:
    - logotipos {Array[Object]} listado de logotipos
    - o error
    """
    try:
        # búsqueda por logotipo_id
        if logotipo_id is not None:
            logger.info(f"Obteniendo logotipo: {logotipo_id}")
            logotipo = await db.get(ORMLogotipos, logotipo_id)
            # error por logotipo no encontrado
            if logotipo is None:
                mensaje = f"Logotipo '{logotipo_id}' no encontrado"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Logotipo con ID: '{logotipo_id}' encontrado")
            return {"data": logotipo}
        # búsqueda por equipo_base_id
        if equipo_base_id is not None:
            logger.info(f"Obteniendo logotipos de equipo base: {equipo_base_id}")
            stmt = (
                select(ORMEquipos)
                .join(ORMEquipos.logotipos)
                .where(ORMLogotiposEquipo.equipo_id == equipo_base_id)
                .options(
                    joinedload(ORMEquipos.logotipos)
                    .joinedload(ORMLogotiposEquipo.logotipo)
                )
            )
            result = await db.execute(stmt)
            logotipos = result.scalars().all()
            # error por equipo base no encontrado
            if logotipos is None:
                mensaje = f"Logotipos pertenecientes a equipo base '{equipo_base_id}' no encontrados"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Logotipos pertenecientes a equipo base con ID: '{equipo_base_id}' encontrados")
            return {"data": logotipos}
        # búsqueda general si no se han especificado ningún parámetro
        logger.info("Obteniendo todos los logotipos")
        result = await db.execute(select(ORMLogotipos))
        logotipos = result.scalars().all()
        # mensaje para búsqueda insatisfactoria
        if not logotipos:
            mensaje = "No hay logotipos creados"
            logger.warning(mensaje)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensaje
            )
        logger.info("Todos los logotipos obtenidos")
        return {"data": logotipos}
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para obtener una dirección, todas las
# direcciones o todas las direcciones de 
# un equipo base en la base de datos
@equipos_router.get("/direcciones/")
async def obtener_direccion(
    direccion_id: int = Query(
        None, description="ID de la dirección"
    ),
    equipo_base_id: int = Query(
        None, description="ID del equipo base"
    ),
    db: AsyncSession = Depends(comunicar_base_datos),
):
    """
    Función asyncrónica parar obtener una dirección
    
    Parámetros:
    - direccion_id {int}: el id de la dirección a buscar
    - equipo_base_id {int}: el id del equipo base a buscar
    - db {Object}: conexión a una base de datos

    Retorna:
    - direcciones {Array[Object]} listado de direcciones
    - o error
    """
    try:
        # búsqueda por direccion_id
        if direccion_id is not None:
            logger.info(f"Obteniendo dirección: {direccion_id}")
            denominacion = await db.get(ORMDirecciones, direccion_id)
            # error por dirección no encontrada
            if denominacion is None:
                mensaje = f"Dirección '{direccion_id}' no encontrada"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Dirección con ID: '{direccion_id}' encontrada")
            return {"data": denominacion}
        # búsqueda por equipo_base_id
        if equipo_base_id is not None:
            logger.info(f"Obteniendo equipos de equipo base: {equipo_base_id}")
            stmt = (
                select(ORMEquipos)
                .join(ORMEquipos.direcciones)
                .where(ORMDireccionesEquipo.equipo_id == equipo_base_id)
                .options(
                    joinedload(ORMEquipos.direcciones)
                    .joinedload(ORMDireccionesEquipo.direccion)
                )
            )
            result = await db.execute(stmt)
            direcciones = result.scalars().all()
            # error por equipo base no encontrado
            if direcciones is None:
                mensaje = f"Direcciones pertenecientes a equipo base '{equipo_base_id}' no encontradas"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Direcciones pertenecientes a equipo base con ID: '{equipo_base_id}' encontradas")
            return {"data": direcciones}
        # búsqueda general si no se han especificado ningún parámetro
        logger.info("Obteniendo todas las direcciones")
        result = await db.execute(select(ORMDirecciones))
        direcciones = result.scalars().all()
        # mensaje para búsqueda insatisfactoria
        if not direcciones:
            mensaje = "No hay direcciones creados"
            logger.warning(mensaje)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensaje
            )
        logger.info("Todas las direcciones obtenidas")
        return {"data": direcciones}
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")


# router para obtener un estadio, todos los
# estadios o todos los estadios de 
# un equipo base en la base de datos
@equipos_router.get("/estadios/")
async def obtener_estadio(
    estadio_id: int = Query(
        None, description="ID del estadio"
    ),
    equipo_base_id: int = Query(
        None, description="ID del equipo base"
    ),
    db: AsyncSession = Depends(comunicar_base_datos),
):
    """
    Función asyncrónica parar obtener un estadio
    
    Parámetros:
    - estadio_id {int}: el id del estadio a buscar
    - equipo_base_id {int}: el id del equipo base a buscar
    - db {Object}: conexión a una base de datos

    Retorna:
    - estadios {Array[Object]} listado de estadios
    - o error
    """
    try:
        # búsqueda por estadio_id
        if estadio_id is not None:
            logger.info(f"Obteniendo estadio: {estadio_id}")
            estadio = await db.get(ORMEstadios, estadio_id)
            # error por estadio no encontrado
            if estadio is None:
                mensaje = f"Estadio '{estadio_id}' no encontrado"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Estadio con ID: '{estadio_id}' encontrado")
            return {"data": estadio}
        # búsqueda por equipo_base_id
        if equipo_base_id is not None:
            logger.info(f"Obteniendo estadios de equipo base: {equipo_base_id}")
            stmt = (
                select(ORMEquipos)
                .join(ORMEquipos.estadios)
                .where(ORMEstadiosEquipo.equipo_id == equipo_base_id)
                .options(
                    joinedload(ORMEquipos.estadios)
                    .joinedload(ORMEstadiosEquipo.estadio)
                )
            )
            result = await db.execute(stmt)
            estadios = result.scalars().all()
            # error por equipo base no encontrado
            if estadios is None:
                mensaje = f"Estadios pertenecientes a equipo base '{equipo_base_id}' no encontrados"
                logger.warning(mensaje)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=mensaje
                )
            # respuesta satisfactoria
            logger.info(f"Estadios pertenecientes a equipo base con ID: '{equipo_base_id}' encontrados")
            return {"data": estadios}
        # búsqueda general si no se han especificado ningún parámetro
        logger.info("Obteniendo todos los estadios")
        result = await db.execute(select(ORMEstadios))
        estadios = result.scalars().all()
        # mensaje para búsqueda insatisfactoria
        if not estadios:
            mensaje = "No hay estadios creados"
            logger.warning(mensaje)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=mensaje
            )
        logger.info("Todos los estadios obtenidos")
        return {"data": estadios}
    # error si se incumple una restricción en la base de datos
    except IntegrityError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"Uno de los datos introducidos ya existe {str(error)}",
        )
    # error si un atributo no cumple con el tipo de dato requerido
    except SQLAlchemyError as error:
        logger.exception(f"Error en la base de datos {str(error)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Uno de los datos introducidos es inválido {str(error)}",
        )
    # error si hay un problema en la solicitud
    except HTTPException as http_exc:
        # error en la solicitud
        logger.exception("Error HTTP: %s", str(http_exc))
        await db.rollback()
        raise http_exc
    # error genérico
    except Exception as error:
        logger.exception("Error: %s", str(error))
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Servicio inaccesible temporalmente")
