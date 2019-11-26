# Seleccionamos la imagen base. En este caso se trata del SO alpine que
# ya contiene instalada la versión de python usada durante el desarrollo:
FROM python:3.6.8-alpine

# Establecer el directorio de trabajo:
WORKDIR /usr/src/app

# Copiar e instalar el requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Borrarlo, ya no nos hará falta:
RUN rm requirements.txt

# Copiar solamente los dos scripts de python necesarios:
COPY src/Events.py ./
COPY src/events_rest.py ./

# Indicar el puerto en el docker debe escuchar:
EXPOSE 80

# Lanzar gunicorn:
# Le indicamos que debe ejecutarse en el puerto 80
CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:80", "events_rest:__hug_wsgi__" ]