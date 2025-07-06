from fastapi import APIRouter, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import VersionApp, App
from schemas import VersionAppOut
from datetime import date

router = APIRouter()

@router.post("/versiones", response_model=VersionAppOut)
def crear_version(
    id_app: int = Body(..., description="ID de la aplicación"),
    numero_version: str = Body(..., description="Ej: 1.0.0"),
    fecha_lanzamiento: date = Body(..., description="Fecha de lanzamiento"),
    enlace_apk: str = Body(..., description="URL del APK"),
    db: Session = Depends(get_db)
):
    app_existe = db.query(App).filter(App.id_app == id_app).first()
    if not app_existe:
        raise HTTPException(404, "La aplicación no existe")
    if db.query(VersionApp).filter(VersionApp.id_app==id_app,
                                   VersionApp.numero_version==numero_version).first():
        raise HTTPException(400, "Esta versión ya existe")
    nueva = VersionApp(
        id_app=id_app,
        numero_version=numero_version,
        fecha_lanzamiento=fecha_lanzamiento,
        enlace_apk=enlace_apk
    )
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@router.get("/versiones", response_model=list[VersionAppOut])
def obtener_versiones(db: Session = Depends(get_db)):
    return db.query(VersionApp).all()

@router.get("/versiones/app/{id_app}", response_model=list[VersionAppOut])
def obtener_versiones_por_app(id_app: int, db: Session = Depends(get_db)):
    return db.query(VersionApp).filter(VersionApp.id_app == id_app).order_by(VersionApp.fecha_lanzamiento.desc()).all()

@router.get("/versiones/{id_version}", response_model=VersionAppOut)
def obtener_version(id_version: int, db: Session = Depends(get_db)):
    version = db.query(VersionApp).filter(VersionApp.id_version == id_version).first()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")
    return version

@router.put("/versiones/{id_version}", response_model=VersionAppOut)
def actualizar_version(
    id_version: int = Path(..., description="ID de versión a actualizar"),
    numero_version: str = Body(..., description="Nuevo número de versión"),
    fecha_lanzamiento: date = Body(..., description="Nueva fecha de lanzamiento"),
    enlace_apk: str = Body(..., description="Nuevo enlace APK"),
    db: Session = Depends(get_db)
):
    v = db.query(VersionApp).get(id_version)
    if not v:
        raise HTTPException(404, "Versión no encontrada")
    v.numero_version = numero_version
    v.fecha_lanzamiento = fecha_lanzamiento
    v.enlace_apk = enlace_apk
    db.commit(); db.refresh(v)
    return v

@router.delete("/versiones/{id_version}")
def eliminar_version(
    id_version: int = Path(..., description="ID de versión a eliminar"),
    db: Session = Depends(get_db)
):
    v = db.query(VersionApp).get(id_version)
    if not v:
        raise HTTPException(404, "Versión no encontrada")
    db.delete(v); db.commit()
    return {"mensaje": "Versión eliminada"}
