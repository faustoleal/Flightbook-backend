from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from utils.db import get_db
from models import HorasDeVuelo
from schemas import HorasDeVueloResponse, PaginationHorasResponse

router = APIRouter(prefix="/horas")

@router.get("/", response_model=list[HorasDeVueloResponse])
def getHoras(db:Session = Depends(get_db)):
  horas = select(HorasDeVuelo)
  result = db.execute(horas).scalars().all()
  return result

@router.get("/{id}", response_model=PaginationHorasResponse)
def getHorasPorPiloto(id:int, page:int = 1, db:Session = Depends(get_db)):
  limit = 15
  offset = (page - 1) * limit if page > 0 else 0

  smt = (
    select(HorasDeVuelo)
    .where(HorasDeVuelo.piloto_id == id)
    .order_by(HorasDeVuelo.dia.asc())
    .options(
       joinedload(HorasDeVuelo.avion),
       joinedload(HorasDeVuelo.piloto)
    )
    .limit(limit)
    .offset(offset)
    )
  
  result = db.execute(smt).scalars().all()
  total = db.execute(
    select(func.count(HorasDeVuelo.id)).where(HorasDeVuelo.piloto_id == id)).scalar()

  return {
    "content": result,
    "totalPages": (total + limit -1) // limit
  }