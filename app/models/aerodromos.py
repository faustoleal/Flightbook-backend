from utils.db import Base
from sqlalchemy import Column
from .custom_types import AerodromoType

class Aerodromos(Base):
  __tablename__ = "aerodromos"

  aerodromo = Column(AerodromoType(4, minLength=3),primary_key=True, nullable=False)

