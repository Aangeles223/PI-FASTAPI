from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import Categoria
from schemas import CategoriaOut
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=list[CategoriaOut])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@router.get("/{id}", response_model=CategoriaOut)
def obtener_categoria(id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/", response_model=CategoriaOut)
def crear_categoria(
    nombre: str = Query(..., min_length=2, max_length=45, description="Nombre de la categoría"),
    db: Session = Depends(get_db)
):
    nueva = Categoria(nombre=nombre, fecha_creacion=datetime.now())
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@router.put("/{id}", response_model=CategoriaOut)
def actualizar_categoria(
    id: int = Path(..., description="ID de la categoría a actualizar"),
    nombre: str = Query(..., min_length=2, max_length=45, description="Nuevo nombre"),
    db: Session = Depends(get_db)
):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria.nombre = nombre
    db.commit(); db.refresh(categoria)
    return categoria

@router.delete("/{id}")
def eliminar_categoria(
    id: int = Path(..., description="ID de la categoría a eliminar"),
    db: Session = Depends(get_db)
):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria); db.commit()
    return {"mensaje": "Categoría eliminada correctamente"}