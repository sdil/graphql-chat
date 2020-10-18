FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirement.txt /app

RUN pip install -r requirement.txt

COPY . /app
WORKDIR /app

