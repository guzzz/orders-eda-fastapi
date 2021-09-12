#!/bin/bash
.PHONY: default
.SILENT:


default:

shell:
	docker-compose stop api_users
	docker-compose run --rm --service-ports api_users bash

start:
	docker-compose up -d
	docker-compose up -d mongo-express

start_api:
	docker-compose up -d
	docker-compose stop api_users
	docker-compose run --rm --service-ports api_users

stop:
	docker-compose down

build:
	docker-compose build --force-rm --no-cache --pull

clean:
	make stop
	docker image rm $$(docker image ls -q -f reference=users_api)

setup:
	docker network create users-network
	make build
	make start
	docker-compose up -d mongo-express

logs:
	docker-compose logs -f

logs_api:
	docker-compose logs -f api_users

test:
	docker-compose up -d
	docker-compose stop api_users
	docker-compose run --rm api_users pytest
