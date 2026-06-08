import re
from sqlalchemy.types import TypeDecorator, String, Date, Time, CHAR, INTEGER

class NotNullableType(TypeDecorator):
  impl = String

  def process_bind_param(self, value, dialect):
    if value is None:
      raise ValueError("El campo modelo no puede estar vacío")
    
    return value.upper()
  
  def process_result_value(self, value, dialect):
      if value is None:
            raise ValueError("Se encontró un valor nulo en la BD, lo cual no está permitido")
      return value
  
class NameType(TypeDecorator):
  impl= String

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
    if value is None:
            raise ValueError("El nombre del usuario no puede ser nulo en la BD")
    return value
  
class MatriculaType(TypeDecorator):
  impl = CHAR

  def __init__(self, *args, **kwargs):
    super().__init__(length=6,*args, **kwargs)
    self.length = 6

  def process_bind_param(self, value, dialect):
    if value is None:
      raise ValueError("El campo matricula es obligatorio")
    
    value = value.upper()

    if len(value) != self.length:
      raise ValueError("La matricula tiene que tener 6 caracteres")
    
    return value
  
  def process_result_value(self, value, dialect):
      if value is None:
            raise ValueError("La matricula del avión no puede ser nula en la BD")
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
        if value is None:
            raise ValueError("La clase del avión no puede ser nula en la BD")
        return value
    
class AerodromoType(TypeDecorator):
  impl = String

  def __init__(self,length=None, minLength=1, *args, **kwargs):
    super().__init__(length=length, *args, **kwargs)
    self.minLength = minLength
    self.maxLength = length
  
  def process_bind_param(self, value, dialect):
    if value is None:
      raise ValueError("El Aerodromo no puede ser nulo")
    
    value = value.upper()

    if not value.isalpha():
      raise ValueError(f"El aerodromo {value} solo puede contener letras")

    if len(value) < self.minLength or len(value) > self.maxLength:
      raise ValueError(f"El aerodromo no puede tener mas de 4 letras o menos de 3")
    
    return value
  

  def process_result_value(self, value, dialect):
    if value is None:
            raise ValueError("El aerodromo no puede ser nulo en la BD")
    return value
  
class NotNullDate(TypeDecorator):
    impl = Date

    def process_bind_param(self, value, dialect):
        if value is None:
            raise ValueError("Te olvidaste de poner el día del vuelo")
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            raise ValueError("El día de vuelo no puede ser nulo en la BD")
        return value
    
class NotNullTime(TypeDecorator):
    impl = Time

    def process_bind_param(self, value, dialect):
        if value is None:
            raise ValueError("La hora de salida o llegada es obligatoria")
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            raise ValueError("El horario de salida o llegada no puede ser nulo en la BD")
        return value
    
class AerodromoSalidaLlegadaTYpe(TypeDecorator):
    impl= String

    def __init__(self, *args, **kwargs):
        super().__init__(length=4, *args, **kwargs)
        self.min_length = 3
        self.max_length = 4
        # Regex: solo letras con acentos y ñ, sin espacios ni números
        self.pattern = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ]+$')
    
    def process_bind_param(self, value, dialect):
        if value is None:
            raise ValueError("El aeródromo de salida o llegada es obligatorio")

        if not self.pattern.match(value):
            raise ValueError("El aeródromo no puede contener espacios o números")

        if not (self.min_length <= len(value) <= self.max_length):
            raise ValueError("El aeródromo debe tener entre 3 y 4 letras")

        return value.upper()

    def process_result_value(self, value, dialect):
        if value is None:
            raise ValueError("El aeródromo no puede ser nulo en la BD")
        return value
    
class FinalidadType(TypeDecorator):
    impl = String

    def __init__(self, *args, **kwargs):
        super().__init__(length=10, *args, **kwargs)
        self.allowed = {"ENT", "INST", "READP", "EXA"}

    def process_bind_param(self, value, dialect):
        if value is None:
            raise ValueError("El campo finalidad es obligatorio")

        if value not in self.allowed:
            raise ValueError(f"Finalidad inválida: {value}. Debe ser uno de {self.allowed}")

        return value

    def process_result_value(self, value, dialect):
        if value is None:
            raise ValueError("El campo finalidad no puede ser nulo en la BD")
        return value

class NotNullAterrizaje(TypeDecorator):
    impl = INTEGER

    def process_bind_param(self, value, dialect):
        if value is None:
            raise ValueError("Tiene que poner los aterrizajes realizados")
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            raise ValueError("El número de aterrizajes no puede ser nulo en la BD")
        return value