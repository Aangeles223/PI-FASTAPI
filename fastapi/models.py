from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Text, DateTime, SmallInteger, BigInteger, Date, Boolean
from conexion import Base
from sqlalchemy.dialects.mysql import BIGINT 
from datetime import datetime


#USUARIOS
class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(45), nullable=False)
    avatar = Column(LargeBinary, nullable=False)
    correo = Column(String(60), nullable=False, unique=True)
    contraseña = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    telefono = Column(String(20), nullable=True)
    pais_id = Column(Integer, ForeignKey("paises.id"), nullable=True)
    direccion = Column(String(100), nullable=True)
    genero_id = Column(Integer, ForeignKey("generos.id"), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
#USUARIOS


#STATUS
#STATUS
class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)
#STATUS

#SECCIONES
class Seccion(Base):
    __tablename__ = "seccion"
    id_seccion = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.now)
#SECCIONES

#CATEGORIAS
class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now)
#CATEGORIAS

# DESARROLLADORES
class Desarrollador(Base):
    __tablename__ = "desarrollador"
    id_desarrollador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    sitio_web = Column(String(255))
    fecha_registro = Column(DateTime, default=datetime.now)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
# DESARROLLADORES

# APPS
class App(Base):
    __tablename__ = "app"
    id_app = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    precio = Column(String(10), nullable=False)
    id_desarrollador = Column(Integer, ForeignKey("desarrollador.id_desarrollador"), nullable=False)
    descripcion = Column(Text, nullable=False)
    img1 = Column(LargeBinary, nullable=True)
    img2 = Column(LargeBinary, nullable=True)
    img3l = Column(LargeBinary, nullable=True)
    icono = Column(LargeBinary, nullable=True)
    rango_edad = Column(String(45), nullable=False)
    peso = Column(String(45), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    is_free = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    is_on_sale = Column(Boolean, default=False)
    is_multiplayer = Column(Boolean, default=False)
    is_offline = Column(Boolean, default=False)
# APPS

# 🌍 Países
class Pais(Base):
    __tablename__ = "paises"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

# 🚻 Géneros
class Genero(Base):
    __tablename__ = "generos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)


# APPS CATEGORÍAS
class AppCategoria(Base):
    __tablename__ = "app_categorias"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id_app = Column(Integer, ForeignKey("app.id_app"), nullable=False)
    categorias_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

class AppSeccion(Base):
    __tablename__ = "app_seccion"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_app = Column(Integer, ForeignKey("app.id_app"), nullable=False)
    id_seccion = Column(Integer, ForeignKey("seccion.id_seccion"), nullable=False)
    prioridad = Column(Integer, default=0)
# APPS SECCIÓN


# APPS DESARROLLADOR
class AppsDesarrollador(Base):
    __tablename__ = "apps_desarrollador"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    desarrollador_id_desarrollador = Column(Integer, ForeignKey("desarrollador.id_desarrollador"), nullable=False)
    app_id_app = Column(Integer, ForeignKey("app.id_app"), nullable=False)
# APPS DESARROLLADOR


# APLICACIONES DESCARGAS
class Descarga(Base):
    __tablename__ = "descarga"
    id_descarga = Column(Integer, primary_key=True, autoincrement=True)
    id_app = Column(Integer, ForeignKey("app.id_app"))
    fecha = Column(Date)
    cantidad = Column(BIGINT(unsigned=True))  
# APLICACIONES DESCARGAS


# MIS APPS
class MisApp(Base):
    __tablename__ = "mis_apps"
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id_app = Column(Integer, ForeignKey("app.id_app"))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
# MIS APPS

# NOTIFICACIONES
class Notificacion(Base):
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
    status_id = Column(Integer, ForeignKey("status.id"))
# NOTIFICACIONES


# VALORACIONES
class Valoracion(Base):
    __tablename__ = "valoracion"
    id_valoracion = Column(Integer, primary_key=True, autoincrement=True)
    id_app = Column(Integer, ForeignKey("app.id_app"))
    puntuacion = Column(SmallInteger, nullable=False)  # Para tinyint unsigned
    comentario = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuario.id"))
# VALORACIONES


# VERSIONES DE APPS
class VersionApp(Base):
    __tablename__ = "version_app"
    id_version = Column(Integer, primary_key=True, autoincrement=True)
    id_app = Column(Integer, ForeignKey("app.id_app"))
    numero_version = Column(String(20))
    fecha_lanzamiento = Column(Date)
    enlace_apk = Column(String(255))
# VERSIONES DE APPS