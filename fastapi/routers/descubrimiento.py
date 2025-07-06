from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from conexion import get_db
from models import App, AppSeccion, Seccion, Descarga, Valoracion
from schemas import AppOut
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/apps-destacadas", response_model=list[AppOut])
def apps_destacadas(limite: int = 10, db: Session = Depends(get_db)):
    return db.query(App).join(AppSeccion).filter(
        AppSeccion.prioridad > 0,
        App.status_id == 1
    ).order_by(desc(AppSeccion.prioridad)).limit(limite).all()

@router.get("/apps-nuevas", response_model=list[AppOut])
def apps_nuevas(limite: int = 10, db: Session = Depends(get_db)):
    return db.query(App).filter(
        App.status_id == 1
    ).order_by(desc(App.fecha_creacion)).limit(limite).all()

@router.get("/apps-tendencia", response_model=list[AppOut])
def apps_tendencia(limite: int = 10, db: Session = Depends(get_db)):
    fecha_limite = datetime.now().date() - timedelta(days=7)
    
    apps_trending = db.query(
        App,
        func.sum(Descarga.cantidad).label('descargas_semana')
    ).join(Descarga).filter(
        Descarga.fecha >= fecha_limite,
        App.status_id == 1
    ).group_by(App.id_app).order_by(desc('descargas_semana')).limit(limite).all()
    
    return [app for app, _ in apps_trending]

@router.get("/apps-gratis-top", response_model=list[AppOut])
def apps_gratis_top(limite: int = 10, db: Session = Depends(get_db)):
    return db.query(App).join(Descarga).filter(
        App.precio == "0",
        App.status_id == 1
    ).group_by(App.id_app).order_by(desc(func.sum(Descarga.cantidad))).limit(limite).all()

@router.get("/apps-por-seccion/{id_seccion}", response_model=list[AppOut])
def apps_por_seccion(id_seccion: int, limite: int = 20, db: Session = Depends(get_db)):
    return db.query(App).join(AppSeccion).filter(
        AppSeccion.id_seccion == id_seccion,
        App.status_id == 1
    ).order_by(desc(AppSeccion.prioridad), desc(App.fecha_creacion)).limit(limite).all()

@router.get("/recomendaciones/{usuario_id}", response_model=list[AppOut])
def recomendaciones_usuario(usuario_id: int, limite: int = 10, db: Session = Depends(get_db)):
    from models import MisApp, AppCategoria
    
    categorias_usuario = db.query(AppCategoria.categorias_id).join(
        MisApp, AppCategoria.app_id_app == MisApp.app_id_app
    ).filter(MisApp.usuario_id == usuario_id).distinct().subquery()
    
    apps_recomendadas = db.query(App).join(AppCategoria).filter(
        AppCategoria.categorias_id.in_(categorias_usuario),
        App.status_id == 1,
        ~App.id_app.in_(
            db.query(MisApp.app_id_app).filter(MisApp.usuario_id == usuario_id)
        )
    ).join(Valoracion).group_by(App.id_app).order_by(
        desc(func.avg(Valoracion.puntuacion))
    ).limit(limite).all()
    
    return apps_recomendadas