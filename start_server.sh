#!/bin/bash

# Apply DB migrations if necessary
alembic upgrade head

python -m application

