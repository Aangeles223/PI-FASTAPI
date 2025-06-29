from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Valoracion
from schemas import ValoracionCreate, ValoracionOut
from datetime import datetime
from conexion import get_db

router = APIRouter()

@router.post("/valoraciones", response_model=ValoracionOut)
def crear_valoracion(valoracion: ValoracionCreate, db: Session = Depends(get_db)):
    nueva = Valoracion(
        id_app=valoracion.id_app,
        puntuacion=valoracion.puntuacion,
        comentario=valoracion.comentario,
        fecha=valoracion.fecha or datetime.utcnow(),
        usuario_id=valoracion.usuario_id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/valoraciones", response_model=list[ValoracionOut])
def obtener_valoraciones(db: Session = Depends(get_db)):
    return db.query(Valoracion).all()

@router.put("/valoraciones/{id_valoracion}", response_model=ValoracionOut)
def actualizar_valoracion(id_valoracion: int, datos: ValoracionCreate, db: Session = Depends(get_db)):
    valoracion_db = db.query(Valoracion).filter_by(id_valoracion=id_valoracion).first()
    if not valoracion_db:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")

    valoracion_db.id_app = datos.id_app
    valoracion_db.puntuacion = datos.puntuacion
    valoracion_db.comentario = datos.comentario
    valoracion_db.fecha = datos.fecha or datetime.utcnow()
    valoracion_db.usuario_id = datos.usuario_id
    db.commit()
    db.refresh(valoracion_db)
    return valoracion_db

@router.delete("/valoraciones/{id_valoracion}")
def eliminar_valoracion(id_valoracion: int, db: Session = Depends(get_db)):
    valoracion = db.query(Valoracion).filter_by(id_valoracion=id_valoracion).first()
    if not valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    db.delete(valoracion)
    db.commit()
    return {"mensaje": "Valoración eliminada correctamente"}
