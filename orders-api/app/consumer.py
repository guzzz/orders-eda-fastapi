import os
import pika
import json
import sys
sys.path.append(os.path.realpath('..'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.database import get_db
from app.services.user_service import UserService

amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue="orders")

SQLALCHEMY_DATABASE_URL: str = os.getenv("POSTGRESQL_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DB = SessionLocal()

user_service = UserService()

def callback(ch, method, properties, body):
    print("Received in ORDERS-API")

    data = json.loads(body)
    action = data.get("action")
    user_id = data.get("user_id")
    body_json = data.get("body")

    if action == "create":
        user_service.eda_create(DB, body_json)
    elif action == "update":
        user_service.eda_update(DB, user_id, body_json)
    elif action == "delete":
        user_service.eda_delete(DB, user_id)
    else:
        pass 

channel.basic_consume(queue="orders", on_message_callback=callback, auto_ack=True)
print("ORDERS-API queue up!")
channel.start_consuming()
channel.close()
