from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import AppCategoria
from schemas import AppCategoriaCreate

router = APIRouter()

# POST - Crear relación
@router.post("/app-categorias")
def asociar_app_categoria(relacion: AppCategoriaCreate, db: Session = Depends(get_db)):
    existe = db.query(AppCategoria).filter_by(
        app_id_app=relacion.app_id_app,
        categorias_id=relacion.categorias_id
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="La relación ya existe")
    nueva = AppCategoria(**relacion.dict())
    db.add(nueva)
    db.commit()
    return {"mensaje": "Relación creada correctamente"}

# DELETE - Eliminar relación
@router.delete("/app-categorias")
def desasociar_app_categoria(relacion: AppCategoriaCreate, db: Session = Depends(get_db)):
    existe = db.query(AppCategoria).filter_by(
        app_id_app=relacion.app_id_app,
        categorias_id=relacion.categorias_id
    ).first()
    if not existe:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    db.delete(existe)
    db.commit()
    return {"mensaje": "Relación eliminada correctamente"}

# GET - Obtener todas las relaciones
@router.get("/app-categorias")
def obtener_relaciones(db: Session = Depends(get_db)):
    relaciones = db.query(AppCategoria).all()
    return relaciones

# PUT - Actualizar relación (ej: cambiar categoría asociada a una app)
@router.put("/app-categorias")
def actualizar_relacion_app_categoria(
    original: AppCategoriaCreate,
    nueva: AppCategoriaCreate,
    db: Session = Depends(get_db)
):
    relacion = db.query(AppCategoria).filter_by(
        app_id_app=original.app_id_app,
        categorias_id=original.categorias_id
    ).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación original no encontrada")

    # Eliminar relación vieja
    db.delete(relacion)
    db.commit()

    # Insertar nueva relación
    nueva_relacion = AppCategoria(**nueva.dict())
    db.add(nueva_relacion)
    db.commit()
    return {"mensaje": "Relación actualizada correctamente"}
