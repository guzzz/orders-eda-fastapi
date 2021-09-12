import os
import pika
import json

from fastapi.encoders import jsonable_encoder


amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(action, body={}, user_id=None):
    print("==> Sending from USERS-API")
    try:
        data = {}
        data["action"] = action
        data["body"] = jsonable_encoder(body)
        data["user_id"] = user_id

        properties = pika.BasicProperties(content_type="application/json")
        channel.basic_publish(exchange="", routing_key="orders", body=json.dumps(data), properties=properties)
    except Exception as exc:
        print(f"==> ERROR: {exc} - Please restart queue link")
