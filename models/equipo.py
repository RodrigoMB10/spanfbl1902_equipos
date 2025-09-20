# spanfbl1902@2025

"""
Módulo para definir las tablas en la
base de datos
"""

# clase para crear un tipo de datos de clase ENUM
import enum
# módulo para definir las columnas
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Enum as PgEnum
from sqlalchemy.orm import DeclarativeBase, relationship

# declarar objeto base
class Base(DeclarativeBase):
    """
    Clase para declarar la base que se heredará
    en todas las demás clases
    """
    # vacía para definir mypy checks
    pass

# declarar tablas
class ComunidadAutonoma(enum.Enum):
    """
    Clase para definir las comunidades autónomas
    """
    ANDALUCIA = "Andalucia"
    ARAGON = "Aragón"
    ASTURIAS = "Asturias"
    CANTABRIA = "Cantabria"
    CASTILLA_LA_MANCHA = "Castilla La-Mancha"
    CASTILLA_LEON = "Castilla y León"
    CATALUÑA = "Cataluña"
    CEUTA = "Ceuta"
    COMUNIDAD_VALENCIANA = "Comunidad Valenciana"
    EXTREMADURA = "Extremadura"
    GALICIA = "Galicia"
    ISLAS_BALEARES = "Islas Baleares"
    ISLAS_CANARIAS = "Islas Canarias"
    LA_RIOJA = "La Rioja"
    MADRID = "Madrid"
    MELILLA = "Melilla"
    MURCIA = "Murcia"
    NAVARRA = "Navarra"
    PAIS_VASCO = "País Vasco"


class Provincia(enum.Enum):
    """
    Clase para definir las provincias
    """
    ALAVA = "Álava"
    ALBACETE = "Albacete"
    ALICANTE = "Alicante"
    ALMERIA = "Almería"
    ASTURIAS = "Asturias"
    AVILA = "Ávila"
    BADAJOZ = "Badajoz"
    BARCELONA = "Barcelona"
    BURGOS = "Burgos"
    CACERES = "Cáceres"
    CADIZ = "Cádiz"
    CANTABRIA = "Cantabria"
    CASTELLON = "Castellón de la Plana"
    CEUTA = "Ceuta"
    CIUDAD_REAL = "Ciudad Real"
    CORDOBA = "Córdoba"
    CUENCA = "Cuenca"
    GERONA = "Gerona"
    GRAN_CANARIA = "Gran Canaria"
    GRANADA = "Granada"
    GUADALAJARA = "Guadalajara"
    GUIPUZCOA = "Guipúzcoa"
    HUELVA = "Huelva"
    HUESCA = "Huesca"
    JAEN = "Jaén"
    LA_CORUÑA = "La Coruña"
    LERIDA = "Lérida"
    LEON = "Léon"
    LUGO = "Lugo"
    MADRID = "Madrid"
    MALAGA = "Málaga"
    MALLORCA = "Mallorca"
    MELILLA = "Melilla"
    MURCIA = "Murcia"
    NAVARRA = "Navarra"
    ORENSE = "Orense"
    PALENCIA = "Palencia"
    PONTEVEDRA = "Pontevedra"
    SALAMANCA = "Salamanca"
    SEGOVIA = "Segovia"
    SEVILLA = "Sevilla"
    SORIA = "Soria"
    TARRAGONA = "Tarragona"
    TENERIFE = "Tenerife"
    TERUEL = "Teruel"
    TOLEDO = "Toledo"
    VALENCIA = "Valencia"
    VALLADOLID = "Valladolid"
    VIZCAYA = "Vizcaya"
    ZAMORA = "Zamora"
    ZARAGOZA = "Zaragoza"


class Denominaciones(Base):
    """
    Clase para crear la tabla denominaciones
    """
    __tablename__ = "denominaciones"
    denominacion_id = Column(Integer, primary_key=True, index=True)
    denominacion = Column(String(length=100), unique=True, nullable=False)

    equipos = relationship("DenominacionesEquipo", back_populates="denominacio")


