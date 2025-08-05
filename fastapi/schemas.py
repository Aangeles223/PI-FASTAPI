from pydantic import BaseModel, EmailStr, Field
import base64
from datetime import datetime, date
from typing import Optional


# ============================
# 🧑‍💻 USUARIOS
# ============================
class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=45, description="Nombre completo del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico válido")
    contraseña: str = Field(..., min_length=6, max_length=50, description="Contraseña (mínimo 6 caracteres)")
    status_id: int = Field(default=1, description="1=Activo, 2=Inactivo, 3=Suspendido")
    avatar: bytes = Field(default=b"", description="Imagen de perfil (opcional)")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del usuario (opcional)")
    pais_id: Optional[int] = Field(None, description="ID del país (opcional)")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección del usuario (opcional)")
    genero_id: Optional[int] = Field(None, description="ID del género (opcional)")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento (opcional)")


class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: str
    fecha_creacion: datetime
    status_id: int
    telefono: Optional[str]
    pais_id: Optional[int]
    direccion: Optional[str]
    genero_id: Optional[int]
    fecha_nacimiento: Optional[date]

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=45, description="Nombre completo del usuario")
    correo: Optional[EmailStr] = Field(None, description="Correo electrónico válido")
    contraseña: Optional[str] = Field(None, min_length=6, max_length=50, description="Contraseña (mínimo 6 caracteres)")
    status_id: Optional[int] = Field(None, description="Status ID (1=Activo, 2=Inactivo, 3=Suspendido)")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del usuario (opcional)")
    pais_id: Optional[int] = Field(None, description="ID del país (opcional)")
    direccion: Optional[str] = Field(None, max_length=100, description="Dirección del usuario (opcional)")
    genero_id: Optional[int] = Field(None, description="ID del género (opcional)")
    fecha_nacimiento: Optional[date] = Field(None, description="Fecha de nacimiento (opcional)")

    class Config:
        from_attributes = True


# ============================
# 📶 STATUS
# ============================
class StatusCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=45, description="Nombre del estado")


class StatusOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


# ============================
# 🧭 SECCIONES
# ============================
class SeccionCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la sección")
    descripcion: Optional[str] = Field(None, max_length=500, description="Descripción opcional")


class SeccionOut(BaseModel):
    id_seccion: int
    nombre: str
    descripcion: Optional[str]
    fecha_creacion: datetime

    class Config:
        from_attributes = True


# ============================
# 🗂️ CATEGORÍAS
# ============================
class CategoriaCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=45, description="Nombre de la categoría")


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
    nombre: str = Field(..., min_length=2, max_length=150, description="Nombre o empresa del desarrollador")
    email: EmailStr = Field(..., description="Correo electrónico de contacto")
    sitio_web: Optional[str] = Field(None, max_length=255, description="URL del sitio web (opcional)")
    status_id: int = Field(default=1, description="1=Activo, 2=Inactivo, 3=Suspendido")


class DesarrolladorOut(BaseModel):
    id_desarrollador: int
    nombre: str
    email: str
    sitio_web: Optional[str]
    fecha_registro: datetime
    status_id: int

    class Config:
        from_attributes = True
        
# ============================
# 🌍 PAISES
# ============================
class PaisCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del país")

class PaisOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

# ============================
# 🚻 GENEROS
# ============================
class GeneroCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50, description="Nombre del género")

class GeneroOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True


# ============================
# 📱 APPS (corregir campo inconsistente)
# ============================
class AppCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=150, description="Nombre de la aplicación")
    precio: str = Field(..., description="Precio (usar '0' para gratis)")
    id_desarrollador: int = Field(..., description="ID del desarrollador")  # Cambiar a id_desarrollador
    descripcion: str = Field(..., min_length=10, description="Descripción de la app")
    img1: Optional[bytes] = Field(None, description="Primera imagen (opcional)")
    img2: Optional[bytes] = Field(None, description="Segunda imagen (opcional)")
    img3l: Optional[bytes] = Field(None, description="Tercera imagen (opcional)")  # Mantener img3l como en BD
    icono: Optional[bytes] = Field(None, description="Ícono de la app (opcional)")
    rango_edad: str = Field(..., description="Ej: 3+, 7+, 12+, 17+")
    peso: str = Field(..., description="Tamaño de la app (Ej: 50MB)")
    status_id: int = Field(default=1, description="1=Activo, 2=Inactivo, 3=Suspendido")
    is_free: bool = Field(default=False, description="¿Gratis?")
    is_premium: bool = Field(default=False, description="¿Premium?")
    is_on_sale: bool = Field(default=False, description="¿En oferta?")
    is_multiplayer: bool = Field(default=False, description="¿Multijugador?")
    is_offline: bool = Field(default=False, description="¿Offline?")


class AppOut(BaseModel):
    id_app: int
    nombre: str
    precio: str
    id_desarrollador: int
    descripcion: str
    img1: Optional[bytes]
    img2: Optional[bytes]
    img3l: Optional[bytes]
    icono: Optional[bytes]
    rango_edad: str
    peso: str
    fecha_creacion: datetime
    status_id: int
    is_free: bool = False
    is_premium: bool = False
    is_on_sale: bool = False
    is_multiplayer: bool = False
    is_offline: bool = False

    class Config:
        from_attributes = True
        json_encoders = {bytes: lambda v: base64.b64encode(v).decode('utf-8') if v is not None else None}


# ============================
# 🔗 RELACIÓN APP-CATEGORÍA
# ============================
class AppCategoriaCreate(BaseModel):
    app_id: int = Field(..., description="ID de la aplicación")
    categoria_id: int = Field(..., description="ID de la categoría")


