from fastapi import FastAPI
from utils.db import Base, engine
from routers import aerodromos

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
async def root():
  return "Hola mundo"

app.include_router(aerodromos.router)