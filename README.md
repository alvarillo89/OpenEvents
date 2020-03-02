[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.com/alvarillo89/UGR-CC-Project.svg?branch=master)](https://travis-ci.com/alvarillo89/UGR-CC-Project)
[![codecov](https://codecov.io/gh/alvarillo89/UGR-CC-Project/branch/master/graph/badge.svg)](https://codecov.io/gh/alvarillo89/UGR-CC-Project)
[![DevQAGRX](https://img.shields.io/badge/DevQAGRX-blueviolet?style=svg&logo=Git)](https://github.com/JJ/curso-tdd)

# Proyecto de la asignatura Cloud Computing (Máster en Ingeniería Informática - UGR)

Puede consultar cómo se configuró Git y Github para el proyecto en [este enlace.](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/gitconfig.md)

## OpenEvents

![](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/imgs/logo.png)

`OpenEvent` es una aplicación open source que permite a organizadores de cualquier tipo publicar información sobre sus eventos y vender entradas para los mismos mediante pagos electrónicos. Todo ello a través de la nube.

### Arquitectura e Infraestructura

La aplicación se implementa siguiendo una arquitectura basada en microservicios. Puede consultar con mayor detalle la *Arquitectura e Infraestructura* del proyecto, y de cada microservicio, en el [siguiente enlace](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/architecture.md).

---

### Prerrequisitos y versiones

El proyecto está implementado en Python. Para su correcto funcionamiento deberá disponer de alguna de las versiones presentes en el siguiente rango:

+ Mínima versión compatible:  3.5 
+ Máxima versión compatible:  3.8 (incluída la versión en desarrollo)

Adicionalmente, deberá disponer de la herramienta `Makefile` y tener instalado [Ghostscript](https://www.ghostscript.com/) en su sistema, dependencia necesaria que deberá instalar manualmente para el correcto funcionamiento del módulo `treepoem`.

> *Nota: El microservicio `Tickets` **solo es compatible con un sistema Linux.** El módulo `treepoem` no reconoce correctamente `ghostscript` en Windows, por lo que no funciona apropiadamente*. El microservicio `Events` funciona sin problemas en ambos sistemas operativos, aunque  las versiones mencionadas anteriormente se han testeado en Linux. En Windows solo se ha comprobado hasta la versión 3.7, por lo que se desconoce el comportamiento para la versión 3.8.

---

### Herramienta de construcción

buildtool: Makefile

Este proyecto utiliza `Makefile` como herramienta de construcción. Los objetivos configurados son los siguientes:

```
$ make install
```

*Instala todos los requisitos (módulos de Python) necesarios para la aplicación. Alternativamente a esto puede ejecutar `pip install -r requirements.txt`*. Si desea conocer qué módulos se instalan con esta órden, consulte el fichero [**requirements.txt**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/requirements.txt).

```
$ make test
```

Ejecuta todos los tests presentes en directorio [tests/](https://github.com/alvarillo89/UGR-CC-Project/tree/master/tests) (tests unitarios, de integración y de cobertura).  

Para los test unitarios y de integración se ha utilizado `unittest`, simplemente porque ya está incorporado en la propia ditribución de Python y no requiere de la instalación de un módulo externo. Para los test de cobertura se ha utilizado `coverage.py`. Dicho módulo generará el archivo `.coverage` que contiene el *report* de los test de cobertura. La herramienta que desee utilizar para la visualización del reporte queda a su elección. En los tests de integración contínua se ha utilizado `Codecov`.

```
$ make clean
```

*Limpia el directorio del proyecto, eliminando los directorios `__pycache__` y el archivo `.coverage` resultante de los test de cobertura.*

```
$ make start
```

*Arranca los servicios web de ambos microservicios utilizando [Gunicorn](https://gunicorn.org/). También arranca la cola de tareas de [Celery](http://www.celeryproject.org/).* Previamente a la ejecución de esta orden, deberá configurar una serie de variables de entorno: 

- `HOST_E` y `PORT_E` conteniendo la dirección y el puerto del server socket para el microservicio `Events`.
- `HOST_T` y `PORT_T` conteniendo la dirección y el puerto del server socket para el microservicio `Tickets`.
- `DB_URI` continendo la uri de la base de datos de MongoDB.
- `CELERY_BROKER` y `CELERY_BACKEND` contiendo las urls del broker y backend que utilizará Celery, respectivamente. 

> Para más información sobre los parámetros con los que gunicorn es arrancado consulte el [**fichero Makefile**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/Makefile).

```
$ make stop
```

*Finaliza la ejecución de los servicios web de ambos microservicios y todos sus workers. También para la ejecución de Celery.*

```
make download
```

*Descarga de [Ansible Galaxy](https://galaxy.ansible.com/home) todos los roles que son necesarios para el provisionamiento de las máquinas virtuales (para instalar MongoDB y docker). Los roles descargados se situarán en el directorio `/provision/roles/`*.

Para más detalles, consulte el [**fichero Makefile**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/Makefile), el cual contiene comentarios explicativos.

---

### Integración contínua

El proyecto utiliza dos sistemas de integración contínua diferentes: `Travis-CI` y `GitHub Actions`. Para obtener más información sobre las funciones que desempeñan cada uno de ellos, consulte el [siguiente enlace](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/ci.md).

----

### Contenedor Docker del microservicio Events

Contenedor: https://hub.docker.com/r/alvarillo89/events

En el enlace superior puede acceder a la imagen del contenedor publicada en Docker Hub, que contiene el microservicio `Events` junto con todas las dependencias que necesita para ejecutarse. También se ha subido adicionalmente a [**Github Packages Registry**](https://github.com/alvarillo89/UGR-CC-Project/packages/63964).

Para más información sobre la construcción del contenedor, consulte el [**siguiente enlace**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/docker.md).

---

### Despliege en Heroku del microservicio Events

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

La aplicación desplegada está disponible bajo la siguiente dirección:

https://openevents.herokuapp.com

Consulte el [**siguiente enlace**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/heroku.md) para conocer más detalles sobre el proceso seguido para el despliegue.

---

### Almacén de Datos

Tal y como se describe en la sección *Arquitectura e infrestructura*, este proyecto utiliza `MongoDB` como almacén de datos. 

> **Nota:** Deberá configurar una variable de entorno llamada `DB_URI` que contenga la uri de la base de datos a la que se conectará el microservicio.

En el [**siguiente enlace**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/mongo.md) se describe cómo se ha integrado este servicio en el microservicio `Events`.

---

### Evaluación de prestaciones del microservicio Events

Prestaciones: performance_evaluation.yml

Las prestaciones del microservicio `Events` se han evaluado utilizando [Taurus](https://gettaurus.org/). Se pedía alcanzar un rendimiento estimado de 1000 peticiones/s con 10 usuarios concurrentes. El resultado que finalmente se ha obtenido en su rendimiento es de **2976 peticiones/s** de media con 10 usuarios concurrentes.

En el [**siguiente enlace**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/performance.md), se puede consultar el proceso de evaluación realizado junto con todas las modificaciones que se han efectuado para alcanzar el rendimiento deseado.

---

### Implementación del microservicio Tickets

La implementación de este microservicio incluye los tres scripts siguientes:

- [**Tickets.py**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/src/Tickets.py)
- [**tickets_task.py**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/src/tickets_tasks.py)
- [**tickets_rest.py**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/src/tickets_rest.py)

Puede consultar con mayor detalle la documentación sobre como se ha implementado este microservicio y como se ha integrado con el resto del sistema en la [descripción de la Arquitectura de la aplicación](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/architecture.md).

---

### Provisionamiento de máquinas virtuales con Ansible

Para finalizar con este proyecto, se ha realizado el despliegue de ambos microservicios (`Events` y `Tickets`) en máquinas virtuales. Se ha llevado a cabo el despliegue tanto en una máquina virtual local, como en la plataforma de [Microsoft Azure](https://azure.microsoft.com/es-es/).

Para el provisionamiento y demás tareas de automatización, se ha utilizado [Ansible](https://www.ansible.com/).

Puede consultar con mayor detalle la documentación sobre este apartado en el [**siguiente enlace**](https://github.com/alvarillo89/UGR-CC-Project/blob/master/docs/ansible.md).
