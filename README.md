# 🪨 Rock Samples API - Backend Dockerizado

Una API REST moderna y asincrónica para gestionar un registro completo de muestras geológicas de rocas. Diseñada como backend escalable y containerizado para sistemas de catalogación de especímenes geológicos.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-336791?style=for-the-badge&logo=database&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)
![asyncpg](https://img.shields.io/badge/asyncpg-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Uso de la API](#uso-de-la-api)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints Disponibles](#endpoints-disponibles)
- [Ejemplos de Requests](#ejemplos-de-requests)
- [Desarrollo Local](#desarrollo-local)
- [Notas Técnicas](#notas-técnicas)

---

## Características

- **CRUD Completo** para Rocas, Ubicaciones y Muestras
- **Arquitectura Asincrónica** con FastAPI y SQLModel async
- **Validación Automática** de esquemas con Pydantic
- **UUIDs Únicos** para todas las entidades
- **Timestamps Automáticos** (created_at, updated_at)
- **Relaciones Many-to-Many** entre tablas
- **Auto-creación de Entidades** mediante patrones get-or-create
- **CORS Configurado** para interoperabilidad con frontends
- **Documentación Interactiva** con Swagger UI y ReDoc
- **Database Logging** para debugging
- **Carga Inicial de Datos** desde CSV
- **Containerizado con Docker** para deployment inmediato
- **NGINX Reverse Proxy** para gestión de tráfico

---

## Arquitectura del Sistema

```plaintext
┌─────────────────────────────────────────────────┐
│          Cliente HTTP (Navegador/App)           │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   NGINX (Puerto 80)    │
        │   Reverse Proxy        │
        └────────┬───────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │  FastAPI (Puerto 8000) │
        │   Uvicorn ASGI Server  │
        │                        │
        │ - Routes               │
        │ - Services             │
        │ - Models               │
        └────────┬───────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │  PostgreSQL (5432)     │
        │   (Solo acceso interno)│
        └────────────────────────┘
```

### Flujo de Datos

```plaintext
HTTP Request (Puerto 80 NGINX)
    ↓
NGINX redirige a FastAPI (Puerto 8000 - interno)
    ↓
Route Handler (routes.py)
    ↓
Service Layer (service.py - Lógica de negocio)
    ↓
SQLModel → PostgreSQL (asyncpg)
    ↓
Schema Validation (schemas.py)
    ↓
JSON Response → NGINX → Cliente
```

---

## Requisitos Previos

- **Docker** ≥ 20.10
- **Docker Compose** ≥ 1.29
- **Git** (para clonar el repositorio)

> **Nota:** No necesitas Python ni PostgreSQL instalados localmente. Todo está containerizado.

---

## Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <tu-repositorio>
cd rocks-back-dockerized
```

### 2. Verificar Docker y Docker Compose

```bash
docker --version          # Verifica Docker
docker-compose --version  # Verifica Docker Compose
```

Si no están instalados, descarga [Docker Desktop](https://www.docker.com/products/docker-desktop).

### 3. Verificar Variables de Entorno

#### Backend (`app/.env`)

Verifica que el archivo exista y contenga:

```env
POSTGRES_URL=postgresql+asyncpg://rocks_user:rocks_password@postgres:5432/rocks_db
```

> **⚠️ Importante:** El host es `postgres` (nombre del servicio Docker), no `localhost`.

Si el archivo no existe, créalo:

```bash
cat > app/.env << EOF
POSTGRES_URL=postgresql+asyncpg://rocks_user:rocks_password@postgres:5432/rocks_db
EOF
```

#### Docker Compose (`docker-compose.yml`)

Verifica que las variables de PostgreSQL coincidan:

```yaml
services:
  postgres:
    environment:
      POSTGRES_USER: rocks_user
      POSTGRES_PASSWORD: rocks_password
      POSTGRES_DB: rocks_db
```

Deben coincidir con la URL en `app/.env`.

### 4. Construir y Levantar la Aplicación

```bash
# Opción 1: Construir y ejecutar en primer plano (ver logs)
docker-compose up --build

# Opción 2: Ejecutar en segundo plano (-d = detached)
docker-compose up -d --build
```

**Primera ejecución:** Puede tomar 2-3 minutos mientras Docker:

- Descarga imágenes base (Python, PostgreSQL, NGINX)
- Instala dependencias Python
- Compila la imagen del backend
- Inicializa PostgreSQL
- Crea tablas automáticamente
- Carga datos desde `app/src/datos_rocas.csv`

**Espera ver en los logs:**

```plaintext
postgres_1  | [1] LOG:  database system is ready to accept connections
backend_1   | INFO:     Uvicorn running on http://0.0.0.0:8000
nginx_1     | [notice] master process started
```

### 5. Verificar que Todo Funciona

```bash
# Ver estado de contenedores
docker-compose ps

# Output esperado:
# NAME                  COMMAND                  STATUS
# rocks_postgres_1      docker-entrypoint...     Up 2 minutes
# rocks_backend_1       python runserver.py      Up 2 minutes
# rocks_nginx_1         nginx -g daemon off      Up 2 minutes
```

### 6. Acceder a la API

Abre en tu navegador:

| Componente | URL | Descripción |
| ----------- | ----- | ------------- |
| **API Swagger** | http://localhost/api/docs | Documentación interactiva |
| **API ReDoc** | http://localhost/api/redoc | Documentación alternativa |
| **Base de Datos** | localhost:5432 | PostgreSQL (conexión interna) |

---

## Uso de la API

### Opción 1: Swagger UI (Recomendado)

1. Abre http://localhost/api/docs
2. Expande los endpoints que quieras probar
3. Haz clic en "Try it out"
4. Modifica los parámetros si es necesario
5. Haz clic en "Execute"

### Opción 2: ReDoc (Solo lectura)

1. Abre http://localhost/api/redoc
2. Navega por la documentación
3. Copia ejemplos de requests

### Opción 3: curl desde terminal

```bash
# Obtener todas las rocas
curl http://localhost/api/rocks

# Crear una roca (ver ejemplos abajo)
curl -X POST http://localhost/api/rocks \
  -H "Content-Type: application/json" \
  -d '{"name":"Granito","description":"Roca ígnea"}'
```

### Opción 4: Postman o Insomnia

1. Descarga [Postman](https://www.postman.com/downloads/) o [Insomnia](https://insomnia.rest/download)
2. Importa la URL: http://localhost/api/openapi.json
3. Prueba los endpoints

---

## Estructura del Proyecto

```plaintext
rocks-back-dockerized/
├── docker-compose.yml              # Orquestación de servicios
├── README.md                       # Este archivo
├── app/                            # Backend FastAPI
│   ├── .env                        # Variables de entorno
│   ├── Dockerfile                  # Construcción imagen Python
│   ├── requirements.txt            # Dependencias Python
│   ├── runserver.py                # Punto de entrada (uvicorn)
│   ├── README.md                   # README específico del backend
│   └── src/
│       ├── __init__.py             # App FastAPI + routers + CORS
│       ├── config.py               # Configuración (variables de entorno)
│       ├── datos_rocas.csv         # Datos iniciales para seed
│       ├── load_initial_data.py    # Script de carga de datos
│       ├── db/
│       │   ├── __init__.py
│       │   ├── main.py             # Engine async, init_db, get_session
│       │   └── models.py           # SQLModel: Rocks, Locations, Samples
│       ├── rocks/
│       │   ├── __init__.py
│       │   ├── routes.py           # GET/POST/PUT/DELETE /rocks
│       │   ├── service.py          # RockService (lógica CRUD)
│       │   └── schemas.py          # Validación Pydantic
│       ├── locations/
│       │   ├── __init__.py
│       │   ├── routes.py           # GET/POST/PUT/DELETE /locations
│       │   ├── service.py          # LocationService
│       │   └── schemas.py
│       └── samples/
│           ├── __init__.py
│           ├── routes.py           # GET/POST/PUT/DELETE /samples
│           ├── service.py          # SampleService (get_or_create)
│           └── schemas.py
└── nginx/                          # Proxy inverso
    ├── Dockerfile                  # Construcción imagen NGINX
    └── nginx.conf                  # Configuración del proxy
```

### Capas de Arquitectura

```plaintext
Routes (HTTP Endpoints)
    ↓
Services (Lógica de negocio)
    ↓
Models (Interacción con BD)
    ↓
Database (PostgreSQL)
    ↓
Schemas (Validación & Response)
```

---

## Endpoints Disponibles

### 🪨 Rocks (Rocas)

| Método | Endpoint | Descripción | Response |
| -------- | ---------- | ------------- | ---------- |
| **GET** | `/api/rocks` | Obtener todas las rocas | Array de rocas |
| **GET** | `/api/rocks/{rock_id}` | Obtener una roca por UUID | Objeto roca |
| **POST** | `/api/rocks` | Crear nueva roca | Objeto creado (201) |
| **PUT** | `/api/rocks/{rock_id}` | Actualizar roca | Objeto actualizado |
| **DELETE** | `/api/rocks/{rock_id}` | Eliminar roca | Sin contenido (204) |

### 📍 Locations (Ubicaciones)

| Método | Endpoint | Descripción |
| -------- | ---------- | ------------- |
| **GET** | `/api/locations` | Obtener todas las ubicaciones |
| **GET** | `/api/locations/{location_id}` | Obtener una ubicación |
| **POST** | `/api/locations` | Crear ubicación |
| **PUT** | `/api/locations/{location_id}` | Actualizar ubicación |
| **DELETE** | `/api/locations/{location_id}` | Eliminar ubicación |

### 🧪 Samples (Muestras)

| Método | Endpoint | Descripción |
| -------- | ---------- | ------------- |
| **GET** | `/api/samples` | Obtener todas las muestras |
| **GET** | `/api/samples/{sample_id}` | Obtener una muestra |
| **POST** | `/api/samples` | Crear muestra (auto-crea rock/location) |
| **PUT** | `/api/samples/{sample_id}` | Actualizar muestra |
| **DELETE** | `/api/samples/{sample_id}` | Eliminar muestra |

---

## Ejemplos de Requests

### ✅ Crear una Roca

```bash
curl -X POST http://localhost/api/rocks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Granito",
    "description": "Roca ígnea plutónica con textura granular y feldespatos"
  }'
```

**Response (201 Created):**

```json
{
  "uid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Granito",
  "description": "Roca ígnea plutónica con textura granular y feldespatos",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### ✅ Obtener todas las Rocas

```bash
curl http://localhost/api/rocks
```

**Response (200 OK):**

```json
[
  {
    "uid": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Granito",
    "description": "Roca ígnea plutónica...",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  {
    "uid": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Basalto",
    "description": "Roca volcánica oscura...",
    "created_at": "2024-01-15T10:35:00",
    "updated_at": "2024-01-15T10:35:00"
  }
]
```

### ✅ Crear una Ubicación

```bash
curl -X POST http://localhost/api/locations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Córdoba",
    "country": "Argentina"
  }'
```

**Response (201 Created):**

```json
{
  "uid": "660e8400-e29b-41d4-a716-446655440001",
  "name": "Córdoba",
  "country": "Argentina",
  "created_at": "2024-01-15T10:35:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

### ✅ Crear una Muestra (La más importante)

> **💡 Nota:** La muestra **auto-crea** rocas y ubicaciones si no existen. Solo necesitas proporcionar sus nombres.

```bash
curl -X POST http://localhost/api/samples \
  -H "Content-Type: application/json" \
  -d '{
    "rock_name": "Basalto",
    "description": "Roca volcánica oscura de grano fino",
    "location_name": "Islas Galápagos",
    "location_country": "Ecuador",
    "cut": true,
    "thin_section": true,
    "picture": "https://ejemplo.com/fotos/basalto_001.jpg"
  }'
```

**Response (201 Created):**

```json
{
  "uid": "770e8400-e29b-41d4-a716-446655440002",
  "cut": true,
  "thin_section": true,
  "picture": "https://ejemplo.com/fotos/basalto_001.jpg",
  "created_at": "2024-01-15T10:40:00",
  "updated_at": "2024-01-15T10:40:00",
  "rock_name": "Basalto",
  "rock_description": "Roca volcánica oscura de grano fino",
  "location_name": "Islas Galápagos",
  "location_country": "Ecuador"
}
```

### ✅ Actualizar una Roca

```bash
curl -X PUT http://localhost/api/rocks/550e8400-e29b-41d4-a716-446655440000 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Granito Rojo",
    "description": "Granito de alta densidad con feldespatos rojizos"
  }'
```

**Response (200 OK):**

```json
{
  "uid": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Granito Rojo",
  "description": "Granito de alta densidad con feldespatos rojizos",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T11:00:00"
}
```

### ✅ Eliminar una Roca

```bash
curl -X DELETE http://localhost/api/rocks/550e8400-e29b-41d4-a716-446655440000
```

**Response (204 No Content):**

```plaintext
(Sin cuerpo, solo headers)
```

---

## Desarrollo Local

### Ejecutar en Desarrollo con Python Local

Si tienes Python ≥ 3.10 instalado localmente:

#### 1. Crear entorno virtual

```bash
cd app
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

#### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 3. Levantar solo PostgreSQL en Docker

```bash
# En otra terminal, desde la raíz del proyecto
docker-compose up -d postgres
```

#### 4. Crear `.env` con localhost

```env
POSTGRES_URL=postgresql+asyncpg://rocks_user:rocks_password@localhost:5432/rocks_db
```

#### 5. Ejecutar el servidor

```bash
python runserver.py
```

La API estará disponible en http://localhost:8000

---

### Ejecutar Todo con Docker Compose

```bash
# Desde la raíz del proyecto
docker-compose up --build
```

---

## Notas Técnicas

### 🔄 Auto-creación de Entidades (Get-or-Create)

En el servicio de muestras ([`SampleService`](app/src/samples/service.py)), los métodos:

- [`get_or_create_rock()`](app/src/samples/service.py)
- [`get_or_create_location()`](app/src/samples/service.py)

Permiten crear una muestra sin necesidad de UIDs previos. Si la roca/ubicación existe, la reutiliza; si no, la crea automáticamente.

**Beneficio:** El cliente no necesita hacer requests previos para crear rocas/ubicaciones.

### 🔗 Relaciones

```plaintext
Rocks  ──────────┐
                 ├──── Samples
Locations ───────┘
```

- Una **Roca** puede tener múltiples **Muestras**
- Una **Ubicación** puede tener múltiples **Muestras**
- Una **Muestra** está vinculada a exactamente una **Roca** y una **Ubicación**

### 🆔 Identificadores Únicos

Cada entidad utiliza **UUID v4** como clave primaria:

```python
uid: UUID = Field(default_factory=uuid4, primary_key=True)
```

**Ventajas:**

- Genera IDs único globalmente
- No secuenciales (más seguros)
- Generables en cliente

### 📅 Timestamps Automáticos

Los campos `created_at` y `updated_at` se asignan automáticamente en PostgreSQL:

```python
created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
```

### 🌐 CORS Configurado

El backend está configurado para aceptar requests desde múltiples orígenes:

```python
# app/src/__init__.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Para cambiar esto en producción, edita `app/src/__init__.py`.

### 🐛 SQL Logging Activado

En [`app/src/db/main.py`](app/src/db/main.py), el engine tiene `echo=True`, imprimiendo todas las queries SQL en los logs:

```python
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Imprime SQL en logs
    future=True
)
```

**Desactívalo en producción** cambiando a `echo=False`.

### 📊 Carga Inicial de Datos

El archivo [`app/src/load_initial_data.py`](app/src/load_initial_data.py) lee datos desde [`app/src/datos_rocas.csv`](app/src/datos_rocas.csv) y los carga automáticamente en el startup:

```python
# En app/src/__init__.py (lifespan event)
async def lifespan(app: FastAPI):
    # ... inicialización ...
    await load_initial_data()  # Carga datos desde CSV
    yield
```

**Para agregar más datos:**

1. Edita `app/src/datos_rocas.csv`
2. Reinicia con:

   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

---

## Monitoreo

### Ver Estado de Contenedores

```bash
docker-compose ps
```

### Ver Logs en Tiempo Real

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo PostgreSQL
docker-compose logs -f postgres

# Solo NGINX
docker-compose logs -f nginx

# Últimas 50 líneas sin seguir
docker-compose logs --tail=50
```

### Ver Uso de Recursos

```bash
docker stats

# Output:
# CONTAINER           CPU %   MEM USAGE / LIMIT
# rocks_postgres_1    0.5%    150MB / 7.8GB
# rocks_backend_1     1.2%    200MB / 7.8GB
# rocks_nginx_1       0.1%    50MB / 7.8GB
```

### Acceder a Contenedores

#### Terminal en el Backend

```bash
docker-compose exec backend bash

# Dentro del contenedor:
python -c "import sys; print(sys.version)"
ls -la src/
```

#### Terminal en PostgreSQL

```bash
docker-compose exec postgres psql -U rocks_user -d rocks_db

# Dentro de psql:
\dt                    # Listar tablas
SELECT * FROM rocks;   # Ver datos
\q                     # Salir
```

#### Ver Variables de Entorno

```bash
docker-compose exec backend env | grep POSTGRES
```

### Health Checks

```bash
# Backend
curl http://localhost/api/rocks -w "\nStatus: %{http_code}\n"

# NGINX
curl http://localhost -w "\nStatus: %{http_code}\n"

# PostgreSQL
docker-compose exec postgres pg_isready -U rocks_user -d rocks_db
```

## Stack Tecnológico Detallado

| Componente | Tecnología | Versión | Propósito |
| ----------- | ----------- | --------- | ---------- |
| **Framework** | FastAPI | ^0.95 | Web framework async |
| **ORM** | SQLModel | ^0.0.12 | Mapeo objeto-relacional |
| **ASGI Server** | Uvicorn | ^0.21 | Servidor web asincrónico |
| **Validación** | Pydantic | ^1.10 | Validación de datos |
| **Base de Datos** | PostgreSQL | ^14 | Persistencia de datos |
| **Driver Async** | asyncpg | ^0.27 | Conexión no-bloqueante |
| **Proxy** | NGINX | ^1.24 | Reverse proxy |
| **Orquestación** | Docker Compose | ^2.0 | Gestión de contenedores |

---

## Documentación Adicional

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [asyncpg Driver](https://magicstack.github.io/asyncpg/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [NGINX Documentation](https://nginx.org/en/docs/)

---

##  Autor

**Aguilar Ramos Enrique Alejandro** | Backend Development • Python • FastAPI • APIs REST • DevOps

---

## Checklist de Arranque Rápido

- [ ] Docker y Docker Compose instalados
- [ ] Variables de entorno configuradas (`app/.env`)
- [ ] `docker-compose.yml` revisado
- [ ] `nginx.conf` correctamente configurado
- [ ] `docker-compose up --build` ejecutado
- [ ] Esperar a que PostgreSQL esté listo (ver logs)
- [ ] Acceder a http://localhost/api/docs
- [ ] Probar endpoints en Swagger UI
- [ ] Crear rocas, ubicaciones y muestras
- [ ] Verificar datos en `http://localhost/api/rocks`
- [ ] Revisar logs: `docker-compose logs -f`

---

## Soporte

Problemas comunes:

| Problema | Solución |
| ---------- | ---------- |
| No conecta a BD | Limpiar volúmenes: `docker-compose down -v` |
| Cambios no reflejan | Reconstruir: `docker-compose up --build` |
| Permiso denegado | `sudo usermod -aG docker $USER` |
| Python/Deps error | Reconstruir sin caché: `docker-compose up --no-cache --build` |

Para más ayuda, revisa los logs:

```bash
docker-compose logs -f
```
