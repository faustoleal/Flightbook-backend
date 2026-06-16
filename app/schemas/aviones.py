from pydantic import BaseModel, field_validator
import re

class AvionSchema(BaseModel):
  matricula: str
  modelo:str
  potencia:str
  clase:str

  @field_validator("matricula")
  def validar_matricula(cls,value):
    if value is None:
      raise ValueError("El campo matrícula es obligatorio")
    if len(value) != 6:
      raise ValueError("La matricula tiene que tener 6 caracteres")
    return value.upper()
  
  @field_validator("modelo")
  def valiar_modelo(cls,value):
    if value is None:
      raise ValueError("El campo modelo no puede estar vacío")
    return value.upper()
  
  @field_validator("potencia")
  def validar_potencia(cls,value):
    if value is None:
      raise ValueError("El campo potencia no puede estar vacío")
    return value.upper()
  
  @field_validator("clase")
  def validar_clase(cls,value):
    if value is None:
      raise ValueError("El campo clase no puede estar vacio")
    pattern = re.compile(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ.,;:\'\"!?()¡¿-]+$')
    if not pattern.match(value):
      raise ValueError("El campo clase no puede contener numeros ni espacios")
    return value
  
  class Config:
     orm_mode = True
  
