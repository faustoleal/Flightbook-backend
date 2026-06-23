from utils.db import Base
from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from .custom_types import NotNullDate, NotNullTime, AerodromoSalidaLlegadaTYpe,FinalidadType, MatriculaType, NotNullAterrizaje

class HorasDeVuelo(Base):
  __tablename__ = "horas_de_vuelos"

  id= Column(Integer,primary_key=True, autoincrement=True)
  dia= Column(NotNullDate(), nullable=False)
  hora_salida= Column(NotNullTime(), nullable=False)
  desde= Column(AerodromoSalidaLlegadaTYpe(),ForeignKey("aerodromos.aerodromo"), nullable=False)
  hasta= Column(AerodromoSalidaLlegadaTYpe(),ForeignKey("aerodromos.aerodromo"), nullable=False)
  hora_llegada= Column(NotNullTime, nullable=False)
  finalidad= Column(FinalidadType(), nullable=False)
  avion_matricula= Column(MatriculaType(), ForeignKey("aviones.matricula"), nullable=False)
  local_dia_p= Column(DECIMAL, default=0)
  local_dia_c= Column(DECIMAL, default=0)
  local_noche_p= Column(DECIMAL, default=0)
  local_noche_c= Column(DECIMAL, default=0)
  travesia_dia_p= Column(DECIMAL, default=0)
  travesia_dia_c= Column(DECIMAL, default=0)
  travesia_noche_p= Column(DECIMAL, default=0)
  travesia_noche_c= Column(DECIMAL, default=0)
  aterrizajes= Column(NotNullAterrizaje(), default=1, nullable=False)
  instructor_de_vuelo= Column(DECIMAL, default=0)
  reactor= Column(DECIMAL, default=0)
  multi_motor= Column(DECIMAL, default=0)
  turbo_helice= Column(DECIMAL, default=0)
  aeroaplicador= Column(DECIMAL, default=0)
  instrumentos_real_p= Column(DECIMAL, default=0)
  instrumentos_real_c= Column(DECIMAL, default=0)
  capota= Column(DECIMAL, default=0)
  piloto_id = Column(Integer,ForeignKey("pilotos.id"),nullable=False ,default=1)

  avion = relationship("Aviones", backref="horas_de_vuelo")
  piloto = relationship("Pilotos", backref="horas_de_vuelo")