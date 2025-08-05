from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Lana App Store API",
)

# Ajustar CORS y prefix de usuarios
origins = [
    "http://localhost:19006",  # Expo Go
    "http://localhost:8081",   # Metro bundler
    "http://localhost:8000",   # si pruebas en web
]
# Añadir allow_credentials para que headers de autorización pasen correctamente
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

#USUARIOS
from routers import usuarios
app.include_router(
    usuarios.router,
    prefix="/usuarios",
    tags=["Usuarios"]
)

#STATUS
from routers import status
app.include_router(status.router, tags=["Status"])

#SECCIONES
from routers import seccion
app.include_router(seccion.router, prefix="/secciones", tags=["Secciones"])

#CATEGORÍAS
from routers import categorias
app.include_router(categorias.router, prefix="/categorias", tags=["Categorías"])

# PAÍSES
from routers import paises
app.include_router(paises.router, prefix="/paises", tags=["Países"])

# GÉNEROS
from routers import generos
app.include_router(generos.router, prefix="/generos", tags=["Géneros"])

#DESARROLLADORES
from routers import desarrollador
app.include_router(desarrollador.router, prefix="/desarrolladores", tags=["Desarrolladores"])

#APLICACIONES
from routers import aplicacion
app.include_router(aplicacion.router, prefix="/apps", tags=["Apps"])

#APLICACIONES CATEGORÍAS
from routers import aplicacion_categorias, app_seccion
app.include_router(aplicacion_categorias.router, prefix="/api/app-categorias", tags=["App-Categorías"])
app.include_router(app_seccion.router, prefix="/api/app-secciones", tags=["App-Secciones"])

#APLICACIONES DESARROLLADOR
from routers import apps_desarrollador
app.include_router(apps_desarrollador.router, prefix="/apps-desarrollador", tags=["Apps-Desarrollador"])

#APLICACIONES DESCARGAS
from routers import descargas
app.include_router(descargas.router, prefix="/descargas", tags=["Descarga"])

#MIS APPS
from routers import mis_apps
app.include_router(mis_apps.router, prefix="/api", tags=["Mis Apps"])

#NOTIFICACIONES
from routers import notificaciones
app.include_router(notificaciones.router, prefix="/api", tags=["Notificaciones"])

#VALORACIONES
from routers import valoracion
app.include_router(valoracion.router, prefix="/api", tags=["Valoraciones"])

#VERSIÓN
from routers import version_app
app.include_router(version_app.router, prefix="/api", tags=["Versiones"])

# Temporalmente comentados hasta crear los archivos
from routers import busqueda
app.include_router(busqueda.router, prefix="/api", tags=["Búsqueda"])

from routers import estadisticas
app.include_router(estadisticas.router, prefix="/api", tags=["Estadísticas"])

from routers import descubrimiento
app.include_router(descubrimiento.router, prefix="/api", tags=["Descubrimiento"])