from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import AppSeccion
from schemas import AppSeccionOut

router = APIRouter()

@router.post("/", response_model=AppSeccionOut)
def asociar_app_seccion(
    app_id: int = Query(..., description="ID de la aplicación"),
    seccion_id: int = Query(..., description="ID de la sección"),
    prioridad: int = Query(0, ge=0, le=10, description="Prioridad 0-10"),
    db: Session = Depends(get_db)
):
    existe = db.query(AppSeccion).filter_by(
        id_app=app_id,
        id_seccion=seccion_id
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="La relación ya existe")
    
    nueva = AppSeccion(id_app=app_id, id_seccion=seccion_id, prioridad=prioridad)
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[AppSeccionOut])
def obtener_todas_las_relaciones(db: Session = Depends(get_db)):
    return db.query(AppSeccion).all()

@router.get("/app/{app_id}", response_model=list[AppSeccionOut])
def obtener_secciones_de_app(app_id: int, db: Session = Depends(get_db)):
    return db.query(AppSeccion).filter(AppSeccion.id_app == app_id).all()

@router.get("/seccion/{seccion_id}", response_model=list[AppSeccionOut])
def obtener_apps_de_seccion(seccion_id: int, db: Session = Depends(get_db)):
    return db.query(AppSeccion).filter(AppSeccion.id_seccion == seccion_id).order_by(AppSeccion.prioridad.desc()).all()

@router.get("/{relacion_id}", response_model=AppSeccionOut)
def obtener_relacion_por_id(relacion_id: int, db: Session = Depends(get_db)):
    relacion = db.query(AppSeccion).filter(AppSeccion.id == relacion_id).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return relacion

@router.put("/{relacion_id}", response_model=AppSeccionOut)
def actualizar_relacion(
    relacion_id: int = Path(..., description="ID de la relación a actualizar"),
    app_id: int = Query(..., description="Nuevo ID de aplicación"),
    seccion_id: int = Query(..., description="Nuevo ID de sección"),
    prioridad: int = Query(..., ge=0, le=10, description="Nueva prioridad"),
    db: Session = Depends(get_db)
):
    relacion = db.query(AppSeccion).filter(AppSeccion.id == relacion_id).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    existe = db.query(AppSeccion).filter_by(
        id_app=app_id,
        id_seccion=seccion_id
    ).filter(AppSeccion.id != relacion_id).first()
    if existe:
        raise HTTPException(status_code=400, detail="La nueva relación ya existe")
    
    relacion.id_app = app_id
    relacion.id_seccion = seccion_id
    relacion.prioridad = prioridad
    db.commit(); db.refresh(relacion)
    return relacion

@router.delete("/{relacion_id}")
def eliminar_relacion(relacion_id: int, db: Session = Depends(get_db)):
    relacion = db.query(AppSeccion).filter(AppSeccion.id == relacion_id).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    db.delete(relacion)
    db.commit()
    return {"mensaje": "Relación eliminada correctamente"}
