from pydantic import BaseModel, field_validator

class AerodromoSchema(BaseModel):
  aerodromo: str
  ciudad: str

  @field_validator("aerodromo")

  def validar_aerodromo(cls,value):
    if value is None:
      raise ValueError("El aeródromo no puede ser nulo")
    
    value = value.upper()

    if not value.isalpha():
      raise ValueError("El aeródromo solo puede contener letras")
    
    if len(value) < 3 or len(value) > 4:
      raise ValueError("El aeródromo debe tener entre 3 y 4 letras")
    
    return value

  @field_validator("ciudad")

  def validar_ciudad(cls,value):
    if value is None:
      raise ValueError("La ciudad no puede ser nula")

    if len(value) < 3:
      raise ValueError("El nombre de la ciudad no puede ser tan corto")
  
  class Config:
    orm_mode = True