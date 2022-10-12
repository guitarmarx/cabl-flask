FROM python:3.10-slim

EXPOSE 5000

ENV PYTHONPATH=/opt/application \
    MYSQL_PORT=3306 \
    MYSQL_DATABASE= \
    MYSQL_USER= \
    MYSQL_PASSWORD= \
    MYSQL_HOST= \
    CABL_DEFAULT_LOCATION= \
    CABL_ADMIN_EMAIL="admin@email.de" \
    CABL_ADMIN_PASSWORD="admin"

RUN apt update \
    && apt install -y  default-libmysqlclient-dev  gcc

WORKDIR /opt/application
COPY requirements.txt /tmp/requirements.txt
COPY flask-api /opt/application

RUN pip install -r /tmp/requirements.txt

HEALTHCHECK CMD curl -f http://localhost:5000/ || exit 1
ENTRYPOINT ["python", "main.py"]
