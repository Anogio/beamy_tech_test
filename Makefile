.PHONY: build
build:
	docker image build -t tech_test .

.PHONY: install
install:
	python -m pip install -r requirements.txt

.PHONY: test_environment
test_environment:
	docker-compose -f docker-compose-test.yaml up

.PHONY: test
test: install
	python -m pytest tests

.PHONY: level_1_server
level_1_server: build
	docker run -p 3000:3000 -v parsed:/opt/app/parsed  tech_test python -m level_1.level_1_app

.PHONY: level_2_server
level_2_server:
	docker-compose -f docker-compose.yaml up

.PHONY: run_exercise
run_exercise: install
	python -m lib.http_emitter
