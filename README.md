# FligthBook Backend

## Descripción

FlightBook es un backend realizado con Python + FastAPI que se conecta con un frontend hecho con React + Redux. Este sirve para llevar un registro ordenado de las horas de vuelo que tiene un piloto de avión, los tipos de aviones que vuela y los aerodromos/aeropuertos a donde vuela

## Tecnologías

- **Backend:** Python, FastAPI
- **Base de datos:** PostgresSQL
- **Otros:** SQLAlchemy, bycrpt, python-jose, python-dotenv, pydantic

## Archivo .env

```
 <!-- Tienes que agregar este archivo para que la app funcione -->

  DATABASE_URL= tu-base-de-datos-postgres

  SECRET = una-clave-secreta-para-bycrpt

  ALGORITHM= para-jwt.encode
```

## Ejecución

- Inicia la app:

  ```
  fastapi dev
  ```

  El backend corre en `http://127.0.0.1:8000`.


## Endpoints

- Endpoint del backend:
  1. "/api/pilotos":
     - GET ──> Obtener el listado de pilotos registrados.
     - POST ──> Registran un nuevo piloto.
  2. "/api/pilotos/:id":
     - GET ──> Obtener un piloto registrado.
  3. "/api/login":
     - POST ──> Login de piloto.
  4. "/api/aerodromos":
     - GET ──> Obtener el listado de aerodromos.
     - POST ──> Agregar un aerodromo al listado.
  5. "/api/aviones":
     - PUT ──> Editar el status de un pedido.
  6. "/api/aviones":
     - GET ──> Obtener listado de aviones.
     - POST ──> Agregar un nuevo avión al listado.
  7. "/api/horas":
      - GET ──> Obtener listado de todas las horas de vuelo registradas en el backend.
      - POST ──> Crear una nueva hora de vuelo.
  8. "/api/horas/:id?page=num":
      - GET ──> Obtener el listado de todas las horas de vuelo de un piloto divido por páginas de  15 horas cada una.
  9. "/api/horas/:id/totales":
     - GET ──> Trae los totales de horas de un piloto por categoría.

## Estructura de carpetas

```
flight-book-backend-python/
├── src/
    ├── app/
    │   │   ├── models/
    |   |   ├── __init__.py
    |   |   ├── aerodromos.py
    |   |   ├── aviones.py
    |   |   ├── custom_types.py
    |   |   ├── horas_de_vuelo_py
    |   |   └── pilotos.py
    |   ├── routers/
    |   |   ├── __init__.py
    |   |   ├── aerodromos.py
    |   |   ├── aviones.py
    |   |   ├── horas_de_vuelo.py
    |   |   ├── login.py
    |   |   └── pilotos.py
    |   ├── schemas/
    |   |   ├── __init__.py
    |   |   ├── aerodromos.py
    |   |   ├── aviones.py
    |   |   ├── horas_de_vuelo.py
    |   |   ├── login.py
    |   |   └── pilotos.py
    │   └── utils/
    |   |   ├── config.py
    |   |   ├── db.py
    |   |   └── middlewares.py
    ├── main.py
    ├── .env
    ├── .gitignore
    └── README.md
```

## Autor

- Fausto Leal
- [Perfil de Github](https://github.com/faustoleal)
- [Perfil de LinkedIn](https://www.linkedin.com/in/fausto-leal-/)
