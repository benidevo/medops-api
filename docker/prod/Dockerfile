FROM python:3.10-slim-bullseye

WORKDIR /app
EXPOSE 80

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y --no-install-recommends install netcat && apt-get install -y build-essential libpq-dev


RUN pip install --upgrade pip
COPY ./requirements ./requirements
RUN pip install psycopg2-binary --no-binary psycopg2-binary
RUN pip install -r requirements/prod.txt
COPY ./docker/prod/entrypoint.sh /entrypoint.sh

COPY . .

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
