from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from models.aerodromos import Aerodromos

router = APIRouter(
  prefix="/aerodromos"
)

@router.get("/")
def getAerodromos(db:Session = Depends(get_db)):
  return db.query(Aerodromos).all()