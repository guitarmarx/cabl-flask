FROM python:3.10-slim

LABEL MAINTAINER="meteorit GbR"
EXPOSE 5000

ENV PYTHONPATH=/opt/application \
    TZ=Europe/Berlin \
    DB_PORT=3306 \
    DB_NAME=jobs \
    DB_USER=jobs \
    DB_PASSWORD=jobs \
    DB_HOST=localhost

RUN apt update \
    && apt install -y curl \
    gcc \
    git \
    musl-dev \
    tzdata

RUN pip install docker \
    flask==2.1.2 \
    flask-cors==3.0.10 \
    flask-httpauth==4.6.0 \
    Flask-Migrate==3.1.0 \
    flask-restx==0.5.1 \
    Flask-Script==2.0.6 \
    flask-sqlalchemy==2.5.1 \
    psycopg2-binary \
    requests==2.27.1 \
    flask-praetorian==1.3.0 \
	greenlet==1.1.2 \
	werkzeug==2.1.2

WORKDIR /opt/application
COPY application /opt/application

HEALTHCHECK CMD curl -f http://localhost:5000/ || exit 1
ENTRYPOINT ["python", "app.py"]
