# Usa el mirror de Google para la imagen oficial de Python Alpine (evita timeouts de red)
FROM mirror.gcr.io/library/python:3.12-alpine

# Define variables de entorno para evitar que Python escriba ficheros .pyc y almacene el buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea un usuario no root para mayor seguridad (sintaxis específica de Alpine Linux)
RUN adduser -D appuser

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los ficheros de la aplicación
# El fichero .dockerignore evitará que se copien tests o entornos virtuales
COPY --chown=appuser:appuser . .

# Cambia al usuario no root
USER appuser

# Expone el puerto en el que el servidor escucha
EXPOSE 8080

# Comando para iniciar la aplicación (server.py escucha en todas las interfaces por defecto)
CMD ["python", "server.py", "--port", "8080"]
