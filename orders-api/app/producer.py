import os
import pika
import json


amqp_url: str = os.getenv("AMQP_URL")
params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    print("==> Sending from ORDERS-API")
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="", routing_key="users", body=json.dumps(body), properties=properties
    )
