# KIT DE EXAMEN: App Monolítica (SQLite)

## 0. Variables a reemplazar

Usa **Ctrl + H** para reemplazar:

| Variable | Ejemplo |
|-----------|----------|
| `[USUARIO_DOCKER]` | jordyromerou |
| `[NOMBRE_APP]` | noticeboard_examen |
| `[VERSION]` | 1.0.0 |
| `[PUERTO_HOST]` | 8080 |
| `[PUERTO_APP]` | 5000 |

---

## 1. Archivos de configuración previos

### Archivo `.gitignore`

Crea este archivo en la raíz del proyecto para evitar subir archivos innecesarios al repositorio o a la imagen Docker.

```text
# Entornos virtuales
venv/
env/
.env

# Caché de Python
__pycache__/
*.pyc

# Base de datos local (opcional)
*.db
instance/
```

---

## 2. Archivo `Dockerfile`

Asegúrate de tener un Dockerfile con buenas prácticas (usuario no root y aprovechamiento de caché de dependencias).

```dockerfile
# 1. Imagen base ligera
FROM python:3.11-slim

# Documentación de la imagen
LABEL maintainer="jromeroa5@est.ups.edu.ec"
LABEL version="1.0.0"
LABEL description="Aplicación web NoticeBoard empaquetada"

# 2. Variables de entorno de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=[PUERTO_APP]

# 3. Crear usuario sin privilegios
RUN useradd -m appuser

WORKDIR /app

# 4. Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar código fuente
COPY --chown=appuser:appuser . .

# 6. Ejecutar como usuario seguro
USER appuser

# 7. Documentar puerto y ejecutar aplicación
EXPOSE $PORT

CMD ["python", "run.py"]
```

---

## 3. Comandos de ejecución

### A. Construcción de la imagen (Build)

```bash
docker build -t jordyromerou/[NOMBRE_APP]:[VERSION] .
docker images
```

---

### B. Ejecución local y pruebas (Run)

```bash
docker run -d \
  -p [PUERTO_HOST]:[PUERTO_APP] \
  -e PORT=[PUERTO_APP] \
  --name [NOMBRE_APP]_local \
  jordyromerou/[NOMBRE_APP]:[VERSION]
```

#### Comprobaciones

```bash
docker ps
docker logs [NOMBRE_APP]_local
docker exec [NOMBRE_APP]_local whoami
```

---

### C. Subida a Docker Hub (Push)

```bash
docker login
docker push jordyromerou/[NOMBRE_APP]:[VERSION]
```

---

### D. Prueba de fuego (descarga desde Docker Hub)

Eliminar el contenedor e imagen local para obligar a Docker a descargar la imagen desde Docker Hub.

```bash
docker rm -f [NOMBRE_APP]_local

docker rmi jordyromerou/[NOMBRE_APP]:[VERSION]

docker run -d \
  -p [PUERTO_HOST]:[PUERTO_APP] \
  -e PORT=[PUERTO_APP] \
  --name [NOMBRE_APP]_nube \
  jordyromerou/[NOMBRE_APP]:[VERSION]
```

#### Verificación final

```bash
docker ps
docker logs [NOMBRE_APP]_nube
```