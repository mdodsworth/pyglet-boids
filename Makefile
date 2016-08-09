init:
	pip install -r requirements.txt

test:
	nosetests tests

run:
	python -m boids
