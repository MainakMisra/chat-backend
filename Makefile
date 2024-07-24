# Reads .env and imports all it's environment variables
-include config/server.env

# Db tools
psql := $(shell which psql)

# Docker tools
docker := $(shell which docker)
docker-compose := $(docker) compose

# Python tools
pip := $(shell which pip3)
python := python
pre-commit := python run pre-commit

MAKEFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
TESTS_DIR := $(MAKEFILE_DIR)/tests

# Variable used to connect to postgres inside docker container using psql and docker compose exec
DOCKER_DB_URI := "postgresql://$${POSTGRES_PASSWORD}:$${POSTGRES_PASSWORD}@0.0.0.0:5432/$${POSTGRES_DB}"

# Name of the services on compose
MAIN_SERVICE_NAME := "fastapi"
POSTGRES_SERVICE_NAME := "postgres"

PYTEST_ARGS := -vv --ff --durations=10 --durations-min=2.0

db:
	$(docker-compose) up -d $(POSTGRES_SERVICE_NAME)

erase-db:
	$(docker-compose) stop $(POSTGRES_SERVICE_NAME)
	$(docker-compose) rm -f -v $(POSTGRES_SERVICE_NAME)
	$(docker) volume rm hr-backend_db-data 2> /dev/null || true


# Recreate database with an empty volume
clean-db: erase-db db


run-compose:
	@echo "\n* Assuring backend is not already running...\n"
	$(docker-compose) down > /dev/null 2>&1 | true
	@echo "\n* Starting backend...\n"
	$(docker-compose) up --build


test-service:
	PYTHONPATH=$(MAKEFILE_DIR) pytest $(TESTS_DIR)/services/

test-repositories:
	PYTHONPATH=$(MAKEFILE_DIR) pytest $(TESTS_DIR)/repositories/

test-routes:
	PYTHONPATH=$(MAKEFILE_DIR) pytest $(TESTS_DIR)/routes/
