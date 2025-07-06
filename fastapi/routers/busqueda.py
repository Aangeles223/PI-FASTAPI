from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from models import App, Categoria, AppCategoria
from schemas import AppOut
from conexion import get_db
from typing import Optional

router = APIRouter()

@router.get("/buscar", response_model=list[AppOut])
def buscar_apps(
    q: str = Query(..., min_length=1, max_length=100, description="Buscar por nombre o descripción (ej: 'mine' encuentra 'Minecraft')"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría ID (opcional)"),
    limite: int = Query(10, ge=1, le=50, description="Máximo resultados"),
    db: Session = Depends(get_db)
):
 
    # Búsqueda flexible con LIKE para coincidencias parciales
    consulta = db.query(App).filter(
        or_(
            App.nombre.ilike(f"%{q}%"),           # "mine" encuentra "Minecraft"
            App.descripcion.ilike(f"%{q}%")       # "juego" encuentra "juego de aventuras"
        )
    )
    
    # Filtrar por categoría si se especifica
    if categoria_id:
        consulta = consulta.join(AppCategoria).filter(
            AppCategoria.categorias_id == categoria_id
        )
    
    # Filtrar solo apps activas
    consulta = consulta.filter(App.status_id == 1)
    
    return consulta.limit(limite).all()

@router.get("/buscar-completa", response_model=list[AppOut])
def buscar_completa(
    q: str = Query(..., min_length=1, description="Búsqueda de texto"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    desarrollador_id: Optional[int] = Query(None, description="Filtrar por desarrollador"),
    gratis: Optional[bool] = Query(None, description="Solo apps gratis (true) o de pago (false)"),
    rango_edad: Optional[str] = Query(None, description="Ej: 3+, 7+, 12+, 17+"),
    limite: int = Query(20, ge=1, le=100, description="Máximo resultados"),
    db: Session = Depends(get_db)
):
   
    # Búsqueda base por texto
    consulta = db.query(App).filter(
        or_(
            App.nombre.ilike(f"%{q}%"),
            App.descripcion.ilike(f"%{q}%")
        )
    )
    
    # Filtros adicionales
    if categoria_id:
        consulta = consulta.join(AppCategoria).filter(
            AppCategoria.categorias_id == categoria_id
        )
    
    if desarrollador_id:
        consulta = consulta.filter(App.id_desarrollador == desarrollador_id)
    
    if gratis is not None:
        if gratis:
            consulta = consulta.filter(App.precio == "0")  # Apps gratis
        else:
            consulta = consulta.filter(App.precio != "0")  # Apps de pago
    
    if rango_edad:
        consulta = consulta.filter(App.rango_edad == rango_edad)
    
    # Solo apps activas
    consulta = consulta.filter(App.status_id == 1)
    
    # Ordenar por relevancia: primero coincidencias exactas en nombre
    consulta = consulta.order_by(
        App.nombre.ilike(f"{q}%").desc(),  # Priorizar nombres que empiecen con la búsqueda
        App.nombre.asc()                   # Luego orden alfabético
    )
    
    return consulta.limit(limite).all()


