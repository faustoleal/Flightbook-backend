from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload
from utils.db import get_db
from models import HorasDeVuelo
from schemas import HorasDeVueloResponse, PaginationHorasResponse, HorasDeVuelosTotalesResponse

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

@router.get("/{id}/totales", response_model=HorasDeVuelosTotalesResponse)
async def getTotales(id:int, db:Session = Depends(get_db)):
    query = select(
            func.sum(
                HorasDeVuelo.local_dia_p + HorasDeVuelo.local_dia_c +
                HorasDeVuelo.travesia_dia_p + HorasDeVuelo.travesia_dia_c
            ).label("total_dia"),
            func.sum(
                HorasDeVuelo.local_noche_p + HorasDeVuelo.local_noche_c +
                HorasDeVuelo.travesia_noche_p + HorasDeVuelo.travesia_noche_c
            ).label("total_noche"),
            func.sum(
                HorasDeVuelo.local_dia_p + HorasDeVuelo.local_noche_p +
                HorasDeVuelo.local_noche_p + HorasDeVuelo.local_noche_c
            ).label("total_local"),
            func.sum(HorasDeVuelo.travesia_dia_p).label("total_travesia"),
            func.sum(
                HorasDeVuelo.local_dia_p + HorasDeVuelo.local_noche_p +
                HorasDeVuelo.travesia_dia_p + HorasDeVuelo.travesia_noche_p
            ).label("total_alMando"),
            func.sum(
                HorasDeVuelo.local_dia_c + HorasDeVuelo.local_noche_c +
                HorasDeVuelo.travesia_dia_c + HorasDeVuelo.travesia_noche_c +
                HorasDeVuelo.local_dia_p + HorasDeVuelo.local_noche_p +
                HorasDeVuelo.travesia_dia_p + HorasDeVuelo.travesia_noche_p
            ).label("total_horas"),
            func.sum(HorasDeVuelo.aterrizajes).label("total_aterrizajes"),
        ).where(HorasDeVuelo.piloto_id == id)
    
    result = db.execute(query)
    totales = result.mappings().first()

    if not totales:
      return HTTPException(status_code=404, detail="No hay horas registradas")
    
    return totales