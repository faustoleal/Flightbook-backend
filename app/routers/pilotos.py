from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.db import get_db
from models.pilotos import Pilotos
from schemas.pilotos import ResponsePilotoSchema, NewPilotoSchema

router = APIRouter(prefix="/pilotos")

@router.get("/", response_model=list[ResponsePilotoSchema])
def getPilotos(db:Session = Depends(get_db)):
  pilotos = select(Pilotos)
  result = db.execute(pilotos).scalars().all()
  return result

@router.post("/", response_model=NewPilotoSchema)
def createPiloto(piloto:NewPilotoSchema, db:Session = Depends(get_db)):
# 1. Verificar si ya existe (usando select + execute)
    stmt = select(Pilotos).where(Pilotos.usuario == piloto.usuario)
    existe = db.execute(stmt).scalars().first()
    if existe:
        raise HTTPException(status_code=400, detail="El usuario ya esta registrado")

    # 2. Crear nuevo registro
    nuevo = Pilotos(**piloto.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # 3. Devolver el objeto serializado con schema
    return nuevo