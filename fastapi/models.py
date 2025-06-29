from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Text, DateTime
from conexion import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(45), nullable=False)
    avatar = Column(LargeBinary, nullable=False)
    correo = Column(String(60), nullable=False, unique=True)
    contraseña = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)

class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)

class Seccion(Base):
    __tablename__ = "seccion"
    id_seccion = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.now)


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(45), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now)


class Desarrollador(Base):
    __tablename__ = "desarrollador"
    id_desarrollador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    sitio_web = Column(String(255))
    fecha_registro = Column(DateTime, default=datetime.now)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)


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