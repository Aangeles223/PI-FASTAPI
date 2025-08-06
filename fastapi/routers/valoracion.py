from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from models import Valoracion
from schemas import ValoracionOut
from datetime import datetime
from conexion import get_db
from typing import Optional

router = APIRouter()

@router.post("/valoraciones", response_model=ValoracionOut)
def crear_valoracion(
    id_app: int = Query(..., description="ID de la aplicación a valorar"),
    puntuacion: int = Query(..., ge=1, le=5, description="Puntuación de 1 a 5 estrellas"),
    comentario: Optional[str] = Query(None, max_length=500, description="Comentario opcional"),  # ← Cambiar a Optional[str]
    usuario_id: int = Query(..., description="ID del usuario"),
    db: Session = Depends(get_db)
):
    existe = db.query(Valoracion).filter(
        Valoracion.id_app == id_app,
        Valoracion.usuario_id == usuario_id
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya has valorado esta aplicación")
    
    nueva = Valoracion(
        id_app=id_app,
        puntuacion=puntuacion,
        comentario=comentario,
        fecha=datetime.utcnow(),
        usuario_id=usuario_id
    )
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@router.get("/valoraciones", response_model=list[ValoracionOut])
def obtener_valoraciones(
    db: Session = Depends(get_db)
):
    return db.query(Valoracion).all()

@router.put("/valoraciones/{id_valoracion}", response_model=ValoracionOut)
def actualizar_valoracion(
    id_valoracion: int = Path(..., description="ID de la valoración a actualizar"),
    id_app: int = Query(..., description="Nuevo ID de aplicación"),
    puntuacion: int = Query(..., ge=1, le=5, description="Nueva puntuación"),
    comentario: Optional[str] = Query(None, max_length=500, description="Nuevo comentario"),
    usuario_id: int = Query(..., description="Nuevo ID de usuario"),
    db: Session = Depends(get_db)
):
    valoracion_db = db.query(Valoracion).filter(Valoracion.id_valoracion == id_valoracion).first()
    if not valoracion_db:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")

    # Removed authentication checks

    valoracion_db.id_app = id_app
    valoracion_db.puntuacion = puntuacion
    valoracion_db.comentario = comentario
    valoracion_db.fecha = datetime.utcnow()
    valoracion_db.usuario_id = usuario_id
    db.commit(); db.refresh(valoracion_db)
    return valoracion_db

@router.delete("/valoraciones/{id_valoracion}")
def eliminar_valoracion(
    id_valoracion: int = Path(..., description="ID de la valoración a eliminar"),
    db: Session = Depends(get_db)
):
    valoracion = db.query(Valoracion).filter(Valoracion.id_valoracion == id_valoracion).first()
    if not valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    
    # Removed authentication check
    
    db.delete(valoracion); db.commit()
    return {"mensaje": "Valoración eliminada correctamente"}
