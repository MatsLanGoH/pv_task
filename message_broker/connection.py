"""
Module to establish connection with message broker
"""

from pika import (
    BlockingConnection,
    ConnectionParameters,
)
from pika.exceptions import AMQPConnectionError
from retry import retry


class ConnectionManager:
    def __init__(self, broker_host: str, queue: str):
        self.broker_host = broker_host
        self.queue = queue

    @retry(AMQPConnectionError, delay=5, jitter=(1, 3))
    def start_channel(self):
        connection = BlockingConnection(ConnectionParameters(self.broker_host))
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.queue_declare(queue=self.queue, durable=True)

        return channel
