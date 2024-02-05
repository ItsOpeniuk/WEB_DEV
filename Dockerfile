FROM python:3.11

RUN pip install poetry

WORKDIR /app

COPY . /app

RUN poetry install

CMD ["poetry", "run", "python", "src/main.py"]