class AppCategoriaOut(BaseModel):
    id: int
    app_id_app: int
    categorias_id: int

    class Config:
        from_attributes = True


# ============================
# 🔗 RELACIÓN APP-SECCIÓN
# ============================
class AppSeccionCreate(BaseModel):
    app_id: int = Field(..., description="ID de la aplicación")
    seccion_id: int = Field(..., description="ID de la sección")
    prioridad: int = Field(default=0, ge=0, le=10, description="Prioridad 0-10")


class AppSeccionOut(BaseModel):
    id: int
    id_app: int
    id_seccion: int
    prioridad: int

    class Config:
        from_attributes = True


# ============================
# 📥 DESCARGAS (corregir campos)
# ============================
class DescargaCreate(BaseModel):
    id_app: int = Field(..., description="ID de la aplicación")  # Cambiar a id_app
    fecha: Optional[date] = Field(None, description="Fecha de descarga (auto si se omite)")
    cantidad: int = Field(default=1, ge=1, description="Número de descargas")


class DescargaOut(BaseModel):
    id_descarga: int
    id_app: int
    fecha: date
    cantidad: int

    class Config:
        from_attributes = True


# ============================
# 📲 MIS APPS (corregir campos)
# ============================
class MisAppCreate(BaseModel):
    app_id_app: int = Field(..., description="ID de la aplicación a guardar")  # Cambiar a app_id_app
    usuario_id: int = Field(..., description="ID del usuario")


class MisAppOut(BaseModel):
    id: int
    app_id_app: int
    usuario_id: int

    class Config:
        from_attributes = True


# ============================
# 🔔 NOTIFICACIONES
# ============================
class NotificacionCreate(BaseModel):
    descripcion: str = Field(..., min_length=5, max_length=100, description="Mensaje de la notificación")
    usuario_id: int = Field(..., description="ID del usuario destinatario")
    status_id: int = Field(default=1, description="1=Activo, 2=Leída")


class NotificacionOut(BaseModel):
    id: int
    descripcion: str
    fecha_creacion: datetime
    usuario_id: int
    status_id: int

    class Config:
        from_attributes = True


# ============================
# ⭐ VALORACIONES (corregir campos)
# ============================
class ValoracionCreate(BaseModel):
    id_app: int = Field(..., description="ID de la aplicación a valorar")  # Cambiar a id_app
    puntuacion: int = Field(..., ge=1, le=5, description="Puntuación de 1 a 5 estrellas")
    comentario: Optional[str] = Field(None, max_length=500, description="Comentario opcional")
    usuario_id: int = Field(..., description="ID del usuario")


class ValoracionOut(BaseModel):
    id_valoracion: int
    id_app: int
    puntuacion: int
    comentario: Optional[str]
    fecha: datetime
    usuario_id: int

    class Config:
        from_attributes = True


# ============================
# 🧾 VERSIONES DE APPS (corregir campos)
# ============================
class VersionAppCreate(BaseModel):
    id_app: int = Field(..., description="ID de la aplicación")  # Cambiar a id_app
    numero_version: str = Field(..., description="Ej: 1.0.0, 2.1.3")
    fecha_lanzamiento: date = Field(..., description="Fecha de lanzamiento")
    enlace_apk: str = Field(..., description="URL del archivo APK")


class VersionAppOut(BaseModel):
    id_version: int
    id_app: int
    numero_version: str
    fecha_lanzamiento: date
    enlace_apk: str

    class Config:
        from_attributes = True


# ============================
# 🛠️ OTRAS RELACIONES Y ACCIONES
# ============================
# APPS DESARROLLADOR
class AppsDesarrolladorCreate(BaseModel):
    desarrollador_id: int = Field(..., description="ID del desarrollador")
    app_id: int = Field(..., description="ID de la aplicación")


class AppsDesarrolladorOut(BaseModel):
    id: int
    desarrollador_id_desarrollador: int
    app_id_app: int

    class Config:
        from_attributes = True


# ============================
# 🔍 BÚSQUEDA
# ============================
class BusquedaRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=100, description="Término de búsqueda")
    categoria_id: Optional[int] = Field(None, description="Filtrar por categoría (opcional)")
    limite: Optional[int] = Field(10, ge=1, le=50, description="Número máximo de resultados")

class BusquedaCompletaRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=100, description="Término de búsqueda")
    categoria_id: Optional[int] = Field(None, description="Filtrar por categoría")
    desarrollador_id: Optional[int] = Field(None, description="Filtrar por desarrollador")
    precio_min: Optional[float] = Field(None, ge=0, description="Precio mínimo")
    precio_max: Optional[float] = Field(None, ge=0, description="Precio máximo")
    rango_edad: Optional[str] = Field(None, description="Filtrar por rango de edad")
    limite: Optional[int] = Field(20, ge=1, le=100, description="Número máximo de resultados")

# ============================
# 📊 ESTADÍSTICAS (para inputs si necesitas)
# ============================
class EstadisticasRequest(BaseModel):
    fecha_inicio: Optional[date] = Field(None, description="Fecha de inicio para filtrar")
    fecha_fin: Optional[date] = Field(None, description="Fecha de fin para filtrar")
    limite: Optional[int] = Field(10, ge=1, le=50, description="Número de resultados")

# ============================
# 🎯 DESCUBRIMIENTO (para inputs si necesitas)
# ============================
class RecomendacionRequest(BaseModel):
    usuario_id: int = Field(..., description="ID del usuario para recomendar")
    limite: Optional[int] = Field(10, ge=1, le=20, description="Número de recomendaciones")
    incluir_instaladas: Optional[bool] = Field(False, description="Incluir apps ya instaladas")
