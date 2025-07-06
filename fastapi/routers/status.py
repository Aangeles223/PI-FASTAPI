from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import Status
from schemas import StatusOut

router = APIRouter()

@router.post("/status", response_model=StatusOut)
def crear_status(
    nombre: str = Query(..., min_length=2, max_length=45, description="Nombre del estado"),
    db: Session = Depends(get_db)
):
    nuevo = Status(nombre=nombre)
    db.add(nuevo); db.commit(); db.refresh(nuevo)
    return nuevo

@router.get("/status", response_model=list[StatusOut])
def obtener_status(db: Session = Depends(get_db)):
    return db.query(Status).all()

@router.get("/status/{id}", response_model=StatusOut)
def obtener_status_por_id(id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    return status

@router.put("/status/{id}", response_model=StatusOut)
def actualizar_status(
    id: int = Path(..., description="ID del status a actualizar"),
    nombre: str = Query(..., min_length=2, max_length=45, description="Nuevo nombre del estado"),
    db: Session = Depends(get_db)
):
    status_db = db.query(Status).filter(Status.id == id).first()
    if not status_db:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    status_db.nombre = nombre
    db.commit(); db.refresh(status_db)
    return status_db

@router.delete("/status/{id}")
def eliminar_status(
    id: int = Path(..., description="ID del status a eliminar"),
    db: Session = Depends(get_db)
):
    status = db.query(Status).filter(Status.id == id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    db.delete(status); db.commit()
    return {"mensaje": "Status eliminado correctamente"}
