from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import Descarga
from schemas import DescargaCreate, DescargaOut
from datetime import date

router = APIRouter()

@router.post("/descargas", response_model=DescargaOut)
def crear_descarga(descarga: DescargaCreate, db: Session = Depends(get_db)):
    nueva = Descarga(
        id_app=descarga.id_app,
        fecha=descarga.fecha or date.today(),
        cantidad=descarga.cantidad
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/descargas", response_model=list[DescargaOut])
def obtener_descargas(db: Session = Depends(get_db)):
    return db.query(Descarga).all()

@router.put("/descargas/{id_descarga}", response_model=DescargaOut)
def actualizar_descarga(id_descarga: int, descarga: DescargaCreate, db: Session = Depends(get_db)):
    descarga_db = db.query(Descarga).filter_by(id_descarga=id_descarga).first()
    if not descarga_db:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")

    descarga_db.id_app = descarga.id_app
    descarga_db.fecha = descarga.fecha or date.today()
    descarga_db.cantidad = descarga.cantidad
    db.commit()
    db.refresh(descarga_db)
    return descarga_db

@router.delete("/descargas/{id_descarga}")
def eliminar_descarga(id_descarga: int, db: Session = Depends(get_db)):
    descarga = db.query(Descarga).filter_by(id_descarga=id_descarga).first()
    if not descarga:
        raise HTTPException(status_code=404, detail="Descarga no encontrada")
    db.delete(descarga)
    db.commit()
    return {"mensaje": "Descarga eliminada correctamente"}
