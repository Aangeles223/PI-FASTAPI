from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import AppSeccion
from schemas import AppSeccionCreate, AppSeccionOut

router = APIRouter()

@router.post("/", response_model=AppSeccionOut)
def crear_app_seccion(data: AppSeccionCreate, db: Session = Depends(get_db)):
    existe = db.query(AppSeccion).filter_by(
        id_app=data.id_app, id_seccion=data.id_seccion
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe esta relación")
    nueva = AppSeccion(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[AppSeccionOut])
def obtener_todas(db: Session = Depends(get_db)):
    return db.query(AppSeccion).all()

@router.put("/", response_model=AppSeccionOut)
def actualizar_prioridad(data: AppSeccionCreate, db: Session = Depends(get_db)):
    relacion = db.query(AppSeccion).filter_by(
        id_app=data.id_app, id_seccion=data.id_seccion
    ).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    relacion.prioridad = data.prioridad
    db.commit()
    db.refresh(relacion)
    return relacion

@router.delete("/")
def eliminar_relacion(data: AppSeccionCreate, db: Session = Depends(get_db)):
    relacion = db.query(AppSeccion).filter_by(
        id_app=data.id_app, id_seccion=data.id_seccion
    ).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    db.delete(relacion)
    db.commit()
    return {"mensaje": "Relación eliminada correctamente"}
