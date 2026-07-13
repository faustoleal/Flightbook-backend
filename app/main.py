from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from utils.db import Base, engine
from utils.middlewares import TokenExtractor
from routers import aerodromos, horas_de_vuelos, aviones, pilotos, login


Base.metadata.create_all(engine)

app = FastAPI()

origins = [
  "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # dominios permitidos
    allow_credentials=True,           # si usás cookies/autenticación
    allow_methods=["*"],              # métodos HTTP permitidos
    allow_headers=["*"],              # headers permitidos
)

@app.get("/")
async def root(request: Request):
  return {"token": request.state.token}

app.add_middleware(TokenExtractor)

app.include_router(aerodromos.router)
app.include_router(horas_de_vuelos.router)
app.include_router(aviones.router)
app.include_router(pilotos.router)
app.include_router(login.router)