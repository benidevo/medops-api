FROM python:3.10-slim-bullseye

WORKDIR /app
EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y --no-install-recommends install netcat

RUN pip install --upgrade pip
COPY ./requirements ./requirements
RUN pip install psycopg2-binary
RUN pip install -r requirements/dev.txt

COPY . .

CMD ["sh", "entrypoint.sh"]
