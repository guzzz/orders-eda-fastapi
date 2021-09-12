#!/bin/bash
.PHONY: default
.SILENT:


default:

shell:
	docker-compose stop api_orders
	docker-compose run --rm --service-ports api_orders bash

start:
	docker-compose up -d

start_api:
	docker-compose up -d
	docker-compose stop api_orders
	docker-compose run --rm --service-ports api_orders

stop:
	docker-compose down

build:
	docker-compose build --force-rm --no-cache --pull

clean:
	make stop
	docker image rm $$(docker image ls -q -f reference=orders_api)

setup:
	docker network create orders-network
	make build
	make start

logs:
	docker-compose logs -f

logs_api:
	docker-compose logs -f api_orders

test:
	docker-compose up -d
	docker-compose stop api_orders
	docker-compose run --rm api_orders pytest
