from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import Seccion
from schemas import SeccionOut
from datetime import datetime
from typing import Optional

router = APIRouter()

@router.get("/", response_model=list[SeccionOut])
def obtener_secciones(db: Session = Depends(get_db)):
    return db.query(Seccion).all()

@router.get("/{id_seccion}", response_model=SeccionOut)
def obtener_seccion(id_seccion: int, db: Session = Depends(get_db)):
    seccion = db.query(Seccion).filter(Seccion.id_seccion == id_seccion).first()
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return seccion

@router.post("/", response_model=SeccionOut)
def crear_seccion(
    nombre: str = Query(..., min_length=2, max_length=100, description="Nombre de la sección"),
    descripcion: Optional[str] = Query(None, max_length=500, description="Descripción opcional"),
    db: Session = Depends(get_db)
):
    nueva = Seccion(nombre=nombre, descripcion=descripcion, fecha_creacion=datetime.now())
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@router.put("/{id_seccion}", response_model=SeccionOut)
def actualizar_seccion(
    id_seccion: int = Path(..., description="ID de la sección a actualizar"),
    nombre: str = Query(..., min_length=2, max_length=100, description="Nuevo nombre"),
    descripcion: Optional[str] = Query(None, max_length=500, description="Nueva descripción"),
    db: Session = Depends(get_db)
):
    seccion = db.query(Seccion).filter(Seccion.id_seccion == id_seccion).first()
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    seccion.nombre = nombre
    seccion.descripcion = descripcion
    db.commit(); db.refresh(seccion)
    return seccion

@router.delete("/{id_seccion}")
def eliminar_seccion(
    id_seccion: int = Path(..., description="ID de la sección a eliminar"),
    db: Session = Depends(get_db)
):
    seccion = db.query(Seccion).filter(Seccion.id_seccion == id_seccion).first()
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    db.delete(seccion); db.commit()
    return {"mensaje": "Sección eliminada correctamente"}