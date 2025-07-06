from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Notificacion, Usuario
from schemas import NotificacionCreate, NotificacionOut
from datetime import datetime
from conexion import get_db
from .usuarios import obtener_usuario_actual

router = APIRouter()

@router.post("/notificaciones", response_model=NotificacionOut)
def crear_notificacion(
    notificacion: NotificacionCreate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    if notificacion.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No autorizado para crear notificaciones para otro usuario")
    
    nueva = Notificacion(
        descripcion=notificacion.descripcion,
        fecha_creacion=datetime.utcnow(),
        usuario_id=notificacion.usuario_id,
        status_id=notificacion.status_id
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/notificaciones", response_model=list[NotificacionOut])
def obtener_notificaciones(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    return db.query(Notificacion).filter(Notificacion.usuario_id == usuario_actual.id).all()

@router.put("/notificaciones/{id}", response_model=NotificacionOut)
def actualizar_notificacion(
    id: int, 
    datos: NotificacionCreate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    notificacion_db = db.query(Notificacion).filter(Notificacion.id == id).first()
    if not notificacion_db:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")

    if notificacion_db.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No autorizado para modificar esta notificación")
    
    if datos.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No autorizado para asignar notificaciones a otro usuario")

    notificacion_db.descripcion = datos.descripcion
    notificacion_db.usuario_id = datos.usuario_id
    notificacion_db.status_id = datos.status_id
    db.commit()
    db.refresh(notificacion_db)
    return notificacion_db

@router.delete("/notificaciones/{id}")
def eliminar_notificacion(
    id: int, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    notificacion = db.query(Notificacion).filter(Notificacion.id == id).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    
    if notificacion.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar esta notificación")
    
    db.delete(notificacion)
    db.commit()
    return {"mensaje": "Notificación eliminada correctamente"}
