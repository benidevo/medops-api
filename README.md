# MedOps API

[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Testing

A test account has been created for testing purposes. The details are as follows:

- email: john@example.com
- password: TestPassword
- The API documentation is available on `http://localhost:8000/docs` on your browser.

![Screenshot](image.png?raw=true "MedOps API")

## Technologies

- [Python 3.10](https://python.org): Base programming language for development
- [PostgreSQL](https://www.postgresql.org/): Application relational databases for development, staging and production environments
- [Django Framework](https://www.djangoproject.com/): Development framework used for the application
- [Django Rest Framework](https://www.django-rest-framework.org/) : Provides API development tools for easy API development
- [Celery](https://github.com/celery/celery): A simple, flexible, and reliable distributed system to process vast amounts of tasks
- [Redis](https://github.com/redis/redis-py): A NoSQL Database that serves as Cache, Celery Broker and Result Backend
- [SendGrid](https://sendgrid.com/): An Email Service Provider for sending emails
- [Docker Engine and Docker Compose](https://www.docker.com/) : Containerization of the application and services orchestration

## How To Start App

- Clone the Repository
- create a .env file with the variables in the .env.example file
  - `cp .env.example .env`
  - You will also need to create an account with [SendGrid](https://sendgrid.com/) and get an API Key. You will need to add this to the .env file
  - Symptoms and diagnosis data are gotten from [APIMedic](https://apimedic.com/apikeys). You will need to create an account and get an API Key. You will need to add this to the .env file

- Run `make build-dev`

  - Running the above command for the first time will download all docker-images and third party packages needed for the app.
  - **NB: This will take several minutes for the first build**

- Run `make up-dev`

  - Running the above command will Start up the following Servers:
    - Postgres Server --> http://localhost:5432
    - Django Development Server --> http://localhost:8000
    - Redis Server --> http://localhost:6379

- Run `make down-dev` to stop the servers

- Run `make test` to run tests

- Other commands can be found in the Makefile

## Exploring The App

Make sure that all the above servers are running before you start exploring the project.

### MedOps

MedOps is a simple application that allows users to get diagnosis for their symptoms. It also recommends a list of doctors based on the diagnosis.

### Key Features

1. Users can create an account and login to the application
2. Users can get a list of symptoms
3. Users can get a list of diagnosis based on the symptoms they select
4. Medical doctors are recommended based on the diagnosis
