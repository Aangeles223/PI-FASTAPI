from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from conexion import get_db
from models import Usuario
from schemas import UsuarioCreate, UsuarioOut
from datetime import datetime
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import status as http_status
from jose import JWTError
from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordRequestForm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "clave-secreta-ultra-segura"  # cámbiala por algo fuerte
ALGORITHM = "HS256"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Función para crear el token JWT
def crear_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Función para obtener usuario por correo
def obtener_usuario_por_correo(db, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()

# Función para verificar token y obtener usuario
def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=http_status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        correo: str = payload.get("sub")
        if correo is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    usuario = obtener_usuario_por_correo(db, correo)
    if usuario is None:
        raise credentials_exception
    return usuario

@router.get("/usuarios", response_model=list[UsuarioOut])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@router.post("/usuarios", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_password = pwd_context.hash(usuario.contraseña)
    
    nuevo = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña=hashed_password,
        status_id=usuario.status_id,
        avatar=usuario.avatar,
        fecha_creacion=datetime.now()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

class LoginRequest(BaseModel):
    correo: EmailStr
    contraseña: str

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = obtener_usuario_por_correo(db, form_data.username)
    if not usuario or not pwd_context.verify(form_data.password, usuario.contraseña):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    access_token = crear_token({"sub": usuario.correo})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/usuarios/me", response_model=UsuarioOut)
def leer_usuario_actual(usuario: Usuario = Depends(obtener_usuario_actual)):
    return usuario

@router.put("/usuarios/{id}", response_model=UsuarioOut)
def actualizar_usuario(id: int, usuario_update: UsuarioCreate, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if usuario_actual.id != usuario.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    datos_update = usuario_update.dict()
    for campo, valor in datos_update.items():
        if campo == "contraseña":
            if valor and not pwd_context.verify(valor, usuario.contraseña):
                valor = pwd_context.hash(valor)
            else:
                continue  # No actualizar si viene vacía o igual
        setattr(usuario, campo, valor)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/usuarios/{id}")
def eliminar_usuario(id: int, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Solo el propio usuario puede eliminarse
    if usuario_actual.id != usuario.id:
        raise HTTPException(status_code=403, detail="No autorizado")
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}

@router.post("/token/refresh")
def refresh_token(usuario: Usuario = Depends(obtener_usuario_actual)):
    access_token = crear_token({"sub": usuario.correo})
    return {"access_token": access_token, "token_type": "bearer"}

