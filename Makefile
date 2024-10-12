.EXPORT_ALL_VARIABLES:
PROJECT ?= "dish-service"
export PYTHONPATH := $(shell pwd):$(PYTHONPATH)


up_all:
	docker-compose -p ${PROJECT} up -d

alembic_upgrade:
	docker-compose -p {PROJECT} run --rm srv alembic upgrade head

alembic_revision:
	docker-compose -p ${PROJECT} run --rm srv alembic revision --autogenerate -m "${MESSAGE}"

alembic_downgrade:
	docker-compose -p ${PROJECT} run --rm srv alembic downgrade -1