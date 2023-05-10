FROM python:3.11-slim

EXPOSE 8081/tcp

RUN pip install poetry

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.in-project true
RUN poetry install

CMD ["python", "main.py"]