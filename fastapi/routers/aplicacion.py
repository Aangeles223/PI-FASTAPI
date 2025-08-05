from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from conexion import get_db
from models import App
from schemas import AppOut
from datetime import datetime
from typing import Optional
import base64
import binascii

router = APIRouter()

def validar_y_decodificar_base64(cadena_base64: Optional[str]) -> bytes:
    """Valida y decodifica base64, retorna bytes vacíos si es inválido o None"""
    if not cadena_base64 or cadena_base64.strip() == "":
        return b""
    
    try:
        # Limpiar espacios y verificar que no sea solo "x" o similar
        cadena_limpia = cadena_base64.strip()
        if len(cadena_limpia) < 4 or cadena_limpia in ["x", "xx", "xxx"]:
            return b""
        
        # Agregar padding si es necesario
        padding_needed = 4 - (len(cadena_limpia) % 4)
        if padding_needed != 4:
            cadena_limpia += "=" * padding_needed
        
        return base64.b64decode(cadena_limpia)
    except (binascii.Error, ValueError):
        # Si falla la decodificación, retornar bytes vacíos
        return b""

# Crear app
@router.post("/", response_model=AppOut)
def crear_app(
    nombre: str = Query(..., min_length=2, max_length=150, description="Nombre de la aplicación"),
    precio: str = Query(..., description="Precio (usar '0' para gratis)"),
    id_desarrollador: int = Query(..., description="ID del desarrollador"),
    descripcion: str = Query(..., min_length=10, description="Descripción de la app"),
    rango_edad: str = Query(..., description="Ej: 3+, 7+, 12+, 17+"),
    peso: str = Query(..., description="Tamaño (Ej: 50MB)"),
    status_id: int = Query(1, description="Status ID"),
    # Cambiar descripción para ser más clara:
    img1_base64: Optional[str] = Query(None, description="Imagen 1 en base64 válido (opcional, dejar vacío si no hay)"),
    img2_base64: Optional[str] = Query(None, description="Imagen 2 en base64 válido (opcional, dejar vacío si no hay)"),
    img3_base64: Optional[str] = Query(None, description="Imagen 3 en base64 válido (opcional, dejar vacío si no hay)"),
    icono_base64: Optional[str] = Query(None, description="Ícono en base64 válido (opcional, dejar vacío si no hay)"),
    db: Session = Depends(get_db)
):
    # Usar la función de validación:
    img1 = validar_y_decodificar_base64(img1_base64)
    img2 = validar_y_decodificar_base64(img2_base64)
    img3l = validar_y_decodificar_base64(img3_base64)
    icono = validar_y_decodificar_base64(icono_base64)
    
    nueva = App(
        nombre=nombre, precio=precio, id_desarrollador=id_desarrollador,
        descripcion=descripcion, img1=img1, img2=img2, img3l=img3l,
        icono=icono, rango_edad=rango_edad, peso=peso,
        fecha_creacion=datetime.now(), status_id=status_id
    )
    db.add(nueva); db.commit(); db.refresh(nueva)
    return nueva

# Obtener todas las apps
@router.get("/", response_model=list[AppOut])
def obtener_apps(db: Session = Depends(get_db)):
    return db.query(App).all()

# Actualizar una app por ID
@router.put("/{id_app}", response_model=AppOut)
def actualizar_app(
    id_app: int = Path(..., description="ID de la app a actualizar"),
    nombre: str = Query(..., min_length=2, max_length=150, description="Nuevo nombre"),
    precio: str = Query(..., description="Nuevo precio"),
    id_desarrollador: int = Query(..., description="Nuevo ID desarrollador"),
    descripcion: str = Query(..., min_length=10, description="Nueva descripción"),
    rango_edad: str = Query(..., description="Nuevo rango de edad"),
    peso: str = Query(..., description="Nuevo peso"),
    status_id: int = Query(..., description="Nuevo status"),
    db: Session = Depends(get_db)
):
    existente = db.query(App).filter(App.id_app == id_app).first()
    if not existente:
        raise HTTPException(status_code=404, detail="App no encontrada")
    
    existente.nombre = nombre
    existente.precio = precio
    existente.id_desarrollador = id_desarrollador
    existente.descripcion = descripcion
    existente.rango_edad = rango_edad
    existente.peso = peso
    existente.status_id = status_id
    db.commit(); db.refresh(existente)
    return existente

# Eliminar una app por ID
@router.delete("/{id_app}")
def eliminar_app(
    id_app: int = Path(..., description="ID de la app a eliminar"),
    db: Session = Depends(get_db)
):
    app = db.query(App).filter(App.id_app == id_app).first()
    if not app:
        raise HTTPException(status_code=404, detail="App no encontrada")
    db.delete(app); db.commit()
    return {"mensaje": "App eliminada correctamente"}
