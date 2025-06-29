from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contraseña: str
    status_id: int = 1  # 👈 valor por defecto
    avatar: bytes = b""

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: str
    fecha_creacion: datetime
    status_id: int

    class Config:
        from_attributes = True



class StatusPydantic(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


class SeccionCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class SeccionOut(BaseModel):
    id_seccion: int
    nombre: str
    descripcion: Optional[str] = None
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class CategoriaCreate(BaseModel):
    nombre: str

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class DesarrolladorCreate(BaseModel):
    nombre: str
    email: EmailStr
    sitio_web: Optional[str] = None
    status_id: int

class DesarrolladorOut(BaseModel):
    id_desarrollador: int
    nombre: str
    email: EmailStr
    sitio_web: Optional[str] = None
    fecha_registro: datetime
    status_id: int

    class Config:
        from_attributes = True


class AppCreate(BaseModel):
    nombre: str
    precio: str
    id_desarrollador: int
    descripcion: str
    img1: Optional[bytes] = None
    img2: Optional[bytes] = None
    img3l: Optional[bytes] = None
    icono: Optional[bytes] = None
    rango_edad: str
    peso: str
    status_id: int

class AppOut(BaseModel):
    id_app: int
    nombre: str
    precio: str
    id_desarrollador: int
    descripcion: str
    img1: Optional[bytes] = None
    img2: Optional[bytes] = None
    img3l: Optional[bytes] = None
    icono: Optional[bytes] = None
    rango_edad: str
    peso: str
    fecha_creacion: datetime
    status_id: int

    class Config:
        from_attributes = True