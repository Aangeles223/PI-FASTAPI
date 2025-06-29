from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import AppsDesarrollador
from schemas import AppsDesarrolladorCreate
from typing import List

router = APIRouter()

# POST: Crear asociación
@router.post("/", tags=["Apps-Desarrollador"])
def crear_asociacion(data: AppsDesarrolladorCreate, db: Session = Depends(get_db)):
    nueva = AppsDesarrollador(
        desarrollador_id_desarrollador=data.desarrollador_id_desarrollador,
        app_id_app=data.app_id_app
    )
    db.add(nueva)
    db.commit()
    return {"mensaje": "Asociación registrada correctamente"}

# GET: Obtener todas las asociaciones
@router.get("/", tags=["Apps-Desarrollador"])
def obtener_asociaciones(db: Session = Depends(get_db)):
    return db.query(AppsDesarrollador).all()

# PUT: Actualizar una asociación existente por ID
@router.put("/{id}", tags=["Apps-Desarrollador"])
def actualizar_asociacion(id: int, data: AppsDesarrolladorCreate, db: Session = Depends(get_db)):
    asociacion = db.query(AppsDesarrollador).filter(AppsDesarrollador.id == id).first()
    if not asociacion:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")

    asociacion.desarrollador_id_desarrollador = data.desarrollador_id_desarrollador
    asociacion.app_id_app = data.app_id_app
    db.commit()
    return {"mensaje": "Asociación actualizada correctamente"}

# DELETE: Eliminar una asociación por ID
@router.delete("/{id}", tags=["Apps-Desarrollador"])
def eliminar_asociacion(id: int, db: Session = Depends(get_db)):
    asociacion = db.query(AppsDesarrollador).filter(AppsDesarrollador.id == id).first()
    if not asociacion:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    
    db.delete(asociacion)
    db.commit()
    return {"mensaje": "Asociación eliminada correctamente"}
