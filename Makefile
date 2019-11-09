# Run "make test" for execute unit test over python's modules:
test:
	python -m unittest -v tests/test_events.py


# Run "make clean" for remove pycache files:
clean:
	rm -rf src/__pycache__/
	rm -rf tests/__pycache__/