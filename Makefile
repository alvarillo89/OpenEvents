# Run "make install" to install all dependences:
install:
	pip install -r requirements.txt

# Run "make test" for execute unit and coverage tests over python's modules:
test:
	coverage run tests/test_events.py

# Run "make clean" for remove pycache folders and .coverage file:
clean:
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/
	rm .coverage