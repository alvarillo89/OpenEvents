# Seleccionamos la imagen base. En este caso, se trata del SO minideb:
FROM bitnami/minideb:latest

# Información sobre el mantenedor:
LABEL maintainer="Álvaro alvaro89@correo.ugr.es"

# Definir el puerto, la uri de la base de datos, y las urls de Celery como variables de entorno:
ENV PORT ${PORT}
ENV DB_URI ${DB_URI}
ENV CELERY_BROKER ${CELERY_BROKER}
ENV CELERY_BACKEND ${CELERY_BACKEND}

# Establecer el directorio de trabajo:
WORKDIR /usr/src/app

# Instalar python3
# Atualizar pip e instalar las dependencias. 
# Instalar netbase para que se cree el fichero /etc/protocols en el contenedor. Este fichero
# es necesario para los workers asíncronos de gunicorn.
# Instalar ghostscript para el módulo Treepoem.
# No usamos el requirements.txt porque contiene módulos que no son necesarios en el contenedor. 
# Además indicamos que no use la caché.
RUN install_packages python3 python3-pip netbase ghostscript \
    && python3 -m pip install --no-cache-dir --upgrade pip \
    && python3 -m pip install --no-cache-dir celery \
    dnspython \
    gunicorn[gevent] \
    gunicorn \
    hug \
    pymongo \
    reportlab \
    treepoem

# Copiar solamente los cuatro scripts de python necesarios:
COPY src/Tickets.py src/tickets_rest.py src/tickets_tasks.py src/mongo_data_manager.py ./

# Esta orden solo tiene carácter informativo. Indica a futuros usuarios de este
# dockerfile el puerto en el que escucha el microservicio.
EXPOSE ${PORT}

# Creamos un usuario para evitar que el servidor se ejecute con permisos de
# superusuario, por temas de seguridad:
# https://devcenter.heroku.com/articles/container-registry-and-runtime#testing-an-image-locally
RUN useradd -m nonroot
USER nonroot

# Lanzar gunicorn y celery:
CMD gunicorn --worker-class gevent -w 10 -b 0.0.0.0:${PORT} --daemon tickets_rest:__hug_wsgi__ ; \
    celery -A tickets_tasks worker