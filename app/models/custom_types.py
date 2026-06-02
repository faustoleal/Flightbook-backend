import re
from sqlalchemy.types import TypeDecorator, String, Integer 

class NotNullableType(TypeDecorator):
  impl = String

  def process_bind_param(self, value, dialect):
    if value is None:
      raise ValueError("El campo modelo no puede estar vacío")
    
    return value.upper()
  
  def process_result_value(self, value, dialect):
      return value
  
class NameType(TypeDecorator):
  impl: String

  def __init__(self, *args, **kwargs):
      super().__init__(length=50,*args, **kwargs)
      self.max_length = 50
      self.pattern = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')

  def process_bind_param(self, value, dialect):
    if value is None:
      raise ValueError("El campo nombre no puede estar vacio")
    
    if len(value) > self.max_length:
      raise ValueError(f"El valor excede la longitud máxima de {self.max_length} caracteres.")
    
    if not self.pattern.match(value):
      raise ValueError("Solo se permiten letras y espacios.")
    
    return value
  
  def process_result_value(self, value, dialect):
    return super().process_result_value(value, dialect)
  
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