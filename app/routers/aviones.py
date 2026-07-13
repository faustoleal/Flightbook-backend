from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.db import get_db
from models import Aviones
from schemas import AvionSchema

router = APIRouter(prefix="/api/aviones")

@router.get("/", response_model=list[AvionSchema])
def getAviones(db:Session = Depends(get_db)):
  aviones = select(Aviones)
  result = db.execute(aviones).scalars().all()
  return result

@router.post("/", response_model=AvionSchema)
def createAvion(avion:AvionSchema, db:Session = Depends(get_db)):
    # 1. Verificar si ya existe (usando select + execute)
    stmt = select(Aviones).where(Aviones.matricula == avion.matricula)
    existe = db.execute(stmt).scalars().first()
    if existe:
        raise HTTPException(status_code=400, detail="El avión ya esta registrado")

    # 2. Crear nuevo registro
    nuevo = Aviones(**avion.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # 3. Devolver el objeto serializado con schema
    return nuevo