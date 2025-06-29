from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import App
from schemas import AppCreate, AppOut
from datetime import datetime

router = APIRouter()

# Crear app
@router.post("/apps", response_model=AppOut)
def crear_app(app: AppCreate, db: Session = Depends(get_db)):
    nueva = App(
        nombre=app.nombre,
        precio=app.precio,
        id_desarrollador=app.id_desarrollador,
        descripcion=app.descripcion,
        img1=app.img1,
        img2=app.img2,
        img3l=app.img3l,
        icono=app.icono,
        rango_edad=app.rango_edad,
        peso=app.peso,
        fecha_creacion=datetime.now(),
        status_id=app.status_id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# Obtener todas las apps
@router.get("/apps", response_model=list[AppOut])
def obtener_apps(db: Session = Depends(get_db)):
    return db.query(App).all()

# Actualizar una app por ID
@router.put("/apps/{id_app}", response_model=AppOut)
def actualizar_app(id_app: int, app: AppCreate, db: Session = Depends(get_db)):
    existente = db.query(App).filter(App.id_app == id_app).first()
    if not existente:
        raise HTTPException(status_code=404, detail="App no encontrada")

    existente.nombre = app.nombre
    existente.precio = app.precio
    existente.id_desarrollador = app.id_desarrollador
    existente.descripcion = app.descripcion
    existente.img1 = app.img1
    existente.img2 = app.img2
    existente.img3l = app.img3l
    existente.icono = app.icono
    existente.rango_edad = app.rango_edad
    existente.peso = app.peso
    existente.status_id = app.status_id

    db.commit()
    db.refresh(existente)
    return existente

# Eliminar una app por ID
@router.delete("/apps/{id_app}")
def eliminar_app(id_app: int, db: Session = Depends(get_db)):
    app = db.query(App).filter(App.id_app == id_app).first()
    if not app:
        raise HTTPException(status_code=404, detail="App no encontrada")
    
    db.delete(app)
    db.commit()
    return {"mensaje": "App eliminada correctamente"}
