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
# 	"-w 4" especifica el número de workers que atenderán las peticiones. Se arrancarán 4 copias
# 		exactas de events_rest que atenderán peticiones sobre el mismo puerto. La documentación de
#		gunicorn recomienda utilizar de 2 a 4 workers. Nosotros hemos escogido el valor más alto.
#	"-p gunicorn.pid" crea un fichero temporal bajo el directorio src (llamado gunicorn.pid) que 
# 		contiene el PID asociado al proceso de gunicorn. Lo almacenamos para poder parar el  
#		servicio más tarde.
#	"--daemon" lanza el servidor en segundo plano para que no se congele la terminal.
# 	Por último, se especifica el nombre del módulo que se va a ejecutar seguido de la interfaz WSGI 
#	(web server gateway interface) __hug_wsgi__, un objeto creado por hug que actúa como interfaz
#	para conectar directamente con las funciones del módulo.
start:
	gunicorn --chdir src -w 4 events_rest:__hug_wsgi__ -p gunicorn.pid --daemon

# Parar el servicio web utilizando el fichero con el PID escrito al arrancarlo:
stop:
	kill `cat src/gunicorn.pid`