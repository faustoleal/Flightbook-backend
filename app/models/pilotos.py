from utils.db import Base
from sqlalchemy import Column, Integer
from .custom_types import NameType, NotNullableType


class Pilotos(Base):
  __tablename__ = "pilotos"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(NameType(), nullable=False)
  usuario = Column(NotNullableType(), nullable=False, unique=True)
  password_hash = Column(NotNullableType(), nullable=False)