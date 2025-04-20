FROM python:3.13.2-slim

# Variables para runtime de Pygame (evita errores de entorno como XDG_RUNTIME_DIR)
ENV SDL_AUDIODRIVER=alsa
ENV XDG_RUNTIME_DIR=/tmp/runtime
RUN mkdir -p /tmp/runtime && chmod 777 /tmp/runtime

# Crea y entra en carpeta de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY . .

# Instala librerías del sistema necesarias para pygame
RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    libasound2 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Ejecuta el juego (asegúrate que main.py está dentro de src/)
CMD ["python", "-m", "src.main"]
