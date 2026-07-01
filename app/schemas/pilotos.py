from pydantic import BaseModel, field_validator
import re

class PilotoSchema(BaseModel):
  name: str
  usuario: str

  @field_validator("name")
  def validar_name(cls,value):
    if value is None:
      raise ValueError("El campo nombre no puede estar vacio")
    if len(value) > 50:
      raise ValueError("El valor excede la longitud máxima de 50 caractéres.")
    pattern = re.compile(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$')
    if not pattern.match(value):
      raise ValueError("Solo se permiten letras y espacios.")
    return value
    
  @field_validator("usuario")
  def validar_usuario(cls,value):
    if value is None:
      raise ValueError("El usuario no puede ser nulo")
    return value
  

  
class NewPilotoSchema(PilotoSchema):
    password: str

    @field_validator("password")
    def validar_passwordHash(cls,value):
      if value is None:
        raise ValueError("Se necesita una contraseña")
      return value
    
    
class ResponsePilotoSchema(BaseModel):
    id:int
    name: str
    usuario: str

    class Config:
      orm_mode = True