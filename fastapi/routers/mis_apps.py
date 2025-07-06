from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import MisApp, Usuario
from schemas import MisAppCreate, MisAppOut
from conexion import get_db
from .usuarios import obtener_usuario_actual

router = APIRouter()

@router.post("/mis-apps", response_model=MisAppOut)
def crear_mis_app(
    data: MisAppCreate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    if data.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No autorizado para agregar apps a otro usuario")
    
    existe = db.query(MisApp).filter(
        MisApp.app_id_app == data.app_id_app,  # Corregido
        MisApp.usuario_id == data.usuario_id
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="La app ya está en tu lista")
    
    nueva = MisApp(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/mis-apps", response_model=list[MisAppOut])
def obtener_mis_apps(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    return db.query(MisApp).filter(MisApp.usuario_id == usuario_actual.id).all()

@router.put("/mis-apps/{id}", response_model=MisAppOut)
def actualizar_mis_app(
    id: int, 
    data: MisAppCreate, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    registro = db.query(MisApp).filter(MisApp.id == id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    if registro.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No autorizado para modificar este registro")
    
    if data.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No autorizado para asignar apps a otro usuario")
    
    registro.app_id_app = data.app_id_app  # Corregido
    registro.usuario_id = data.usuario_id
    db.commit()
    db.refresh(registro)
    return registro

@router.delete("/mis-apps/{id}")
def eliminar_mis_app(
    id: int, 
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    registro = db.query(MisApp).filter(MisApp.id == id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    if registro.usuario_id != usuario_actual.id:
        raise HTTPException(status_code=403, detail="No autorizado para eliminar este registro")
    
    db.delete(registro)
    db.commit()
    return {"mensaje": "Registro eliminado correctamente"}
