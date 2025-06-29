from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import Seccion
from schemas import SeccionCreate, SeccionOut
from datetime import datetime

router = APIRouter()

@router.get("/secciones", response_model=list[SeccionOut])
def obtener_secciones(db: Session = Depends(get_db)):
    return db.query(Seccion).all()

@router.get("/secciones/{id_seccion}", response_model=SeccionOut)
def obtener_seccion(id_seccion: int, db: Session = Depends(get_db)):
    seccion = db.query(Seccion).filter(Seccion.id_seccion == id_seccion).first()
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return seccion

@router.post("/secciones", response_model=SeccionOut)
def crear_seccion(seccion: SeccionCreate, db: Session = Depends(get_db)):
    nueva = Seccion(
        nombre=seccion.nombre,
        descripcion=seccion.descripcion,
        fecha_creacion=datetime.now()
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/secciones/{id_seccion}", response_model=SeccionOut)
def actualizar_seccion(id_seccion: int, seccion_update: SeccionCreate, db: Session = Depends(get_db)):
    seccion = db.query(Seccion).filter(Seccion.id_seccion == id_seccion).first()
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    seccion.nombre = seccion_update.nombre
    seccion.descripcion = seccion_update.descripcion
    db.commit()
    db.refresh(seccion)
    return seccion

@router.delete("/secciones/{id_seccion}")
def eliminar_seccion(id_seccion: int, db: Session = Depends(get_db)):
    seccion = db.query(Seccion).filter(Seccion.id_seccion == id_seccion).first()
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    db.delete(seccion)
    db.commit()
    return {"mensaje": "Sección eliminada correctamente"}