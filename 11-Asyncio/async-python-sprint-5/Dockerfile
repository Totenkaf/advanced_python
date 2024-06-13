FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .

COPY ./.env .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./src .
