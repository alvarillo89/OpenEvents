# Seleccionamos la imagen base. En este caso, se trata del SO minideb:
FROM bitnami/minideb:latest

# Información sobre el mantenedor:
LABEL maintainer="Álvaro alvaro89@correo.ugr.es"

# Definir el puerto como variable de entorno:
ENV PORT ${PORT}

# Establecer el directorio de trabajo:
WORKDIR /usr/src/app

# Instalar python3
# Atualizar pip e instalar las dependencias. No usamos el requirements.txt porque
# contiene módulos que no son necesarios en el contenedor. Además indicamos que no use la caché.
RUN install_packages python3 python3-pip \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir gunicorn \
    hug    

# Copiar solamente los dos scripts de python necesarios:
COPY src/Events.py src/events_rest.py ./

# Esta orden solo tiene carácter informativo. Indica a futuros usuarios de este
# dockerfile el puerto en el que escucha el microservicio.
EXPOSE ${PORT}

# Creamos un usuario para evitar que el servidor se ejecute con permisos de
# superusuario, por temas de seguridad:
# https://devcenter.heroku.com/articles/container-registry-and-runtime#testing-an-image-locally
RUN useradd -m nonroot
USER nonroot

# Lanzar gunicorn:
CMD gunicorn -w 4 -b 0.0.0.0:${PORT} events_rest:__hug_wsgi__