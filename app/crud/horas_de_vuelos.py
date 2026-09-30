from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, select
from models import  HorasDeVuelo
from schemas.horas_de_vuelos import NuevaHoraRequest


def get_all(db:Session):
  return db.query(HorasDeVuelo).all()

def horas_de_vuelo_por_piloto(db:Session, id:int, page:int=1, limit:int = 15):
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
    "totalPages": (total + limit - 1) // limit + 1
  }

def horas_totales_del_piloto(db:Session, id:int):
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

def crear_hora(db:Session, request:NuevaHoraRequest):
    # 1. Verificar que el formulario este completo
        if not request.nuevaHora:
           raise HTTPException(status_code=401, detail="No se registro una nueva hora")
        
        if not request.pilotoId:
           raise HTTPException(status_code=401, detail="El id del piloto es necesario")
    
        # Crear nueva hora de vuelo
    
        nueva_hora = HorasDeVuelo(
           piloto_id= request.pilotoId,
           **request.nuevaHora.model_dump()
        )
    
        # 2. Crear nuevo registro
        db.add(nueva_hora)
        db.commit()
        db.refresh(nueva_hora)
    
        # 3. Devolver el objeto serializado con schema
        return nueva_hora