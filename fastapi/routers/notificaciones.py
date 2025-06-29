from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from models import Notificacion
from schemas import NotificacionCreate, NotificacionOut
from conexion import get_db

router = APIRouter()

@router.post("/notificaciones", response_model=NotificacionOut)
def crear_notificacion(noti: NotificacionCreate, db: Session = Depends(get_db)):
    nueva = Notificacion(
        descripcion=noti.descripcion,
        usuario_id=noti.usuario_id,
        status_id=noti.status_id,
        fecha_creacion=datetime.utcnow()
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/notificaciones", response_model=list[NotificacionOut])
def obtener_notificaciones(db: Session = Depends(get_db)):
    return db.query(Notificacion).all()

@router.put("/notificaciones/{id}", response_model=NotificacionOut)
def actualizar_notificacion(id: int, noti: NotificacionCreate, db: Session = Depends(get_db)):
    notificacion = db.query(Notificacion).filter_by(id=id).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    notificacion.descripcion = noti.descripcion
    notificacion.usuario_id = noti.usuario_id
    notificacion.status_id = noti.status_id
    db.commit()
    db.refresh(notificacion)
    return notificacion

@router.delete("/notificaciones/{id}")
def eliminar_notificacion(id: int, db: Session = Depends(get_db)):
    noti = db.query(Notificacion).filter_by(id=id).first()
    if not noti:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    db.delete(noti)
    db.commit()
    return {"mensaje": "Notificación eliminada correctamente"}
