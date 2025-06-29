from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional


# ============================
# 🧑‍💻 USUARIOS
# ============================
class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contraseña: str
    status_id: int = 1  # Valor por defecto
    avatar: bytes = b""


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: str
    fecha_creacion: datetime
    status_id: int

    class Config:
        from_attributes = True


# ============================
# 📶 STATUS
# ============================
class StatusPydantic(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


# ============================
# 🧭 SECCIONES
# ============================
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


# ============================
# 🗂️ CATEGORÍAS
# ============================
class CategoriaCreate(BaseModel):
    nombre: str


class CategoriaOut(BaseModel):
    id: int
    nombre: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True


# ============================
# 🧑‍💼 DESARROLLADORES
# ============================
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


# ============================
# 📱 APPS
# ============================
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


# ============================
# 🔗 RELACIÓN APP-CATEGORÍA
# ============================
class AppCategoriaCreate(BaseModel):
    app_id_app: int
    categorias_id: int


# ============================
# 🔗 RELACIÓN APP-SECCIÓN
# ============================
class AppSeccionCreate(BaseModel):
    id_app: int
    id_seccion: int
    prioridad: int


class AppSeccionOut(BaseModel):
    id_app: int
    id_seccion: int
    prioridad: int

    class Config:
        from_attributes = True


# ============================
# 🔗 RELACIÓN APP-DESARROLLADOR
# ============================
class AppsDesarrolladorCreate(BaseModel):
    desarrollador_id_desarrollador: int
    app_id_app: int


# ============================
# 📥 DESCARGAS
# ============================
class DescargaCreate(BaseModel):
    id_app: int
    fecha: Optional[date] = None
    cantidad: int


class DescargaOut(DescargaCreate):
    id_descarga: int

    class Config:
        orm_mode = True


# ============================
# 📲 MIS APPS (guardadas por el usuario)
# ============================
class MisAppCreate(BaseModel):
    app_id_app: int
    usuario_id: int


class MisAppOut(MisAppCreate):
    id: int

    class Config:
        orm_mode = True


# ============================
# 🔔 NOTIFICACIONES
# ============================
class NotificacionCreate(BaseModel):
    descripcion: str
    usuario_id: int
    status_id: int


class NotificacionOut(NotificacionCreate):
    id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True


# ============================
# ⭐ VALORACIONES
# ============================
class ValoracionCreate(BaseModel):
    id_app: int
    puntuacion: int
    comentario: Optional[str] = None
    fecha: Optional[datetime] = None
    usuario_id: int


class ValoracionOut(ValoracionCreate):
    id_valoracion: int

    class Config:
        orm_mode = True


# ============================
# 🧾 VERSIONES DE APPS
# ============================
class VersionAppCreate(BaseModel):
    id_app: int
    numero_version: str
    fecha_lanzamiento: date
    enlace_apk: str


class VersionAppOut(VersionAppCreate):
    id_version: int

    class Config:
        orm_mode = True
