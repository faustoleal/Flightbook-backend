from pydantic import BaseModel, field_validator

class AerodromoSchema(BaseModel):
  aerodromo: str

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
  
  class Config:
    orm_mode = True