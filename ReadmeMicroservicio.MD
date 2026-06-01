# KIT DE EXAMEN: Microservicios (App + PostgreSQL)

## 0. VARIABLES A REEMPLAZAR (Usa Ctrl+H)

* `[USUARIO_DOCKER]` -> Tu usuario de Docker Hub (ej. jordyromerou)
* `[NOMBRE_APP]` -> Nombre del proyecto
* `[VERSION]` -> Versión (ej. 1.0.0)
* `[PUERTO_HOST]` -> Puerto para el navegador (ej. 8080)
* `[PUERTO_APP]` -> Puerto interno de la app (ej. 5000)

---

## 1. ARCHIVOS DE CONFIGURACIÓN PREVIOS

### Archivo: `.gitignore`

```text
venv/
__pycache__/
*.pyc
.env
```

**IMPORTANTE:** Asegúrate de que el archivo `requirements.txt` incluya `psycopg2-binary` o `psycopg2` para conectar a PostgreSQL.

### Archivo: `Dockerfile`

(Es exactamente el mismo que el de SQLite; la conexión a PostgreSQL se configura mediante `docker-compose.yml`).

```dockerfile
FROM python:3.11-slim

# Documentación de la imagen
LABEL maintainer="jromeroa5@est.ups.edu.ec"
LABEL version="1.0.0"
LABEL description="Aplicación web NoticeBoard empaquetada"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=[PUERTO_APP]

RUN useradd -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE $PORT

CMD ["python", "run.py"]
```

### Archivo: `docker-compose.yml`

Este es el orquestador. Guárdalo en la raíz de tu proyecto.

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: admin_db
      POSTGRES_PASSWORD: password123
      POSTGRES_DB: base_examen
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    image: jordyromerou/[NOMBRE_APP]:[VERSION]
    ports:
      - "[PUERTO_HOST]:[PUERTO_APP]"
    environment:
      - PORT=[PUERTO_APP]
      # URL de conexión (Debe coincidir con las credenciales de arriba)
      - DATABASE_URL=postgresql://admin_db:password123@db:5432/base_examen
    depends_on:
      - db

volumes:
  postgres_data:
```

---

## 2. COMANDOS DE EJECUCIÓN PASO A PASO

### A. Construcción y Ejecución Simultánea (Compose Up)

```bash
docker compose up -d --build
```

#### Comprobaciones para el profesor

```bash
docker compose ps
docker compose logs app
docker compose exec app whoami
```

---

### B. Subida a Docker Hub (Push)

(El comando `docker compose up --build` ya generó y etiquetó la imagen de tu aplicación).

```bash
docker login
docker push jordyromerou/[NOMBRE_APP]:[VERSION]
```

---

### C. Prueba de Fuego (Forzar descarga desde la nube)

```bash
# Apagar todo y borrar contenedores
docker compose down

# Borrar la imagen local para forzar el pull
docker rmi jordyromerou/[NOMBRE_APP]:[VERSION]

# Volver a levantar todo (al no existir la imagen local, Docker la descargará desde Docker Hub)
docker compose up -d
```