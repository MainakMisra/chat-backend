FROM python:3.10.10-bullseye as builder

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update -y &&\
    apt-get install -y --no-install-recommends \
      build-essential &&\
    rm -rf /var/lib/apt/lists/* &&\
    pip install --no-cache-dir -r requirements.txt &&\
    apt-get remove -y build-essential &&\
    apt-get autoremove -y


COPY alembic alembic
COPY application application
COPY alembic.ini start_server.sh ./

RUN chmod +x ./start_server.sh


ENTRYPOINT [ "./start_server.sh" ]