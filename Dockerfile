# Seleccionamos la imagen base. En este caso se trata del SO alpine que
# ya contiene instalada la versión de python usada durante el desarrollo:
FROM python:3.6.8-alpine

# Información sobre el mantenedor:
LABEL maintainer="Álvaro alvaro89@correo.ugr.es"

# Definir el puerto como variable de entorno:
ENV PORT ${PORT}

# Establecer el directorio de trabajo:
WORKDIR /usr/src/app

# Atualizar pip e instalar las dependencias. No usamos el requirements.txt porque
# contiene módulos que no son necesarios en el contenedor. Además indicamos que no use la caché.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir gunicorn \
    hug    

# Copiar solamente los dos scripts de python necesarios:
COPY src/Events.py src/events_rest.py ./

# Indicar el puerto en el que docker debe escuchar: (a título informativo):
EXPOSE ${PORT}

# Creamos un usuario para evitar que el servidor se ejecute con permisos de
# superusuario, por temas de seguridad:
RUN adduser -D myuser
USER myuser

# Lanzar gunicorn:
CMD gunicorn -w 4 -b 0.0.0.0:${PORT} events_rest:__hug_wsgi__