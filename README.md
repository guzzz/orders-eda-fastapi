<p align="center">

![alt text](https://i.imgur.com/spLv8IN.png)

</p>

<p align="center">
<img src="https://img.shields.io/badge/docker-20.10.08-blue"/>
<img src="https://img.shields.io/badge/docker--compose-1.29.2-9cf"/>
<img src="https://img.shields.io/badge/python-3.8-yellowgreen"/>
<img src="https://img.shields.io/badge/framework-fastAPI-brightgreen"/>
<img src="https://img.shields.io/badge/mongo-5.0.2--focal-green"/>
<img src="https://img.shields.io/badge/postgres-13.4-lightgrey"/>
<img src="https://img.shields.io/badge/redis-6.2.5--alpine-red"/>
</p>

---

<h1 align="center">
   🚀 Orders EDA FastAPI
</h1>
<p align="center">
    <em>
    Decentralized system for registration and management of users and orders
    </em>
</p>

---

Summary
=================

   * [The project](#the-project)
   * [Specifications](#specifications)
   * [Swagger (OpenAPI)](#swagger-openapi)
   * [Endpoints](#endpoints-users-api)
      * [users-api](#endpoints-users-api)
      * [orders-api](#endpoints-orders-api)
   * [Makefile](#makefile)
   * [Run Locally](#run-locally)
   * [Tests](#tests)
   * [Requirements](#requirements)

---

## The project

The main features of the system are:

1. Users creation. The data inputs of each user are: name, cpf, email, phone_number.
2. Orders creation. The data inputs of each order are: item_description, item_quantity, item_price, user_id.
3. Edit, list and delete users.
4. Edit, list and delete orders.
5. List orders filtered by user.

Obs.: In addition to these, some other features were included, such as: encrypted user data, cache layers, paging listing and configurable page size.

---

## Specifications

This project uses event driven architecture (EDA).

The system consists of:

1. API Python FastAPI + MongoDB.
2. API Python FastAPI + PostgreSQL.
3. Redis layers for both APIs.
4. Broker RabbitMQ.
5. Docker + Docker-compose.

Organization:

1. users-api:

API responsible for managing users. User-related activities generate events that seek to keep user data in the orders-api consistent.

2. orders-api:

API responsible for order management.

---

## Swagger (OpenAPI)

Both APIs uses fastAPI, so they are documented with OpenAPI. The projects documentation can be found in the "/docs" and "/redoc" endpoints.

* users-api: http://localhost:8000/docs
* orders-api: http://localhost:8001/docs

---

## Endpoints users-api

1. **(GET)** **_"/v0/users/"_** - *Returns all users registered.*
2. **(POST)** **_"/v0/users/"_** - *Register a new user.*
3. **(GET)** **_"/v0/users/{uuid}"_** - *Returns a specific user.*
4. **(PUT)** **_"/v0/users/{uuid}"_** - *Updates a specific user.*
5. **(DELETE)** **_"/v0/users/{uuid}"_** - *Deletes one user.*


#### Specifications

1. The endpoint for listing users have 2 additional parameters that can be sent in the headers in order to paginate the results:

* page ( page number )
* limit ( page size )

2. The users model uses UUID.

3. All stored sensitive data and all data in transit are encrypted.

_Obs._: It runs in: http://localhost:8000/

---

## Endpoints orders-api

1. **(GET)** **_"/v0/users/"_** - *Returns all users registered.*
3. **(GET)** **_"/v0/users/{uuid}"_** - *Returns a specific user.*
3. **(GET)** **_"/v0/orders/"_** - *Returns all orders registered.*
4. **(POST)** **_"/v0/orders/"_** - *Register a new order.*
5. **(GET)** **_"/v0/orders/{uuid}"_** - *Returns a specific order.*
6. **(PUT)** **_"/v0/orders/{uuid}"_** - **Updates a specific order.*
7. **(DELETE)** **_"/v0/orders/{uuid}"_** - *Deletes one order.*


#### Specifications

1. The endpoint for listing users and orders have 2 additional parameters that can be sent in the headers in order to paginate the results. (Same as users-api)
2. The orders and users models uses UUID.
3. All stored sensitive data is encrypted.
4. It's possible to use an additional query param __user_api__ in order to **filter orders by users** in the listing orders endpoint.

_Obs._: It runs in: http://localhost:8001/

---

## Makefile

Both APIs have a _Makefile_ in their root. However, in this project root there is this third _Makefile_ to facilitate the entire system usage. The main commands are:

* **_make setup_**: Setup the entire environment to run the projects. Only need to use this command once.
* **_make stop_**: Stop all containers.
* **_make start_**: Create containers and run the API's.
* **_make test_**: Run all tests.
* **_make clear_**: Clean this project's containers, images, volumes and network from your computer. It's recommended to read this Makefile command before you use it, to make sure that you do not have other projects with similar names.

---

## Run Locally

1. Make sure you have the Docker and Docker-compose installed.
2. Go into the **.env-example** and generate your own vars: [CRYPTOGRAPHY_KEY](https://8gwifi.org/fernet.jsp) and [AMQP_URL](https://www.cloudamqp.com) .
3. In the first time running the project (and just in the first one) you will have to use the command **make setup** .
3. Next time, you will just have to use **make start** and **make stop** commands.

* Each API have their own Makefile archive, in case you want to run each project individually.
* The command **make logs_api** and **make logs** helps to visualize the system logs.

---

## Tests

==> There are 34 tests being tested in this project. The characteristics of this tests can be readden below:

1. [orders-api] Thirteen tests running in the orders area.
2. [orders-api] Thirteen tests running in the users area.
3. [users-api] Eight tests running in the users app.

* To test the system, just run the command **make test** ( remembering that if it is the first time to run the project, the command "make setup" must run first )

---

## Requirements

* **DOCKER-COMPOSE**: 1.29.2
* **DOCKER**: 20.10.08
