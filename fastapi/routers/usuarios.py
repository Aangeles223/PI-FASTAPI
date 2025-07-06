from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import Optional
from pydantic import BaseModel, EmailStr
from starlette import status as http_status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session
from conexion import get_db
from models import Usuario
from schemas import UsuarioOut
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "clave-secreta-ultra-segura"
ALGORITHM = "HS256"
security = HTTPBearer()

router = APIRouter()

# Función para crear el token JWT
def crear_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class LoginRequest(BaseModel):
    correo: EmailStr
    contraseña: str

def obtener_usuario_actual(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.post("/usuarios", response_model=UsuarioOut)
def crear_usuario(
    nombre: str = Query(..., min_length=2, max_length=45, description="Nombre del usuario"),
    correo: EmailStr = Query(..., description="Correo electrónico"),
    contraseña: str = Query(..., min_length=6, max_length=50, description="Contraseña"),
    status_id: int = Query(1, description="Status ID (1=Activo)"),
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
        fecha_creacion=datetime.now()
    )
    db.add(u); db.commit(); db.refresh(u)
    return u

@router.post("/token")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == login_data.correo).first()
    if not usuario or not pwd_context.verify(login_data.contraseña, usuario.contraseña):
        raise HTTPException(401, "Credenciales incorrectas")
    token = crear_token({"sub": usuario.correo})
    return {"access_token": token, "token_type": "bearer"}

@router.put("/usuarios/{id}", response_model=UsuarioOut)
def actualizar_usuario(
    id: int = Path(..., ge=1, description="ID del usuario a actualizar"),
    nombre: str = Query(..., min_length=2, max_length=45, description="Nuevo nombre"),
    correo: EmailStr = Query(..., description="Nuevo correo"),
    contraseña: Optional[str] = Query(None, min_length=6, max_length=50, description="Nueva contraseña (opcional)"),
    status_id: int = Query(..., description="Nuevo status ID"),
    db: Session = Depends(get_db),
    token=Depends(security)
):
    u = db.query(Usuario).get(id)
    if not u: 
        raise HTTPException(404, "Usuario no encontrado")
    u.nombre = nombre
    u.correo = correo
    u.status_id = status_id
    if contraseña:
        u.contraseña = pwd_context.hash(contraseña)
    db.commit(); db.refresh(u)
    return u

@router.delete("/usuarios/{id}")
def eliminar_usuario(
    id: int = Path(..., ge=1, description="ID del usuario a eliminar"),
    db: Session = Depends(get_db),
    token=Depends(security)
):
    u = db.query(Usuario).get(id)
    if not u: 
        raise HTTPException(404, "Usuario no encontrado")
    db.delete(u); db.commit()
    return {"mensaje": "Usuario eliminado"}

@router.get("/usuarios", response_model=list[UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.get("/usuarios/me", response_model=UsuarioOut)
def leer_usuario_actual(usuario: Usuario = Depends(obtener_usuario_actual)):
    return usuario

# ...resto de endpoints GET igual...

