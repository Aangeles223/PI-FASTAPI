from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import Pais
from schemas import PaisCreate, PaisOut

router = APIRouter()

@router.get("/", response_model=list[PaisOut])
def obtener_paises(db: Session = Depends(get_db)):
    return db.query(Pais).all()

@router.get("/{id}", response_model=PaisOut)
def obtener_pais(id: int = Path(..., description="ID del país"), db: Session = Depends(get_db)):
    pais = db.query(Pais).filter(Pais.id == id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return pais

@router.post("/", response_model=PaisOut)
def crear_pais(
    nombre: str = Query(..., min_length=1, max_length=100, description="Nombre del país"),
    db: Session = Depends(get_db)
):
    nuevo = Pais(nombre=nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{id}", response_model=PaisOut)
def actualizar_pais(
    id: int = Path(..., description="ID del país a actualizar"),
    nombre: str = Query(..., min_length=1, max_length=100, description="Nuevo nombre"),
    db: Session = Depends(get_db)
):
    pais = db.query(Pais).filter(Pais.id == id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    pais.nombre = nombre
    db.commit()
    db.refresh(pais)
    return pais

@router.delete("/{id}")
def eliminar_pais(id: int = Path(..., description="ID del país a eliminar"), db: Session = Depends(get_db)):
    pais = db.query(Pais).filter(Pais.id == id).first()
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    db.delete(pais)
    db.commit()
    return {"mensaje": "País eliminado correctamente"}
