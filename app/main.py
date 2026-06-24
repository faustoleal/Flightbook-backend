from fastapi import FastAPI, Request
from utils.db import Base, engine
from utils.middelwares import TokenExtractor
from routers import aerodromos, horas_de_vuelos, aviones, pilotos


Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def root(request: Request):
  return {"token": request.state.token}

app.add_middleware(TokenExtractor)

app.include_router(aerodromos.router)
app.include_router(horas_de_vuelos.router)
app.include_router(aviones.router)
app.include_router(pilotos.router)