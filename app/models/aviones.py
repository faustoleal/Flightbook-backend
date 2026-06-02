from utils.db import Base
from sqlalchemy import Column
from custom_types import MatriculaType, NotNullableType, ClaseType

class Aviones(Base):
  __tablename__ = "aviones"

  matricula = Column(MatriculaType, primary_key=True, unique=True, nullable=False)
  modelo = Column(NotNullableType, nullable=False)
  potencia = Column(NotNullableType, nullable=False)
  clase = Column(ClaseType, nullable=False)