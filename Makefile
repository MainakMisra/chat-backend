# Reads .env and imports all it's environment variables
-include config/server.env

# Db tools
psql := $(shell which psql)

# Docker tools
docker := $(shell which docker)
docker-compose := $(docker) compose

# Python tools
pip := $(shell which pip3)
python := $(poetry) run python
pytest := $(poetry) run pytest
alembic := $(poetry) run alembic
pre-commit := $(poetry) run pre-commit

MAKEFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

# Variable used to connect to postgres inside docker container using psql and docker compose exec
DOCKER_DB_URI := "postgresql://$${POSTGRES_PASSWORD}:$${POSTGRES_PASSWORD}@0.0.0.0:5432/$${POSTGRES_DB}"

# Name of the services on compose
MAIN_SERVICE_NAME := "fastapi"
POSTGRES_SERVICE_NAME := "postgres"

db:
	$(docker-compose) up -d $(POSTGRES_SERVICE_NAME)

erase-db:
	$(docker-compose) stop $(POSTGRES_SERVICE_NAME)
	$(docker-compose) rm -f -v $(POSTGRES_SERVICE_NAME)
	$(docker) volume rm hr-backend_db-data 2> /dev/null || true


# Recreate database with an empty volume
clean-db: erase-db db