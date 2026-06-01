from utils.db import Base
from sqlalchemy import Column
from sqlalchemy.types import TypeDecorator, String

class MatriculaType(TypeDecorator):
  impl = String

  def __init__(self, *args, **kwargs):
    super().__init__(lenght=6,*args, **kwargs)
    self.lenght = 6

  def process_bind_param(self, value, dialect):
    if value is None:
      raise ValueError("El campo matricula es obligatorio")
    
    value = value.upper()

    if len(value) != self.lenght:
      raise ValueError("La matricula tiene que tener 6 caracteres")
    
    return value
  
  def process_result_value(self, value, dialect):
      return value
  

class NotNullableType(TypeDecorator):
  impl = String

  def process_bind_param(self, value, dialect):
    if value is None:
      raise ValueError("El campo modelo no puede estar vacío")
    
    return value.upper()
  
  def process_result_value(self, value, dialect):
      return value
  
import re
from sqlalchemy.types import TypeDecorator, String

class ClaseType(TypeDecorator):
    impl = String

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Compilamos la regex para eficiencia
        self.pattern = re.compile(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ.,;:\'\"!?()¡¿-]+$')

    def process_bind_param(self, value, dialect):
        # No permitir nulos
        if value is None:
            raise ValueError("El campo clase no puede estar vacio")

        # Validar contra la expresión regular
        if not self.pattern.match(value):
            raise ValueError(
                "El campo clase no puede contener numeros ni espacios"
            )

        return value

    def process_result_value(self, value, dialect):
        return value


class Aviones(Base):
  __tablename__ = "aviones"

  matricula = Column(MatriculaType, primary_key=True, unique=True, nullable=False)
  modelo = Column(NotNullableType, nullable=False)
  potencia = Column(NotNullableType, nullable=False)
  clase = Column(ClaseType, nullable=False)