from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.db import get_db
from models.horas_de_vuelo import HorasDeVuelo
from schemas.horas_de_vuelos import HorasDeVueloResponse 

router = APIRouter(prefix="/horas")

@router.get("/", response_model=list[HorasDeVueloResponse])
def getHoras(db:Session = Depends(get_db)):
  horas = select(HorasDeVuelo)
  result = db.execute(horas).scalars().all()
  return result