class Logotipos(Base):
    """
    Clase para crear la tabla logotipos
    """
    __tablename__ = "logotipos"
    logotipo_id = Column(Integer,primary_key=True, index=True)
    logotipo = Column(String(length=100), unique=True, nullable=False)

    equipos = relationship("LogotiposEquipo", back_populates="logotipo")


class ComunidadesAutonomas(Base):
    """
    Clase para crear la tabla comunidades autonomas
    """
    __tablename__ = "comunidades_autonomas"
    comunidad_autonoma_id = Column(Integer,primary_key=True, index=True)
    comunidad_autonoma= Column(PgEnum(ComunidadAutonoma, name='comunidad_autonoma', create_type=True), unique=False, nullable=False)


class Provincias(Base):
    """
    Clase para crear la tabla provincias
    """
    __tablename__ = "provincias"
    provincia_id = Column(Integer, primary_key=True, index=True)
    provincia = Column(PgEnum(Provincia, name='provincia', create_type=True), unique=False, nullable=False)


class IndiceEquipos(Base):
    """
    Clase para crear la tabla índice equipos
    """
    __tablename__ = "indice_equipos"
    indice_equipo_id = Column(Integer, primary_key=True, index=True)
    fundacion = Column(Integer, unique=False, nullable=False)


class Direcciones(Base):
    """
    Clase para crear la tabla direcciones
    """
    __tablename__ = "direcciones"
    direccion_id = Column(Integer, primary_key=True, index=True)
    direccion = Column(String(length=100), unique=False, nullable=False)
    comunidad_autonoma = Column(Integer, ForeignKey("comunidades_autonomas.comunidad_autonoma_id"), unique=False, nullable=False)
    provincia = Column(Integer, ForeignKey("provincias.provincia_id"), unique=False, nullable=False)
    localidad = Column(String(length=100), unique=False, nullable=False)

    equipos = relationship("DireccionesEquipo", back_populates="direccion")


class Estadios(Base):
    """
    Clase para crear la tabla estadios
    """
    __tablename__ = "estadios"
    estadio_id = Column(Integer, primary_key=True, index=True)
    inauguracion = Column(Integer, unique=False, nullable=False)
    nombre_estadio = Column(String(length=100), unique=True, nullable=False)
    capacidad = Column(Integer, unique=False, nullable=True)
    comunidad_autonoma_id = Column(Integer, ForeignKey("comunidades_autonomas.comunidad_autonoma_id"), unique=False, nullable=False)
    provincia_id = Column(Integer, ForeignKey("provincias.provincia_id"), unique=False, nullable=False)
    localidad = Column(String(length=100), unique=False, nullable=False)

    equipos = relationship("EstadiosEquipo", back_populates="estadio")


class Equipos(Base):
    """
    Clase para crear la tabla equipos
    """
    __tablename__ = "equipos"
    equipo_id = Column(Integer, primary_key=True, index=True)
    equipo_base_id = Column(Integer, ForeignKey("indice_equipos.indice_equipo_id"), unique=False, nullable=False)
    denominacion_equipo_id = Column(Integer, ForeignKey("denominaciones.denominacion_id"), unique=False, nullable=False)
    logotipo_equipo_id = Column(Integer, ForeignKey("logotipos.logotipo_id"), unique=False, nullable=False)
    estadio_id = Column(Integer, ForeignKey("estadios.estadio_id"), unique=False, nullable=True)
    direccion_id = Column(Integer, ForeignKey("direcciones.direccion_id"), unique=False, nullable=True)
    temporada_id = Column(Integer, ForeignKey("temporadas.temporada_id"), unique=False, nullable=False)

    # relaciones con las tablas de unión
    competiciones = relationship("CompeticionesEquipo", back_populates="equipo")
    denominaciones = relationship("DenominacionesEquipo", back_populates="equipo")
    logotipos = relationship("LogotiposEquipo", back_populates="equipo")
    direcciones = relationship("DireccionesEquipo", back_populates="equipo")
    estadios = relationship("EstadiosEquipo", back_populates="equipo")


