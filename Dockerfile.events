# Seleccionamos la imagen base. En este caso, se trata del SO minideb:
FROM bitnami/minideb:latest

# Información sobre el mantenedor:
LABEL maintainer="Álvaro alvaro89@correo.ugr.es"

# Definir el puerto y la url de la base de datos como variables de entorno:
ENV PORT ${PORT}
ENV DB_URI ${DB_URI} 

# Establecer el directorio de trabajo:
WORKDIR /usr/src/app

# Instalar python3
# Atualizar pip e instalar las dependencias. 
# Instalar netbase para que se cree el fichero /etc/protocols en el contenedor. Este fichero
# es necesario para los workers asíncronos de gunicorn.
# No usamos el requirements.txt porque contiene módulos que no son necesarios en el contenedor. 
# Además indicamos que no use la caché.
RUN install_packages python3 python3-pip netbase \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir dnspython \
    eventlet \
    gunicorn \
    hug \
    pymongo

# Copiar solamente los tres scripts de python necesarios:
COPY src/Events.py src/events_rest.py src/mongo_data_manager.py ./

# Esta orden solo tiene carácter informativo. Indica a futuros usuarios de este
# dockerfile el puerto en el que escucha el microservicio.
EXPOSE ${PORT}

# Creamos un usuario para evitar que el servidor se ejecute con permisos de
# superusuario, por temas de seguridad:
# https://devcenter.heroku.com/articles/container-registry-and-runtime#testing-an-image-locally
RUN useradd -m nonroot
USER nonroot

# Lanzar gunicorn:
CMD gunicorn --worker-class eventlet -w 10 -b 0.0.0.0:${PORT} events_rest:__hug_wsgi__