build:
	docker-compose -f docker-compose-prod.yml up --build -d --remove-orphans
build-dev:
	docker-compose -f docker-compose.yml build

up:
	docker-compose -f docker-compose-prod.yml up -d
up-dev:
	docker-compose -f docker-compose.yml up

down:
	docker-compose -f docker-compose-prod.yml down
down-dev:
	docker-compose -f docker-compose.yml down

down_volumes:
	docker-compose -f docker-compose-prod.yml down -v
down-dev_volumes:
	docker-compose -f docker-compose.yml down -v

show_logs:
	docker-compose -f docker-compose-prod.yml logs
show_logs-dev:
	docker-compose -f docker-compose.yml logs

superuser:
	docker-compose -f docker-compose-prod.yml run --rm api python3 manage.py createsuperuser
superuser-dev:
	docker-compose -f docker-compose.yml run --rm api python3 manage.py createsuperuser

black-check:
	docker-compose -f docker-compose.yml exec api black --check --exclude=migrations --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .
black-diff:
	docker-compose -f docker-compose.yml exec api black --diff --exclude=migrations --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .
black:
	docker-compose -f docker-compose.yml exec api black --exclude=migrations --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .

isort-check:
	docker-compose -f docker-compose.yml exec api isort . --check-only --skip /app/env --skip migrations --skip /app/venv
isort-diff:
	docker-compose -f docker-compose.yml exec api isort . --diff --skip /app/env --skip migrations --skip /app/venv
isort:
	docker-compose -f docker-compose.yml exec api isort . --skip /app/env --skip migrations --skip /app/venv

test:
	docker-compose -f docker-compose.yml exec api pytest $(TEST_PATH)
test-cov:
	docker-compose -f docker-compose.yml exec api find . -name "*.pyc" -delete && docker-compose -f docker-compose.yml exec api coverage report
test-cov-html:
	docker-compose -f docker-compose.yml exec api find . -name "*.pyc" -delete && docker-compose -f docker-compose.yml exec api coverage html
