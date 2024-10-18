.EXPORT_ALL_VARIABLES:
PROJECT ?= "dish-service"
export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

build:
	docker-compose -p ${PROJECT} build $(SERVICE)

up:
	docker-compose -p ${PROJECT} up -d $(SERVICE)

restart:
	docker-compose -p ${PROJECT} restart $(SERVICE)

stop:
	docker-compose -p ${PROJECT} stop $(SERVICE)

db_upgrade:
	docker-compose -p ${PROJECT} run --rm srv alembic upgrade head

db_revision:
	docker-compose -p ${PROJECT} run --rm srv alembic revision --autogenerate -m "${MESSAGE}"

db_downgrade:
	docker-compose -p ${PROJECT} run --rm srv alembic downgrade -1