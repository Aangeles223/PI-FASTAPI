from fastapi import FastAPI
from routers import usuarios
from routers import status, seccion, categorias,desarrollador, app
app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, FastAPI está corriendo!"}

app.include_router(usuarios.router, tags=["Usuarios"])

app.include_router(status.routerStatus)

app.include_router(seccion.router, prefix="/secciones", tags=["Secciones"])

app.include_router(categorias.router, prefix="/categorias", tags=["Categorías"])

app.include_router(desarrollador.router, prefix="/desarrolladores", tags=["Desarrolladores"])

app.include_router(app.router, prefix="/app", tags=["App"])