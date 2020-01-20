# Instala las dependencias necesarias para el proyecto:
install:
	# Instalar los modulos de Python necesarios desde el fichero
	# requirements.txt
	pip install -r requirements.txt

# Ejecutar los test unitarios, de integración y de cobertura
test:
	# Usamos coverage.py para generar el fichero .coverage:
	coverage run tests/test_events.py
	coverage run -a tests/test_events_rest.py
	coverage run -a tests/test_mongo_dm.py
	coverage run -a tests/test_tickets.py
	coverage run -a tests/test_tickets_rest_tasks.py

# Limpiar el directorio de las carpetas y ficheros que se generan
# tras la ejecución:
clean:
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/
	rm .coverage

# (1) Arrancar los servicios web de ambos microservicios utilizando gunicorn (Green Unicorn):
# 	"--chdir src" sirve para movernos al directorio src antes de que la app se cargue. Es necesario
# 		porque los scripts de ambos microservicios se encuentra bajo este directorio, sin embargo  
#		nosotros ejecutamos make desde el directorio raíz.
#	"--worker-class gevent" con esta opción especificamos el tipo de workers que utilizará
#		gunicorn. `gevent` es un modulo que proporciona workers asíncronos, los cuales nos
#		permitiran obtener mejores prestaciones.
# 	"-w 10" especifica el número de workers que atenderán las peticiones. Se arrancarán 10 copias
# 		exactas de cada api rest que atenderán peticiones sobre el mismo puerto. Puesto que queremos
#		unas prestaciones en las que los servidores sean capaces de atender 10 usuarios simultáneos,
#		estableceremos un worker por cada uno de ellos.
#	"-b HOST_X:PORT_X" especficia el server socket al que enlazarse. Previamente hay que definir las
#		variables de entorno correspondientes. Se debe definir un par de variables para cada uno de
#		los microservicios.
#	"-p *.pid" crea un fichero temporal bajo el directorio src que contiene el PID asociado al 
#		proceso de gunicorn. Lo almacenamos para poder parar el servicio más tarde.
#	"--daemon" lanza los servicios en segundo plano para que no se congele la terminal.
# 	Por último, se especifica el nombre del módulo que se va a ejecutar seguido de la interfaz WSGI 
#	(web server gateway interface) __hug_wsgi__, un objeto creado por hug que actúa como interfaz
#	para conectar directamente con las funciones del módulo.
# (2) Arrancar Celery para el microservicio tickets:
#	- Primero nos movemos al directorio src, pues el script que contiene la App de celery se 
#	encuentra ahí.
#	- Con -A le indicamos el script que contiene la App de Celery.
#	- worker para indicar que deseamos lanzar un worker para la App especificada anteriormente.
#	- Con --detach hacemos que Celery se ejecute en segundo plano para no bloquear la terminal.

start:
	gunicorn --chdir src --worker-class gevent -w 10 -b ${HOST_E}:${PORT_E} -p events.pid \
		--daemon events_rest:__hug_wsgi__
	
	gunicorn --chdir src --worker-class gevent -w 10 -b ${HOST_T}:${PORT_T} -p tickets.pid \
		--daemon tickets_rest:__hug_wsgi__

	cd src && celery -A tickets_tasks worker --detach

# Parar los servicios web y Celery utilizando los ficheros con el PID escritos al arrancarlos:
stop:
	kill `cat src/events.pid`
	kill `cat src/tickets.pid`
	kill `cat src/celeryd.pid`

# Instala desde ansible galaxy todos los roles necesarios para el aprovisionamiento:
# Con -p especificamos la ruta en la que se descargará el rol:
download:
	mkdir provision/roles
	ansible-galaxy install -p provision/roles enix.mongodb
	ansible-galaxy install -p provision/roles geerlingguy.rabbitmq