#!/bin/bash
.PHONY: default
.SILENT:


default:

start:
	make startusers
	make startorders

startusers:
	cd users-api; \
	make start

startorders:
	cd orders-api; \
	make start

stop:
	make stopusers
	make stoporders

stopusers:	
	cd users-api; \
	make stop

stoporders:
	cd orders-api; \
	make stop

setup:
	make setupusers
	make setuporders

setupusers:
	cp .env-example users-api/.env
	cd users-api; \
	make setup

setuporders:
	cp .env-example orders-api/.env
	cd orders-api; \
	make setup

test:
	make testusers
	make testorders

testusers:
	make startusers
	cd users-api; \
	docker-compose stop api_users; \
	docker-compose run --rm api_users pytest; \
	docker-compose stop api_users; \
	docker-compose up -d api_users; \

testorders:
	make startorders
	cd orders-api; \
	docker-compose stop api_orders; \
	docker-compose run --rm api_orders pytest; \
	docker-compose stop api_orders; \
	docker-compose up -d api_orders; \

clear:
	make stop
	docker network rm orders-network users-network
	docker volume rm mongodb-data postgres-data postgres-data-teste