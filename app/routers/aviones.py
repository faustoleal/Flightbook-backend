from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from models.aviones import Aviones

router = APIRouter(prefix="/aviones")

@router.get("/")
def getAviones(db:Session = Depends(get_db)):
  return db.query(Aviones).all()