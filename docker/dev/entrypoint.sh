#!/bin/sh

if [ -z ${LOG_LEVEL} ]; then
export LOG_LEVEL="info"
fi

if [ -z ${HTTP_PORT} ]; then
export HTTP_PORT=":8000"
fi
if [ -z ${HTTP_WORKERS} ]; then
export HTTP_WORKERS=2
fi

# wait for postgres
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done

echo "Initializing DB..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
status=$?
if [ $status -eq 0 ]; then
  echo "Starting Gunicorn..."

  gunicorn --workers $HTTP_WORKERS \
           --worker-class=gthread \
           --reload core.wsgi \
          -b $HTTP_PORT \
          --timeout 120 \
          --log-level $LOG_LEVEL
else
  echo "Error initializing DB, exiting..."
fi
