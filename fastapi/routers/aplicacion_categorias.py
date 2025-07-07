from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import AppCategoria, App, Categoria  # ← Importar Categoria también
from schemas import AppCategoriaOut

router = APIRouter()

@router.post("/", response_model=AppCategoriaOut)
def asociar_app_categoria(
    app_id: int = Query(..., description="ID de la aplicación"),
    categoria_id: int = Query(..., description="ID de la categoría"),
    db: Session = Depends(get_db)
):
    # ← VALIDAR QUE EXISTAN LOS REGISTROS PADRE:
    app_existe = db.query(App).filter(App.id_app == app_id).first()
    if not app_existe:
        raise HTTPException(status_code=404, detail=f"No existe la aplicación con ID {app_id}")
    
    categoria_existe = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not categoria_existe:
        raise HTTPException(status_code=404, detail=f"No existe la categoría con ID {categoria_id}")
    
    # Verificar que no exista ya la relación
    existe = db.query(AppCategoria).filter_by(
        app_id_app=app_id,
        categorias_id=categoria_id
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="La relación ya existe")
    
    nueva = AppCategoria(app_id_app=app_id, categorias_id=categoria_id)
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

@router.get("/", response_model=list[AppCategoriaOut])
def obtener_todas_las_relaciones(db: Session = Depends(get_db)):
    return db.query(AppCategoria).all()

@router.get("/app/{app_id}", response_model=list[AppCategoriaOut])
def obtener_categorias_de_app(app_id: int, db: Session = Depends(get_db)):
    return db.query(AppCategoria).filter(AppCategoria.app_id_app == app_id).all()

@router.get("/categoria/{categoria_id}", response_model=list[AppCategoriaOut])
def obtener_apps_de_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return db.query(AppCategoria).filter(AppCategoria.categorias_id == categoria_id).all()

@router.get("/{relacion_id}", response_model=AppCategoriaOut)
def obtener_relacion_por_id(relacion_id: int, db: Session = Depends(get_db)):
    relacion = db.query(AppCategoria).filter(AppCategoria.id == relacion_id).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return relacion

@router.put("/{relacion_id}", response_model=AppCategoriaOut)
def actualizar_relacion(
    relacion_id: int = Path(..., description="ID de la relación a actualizar"),
    app_id: int = Query(..., description="Nuevo ID de aplicación"),
    categoria_id: int = Query(..., description="Nuevo ID de categoría"),
    db: Session = Depends(get_db)
):
    relacion = db.query(AppCategoria).filter(AppCategoria.id == relacion_id).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    existe = db.query(AppCategoria).filter_by(
        app_id_app=app_id,
        categorias_id=categoria_id
    ).filter(AppCategoria.id != relacion_id).first()
    if existe:
        raise HTTPException(status_code=400, detail="La nueva relación ya existe")
    
    relacion.app_id_app = app_id
    relacion.categorias_id = categoria_id
    db.commit(); db.refresh(relacion)
    return relacion

@router.delete("/{relacion_id}")
def eliminar_relacion(relacion_id: int, db: Session = Depends(get_db)):
    relacion = db.query(AppCategoria).filter(AppCategoria.id == relacion_id).first()
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    
    db.delete(relacion)
    db.commit()
    return {"mensaje": "Relación eliminada correctamente"}
