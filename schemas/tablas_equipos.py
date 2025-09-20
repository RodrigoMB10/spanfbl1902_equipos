# spanfbl1902@2025

"""
Módulo para definir las tablas de los equipos
"""

# módulo para crear una clase base
from pydantic import BaseModel
# módulo para definir los atributis opcionales
from typing import Optional, List

class IndiceEquipos(BaseModel):
    """
    Clase para crear la tabla índice equipos
    """
    fundacion = int


class Equipos(BaseModel):
    """
    Clase para definir los equipos
    """
    equipos_base_id: int
    denominacion_equipo_id: int
    logotipo_equipo_id: int
    estadio_id: Optional[int] = None
    direcction_id: Optional[int] = None
    temporada_id: int

    class Config:
        orm_mode = True

class Denominaciones(BaseModel):
    """
    Clase para definir las denominaciones
    """
    denominacion: str

    class Config:
        orm_mode = True


class Logotipos(BaseModel):
    """
    Clase parar definir los logotipos
    """
    logotipo: str


class Direcciones(BaseModel):
    """
    Clase para definir las direcciones
    """
    direccion: str
    comunidad_autonoma_id: int
    provincia_id: int
    localidad: str


class Estadios(BaseModel):
    """
    Clase para definir los estadios
    """
    inauguracion: int
    nombre_estadio: str
    capacidad: Optional[int] = None
    comunidad_autonoma_id: int
    provincia_id: int
    localidad: str


class CompeticionesEquipo(BaseModel):
    """
    Clase para crear la tabla de unión
    muchas competiciones para un equipo durante una temporada
    """
    competicion = int
    temporada = int
    equipo = int


class DenominacionesEquipo(BaseModel):
    """
    Clase para crear la tabla de unión
    muchas denominaciones para un equipo
    """
    equipo = int
    denominacion = int

    class Config:
        orm_mode = True


class LogotiposEquipo(BaseModel):
    """
    Clase para crear la tabla de unión
    muchos logotipos para un equipo
    """
    equipo = int
    logotipo = int


class DireccionesEquipo(BaseModel):
    """
    Clase para crear la tabla de unión
    muchas direcciones para un equipo
    """
    equipo_id = int
    direccion_id = int


class EstadiosEquipo(BaseModel):
    """
    Clase para crear la tabla de unión
    muchos estadios para un equipo
    """
    equipo_id = int
    estadio_id = int

class EditarIndiceEquipos(BaseModel):
    """
    Clase para editar los equipos base
    """
    fundacion: int

    model_config = {
        "from_attributes": True
    }

class EditarEquipos(BaseModel):
    """
    Clase para editar los equipos
    """
    equipos_base_id: Optional[int] = None
    denominacion_equipo_id: Optional[int] = None
    logotipo_equipo_id: Optional[int] = None
    estadio_id: Optional[int] = None
    direcction_id: Optional[int] = None
    temporada_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }

class EditarDenominaciones(BaseModel):
    """
    Clase para editar las denominaciones
    """
    denominacion: str

    model_config = {
        "from_attributes": True
    }


class EditarLogotipos(BaseModel):
    """
    Clase parar editar los logotipos
    """
    logotipo: str

    model_config = {
        "from_attributes": True
    }


class EditarDirecciones(BaseModel):
    """
    Clase para editar las direcciones
    """
    direccion: Optional[str] = None
    comunidad_autonoma_id: Optional[int] = None
    provincia_id: Optional[int] = None
    localidad: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class EditarEstadios(BaseModel):
    """
    Clase para editar los estadios
    """
    inauguracion: Optional[int] = None
    nombre_estadio: Optional[str] = None
    capacidad: Optional[int] = None
    comunidad_autonoma_id: Optional[int] = None
    provincia_id: Optional[int] = None
    localidad: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class EditarCompeticionesEquipo(BaseModel):
    """
    Clase para editar la tabla de unión
    muchas competiciones para un equipo durante una temporada
    """
    competicion_id: Optional[int] = None
    temporada_id: Optional[int] = None
    equipo_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


class EditarDenominacionesEquipo(BaseModel):
    """
    Clase para editar la tabla de unión
    muchas denominaciones para un equipo
    """
    equipo_id: Optional[int] = None
    denominacion_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


class EditarLogotiposEquipo(BaseModel):
    """
    Clase para editar la tabla de unión
    muchos logotipos para un equipo
    """
    equipo_id: Optional[int] = None
    logotipo_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


class EditarDireccionesEquipo(BaseModel):
    """
    Clase para editar la tabla de unión
    muchas direcciones para un equipo
    """
    equipo_id: Optional[int] = None
    direccion_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


class EditarEstadiosEquipo(BaseModel):
    """
    Clase para editar la tabla de unión
    muchos estadios para un equipo
    """
    equipo_id: Optional[int] = None
    estadio_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }