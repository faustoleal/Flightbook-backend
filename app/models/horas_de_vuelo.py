from utils.db import Base
from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from .custom_types import NotNullDate, NotNullTime, AerodromoSalidaLlegadaTYpe,FinalidadType, MatriculaType, NotNullAterrizaje

class HorasDeVuelo(Base):
  __tablename__ = "horas_de_vuelos"

  id= Column(Integer,primary_key=True, autoincrement=True)
  dia= Column(NotNullDate(), nullable=False)
  horaSalida= Column(NotNullTime(), nullable=False)
  desde= Column(AerodromoSalidaLlegadaTYpe(),ForeignKey("aerodromos.aerodromo"), nullable=False)
  hasta= Column(AerodromoSalidaLlegadaTYpe(),ForeignKey("aerodromos.aerodromo"), nullable=False)
  horaLlegada= Column(NotNullTime, nullable=False)
  finalidad= Column(FinalidadType(), nullable=False)
  avionMatricula= Column(MatriculaType(), ForeignKey("aviones.matricula"), nullable=False)
  localDiaP= Column(DECIMAL, default=0)
  localDiaC= Column(DECIMAL, default=0)
  localNocheP= Column(DECIMAL, default=0)
  localNocheC= Column(DECIMAL, default=0)
  travesiaDiaP= Column(DECIMAL, default=0)
  travesiaDiaC= Column(DECIMAL, default=0)
  travesiaNocheP= Column(DECIMAL, default=0)
  travesiaNocheC= Column(DECIMAL, default=0)
  aterrizajes= Column(NotNullAterrizaje(), default=1, nullable=False)
  instructorDeVuelo= Column(DECIMAL, default=0)
  reactor= Column(DECIMAL, default=0)
  multiMotor= Column(DECIMAL, default=0)
  turboHelice= Column(DECIMAL, default=0)
  aeroaplicador= Column(DECIMAL, default=0)
  instrumentosRealP= Column(DECIMAL, default=0)
  instrumentosRealC= Column(DECIMAL, default=0)
  capota= Column(DECIMAL, default=0)