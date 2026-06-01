# 1. IMAGEN BASE APROPIADA
FROM python:3.11-slim

# 2. DOCUMENTACIÓN DE LA IMAGEN 
LABEL maintainer="jromeroa5@est.ups.edu.ec"
LABEL version="1.0.0"
LABEL description="Aplicación web NoticeBoard empaquetada"

# 3. VARIABLES DE ENTORNO PARA CONFIGURACIÓN
ENV PORT=5000 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. USUARIO DEDICADO (no-root)
RUN useradd -m appuser

# 5. DIRECTORIO DE TRABAJO
WORKDIR /app

# 6. ORDEN DE INSTRUCCIONES
COPY requirements.txt .

# 7. DEPENDENCIAS CORRECTAMENTE INSTALADAS 
RUN pip install --no-cache-dir -r requirements.txt

# 8. CÓDIGO FUENTE 
COPY --chown=appuser:appuser . .

# Cambiar al usuario sin privilegios
USER appuser

# 9. DOCUMENTACIÓN DEL PUERTO
EXPOSE $PORT

# 10. CONTENEDOR AUTOCONTENIDO
CMD python run.py