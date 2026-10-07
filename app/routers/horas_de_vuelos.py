from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.db import get_db
from schemas import HorasDeVueloResponse, PaginationHorasResponse, HorasDeVuelosTotalesResponse, NuevaHoraRequest, HorasDeVuelosStats
from crud.horas_de_vuelos import get_all, horas_de_vuelo_por_piloto, horas_totales_del_piloto, crear_hora, horas_de_vuelos_stats

router = APIRouter(prefix="/api/horas")

@router.get("/", response_model=list[HorasDeVueloResponse])
def getHoras(db:Session = Depends(get_db)):
  return get_all(db)

@router.get("/{id}", response_model=PaginationHorasResponse)
def getHorasPorPiloto(id:int, page:int = 1, db:Session = Depends(get_db)):
  return horas_de_vuelo_por_piloto(db,page,id)

@router.get("/{id}/totales", response_model=HorasDeVuelosTotalesResponse)
async def getTotales(id:int, db:Session = Depends(get_db)):
  return horas_totales_del_piloto(db, id)

@router.get("/{id}/stats", response_model=HorasDeVuelosStats)
async def getStats(id:int, db:Session = Depends(get_db)):
  return horas_de_vuelos_stats(db, id)

@router.post("/", response_model=HorasDeVueloResponse)
def createHora(request:NuevaHoraRequest, db:Session = Depends(get_db)):
  return  crear_hora(db, request)