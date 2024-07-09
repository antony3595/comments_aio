FROM python:3.10.14-alpine3.20
ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN apk --no-cache add  bash
COPY requirements.txt .

RUN python -m  pip install -r requirements.txt

COPY docker/supervisord.conf /etc/supervisord.conf
COPY . .
RUN pwd
RUN ls -la

CMD ["supervisord", "-c", "/etc/supervisord.conf"]