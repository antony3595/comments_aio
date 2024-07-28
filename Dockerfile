FROM python:3.10.14-alpine3.20
ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN apk --no-cache add  bash
COPY requirements.txt .

RUN python -m  pip install -r requirements.txt

COPY . .
RUN pwd
RUN ls -la

CMD ["echo", "Specify the command to run at the docker-compose.yml file"]