from pydantic import BaseModel, field_validator,Field
from datetime import date, time
from decimal import Decimal
from enum import Enum
from typing import Annotated
import re
from schemas import AvionSchema, ResponsePilotoSchema

class FinalidadEnum(str, Enum):
    ENT = "ENT"
    INST = "INST"
    READP = "READP"
    EXA = "EXA"


class HorasDeVueloSchema(BaseModel):
  dia: date
  hora_salida: time
  desde:str
  hasta:str
  hora_llegada: time
  finalidad: FinalidadEnum
  local_dia_p: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  local_dia_c: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  local_noche_p: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  local_noche_c: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  travesia_dia_p: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  travesia_dia_c: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  travesia_noche_p: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  travesia_noche_c: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  aterrizajes: int
  instructor_de_vuelo: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  reactor: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  multi_motor: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  turbo_helice: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  aeroaplicador: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  instrumentos_real_p: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  instrumentos_real_c: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]
  capota: Annotated[Decimal, Field(max_digits=2, decimal_places=1, ge=0, default=0)]

  @field_validator("desde")
  def validar_desde(cls,value):
     if value is None:
        raise ValueError("El aerodromo de salida no puede ser nulo.")
     if len(value) < 3 or len(value) > 4:
        raise ValueError("El aerodromo no puede tener menos de 3 caracteres o mayor a 4")
     return value
  
  @field_validator("hasta")
  def validar_desde(cls,value):
     if value is None:
        raise ValueError("El aerodromo de salida no puede ser nulo.")
     if len(value) < 3 or len(value) > 4:
        raise ValueError("El aerodromo no puede tener menos de 3 caracteres o mayor a 4")
     return value
  


class HorasDeVueloResponse(HorasDeVueloSchema):
  id: int
  avion_matricula: str
  piloto_id:int

  @field_validator("avion_matricula")
  def validar_avion_matricula(cls,value):
     if value is None:
        raise ValueError("La matrícula del avión es obligatoria.")
     if len(value) != 6:
        raise ValueError("El largo de la matrícula tiene que ser de 6 caractéres.")
     pattern = re.compile(r"^LV-[A-Z]{3}$")
     if not pattern.match(value):
        raise ValueError("La matricula debe respetar el siguiente formato LV-AAA")
     return value


class HorasDeVueloPorPilotoResponse(HorasDeVueloSchema):
   id:int
   avion: AvionSchema
   piloto: ResponsePilotoSchema

   class Config:
      orm_mode:True


class PaginationHorasResponse(BaseModel):
   content: list[HorasDeVueloPorPilotoResponse]
   totalPages: int

   class Config:
      orm_mode:True
