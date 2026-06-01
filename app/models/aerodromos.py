from utils.db import Base
from sqlalchemy import Column
from sqlalchemy.types import TypeDecorator, String


class AerodromoType(TypeDecorator):
  impl = String

  def __init__(self,lenght=None, minLenght=1, *args, **kwargs):
    super().__init__(lenght=lenght, *args, **kwargs)
    self.minLenght = minLenght
    self.maxLenght = lenght
  
  def process_bind_param(self, value, dialect):
    if value is None:
      raise ValueError("El Aerodromo no puede ser nulo")
    
    value = value.upper()

    if not value.isalpha():
      raise ValueError(f"El aerodromo {value} solo puede contener letras")

    if len(value) < self.minLenght or len(value) > self.maxLenght:
      raise ValueError(f"El aerodromo no puede tener mas de 4 letras o menos de 3")
    
    return value
  

  def process_result_value(self, value, dialect):
    return value

class Aerodromos(Base):
  __tablename__ = "aerodromos"

  aerodromo = Column(AerodromoType(4, minLenght=3),primary_key=True, nullable=False)

