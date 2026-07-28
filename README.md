# FligthBook Backend

## Descripción

FlightBook es un backend realizado con Python + FastAPI que se conecta con un frontend hecho con React + Redux. Este sirve para llevar un registro ordenado de las horas de vuelo que tiene un piloto de avión y los tipos de aviones que vuela.

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

## Funcionalidades

- **Vistas:** inico, listado de productos (filtro + pagination), producto detallado (con productos relacionados por marca), contacto, login , register, carrito y panel de adminstración.
- **Contacto:** cuando el formulario de contacto se envia, el administrador recibe el mail con la consulta realizada.
- **Creación de usuarios:** con bycpry para el guardado seguro del password.
- **Autenticación:** JWT para login seguro y persistencia de sesión.
- **Carrito de compras:** CRUD completa, sincronización entre el frontend y backend, simulación de compra + envio de email de confirmación de pedido.
- **Rol admin:** si posees el rol de amdinistrador, puedes: ver los pedidos que se realizaron y modificar su estatus, y también ver los productos que tenes, crear uno nuevo, modificar la cantidad en stock o eliminar uno.

## Endpoints

- Vistas frontend:
  1. "/": vista home.
  2. "/productos": listado de productos.
  3. "/productos/:id": producto detallado.
  4. "/carrito": carrito de compras.
  5. "/admin": vista del panel de administrador.
  6. "/login": vista para logearse.
  7. "/register": página para crear usuario.

- Endpoint del backend:
  1. "/api/carrito/:id":
     - GET ──> Obtener el carrito de un usario en particular.
     - DELETE ──> Limpiar el carrito.
  2. "/api/carrito/:id/:productoId":
     - DELETE ──> Eliminar item del carrito.
     - PUT ──> Modificar cantidad de un item.
  3. "/api/login":
     - POST ──> Login de usuarios.
  4. "/api/pedidos":
     - GET ──> Obtener pedidos.
     - POST ──> Realizar un nuevo pedido.
  5. "/api/pedidos/:id":
     - PUT ──> Editar el status de un pedido.
  6. "/api/phones":
     - GET ──> Obtener listado de smartphones.
     - POST ──> Agregar nuevo smartphone al listado.
  7. "/api/phones/:id":
     - GET ──> Obtener un celular.
  8. "/api/phones/destacados":
     - GET ──> Trae tres productos destacados de las marca Apple, Samsung y Xiaomi.
  9. "/api/phones/relacionados/:brand":
     - GET ──> Trae tres productos relacionas a la marca del celular que se encuentra en la vista /producto/:id.
  10. "/api/user":
      - GET ──> Obtener lista de usuarios.
      - POST ──> Crear nuevo usuario.
  11. "/api/user/:id":
      - GET ──> Obtener usuario.

## Estructura de carpetas

```
ecommerce-phones/
├── src/
│   ├── app/
│   │   ├── admin/page.tsx
│   │   ├── api/
|   |   |   ├── carrito/[id]
|   |   |   |   ├──[productoId]
|   |   |   |   |  └── route.ts
|   |   |   |   └── route.ts
|   |   |   ├── login/
|   |   |   |   └──route.ts
|   |   |   ├── pedidos/
|   |   |   |   ├── [id]
|   |   |   |   |   └── route.ts
|   |   |   |   └── route.ts
|   |   |   ├── phones/
|   |   |   |   ├──[id]
|   |   |   |   |  └── route.ts
|   |   |   |   ├── destacados/
|   |   |   |   |   └── route.ts
|   |   |   |   ├── relacionados/
|   |   |   |   |   └── route.ts
|   |   |   |   └── route.ts
|   |   |   ├── user/
|   |   |   |   ├── [id]
|   |   |   |   |   └── route.ts
|   |   |   |   └── route.ts
|   |   |   └── route.ts
|   |   ├── carrito/page.tsx
|   |   ├── login/pages.tsx
|   |   ├── productos/
|   |   |   ├── [id]/page.tsx
|   |   |   └── page.tsx
|   |   ├── register/page.tsx
|   |   ├── favicon.ico
|   |   ├── globals.css
|   |   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
|   |   ├── admin/
|   |   |   ├── CreateForm.tsx
|   |   |   ├── PedidosTable.tsx
|   |   |   ├── ProductosTable.tsx
|   |   |   └── StatusSelect.tsx
|   |   ├── carrito/
|   |   |   ├── NotContentCarrito.tsx
|   |   |   └── NotUserCarrito.tsx
|   |   ├── display/
|   |   |   ├── Card.tsx
|   |   |   ├── Modal.tsx
|   |   |   └── Table.tsx
|   |   ├── feedback/
|   |   |   ├── Toaster.tsx
|   |   |   └── ToasterContainer.tsx
|   |   ├── forms/
|   |   |   ├── CreateAccountForm.tsx
|   |   |   └── LoginForm.tsx
|   |   ├── layout/
|   |   |   ├── DropdownMenu.tsx
|   |   |   ├── Footer.tsx
|   |   |   ├── MobileMenu.tsx
|   |   |   └── Navbar.tsx
|   |   ├── productos/
|   |   |   ├── Destacados.tsx
|   |   |   ├── DestacadosSection.tsx
|   |   |   ├── FiltroSection.tsx
|   |   |   ├── PhoneList.tsx
|   |   |   ├── PhoneSection.tsx
|   |   |   └── Relacionados.tsx
|   |   ├── ui/
|   |   |   ├── Button.tsx
|   |   |   ├── Input.tsx
|   |   |   ├── Label.tsx
|   |   |   ├── Pagination.tsx
|   |   |   ├── RatingEstrellas.tsx
|   |   |   ├── Select.tsx
|   |   |   └── Textarea.tsx
|   |   └── views/
|   |       ├── AdminPage.tsx
|   |       ├── CarritoPage.tsx
|   |       ├── ContactoPage.tsx
|   |       ├── HomePage.tsx
|   |       ├── LoginPage.tsx
|   |       ├── ProductosByIdPage.tsx
|   |       ├── ProductosPage.tsx
|   |       └── RegisterPage.tsx
|   ├── context/
|   |   ├── authFunction.ts
|   |   ├── cartFunction.ts
|   |   ├── PedidosContext.tsx
|   |   ├── ToastContext.tsx
|   |   └── UserContext.tsx
|   ├── controllers/
|   |   ├── carrito.ts
|   |   ├── login.ts
|   |   ├── pedidos.ts
|   |   ├── phones.ts
|   |   └── user.ts
|   ├── lib/
|   |   ├── db.ts
|   |   └── mailer.ts
|   ├── models/
|   |   ├── index.ts
|   |   ├── pedidos.ts
|   |   ├── phones.ts
|   |   └── user.ts
|   ├── services/
|   |   ├── carritoService.ts
|   |   ├── pedidoService.ts
|   |   ├── phonesService.ts
|   |   └── userService.ts
|   └── types/
|       ├── pedidos.ts
|       ├── phones.ts
|       └── user.ts
├── .gitignore
├── README.md
├── eslint.config.mjs
├── next.config.ts
├── package-lock.json
├── package.json
├── postcss.config.mjs
└── tsconfig.json
```

## Autor

- Fausto Leal
- [Perfil de Github](https://github.com/faustoleal)
- [Perfil de LinkedIn](https://www.linkedin.com/in/fausto-leal-/)
