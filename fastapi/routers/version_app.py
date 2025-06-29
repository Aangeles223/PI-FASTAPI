from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import VersionApp
from schemas import VersionAppCreate, VersionAppOut

router = APIRouter()

@router.post("/versiones", response_model=VersionAppOut)
def crear_version(version: VersionAppCreate, db: Session = Depends(get_db)):
    nueva = VersionApp(**version.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/versiones", response_model=list[VersionAppOut])
def obtener_versiones(db: Session = Depends(get_db)):
    return db.query(VersionApp).all()

@router.put("/versiones/{id_version}", response_model=VersionAppOut)
def actualizar_version(id_version: int, version: VersionAppCreate, db: Session = Depends(get_db)):
    version_db = db.query(VersionApp).filter_by(id_version=id_version).first()
    if not version_db:
        raise HTTPException(status_code=404, detail="Versión no encontrada")
    for campo, valor in version.dict().items():
        setattr(version_db, campo, valor)
    db.commit()
    db.refresh(version_db)
    return version_db

@router.delete("/versiones/{id_version}")
def eliminar_version(id_version: int, db: Session = Depends(get_db)):
    version = db.query(VersionApp).filter_by(id_version=id_version).first()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")
    db.delete(version)
    db.commit()
    return {"mensaje": "Versión eliminada correctamente"}
