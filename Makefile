# Instala las dependencias necesarias para el proyecto:
install:
	# Instalar los modulos de Python necesarios desde el fichero
	# requirements.txt
	pip install -r requirements.txt

# Ejecutar los test unitarios y de cobertura
test:
	# Usamos coverage.py para generar el fichero .coverage:
	coverage run tests/test_events.py
	coverage run -a tests/test_events_rest.py
	coverage run -a tests/test_mongo_dm.py

# Limpiar el directorio de las carpetas y ficheros que se generan
# tras la ejecución:
clean:
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/
	rm .coverage

# Arrancar el servicio web utilizando gunicorn (Green Unicorn):
# 	"--chdir src" sirve para movernos al directorio src antes de que la app se cargue. Es necesario
# 		porque el script events_rest.py se encuentra bajo este directorio, sin embargo nosotros 
#		ejecutamos make desde el directorio raíz.
#	"--worker-class eventlet" con esta opción especificamos el tipo de workers que utilizará
#		gunicorn. `eventlet` es un modulo que proporciona workers asíncronos, los cuales nos
#		permitiran obtener mejores prestaciones.
# 	"-w 10" especifica el número de workers que atenderán las peticiones. Se arrancarán 10 copias
# 		exactas de events_rest que atenderán peticiones sobre el mismo puerto. Puesto que queremos
#		unas prestaciones en las que el servidor sea capaz de atender 10 usuarios simultáneos,
#		estableceremos un worker por cada uno de ellos.
#	"-b HOST:PORT" especficia el server socket al que enlazarse. Previamente hay que definir las dos
#		variables de entorno correspondientes.
#	"-p gunicorn.pid" crea un fichero temporal bajo el directorio src (llamado gunicorn.pid) que 
# 		contiene el PID asociado al proceso de gunicorn. Lo almacenamos para poder parar el  
#		servicio más tarde.
#	"--daemon" lanza el servicio en segundo plano para que no se congele la terminal.
# 	Por último, se especifica el nombre del módulo que se va a ejecutar seguido de la interfaz WSGI 
#	(web server gateway interface) __hug_wsgi__, un objeto creado por hug que actúa como interfaz
#	para conectar directamente con las funciones del módulo.
start:
	gunicorn --chdir src --worker-class eventlet -w 10 -b ${HOST}:${PORT} -p gunicorn.pid \
		--daemon events_rest:__hug_wsgi__

# Parar el servicio web utilizando el fichero con el PID escrito al arrancarlo:
stop:
	kill `cat src/gunicorn.pid`