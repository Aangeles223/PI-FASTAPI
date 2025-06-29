from fastapi import FastAPI
app = FastAPI()

app = FastAPI(
    title="Lana App Store API",
    description="""
📱 **Lana App Store API**

Bienvenido a la API oficial de Lana App, una plataforma tipo Play Store donde los usuarios pueden:

🔹 Explorar aplicaciones  
🔹 Descargar e instalar apps  
🔹 Valorar y comentar sus experiencias  
🔹 Ver el historial de versiones  
🔹 Recibir notificaciones importantes

Además, los desarrolladores pueden gestionar sus propias apps y lanzamientos.

Esta API es el backend central para la app móvil, conectada con una base de datos MySQL.
""",
)

# Importa las rutas de los módulos

#USUARIOS
from routers import usuarios
app.include_router(usuarios.router, tags=["Usuarios"])

#STATUS
from routers import status
app.include_router(status.routerStatus)

#SECCIONES
from routers import seccion
app.include_router(seccion.router, prefix="/secciones", tags=["Secciones"])

#CATEGORÍAS
from routers import categorias
app.include_router(categorias.router, prefix="/categorias", tags=["Categorías"])

#DESARROLLADORES
from routers import desarrollador
app.include_router(desarrollador.router, prefix="/desarrolladores", tags=["Desarrolladores"])

#APLICACIONES
from routers import aplicacion
app.include_router(aplicacion.router, prefix="/app", tags=["App"])

#APLICACIONES CATEGORÍAS
from routers import aplicacion_categorias
app.include_router(aplicacion_categorias.router, prefix="/app-categorias", tags=["App-Categorías"])

#APLICACIONES SECCIÓN
from routers import app_seccion
app.include_router(app_seccion.router, prefix="/app-seccion", tags=["App-Sección"])

#APLICACIONES DESARROLLADOR
from routers import apps_desarrollador
app.include_router(apps_desarrollador.router, prefix="/apps-desarrollador", tags=["Apps-Desarrollador"])

#APLICACIONES DESCARGAS
from routers import descargas
app.include_router(descargas.router, prefix="/api", tags=["Descarga"])

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
from routers import version_app  # asegúrate de tener __init__.py en routers
app.include_router(version_app.router, prefix="/api", tags=["Version App"])

