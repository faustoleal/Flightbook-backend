from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from models.pilotos import Pilotos

router = APIRouter(prefix="/pilotos")

@router.get("/")
def getPilotos(db:Session = Depends(get_db)):
  return db.query(Pilotos).all()