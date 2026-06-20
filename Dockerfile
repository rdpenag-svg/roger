# 1. Imagen base de Python (versión ligera)
FROM python:3.11-slim

# 2. Metadatos del mantenedor
LABEL maintainer="fintech@nova.com"
LABEL version="1.0.0"
LABEL description="FinTech Nova API - Evaluación Crediticia"

# 3. Variables de entorno para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 4. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 5. Crear usuario no-root (Principio de Mínimo Privilegio)
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

# 6. Instalar herramientas del sistema (curl para healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 7. Copiar requirements.txt y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copiar todo el código de la aplicación
COPY . .

# 9. Cambiar propietario de los archivos al usuario no-root
RUN chown -R appuser:appgroup /app

# 10. Cambiar al usuario no-root
USER appuser

# 11. Documentar el puerto que usa la aplicación
EXPOSE 8000

# 12. HEALTHCHECK - Docker verifica la salud automáticamente
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 13. Comando para iniciar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
