# Events App Backend

Este proyecto es el backend de una aplicacion de gestion de eventos, construido con **Python**, **FastAPI** y **SQLModel**. Permite la creacion, actualizacion, listado y eliminacion de usuarios, eventos y sesiones.

## Tecnologias Usadas

- Python 3.12
- FastAPI
- SQLModel
- SQLite (para desarrollo/pruebas)
- PostgreSQL (para produccion)
- Poetry (gestion de dependencias)
- Alembic (migraciones de base de datos)
- Pytest (testing)
- pytest-cov (cobertura de tests)
- Docker / Docker Compose
- Swagger (Documntacion API)

## Instalacion

1. Clonar el repositorio:

    ```bash
    git clone https://github.com/jimmydmd/events_backend.git
    cd events_app_backend
    ```

2. Instalar dependencias con Poetry:

    ```bash
    poetry install
    ```

3. Configurar variables de entorno:

    ```bash
    cp .env.example .env
    ```

4. Base de datos: Se utiliza SQLModel con SQLite para testing y PostgreSQL para desarrollo, gestionado mediante Alembic. 

    Crear migraciones:

    ```bash
    poetry run alembic revision --autogenerate -m "mensaje de la migracion"
    ```

    Aplicar migraciones:

    ```bash
    poetry run alembic upgrade head
    ```

5. Crear usuario administrador:

    Despues de aplicar las migraciones, puedes inicializar roles y crear un usuario administrador:

    ```bash
    poetry run python src/events_app_backend/users/init_roles_admin.py
    ```

    Usando Docker

    Levantar los contenedores:
    ```bash
    docker-compose up -d
    ```

    Ejecutar el script dentro del contenedor backend (ajusta el nombre del servicio si es diferente):
    ```bash
    docker-compose exec django poetry run python src/events_app_backend/users/init_roles_admin.py
    ```

## Ejecucion

Levantar el backend en modo desarrollo:

```bash
poetry run uvicorn src.main:app --reload
```

O usando Docker Compose:

```bash
docker-compose up --build
```

## Documentacion

Este proyecto cuenta con documentación automática de la API generada con Swagger.

Acceso a Swagger UI

```bash
http://localhost:8000/docs/
```

## Test

Ejecutar tests y generar reporte de cobertura:

```bash
poetry run pytest --cov=src/events_app_backend --cov-report=term-missing
```

Los reportes HTML se generan en htmlcov/:
```bash
open htmlcov/index.html
```

## Probar la API con Postman

Se incluye una coleccion de Postman para probar los endpoints del backend.

1. Abrir Postman
2. Importar la coleccion desde `rest/events.coleccion.json`
3. Ejecutar los endpoints
