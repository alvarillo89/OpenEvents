# Instala las dependencias necesarias para el proyecto:
install:
	# Instalar los modulos de Python necesarios desde el fichero
	# requirements.txt
	pip install -r requirements.txt

# Ejecutar los test unitarios y de cobertura
test:
	# Usamos coverage.py para generar el fichero .coverage:
	coverage run tests/test_events.py

# Limpiar el directorio de las carpetas y ficheros que se generan
# tras la ejecución:
clean:
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/
	rm .coverage