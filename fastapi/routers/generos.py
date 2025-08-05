from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import Genero
from schemas import GeneroCreate, GeneroOut

router = APIRouter()

@router.get("/", response_model=list[GeneroOut])
def obtener_generos(db: Session = Depends(get_db)):
    return db.query(Genero).all()

@router.get("/{id}", response_model=GeneroOut)
def obtener_genero(id: int = Path(..., description="ID del género"), db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == id).first()
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    return genero

@router.post("/", response_model=GeneroOut)
def crear_genero(
    nombre: str = Query(..., min_length=1, max_length=50, description="Nombre del género"),
    db: Session = Depends(get_db)
):
    nuevo = Genero(nombre=nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id}", response_model=GeneroOut)
def actualizar_genero(
    id: int = Path(..., description="ID del género a actualizar"),
    nombre: str = Query(..., min_length=1, max_length=50, description="Nuevo nombre"),
    db: Session = Depends(get_db)
):
    genero = db.query(Genero).filter(Genero.id == id).first()
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    genero.nombre = nombre
    db.commit()
    db.refresh(genero)
    return genero

@router.delete("/{id}")
def eliminar_genero(id: int = Path(..., description="ID del género a eliminar"), db: Session = Depends(get_db)):
    genero = db.query(Genero).filter(Genero.id == id).first()
    if not genero:
        raise HTTPException(status_code=404, detail="Género no encontrado")
    db.delete(genero)
    db.commit()
    return {"mensaje": "Género eliminado correctamente"}
