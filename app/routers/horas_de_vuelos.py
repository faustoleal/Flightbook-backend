from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from models.horas_de_vuelo import HorasDeVuelo

router = APIRouter(prefix="/horas")

@router.get("/")
def getHoras(db:Session = Depends(get_db)):
  return db.query(HorasDeVuelo).all()