from .aerodromos import AerodromoSchema
from .aviones import AvionSchema
from .pilotos import PilotoSchema, ResponsePilotoSchema, NewPilotoSchema
from .horas_de_vuelos import HorasDeVueloSchema, HorasDeVueloResponse, HorasDeVueloPorPilotoResponse, PaginationHorasResponse

__all__ = [
  "AerodromoSchema",
  "AvionSchema",
  "PilotoSchema",
  "ResponsePilotoSchema",
  "NewPilotoSchema",
  "HorasDeVueloSchema",
  "HorasDeVueloResponse",
  "HorasDeVueloPorPilotoResponse",
  "PaginationHorasResponse"
]