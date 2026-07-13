from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.db import get_db
from utils.config import SECRET, ALGORITHM
import bcrypt
from jose import jwt
from models import Pilotos
from schemas import LoginResponse, LoginRequest

router = APIRouter(prefix="/api/login")

@router.post("/", response_model=LoginResponse)
async def login(data: LoginRequest, db:Session = Depends(get_db)):
  #1. Buscar piloto
  find_piloto = select(Pilotos).where(Pilotos.usuario == data.usuario)
  result = db.execute(find_piloto).scalar_one_or_none()

  piloto = result

  #2. Verificar contraseña

  password_correct = (
    piloto is not None and bcrypt.checkpw(data.password.encode("utf-8"), piloto.password_hash.encode("utf-8"))
  )

  if not password_correct:
    return HTTPException(status_code=401, detail="invalid username or password")
  
  piloto_for_token = {
    "usuario": piloto.usuario,
    "id": piloto.id
  }

  token = jwt.encode(piloto_for_token, SECRET, algorithm=ALGORITHM)

  return {"token": token, **piloto_for_token}
