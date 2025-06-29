from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import Categoria
from schemas import CategoriaCreate, CategoriaOut
from datetime import datetime

router = APIRouter()

@router.get("/categorias", response_model=list[CategoriaOut])
def obtener_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@router.get("/categorias/{id}", response_model=CategoriaOut)
def obtener_categoria(id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/categorias", response_model=CategoriaOut)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    nueva = Categoria(
        nombre=categoria.nombre,
        fecha_creacion=datetime.now()
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/categorias/{id}", response_model=CategoriaOut)
def actualizar_categoria(id: int, categoria_update: CategoriaCreate, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria.nombre = categoria_update.nombre
    db.commit()
    db.refresh(categoria)
    return categoria

@router.delete("/categorias/{id}")
def eliminar_categoria(id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    db.delete(categoria)
    db.commit()
    return {"mensaje": "Categoría eliminada correctamente"}