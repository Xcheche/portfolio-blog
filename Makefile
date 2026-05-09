.PHONY: help build up down logs exec migrate

help:
	@echo "Portfolio Blog"
	@echo ""
	@echo "Usage:"
	@echo "  make build      Build Docker image (BUILD_NO_CACHE=true for full rebuild)"
	@echo "  make up         Start services with docker-compose"
	@echo "  make down       Stop services"
	@echo "  make logs       Follow app logs"
	@echo "  make exec       Open shell in app container"
	@echo "  make migrate    Run Django migrations"

build:
	docker build $(if $(filter true,$(BUILD_NO_CACHE)),--no-cache) -t portfolio-blog:latest .

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f app

exec:
	docker compose exec app /bin/bash

migrate:
	docker compose exec app python manage.py migrate

makemigrations:
	docker compose exec app python manage.py makemigrations

which-settings:
	docker compose exec app python manage.py shell -c "from django.conf import settings; print(settings.SETTINGS_MODULE)"

create-superuser:
	docker compose exec app python manage.py createsuperuser

collect-static:
	docker compose exec app python manage.py collectstatic --noinput
