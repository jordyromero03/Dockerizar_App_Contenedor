# KIT DE EXAMEN: App Java (Monolítica)

## 0. VARIABLES A REEMPLAZAR EN ESTE DOC (Usa Ctrl+H)

* `[USUARIO_DOCKER]` -> Tu usuario de Docker Hub (ej. jordyromerou)
* `[NOMBRE_APP]` -> Nombre del proyecto (ej. api_java)
* `[VERSION]` -> Versión (ej. 1.0.0)
* `[PUERTO_HOST]` -> Puerto para el navegador (ej. 80)
* `[PUERTO_APP]` -> Puerto interno de Java/Spring Boot (generalmente 8080)

---

## 1. ARCHIVOS DE CONFIGURACIÓN PREVIOS

### Archivo: `.gitignore`

Para proyectos Java (Maven/Gradle), esto es vital para no subir los compilados pesados.

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

Arquitectura profesional Multi-stage Build (compila el código y luego lo ejecuta en una imagen limpia utilizando un usuario seguro).

```dockerfile
# ETAPA 1: Construcción (Build)
FROM maven:3.9-eclipse-temurin-17 AS builder

# Documentación de la imagen
LABEL maintainer="jromeroa5@est.ups.edu.ec"
LABEL version="1.0.0"
LABEL description="Aplicación Java [NOMBRE_APP] empaquetada"

WORKDIR /app

# Copiamos el pom.xml y el código fuente
COPY pom.xml .
COPY src ./src

# Compilamos el proyecto generando el .jar
RUN mvn clean package -DskipTests

# ETAPA 2: Producción (Run)
FROM eclipse-temurin:17-jre-alpine

ENV PORT=[PUERTO_APP]

# Usuario seguro no-root
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copiamos SOLO el .jar compilado desde la ETAPA 1
COPY --from=builder --chown=appuser:appgroup /app/target/*.jar app.jar

USER appuser

EXPOSE $PORT

# Ejecutar el archivo Java
CMD ["java", "-jar", "app.jar"]
```

---

## 2. COMANDOS DE EJECUCIÓN PASO A PASO

### A. Construcción (Build)

```bash
docker build -t jordyromerou/[NOMBRE_APP]:[VERSION] .
docker images
```

---

### B. Ejecución Local y Pruebas (Run)

```bash
docker run -d \
  -p [PUERTO_HOST]:[PUERTO_APP] \
  -e SERVER_PORT=[PUERTO_APP] \
  --name [NOMBRE_APP]_local \
  jordyromerou/[NOMBRE_APP]:[VERSION]
```

#### Comprobaciones para el profesor

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

### D. Prueba de Fuego (Forzar descarga)

```bash
docker rm -f [NOMBRE_APP]_local

docker rmi jordyromerou/[NOMBRE_APP]:[VERSION]

docker run -d \
  -p [PUERTO_HOST]:[PUERTO_APP] \
  -e SERVER_PORT=[PUERTO_APP] \
  --name [NOMBRE_APP]_nube \
  jordyromerou/[NOMBRE_APP]:[VERSION]
```

#### Verificación final

```bash
docker ps
docker logs [NOMBRE_APP]_nube
```