class Competiciones(Base):
    """
    Clase para crear la tabla competiciones
    """
    __tablename__ = "competiciones"
    competicion_id = Column(Integer, primary_key=True, index=True)
    nombre_competicion = Column(String(length=100), unique=False, nullable=False)
    fundacion = Column(Integer, unique=False, nullable=False)
    logotipo_id = Column(Integer, ForeignKey("logotipos.logotipo_id"), unique=True, nullable=True)
    trofeo_id = Column(Integer, ForeignKey("trofeos.trofeo_id"))

    # relación con la tabla de unión
    equipos = relationship("CompeticionesEquipo", back_populates="competicion")


class Temporadas(Base):
    """
    Clase para crear la tabla temporadas
    """
    __tablename__ = "temporadas"
    temporada_id = Column(Integer, primary_key=True, index=True)
    competicion_id = Column(Integer, ForeignKey("competiciones.competicion_id"), unique=False, nullable=False)
    fecha_inicio = Column(Date, unique=False, nullable=False)
    fecha_final = Column(Date, unique=False, nullable=False)
    contiene_grupos = Column(Boolean, unique=False, nullable=False)
    numero_grupos = Column(Integer, unique=False, nullable=True)


class DenominacionesEquipo(Base):
    """
    Clase para crear la tabla de unión
    muchas denominaciones para un equipo
    """
    __tablename__ = "denominaciones_equipo"
    denominaciones_equipo_id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("indice_equipos.indice_equipo_id"), unique=False, nullable=False)
    denominacion_id = Column(Integer, ForeignKey("denominaciones.denominacion_id"), unique=True, nullable=False)

    equipo = relationship("Equipos", back_populates="denominaciones")
    denominacion = relationship("Denominaciones", back_populates="equipos")


class LogotiposEquipo(Base):
    """
    Clase para crear la tabla de unión
    muchos logotipos para un equipo
    """
    __tablename__ = "logotipos_equipo"
    logotipos_equipo_id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("indice_equipos.indice_equipo_id"), unique=False, nullable=False)
    logotipo_id = Column(Integer, ForeignKey("logotipos.logotipo_id"), unique=True, nullable=False)

    equipos = relationship("Equipos", back_populates="logotipos")
    logotipo = relationship("Logotipos", back_populates="equipos")


class DireccionesEquipo(Base):
    """
    Clase para crear la tabla de unión
    muchas direcciones para un equipo
    """
    __tablename__ = "direcciones_equipo"
    direcciones_equipo_id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("indice_equipos.indice_equipo_id"), unique=False, nullable=False)
    direccion_id = Column(Integer, ForeignKey("direcciones.direccion_id"), unique=True, nullable=False)

    equipos = relationship("Equipos", back_populates="direcciones")
    direccion = relationship("Direcciones", back_populates="equipos")


class EstadiosEquipo(Base):
    """
    Clase para crear la tabla de unión
    muchos estadios para un equipo
    """
    __tablename__ = "estadios_equipo"
    estadios_equipo_id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("indice_equipos.indice_equipo_id"), unique=False, nullable=False)
    estadio_id = Column(Integer, ForeignKey("estadios.estadio_id"), unique=True, nullable=False)

    equipo = relationship("Equipos", back_populates="estadios")
    estadio = relationship("Estadios", back_populates="equipos")


class CompeticionesEquipo(Base):
    """
    Clase para crear la tabla de unión
    muchas competiciones para un equipo durante una temporada
    """
    __tablename__ = "competiciones_equipo"
    competiciones_equipo_id = Column(Integer, primary_key=True, index=True)
    competicion_id = Column(Integer, ForeignKey("competiciones.competicion_id"), unique=False, nullable=False)
    temporada_id = Column(Integer, ForeignKey("temporadas.temporada_id"), unique=False, nullable=False)
    equipo_id = Column(Integer, ForeignKey("equipos.equipo_id"), unique=False, nullable=False)

    # relación con las tablas
    equipo = relationship("Equipos", back_populates="competiciones")
    competicion = relationship("Competiciones", back_populates="equipos")