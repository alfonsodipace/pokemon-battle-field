
.PHONY: ready
ready: build test run

build:
	docker-compose build

test:
	docker-compose run app python -m unittest src/models/tests.py
run:
	docker-compose up db -d
	docker-compose run app

stop:
	docker-compose down
