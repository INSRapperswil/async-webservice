# Async Webservice

A simple webservice which allows to create and start tasks using a REST-API and get notified about changes using websockets.

## Installation

Install the requirements:

    python -m venv env
    env/bin/pip install -r requirements.txt

## Running

Start redis:

    docker run --name redis -p 6379:6379 -d redis

Create a superuser:

    env/bin/python manage.py migrate
    env/bin/python manage.py createsuperuser

Start the celery worker:

    env/bin/celery -A webservice worker

Start celery beat:

    env/bin/celery -A webservice beat

Start the webserver:

    env/bin/python manage.py runserver


Now you can browse:
- The updates (websocket): http://127.0.0.1:8000/updates
- The API: http://127.0.0.1:8000/api/tasks
- The admin UI: http://127.0.0.1:8000/admin

## Testing

Run the tests:

    env/bin/py.test

## Dockerization

Build the webservice:

    docker-compose build --no-cache webservice
    docker build  --tag nettowel_orchestrator_zrh:latest .

Start the containers:

    docker-compose up

Create a superuser:

    docker-compose exec webservice python manage.py createsuperuser

Now you can browse:
- Backend: http://localhost:8000/
- Adminer: http://localhost:8080/
- Flower: http://localhost:5555/
