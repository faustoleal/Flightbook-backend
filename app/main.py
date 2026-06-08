from fastapi import FastAPI
from utils.db import Base, engine
from routers import aerodromos, horas_de_vuelos

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def root():
  return "Hola mundo"

app.include_router(aerodromos.router)
app.include_router(horas_de_vuelos.router)