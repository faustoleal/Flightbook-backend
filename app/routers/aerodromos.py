from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.db import get_db
from models.aerodromos import Aerodromos
from schemas.aerodromos import AerodromoSchema

router = APIRouter(
  prefix="/aerodromos"
)

@router.get("/", response_model=list[AerodromoSchema])
def getAerodromos(db:Session = Depends(get_db)):
  aerodromos= select(Aerodromos)
  result = db.execute(aerodromos).scalars().all()
  return result

@router.post("/", response_model=AerodromoSchema)
def createAerodromo(aerodromo:AerodromoSchema, db:Session = Depends(get_db)):
  # 1. Verificar si ya existe (usando select + execute)
    stmt = select(Aerodromos).where(Aerodromos.aerodromo == aerodromo.aerodromo)
    existe = db.execute(stmt).scalars().first()
    if existe:
        raise HTTPException(status_code=400, message="El aeródromo ya existe")

    # 2. Crear nuevo registro
    nuevo = Aerodromos(**aerodromo.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # 3. Devolver el objeto serializado con schema
    return nuevo