.EXPORT_ALL_VARIABLES:
PROJECT ?= "dish-service"
export PYTHONPATH := $(shell pwd):$(PYTHONPATH)


up_all:
	docker-compose -p ${PROJECT} up -d

alembic_upgrade:
	docker-compose -p {PROJECT} run --rm srv alembic upgrade head

alembic_revision:
	docker-compose -p ${PROJECT} run --rm --no-deps srv alembic revision --autogenerate -m "${MESSAGE}"