from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, select, extract, union_all
from models import  HorasDeVuelo
from schemas.horas_de_vuelos import NuevaHoraRequest
from models.aviones import Aviones
from models.aerodromos import Aerodromos


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

def horas_de_vuelos_stats(db:Session,id:int):
  #horas totales
  totales = (HorasDeVuelo.local_dia_p + HorasDeVuelo.local_dia_c + HorasDeVuelo.local_noche_p + HorasDeVuelo.local_noche_c + HorasDeVuelo.travesia_dia_p + HorasDeVuelo.travesia_dia_c + HorasDeVuelo.travesia_noche_p + HorasDeVuelo.local_noche_c)

  # horas por año
  stmt_por_año = (
      select(
          extract("year", HorasDeVuelo.dia).label("año"),
          func.sum(totales).label("horas")
      )
      .where(HorasDeVuelo.piloto_id == id)
      .group_by(extract("year", HorasDeVuelo.dia))
  )
  horas_por_año = db.execute(stmt_por_año).all()

  # horas por avión
  stmt_por_avion = (
      select(
          Aviones,
          func.sum(totales).label("horas")
      )
      .join(HorasDeVuelo.avion)
      .where(HorasDeVuelo.piloto_id == id)
      .group_by(Aviones.matricula)
  )

  horas_por_avion = db.execute(stmt_por_avion).all()

  # destinos preferidos

  desde_q = (
        select(HorasDeVuelo.desde.label("destino"))
        .where(HorasDeVuelo.piloto_id == id)
    )

  hasta_q = (
        select(HorasDeVuelo.hasta.label("destino"))
        .where(HorasDeVuelo.piloto_id == id)
    )

  # Unimos ambas columnas en una sola lista
  union_q = union_all(desde_q, hasta_q).alias("destino_union")

  stmt_destinos = (
        select(
            Aerodromos,
            func.count().label("cantidad")
        )
        .select_from(union_q)
        .join(Aerodromos, Aerodromos.aerodromo == union_q.c.destino)
        .where(union_q.c.destino != "ATE")
        .group_by(Aerodromos.aerodromo)
        .order_by(func.count().desc())
        .limit(5)
    )

  destinos_preferidos = db.execute(stmt_destinos).all()

  return {
        "horas_por_año": [{"año": int(a), "horas": float(h)} for a, h in horas_por_año],
        "horas_por_avion": [{"avion":{
            "matricula": av.matricula,
            "modelo": av.modelo,
            "potencia": av.potencia,
            "clase": av.clase
        }, "horas": float(h)} for av, h in horas_por_avion],
        "destinos_preferidos": [{"destino": {
            "aerodromo": d.aerodromo,
            "ciudad": d.ciudad
        }, "cantidad": c} for d, c in destinos_preferidos]
    }

 