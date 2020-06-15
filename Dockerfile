FROM python:3.7

WORKDIR /code/
COPY ./ ./

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install vim -y
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install psycopg2 && \
    pip install daphne


ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=webservice.settings

EXPOSE 8000/TCP

CMD ["./init.sh", "daphne", "--bind 0.0.0.0", "--port 8000", "webservice.asgi:application"]
