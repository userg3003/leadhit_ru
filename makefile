SCRIPTS=scripts/
TESTS_FOLDER=tests/
REQ=requirements.txt
REQ_DEV=requirements_dev.txt

ENV_FILE_TEST=leadhit.test.env
ENV_FILE=leadhit.env

DOCKER_COMPOSE_FULL=.deploy/docker-compose.full.yml
DOCKER_COMPOSE_MONGO=.deploy/docker-compose.test.yml
UVICORN=uvicorn

ifndef PYTHON
	PYTHON=python
endif
ifndef DOCKER_COMPOSE
	DOCKER_COMPOSE=docker-compose
endif
ifndef DOCKER
	DOCKER=docker
endif
ifndef PYTEST
	PYTEST=pytest
endif
ifndef PIP
	PIP=pip
endif

.PHONY: config build publish clean deps run run-env run-full run-rebuild  tests

ENVS=APP_ENV=${ENV_FILE} ${PYTHON}
ENVS_DOCKER=APP_ENV=${ENV_FILE}
ENVS_TEST=PYTHONPATH=${PYTHON} APP_ENV=${ENV_FILE_TEST}

build-image:
	$(ENVS_DOCKER) $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FULL) build

deps:
	$(PIP) install -r $(REQ)

deps-dev:
	$(PIP) install -r $(REQ_DEV)

run:
	$(ENVS) -m  app.main

fill-db:
	$(ENVS) -m  scripts.fill_base

run-full:
	$(ENVS_DOCKER) $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FULL) up

run-mongo:
	$(ENVS) $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_MONGO) up

run-rebuild:
	$(ENVS_DOCKER) $(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FULL) up --build

tests:
	$(ENVS_TEST) $(PYTEST) -v -l --disable-warnings ${TESTS_FOLDER}

