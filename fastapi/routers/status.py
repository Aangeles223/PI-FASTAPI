from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from conexion import get_db
from models import Status
from schemas import StatusPydantic

routerStatus = APIRouter()

@routerStatus.get("/status", tags=["Status"])
def obtener_todos(db: Session = Depends(get_db)):
    return db.query(Status).all()

@routerStatus.get("/status/{id}", tags=["Status"])
def obtener_por_id(id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    return status

@routerStatus.post("/status", tags=["Status"])
def crear_status(nuevo: StatusPydantic, db: Session = Depends(get_db)):
    existe = db.query(Status).filter(Status.id == nuevo.id).first()
    if existe:
        raise HTTPException(status_code=400, detail="El ID ya existe")
    nuevo_status = Status(**nuevo.dict())
    db.add(nuevo_status)
    db.commit()
    return {"mensaje": "Status creado exitosamente"}

@routerStatus.put("/status/{id}", tags=["Status"])
def actualizar_status(id: int, datos: StatusPydantic, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    for campo, valor in datos.dict().items():
        setattr(status, campo, valor)
    db.commit()
    return {"mensaje": "Status actualizado correctamente"}

@routerStatus.delete("/status/{id}", tags=["Status"])
def eliminar_status(id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    db.delete(status)
    db.commit()
    return {"mensaje": "Status eliminado exitosamente"}
