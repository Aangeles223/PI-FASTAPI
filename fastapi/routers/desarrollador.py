from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import Desarrollador
from schemas import DesarrolladorCreate, DesarrolladorOut
from datetime import datetime

router = APIRouter()

@router.get("/desarrolladores", response_model=list[DesarrolladorOut])
def obtener_desarrolladores(db: Session = Depends(get_db)):
    return db.query(Desarrollador).all()

@router.get("/desarrolladores/{id_desarrollador}", response_model=DesarrolladorOut)
def obtener_desarrollador(id_desarrollador: int, db: Session = Depends(get_db)):
    desarrollador = db.query(Desarrollador).filter(Desarrollador.id_desarrollador == id_desarrollador).first()
    if not desarrollador:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")
    return desarrollador

@router.post("/desarrolladores", response_model=DesarrolladorOut)
def crear_desarrollador(desarrollador: DesarrolladorCreate, db: Session = Depends(get_db)):
    nuevo = Desarrollador(
        nombre=desarrollador.nombre,
        email=desarrollador.email,
        sitio_web=desarrollador.sitio_web,
        fecha_registro=datetime.now(),
        status_id=desarrollador.status_id
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/desarrolladores/{id_desarrollador}", response_model=DesarrolladorOut)
def actualizar_desarrollador(id_desarrollador: int, desarrollador_update: DesarrolladorCreate, db: Session = Depends(get_db)):
    desarrollador = db.query(Desarrollador).filter(Desarrollador.id_desarrollador == id_desarrollador).first()
    if not desarrollador:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")
    desarrollador.nombre = desarrollador_update.nombre
    desarrollador.email = desarrollador_update.email
    desarrollador.sitio_web = desarrollador_update.sitio_web
    desarrollador.status_id = desarrollador_update.status_id
    db.commit()
    db.refresh(desarrollador)
    return desarrollador

@router.delete("/desarrolladores/{id_desarrollador}")
def eliminar_desarrollador(id_desarrollador: int, db: Session = Depends(get_db)):
    desarrollador = db.query(Desarrollador).filter(Desarrollador.id_desarrollador == id_desarrollador).first()
    if not desarrollador:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")
    db.delete(desarrollador)
    db.commit()
    return {"mensaje": "Desarrollador eliminado correctamente"}