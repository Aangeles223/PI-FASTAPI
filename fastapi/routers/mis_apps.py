from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import MisApp
from schemas import MisAppCreate, MisAppOut
from conexion import get_db

router = APIRouter()

@router.post("/mis-apps", response_model=MisAppOut)
def crear_mis_app(data: MisAppCreate, db: Session = Depends(get_db)):
    nueva = MisApp(**data.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/mis-apps", response_model=list[MisAppOut])
def obtener_mis_apps(db: Session = Depends(get_db)):
    return db.query(MisApp).all()

@router.put("/mis-apps/{id}", response_model=MisAppOut)
def actualizar_mis_app(id: int, data: MisAppCreate, db: Session = Depends(get_db)):
    registro = db.query(MisApp).filter_by(id=id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    registro.app_id_app = data.app_id_app
    registro.usuario_id = data.usuario_id
    db.commit()
    db.refresh(registro)
    return registro

@router.delete("/mis-apps/{id}")
def eliminar_mis_app(id: int, db: Session = Depends(get_db)):
    registro = db.query(MisApp).filter_by(id=id).first()
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    db.delete(registro)
    db.commit()
    return {"mensaje": "Registro eliminado correctamente"}
