from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import Desarrollador
from schemas import DesarrolladorOut
from datetime import datetime
from typing import Optional
from pydantic import EmailStr

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
def crear_desarrollador(
    nombre: str = Query(..., min_length=2, max_length=150, description="Nombre del desarrollador"),
    email: EmailStr = Query(..., description="Correo electrónico"),
    sitio_web: Optional[str] = Query(None, max_length=255, description="Sitio web (opcional)"),
    status_id: int = Query(1, description="Status ID"),
    db: Session = Depends(get_db)
):
    nuevo = Desarrollador(
        nombre=nombre, email=email, sitio_web=sitio_web,
        fecha_registro=datetime.now(), status_id=status_id
    )
    db.add(nuevo); db.commit(); db.refresh(nuevo)
    return nuevo

@router.put("/desarrolladores/{id_desarrollador}", response_model=DesarrolladorOut)
def actualizar_desarrollador(
    id_desarrollador: int = Path(..., description="ID del desarrollador"),
    nombre: str = Query(..., min_length=2, max_length=150, description="Nuevo nombre"),
    email: EmailStr = Query(..., description="Nuevo email"),
    sitio_web: Optional[str] = Query(None, max_length=255, description="Nuevo sitio web"),
    status_id: int = Query(..., description="Nuevo status ID"),
    db: Session = Depends(get_db)
):
    desarrollador = db.query(Desarrollador).filter(Desarrollador.id_desarrollador == id_desarrollador).first()
    if not desarrollador:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")
    desarrollador.nombre = nombre
    desarrollador.email = email
    desarrollador.sitio_web = sitio_web
    desarrollador.status_id = status_id
    db.commit(); db.refresh(desarrollador)
    return desarrollador

@router.delete("/desarrolladores/{id_desarrollador}")
def eliminar_desarrollador(
    id_desarrollador: int = Path(..., description="ID del desarrollador a eliminar"),
    db: Session = Depends(get_db)
):
    desarrollador = db.query(Desarrollador).filter(Desarrollador.id_desarrollador == id_desarrollador).first()
    if not desarrollador:
        raise HTTPException(status_code=404, detail="Desarrollador no encontrado")
    db.delete(desarrollador); db.commit()
    return {"mensaje": "Desarrollador eliminado correctamente"}