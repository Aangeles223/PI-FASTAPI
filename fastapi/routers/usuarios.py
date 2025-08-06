from fastapi import APIRouter, Depends, HTTPException, Query, Path, Body
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from starlette import status as http_status
from sqlalchemy.orm import Session
from conexion import get_db
from models import Usuario
from schemas import UsuarioOut, UsuarioUpdate
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, date

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "clave-secreta-ultra-segura"
ALGORITHM = "HS256"

router = APIRouter()

# Función para crear el token JWT
def crear_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class LoginRequest(BaseModel):
    correo: EmailStr
    contrasena: str = Field(..., alias="contraseña")

    model_config = ConfigDict(populate_by_name=True)


@router.post("/", response_model=UsuarioOut)
def crear_usuario(
    nombre: str = Query(..., min_length=2, max_length=45, description="Nombre del usuario"),
    correo: EmailStr = Query(..., description="Correo electrónico"),
    contraseña: str = Query(..., min_length=6, max_length=50, description="Contraseña"),
    status_id: int = Query(1, description="Status ID (1=Activo)"),
    telefono: Optional[str] = Query(None, max_length=20, description="Teléfono (opcional)"),
    pais_id: Optional[int] = Query(None, description="ID de país (opcional)"),
    direccion: Optional[str] = Query(None, max_length=100, description="Dirección (opcional)"),
    genero_id: Optional[int] = Query(None, description="ID de género (opcional)"),
    fecha_nacimiento: Optional[date] = Query(None, description="Fecha de nacimiento (opcional)"),
    db: Session = Depends(get_db)
):
    if db.query(Usuario).filter(Usuario.correo == correo).first():
        raise HTTPException(400, "Correo ya registrado")
    hashed = pwd_context.hash(contraseña)
    u = Usuario(
        nombre=nombre,
        correo=correo,
        contraseña=hashed,
        status_id=status_id,
        avatar=b"",
        fecha_creacion=datetime.now(),
        telefono=telefono,
        pais_id=pais_id,
        direccion=direccion,
        genero_id=genero_id,
        fecha_nacimiento=fecha_nacimiento
    )
    db.add(u); db.commit(); db.refresh(u)
    return u

@router.post("/token")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == login_data.correo).first()
    if not usuario or not pwd_context.verify(login_data.contrasena, usuario.contraseña):
        raise HTTPException(401, "Credenciales incorrectas")
    token = crear_token({"sub": usuario.correo})
    return {"access_token": token, "token_type": "bearer"}

# Refactorizar endpoint PUT para recibir body en lugar de query
@router.put("/{id}", response_model=UsuarioOut)
def actualizar_usuario(
    id: int = Path(..., ge=1, description="ID del usuario a actualizar"),
    datos: UsuarioUpdate = Body(...),
    db: Session = Depends(get_db)
):
    u = db.query(Usuario).get(id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    update_data = datos.dict(exclude_unset=True)
    if "contraseña" in update_data:
        update_data["contraseña"] = pwd_context.hash(update_data["contraseña"])
    for campo, valor in update_data.items():
        setattr(u, campo, valor)
    db.commit(); db.refresh(u)
    return u

@router.delete("/{id}")
def eliminar_usuario(
    id: int = Path(..., ge=1, description="ID del usuario a eliminar"),
    db: Session = Depends(get_db)
):
    u = db.query(Usuario).get(id)
    if not u: 
        raise HTTPException(404, "Usuario no encontrado")
    db.delete(u); db.commit()
    return {"mensaje": "Usuario eliminado"}

@router.get("/", response_model=list[UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get("/me", response_model=UsuarioOut)
def leer_usuario_actual(
    id: int = Query(..., ge=1, description="ID del usuario a obtener"),
    db: Session = Depends(get_db)
):
    u = db.query(Usuario).get(id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    return u

# Añadir endpoint PUT /me para actualizar perfil actual
@router.put("/me", response_model=UsuarioOut)
def actualizar_mi_usuario(
    id: int = Query(..., ge=1, description="ID del usuario a actualizar"),
    datos: UsuarioUpdate = Body(...),
    db: Session = Depends(get_db)
):
    u = db.query(Usuario).get(id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    update_data = datos.dict(exclude_unset=True)
    if "contraseña" in update_data:
        update_data["contraseña"] = pwd_context.hash(update_data["contraseña"])
    for campo, valor in update_data.items():
        setattr(u, campo, valor)
    db.commit(); db.refresh(u)
    return u

