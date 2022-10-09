FROM python:3.10-slim

EXPOSE 5000

ENV PYTHONPATH=/opt/application \
    MYSQL_PORT=3306 \
    MYSQL_DATABASE= \
    MYSQL_USER= \
    MYSQL_PASSWORD= \
    MYSQL_HOST=

RUN apt update\
    && apt install -y  default-libmysqlclient-dev  gcc

RUN pip install \
    flask==2.2.2 \
    flask-sqlalchemy==3.0.0 \
    werkzeug==2.2.2 \
    uuid==1.30 \
    pyjwt==2.5.0 \
    mysqlclient==2.1.1


WORKDIR /opt/application
COPY flask-api /opt/application

HEALTHCHECK CMD curl -f http://localhost:5000/ || exit 1
ENTRYPOINT ["python", "main.py"]
