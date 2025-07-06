from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import Descarga, Usuario
from schemas import DescargaOut
from datetime import date
from typing import Optional
from .usuarios import obtener_usuario_actual  # ← Importar función de autenticación

router = APIRouter()

@router.get("/descargas", response_model=list[DescargaOut])
def obtener_descargas(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)  # ← Requiere autenticación
):
    return db.query(Descarga).all()

@router.post("/descargas", response_model=DescargaOut)
def crear_descarga(
    id_app: int = Query(..., description="ID de la aplicación"),
    fecha: Optional[date] = Query(None, description="Fecha de descarga (auto si se omite)"),
    cantidad: int = Query(1, ge=1, description="Número de descargas"),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)  # ← Requiere autenticación
):
    nueva = Descarga(
        id_app=id_app,
        fecha=fecha or date.today(),
        cantidad=cantidad
    )
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@router.put("/descargas/{id_descarga}", response_model=DescargaOut)
def actualizar_descarga(
    id_descarga: int = Path(..., description="ID de la descarga a actualizar"),
    id_app: int = Query(..., description="Nuevo ID de aplicación"),
    fecha: Optional[date] = Query(None, description="Nueva fecha"),
    cantidad: int = Query(..., ge=1, description="Nueva cantidad"),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)  # ← Requiere autenticación
):
    descarga_db = db.query(Descarga).filter_by(id_descarga=id_descarga).first()
    if not descarga_db:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")

    descarga_db.id_app = id_app
    descarga_db.fecha = fecha or date.today()
    descarga_db.cantidad = cantidad
    db.commit(); db.refresh(descarga_db)
    return descarga_db

@router.delete("/descargas/{id_descarga}")
def eliminar_descarga(
    id_descarga: int = Path(..., description="ID de la descarga a eliminar"),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)  # ← Requiere autenticación
):
    descarga = db.query(Descarga).filter_by(id_descarga=id_descarga).first()
    if not descarga:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")
    
    db.delete(descarga); db.commit()
    return {"mensaje": "Descarga eliminada correctamente"}
