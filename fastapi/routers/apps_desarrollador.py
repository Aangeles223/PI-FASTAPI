from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import AppsDesarrollador
from schemas import AppsDesarrolladorOut

router = APIRouter()

@router.post("/", response_model=AppsDesarrolladorOut)
def asociar_desarrollador_app(
    desarrollador_id: int = Query(..., description="ID del desarrollador"),
    app_id: int = Query(..., description="ID de la aplicación"),
    db: Session = Depends(get_db)
):
    existe = db.query(AppsDesarrollador).filter_by(
        desarrollador_id_desarrollador=desarrollador_id,
        app_id_app=app_id
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="La relación ya existe")
    
    nueva = AppsDesarrollador(
        desarrollador_id_desarrollador=desarrollador_id,
        app_id_app=app_id
    )
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[AppsDesarrolladorOut])
def obtener_todas_las_relaciones(db: Session = Depends(get_db)):
    return db.query(AppsDesarrollador).all()

@router.get("/desarrollador/{desarrollador_id}", response_model=list[AppsDesarrolladorOut])
def obtener_apps_de_desarrollador(desarrollador_id: int, db: Session = Depends(get_db)):
    return db.query(AppsDesarrollador).filter(AppsDesarrollador.desarrollador_id_desarrollador == desarrollador_id).all()

@router.get("/app/{app_id}", response_model=list[AppsDesarrolladorOut])
def obtener_desarrolladores_de_app(app_id: int, db: Session = Depends(get_db)):
    return db.query(AppsDesarrollador).filter(AppsDesarrollador.app_id_app == app_id).all()

@router.put("/{relacion_id}", response_model=AppsDesarrolladorOut)
def actualizar_relacion(
    relacion_id: int = Path(..., description="ID de la relación a actualizar"),
    desarrollador_id: int = Query(..., description="Nuevo ID del desarrollador"),
    app_id: int = Query(..., description="Nuevo ID de la aplicación"),
    db: Session = Depends(get_db)
):
    relacion = db.query(AppsDesarrollador).filter(AppsDesarrollador.id == relacion_id).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    existe = db.query(AppsDesarrollador).filter_by(
        desarrollador_id_desarrollador=desarrollador_id,
        app_id_app=app_id
    ).filter(AppsDesarrollador.id != relacion_id).first()
    if existe:
        raise HTTPException(status_code=400, detail="La nueva relación ya existe")
    
    relacion.desarrollador_id_desarrollador = desarrollador_id
    relacion.app_id_app = app_id
    db.commit(); db.refresh(relacion)
    return relacion

@router.delete("/{relacion_id}")
def eliminar_relacion(relacion_id: int, db: Session = Depends(get_db)):
    relacion = db.query(AppsDesarrollador).filter(AppsDesarrollador.id == relacion_id).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    db.delete(relacion)
    db.commit()
    return {"mensaje": "Relación eliminada correctamente"}
