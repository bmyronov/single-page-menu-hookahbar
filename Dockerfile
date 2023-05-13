FROM python:3.11

RUN mkdir /app 

WORKDIR /app

COPY . .
COPY pyproject.toml .

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev