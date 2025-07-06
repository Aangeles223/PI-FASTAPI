from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from conexion import get_db
from models import App, Descarga, Valoracion, Desarrollador
from schemas import AppOut
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/apps-mas-descargadas", response_model=list[dict])
def apps_mas_descargadas(limite: int = 10, db: Session = Depends(get_db)):
    resultado = db.query(
        App.id_app,
        App.nombre,
        func.sum(Descarga.cantidad).label('total_descargas')
    ).join(Descarga).group_by(App.id_app, App.nombre).order_by(desc('total_descargas')).limit(limite).all()
    
    return [{"id_app": r.id_app, "nombre": r.nombre, "total_descargas": r.total_descargas} for r in resultado]

@router.get("/apps-mejor-valoradas", response_model=list[dict])
def apps_mejor_valoradas(limite: int = 10, db: Session = Depends(get_db)):
    resultado = db.query(
        App.id_app,
        App.nombre,
        func.avg(Valoracion.puntuacion).label('promedio_valoracion'),
        func.count(Valoracion.id_valoracion).label('total_valoraciones')
    ).join(Valoracion).group_by(App.id_app, App.nombre).having(func.count(Valoracion.id_valoracion) >= 5).order_by(desc('promedio_valoracion')).limit(limite).all()
    
    return [{"id_app": r.id_app, "nombre": r.nombre, "promedio_valoracion": round(float(r.promedio_valoracion), 2), "total_valoraciones": r.total_valoraciones} for r in resultado]

@router.get("/estadisticas-app/{id_app}")
def estadisticas_app(id_app: int, db: Session = Depends(get_db)):
    app = db.query(App).filter(App.id_app == id_app).first()
    if not app:
        raise HTTPException(status_code=404, detail="Aplicación no encontrada")
    
    total_descargas = db.query(func.sum(Descarga.cantidad)).filter(Descarga.id_app == id_app).scalar() or 0
    
    valoraciones_stats = db.query(
        func.avg(Valoracion.puntuacion).label('promedio'),
        func.count(Valoracion.id_valoracion).label('total')
    ).filter(Valoracion.id_app == id_app).first()
    
    descargas_recientes = db.query(
        func.sum(Descarga.cantidad)
    ).filter(
        Descarga.id_app == id_app,
        Descarga.fecha >= datetime.now().date() - timedelta(days=30)
    ).scalar() or 0
    
    return {
        "id_app": id_app,
        "nombre": app.nombre,
        "total_descargas": total_descargas,
        "descargas_ultimo_mes": descargas_recientes,
        "promedio_valoracion": round(float(valoraciones_stats.promedio), 2) if valoraciones_stats.promedio else 0,
        "total_valoraciones": valoraciones_stats.total
    }

@router.get("/desarrolladores-top", response_model=list[dict])
def desarrolladores_top(limite: int = 10, db: Session = Depends(get_db)):
    resultado = db.query(
        Desarrollador.id_desarrollador,
        Desarrollador.nombre,
        func.count(App.id_app).label('total_apps'),
        func.sum(Descarga.cantidad).label('total_descargas')
    ).join(App).join(Descarga).group_by(
        Desarrollador.id_desarrollador, 
        Desarrollador.nombre
    ).order_by(desc('total_descargas')).limit(limite).all()
    
    return [{"id_desarrollador": r.id_desarrollador, "nombre": r.nombre, "total_apps": r.total_apps, "total_descargas": r.total_descargas} for r in resultado]

@router.get("/resumen-general")
def resumen_general(db: Session = Depends(get_db)):
    total_apps = db.query(func.count(App.id_app)).filter(App.status_id == 1).scalar()
    total_desarrolladores = db.query(func.count(Desarrollador.id_desarrollador)).filter(Desarrollador.status_id == 1).scalar()
    total_descargas = db.query(func.sum(Descarga.cantidad)).scalar() or 0
    total_valoraciones = db.query(func.count(Valoracion.id_valoracion)).scalar()
    
    return {
        "total_aplicaciones": total_apps,
        "total_desarrolladores": total_desarrolladores,
        "total_descargas": total_descargas,
        "total_valoraciones": total_valoraciones
    }