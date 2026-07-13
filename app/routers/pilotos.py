from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.db import get_db
from models import Pilotos
import bcrypt
from schemas import ResponsePilotoSchema, NewPilotoSchema

router = APIRouter(prefix="/api/pilotos")


@router.get("/", response_model=list[ResponsePilotoSchema])
def getPilotos(db:Session = Depends(get_db)):
  pilotos = select(Pilotos)
  result = db.execute(pilotos).scalars().all()
  return result

@router.get("/{id}", response_model=ResponsePilotoSchema)
def getPilotoById(id:int, db:Session = Depends(get_db)):
   piloto= select(Pilotos).where(Pilotos.id == id)
   piloto_existe = db.execute(piloto).scalar_one_or_none()
   if piloto_existe is None:
      raise HTTPException(status_code=404, detail="El usuario no existe." )
   return piloto_existe

@router.post("/", response_model=NewPilotoSchema)
def createPiloto(piloto:NewPilotoSchema, db:Session = Depends(get_db)):
    # 1. Verificar si ya existe y si el formulario esta completo
    if not piloto.name or not piloto.usuario or not piloto.password:
       raise HTTPException(status_code=401, detail="El formulario no esta completo.")
    
    stmt = select(Pilotos).where(Pilotos.usuario == piloto.usuario)
    existe = db.execute(stmt).scalars().first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya esta registrado.")
    
    # Hash de contraseña

    salt = bcrypt.gensalt(rounds=10)
    password_hash = bcrypt.hashpw(piloto.password.encode("utf-8")[:72],salt).decode("utf-8")

    # Crear piloto

    new_piloto = Pilotos(
       name=piloto.name,
       usuario = piloto.usuario,
       password_hash = password_hash
    )

    # 2. Crear nuevo registro
    db.add(new_piloto)
    db.commit()
    db.refresh(new_piloto)

    # 3. Devolver el objeto serializado con schema
    return new_piloto