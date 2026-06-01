# KIT DE EXAMEN: Microservicios Java (App + PostgreSQL)

## 0. VARIABLES A REEMPLAZAR (Usa Ctrl+H)

* `[NOMBRE_APP]` -> Nombre del proyecto
* `[VERSION]` -> Versión (ej. 1.0.0)
* `[PUERTO_HOST]` -> Puerto para el navegador (ej. 80)
* `[PUERTO_APP]` -> Puerto interno de Java/Spring Boot (ej. 8080)

---

## 1. ARCHIVOS DE CONFIGURACIÓN PREVIOS

### Archivo: `.gitignore`

```text
# Archivos compilados y empaquetados
target/
build/
out/
*.class
*.jar
*.war

# IDEs
.idea/
*.iml
.vscode/

# Logs y SO
*.log
.DS_Store
```

### Archivo: `Dockerfile`

(Exactamente el mismo Multi-stage Build de la aplicación Java monolítica).

```dockerfile
# ETAPA 1: Construcción (Build)
FROM maven:3.9-eclipse-temurin-17 AS builder

# Documentación de la imagen
LABEL maintainer="jromeroa5@est.ups.edu.ec"
LABEL version="1.0.0"
LABEL description="Aplicación Java [NOMBRE_APP] conectada a PostgreSQL"

WORKDIR /app

COPY pom.xml .
COPY src ./src

RUN mvn clean package -DskipTests

# ETAPA 2: Producción (Run)
FROM eclipse-temurin:17-jre-alpine

ENV PORT=[PUERTO_APP]

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app/target/*.jar app.jar

USER appuser

EXPOSE $PORT

CMD ["java", "-jar", "app.jar"]
```

### Archivo: `docker-compose.yml`

Las aplicaciones Java/Spring Boot normalmente utilizan propiedades JDBC en lugar de `DATABASE_URL`.

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
      - SERVER_PORT=[PUERTO_APP]
      # Variables de conexión estándar para Spring Boot / Java JDBC
      - SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/base_examen
      - SPRING_DATASOURCE_USERNAME=admin_db
      - SPRING_DATASOURCE_PASSWORD=password123
      - SPRING_JPA_HIBERNATE_DDL_AUTO=update
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

```bash
docker login
docker push jordyromerou/[NOMBRE_APP]:[VERSION]
```

---

### C. Prueba de Fuego (Forzar descarga desde la nube)

```bash
# 1. Apagar todo y borrar contenedores
docker compose down

# 2. Borrar la imagen local para forzar el pull
docker rmi jordyromerou/[NOMBRE_APP]:[VERSION]

# 3. Volver a levantar todo (Descargará tu imagen Java desde Docker Hub)
docker compose up -d
```

#### Verificación final

```bash
docker compose ps
docker compose logs app
```